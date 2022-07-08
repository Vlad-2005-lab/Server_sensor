# -*- coding: utf-8 -*-
import random
import time
from flask import Flask, request
from data import db_session
from data.sensor import Sensor
from data.user import User
import hashlib
from emoji import emojize
import threading
import datetime
import telebot
from telebot import types

SMILE = ["✏", "🗑"]
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my genius secret key'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "mysen.help@yandex.ru"
app.config["MAIL_PASSWORD"] = "AnikanovVlad2005"
db_session.global_init("db/data.sqlite")
password_hash = "27b80f2b0304bef4da58f2bde7e93e5b948f96f1c4a3f60abab033e39b41428b"
bot = telebot.TeleBot(open('extras/token/telegram_token.txt').read())
time_start = datetime.datetime.now()


# def send_mail(id):
#     me = "mysen.help@yandex.ru"
#
#     session = db_session.create_session()
#     user = session.query(User).filter(User.id == id).first()
#     you = user.mail
#
#     # Create message container - the correct MIME type is multipart/alternative.
#     msg = MIMEMultipart('alternative')
#     msg['Subject'] = "Восстановление пароля"
#     msg['From'] = me
#     msg['To'] = you
#
#     number = "".join([random.choice("0123456789QWERTYUIOPASDFGHJKLZXCVBNM") for _ in range(10)])
#     user.extra = number
#     session.commit()
#     session.close()
#     html = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <style>
#             .text{text-indent: 10px;
#             align: "justify";}
#         </style>
#     </head>
#     """ + f"""<body style="width: 100%; margin: 0px;">
#     <div style="display: inline-block; width: 100%; background: #FF9900;">
#         <p style="margin: 2%; font-weight: bold; font-size: 20px; color: #000000;">Mysen</p>
#     </div>
#     <div style="display: inline-block; width: 96%; margin-left: 2%;">
#         <p class="text">
#             Вам пришло это письмо, потому что кто-то захотел изменить пароль от вашего аккаунта. Если это были не вы, никому
#             не говорите код и проигнорируйте это письмо. Код для восстановления пароля:
#         </p>
#         <p align="center" style="font-size: 40px; color: #ED760E">{number}</p>
#         <p class="text">Это письмо отправленно автоматически, на него не нужно отвечать.</p>
#     </div>
#     </body>
#     </html>
#     """
#
#     # part1 = MIMEText(text, 'plain')
#     part2 = MIMEText(html, 'html')
#
#     # msg.attach(part1)
#     msg.attach(part2)
#     smtpObj = smtplib.SMTP('smtp.yandex.ru', 587)
#     smtpObj.starttls()
#     smtpObj.login(me, 'AnikanovVlad2005')
#     smtpObj.sendmail(me, you, msg.as_string())
#     smtpObj.quit()
#     print("send")


def get(data):
    return list(map(int, data.split(";")))


def keyboard_creator(list_of_names, one_time=True):
    """
    :param list_of_names: list; это список с именами кнопок(['1', '2'] будет каждая кнопка в ряд)
    [['1', '2'], '3'] первые 2 кнопки будут на 1 линии, а 3 снизу)
    :param one_time: bool; скрыть клаву после нажатия или нет
    :return: готовый класс клавиатуры внизу экрана
    """
    returned_k = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    for i in list_of_names:
        if isinstance(i, list):
            string = ""
            for o in range(len(i) - 1):
                string += f"'{i[o]}', "
            string += f"'{i[-1]}'"
            exec(f"""returned_k.row({string})""")
            continue
        exec(f"""returned_k.row('{i}')""")
    return returned_k


