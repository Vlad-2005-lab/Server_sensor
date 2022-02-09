import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    mail = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    sensors = sqlalchemy.Column(sqlalchemy.String, default="")
    extra = sqlalchemy.Column(sqlalchemy.String, default="")
