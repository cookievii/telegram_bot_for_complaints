from sqlalchemy import BigInteger, String, Column

from models.datebase import Base, session


class User(Base):
    __tablename__ = "user"
    user_id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100))
    phone = Column(String(11))

    def __init__(self, user_id: int, full_name: str = None, phone: str = None):
        self.user_id = user_id
        self.full_name = full_name
        self.phone = phone

    def __repr__(self):
        info: str = f"User [user_id: {self.user_id}, full_name: {self.full_name}, phone: {self.phone}]"
        return info

    async def create(self):
        session.add(self)
        session.commit()

    async def exists(self):
        users = session.query(User).filter(User.user_id == self.user_id).scalar()
        if users:
            return True
        return False
