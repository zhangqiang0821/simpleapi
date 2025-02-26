from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    UniqueConstraint
)
from simpleapi import db
import time


class PermissionModel(db.Model):
    __tablename__ = "permissions"
    __bind_key__ = "zqdb"
    __table_args__ = (
        UniqueConstraint("code", name="uq_permissions_code"),
    )

    id = Column(Integer, primary_key=True)
    code = Column(String, comment="")
    name = Column(String, comment="")
    ctime = Column(BigInteger, nullable=False, default=time.time)
    utime = Column(BigInteger, default=time.time, onupdate=time.time)

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "ctime": self.ctime,
            "utime": self.utime
        }


class UsersPermissionsModel(db.Model):
    __tablename__ = "users_permissions"
    __bind_key__ = "zqdb"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    permission_id = Column(Integer, nullable=False)
    ctime = Column(BigInteger, nullable=False, default=time.time)
    utime = Column(BigInteger, default=time.time, onupdate=time.time)

    def to_dict(self):
        # 将对象转换为字典
        return {
            "id": self.id,  # 对象的id
            "user_id": self.user_id,  # 对象的用户id
            "permission_id": self.permission_id,  # 对象的权限id
            "ctime": self.ctime,  # 对象的创建时间
            "utime": self.utime  # 对象的更新时间
        }