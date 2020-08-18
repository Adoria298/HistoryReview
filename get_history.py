"""
get_history.py - Copies and analyzes your Chrome history
Copyright (C) <2020>  <Adoria298>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
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
print("Sampling tables.")
for table in tables:
    print(f"Table: {table[0]}")
    try: #TODO: more verbose errors
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 5")
        #TODO: make below output a function - DRY
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
#TODO: limit this to all sites visited since 00:00 23rd March 2020 
## (first Mon. after school closing - schools closed 20th March 2020)
print("Connecting visits and urls.")
march23 = datetime(2020, 3, 23, 0, 0, 0, 0)
condition = f"WHERE urls.last_visit_time = visits.visit_time AND visits.visit_time > {march23.timestamp()} AND urls.url LIKE 'http%' LIMIT 20"
cursor.execute(f"SELECT DISTINCT count(visits.id) FROM urls, visits {condition}")
print("Amount:", cursor.fetchone()[0]) # 1st column of 1st row
cursor.execute(("SELECT DISTINCT urls.url, urls.last_visit_time, visits.id FROM urls, "
    f"visits {condition}")) 
results = cursor.fetchall()
print(" | ".join((description[0] for description in cursor.description)))
pprint(results)

# final actions
conn.commit()
conn.close()

#TODO: clear cache folder where old chrome histories are kept