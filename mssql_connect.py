import sqlalchemy
import logging

USERNAME = 'sa'
PASSWORD = 'passworD0'
SERVER = 'localhost'
DATABASE = 'testDB'
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
    engine = sqlalchemy.create_engine(engine_stmt, echo=True)
    logging.info('Trying to connect MSSQL')
except Exception as e:
    logging.error('{}'.format(e))
