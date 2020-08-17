import sqlite3
from shutil import copyfile
from pprint import pprint
from datetime import datetime

from appdirs import user_cache_dir, user_data_dir

# copy file because Chrome locks the database when open
# currently the user's responsibility to delete these files
# may not work on other platforms - never been tested
db_file = copyfile(user_data_dir("Chrome", "Google") + \
        "\\User Data\\Default\\History", 
    user_cache_dir("HistoryReview", "Adoria298") + \
        "\Chrome_History_Copy_" + \
        str(datetime(2020, 8, 12).now().toordinal()))

# set sqlite by connecting to the copied file
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# find the names of the tables
#cursor.execute("SELECT name from sqlite_master WHERE type='table'")
#pprint(cursor.fetchall())

cursor.execute("SELECT * FROM urls LIMIT 1")
# prints the coloumn header
#TODO: make this output prettier
print([description[0] for description in cursor.description]) 
pprint(cursor.fetchall())

# number of urls
cursor.execute("SELECT count(url) FROM urls")
no_urls = cursor.fetchall()[0][0]
print(f"There are {no_urls} URLs in the History database.")

#cursor.execute("SELECT id, url, visit_count FROM urls")
# note how there are less headers
#print([description[0] for description in cursor.description])
#for url in range(no_urls):
#    pprint(cursor.fetchone())

cursor.execute("SELECT * FROM visits LIMIT 1")
print([description[0] for description in cursor.description])
pprint(cursor.fetchall())

# final actions
conn.commit()
conn.close()

#TODO: clear cache folder where old chrome histories are kept