def buttons_creator(dict_of_names, how_many_rows=8):
    """
    :param dict_of_names: dict; это словарь, первые ключи могут быть любыми, они разделяют кнопки на ряды, а значениями этих ключей
           являются другие словари. Первый их аргумент это текст кнопки, а 2 это callback_data(то что будет передаваться в
           коллбек). Например: {
                                   '1': {
                                       'текст первой кнопки': 'нажали на кнопку 1',
                                       'текст второй кнопки': 'нажали на кнопку 2'
                                       },
                                   '2': {
                                       'текст третьей кнопки': 'нажали на кнопку 3'
                                       }
                               }
    :param how_many_rows: int; это максимальное количество кнопок в ряду
    :return: готовый класс кнопок под сообщением
    """
    returned_k = types.InlineKeyboardMarkup(row_width=how_many_rows)
    for i in dict_of_names.keys():
        if type(dict_of_names[i]) is dict:
            count = 0
            for o in dict_of_names[i].keys():
                count += 1
                exec(
                    f"""button{count} = types.InlineKeyboardButton(text='{o}', callback_data='{dict_of_names[i][o]}')""")
            s = []
            for p in range(1, count + 1):
                s.append(f"button{p}")
            exec(f"""returned_k.add({', '.join(s)})""")
        else:
            exec(f"""button = types.InlineKeyboardButton(text='{i}', callback_data='{dict_of_names[i]}')""")
            exec(f"""returned_k.add(button)""")
    return returned_k


