"""
Flux — Real-time Crypto Intelligence
Built with Aiogram 3.x
"""

import asyncio
import logging
from html import escape
from typing import Optional, Dict, List
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery , BufferedInputFile
)
from aiogram.enums import ChatAction

import db
import config
import api_utils
from cache import init_cache, get_cache, get_rate_limiter
from message import get_message, LANGUAGES

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ============================================================================
# SETUP & CONFIG
# ============================================================================

# Initialize logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()

# Initialize cache
init_cache(
    max_entries=config.MAX_CHART_CACHE_SIZE,
    ttl_seconds=config.CHART_CACHE_TTL
)

# ============================================================================
# FSM STATES
# ============================================================================

class ConverterStates(StatesGroup):
    """Converter conversation states"""
    select_source_coin = State()
    select_target_type = State()
    select_target = State()
    enter_amount = State()


# ============================================================================
# UTILITIES
# ============================================================================

async def send_text_menu(query: CallbackQuery, text: str, reply_markup: InlineKeyboardMarkup):
    if query.message.photo:
        await query.message.delete()
        await bot.send_message(query.from_user.id, text=text, reply_markup=reply_markup)
    else:
        try:
            await query.message.edit_text(text=text, reply_markup=reply_markup)
        except Exception:
            await query.message.delete()
            await bot.send_message(query.from_user.id, text=text, reply_markup=reply_markup)

# ============================================================================


def get_user_lang(user_id: int) -> str:
    """Get user's preferred language"""
    user = db.get_user(user_id)
    if user and user.get("language") in LANGUAGES:
        return user["language"]
    return "en"


def create_info_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Create trust and policy keyboard."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_message(lang, "privacy_button"),
                    callback_data="menu_privacy"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "terms_button"),
                    callback_data="menu_terms"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "support_button"),
                    callback_data="menu_support"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "home_button"),
                    callback_data="back_to_menu"
                ),
            ],
        ]
    )


def create_main_menu(lang: str) -> InlineKeyboardMarkup:
    """Create main menu keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_message(lang, "prices_button"),
                    callback_data="menu_prices"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "converter_button"),
                    callback_data="menu_converter"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "news_button"),
                    callback_data="news_fetch"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "settings_button"),
                    callback_data="menu_settings"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "help_button"),
                    callback_data="menu_help"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "privacy_button"),
                    callback_data="menu_privacy"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "terms_button"),
                    callback_data="menu_terms"
                ),
            ]
        ]
    )

def create_coins_keyboard(lang: str, page: int = 0, columns: int = 3, per_page: int = 15) -> InlineKeyboardMarkup:
    """Create cryptocurrency selection keyboard with pagination"""
    coins_list = list(config.SUPPORTED_COINS.items())
    total_pages = (len(coins_list) + per_page - 1) // per_page
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    current_coins = coins_list[start_idx:end_idx]
    
    buttons = []
    for symbol, coin_info in current_coins:
        emoji = coin_info.get("emoji", "💰")
        buttons.append(
            InlineKeyboardButton(
                text=f"{emoji} {symbol}",
                callback_data=f"coin_{symbol}"
            )
        )
    
    # Create rows
    keyboard = [buttons[i:i+columns] for i in range(0, len(buttons), columns)]
    
    # Pagination row
    pagination_row = []
    if page > 0:
        pagination_row.append(
            InlineKeyboardButton(text="⬅️ Prev", callback_data=f"coins_page_{page-1}")
        )
    if page < total_pages - 1:
        pagination_row.append(
            InlineKeyboardButton(text="Next ➡️", callback_data=f"coins_page_{page+1}")
        )
        
    if pagination_row:
        keyboard.append(pagination_row)
        
    keyboard.append([
        InlineKeyboardButton(
            text=get_message(lang, "back_button"),
            callback_data="back_to_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_languages_keyboard() -> InlineKeyboardMarkup:
    """Create language selection keyboard"""
    buttons = []
    for lang_code, lang_name in LANGUAGES.items():
        buttons.append(
            InlineKeyboardButton(
                text=lang_name,
                callback_data=f"lang_{lang_code}"
            )
        )
    
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# ============================================================================
# COMMAND HANDLERS
# ============================================================================

@dp.message(Command("start"))
async def start_handler(message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    user_name = escape(message.from_user.full_name or "there")
    
    # Create user if not exists
    if not db.user_exists(user_id):
        db.create_user(user_id)
        logger.info(f"👤 New user registered: {user_id}")
    
    # Get user's language
    lang = get_user_lang(user_id)

    await message.answer(
        text=f"Hello, {user_name}.\n\n{get_message(lang, 'welcome')}",
        reply_markup=create_main_menu(lang)
    )
    


@dp.message(Command("help"))
async def help_handler(message: Message):
    """Handle /help command"""
    lang = get_user_lang(message.from_user.id)
    
    help_text = (
    "<b>Flux</b>\n\n"
    "View live market data.\n"
    "Track prices, view charts, convert assets, and follow market headlines.\n\n"
    "<i>For informational purposes only. Not financial advice.</i>\n\n"
    "Use /privacy and /terms for details."
    )
    
    await message.answer(
        help_text,
        reply_markup=create_info_keyboard(lang),
        disable_web_page_preview=True
    )

@dp.callback_query(F.data == "menu_help")
async def helper_info(query: CallbackQuery):
    """Show help info"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    help_text = (
        "<b>Flux</b>\n\n"
        "View live market data.\n"
        "Track prices, view charts, convert assets, and follow market headlines.\n\n"
        "<i>For informational purposes only. Not financial advice.</i>\n\n"
        "Use /privacy and /terms for details."
        )
        
    await send_text_menu(query, help_text, create_info_keyboard(lang))


