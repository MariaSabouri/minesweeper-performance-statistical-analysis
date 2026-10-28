import telebot
import time
from telebot import types
import sqlite3
from API import TOKEN

bot = telebot.TeleBot(TOKEN)

db = sqlite3.connect("./data.db", check_same_thread=False)
cur = db.cursor()

null_data = cur.execute("SELECT id FROM players WHERE (time1 IS NULL) \
                                                   OR (time2 IS NULL) \
                                                   OR (time3 IS NULL) ").fetchall()
null_list = []
for i in null_data:
    null_list.append(i[0])


start_text = "کافیه دستور استارت رو ارسال کنید." + "\n" + "/start"

singup_text = "سلام وقتتون بخیر؛\nخیلی از شما سپاسگزاریم که در این بازی شرکت کردید." + '\U00002764' + "\n" \
+ "در این بازی باید 3 بار برد داشته باشید." + "\n" \
+ 'متاسفانه مراحل انجام این بات توسط شما ناقص انجام شده است.' + '\n' \
+ "امکانش هست لطفا مراحل بازی رو طی کنید تا بتوانیم از داده های شما نیز استفاده بکنیم؟" \
+ '\U0001F97A ' + '\U0001F448' + '\U0001F449'

for i in null_list:
    try:
        win = cur.execute(f"SELECT wins FROM players WHERE id = {i}").fetchall()[0][0]

        if win == None:
            bot.send_message(i, singup_text)
            bot.send_message(i, start_text)

        elif int(win) < 3:
            message_text = "سلام وقتتون بخیر؛" + "\n" + "خیلی از شما سپاسگزاریم که در این بازی شرکت کردید." + '\U00002764' + "\n" \
            + "در این بازی باید 3 بار برد داشته باشید. شما لطف کردید و " \
            + f"{win}" \
            + " بار بازی را برده اید.\n" + "امکانش هست لطفا " \
            + f"{3-win}" \
            + " بار دیگر هم این بازی را ببرید تا بتوانیم از داده های شما نیز استفاده بکنیم؟" \
            + '\U0001F97A ' + '\U0001F448' + '\U0001F449'

            bot.send_message(i, message_text)
            bot.send_message(i, start_text)


    except Exception as error:
        print(error)


# bot.polling()

# link_problems = cur.execute("SELECT id FROM players WHERE (link1 NOT LIKE '%minesweeper.online/game%') \
#                                                        OR (link2 NOT LIKE '%minesweeper.online/game%') \
#                                                        OR (link3 NOT LIKE '%minesweeper.online/game%') ") .fetchall()
# link_list = []
# for i in link_problems:
#     link_list.append(i[0])


# ids = null_list

# for i in link_list:
#     if i not in null_list:
#         ids.append(i)
#         # print(i)


    
# wrong_data = cur.execute("SELECT id FROM players WHERE (time1 NOT GLOB '*[0-9]*')").fetchall()
# wrong_data = [i[0] for i in wrong_data]
# for i in wrong_data:
#     print(cur.execute(f"SELECT time1 FROM players WHERE id = {i}").fetchall())
#     print(i, '\n')
    


# for i in link_list:
#     links = cur.execute(f"SELECT link1 FROM players WHERE id={i}").fetchall()
#     print(links)

# print(link_list)
# print(null_list, '\n\n', link_list)