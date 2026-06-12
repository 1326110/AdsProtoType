"""
Messages for Flux — Real-time Crypto Intelligence.
"""

LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "hi": "हिन्दी",
    "zh": "中文",
    "ja": "日本語"
}

MESSAGES = {
    "en": {
        "welcome": (
            "<b>Flux</b>\n\n"
            "View live market data, track price movements,\n"
            "and compare asset values.\n\n"
            "<i>For informational purposes only. Not financial advice.</i>"
        ),
        "choose_language": (
            "<b>Language</b>\n\n"
            "Select your preferred language:"
        ),
        "language_saved": (
            "<b>Language saved</b>\n\n"
            "Your selection has been saved."
        ),
        "main_menu": (
            "<b>Flux</b>\n\n"
            "View live market data, track price movements,\n"
            "and compare asset values.\n\n"
            "<i>For informational purposes only. Not financial advice.</i>"
        ),
        "prices_button": "📊 Prices",
        "news_button": "📰 Headlines",
        "converter_button": "🔄 Converter",
        "settings_button": "⚙️ Settings",
        "help_button": "ℹ️ About",
        "privacy_button": "Privacy",
        "terms_button": "Terms",
        "support_button": "Support",
        "back_button": "← Back",
        "refresh_button": "⟳ Refresh",
        "home_button": "Home",

        "prices_title": (
            "<b>Market Prices</b>\n\n"
            "Select an asset to view current market data."
        ),
        "coin_detail_header": "<b>{emoji} {name} ({symbol})</b>",
        "price_label": "<b>Price:</b>",
        "change_label": "<b>24h change:</b>",
        "high_label": "<b>24h high:</b>",
        "low_label": "<b>24h low:</b>",
        "market_cap_label": "<b>Market cap:</b>",
        "volume_label": "<b>24h volume:</b>",
        "source_label": "Data: public market feed",

        "generating_chart": (
            "<b>Loading chart</b>\n"
            "Fetching price history..."
        ),
        "chart_ready": "<b>Chart ready</b>",
        "chart_error": (
            "<b>Chart unavailable</b>\n\n"
            "Try again in a moment."
        ),

        "news_prompt": (
            "<b>Market Headlines</b>\n\n"
            "Latest market stories and updates."
        ),
        "news_enabled": (
            "Headlines enabled\n\n"
            "You will receive market updates."
        ),
        "news_disabled": (
            "Headlines disabled\n\n"
            "Market updates are turned off."
        ),
        "fetching_news": (
            "<b>Loading headlines</b>\n"
            "Fetching the latest stories..."
        ),
        "news_unavailable": (
            "<b>No headlines available</b>\n\n"
            "News feed is currently unavailable. Check back later."
        ),
        "latest_news": "<b>Latest Headlines</b>",
        "news_item": "<b>{title}</b>\nSource: {source}",
        "no_news": (
            "No stories available\n\n"
            "Check again later."
        ),

        "converter_title": (
            "<b>Asset Converter</b>\n\n"
            "Calculate equivalent values across currencies and assets using live rates."
        ),
        "select_coin": (
            "<b>Step 1 - Select Asset</b>\n\n"
            "Choose the asset you want to convert from."
        ),
        "select_type": (
            "<b>Step 2 - Target Type</b>\n\n"
            "Convert to fiat or another cryptocurrency?"
        ),
        "select_target": (
            "<b>Step 3 - Choose Target</b>\n\n"
            "Select the target currency or asset."
        ),
        "enter_amount": (
            "<b>Step 4 - Enter Amount</b>\n\n"
            "How much {coin} to convert?\n\n"
            "Enter a positive number."
        ),

        "to_fiat_button": "💵 Fiat",
        "to_crypto_button": "🪙 Crypto",

        "conversion_result": (
            "<b>Conversion Result</b>\n\n"
            "{amount} {coin_symbol} = {result} {target_symbol}\n\n"
            "Based on current market rates."
        ),
        "invalid_amount": (
            "<b>Invalid amount</b>\n\n"
            "Enter a positive number."
        ),
        "conversion_error": (
            "<b>Conversion unavailable</b>\n\n"
            "Could not fetch rates. Try again."
        ),

        "settings_title": (
            "<b>Settings</b>\n\n"
            "Manage your preferences."
        ),
        "language_button": "🌐 Language",
        "news_toggle_button": "📰 Headlines",
        "news_status": "<b>Settings</b>\n\nHeadlines: {status}",
        "on": "ON",
        "off": "OFF",

        "error_timeout": "<b>Request timed out</b>\n\nTry again in a moment.",
        "error_connection": "<b>Connection error</b>\n\nData source unreachable. Try again.",
        "error_generic": "<b>Something went wrong</b>\n\nPlease try again.",
        "privacy_text": (
            "<b>Privacy</b>\n\n"
            "Flux stores your Telegram ID, language preference, and headlines setting to remember your preferences.\n\n"
            "No wallet addresses, private keys, seed phrases, or financial data are ever requested or stored.\n\n"
            "Market data is fetched from public APIs. You can stop using Flux at any time."
        ),
        "terms_text": (
            "<b>Terms of Use</b>\n\n"
            "Flux provides informational market data only. It is not investment advice, a broker, an exchange, or a wallet.\n\n"
            "Prices, charts, conversions, and headlines may be delayed or unavailable. Always verify data independently.\n\n"
            "Do not share private keys, seed phrases, passwords, or financial credentials with any bot."
        ),
        "support_text": (
            "<b>Support</b>\n\n"
            "Use /start to return to the menu, or reach out to the bot owner via their Telegram profile.\n\n"
            "Flux will never ask for wallet access, private keys, or passwords."
        ),

        "typing": "typing",
        "uploading": "uploading photo",
    },
    "ru": {
        "welcome": (
            "<b>Flux</b>\n\n"
            "Просматривайте рыночные данные в реальном времени, "
            "анализируйте ценовые движения и сравнивайте стоимость активов.\n\n"
            "<i>Исключительно для информационных целей. Не является финансовой консультацией.</i>"
        ),
        "choose_language": "<b>Язык</b>\n\nВыберите предпочитаемый язык:",
        "language_saved": "<b>Язык обновлен</b>\n\nВаш выбор сохранен.",
        "main_menu": (
            "<b>Flux</b>\n\n"
            "Просматривайте рыночные данные в реальном времени, "
            "анализируйте ценовые движения и сравнивайте стоимость активов.\n\n"
            "<i>Исключительно для информационных целей. Не является финансовой консультацией.</i>"
        ),
        "prices_button": "📊 Данные рынка",
        "news_button": "📰 Обзоры рынка",
        "converter_button": "🔄 Оценка стоимости",
        "settings_button": "⚙️ Настройки",
        "help_button": "ℹ️ Информация",
        "privacy_button": "Конфиденциальность",
        "terms_button": "Условия",
        "support_button": "Поддержка",
        "back_button": "← Назад",
        "refresh_button": "⟳ Обновить",
        "home_button": "Главная",
        "prices_title": "<b>Данные рынка</b>\n\nВыберите актив для просмотра текущих данных.",
        "coin_detail_header": "<b>{emoji} {name} ({symbol})</b>",
        "price_label": "<b>Цена:</b>",
        "change_label": "<b>Изменение за 24ч:</b>",
        "high_label": "<b>Макс. за 24ч:</b>",
        "low_label": "<b>Мин. за 24ч:</b>",
        "market_cap_label": "<b>Капитализация:</b>",
        "volume_label": "<b>Объем за 24ч:</b>",
        "source_label": "Источник данных: публичный ценовой канал",
        "generating_chart": "<b>Загрузка графика</b>\nПолучение данных...",
        "chart_ready": "<b>График готов</b>",
        "chart_error": "<b>График недоступен</b>\n\nПовторите попытку.",
        "news_prompt": "<b>Обзоры рынка</b>\n\nПоследние события и заголовки рынка.",
        "news_enabled": "Обзоры включены\n\nВы будете получать обзоры рынка.",
        "news_disabled": "Обзоры отключены\n\nОбзоры рынка отключены.",
        "fetching_news": "<b>Загрузка статей</b>\nПолучение последних данных...",
        "news_unavailable": "<b>Статьи недоступны</b>\n\nИсточник временно недоступен. Повторите позже.",
        "latest_news": "<b>Новости рынка</b>",
        "news_item": "<b>{title}</b>\nИсточник: {source}",
        "no_news": "Нет доступных статей\n\nПроверьте позже.",
        "converter_title": "<b>Оценка курса</b>\n\nРассчитайте эквивалентную стоимость активов и валют на основе текущих рыночных курсов.",
        "select_coin": "<b>Шаг 1 - Базовый актив</b>\n\nВыберите актив для конвертации.",
        "select_type": "<b>Шаг 2 - Тип цели</b>\n\nКонвертировать в фиат или другую криптовалюту?",
        "select_target": "<b>Шаг 3 - Выберите цель</b>\n\nВыберите целевую валюту или актив.",
        "enter_amount": "<b>Шаг 4 - Введите сумму</b>\n\nВведите количество {coin} для конвертации.\n\nВведите положительное число.",
        "to_fiat_button": "💵 Фиат",
        "to_crypto_button": "🪙 Крипто",
        "conversion_result": "<b>Результат конвертации</b>\n\n{amount} {coin_symbol} = {result} {target_symbol}\n\nНа основе текущих рыночных курсов.",
        "invalid_amount": "<b>Неверный ввод</b>\n\nЗначение должно быть положительным числом.",
        "conversion_error": "<b>Конвертация недоступна</b>\n\nНе удалось получить курсы. Повторите позже.",
        "settings_title": "<b>Настройки</b>\n\nУправляйте настройками.",
        "language_button": "🌐 Язык",
        "news_toggle_button": "📰 Обзоры рынка",
        "news_status": "<b>Настройки</b>\n\nОбзоры рынка: {status}",
        "on": "Включено",
        "off": "Отключено",
        "error_timeout": "<b>Таймаут запроса</b>\n\nПовторите позже.",
        "error_connection": "<b>Ошибка соединения</b>\n\nИсточник данных недоступен. Повторите попытку.",
        "error_generic": "<b>Что-то пошло не так</b>\n\nПовторите попытку.",
        "privacy_text": (
            "<b>Конфиденциальность</b>\n\n"
            "Flux сохраняет ваш Telegram ID, выбранный язык и настройку обзоров рынка для запоминания предпочтений.\n\n"
            "Бот не запрашивает адреса кошельков, приватные ключи, сид-фразы или финансовые данные.\n\n"
            "Рыночные данные запрашиваются из публичных API. Вы можете прекратить использование в любое время."
        ),
        "terms_text": (
            "<b>Условия использования</b>\n\n"
            "Flux предоставляет исключительно информационные рыночные данные. "
            "Это не инвестиционная консультация, не брокер, не биржа и не кошелек.\n\n"
            "Цены, графики, конвертации и обзоры могут быть задержаны или недоступны. "
            "Всегда проверяйте данные самостоятельно.\n\n"
            "Не отправляйте приватные ключи, сид-фразы, пароли или финансовые данные этому боту."
        ),
        "support_text": (
            "<b>Поддержка</b>\n\n"
            "Используйте /start для возврата в меню или свяжитесь с владельцем бота через Telegram-профиль.\n\n"
            "Flux никогда не запрашивает доступ к кошельку, приватные ключи или пароли."
        ),
        "typing": "typing",
        "uploading": "uploading photo",
    },
    "hi": {
        "welcome": (
            "<b>Flux</b>\n\n"
            "रीयल-टाइम बाजार डेटा देखें, मूल्य गतिविधियों का विश्लेषण करें, "
            "और संपत्तियों के मूल्यों की तुलना करें।\n\n"
            "<i>केवल सूचनात्मक उद्देश्यों के लिए। कोई वित्तीय सलाह नहीं।</i>"
        ),
        "choose_language": "<b>भाषा</b>\n\nअपनी पसंदीदा भाषा चुनें:",
        "language_saved": "<b>भाषा सहेजी गई</b>\n\nआपकी पसंद सहेज दी गई है।",
        "main_menu": (
            "<b>Flux</b>\n\n"
            "रीयल-टाइम बाजार डेटा देखें, मूल्य गतिविधियों का विश्लेषण करें, "
            "और संपत्तियों के मूल्यों की तुलना करें।\n\n"
            "<i>केवल सूचनात्मक उद्देश्यों के लिए। कोई वित्तीय सलाह नहीं।</i>"
        ),
        "prices_button": "📊 बाजार डेटा",
        "news_button": "📰 बाजार समीक्षाएं",
        "converter_button": "🔄 मूल्य अनुमानक",
        "settings_button": "⚙️ सेटिंग्स",
        "help_button": "ℹ️ जानकारी",
        "privacy_button": "गोपनीयता",
        "terms_button": "शर्तें",
        "support_button": "सहायता",
        "back_button": "← वापस",
        "refresh_button": "⟳ रीफ्रेश",
        "home_button": "होम",
        "prices_title": "<b>बाजार डेटा</b>\n\nवर्तमान बाजार डेटा देखने के लिए एक संपत्ति चुनें।",
        "coin_detail_header": "<b>{emoji} {name} ({symbol})</b>",
        "price_label": "<b>Price:</b>",
        "change_label": "<b>24hr change:</b>",
        "high_label": "<b>24hr high:</b>",
        "low_label": "<b>24hr low:</b>",
        "market_cap_label": "<b>Market cap:</b>",
        "volume_label": "<b>24hr volume:</b>",
        "source_label": "बाजार डेटा स्रोत: सार्वजनिक मूल्य फ़ीड",
        "generating_chart": "<b>चार्ट लोड हो रहा है</b>\nडेटा प्राप्त किया जा रहा है...",
        "chart_ready": "<b>चार्ट तैयार</b>",
        "chart_error": "<b>चार्ट अनुपलब्ध</b>\n\nपुनः प्रयास करें।",
        "news_prompt": "<b>बाजार समीक्षाएं</b>\n\nनवीनतम बाजार घटनाक्रम और सुर्खियां।",
        "news_enabled": "समीक्षाएं सक्षम\n\nआप बाजार अपडेट प्राप्त करेंगे।",
        "news_disabled": "समीक्षाएं अक्षम\n\nबाजार अपडेट बंद हैं।",
        "fetching_news": "<b>लेख लोड किए जा रहे हैं</b>\nनवीनतम डेटा प्राप्त किया जा रहा है...",
        "news_unavailable": "<b>लेख अनुपलब्ध</b>\n\nस्रोत अस्थायी रूप से अनुपलब्ध है। बाद में प्रयास करें।",
        "latest_news": "<b>बाजार समाचार</b>",
        "news_item": "<b>{title}</b>\nस्रोत: {source}",
        "no_news": "कोई लेख उपलब्ध नहीं\n\nबाद में देखें।",
        "converter_title": "<b>मूल्य अनुमानक</b>\n\nलाइव बाजार दरों के आधार पर विभिन्न संपत्तियों और मुद्राओं में समतुल्य मूल्यों की गणना करें।",
        "select_coin": "<b>चरण 1 - संपत्ति चुनें</b>\n\nवह संपत्ति चुनें जिसे आप कन्वर्ट करना चाहते हैं।",
        "select_type": "<b>चरण 2 - लक्ष्य प्रकार</b>\n\nफिएट या क्रिप्टो में कन्वर्ट करें?",
        "select_target": "<b>चरण 3 - लक्ष्य चुनें</b>\n\nलक्ष्य मुद्रा या संपत्ति चुनें।",
        "enter_amount": "<b>चरण 4 - राशि दर्ज करें</b>\n\nकन्वर्ट करने के लिए {coin} की राशि दर्ज करें।\n\nएक सकारात्मक संख्या दर्ज करें।",
        "to_fiat_button": "💵 फिएट",
        "to_crypto_button": "🪙 क्रिप्टो",
        "conversion_result": "<b>कन्वर्ज़न परिणाम</b>\n\n{amount} {coin_symbol} = {result} {target_symbol}\n\nवर्तमान बाजार दरों पर आधारित।",
        "invalid_amount": "<b>अमान्य राशि</b>\n\nएक सकारात्मक संख्या दर्ज करें।",
        "conversion_error": "<b>कन्वर्ज़न अनुपलब्ध</b>\n\nदरें प्राप्त नहीं हो सकीं। पुनः प्रयास करें।",
        "settings_title": "<b>सेटिंग्स</b>\n\nअपनी प्राथमिकताएं प्रबंधित करें।",
        "language_button": "🌐 भाषा",
        "news_toggle_button": "📰 बाजार समीक्षाएं",
        "news_status": "<b>सेटिंग्स</b>\n\nबाजार समीक्षाएं: {status}",
        "on": "सक्षम",
        "off": "अक्षम",
        "error_timeout": "<b>अनुरोध टाइमआउट</b>\n\nपुनः प्रयास करें।",
        "error_connection": "<b>कनेक्शन त्रुटि</b>\n\nडेटा स्रोत अनुपलब्ध। पुनः प्रयास करें।",
        "error_generic": "<b>कुछ गलत हो गया</b>\n\nकृपया पुनः प्रयास करें।",
        "privacy_text": (
            "<b>गोपनीयता</b>\n\n"
            "Flux आपका Telegram ID, भाषा प्राथमिकता और बाजार समीक्षा सेटिंग संग्रहीत करता है।\n\n"
            "कोई वॉलेट पता, निजी कुंजी, सीड वाक्यांश या वित्तीय डेटा कभी नहीं मांगा या संग्रहीत नहीं किया जाता।\n\n"
            "बाजार डेटा सार्वजनिक APIs से प्राप्त किया जाता है। आप किसी भी समय उपयोग बंद कर सकते हैं।"
        ),
        "terms_text": (
            "<b>उपयोग की शर्तें</b>\n\n"
            "Flux केवल सूचनात्मक बाजार डेटा प्रदान करता है। "
            "यह निवेश सलाह, ब्रोकर, एक्सचेंज या वॉलेट नहीं है।\n\n"
            "मूल्य, चार्ट, कन्वर्ज़न और समीक्षाएं विलंबित या अनुपलब्ध हो सकती हैं। "
            "हमेशा डेटा को स्वतंत्र रूप से सत्यापित करें।\n\n"
            "निजी कुंजी, सीड वाक्यांश, पासवर्ड या वित्तीय क्रेडेंशियल किसी भी बॉट के साथ साझा न करें।"
        ),
        "support_text": (
            "<b>सहायता</b>\n\n"
            "मेनू पर लौटने के लिए /start का उपयोग करें या बॉट स्वामी से Telegram प्रोफाइल के माध्यम से संपर्क करें।\n\n"
            "Flux कभी भी वॉलेट एक्सेस, निजी कुंजी या पासवर्ड नहीं मांगेगा।"
        ),
        "typing": "typing",
        "uploading": "uploading photo",
    },
    "zh": {
        "welcome": (
            "<b>Flux</b>\n\n"
            "查看实时市场数据，追踪价格变动，比较资产价值。\n\n"
            "<i>仅供参考。不提供任何财务建议。</i>"
        ),
        "choose_language": "<b>语言</b>\n\n选择您的首选语言：",
        "language_saved": "<b>语言已保存</b>\n\n您的选择已保存。",
        "main_menu": (
            "<b>Flux</b>\n\n"
            "查看实时市场数据，追踪价格变动，比较资产价值。\n\n"
            "<i>仅供参考。不提供任何财务建议。</i>"
        ),
        "prices_button": "📊 市场数据",
        "news_button": "📰 市场简报",
        "converter_button": "🔄 价值估算",
        "settings_button": "⚙️ 设置",
        "help_button": "ℹ️ 关于",
        "privacy_button": "隐私",
        "terms_button": "条款",
        "support_button": "支持",
        "back_button": "← 返回",
        "refresh_button": "⟳ 刷新",
        "home_button": "首页",
        "prices_title": "<b>市场价格</b>\n\n选择一项资产查看当前市场数据。",
        "coin_detail_header": "<b>{emoji} {name} ({symbol})</b>",
        "price_label": "<b>Price:</b>",
        "change_label": "<b>24hr change:</b>",
        "high_label": "<b>24hr high:</b>",
        "low_label": "<b>24hr low:</b>",
        "market_cap_label": "<b>Market cap:</b>",
        "volume_label": "<b>24hr volume:</b>",
        "source_label": "市场数据来源：公共价格接口",
        "generating_chart": "<b>加载图表</b>\n正在获取价格历史...",
        "chart_ready": "<b>图表已就绪</b>",
        "chart_error": "<b>图表不可用</b>\n\n请稍后重试。",
        "news_prompt": "<b>市场简报</b>\n\n最新市场动态和头条新闻。",
        "news_enabled": "简报已启用\n\n您将收到市场更新。",
        "news_disabled": "简报已禁用\n\n市场更新已关闭。",
        "fetching_news": "<b>加载文章</b>\n正在获取最新数据...",
        "news_unavailable": "<b>暂无简报</b>\n\n新闻源暂时不可用。请稍后查看。",
        "latest_news": "<b>最新简报</b>",
        "news_item": "<b>{title}</b>\n来源：{source}",
        "no_news": "暂无文章\n\n稍后查看。",
        "converter_title": "<b>资产转换器</b>\n\n使用实时汇率计算不同货币和资产的等值价值。",
        "select_coin": "<b>步骤 1 - 选择资产</b>\n\n选择您要转换的资产。",
        "select_type": "<b>步骤 2 - 目标类型</b>\n\n转换为法币还是另一种加密货币？",
        "select_target": "<b>步骤 3 - 选择目标</b>\n\n选择目标货币或资产。",
        "enter_amount": "<b>步骤 4 - 输入金额</b>\n\n输入要转换的 {coin} 数量。\n\n请输入正数。",
        "to_fiat_button": "💵 法币",
        "to_crypto_button": "🪙 加密",
        "conversion_result": "<b>转换结果</b>\n\n{amount} {coin_symbol} = {result} {target_symbol}\n\n基于当前市场汇率。",
        "invalid_amount": "<b>无效金额</b>\n\n请输入正数。",
        "conversion_error": "<b>转换不可用</b>\n\n无法获取汇率。请重试。",
        "settings_title": "<b>设置</b>\n\n管理您的偏好设置。",
        "language_button": "🌐 语言",
        "news_toggle_button": "📰 简报",
        "news_status": "<b>设置</b>\n\n简报：{status}",
        "on": "已启用",
        "off": "已禁用",
        "error_timeout": "<b>请求超时</b>\n\n请稍后重试。",
        "error_connection": "<b>连接错误</b>\n\n数据源不可达。请重试。",
        "error_generic": "<b>出了点问题</b>\n\n请重试。",
        "privacy_text": (
            "<b>隐私</b>\n\n"
            "Flux 存储您的 Telegram ID、语言偏好和简报设置以记住您的偏好。\n\n"
            "绝不要求或存储钱包地址、私钥、助记词或任何财务数据。\n\n"
            "市场数据来自公共 API。您可以随时停止使用 Flux。"
        ),
        "terms_text": (
            "<b>使用条款</b>\n\n"
            "Flux 仅提供信息性市场数据。它不是投资建议、经纪人、交易所或钱包。\n\n"
            "价格、图表、转换和简报可能延迟或不可用。请始终独立验证数据。\n\n"
            "请勿向任何机器人分享私钥、助记词、密码或财务凭证。"
        ),
        "support_text": (
            "<b>支持</b>\n\n"
            "使用 /start 返回菜单，或通过 Telegram 个人资料联系机器人所有者。\n\n"
            "Flux 绝不会要求钱包访问权限、私钥或密码。"
        ),
        "typing": "typing",
        "uploading": "uploading photo",
    },
    "ja": {
        "welcome": (
            "<b>Flux</b>\n\n"
            "リアルタイムの市場データを表示し、価格の動きを追跡し、資産価値を比較します。\n\n"
            "<i>情報提供のみを目的としています。金融アドバイスを提供するものではありません。</i>"
        ),
        "choose_language": "<b>言語</b>\n\n希望する言語を選択してください：",
        "language_saved": "<b>言語を保存しました</b>\n\n選択が保存されました。",
        "main_menu": (
            "<b>Flux</b>\n\n"
            "リアルタイムの市場データを表示し、価格の動きを追跡し、資産価値を比較します。\n\n"
            "<i>情報提供のみを目的としています。金融アドバイスを提供するものではありません。</i>"
        ),
        "prices_button": "📊 市場データ",
        "news_button": "📰 ヘッドライン",
        "converter_button": "🔄 コンバーター",
        "settings_button": "⚙️ 設定",
        "help_button": "ℹ️ 情報",
        "privacy_button": "プライバシー",
        "terms_button": "利用規約",
        "support_button": "サポート",
        "back_button": "← 戻る",
        "refresh_button": "⟳ 更新",
        "home_button": "ホーム",
        "prices_title": "<b>市場価格</b>\n\n資産を選択して現在の市場データを表示します。",
        "coin_detail_header": "<b>{emoji} {name} ({symbol})</b>",
        "price_label": "<b>Price:</b>",
        "change_label": "<b>24hr change:</b>",
        "high_label": "<b>24hr high:</b>",
        "low_label": "<b>24hr low:</b>",
        "market_cap_label": "<b>Market cap:</b>",
        "volume_label": "<b>24hr volume:</b>",
        "source_label": "市場データソース：公開価格フィード",
        "generating_chart": "<b>チャート読み込み中</b>\n価格履歴を取得中...",
        "chart_ready": "<b>チャート準備完了</b>",
        "chart_error": "<b>チャート利用不可</b>\n\nしばらくしてからもう一度お試しください。",
        "news_prompt": "<b>市場ヘッドライン</b>\n\n最新の市場記事と更新情報。",
        "news_enabled": "ヘッドライン有効\n\n市場更新を受信します。",
        "news_disabled": "ヘッドライン無効\n\n市場更新はオフになっています。",
        "fetching_news": "<b>ヘッドライン読み込み中</b>\n最新の記事を取得中...",
        "news_unavailable": "<b>ヘッドラインなし</b>\n\nニュースソースが利用できません。後でもう一度お試しください。",
        "latest_news": "<b>最新ヘッドライン</b>",
        "news_item": "<b>{title}</b>\nソース：{source}",
        "no_news": "記事なし\n\n後でもう一度確認してください。",
        "converter_title": "<b>資産コンバーター</b>\n\nライブレートを使用して通貨や資産の等価値を計算します。",
        "select_coin": "<b>ステップ 1 - 資産を選択</b>\n\n変換元の資産を選択してください。",
        "select_type": "<b>ステップ 2 - ターゲットタイプ</b>\n\n法定通貨または別の暗号資産に変換しますか？",
        "select_target": "<b>ステップ 3 - ターゲットを選択</b>\n\nターゲットの通貨または資産を選択してください。",
        "enter_amount": "<b>ステップ 4 - 金額を入力</b>\n\n変換する {coin} の金額を入力してください。\n\n正の数を入力してください。",
        "to_fiat_button": "💵 法定通貨",
        "to_crypto_button": "🪙 暗号資産",
        "conversion_result": "<b>変換結果</b>\n\n{amount} {coin_symbol} = {result} {target_symbol}\n\n現在の市場レートに基づきます。",
        "invalid_amount": "<b>無効な金額</b>\n\n正の数を入力してください。",
        "conversion_error": "<b>変換できません</b>\n\nレートを取得できませんでした。もう一度お試しください。",
        "settings_title": "<b>設定</b>\n\n設定を管理します。",
        "language_button": "🌐 言語",
        "news_toggle_button": "📰 ヘッドライン",
        "news_status": "<b>設定</b>\n\nヘッドライン：{status}",
        "on": "有効",
        "off": "無効",
        "error_timeout": "<b>リクエストタイムアウト</b>\n\nしばらくしてからもう一度お試しください。",
        "error_connection": "<b>接続エラー</b>\n\nデータソースに到達できません。もう一度お試しください。",
        "error_generic": "<b>エラーが発生しました</b>\n\nもう一度お試しください。",
        "privacy_text": (
            "<b>プライバシー</b>\n\n"
            "Fluxは、設定を記憶するためにあなたのTelegram ID、言語設定、ヘッドライン設定を保存します。\n\n"
            "ウォレットアドレス、秘密鍵、シードフレーズ、または金融データを要求または保存することはありません。\n\n"
            "市場データは公開APIから取得されます。いつでも使用を中止できます。"
        ),
        "terms_text": (
            "<b>利用規約</b>\n\n"
            "Fluxは情報提供のみの市場データを提供します。"
            "これは投資アドバイス、ブローカー、取引所、またはウォレットではありません。\n\n"
            "価格、チャート、変換、ヘッドラインは遅延または利用不可の場合があります。"
            "常にデータを独自に検証してください。\n\n"
            "秘密鍵、シードフレーズ、パスワード、または金融資格情報をどのボットとも共有しないでください。"
        ),
        "support_text": (
            "<b>サポート</b>\n\n"
            "/startを使用してメニューに戻るか、Telegramプロフィールからボットの所有者にお問い合わせください。\n\n"
            "Fluxはウォレットアクセス、秘密鍵、またはパスワードを要求することはありません。"
        ),
        "typing": "typing",
        "uploading": "uploading photo",
    },
}

def get_message(lang: str, key: str, **kwargs) -> str:
    """
    Get translated message with variable substitution
    
    Args:
        lang: Language code (e.g., 'en', 'ru')
        key: Message key
        **kwargs: Variables for formatting
    
    Returns:
        Translated and formatted message
    """
    messages = MESSAGES.get(lang, MESSAGES["en"])
    message = messages.get(key, MESSAGES["en"].get(key, f"[{key}]"))
    
    try:
        return message.format(**kwargs) if kwargs else message
    except KeyError as e:
        return f"[Missing: {e}]"

def get_language_name(lang_code: str) -> str:
    """Get display name for language code"""
    return LANGUAGES.get(lang_code, lang_code)

