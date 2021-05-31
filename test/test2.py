import pymysql
import time
from datetime import datetime

db = pymysql.connect(
    user='dbuser', 
    passwd='abcd1234', 
    host='127.0.0.1', 
    db='study', 
    charset='utf8'
)   

# now = datetime.now()
# date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + ' ' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second)

# sql = 'SELECT * FROM chat WHERE date >= "'+date+'";'

cursor = db.cursor(pymysql.cursors.DictCursor)

sql2 = "INSERT INTO chat(msg, date) VALUES('haha', NOW());"

# sql = 'SELECT MAX(no) AS lastno FROM chat;'
# sql = "SELECT * FROM chat where no > 69;"

i=0
while i<20:
    cursor.execute(sql2)
    time.sleep(0.5)
    # print(result)
    i+=1

# cursor.execute(sql)
# result = cursor.fetchall()


# print(len(result) + '60')
# print(cursor.fetchone()['lastno'])