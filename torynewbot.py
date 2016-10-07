# import time
# import random
# import datetime
# import telepot
import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    command = msg['text']
    print 'Got command: %s' % command
    if command == '/roll':
        button_text = random.randint(1,6)
    elif command == '/time':
        button_text = str(datetime.datetime.now())
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Press me', callback_data='press')],
               ])
    bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print msg['message']['text']
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='got it')


# TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.Bot("264200303:AAEqnIU8cnDmbFfRZuxVD5pfkRwXAJgxH10")
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')

while 1:
    time.sleep(10)

# def handle(msg):
#     # chat_id = msg['chat']['id']
#     content_type, chat_type, chat_id = telepot.glance(msg)
#     command = msg['text']
#     print 'Got command: %s' % command
#     if command == '/roll':
#         bot.sendMessage(chat_id, random.randint(1,6))
#     elif command == '/time':
#         bot.sendMessage(chat_id, str(datetime.datetime.now()))
#
# bot = telepot.Bot("264200303:AAEqnIU8cnDmbFfRZuxVD5pfkRwXAJgxH10")
# bot.message_loop(handle)
# print 'I am listening ...'
#
# while 1:
#     time.sleep(10)