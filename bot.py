import os
import threading
from flask import Flask
import telebot
from telebot import types

TOKEN = "8875256622:AAFITd9tC9O5Y2EcMuTSfNEraN6ihlBWciA"
bot = telebot.TeleBot(TOKEN)

# سيرفر وهمي لتجنب نوم الاستضافة المجانية
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 1. أمر /start لإظهار القائمة الرئيسية (الزرين الأساسيين)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_black = types.InlineKeyboardButton("بلاك سول", callback_data="menu_blacksoul")
    btn_visa = types.InlineKeyboardButton("فيزا", callback_data="menu_visa")
    markup.add(btn_black, btn_visa)
    
    bot.send_message(message.chat.id, "أهلاً بك! اختر أحد الأقسام أدناه:", reply_markup=markup)

# 2. استقبال الضغطات على الأزرار (Callback Queries)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # إذا ضغط على زر "بلاك سول"
    if call.data == "menu_blacksoul":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("خيارات بلاك سول 1", callback_data="bs_1")
        btn2 = types.InlineKeyboardButton("خيارات بلاك سول 2", callback_data="bs_2")
        back_btn = types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_home")
        markup.add(btn1, btn2, back_btn)
        
        bot.edit_message_text("أنت الآن في قسم **بلاك سول**، اختر ما يناسبك:", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup, 
                              parse_mode="Markdown")

    # إذا ضغط على زر "فيزا"
    elif call.data == "menu_visa":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("خيارات الفيزا 1", callback_data="visa_1")
        btn2 = types.InlineKeyboardButton("خيارات الفيزا 2", callback_data="visa_2")
        back_btn = types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_home")
        markup.add(btn1, btn2, back_btn)
        
        bot.edit_message_text("أنت الآن في قسم **الفيزا**، اختر ما يناسبك:", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup, 
                              parse_mode="Markdown")

    # زر الرجوع للقائمة الرئيسية
    elif call.data == "back_home":
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_black = types.InlineKeyboardButton("بلاك سول", callback_data="menu_blacksoul")
        btn_visa = types.InlineKeyboardButton("فيزا", callback_data="menu_visa")
        markup.add(btn_black, btn_visa)
        
        bot.edit_message_text("أهلاً بك! اختر أحد الأقسام أدناه:", 
                              chat_id=call.message.chat.id, 
                              message_id=call.message.message_id, 
                              reply_markup=markup)

    # تفاعل مع الخيارات الفرعية الداخلية
    elif call.data.startswith("bs_") or call.data.startswith("visa_"):
        bot.answer_callback_query(call.id, text="تم اختيار هذا الخيار بنجاح! 🚀", show_alert=True)


if __name__ == "__main__":
    # تشغيل السيرفر في الخلفية
    t = threading.Thread(target=run_web)
    t.start()
    
    # تشغيل البوت
    print("البوت يعمل مع الأزرار...")
    bot.infinity_polling()