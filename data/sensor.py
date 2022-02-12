import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class Sensor(SqlAlchemyBase, UserMixin):
    __tablename__ = 'sensor'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, default="My Sensor")
    data = sqlalchemy.Column(sqlalchemy.String, default="gray")
