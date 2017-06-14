# coding=utf-8
import MySQLdb

HOST="140.120.57.34"
#HOST="localhost"

allwords=[]
text_file = open("7000.txt", "r")
allwords=text_file.readline().rstrip('\n').split(',')
text_file.close()

print len(allwords)

try:
    db = MySQLdb.connect(HOST,"entypeuser","entypeuser","entype",charset='utf8')
    for word in allwords:
	    insert_sql = "INSERT INTO words (word) VALUES (\'%s\');"% (word)
	    #sql = "INSERT INTO user (id, account, password) VALUES (NULL, '123','456')"
	    # 執行SQL statement
	    cursor = db.cursor()
	    cursor.execute(insert_sql)
	    db.commit()
    # 關閉連線
    db.close()

except MySQLdb.Error as e:
    print "Error %d: %s" % (e.args[0], e.args[1])