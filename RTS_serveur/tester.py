import sqlite3 as sql

con = sql.connect('RTS_serveur_DB.db')
cur = con.cursor()
cur.execute('SELECT * FROM partiecourante')
rows = cur.fetchall()
assert rows == [('courante',)]
print("partiecourante OK")
