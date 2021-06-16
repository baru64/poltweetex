import urllib
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 f"SERVER={os.environ[DATABASE_SERVER]};"
                                 f"DATABASE={os.environ[DATABASE_NAME]};"
                                 f"UID={os.environ[DATABASE_LOGIN]};"
                                 f"PWD={os.environ[DATABASE_PASSWD]}")

engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
