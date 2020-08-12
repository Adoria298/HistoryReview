import sqlite3
from shutil import copyfile
from pprint import pprint
from appdirs import user_cache_dir, user_data_dir
from datetime import datetime

db_file = copyfile(user_data_dir("Chrome", "Google") + \
        "\\User Data\\Default\\History", 
    user_cache_dir("HistoryReview", "Adoria298") + \
        "\Chrome_History_Copy_" + \
        str(datetime(2020, 8, 12).now().toordinal()))
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

#cursor.execute("SELECT name from sqlite_master WHERE type='table'")
#pprint(cursor.fetchall())

cursor.execute("SELECT * FROM urls LIMIT 20")
print([description[0] for description in cursor.description])
pprint(cursor.fetchall())

cursor.execute("SELECT id, url, visit_count FROM urls LIMIT 20")
print([description[0] for description in cursor.description])
pprint(cursor.fetchall())

# final actions
conn.commit()
conn.close()
