"""
API Utilities — Flux
Handles all external API calls with error handling and caching
"""

import aiohttp
import logging
import asyncio
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import json
import matplotlib.dates as mdates
from datetime import datetime, timezone
import io

import config
from cache import get_cache, get_rate_limiter, cache_key

logger = logging.getLogger(__name__)


# ============================================================================
# COINGECKO API - PRICE CHARTS
# ============================================================================

async def fetch_price_chart(
    coin_id: str,
    vs_currency: str = "usd",
    days: int = 1,
    use_cache: bool = True
) -> Optional[io.BytesIO]:
    """
    Fetch 24h price chart for a cryptocurrency from Render service
    
    Args:
        coin_id: Coin ID (e.g., 'internet-computer')
        vs_currency: Kept for compatibility, not used by Render API
        days: Kept for compatibility, not used by Render API
        use_cache: Use in-memory cache (default: True)
    
    Returns:
        BytesIO object containing PNG chart data
    """
    
    # Check cache first
    cache_key_str = cache_key(coin_id, "render_chart")
    if use_cache:
        cached = get_cache().get(cache_key_str)
        if cached:
            logger.info(f"📊 Using cached chart for {coin_id}")
            return cached
    
    try:
        # Fetch data directly from Render API (No rate limits)
        url = f"https://cryptweb.onrender.com/api/charts/{coin_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=config.COINGECKO_TIMEOUT) as resp:
                if resp.status != 200:
                    logger.error(f"❌ Chart API error: {resp.status}")
                    return None

                data = await resp.json()
        print(f"Received chart data for {coin_id}: {data}")
        prices = data.get("data")
        if not prices:
            logger.warning(f"⚠️ No price data for {coin_id}")
            return None
        
        # Generate chart
        chart = _generate_chart(coin_id, prices)
        
        # Cache the chart
        if use_cache and chart:
            get_cache().set(cache_key_str, chart)
        
        return chart
    
    except asyncio.TimeoutError:
        logger.error(f"⏱️ Timeout fetching chart for {coin_id}")
        return None
    except Exception as e:
        logger.error(f"❌ Chart fetch error for {coin_id}: {e}")
        return None


def _generate_chart(coin_name: str, prices: List[List[float]]) -> io.BytesIO:
    try:
        times = [
            datetime.fromtimestamp(p[0] / 1000.0, tz=timezone.utc)
            for p in prices
        ]
        values = [p[1] for p in prices]
        
        is_up = values[-1] >= values[0]
        color = config.COLORS["success"] if is_up else config.COLORS["danger"]
        trend_emoji = "📈" if is_up else "📉"
        
        bg = config.COLORS["dark"]
        grid_c = config.COLORS["grid"]
        muted = config.COLORS["muted"]
        accent = config.COLORS["accent"]
        
        fig, ax = plt.subplots(figsize=(10, 5), facecolor=bg)
        ax.set_facecolor(bg)
        
        ax.plot(times, values, color=color, linewidth=2.5, zorder=5)
        ax.fill_between(
            times, values, min(values) * 0.98,
            color=color, alpha=0.08, zorder=2
        )
        ax.fill_between(
            times, values, min(values) * 0.98,
            color=color, alpha=0.12, zorder=3,
            interpolate=True
        )
        
        title = f"{trend_emoji}  {coin_name.upper()}  ·  24H"
        ax.set_title(title, color="white", pad=20, fontsize=15, fontweight="bold", loc="left")
        ax.grid(True, color=grid_c, linestyle="-", alpha=0.3, linewidth=0.5)
        
        ax.tick_params(colors=muted, which="both", labelsize=9)
        for spine in ax.spines.values():
            spine.set_color(grid_c)
            spine.set_linewidth(0.3)
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha="center")
        
        min_y, max_y = min(values), max(values)
        ax.set_ylim(min_y * 0.97, max_y * 1.03)
        
        buf = io.BytesIO()
        plt.savefig(
            buf, format="png", bbox_inches="tight", dpi=120,
            facecolor=bg, edgecolor="none",
            transparent=False
        )
        buf.seek(0)
        plt.close("all")
        
        logger.info(f"✅ Chart generated for {coin_name}")
        return buf
    
    except Exception as e:
        logger.error(f"❌ Chart generation error: {e}")
        plt.close("all")
        return None


# ============================================================================
# COINGECKO API - PRICE DATA
# ============================================================================

