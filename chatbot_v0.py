## chatbot.py
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import firebase_admin
from firebase_admin import db
# The messageHandler is used for all message updates
import configparser
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


### You need to download your own service account key file and store it together with your PY files
cred_obj = firebase_admin.credentials.Certificate('22451498.json')

### Check the database URL and storage URL from your Firebase console
### Replace the databaseURL and storageBucket with your owns
firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://comp7510-71dfe-default-rtdb.firebaseio.com/',
    'storageBucket':'comp7510-71dfe.appspot.com'
	})

comment_flag = 0
msg = ''
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)


    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("list", list))
    dispatcher.add_handler(CommandHandler("view", show_comment))
    dispatcher.add_handler(CommandHandler("write", write_comment))

    # To start the bot:
    updater.start_polling()
    updater.idle()



def echo(update, context):
    global comment_flag
    global msg
    if comment_flag == 1:
        db_ref = db.reference('/')
        data = db_ref.child('Films').get()
        reply_message = update.message.text
        logging.info("Update: " + str(update))
        logging.info("context: " + str(context))
        for key in data.keys():
            if msg == key:
                db_ref.child('Films/' + msg + '/comment').push(reply_message)
                update.message.reply_text('Comment successfully.')
                # data = db_ref.child('Films/'+msg+'/comment').get()
                # context.bot.send_message(chat_id=update.effective_chat.id, text=data)
                flag = 1
                comment_flag = 0
                break

        if flag == 0:
            update.message.reply_text('Can not find the movie')

        # db_ref = db.reference('/')
        # data = db_ref.child('Films/Howard the Duck/RottenTomatoes').get()
        # reply_message = update.message.text.upper()
        # reply_message1 = update.message.text
        # logging.info("Update: " + str(update))
        # logging.info("context: " + str(context))
        # context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message+data+reply_message1)

def help_command(update: Update, context: CallbackContext) -> None:
    try:
        """Send a message when the command /help is issued."""
        update.message.reply_text('Command menu~')
        update.message.reply_text('Usage: /list\nList all the movies.')
        update.message.reply_text('Usage: /view <movie name>\nSee the comments of the selected movie.')
        update.message.reply_text('Usage: /write <movie name>\nWrite comment for the selected movie.')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /help')

def list(update, context):
    try:
        db_ref = db.reference('/')
        data = db_ref.child('Films').get()
        for key in data.keys():
            context.bot.send_message(chat_id=update.effective_chat.id, text=key)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /list')

def show_comment(update: Update, context: CallbackContext) -> None:
    try:
        # global redis1
        flag = 0
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        # context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        db_ref = db.reference('/')
        data = db_ref.child('Films').get()
        for key in data.keys():
            if msg == key:
                flag = 1
                data = db_ref.child('Films/'+msg+'/comment/').get()
                if data == '':
                    update.message.reply_text('The movie has no comments.')
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=data)
                break

        if flag == 0:
            update.message.reply_text('Can not find the movie')

        # redis1.incr(msg)
        # update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /view <movie name>')

def write_comment(update: Update, context: CallbackContext) -> None:
    try:
        global comment_flag
        global msg
        comment_flag = 1
        flag = 0
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        # context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
        # logging.info(context.args[4])
        # msg1 = context.args[4]
        update.message.reply_text('Please write the comment.')


        # msg1 = context.args[4] # /add keyword <-- this should store the keyword
        # context.bot.send_message(chat_id=update.effective_chat.id, text=msg1)
        # db_ref = db.reference('/')
        # data = db_ref.child('Films').get()
        # for key in data.keys():
        #     if msg == key:
        #         db_ref.child('Films/' + msg + '/comment').push(msg1)
        #         update.message.reply_text('Comment successfully.')
        #         # data = db_ref.child('Films/'+msg+'/comment').get()
        #         # context.bot.send_message(chat_id=update.effective_chat.id, text=data)
        #         flag = 1
        #         break
        #
        # if flag == 0:
        #     update.message.reply_text('Can not find the movie')

        # redis1.incr(msg)
        # update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /write <movie name>')




if __name__ == '__main__':
    main()

