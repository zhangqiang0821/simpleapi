from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint
)
from simpleapi import db
from werkzeug.security import generate_password_hash, check_password_hash



class UserModel(db.Model):
    __tablename__ = "users"
    __bind_key__ = "zqdb"
    __table_args__ = (
        UniqueConstraint("mobile", name="uq_users_mobile"),
    )
    id = Column(Integer, primary_key=True)
    mobile = Column(Integer, comment="", unique=True, nullable=False)
    user_name = Column(String, comment="", nullable=False)
    password_hash = Column(String, comment="", nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "mobile": self.mobile,
            "user_name": self.user_name,
            "password_hash": self.password_hash,
        }

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