async def fetch_price_data(coin_id: str, vs_currency: str = "usd") -> Optional[Dict[str, Any]]:
    """
    Fetch current price and market data for a coin
    
    Args:
        coin_id: CoinGecko coin ID
        vs_currency: Target currency
    
    Returns:
        Dict with price, market_cap, volume, change, etc.
    """
    
    try:
        # Rate limiting
        limiter = get_rate_limiter()
        await limiter.wait_if_needed()
        
        url = (
            f"{config.COINGECKO_API_BASE}/coins/markets"
            f"?vs_currency={vs_currency}&ids={coin_id}"
            f"&order=market_cap_desc&per_page=1"
        )
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=config.COINGECKO_TIMEOUT) as resp:
                if resp.status != 200:
                    logger.error(f"❌ Price API error: {resp.status}")
                    return None
                
                data = await resp.json()
                if data:
                    logger.debug(f"✅ Price data fetched for {coin_id}")
                    return data[0]
        
        return None
    
    except asyncio.TimeoutError:
        logger.error(f"⏱️ Timeout fetching price for {coin_id}")
        return None
    except Exception as e:
        logger.error(f"❌ Price fetch error: {e}")
        return None


# ============================================================================
# COINDESK API - NEWS
# ============================================================================

async def fetch_crypto_news(limit: int = 5) -> List[Dict[str, str]]:
    """
    Fetch latest crypto news from CoinDesk RSS feed
    
    Args:
        limit: Maximum number of articles to fetch
    
    Returns:
        List of dicts with 'title' and 'link'
    """
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                config.COINDESK_NEWS_URL,
                timeout=config.COINDESK_TIMEOUT
            ) as resp:
                if resp.status != 200:
                    logger.error(f"❌ News API error: {resp.status}")
                    return []
                
                content = await resp.read()
        
        # Parse RSS
        root = ET.fromstring(content)
        news = []
        
        for item in root.findall(".//item")[:limit]:
            title = item.findtext("title", default="Untitled")
            link = item.findtext("link", default="")
            
            if title and link:
                news.append({
                    "title": title.strip(),
                    "link": link.strip(),
                    "source": "CoinDesk"
                })
        
        logger.info(f"✅ Fetched {len(news)} news articles")
        return news
    
    except asyncio.TimeoutError:
        logger.error("⏱️ Timeout fetching news")
        return []
    except Exception as e:
        logger.error(f"❌ News fetch error: {e}")
        return []


# ============================================================================
# AI SUMMARIZATION (GROQ)
# ============================================================================

async def scrape_and_summarize(url: str) -> Optional[str]:
    """Scrape article and summarize using Groq API"""
    if not config.GROQ_API:
        logger.warning("⚠️ GROQ_API not set, skipping summarization")
        return None
        
    try:
        # 1. Scrape content
        headers_scrape = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers_scrape, timeout=10) as resp:
                if resp.status != 200:
                    return None
                html = await resp.text()
                
        soup = BeautifulSoup(html, "html.parser")
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator=' ')
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Truncate to avoid huge prompts (first 4000 chars is usually enough for a summary)
        text = text[:4000]
        
        # 2. Summarize with Groq
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.GROQ_API}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a professional financial news summarizer. Provide a highly concise, neutral 1-2 sentence summary of the following article. Do not use hype words like 'rocket' or 'moon'. Do not give financial advice. Output ONLY the summary text."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            "max_tokens": 150
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(groq_url, headers=headers, json=data, timeout=15) as resp:
                if resp.status != 200:
                    logger.error(f"❌ Groq API error: {resp.status} {await resp.text()}")
                    return None
                
                result = await resp.json()
                summary = result["choices"][0]["message"]["content"].strip()
                return summary
                
    except Exception as e:
        logger.error(f"❌ Scrape/Summarize error for {url}: {e}")
        return None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_large_number(num: float) -> str:
    """Format large numbers with readable units"""
    if num is None or num == 0:
        return "N/A"
    
    if num >= 1_000_000_000_000:
        return f"${num / 1_000_000_000_000:.2f}T"
    elif num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num / 1_000:,.2f}K"
    else:
        return f"${num:,.2f}"


def format_price(price: float, symbol: str = "$") -> str:
    """Format price with appropriate decimal places"""
    if price is None:
        return "N/A"
    
    if price >= 1:
        return f"{symbol}{price:,.2f}"
    else:
        # Show more decimals for small prices
        return f"{symbol}{price:.8f}".rstrip("0").rstrip(".")


def get_trend_emoji(change: Optional[float]) -> str:
    """Get emoji based on percentage change"""
    if change is None:
        return "➡️"
    elif change > 0:
        return "📈"
    elif change < 0:
        return "📉"
    else:
        return "➡️"