@dp.message(Command("privacy"))
async def privacy_handler(message: Message):
    """Handle /privacy command"""
    lang = get_user_lang(message.from_user.id)
    await message.answer(get_message(lang, "privacy_text"), reply_markup=create_info_keyboard(lang))


@dp.message(Command("terms"))
async def terms_handler(message: Message):
    """Handle /terms command"""
    lang = get_user_lang(message.from_user.id)
    await message.answer(get_message(lang, "terms_text"), reply_markup=create_info_keyboard(lang))


@dp.message(Command("support"))
async def support_handler(message: Message):
    """Handle /support command"""
    lang = get_user_lang(message.from_user.id)
    await message.answer(get_message(lang, "support_text"), reply_markup=create_info_keyboard(lang))


@dp.callback_query(F.data == "menu_privacy")
async def privacy_menu(query: CallbackQuery):
    """Show privacy policy"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await send_text_menu(query, get_message(lang, "privacy_text"), create_info_keyboard(lang))


@dp.callback_query(F.data == "menu_terms")
async def terms_menu(query: CallbackQuery):
    """Show terms"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await send_text_menu(query, get_message(lang, "terms_text"), create_info_keyboard(lang))


@dp.callback_query(F.data == "menu_support")
async def support_menu(query: CallbackQuery):
    """Show support details"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    await send_text_menu(query, get_message(lang, "support_text"), create_info_keyboard(lang))

# ============================================================================
# PRICES MENU
# ============================================================================

@dp.callback_query(F.data == "menu_prices")
async def prices_menu(query: CallbackQuery):
    """Show prices menu"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    await send_text_menu(
        query,
        get_message(lang, "prices_title"),
        create_coins_keyboard(lang)
    )

