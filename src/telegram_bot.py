# 📂 src/telegram_bot.py - Bot de Telegram para gestión de tickets
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "TU_TELEGRAM_BOT_TOKEN"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bienvenido al bot de gestión de tickets. Usa /crear_ticket para generar uno.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()