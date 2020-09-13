import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

#---------------------------------------------------------------
# DATABASE SETTINGS
#---------------------------------------------------------------
DATABASE = os.environ.get('DATABASE_URL')
ENGINE = create_engine(DATABASE, encoding="utf-8")

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=ENGINE
                                      ))

Base = declarative_base()
Base.query = session.query_property()


