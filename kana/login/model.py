from sqlalchemy import Column, Table, Integer, String, MetaData


meta = MetaData()
users = Table('users', meta,
              Column('id', Integer, primary_key=True),
              Column('user', String(64)),
              Column('salt', String(128), #salt, should be random
              Column('password', String(64)),
              Column('name', String(128)))

def create_handler(engine):
    meta.create_all(engine)
