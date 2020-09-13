from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Float
from database import Base
from database import ENGINE

#---------------------------------------------------------------
# model of time data
#---------------------------------------------------------------
class TimeData(Base):
    __tablename__ = "negaposi"
    id = Column("id", BigInteger, nullable=False, primary_key=True)
    pos00 = Column("pos00", Float, default=0.0, nullable=False)
    neg00 = Column("neg00", Float, default=0.0, nullable=False)
    pos05 = Column("pos05", Float, default=0.0, nullable=False)
    neg05 = Column("neg05", Float, default=0.0, nullable=False)
    pos10 = Column("pos10", Float, default=0.0, nullable=False)
    neg10 = Column("neg10", Float, default=0.0, nullable=False)
    pos15 = Column("pos15", Float, default=0.0, nullable=False)
    neg15 = Column("neg15", Float, default=0.0, nullable=False)
    pos20 = Column("pos20", Float, default=0.0, nullable=False)
    neg20 = Column("neg20", Float, default=0.0, nullable=False)
    pos25 = Column("pos25", Float, default=0.0, nullable=False)
    neg25 = Column("neg25", Float, default=0.0, nullable=False)
    pos30 = Column("pos30", Float, default=0.0, nullable=False)
    neg30 = Column("neg30", Float, default=0.0, nullable=False)
    pos35 = Column("pos35", Float, default=0.0, nullable=False)
    neg35 = Column("neg35", Float, default=0.0, nullable=False)
    pos40 = Column("pos40", Float, default=0.0, nullable=False)
    neg40 = Column("neg40", Float, default=0.0, nullable=False)
    pos45 = Column("pos45", Float, default=0.0, nullable=False)
    neg45 = Column("neg45", Float, default=0.0, nullable=False)
    pos50 = Column("pos50", Float, default=0.0, nullable=False)
    neg50 = Column("neg50", Float, default=0.0, nullable=False)
    pos55 = Column("pos55", Float, default=0.0, nullable=False)
    neg55 = Column("neg55", Float, default=0.0, nullable=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}