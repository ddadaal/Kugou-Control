import sqlite3

class Database(object):
	def __init__(self):
		self.conn = sqlite3.connect("database.db")
		self.cursor = self.conn.cursor()

	def acquire_properties(self,*pname):
		results= []
		for name in pname:
			self.cursor.execute('select %s from info where id=1' % (name))
			results.append(self.cursor.fetchone()[0])
		return results

	def modify_properties(self,**kw):
		for key in kw:
			value = kw[key]
			if isinstance(value,str):
				self.cursor.execute('update info set %s=\'%s\' where id=1' % (key,value))
			else:
				self.cursor.execute('update info set %s=%s where id=1' % (key,value))
		self.cursor.close()
		self.conn.commit()
		self.cursor = self.conn.cursor()

	def release(self):
		self.cursor.close()
		self.conn.close()

if __name__=="__main__":
	d = Database()
	d.modify_properties(name="中文测试",close=0)
	print(d.acquire_properties("name","close"))
	