@app.route("/change_mail", methods=['GET', 'POST'])
def change_mail():
    id = request.args.get("i", default="нет", type=int)
    password = request.args.get("p", default="нет", type=str)
    mail = request.args.get("m", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user.password == password:
        user.mail = mail
        return "ok"
    return "bad password"


@app.route("/change_password", methods=['GET', 'POST'])
def change_password():
    id = request.args.get("i", default="нет", type=int)
    old_password = request.args.get("o", default="нет", type=str)
    new_password = request.args.get("n", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user.password == old_password:
        user.password = new_password
        session.commit()
        return "ok"
    else:
        return "bad password"


@app.route("/delete_me", methods=['GET', 'POST'])
def delete_me():
    id = request.args.get("i", default="нет", type=int)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    session.delete(user)
    session.commit()
    return "ok"


@app.route("/are_you_alive", methods=['GET', 'POST'])
def are_you_alive():
    return str(datetime.datetime.now() - time_start)


@app.route("/delete_sensor", methods=['GET', 'POST'])
def delete_sensor():
    id = request.args.get("i", default="нет", type=int)
    sensor = request.args.get("s", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        return "doesnt_exist"
    user.sensors = ";".join(user.sensors.replace(";", " ").replace(sensor, "").split())
    session.commit()
    session.close()
    return "ok"


@app.route("/change_name_sensor", methods=['GET', 'POST'])
def change_name_sensor():
    id = request.args.get("i", default="нет", type=int)
    name = request.args.get("n", default="нет", type=str)
    session = db_session.create_session()
    sensor = session.query(Sensor).filter(Sensor.id == id).first()
    if sensor is None:
        return " dont_exist"
    sensor.name = name
    session.commit()
    return "ok"


@app.route("/set_data_sensor", methods=['GET', 'POST'])
def set_data_sensor():
    id = request.args.get("i", default="нет", type=int)
    data = request.args.get("d", default="нет", type=str)
    session = db_session.create_session()
    sensor = session.query(Sensor).filter(Sensor.id == id).first()
    sensor.data = data
    session.commit()
    session.close()
    return "done"


@app.route("/get_sensor_name", methods=['GET', 'POST'])
def get_sensor_name():
    id = request.args.get("i", default="нет", type=int)
    session = db_session.create_session()
    sensor = session.query(Sensor).filter(Sensor.id == id).first()
    return sensor.name


@app.route("/add_sensor_to_user", methods=['GET', 'POST'])
def add_sensor_to_user():
    id = request.args.get("i", default="нет", type=int)
    id_sensor = request.args.get("is", default="нет", type=str)
    name = request.args.get("n", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    sensor = session.query(Sensor).filter(Sensor.id == int(id_sensor)).first()
    if user is None:
        return "unauthorized"
    if id_sensor not in user.sensors:
        sensor.name = name
        user.sensors = ";".join(user.sensors.split(";") + [id_sensor]) if len(user.sensors) > 0 else id_sensor
    session.commit()
    session.close()
    return "ok"


@app.route("/exist_sensor", methods=['GET', 'POST'])
def exist_sensor():
    id = request.args.get("i", default="нет", type=int)
    session = db_session.create_session()
    sensor = session.query(Sensor).filter(Sensor.id == id).first()
    if sensor is None:
        return "not exist"
    return "yes"


@app.route("/get_data_sensor", methods=['GET', 'POST'])
def get_data_sensor():
    id = request.args.get("i", default="нет", type=int)
    session = db_session.create_session()
    sensor = session.query(Sensor).filter(Sensor.id == id).first()
    return sensor.data


@app.route("/get_sensors", methods=['GET', 'POST'])
def get_sensors():
    id = request.args.get("i", default="нет", type=int)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        return "unauthorized"
    return user.sensors


@app.route("/change_user_password", methods=['GET', 'POST'])
def change_user_password():
    id = request.args.get("i", default="нет", type=int)
    password = request.args.get("p", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        return "unauthorized"
    user.password = password
    session.commit()
    session.close()
    return "ok"


# @app.route("/resend_mail", methods=['GET', 'POST'])
# def resend_mail():
#     id = request.args.get("i", default="нет", type=int)
#     sendmail = threading.Thread(target=send_mail, args=(id,))
#     sendmail.start()
#     return "ok"


@app.route("/check_mail", methods=['GET', 'POST'])
def check_mail():
    id = request.args.get("i", default="нет", type=int)
    code = request.args.get("c", default="нет", type=str).replace(" ", "").upper()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        return "unauthorized"
    if user.extra == code:
        return "yes"
    return "no"


# @app.route("/exist_user", methods=['GET', 'POST'])
# def exist_user():
#     login = request.args.get("l", default="нет", type=str)
#     session = db_session.create_session()
#     user = session.query(User).filter(User.login == login).first()
#     if user is None:
#         return "no"
#     sendmail = threading.Thread(target=send_mail, args=(user.id,))
#     sendmail.start()
#     return str(user.id)


@app.route("/check_user", methods=['GET', 'POST'])
def check_user():
    login = request.args.get("l", default="нет", type=str)
    password = request.args.get("p", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.login == login).first()
    if user is None:
        return "not ok"
    if password == user.password:
        return str(user.id)
    return "not ok"


@app.route("/create_user", methods=['GET', 'POST'])
def create_user():
    login = request.args.get("l", default="нет", type=str)
    password = request.args.get("p", default="нет", type=str)
    mail = request.args.get("m", default="нет", type=str).replace(" ", "").lower()
    session = db_session.create_session()
    users = list(map(lambda x: x.login, session.query(User).all()))
    if mail.count("@") == 1 and mail.split("@")[1].count(".") == 1 and login not in users:
        user = User()
        user.login = login
        user.password = password
        user.mail = mail
        user.sensors = ""
        session.add(user)
        session.commit()
        return str(user.id)
    elif login in users:
        return "busy"
    else:
        return "invalid mail"


@app.route("/add_new_sensor", methods=['POST'])
def add_new_sensor():
    password = request.args.get("p", default="нет", type=str)
    password_hash_object = hashlib.sha256(password.encode("utf-8"))
    password_hex_dig = password_hash_object.hexdigest()
    if password_hex_dig == password_hash:
        session = db_session.create_session()
        sensor = Sensor()
        sensor.id = len(session.query(Sensor).all()) + 1
        session.add(sensor)
        session.commit()
        session.close()
    return "ok"


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """
    принимает все сообщения если функция никуда не переадресовала в другую
    :param message: class, тг возращает
    :return: переход в vilka(message)
    """
    session = db_session.create_session()
    check = session.query(User).filter(User.tg_id == message.from_user.id).first()
    if check is None:
        user = User()
        user.tg_id = int(message.from_user.id)
        user.sensors = ""
        user.extra = ""
        session.add(user)
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, f"""Здравствуйте, это бот Mysen. Я буду
    помогать вам с вашими датчиками. Приятного использования.""",
                         reply_markup=keyboard_creator(["Начать"]))
    else:
        main_menu(message)
        return
    return bot.register_next_step_handler(message, main_menu)


def main_menu(message):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == message.from_user.id).first()
    if user.extra == "id" and message.text != "Отмена":
        if int(message.text) in list(map(lambda x: x.id, session.query(Sensor).all())):
            user.sensors = user.sensors + (";" if len(user.sensors) > 0 else "") \
                           + str(message.text) if user.sensors.count(";") == 0 else \
                ";".join(user.sensors.split(";") + [message.text])
            user.extra = ""
            session.commit()
        else:
            bot.send_message(message.from_user.id, "Устройства с таким ID не существует, "
                             + "попробуйте снова:", reply_markup=keyboard_creator(["Отмена"]))
            return bot.register_next_step_handler(message, main_menu)
    elif user.extra == "id" and message.text == "Отмена":
        user.extra = ""
        session.commit()
    if user.extra != "" and user.extra.split()[0] == "name":
        sensor = session.query(Sensor).filter(Sensor.id == int(user.extra.split()[1])).first()
        sensor.name = message.text
        user.extra = ""
        session.commit()
    keyboard = {}
    i = 0
    if len(user.sensors) > 0:
        for sensor_id in user.sensors.split(";") if user.sensors.count(";") > 0 else [user.sensors]:
            i += 1
            sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
            keyboard[f"{i}"] = {}
            keyboard[f"{i}"][sensor.name] = f"open {sensor_id}"
            # keyboard[f"{i}"][f"{emojize(SMILE[0], use_aliases=True)}"] = f"new_name {sensor_id}"
    i += 1
    keyboard[f"{i}"] = {}
    keyboard[f"{i}"]["Добавить устройство"] = "add_device"
    if len(user.sensors) > 0:
        text = "Ваши устройства:"
    else:
        text = "У вас нет устройств. Вы можете добавить нажав по кнопке:"
    bot.send_message(message.from_user.id, text,
                     reply_markup=buttons_creator(keyboard))
    session.close()
    return bot.register_next_step_handler(message, main_menu)


@bot.callback_query_handler(
    func=lambda call: call.data == "add_device")
def callback_main_menu(call):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == call.message.chat.id).first()
    user.extra = "id"
    bot.send_message(call.message.chat.id, "Введите ID устройства:",
                     reply_markup=keyboard_creator(["Отмена"]))
    session.commit()
    session.close()


@bot.callback_query_handler(
    func=lambda call: call.data.split()[0] in ["open", "back_device"])
def callback_main_menu(call):
    session = db_session.create_session()
    sensor_id = int(call.data.split()[1])
    sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
    text = f"""Ваше устройство "{sensor.name}":\n""" + \
           f"""ID: {sensor_id}\n""" + \
           f"""Состояние: {"Пустой" if sensor.data == "green" else ("Полный" if sensor.data == "red" else ("Нет данных" if sensor.data == "gray" else "Заполняется"))}\n""" + \
           f"""Температура 1: {random.randint(20, 40)}\n""" + \
           f"""Температура 2: {random.randint(20, 40)}"""
    buttons = buttons_creator({"1": {f"Удалить {emojize(SMILE[1], use_aliases=True)}": f"delete {sensor_id}",
                                     f"Изменить название {emojize(SMILE[0], use_aliases=True)}": f"new_name {sensor_id}"},
                               "2": {"Обновить данные": f"update {sensor_id}"},
                               "3": {"Назад": "back"}})
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=buttons)
    session.close()


@bot.callback_query_handler(
    func=lambda call: call.data.split()[0] == "update")
def callback_update(call):
    session = db_session.create_session()
    sensor_id = int(call.data.split()[1])
    sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
    text = f"""Ваше устройство "{sensor.name}":\n""" + \
           f"""ID: {sensor_id}\n""" + \
           f"""Состояние: {"Пустой" if sensor.data == "green" else ("Полный" if sensor.data == "red" else ("Нет данных" if sensor.data == "gray" else "Заполняется"))}\n""" + \
           f"""Температура 1: {random.randint(20, 40)}\n""" + \
           f"""Температура 2: {random.randint(20, 40)}"""
    buttons = buttons_creator({"1": {f"Удалить {emojize(SMILE[1], use_aliases=True)}": f"delete {sensor_id}",
                                     f"Изменить название {emojize(SMILE[0], use_aliases=True)}": f"new_name {sensor_id}"},
                               "2": {"Обновить данные": f"update {sensor_id}"},
                               "3": {"Назад": "back"}})
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=buttons)
    session.close()