@dp.callback_query(F.data.startswith("coins_page_"))
async def paginate_coins(query: CallbackQuery):
    """Handle pagination for coins menu"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    page = int(query.data.split("_")[-1])
    
    try:
        await query.message.edit_reply_markup(
            reply_markup=create_coins_keyboard(lang, page=page)
        )
    except Exception:
        pass  # Ignore if identical


@dp.callback_query(StateFilter(None), F.data.startswith("coin_"))
async def show_coin_price(query: CallbackQuery):
    """Show price for selected coin (Redis-based)"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)

    symbol = query.data.replace("coin_", "").upper()

    if symbol not in config.SUPPORTED_COINS:
        await query.answer("❌ Coin not found")
        return

    coin_info = config.SUPPORTED_COINS[symbol]
    coin_id = coin_info["id"]
    print(f"Fetching price for {symbol} (ID: {coin_id}) from Redis...")

    # Show typing
    await bot.send_chat_action(query.from_user.id, ChatAction.TYPING)
    await query.message.edit_text("Fetching live data")

    try:
        # ✅ FIX 1: await
        price_list = await db.get_market_prices()

        price_data = None
        if price_list:
            price_map = {coin["symbol"].upper(): coin for coin in price_list}
            price_data = price_map.get(symbol)

        if not price_data:
            fallback_data = await api_utils.fetch_price_data(coin_id)
            if fallback_data:
                price_data = {
                    "price_usd": fallback_data.get("current_price"),
                    "price_change_24h_pct": fallback_data.get("price_change_percentage_24h"),
                    "high_24h": fallback_data.get("high_24h"),
                    "low_24h": fallback_data.get("low_24h"),
                    "market_cap_usd": fallback_data.get("market_cap"),
                    "volume_24h_usd": fallback_data.get("total_volume"),
                }

        if not price_data:
            await query.message.edit_text(get_message(lang, "error_connection"))
            return

        # ✅ FIX 3: Correct Redis field names
        price = price_data.get("price_usd", 0)
        change_24h = price_data.get("price_change_24h_pct") or 0
        high = price_data.get("high_24h", 0)
        low = price_data.get("low_24h", 0)
        market_cap = price_data.get("market_cap_usd", 0)
        volume = price_data.get("volume_24h_usd", 0)

        price_text = (
            f"{get_message(lang, 'coin_detail_header', emoji=escape(coin_info['emoji']), name=escape(coin_info['name']), symbol=escape(symbol))}\n\n"
            f"{get_message(lang, 'price_label')} {api_utils.format_price(price)}\n"
            f"{get_message(lang, 'change_label')} {change_24h:+.2f}% {api_utils.get_trend_emoji(change_24h)}\n\n"
            f"{get_message(lang, 'high_label')} {api_utils.format_price(high)}\n"
            f"{get_message(lang, 'low_label')} {api_utils.format_price(low)}\n"
            f"{get_message(lang, 'market_cap_label')} {api_utils.format_large_number(market_cap)}\n"
            f"{get_message(lang, 'volume_label')} {api_utils.format_large_number(volume)}\n\n"
            f"{get_message(lang, 'source_label')}"
        )

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Chart",
                        callback_data=f"chart_{coin_id}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=get_message(lang, "back_button"),
                        callback_data="menu_prices"
                    ),
                ],
            ]
        )

        await query.message.edit_text(price_text, reply_markup=keyboard,message_effect_id="5107584321108051014")

    except Exception as e:
        logger.error(f"❌ Price fetch error: {e}")

        await query.message.edit_text(
            get_message(lang, "error_generic")
        )

@dp.callback_query(F.data.startswith("chart_"))
async def show_chart(query: CallbackQuery):
    """Generate and show price chart"""
    await query.answer()

    lang = get_user_lang(query.from_user.id)

    coin_id = query.data.replace("chart_", "")

    # Show loading message
    await query.message.edit_text(
        get_message(lang, "generating_chart")
    )

    # Show upload photo action
    await bot.send_chat_action(
        query.from_user.id,
        ChatAction.UPLOAD_PHOTO
    )

    try:
        # Fetch chart
        chart_image = await api_utils.fetch_price_chart(coin_id)

        if not chart_image:
            await query.message.edit_text(
                get_message(lang, "chart_error")
            )
            return

        # Convert BytesIO -> Telegram InputFile
        photo = BufferedInputFile(
            chart_image.getvalue(),
            filename="chart.png"
        )

        # Send chart
        await bot.send_photo(
            chat_id=query.from_user.id,
            photo=photo,
            caption=get_message(lang, "chart_ready"),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=get_message(lang, "back_button"),
                            callback_data="menu_prices"
                        )
                    ]
                ]
            ),message_effect_id="5104841245755180586"
        )

        # Delete loading message
        await query.message.delete()

    except Exception as e:
        logger.error(f"❌ Chart error: {e}")

        await query.message.edit_text(
            get_message(lang, "chart_error")
        )


# ============================================================================
# NEWS MENU
# ============================================================================

@dp.callback_query(F.data == "menu_news")
async def news_menu(query: CallbackQuery):
    """Show news menu"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="View Headlines",
                    callback_data="news_fetch"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "back_button"),
                    callback_data="back_to_menu"
                ),
            ],
        ]
    )
    
    await send_text_menu(query, get_message(lang, "latest_news"), keyboard)


@dp.callback_query(F.data == "news_fetch")
async def fetch_news(query: CallbackQuery):
    """Fetch and show latest news"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    # Show loading
    await send_text_menu(
        query,
        get_message(lang, "fetching_news"),
        None
    )
    
    # Show typing action
    await bot.send_chat_action(query.from_user.id, ChatAction.TYPING)
    
    try:
        # Fetch news
        news_items = await api_utils.fetch_crypto_news(limit=5)
        
        if not news_items:
            await bot.send_message(
                chat_id=query.from_user.id,
                text=get_message(lang, "news_unavailable")
            )
            return
        
        # Format brief titles with outbound links.
        news_text = "<b>Market Headlines</b>\n\n"
        for i, item in enumerate(news_items, 1):
            title = escape(item.get("title", "Market article"))
            source = escape(item.get("source", "Market source"))
            link = item.get("link", "")
            if link:
                news_text += f"<b>{title}</b>\nSource: {source}\n<a href='{link}'>Read more</a>\n\n"
            else:
                news_text += f"<b>{title}</b>\nSource: {source}\n\n"
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=get_message(lang, "back_button"),
                    callback_data="back_to_menu"
                )
            ]]
        )
        
        await bot.send_message(
            chat_id=query.from_user.id,
            text=news_text,
            reply_markup=keyboard
        )
    
    except Exception as e:
        logger.error(f"❌ News error: {e}")
        await bot.send_message(
            chat_id=query.from_user.id,
            text=get_message(lang, "error_generic")
        )


