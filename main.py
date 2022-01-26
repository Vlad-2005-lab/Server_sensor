from flask import Flask, request
from data import db_session
from data.sensor import Sensor
from data.user import User
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my genius secret key'
db_session.global_init("db/data.sqlite")
password_hash = "6ce7f9ed39b43bbfd84d36f4b8849fb8bf00e2aaa71773aa8fae4e24ea71d4ae"


def get(data):
    return list(map(int, data.split(";")))


@app.route("/check_user", methods=['GET', 'POST'])
def check_user():
    login = request.args.get("l", default="нет", type=str)
    password = request.args.get("p", default="нет", type=str)
    session = db_session.create_session()
    user = session.query(User).filter(User.login == login).first()
    try:
        if password == user.password:
            return "ok"
    except Exception:
        return "not ok"
    return "not ok"


@app.route("/add_new_sensor", methods=['POST'])
def add_new_sensor():
    password = request.args.get("p", default="нет", type=str)
    password_hash_object = hashlib.sha256(password.encode("utf-8"))
    password_hex_dig = password_hash_object.hexdigest()
    if password_hex_dig == password_hash:
        session = db_session.create_session()
        sensor = Sensor()
        session.add(sensor)
        session.commit()
        session.close()
    return "ok"


@app.route("/add_new_data", methods=['POST'])
def add_new_data():
    id = request.args.get('id', default=-1, type=int)
    new_data = request.args.get("data", default=-1, type=int)
    if new_data == -1:
        return "ok"
    session = db_session.create_session()
    sensor = session.query(Sensor).filter(Sensor.id == id).first()
    sensor_data = get(sensor.data) if sensor.data != "" else []
    if len(sensor_data) > 0 and sensor_data[-1] != new_data or len(sensor_data) == 0:
        sensor.data = ";".join(list(map(str, sensor_data + [new_data])))
        session.commit()
    session.close()
    return "ok"


def main():
    # app.run(port=int(os.environ.get("PORT")), host='0.0.0.0')
    app.run(port=8080, host='192.168.1.10')


if __name__ == '__main__':
    main()
