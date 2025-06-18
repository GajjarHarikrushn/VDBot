from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        if update.message.text == "/start":
            await update.message.reply_text("Jay Swaminarayan.\nWelcome to the Vachanamrut Dictionary bot.")
        else:
            await update.message.reply_text("That is not the start command.")

if __name__ == '__main__':
    app = ApplicationBuilder().token("7529239912:AAEFQ6sbf75TqngCv5amCEa1NEL2qP7x0Nk").build()
    
    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()
