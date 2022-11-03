

import sqlite3
# Import sqllite db

createdb = sqlite3.connect('login.db')
#create db called login.db

cursor = createdb.cursor()
#cursor to start the creation

command = """CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)"""
# command to create datable table if it doesnt exist

cursor.execute(command)
# run cursor command to create login.db and users table

cursor.execute("INSERT INTO users VALUES ('Admin', 'admin')")
# adds admin account to database

createdb.commit()
# commits the new changes to database *** adds user admin to the database ***