@bot.callback_query_handler(
    func=lambda call: call.data.split()[0] == "delete")
def callback_delete(call):
    session = db_session.create_session()
    sensor_id = int(call.data.split()[1])
    sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
    text = f"""Вы точно хотите удалить "{sensor.name}"?"""
    buttons = buttons_creator({"1": {"Да": f"confirm {sensor_id}",
                                     "Нет": f"back_device {sensor_id}"}})
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=buttons)
    session.close()


@bot.callback_query_handler(
    func=lambda call: call.data.split()[0] == "confirm")
def callback_delete(call):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == call.message.chat.id).first()
    all_sensors = user.sensors.split(";")
    all_sensors.pop(all_sensors.index(call.data.split()[1]))
    user.sensors = ";".join(all_sensors)
    session.commit()
    keyboard = {}
    i = 0
    if len(user.sensors) > 0:
        for sensor_id in user.sensors.split(";") if user.sensors.count(";") > 0 else [user.sensors]:
            i += 1
            sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
            keyboard[f"{i}"] = {}
            keyboard[f"{i}"][sensor.name] = f"open {sensor_id}"
    i += 1
    keyboard[f"{i}"] = {}
    keyboard[f"{i}"]["Добавить устройство"] = "add_device"
    if len(user.sensors) > 0:
        text = "Ваши устройства:"
    else:
        text = "У вас нет устройств. Вы можете добавить нажав по кнопке:"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=buttons_creator(keyboard))
    session.close()