@dp.callback_query(F.data == "news_toggle")
async def toggle_news(query: CallbackQuery):
    """Toggle news subscription"""
    await query.answer()
    user_id = query.from_user.id
    lang = get_user_lang(user_id)
    
    user = db.get_user(user_id)
    if not user:
        db.create_user(user_id)
        user = db.get_user(user_id)
    
    new_status = not user.get("news_subscription", False)
    db.update_user(user_id, "news_subscription", new_status)
    
    status_text = get_message(lang, "on") if new_status else get_message(lang, "off")
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=get_message(lang, "back_button"),
                callback_data="menu_settings"
            )
        ]]
    )
    
    await send_text_menu(
        query,
        f"{get_message(lang, 'settings_title')}\n\n{get_message(lang, 'news_status', status=status_text)}",
        keyboard
    )


# ============================================================================
# CONVERTER
# ============================================================================

@dp.callback_query(F.data == "menu_converter")
async def converter_start(query: CallbackQuery, state: FSMContext):
    """Start converter"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    await state.set_state(ConverterStates.select_source_coin)
    
    await send_text_menu(query, get_message(lang, "select_coin"), create_coins_keyboard(lang))


@dp.callback_query(
    ConverterStates.select_source_coin,
    F.data.startswith("coin_")
)
async def converter_select_type(query: CallbackQuery, state: FSMContext):
    """Select conversion type (fiat or crypto)"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    symbol = query.data.replace("coin_", "")
    await state.update_data(source_coin=symbol)
    await state.set_state(ConverterStates.select_target_type)
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_message(lang, "to_fiat_button"),
                    callback_data="type_fiat"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "to_crypto_button"),
                    callback_data="type_crypto"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "back_button"),
                    callback_data="back_to_menu"
                ),
            ],
        ]
    )
    
    await send_text_menu(query, get_message(lang, "select_type"), keyboard)


@dp.callback_query(
    ConverterStates.select_target_type,
    F.data == "type_fiat"
)
async def converter_select_fiat(query: CallbackQuery, state: FSMContext):
    """Select fiat target"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    await state.update_data(target_type="fiat")
    await state.set_state(ConverterStates.select_target)
    
    # Create fiat buttons
    buttons = []
    for code, fiat_info in config.SUPPORTED_FIATS.items():
        buttons.append(
            InlineKeyboardButton(
                text=f"{fiat_info['flag']} {code.upper()}",
                callback_data=f"fiat_{code}"
            )
        )
    
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    keyboard.append([
        InlineKeyboardButton(
                    text=get_message(lang, "back_button"),
                    callback_data="back_to_menu"
                )
    ])
    
    await send_text_menu(query, get_message(lang, "select_target"), InlineKeyboardMarkup(inline_keyboard=keyboard))


@dp.callback_query(
    ConverterStates.select_target_type,
    F.data == "type_crypto"
)
async def converter_select_crypto(query: CallbackQuery, state: FSMContext):
    """Select crypto target"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    data = await state.get_data()
    source_coin = data.get("source_coin")
    
    await state.update_data(target_type="crypto")
    await state.set_state(ConverterStates.select_target)
    
    # Create crypto buttons (excluding source)
    buttons = []
    for symbol in config.SUPPORTED_COINS.keys():
        if symbol != source_coin:
            buttons.append(
                InlineKeyboardButton(
                    text=f"🪙 {symbol}",
                    callback_data=f"crypto_{symbol}"
                )
            )
    
    keyboard = [buttons[i:i+3] for i in range(0, len(buttons), 3)]
    keyboard.append([
        InlineKeyboardButton(
                    text=get_message(lang, "back_button"),
                    callback_data="back_to_menu"
                )
    ])
    
    await send_text_menu(query, get_message(lang, "select_target"), InlineKeyboardMarkup(inline_keyboard=keyboard))


