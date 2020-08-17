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

# setup sqlite by connecting to the copied file
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# find the names of the tables
cursor.execute("SELECT name from sqlite_master WHERE type='table'")
tables = cursor.fetchall() # list of tuples

# get a data sample and columns from each table
for table in tables:
    print(f"Table: {table[0]}")
    try:
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
        print(" | ".join((description[0] for description in cursor.description)))
        try:
            for row in cursor.fetchall():
                #" | ".join((str(col) for col in row))
                print(" | ".join((str(col) for col in row)))
        except TypeError:
            print("Formatting of data could not be done due to type error; printing with pprint.")
            pprint(cursor.fetchone())
        cursor.execute(f"SELECT count(*) FROM {table[0]} LIMIT 1")
        print("Amount:", cursor.fetchone()[0])
    except sqlite3.OperationalError:
        print(f"Could not get data for table {table} due to Operational Error.")

# find a connection between **`visits`** and **`urls`**
cursor.execute("SELECT urls.url, urls.last_visit_time, visits.id FROM urls, visits WHERE urls.last_visit_time = visits.visit_time") 
results = cursor.fetchall()
print(" | ".join((description[0] for description in cursor.description)))
pprint(results)

# final actions
conn.commit()
conn.close()

#TODO: clear cache folder where old chrome histories are kept