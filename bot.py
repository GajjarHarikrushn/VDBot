token = "7529239912:AAEFQ6sbf75TqngCv5amCEa1NEL2qP7x0Nk"

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# First set of buttons
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Definitions", callback_data='defination')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Second set of buttons
def get_secondary_keyboard(message):
    keyboard = [
        [InlineKeyboardButton(message, callback_data='heres the definition')],
        [InlineKeyboardButton(message, callback_data='type the name in the message below and send it')]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Choose an option:", reply_markup=get_main_keyboard())

# Callback query handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # if query.data == 'hello':
    #     # Send a new message (preserve original)
    #     await query.message.chat.send_message("Hello there!", reply_markup=get_main_keyboard())

    if query.data == 'defination':
        # Edit the original message in-place (replace both text and buttons)
        # await query.edit_message_text("Hi there!", reply_markup=get_secondary_keyboard())
        # change the buttons without changing the text
        await query.edit_message_reply_markup(reply_markup=get_secondary_keyboard("bye"))

    elif query.data == 'bye':
        await query.message.reply_text("Goodbye!")
    elif query.data == 'byebye':
        await query.message.reply_text("Bye Bye 👋")

# Bot setup
app = Application.builder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()
