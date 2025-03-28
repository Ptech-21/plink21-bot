import telebot
import firebase_admin
from firebase_admin import credentials, db

# ✅ Replace with your real Telegram Bot API token (DO NOT SHARE PUBLICLY)
API_TOKEN = "7835083999:AAG-cV5A6t8msRTBQyMZ7FxBBzaL-wxBoyE"
bot = telebot.TeleBot(API_TOKEN)

# ✅ Replace with your Firebase credentials JSON file
cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://e-commerce-b929a.firebaseapp.com/'})

# ✅ Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Plink21! How can we help you today? 😊\n\n"
                          "Use /faq to see common questions\n"
                          "Use /order to track your order\n"
                          "Use /register to save your details")

# ✅ Auto-reply for FAQs
faq_responses = {
    "price": "Our pricing starts from $10. Visit www.plink21.com for details.",
    "services": "We offer Marketing, E-commerce, and IT solutions.",
    "contact": "📞 Call us: 0983412121 \n✉️ Email: plink2121@gmail.com",
}

@bot.message_handler(commands=['faq'])
def faq_menu(message):
    bot.reply_to(message, "Type one of the following: \n- price \n- services \n- contact")

@bot.message_handler(func=lambda msg: msg.text.lower() in faq_responses.keys())
def reply_faq(message):
    bot.reply_to(message, faq_responses[message.text.lower()])

# ✅ Order Tracking
@bot.message_handler(commands=['order'])
def order_track(message):
    bot.reply_to(message, "Enter your Order ID:")

@bot.message_handler(func=lambda msg: msg.text.isnumeric())
def track_order(message):
    bot.reply_to(message, f"Your order #{message.text} is being processed. 🚀")

# ✅ User Registration (Lead Generation)
@bot.message_handler(commands=['register'])
def register_user(message):
    user_data = {
        "user_id": message.chat.id,
        "name": message.chat.first_name,
        "username": message.chat.username
    }
    ref = db.reference("customers")
    ref.child(str(message.chat.id)).set(user_data)
    bot.reply_to(message, "You're registered! 🎉")

# ✅ Send Broadcast Message (Admin Only)
def send_broadcast(message):
    user_list = db.reference("customers").get()
    if user_list:
        for user_id in user_list.keys():
            bot.send_message(user_id, message)

# ✅ Run the bot 24/7
print("Bot is running...")
bot.polling()
