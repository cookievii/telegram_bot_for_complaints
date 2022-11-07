from sqlalchemy import BigInteger, Boolean, Column, String, or_

from models.datebase import Base, session


class User(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(100))
    full_name = Column(String(100))
    phone = Column(String(11))
    banned = Column(Boolean, default=False)

    def __init__(
        self,
        user_id: int = None,
        username: str = None,
        full_name: str = None,
        phone: str = None,
        banned: bool = False,
    ):
        self.user_id = user_id
        self.username = username
        self.full_name = full_name
        self.phone = phone
        self.banned = banned

    async def create(self):
        session.add(self)
        session.commit()

    @staticmethod
    async def chance_phone_by_id(user_id: int, phone: str):
        user = (
            session.query(User).filter(User.user_id == user_id).update({"phone": phone})
        )
        session.commit()
        return user

    @staticmethod
    async def chance_fullname_by_id(user_id: int, full_name: str):
        user = (
            session.query(User)
            .filter(User.user_id == user_id)
            .update({"full_name": full_name})
        )
        session.commit()
        return user

    @staticmethod
    async def search_user_by_any_arg(arg):
        user = (
            session.query(User)
            .filter(
                or_(
                    User.user_id == arg,
                    User.username == arg,
                    User.phone == arg,
                    User.full_name == arg,
                )
            )
            .scalar()
        )
        return user

    @staticmethod
    async def ban_by_user_id(user_id):
        user = (
            session.query(User).filter(User.user_id == user_id).update({"banned": True})
        )
        session.commit()
        return user

    @staticmethod
    async def unban_by_user_id(user_id):
        user = (
            session.query(User)
            .filter(User.user_id == user_id)
            .update({"banned": False})
        )
        session.commit()
        return user

    @staticmethod
    async def get_all():
        users = session.query(User).all()
        return users
