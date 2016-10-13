import sys
import time
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from db import get_categories


def show_categories(show_type):
    cate_ordered = [{'CATEGORY': 'View All', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'New Arrivals', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Baby Bags', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Backpacks', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Clutches & Evening Bags', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Cross-Body Bags', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Hobos', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Mini Bags', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Satchels & Shoulder Bags', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Totes', 'COUNT': 0, 'CATEGORY_URL': ''},
        {'CATEGORY': 'Sale', 'COUNT': 0, 'CATEGORY_URL': ''}]
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
                    co["CATEGORY_URL"] = c.get("CATEGORY_URL")
    return cate_ordered


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    inline_kb = []
    command = msg['text'].upper()
    print 'Got command: %s' % msg['text']
    if command == "VIEW ALL (/ALL)":
        command = "/ALL"
    elif command == "ON SALE (/SALE)":
        command = "/SALE"
    if command == '/ALL' or command == '/SALE':
        categories = show_categories(command)
        for cate in categories:
            inline_kb.append([InlineKeyboardButton(text=cate["CATEGORY"] +'('+ str(cate["COUNT"]) +')'
                                                   , callback_data=cate["CATEGORY"], url=cate["CATEGORY_URL"])])
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_kb)
        bot.sendMessage(chat_id, 'Results', reply_markup=keyboard)
    keyboard_layout = [["View All (/all)"], ["On Sale (/sale)"]]
    reply_keyboard_makeup = {'keyboard': keyboard_layout, 'resize_keyboard': True, 'one_time_keyboard': True}
    bot.sendMessage(chat_id, 'Choose One', reply_markup=reply_keyboard_makeup)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    # print msg['message']['text']
    print('Callback Query:', query_id, from_id, query_data)
    bot.answerCallbackQuery(query_id, text='got it', show_alert=False)


TOKEN = sys.argv[1]  # get token from command-line
bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})

print('Listening ...')

while 1:
    time.sleep(10)