@dp.callback_query(
    ConverterStates.select_target,
    F.data.startswith(("fiat_", "crypto_"))
)
async def converter_enter_amount(query: CallbackQuery, state: FSMContext):
    """Ask for amount"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    if query.data.startswith("fiat_"):
        target = query.data.replace("fiat_", "")
    else:
        target = query.data.replace("crypto_", "")
    
    data = await state.get_data()
    source = data.get("source_coin")
    
    await state.update_data(target=target)
    await state.set_state(ConverterStates.enter_amount)
    
    coin_name = escape(config.SUPPORTED_COINS[source]["name"])
    
    await send_text_menu(query, get_message(lang, "enter_amount", coin=f"{coin_name} ({source})"), None)

@dp.message(ConverterStates.enter_amount)
async def converter_calculate(message: Message, state: FSMContext):
    """Calculate conversion"""
    lang = get_user_lang(message.from_user.id)
    
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer(
                get_message(lang, "invalid_amount")
            )
            return
    except ValueError:
        await message.answer(
            get_message(lang, "invalid_amount")
        )
        return
    
    # Show typing
    await bot.send_chat_action(message.from_user.id, ChatAction.TYPING)
    
    try:
        data = await state.get_data()
        source_coin = data.get("source_coin")
        target = data.get("target")
        target_type = data.get("target_type")
        
        # Fetch prices from Redis
        prices = await db.get_market_prices()
        
        if not prices:
            await message.answer(
                get_message(lang, "conversion_error")
            )
            return
        
        # Find source price (UPDATED: Case-insensitive match)
        source_price = next(
            (p for p in prices if p.get("symbol", "").upper() == source_coin.upper()),
            None
        )
        
        if not source_price:
            await message.answer(
                get_message(lang, "conversion_error")
            )
            return
        
        source_price_usd = float(source_price.get("price_usd") or 0)
        if source_price_usd <= 0:
            await message.answer(
                get_message(lang, "conversion_error")
            )
            return
        
        if target_type == "fiat":
            # Crypto to Fiat
            fiat_info = config.SUPPORTED_FIATS.get(target.lower())
            if not fiat_info:
                await message.answer(
                    get_message(lang, "conversion_error")
                )
                return
            
            # Simplified rate (in production, use actual forex API)
            fiat_rates = {
                "usd": 1.0, "inr": 83.5, "eur": 0.92, "gbp": 0.79,
                "aed": 3.67, "jpy": 110.0, "cad": 1.35, "aud": 1.45,
                "chf": 0.92, "cny": 6.45, "krw": 1200, "mxn": 20
            }
            
            rate = fiat_rates.get(target.lower(), 1.0)
            result = amount * source_price_usd * rate
            symbol = fiat_info["symbol"]
        else:
            # Crypto to Crypto (UPDATED: Case-insensitive match)
            target_price = next(
                (p for p in prices if p.get("symbol", "").upper() == target.upper()),
                None
            )
            
            if not target_price:
                await message.answer(
                    get_message(lang, "conversion_error")
                )
                return
            
            target_price_usd = float(target_price.get("price_usd") or 0)
            if target_price_usd <= 0:
                await message.answer(
                    get_message(lang, "conversion_error")
                )
                return
            result = amount * (source_price_usd / target_price_usd)
            symbol = target
        
        result_text = get_message(
            lang, "conversion_result",
            amount=f"{amount:,.2f}",
            coin_symbol=source_coin.upper(),
            result=f"{result:,.4f}",
            target_symbol=symbol.upper()
        )
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=get_message(lang, "converter_button"),
                    callback_data="menu_converter"
                ),
                InlineKeyboardButton(
                    text=get_message(lang, "home_button"),
                    callback_data="back_to_menu"
                ),
            ]]
        )
        
        await message.answer(result_text, reply_markup=keyboard)
    
    except Exception as e:
        logger.error(f"❌ Conversion error: {e}")
        await message.answer(
            get_message(lang, "conversion_error")
        )
    
    finally:
        await state.clear()


# ============================================================================
# SETTINGS
# ============================================================================

@dp.callback_query(F.data == "menu_settings")
async def settings_menu(query: CallbackQuery):
    """Show settings menu"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    user = db.get_user(query.from_user.id)
    news_enabled = user.get("news_subscription", False) if user else False
    
    status_text = get_message(lang, "on") if news_enabled else get_message(lang, "off")
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_message(lang, "language_button"),
                    callback_data="settings_language"
                ),
                InlineKeyboardButton(
                    text=f"{get_message(lang, 'news_toggle_button')}: {status_text}",
                    callback_data="news_toggle"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=get_message(lang, "back_button"),
                    callback_data="back_to_menu"
                ),
            ],
        ]
    )
    
    text = f"{get_message(lang, 'settings_title')}\n\n{get_message(lang, 'news_status', status=status_text)}"
    await send_text_menu(query, text, keyboard)


