import os
from flask import Flask, request
from data import db_session
from data.sensor import Sensor
from data.user import User
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my genius secret key'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "mysen.help@gmail.com"
app.config["MAIL_PASSWORD"] = "mysen2021"
db_session.global_init("db/data.sqlite")
password_hash = "27b80f2b0304bef4da58f2bde7e93e5b948f96f1c4a3f60abab033e39b41428b"


def send_mail(id):
    me = "mysen.help@gmail.com"

    session = db_session.create_session()
    user = session.query(User).filter(User.id == id).first()
    you = user.mail

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Восстановление пароля"
    msg['From'] = me
    msg['To'] = you

    number = "".join([random.choice("0123456789QWERTYUIOPASDFGHJKLZXCVBNM") for _ in range(10)])
    user.extra = number
    session.commit()
    session.close()
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            .text{text-indent: 10px;
            align: "justify";}
        </style>
    </head>
    """ + f"""<body style="width: 100%; margin: 0px;">
    <div style="display: inline-block; width: 100%; background: #FF9900;">
        <p style="margin: 2%; font-weight: bold; font-size: 20px; color: #000000;">Mysen</p>
    </div>
    <div style="display: inline-block; width: 96%; margin-left: 2%;">
        <p class="text">
            Вам пришло это письмо, потому что кто-то захотел изменить пароль от вашего аккаунта. Если это были не вы, никому
            не говорите код и проигнорируйте это письмо. Код для восстановления пароля:
        </p>
        <p align="center" style="font-size: 40px; color: #ED760E">{number}</p>
        <p class="text">Это письмо отправленно автоматически, на него не нужно отвечать.</p>
    </div>
    </body>
    </html>
    """

    # part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # msg.attach(part1)
    msg.attach(part2)
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(me, 'mysen2021')
    smtpObj.sendmail(me, you, msg.as_string())
    smtpObj.quit()


def get(data):
    return list(map(int, data.split(";")))


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
    print(user.sensors)
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


@app.route("/resend_mail", methods=['GET', 'POST'])
def resend_mail():
    id = request.args.get("i", default="нет", type=int)
    sendmail = threading.Thread(target=send_mail, args=(id,))
    sendmail.start()
    return "ok"


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


@app.route("/exist_user", methods=['GET', 'POST'])
def exist_user():
    login = request.args.get("l", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.login == login).first()
    if user is None:
        return "no"
    sendmail = threading.Thread(target=send_mail, args=(user.id,))
    sendmail.start()
    return str(user.id)


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


def main():
    app.run(port=int(os.environ.get("PORT")), host='0.0.0.0')
    # app.run(port=8080, host='192.168.56.1')


if __name__ == '__main__':
    x = threading.Thread(target=main)
    x.start()
