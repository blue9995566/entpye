# coding=UTF-8
import MySQLdb
try:
	# 建立DB 連線資訊定設定中文編碼utf-8
	db = MySQLdb.connect("140.120.57.34","entypeuser","entypeuser","entype",charset='utf8')
	#db = MySQLdb.connect("localhost","entypeuser","entypeuser","entype",charset='utf8')
	account="789"
	password="7"
	sql= "INSERT INTO user (id, account, password) VALUES (NULL, %s, %s)" %(account,password)
	# 執行SQL statement
	cursor = db.cursor()
	#cursor.execute(sql)
	#db.commit()
	# 撈取多筆資料
	sql = "SELECT * FROM user"
	cursor.execute(sql)
	results = cursor.fetchall()
	# 迴圈撈取資料
	for record in results: 
	  id = record[0]
	  account = record[1]
	  password = record[2]

	  print id,account,password
	# 關閉連線
	db.close()

except MySQLdb.Error as e:
	print "Error %d: %s" % (e.args[0], e.args[1])