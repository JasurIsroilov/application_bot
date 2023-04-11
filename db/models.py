from sqlalchemy import Column, BigInteger, String


from db.base import Base


class Crew(Base):
    __tablename__ = 'crew_it'

    crew_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    fio = Column(String(length=255), nullable=False)
    phone = Column(String(length=30), nullable=False)
    username = Column(String(length=60), nullable=False)
    dep = Column(String(length=40), nullable=True)
