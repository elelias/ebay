# coding: utf-8
# POKERSTARS HISTORY PARSER
#

import sys
import MySQLdb as mdb
import copy



def translateValues(value):
	'''translates a python variable to the database language'''

	if type(value)==str:
		val='\"'+value+'\"'
	elif type(value)==unicode:
		val='\"'+value+'\"'
	elif type(value)==bool:
		val=int(value)
	elif value==None:
		val='NULL'
	else:
		val=value

	return val


def executeQuery(connection,execute_string):

	cur=connection.cursor()		
	try:
		cur.execute(execute_string)
	except Exception as e:
		print 'something happened',e
		print 'the string was ',execute_string

	
	connection.commit()
	rows=cur.fetchall()
	#for row in rows:
	#	print row
	return rows

def insertIntoTable(tableName,tableDict,connection,verbose=False):
	'''Inserts the pokerhand info contained in a dictionary inside
	the database'''
	#insert the table
	#the trick is to name the colums after the dict keys (well, the other way around)
	#
	#
	#
	#BUILD THE SQL INPUT
	#
	execute_string='INSERT INTO '+tableName +' SET '
	for key,value in tableDict.iteritems():
		val=translateValues(value)
		execute_string+=key+'='+unicode(val)+', '
	#remove the last comma and extra space:
	execute_string=execute_string[:-2]
	execute_string+=';'
	#
	#
	#
	if verbose:
		print ''
		print 'inserting into the table '+tableName
		print 'the dictionary reads: '
		for key,value in tableDict.iteritems():
			print '    key = ',key
			print '    value = ',value
		#
		print
		print
		print 'the string is',execute_string
		print 	
	#raw_input()
	#
	#
	executeQuery(connection,execute_string)

