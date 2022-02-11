import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import threading


def send_mail():
    me = "mysen.help@gmail.com"
    you = "anikanovvlad@yandex.ru"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Восстановление пароля"
    msg['From'] = me
    msg['To'] = you

    number = "".join([random.choice("0123456789QWERTYUIOPASDFGHJKLZXCVBNM") for _ in range(10)])
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
        <p style="margin: 2%; font-weight: bold; font-size: 30px; color: #000000;">Mysen</p>
    </div>
    <div style="display: inline-block; width: 96%; margin-left: 2%;">
        <p class="text">
            Вам пришло это письмо, потому что кто-то захотел изменить пароль от вашего аккаунта. Если это были не вы, никому
            не говорите код и проигнорируйте это письмо. Код для восстановления пароля:
        </p>
        <p align="center" style="font-size: 50px; color: #ED760E">{number}</p>
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
    smtpObj.login('mysen.help@gmail.com', 'mysen2021')
    smtpObj.sendmail(me, you, msg.as_string())
    smtpObj.quit()
    print("mail sended")


def print_aaa():
    time.sleep(1)
    print("print_aaa")


x = threading.Thread(target=send_mail)
x.start()
x = threading.Thread(target=print_aaa)
x.start()

# number = randint(1, 999999)
# smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
# smtpObj.starttls()
# smtpObj.login('testapipythonn@gmail.com', 'testAPIpython2021')
# smtpObj.sendmail("vns.social.networks@gmail.com", "anikanovvlad@yandex.ru", str(number).rjust(6, "0"))
# smtpObj.quit()
