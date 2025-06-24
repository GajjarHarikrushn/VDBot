import string
import copy

token = "7529239912:AAEFQ6sbf75TqngCv5amCEa1NEL2qP7x0Nk"

vachanamrut = "This is the vachanamrut. Pagh vagha mojadi pah mjadi vgha kesh ph ojadi gha hesh."

vachanamrut_definations = []

definations = {}

buttons = []

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters


def main_buttons():
    keyboard = [
        [InlineKeyboardButton("Definitions", callback_data='defination')]
    ]
    return InlineKeyboardMarkup(keyboard)


def secondary_buttons():
    keyboard = [
        [InlineKeyboardButton("definations from this vachanamrut", callback_data='definations from this vachanamrut')],
        [InlineKeyboardButton("search any vachanamrut definations", callback_data='search any vachanamrut definations')]
    ]
    return InlineKeyboardMarkup(keyboard)


def defination_buttons(caller):
    keyboard = []
    if caller == "definations from this vachanamrut":
        keyboard = copy.deepcopy(buttons[0])
        keyboard.append([InlineKeyboardButton("<<back", callback_data='back'),InlineKeyboardButton("more>>", callback_data='more_0')])
    else:
        index = int(caller.split("_")[1])+1
        if index < len(buttons):
            keyboard = copy.deepcopy(buttons[index])
            callback = f'more_{index+1}'

            if index+1 < len(buttons):
                keyboard.append([InlineKeyboardButton("<<back", callback_data='back'),InlineKeyboardButton("more>>", callback_data=callback)])
            else:
                keyboard.append([InlineKeyboardButton("<<back", callback_data='back')])
        else:
            keyboard.append([InlineKeyboardButton("<<back", callback_data='back')])
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(vachanamrut, reply_markup=main_buttons())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'defination':
        await query.edit_message_reply_markup(reply_markup=secondary_buttons())
    elif query.data == 'definations from this vachanamrut' or 'more' in query.data:
        await query.edit_message_reply_markup(reply_markup=defination_buttons(query.data))
    elif query.data == 'search any vachanamrut definations':
        await query.message.reply_text("send us the word that you want to get the definition of.\nNOTE: you must send the word alone")
    elif query.data == 'back':
        await query.edit_message_reply_markup(reply_markup=main_buttons())
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


with open("definations.txt","r") as file:
    for line in file:
        line = line.split(":")
        definations[line[0].lower()] = line[1]


for word in vachanamrut.split():
    word = word.translate(str.maketrans('', '', string.punctuation)).lower()
    if word in definations:
        vachanamrut_definations.append(word)


keyboard = []
row = []
for i,key in enumerate(vachanamrut_definations):
    row.append(InlineKeyboardButton(key, callback_data=key))
    if (i+1) % 2 == 0:
        keyboard.append(row)
        row = []
    elif i+1 == len(vachanamrut_definations):
        buttons.append([row])
        row = []
        keyboard = []
    if (i+1)%10 == 0:
        buttons.append(keyboard)
        row = []
        keyboard = []


app = Application.builder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT& ~filters.COMMAND, handle_message))
app.run_polling()
    