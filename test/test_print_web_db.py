import pymysql

db = pymysql.connect(
    user='dbuser', 
    passwd='abcd1234', 
    host='127.0.0.1', 
    db='study', 
    charset='utf8'
)  
cursor = db.cursor(pymysql.cursors.DictCursor)

def print_web(*args):    
    sentence = "".join(map(str,args))
    sentence = sentence.replace('"', '\\"')
    sql = 'INSERT INTO chat(msg, date) VALUES("' + sentence + '", NOW());'
    cursor.execute(sql)

print_web("hello")
print_web("world!", "good")

