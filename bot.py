import os
import telebot
import requests
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


def get_daily_horoscope(sign: str, day: str) -> dict:
  
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params=params)
    return response.json()


@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = (
        "🔮 *What's your zodiac sign?*\n"
        "_Choose one:_\n"
        "`Aries`, `Taurus`, `Gemini`, `Cancer`, `Leo`, `Virgo`, `Libra`, `Scorpio`, "
        "`Sagittarius`, `Capricorn`, `Aquarius`, `Pisces`"
    )
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text.strip()
    text = (
        "📅 *What day do you want the horoscope for?*\n"
        "_Options:_ `TODAY`, `TOMORROW`, `YESTERDAY`, or enter date as `YYYY-MM-DD`."
    )
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

def fetch_horoscope(message, sign):
    day = message.text.strip().upper()
    try:
        horoscope = get_daily_horoscope(sign, day)
        if horoscope.get("success"):
            data = horoscope["data"]
            horoscope_message = (
                f"*🌟 Horoscope for {sign}*\n"
                f"*Date:* {data['date']}\n"
                f"*Message:* {data['horoscope_data']}"
            )
            bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
        else:
            bot.send_message(message.chat.id, "⚠️ Failed to fetch horoscope. Please try again.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {e}")


print("🤖 Horoscope Bot is running...")
bot.polling(non_stop=True)
