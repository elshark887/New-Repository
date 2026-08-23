import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = "8875256622:AAFITd9tC9O5Y2EcMuTSfNEraN6ihlBWciA"
bot = telebot.TeleBot(TOKEN)

# محفظة الـ USDT (BEP20) المطلوبة للدفع
USDT_WALLET = "0x7Da0273E816bBAB96a6fb7285753330c48CA6Cd5"

# سيرفر وهمي لتجنب نوم الاستضافة المجانية
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 1. القائمة الرئيسية عند كتابة /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_black = types.InlineKeyboardButton("🖤 Black Sol", callback_data="menu_blacksoul")
    btn_visa = types.InlineKeyboardButton("💳 Visa", callback_data="menu_visa")
    markup.add(btn_black, btn_visa)
    
    welcome_text = (
        "🌟 *Welcome to Our Store Bot!* 🌟\n\n"
        "Please choose a category below to browse available options:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# 2. استقبال الضغطات على الأزرار (Callback Queries)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    
    # قائمة خيارات Black Sol
    if call.data == "menu_blacksoul":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("💵 $45 = 5 SOL", callback_data="buy_bs_45")
        btn2 = types.InlineKeyboardButton("💵 $90 = 10 SOL", callback_data="buy_bs_90")
        btn3 = types.InlineKeyboardButton("💵 $120 = 15 SOL", callback_data="buy_bs_120")
        btn4 = types.InlineKeyboardButton("💵 $160 = 20 SOL", callback_data="buy_bs_160")
        btn5 = types.InlineKeyboardButton("💵 $200 = 25 SOL", callback_data="buy_bs_200")
        back_btn = types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_home")
        markup.add(btn1, btn2, btn3, btn4, btn5, back_btn)
        
        bot.edit_message_text("🖤 *Black Sol Section*\nSelect your desired option below:", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup, 
                              parse_mode="Markdown")

    # قائمة خيارات Visa
    elif call.data == "menu_visa":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("💳 Visa - $45 have $400", callback_data="buy_visa_45")
        btn2 = types.InlineKeyboardButton("💳 Visa - $90 have $800", callback_data="buy_visa_90")
        btn3 = types.InlineKeyboardButton("💳 Visa - $120 have $1400", callback_data="buy_visa_120")
        btn4 = types.InlineKeyboardButton("💳 Visa - $160 have $1800", callback_data="buy_visa_160")
        btn5 = types.InlineKeyboardButton("💳 Visa - $200 have $2200", callback_data="buy_visa_200")
        back_btn = types.InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_home")
        markup.add(btn1, btn2, btn3, btn4, btn5, back_btn)
        
        bot.edit_message_text("💳 *Visa Section*\nSelect your desired option below:", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup, 
                              parse_mode="Markdown")

    # زر الرجوع للقائمة الرئيسية
    elif call.data == "back_home":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_black = types.InlineKeyboardButton("🖤 Black Sol", callback_data="menu_blacksoul")
        btn_visa = types.InlineKeyboardButton("💳 Visa", callback_data="menu_visa")
        markup.add(btn_black, btn_visa)
        
        bot.edit_message_text("🌟 *Welcome to Our Store Bot!* 🌟\n\nPlease choose a category below to browse available options:", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup, 
                              parse_mode="Markdown")

    # تفاصيل الدفع عند اختيار أي منتج من Black Sol أو Visa
    elif call.data.startswith("buy_bs_") or call.data.startswith("buy_visa_"):
        # استخراج السعر أو تفاصيل الطلب بناءً على الضغطة
        parts = call.data.split("_")
        category = parts[1].upper() # BS أو VISA
        price = parts[2]
        
        item_name = "Black Sol" if category == "BS" else "Visa"
        
        payment_text = (
            f"🛒 *Order Details:*\n"
            f"• Item: {item_name}\n"
            f"• Price: ${price} USDT\n\n"
            f"📌 *Payment Instructions:*\n"
            f"Please send the exact amount via *USDT (BEP20)* to the wallet address below:\n\n"
            f"`{USDT_WALLET}`\n\n"
            f"⚠️ *Note:* After payment, send a screenshot of the transaction here to confirm your order and txd !"
        )
        
        markup = types.InlineKeyboardMarkup()
        back_btn = types.InlineKeyboardButton("🔙 Back to Menu", callback_data="back_home")
        markup.add(back_btn)
        
        bot.edit_message_text(payment_text, 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup, 
                              parse_mode="Markdown")


if __name__ == "__main__":
    # تشغيل السيرفر في الخلفية
    t = threading.Thread(target=run_web)
    t.start()
    
    # تشغيل البوت
    print("Bot is running with buttons...")
    bot.infinity_polling()
