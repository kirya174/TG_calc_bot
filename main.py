from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
from config import token, password

allowed_operators = ['+', '-', '(', ')', '*', '/', '%', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ' ']
password_is_correct = False
welcome_message = "I'm a calc bot, please send me your expression.\n" \
                  "please use these operators in your expression:\n" \
                  "'+', '-', '*', '/', '()';\n" \
                  "'//' for division without remainder;\n" \
                  "'%' for remainder of division;\n" \
                  "'**' for power calculation."


def start(update: Update, context: CallbackContext):
    if not password_is_correct:
        text = "Please, enter the password to access the bot:"
    else:
        text = welcome_message
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def input_handler(update: Update, context: CallbackContext):
    if password_is_correct:
        expression = update.message.text
        expression_is_valid = True
        for char in expression:
            if char not in allowed_operators and expression_is_valid:
                expression_is_valid = False
                text = "Entered expression is not supported, please use these operators:\n" \
                       "'+', '-', '*', '/', '()';\n" \
                       "'//' for division without remainder;\n" \
                       "'%' for remainder of division;\n" \
                       "'**' for power calculation."
                # context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        if expression_is_valid:
            text = eval(update.message.text)
    else:
        entered_password = update.message.text
        if entered_password == password:
            globals()['password_is_correct'] = True
            text = welcome_message
        else:
            text = "Password is not correct, please, try again"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


if __name__ == '__main__':
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    equation_handled = MessageHandler(Filters.text & (~Filters.command), input_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(equation_handled)

    updater.start_polling()
    updater.idle()
