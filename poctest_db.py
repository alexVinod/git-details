import pymysql

from pymysql import cursors

def createPocTest():
	db = pymysql.connect(
		host='localhost',
		user='root',
		password='',
		db='poctest',
		charset='utf8'
	)
	cursor1 = db.cursor(cursors.DictCursor)
	cursor = db.cursor()
	