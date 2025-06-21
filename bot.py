import array
token = "7529239912:AAEFQ6sbf75TqngCv5amCEa1NEL2qP7x0Nk"

vachanamrut = "This is the vachanamrut."

definations = {"vagha":"the term pagh or pagdi generally refers to a turban, a headdress worn by men, particularly in certain regions and on special occasions",
               "pagh":"mojadi typically refers to traditional Indian shoes, often embellished and worn by men, particularly during weddings and other festive occasions",
               "mojadi":"the clothing, or attire, worn by deities, particularly images or statues of deities, like those of Lord Krishna or Swaminarayan, during worship or festivals",
               "khesh":"Khesh refers to a type of handwoven fabric, often used in traditional Indian clothing like the dhoti or kurta"
            }

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# First set of buttons
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Definitions", callback_data='defination')]
    ]
    return InlineKeyboardMarkup(keyboard)

# Second set of buttons
def get_secondary_keyboard():
    keyboard = [
        [InlineKeyboardButton("definations from this vachanamrut", callback_data='definations from this vachanamrut')],
        [InlineKeyboardButton("search any vachanamrut definations", callback_data='search any vachanamrut definations')]
    ]
    return InlineKeyboardMarkup(keyboard)


# Second set of buttons
def get_third_keyboard():
    keyboard = []
    for key in definations:
        keyboard.append([InlineKeyboardButton(key, callback_data=key)])
    
    keyboard.append([InlineKeyboardButton("<<back", callback_data='back')])
    return InlineKeyboardMarkup(keyboard)



# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(vachanamrut, reply_markup=get_main_keyboard())

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
        await query.edit_message_reply_markup(reply_markup=get_secondary_keyboard())

    elif query.data == 'definations from this vachanamrut':
        await query.edit_message_reply_markup(reply_markup=get_third_keyboard())
    elif query.data == 'search any vachanamrut definations':
        await query.message.reply_text("send us the word that you want to get the definition of.\nNOTE: you must send the word alone")
    elif query.data == 'back':
        await query.edit_message_reply_markup(reply_markup=get_main_keyboard())
    elif query.data in definations:
        await query.message.reply_text(definations[query.data])
    else:
        await query.message.reply_text("Sorry, that command didn't work.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    if text in definations:
        await update.message.reply_text(definations[text])
    else:
        await update.message.reply_text("Sorry, no definition found for that word.")


# Bot setup
app = Application.builder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT& ~filters.COMMAND, handle_message))
app.run_polling()
    