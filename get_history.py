import sqlite3
from shutil import copyfile
from pprint import pprint

db_file = copyfile(r"C:\Users\banan\AppData\Local\Google\Chrome\User Data\Default\History", "./Chrome_History_Copy_202008120012")
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("SELECT * FROM urls LIMIT 10")
pprint(cursor.fetchall())

# final actions
conn.commit()
conn.close()
