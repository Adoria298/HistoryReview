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

cursor.execute("SELECT * FROM urls LIMIT 10")
pprint(cursor.fetchall())

# final actions
conn.commit()
conn.close()
