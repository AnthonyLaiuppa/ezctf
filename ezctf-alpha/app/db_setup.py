from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Date, Integer, String, JSON 
from sqlalchemy.schema import CreateSchema
from sqlalchemy_utils import database_exists, create_database, drop_database

from datetime import date
from passlib.hash import sha256_crypt
import json

engine = create_engine('', echo=True)
meta = MetaData()
meta.bind = engine


if not database_exists(engine.url):
    create_database(engine.url)
else:
	drop_database(engine.url)
	create_database(engine.url)

print('[INFO] Creating user table.')
users = Table('users', meta,
    Column('name', String(40), primary_key=True),
    Column('username', String(50)),
    Column('email', String(50)),
    Column('password', String(512)),
    Column('score', String(10)),
    Column('flags', JSON),
    Column('is_admin', Integer)
)
users.create()
print('[SUCCESS] Created user table.')
print('[INFO] Creating challenge table.')
challenges = Table('challenges', meta,
    Column('ch_id', Integer, primary_key=True, nullable=False, autoincrement=True ),
    Column('ch_name', String(50)),
    Column('ch_desc', String(256)),
    Column('ch_score', Integer),
    Column('ch_author', String(10)),
    Column('ch_date', Date),
    Column('ch_flag', String(100)),
    Column('ch_filepath', String(256)),
    Column('ch_category', String(100)),
    Column('ch_solves', Integer),
    Column('ch_difficulty', String(50))
)
challenges.create()
print('[SUCCESS] Created challenge table.')
print('[INFO] Creating first user.')

#Prep some of the values we're inserting
password = sha256_crypt.encrypt('')
flags = {"c1":0}

users = Table('users', meta, autoload=True)
i = users.insert()

i.execute(name='Anthony Laiuppa', 
		  email='administrator@ezctf.com', 
		  username='floridaman',
		  password=password,
		  score=0,
		  flags=flags,
		  is_admin=1
		  )
print('[SUCCESS] Created first user.')
print('[INFO] Creating first challenge.')
challenges = Table('challenges', meta, autoload=True)
i = challenges.insert()
i.execute(ch_name='web1',
	      ch_desc='Look around, this ones the easiest trick in the book',
	      ch_score='10',
	      ch_author='floridaman',
	      ch_date=date.today(),
	      ch_flag='flag'+'{'+'HIDDEN_iN_pLaIN_SigHT}',
	      ch_filepath='<a href="/challenge/1/">mira aqui</a>',
	      ch_category='web',
	      ch_solves=0,
          ch_difficulty='novice'
		  )

print('[SUCCESS] Created first challenge.')
