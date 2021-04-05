import os
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# Global Variables
SQLITE = 'sqlite'

# Table Names
USERS = 'users'
ADDRESSES = 'addresses'
WORDS = 'words_stishechko'
SETTINGS = 'settings_stishechko'
basedir = os.path.abspath(os.path.dirname(__file__))

class MyDatabase:
    DB_ENGINE = {
        SQLITE: f'sqlite:///{basedir}/static/files/db.db'
    }

    # Main DB Connection Ref Obj
    db_engine = None

    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
        else:
            print("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        users = Table(USERS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('first_name', String),
                      Column('last_name', String)
                      )
        address = Table(ADDRESSES, metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', None, ForeignKey('users.id')),
                        Column('email', String, nullable=False),
                        )
        words = Table(WORDS, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('source', String(250), nullable=False),
                      Column('target', String(250), nullable=False),
                      Column('zero', Integer),
                      Column('one', Integer),
                      Column('two', Integer),
                      Column('three', Integer),
                      Column('four', Integer)
                      )
        settings = Table(SETTINGS, metadata,
                        Column('randomize', Integer, nullable=False),
                        Column('round_size', Integer, nullable=False)
                        )

        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def add_new_word_table(self, user_id):
        metadata = MetaData()
        words = Table(f'words_{user_id}', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('source', String(250), unique=True, nullable=False),
                      Column('target', String(250), nullable=False),
                      Column('zero', Integer),
                      Column('one', Integer),
                      Column('two', Integer),
                      Column('three', Integer),
                      Column('four', Integer)
                      )
        try:
            metadata.create_all(self.db_engine)
            print("Tables created")
        except Exception as e:
            print("Error occurred during Table creation!")
            print(e)

    def execute_query(self, query=''):
        if query == '':
            return 'Nothing happened'
        with self.db_engine.connect() as connection:
            try:
                connection.execute(query)
                print(f"Query {query} Complete!")
            except Exception as e:
                return e

    def return_rows(self, query=''):
        rows = []
        if query == '':
            return 'Nothing happened'
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                return e
            else:
                for row in result:
                    rows.append(row)
                result.close()
                return rows


