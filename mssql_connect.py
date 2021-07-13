import sqlalchemy as db
import logging
import pyodbc
from sqlalchemy import inspect


USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'oktell_settings'
DRIVER = 'ODBC+DRIVER+17+for+SQL+Server'

logging.basicConfig(
    filename='mssql.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    )

engine_stmt = (
    "mssql+pyodbc://{}:{}@{}/{}?driver={}".format(
        USERNAME, PASSWORD, SERVER, DATABASE, DRIVER
        )
    )

try:
    drivers = [item for item in pyodbc.drivers()]
    print(pyodbc.drivers())
    engine = db.create_engine(engine_stmt, echo=True)
    logging.info('Trying to connect MSSQL')
    inspector = inspect(engine)
    print('1')
    for table_name in inspector.get_table_names():
        for column in inspector.get_columns(table_name):
            print("Column: %s" % column['name'])

except Exception as e:
    logging.error('{}'.format(e))
