import sys
import codecs
import pymysql
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

class Operate(object):
	def __init__(self, url, username, password, db, sql):
		self.db = pymysql.connect(url,username,password,db,charset='utf8')
		self.cursor = self.db.cursor()
		self.cursor.execute(sql)

	def getData(self):
		data = []
		sqlRes = self.cursor.fetchall()
		for row in sqlRes:
			_len = len(row)
			_r = []
			for j in range(_len):
				_r.append(row[j].encode('utf8').decode('utf8') if type(row[j]) == str else row[j])
			data.append(_r)
		return data

	def getFields(self):
		fields = []
		for tup in self.cursor.description:
			fields.append(tup[0])
		return fields


	