@dp.callback_query(F.data == "settings_language")
async def select_language(query: CallbackQuery):
    """Show language selection"""
    await query.answer()
    
    await query.message.edit_text(
        "<b>Language</b>",
        reply_markup=create_languages_keyboard()
    )


@dp.callback_query(F.data.startswith("lang_"))
async def set_language(query: CallbackQuery):
    """Set user language"""
    await query.answer("Language updated.")
    
    lang_code = query.data.replace("lang_", "")
    user_id = query.from_user.id
    
    db.update_user(user_id, "language", lang_code)
    
    await query.message.edit_text(
        get_message(lang_code, "language_saved"),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text=get_message(lang_code, "home_button"),
                    callback_data="back_to_menu"
                )
            ]]
        )
    )


# ============================================================================
# BACK BUTTONS
# ============================================================================

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(query: CallbackQuery, state: FSMContext):
    """Go back to main menu"""
    await query.answer()
    lang = get_user_lang(query.from_user.id)
    
    await state.clear()
    
    await send_text_menu(query, get_message(lang, "main_menu"), create_main_menu(lang))


# ============================================================================
# BACKGROUND JOBS
# ============================================================================

async def background_fetch_news():
    """Periodically fetch and store news"""
    while True:
        try:
            await asyncio.sleep(300)  # Every 5 minutes
            
            news_items = await api_utils.fetch_crypto_news(limit=5)
            for item in news_items:
                db.add_news_item(item)
            
            logger.info(f"✅ News updated: {len(news_items)} items")
        
        except Exception as e:
            logger.error(f"❌ News fetch job error: {e}")


async def background_broadcast_news():
    """Periodically broadcast news to subscribed users"""
    while True:
        try:
            await asyncio.sleep(43200)  # Every 12 hours
            
            news_queue = db.get_news_queue()
            if not news_queue:
                continue
            
            import random
            batch_size = random.randint(1, min(3, len(news_queue)))
            raw_batch = db.pop_news_batch(batch_size=batch_size)
            
            # Summarize right before broadcasting to save API limits
            batch = []
            for item in raw_batch:
                summary = await api_utils.scrape_and_summarize(item["link"])
                if summary:
                    item["summary"] = summary
                batch.append(item)
                
            subscribed_users = db.get_subscribed_users()
            
            for user_id in subscribed_users:
                try:
                    news_text = "<b>Market Headlines</b>\n\n"
                    for item in batch:
                        title = escape(item.get("title", "Market article"))
                        link = item.get("link", "")
                        summary = escape(item.get("summary", ""))
                        if summary:
                            news_text += f"<b>{title}</b>\n{summary}\n<a href='{link}'>Read more</a>\n\n"
                        else:
                            news_text += f"<b>{title}</b>\n<a href='{link}'>Read more</a>\n\n"
                    
                    await bot.send_message(
                        user_id, news_text,
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[[
                                InlineKeyboardButton(
                                    text="Headline Settings",
                                    callback_data="menu_settings"
                                )
                            ]]
                        )
                    )
                except Exception as e:
                    logger.warning(f"⚠️ Failed to send news to {user_id}: {e}")
            
            logger.info(f"✅ Broadcast sent to {len(subscribed_users)} users")
        
        except Exception as e:
            logger.error(f"❌ Broadcast job error: {e}")


# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

async def on_startup():
    """Bot startup"""
    logger.info("Flux is starting...")
    logger.info(f"📊 Cache: {get_cache().get_stats()}")
    logger.info(f"⏳ Rate limiter: {get_rate_limiter().get_stats()}")


async def on_shutdown():
    """Bot shutdown"""
    logger.info("Shutting down Flux...")
    await db.close_redis()


async def main():
    """Main entry point"""
    # Set up background tasks
    asyncio.create_task(background_fetch_news())
    asyncio.create_task(background_broadcast_news())
    
    # Set handlers
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    # Start polling
    logger.info("Flux is online.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
