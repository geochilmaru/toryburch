import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from db import get_categories


def show_categories(show_type):
    cate_ordered = [{'CATEGORY': 'View All', 'COUNT': 0},
        {'CATEGORY': 'New Arrivals', 'COUNT': 0},
        {'CATEGORY': 'Baby Bags', 'COUNT': 0},
        {'CATEGORY': 'Backpacks', 'COUNT': 0},
        {'CATEGORY': 'Clutches & Evening Bags', 'COUNT': 0},
        {'CATEGORY': 'Cross-Body Bags', 'COUNT': 0},
        {'CATEGORY': 'Mini Bags', 'COUNT': 0},
        {'CATEGORY': 'Satchels & Shoulder Bags', 'COUNT': 0},
        {'CATEGORY': 'Totes', 'COUNT': 0},
        {'CATEGORY': 'Sale', 'COUNT': 0}]
    cate = get_categories(show_type)
    if len(cate) == 1:
        cate_ordered = cate
    else:
        for co in cate_ordered:
            for c in cate:
                if c.get("CATEGORY") == co.get("CATEGORY"):
                    if c.get("COUNT") == "":
                        co["COUNT"] = "0"
                    else:
                        co["COUNT"] = str(c["COUNT"])
    return cate_ordered


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    inline_kb = []
    command = msg['text']
    print 'Got command: %s' % command
    if command.upper() == '/ALL' or command.upper() == '/SALE':
        categories = show_categories(command)
        # cate_names = ('View All', 'New Arrivals', 'Baby Bags', 'Backpacks'
        #     , 'Clutches & Evening Bags', 'Cross-Body Bags', 'Mini Bags'
        #     , 'Satchels & Shoulder Bags', 'Totes', 'Sale')
        for cate in categories:
            inline_kb.append([InlineKeyboardButton(text=cate["CATEGORY"] +'('+ str(cate["COUNT"]) +')'
                                                   , callback_data=cate["CATEGORY"])])
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_kb)
        bot.sendMessage(chat_id, 'Results', reply_markup=keyboard)

    # if command == '/help':
    #     bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)
    # elif command == '/time':
    #     button_text = str(datetime.datetime.now())
    # keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #     [InlineKeyboardButton(text='Press me1', callback_data='press1')],
    #     [InlineKeyboardButton(text='Press me2', callback_data='press2')],
    #            ])
    # bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)


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