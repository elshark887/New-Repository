import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = "8875256622:AAFITd9tC9O5Y2EcMuTSfNEraN6ihlBWciA"
bot = telebot.TeleBot(TOKEN)

# محفظة الـ USDT (BEP20) المطلوبة للدفع
USDT_WALLET = "0xeeabeb6520394f2e910547e7431df6b2401a92ef"

# تخزين لغة المستخدم المؤقتة
user_languages = {}

# سيرفر وهمي لتجنب نوم الاستضافة المجانية
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 1. الترحيب التلقائي فور دخول المستخدم (عند إرسال أي رسالة أو فتح البوت)
@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    chat_id = message.chat.id
    
    # محاولة تنظيف رسالة المستخدم قدر الإمكان
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_start = types.InlineKeyboardButton("✨ Enter Renna Black Sol Bot ✨", callback_data="start_bot_action")
    markup.add(btn_start)
    
    welcome_text = "Welcome to renna Black Sol Bot!"
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# 2. استقبال الضغطات على الأزرار (Callback Queries)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    user_lang = user_languages.get(chat_id, "ar")

    # الانتقال لوظيفة البوت الطبيعية واختيار اللغة عند الضغط على زر الدخول
    if call.data == "start_bot_action":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_ar = types.InlineKeyboardButton(" العربية", callback_data="lang_ar")
        btn_en = types.InlineKeyboardButton(" English", callback_data="lang_en")
        markup.add(btn_ar, btn_en)
        
        lang_text = (
            "🌟 *Welcome to renna Store Bot!*\n"
            "مرحباً بك في بوت المتجر!\n\n"
            "Please choose your language / يرجى اختيار لغتك:"
        )
        bot.edit_message_text(lang_text, chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    # اختيار اللغة العربية
    elif call.data == "lang_ar":
        user_languages[chat_id] = "ar"
        show_main_menu(call.message, "ar")

    # اختيار اللغة الإنجليزية
    elif call.data == "lang_en":
        user_languages[chat_id] = "en"
        show_main_menu(call.message, "en")

    # قائمة خيارات Black Sol
    elif call.data == "menu_blacksoul":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("💵 $35 = 3.8 SOL", callback_data="buy_bs_35")
        btn2 = types.InlineKeyboardButton("💵 $90 = 7.5 SOL", callback_data="buy_bs_90")
        btn3 = types.InlineKeyboardButton("💵 $120 = 11 SOL", callback_data="buy_bs_120")
        btn4 = types.InlineKeyboardButton("💵 $160 = 15 SOL", callback_data="buy_bs_160")
        btn5 = types.InlineKeyboardButton("💵 $200 = 22 SOL", callback_data="buy_bs_200")
        
        back_text = "🔙 العودة للقائمة" if user_lang == "ar" else "🔙 Back to Main Menu"
        clear_text = "🗑️ مسح الكل (Clear)" if user_lang == "ar" else "🗑️ Clear All"
        
        back_btn = types.InlineKeyboardButton(back_text, callback_data="back_home")
        clear_btn = types.InlineKeyboardButton(clear_text, callback_data="clear_chat")
        markup.add(btn1, btn2, btn3, btn4, btn5, back_btn, clear_btn)
        
        text = "🖤 *قسم Black Sol*\nاختر الخيار المناسب لك أدناه:" if user_lang == "ar" else "🖤 *Black Sol Section*\nSelect your desired option below:"
        bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    # قائمة خيارات Visa
    elif call.data == "menu_visa":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("💳 Visa - $35 have $400", callback_data="buy_visa_35")
        btn2 = types.InlineKeyboardButton("💳 Visa - $90 have $800", callback_data="buy_visa_90")
        btn3 = types.InlineKeyboardButton("💳 Visa - $120 have $1400", callback_data="buy_visa_120")
        btn4 = types.InlineKeyboardButton("💳 Visa - $160 have $1800", callback_data="buy_visa_160")
        btn5 = types.InlineKeyboardButton("💳 Visa - $200 have $2200", callback_data="buy_visa_200")
        
        back_text = "🔙 العودة للقائمة" if user_lang == "ar" else "🔙 Back to Main Menu"
        clear_text = "🗑️ مسح الكل (Clear)" if user_lang == "ar" else "🗑️ Clear All"
        
        back_btn = types.InlineKeyboardButton(back_text, callback_data="back_home")
        clear_btn = types.InlineKeyboardButton(clear_text, callback_data="clear_chat")
        markup.add(btn1, btn2, btn3, btn4, btn5, back_btn, clear_btn)
        
        text = "💳 *قسم Visa*\nاختر الخيار المناسب لك أدناه:" if user_lang == "ar" else "💳 *Visa Section*\nSelect your desired option below:"
        bot.edit_message_text(text, chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    # زر الرجوع للقائمة الرئيسية
    elif call.data == "back_home":
        show_main_menu(call.message, user_lang, edit=True)

    # زر مسح الرسالة تماماً وكأن شيئاً لم يكن
    elif call.data == "clear_chat":
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except Exception:
            pass

    # تفاصيل الدفع عند اختيار أي منتج من Black Sol أو Visa
    elif call.data.startswith("buy_bs_") or call.data.startswith("buy_visa_"):
        parts = call.data.split("_")
        category = parts[1].upper()
        price = parts[2]
        
        item_name = "Black Sol" if category == "BS" else "Visa"
        
        if user_lang == "ar":
            payment_text = (
                f"🛒 *تفاصيل الطلب:*\n"
                f"• المنتج: {item_name}\n"
                f"• السعر: ${price} USDT\n\n"
                f"📌 *تعليمات الدفع:*\n"
                f"يرجى إرسال المبلغ بالضبط عبر شبكة *USDT (BEP20)* إلى عنوان المحفظة أدناه:\n\n"
                f"`{USDT_WALLET}`\n\n"
                f"⚠️ *ملاحظة:* بعد الدفع، أرسل لقطة écran (صورة) للتحويل هنا لتأكيد طلبك و txd !"
            )
            back_text = "🔙 العودة للقائمة"
            clear_text = "🗑️ مسح الكل (Clear)"
        else:
            payment_text = (
                f"🛒 *Order Details:*\n"
                f"• Item: {item_name}\n"
                f"• Price: ${price} USDT\n\n"
                f"📌 *Payment Instructions:*\n"
                f"Please send the exact amount via *USDT (BEP20)* to the wallet address below:\n\n"
                f"`{USDT_WALLET}`\n\n"
                f"⚠️ *Note:* After payment, send a screenshot of the transaction here to confirm your order and txd !"
            )
            back_text = "🔙 Back to Menu"
            clear_text = "🗑️ Clear All"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        back_btn = types.InlineKeyboardButton(back_text, callback_data="back_home")
        clear_btn = types.InlineKeyboardButton(clear_text, callback_data="clear_chat")
        markup.add(back_btn, clear_btn)
        
        bot.edit_message_text(payment_text, chat_id=chat_id, message_id=call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# دالة عرض القائمة الرئيسية
def show_main_menu(message, lang, edit=True):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if lang == "ar":
        btn_black = types.InlineKeyboardButton("🖤 Black Sol", callback_data="menu_blacksoul")
        btn_visa = types.InlineKeyboardButton("💳 Visa", callback_data="menu_visa")
        clear_btn = types.InlineKeyboardButton("🗑️ مسح الرسالة (Clear)", callback_data="clear_chat")
        markup.add(btn_black, btn_visa, clear_btn)
        text = "🌟 *مرحباً بك في بوت المتجر!* 🌟\n\nالرجاء اختيار القسم المطلوب تصفحه أدناه:"
    else:
        btn_black = types.InlineKeyboardButton("🖤 Black Sol", callback_data="menu_blacksoul")
        btn_visa = types.InlineKeyboardButton("💳 Visa", callback_data="menu_visa")
        clear_btn = types.InlineKeyboardButton("🗑️ Clear Chat", callback_data="clear_chat")
        markup.add(btn_black, btn_visa, clear_btn)
        text = "🌟 *Welcome to Our Store Bot!* 🌟\n\nPlease choose a category below to browse available options:"

    if edit:
        try:
            bot.edit_message_text(text, chat_id=message.chat.id, message_id=message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception:
            bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    
    print("Bot is running...")
    bot.infinity_polling()