@bot.callback_query_handler(
    func=lambda call: call.data.split()[0] == "new_name")
def callback_new_name(call):
    session = db_session.create_session()
    sensor_id = int(call.data.split()[1])
    user = session.query(User).filter(User.tg_id == call.message.chat.id).first()
    bot.send_message(call.message.chat.id, "Введите новое название для устройства:")
    user.extra = f"name {sensor_id}"
    session.commit()
    session.close()


@bot.callback_query_handler(
    func=lambda call: call.data == "back")
def callback_back(call):
    session = db_session.create_session()
    user = session.query(User).filter(User.tg_id == call.message.chat.id).first()
    keyboard = {}
    i = 0
    if len(user.sensors) > 0:
        for sensor_id in user.sensors.split(";") if user.sensors.count(";") > 0 else [user.sensors]:
            i += 1
            sensor = session.query(Sensor).filter(Sensor.id == sensor_id).first()
            keyboard[f"{i}"] = {}
            keyboard[f"{i}"][sensor.name] = f"open {sensor_id}"
            # keyboard[f"{i}"][f"{emojize(SMILE[0], use_aliases=True)}"] = f"new_name {sensor_id}"
    i += 1
    keyboard[f"{i}"] = {}
    keyboard[f"{i}"]["Добавить устройство"] = "add_device"
    if len(user.sensors) > 0:
        text = "Ваши устройства:"
    else:
        text = "У вас нет устройств. Вы можете добавить нажав по кнопке:"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                          reply_markup=buttons_creator(keyboard))
    session.close()


def server():
    # app.run(port=int(os.environ.get("PORT")), host='0.0.0.0')
    while True:
        try:
            app.run(port=8080)
            time.sleep(5)
            print("Started Server")
        except Exception as ex:
            print(f"ERROR: {ex}\nRestarting Server....")
            time.sleep(10)


def telegram_bot():
    while True:
        try:
            bot.infinity_polling()
            print("Started Telegram Bot")
            time.sleep(5)
        except Exception as ex:
            print(f"ERROR: {ex}\nRestarting Telegram Bot....")
            time.sleep(10)


def checker():
    while True:
        try:
            # some work
            break
            # print("Started Checker")
        except Exception as ex:
            print(f"ERROR: {ex}\nRestarting Cheker....")
            time.sleep(10)


if __name__ == '__main__':
    server = threading.Thread(target=server)
    server.start()
    telegram_bot = threading.Thread(target=telegram_bot)
    telegram_bot.start()
    checker = threading.Thread(target=checker)
    checker.start()
