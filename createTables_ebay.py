#
#
#
import sys
import MySQLdb as mdb
from getConnectionToDB import *


def createTables():
	'''creates the test table if it doesn't exist'''

	global con
	con=getConnectionToDataBase()
	with con:
		cur=con.cursor()
		sqlstring='CREATE TABLE IF NOT EXISTS products('
		sqlstring+='itemid BIGINT PRIMARY KEY,'
		sqlstring+='procspeed FLOAT(5,2),'			
		sqlstring+='screensize FLOAT(5,2),'
		sqlstring+='harddrive DOUBLE(7,2),'
		sqlstring+='memory FLOAT(4,2),'		
		sqlstring+='price DOUBLE(8,2),'
		sqlstring+='brand VARCHAR(40),'	
		sqlstring+='proctype VARCHAR(40)'
		sqlstring+=');'
		print sqlstring
		cur.execute(sqlstring)
		rows=cur.fetchone()
		print rows


		sqlstring='CREATE TABLE IF NOT EXISTS seller('
		sqlstring+='itemid  BIGINT PRIMARY KEY,'
		sqlstring+='sellerid VARCHAR(40),'			
		sqlstring+='feedback FLOAT(5,2),'
		sqlstring+='aboutme TINYINT,'
		sqlstring+='fcolor VARCHAR(20)'
		sqlstring+=');'
		print sqlstring
		cur.execute(sqlstring)
		rows=cur.fetchone()
		print rows		





if __name__=='__main__':
	createTables()
