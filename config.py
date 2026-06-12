"""
Configuration & Constants
Flux — Real-time Crypto Intelligence
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
load_dotenv()

# ============================================================================
# BOT CONFIG
# ============================================================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_NAME = "Flux"
GROQ_API = os.getenv("GROQ_API", "")

# ============================================================================
# REDIS CONFIG (FOR REAL-TIME PRICES)
REDIS_URL = os.getenv("REDIS_URL", "")
REDIS_PRICE_KEY = "market_prices"

# ============================================================================
# API ENDPOINTS & TIMEOUTS
# ============================================================================
COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"
COINGECKO_TIMEOUT = 8  # seconds
COINGECKO_CHART_DAYS = 1  # 24-hour chart

COINDESK_NEWS_URL = "https://www.coindesk.com/arc/outboundfeeds/rss/"
COINDESK_TIMEOUT = 8
COINDESK_NEWS_LIMIT = 5

# ============================================================================
# CACHE CONFIG
# ============================================================================
CHART_CACHE_TTL = 1000  # Update every 15 minutes (1000 seconds)
MAX_CHART_CACHE_SIZE = 50  # Keep cache for max 50 coins

# ============================================================================
# DATABASE CONFIG
# ============================================================================
DB_FILE_NAME = "data.json"

# ============================================================================
# SUPPORTED CRYPTOCURRENCIES
# ============================================================================
SUPPORTED_COINS: Dict[str, Dict[str, str]] = {
    "BTC": {"id": "bitcoin", "name": "Bitcoin", "emoji": "₿"},
    "ETH": {"id": "ethereum", "name": "Ethereum", "emoji": "Ξ"},
    "USDT": {"id": "tether", "name": "Tether", "emoji": "₮"},
    "BNB": {"id": "binancecoin", "name": "BNB", "emoji": "⬟"},
    "SOL": {"id": "solana", "name": "Solana", "emoji": "◎"},
    "XRP": {"id": "ripple", "name": "XRP", "emoji": "✕"},
    "USDC": {"id": "usd-coin", "name": "USDC", "emoji": "💵"},
    "STETH": {"id": "staked-ether", "name": "Lido Staked Ether", "emoji": "💧"},
    "DOGE": {"id": "dogecoin", "name": "Dogecoin", "emoji": "Ð"},
    "ADA": {"id": "cardano", "name": "Cardano", "emoji": "₳"},
    "TRX": {"id": "tron", "name": "TRON", "emoji": "T"},
    "SHIB": {"id": "shiba-inu", "name": "Shiba Inu", "emoji": "🐕"},
    "AVAX": {"id": "avalanche-2", "name": "Avalanche", "emoji": "▲"},
    "LINK": {"id": "chainlink", "name": "Chainlink", "emoji": "🔗"},
    "BCH": {"id": "bitcoin-cash", "name": "Bitcoin Cash", "emoji": "₿"},
    "DOT": {"id": "polkadot", "name": "Polkadot", "emoji": "●"},
    "NEAR": {"id": "near", "name": "NEAR Protocol", "emoji": "Ⓝ"},
    "LTC": {"id": "litecoin", "name": "Litecoin", "emoji": "Ł"},
    "UNI": {"id": "uniswap", "name": "Uniswap", "emoji": "🦄"},
    "DAI": {"id": "dai", "name": "Dai", "emoji": "🟡"},
    "WBTC": {"id": "wrapped-bitcoin", "name": "Wrapped Bitcoin", "emoji": "Wrapped ₿"},
    "POL": {"id": "polygon-ecosystem-token", "name": "POL (ex-MATIC)", "emoji": "🪙"},
    "ICP": {"id": "internet-computer", "name": "Internet Computer", "emoji": "∞"},
    "ETC": {"id": "ethereum-classic", "name": "Ethereum Classic", "emoji": "⟠"},
    "HBAR": {"id": "hedera-hashgraph", "name": "Hedera", "emoji": "ℏ"},
    "XLM": {"id": "stellar", "name": "Stellar", "emoji": "⭐"},
    "ATOM": {"id": "cosmos", "name": "Cosmos Hub", "emoji": "⚛️"},
    "XMR": {"id": "monero", "name": "Monero", "emoji": "Ⓜ️"},
    "OKB": {"id": "okb", "name": "OKB", "emoji": "🪙"},
    "FIL": {"id": "filecoin", "name": "Filecoin", "emoji": "🪙"},
    "LDO": {"id": "lido-dao", "name": "Lido DAO", "emoji": "🪙"},
    "ARB": {"id": "arbitrum", "name": "Arbitrum", "emoji": "🪙"},
    "OP": {"id": "optimism", "name": "Optimism", "emoji": "🪙"},
    "APT": {"id": "aptos", "name": "Aptos", "emoji": "🪙"},
    "VET": {"id": "vechain", "name": "VeChain", "emoji": "🪙"},
    "AAVE": {"id": "aave", "name": "Aave", "emoji": "🪙"},
    "GRT": {"id": "the-graph", "name": "The Graph", "emoji": "🪙"},
    "MKR": {"id": "maker", "name": "Maker", "emoji": "🪙"},
    "ALGO": {"id": "algorand", "name": "Algorand", "emoji": "🪙"},
    "RENDER": {"id": "render-token", "name": "Render", "emoji": "🪙"},
    "INJ": {"id": "injective-protocol", "name": "Injective", "emoji": "🪙"},
    "RPL": {"id": "rocket-pool", "name": "Rocket Pool", "emoji": "🪙"},
    "KAS": {"id": "kaspa", "name": "Kaspa", "emoji": "🪙"},
    "BONK": {"id": "bonk", "name": "Bonk", "emoji": "🪙"},
    "SEI": {"id": "sei-network", "name": "Sei", "emoji": "🪙"},
    "TIA": {"id": "celestia", "name": "Celestia", "emoji": "🪙"},
    "SUI": {"id": "sui", "name": "Sui", "emoji": "🪙"},
    "WLD": {"id": "worldcoin-wld", "name": "Worldcoin", "emoji": "🪙"},
    "PYTH": {"id": "pyth-network", "name": "Pyth Network", "emoji": "🪙"},
    "PEPE": {"id": "pepe", "name": "Pepe", "emoji": "🪙"},
    "FLOKI": {"id": "floki", "name": "FLOKI", "emoji": "🪙"},
    "FTM": {"id": "fantom", "name": "Fantom", "emoji": "🪙"},
    "TAO": {"id": "bittensor", "name": "Bittensor", "emoji": "🪙"},
    "MNT": {"id": "mantle", "name": "Mantle", "emoji": "🪙"},
    "RUNE": {"id": "thorchain", "name": "THORChain", "emoji": "🪙"},
    "GALA": {"id": "gala", "name": "GALA", "emoji": "🪙"},
    "CHZ": {"id": "chiliz", "name": "Chiliz", "emoji": "🪙"},
    "NEO": {"id": "neo", "name": "NEO", "emoji": "🪙"},
    "FLOW": {"id": "flow", "name": "Flow", "emoji": "🪙"},
    "ETHDYDX": {"id": "dydx", "name": "dYdX", "emoji": "🪙"},
    "AXS": {"id": "axie-infinity", "name": "Axie Infinity", "emoji": "🪙"},
    "KCS": {"id": "kucoin-shares", "name": "KuCoin", "emoji": "🪙"},
    "MINA": {"id": "mina-protocol", "name": "Mina Protocol", "emoji": "🪙"},
    "EOS": {"id": "eos", "name": "EOS", "emoji": "🪙"},
    "XTZ": {"id": "tezos", "name": "Tezos", "emoji": "🪙"},
    "KAVA": {"id": "kava", "name": "Kava", "emoji": "🪙"},
    "BLUR": {"id": "blur", "name": "Blur", "emoji": "🪙"},
    "FET": {"id": "fetch-ai", "name": "Artificial Superintelligence Alliance", "emoji": "🪙"},
    "AGIX": {"id": "singularitynet", "name": "SingularityNET", "emoji": "🪙"},
    "ROSE": {"id": "oasis-network", "name": "Oasis", "emoji": "🪙"},
    "ZIL": {"id": "zilliqa", "name": "Zilliqa", "emoji": "🪙"},
    "ENJ": {"id": "enjincoin", "name": "Enjin Coin", "emoji": "🪙"},
    "DASH": {"id": "dash", "name": "Dash", "emoji": "🪙"},
    "TWT": {"id": "trust-wallet-token", "name": "Trust Wallet", "emoji": "🪙"},
    "1INCH": {"id": "1inch", "name": "1INCH", "emoji": "🪙"},
    "BAT": {"id": "basic-attention-token", "name": "Basic Attention", "emoji": "🪙"},
    "CAKE": {"id": "pancakeswap-token", "name": "PancakeSwap", "emoji": "🪙"},
    "THETA": {"id": "theta-token", "name": "Theta Network", "emoji": "🪙"},
    "GMX": {"id": "gmx", "name": "GMX", "emoji": "🪙"},
    "KLAY": {"id": "klay-token", "name": "Klaytn", "emoji": "🪙"},
    "CVX": {"id": "convex-finance", "name": "Convex Finance", "emoji": "🪙"},
    "HNT": {"id": "helium", "name": "Helium", "emoji": "🪙"},
    "NEXO": {"id": "nexo", "name": "NEXO", "emoji": "🪙"},
    "ZEC": {"id": "zcash", "name": "Zcash", "emoji": "🪙"},
    "IOTA": {"id": "iota", "name": "IOTA", "emoji": "🪙"},
    "GNO": {"id": "gnosis", "name": "Gnosis", "emoji": "🪙"},
    "BICO": {"id": "biconomy", "name": "Biconomy", "emoji": "🪙"},
    "LRC": {"id": "loopring", "name": "Loopring", "emoji": "🪙"},
    "SUSHI": {"id": "sushi", "name": "Sushi", "emoji": "🪙"},
    "RSR": {"id": "reserve-rights-token", "name": "Reserve Rights", "emoji": "🪙"},
    "GMT": {"id": "stepn", "name": "GMT", "emoji": "🪙"},
    "MASK": {"id": "mask-network", "name": "Mask Network", "emoji": "🪙"},
    "TON": {"id": "the-open-network", "name": "Toncoin", "emoji": "◆"},
}


# ============================================================================
# FIAT CURRENCIES
# ============================================================================
SUPPORTED_FIATS: Dict[str, Dict[str, str]] = {
    "usd": {"name": "US Dollar", "symbol": "$", "flag": "🇺🇸"},
    "eur": {"name": "Euro", "symbol": "€", "flag": "🇪🇺"},
    "inr": {"name": "Indian Rupee", "symbol": "₹", "flag": "🇮🇳"},
    "gbp": {"name": "British Pound", "symbol": "£", "flag": "🇬🇧"},
    "aed": {"name": "UAE Dirham", "symbol": "د.إ", "flag": "🇦🇪"},
    "jpy": {"name": "Japanese Yen", "symbol": "¥", "flag": "🇯🇵"},
    "cad": {"name": "Canadian Dollar", "symbol": "C$", "flag": "🇨🇦"},
    "aud": {"name": "Australian Dollar", "symbol": "A$", "flag": "🇦🇺"},
    "chf": {"name": "Swiss Franc", "symbol": "CHF", "flag": "🇨🇭"},
    "cny": {"name": "Chinese Yuan", "symbol": "¥", "flag": "🇨🇳"},
    "krw": {"name": "South Korean Won", "symbol": "₩", "flag": "🇰🇷"},
    "mxn": {"name": "Mexican Peso", "symbol": "Mex$", "flag": "🇲🇽"},
}

# ============================================================================
# COLORS FOR UI (HEX CODES FOR CONSISTENCY)
# ============================================================================
COLORS = {
    "primary": "#00d4aa",      # Flux Teal
    "success": "#00d4aa",       # Gains (teal)
    "danger": "#ff4757",        # Losses (red)
    "warning": "#ffa502",       # Alerts (amber)
    "dark": "#0d1117",          # Dark bg (GitHub-dark style)
    "light": "#e6edf3",         # Light text
    "accent": "#58a6ff",        # Blue accent
    "grid": "#21262d",          # Grid lines
    "muted": "#8b949e",         # Muted text
}

# ============================================================================
# CHAT ACTIONS
# ============================================================================
CHAT_ACTIONS = {
    "typing": "typing",
    "upload_photo": "upload_photo",
    "upload_document": "upload_document",
    "find_location": "find_location",
}

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
