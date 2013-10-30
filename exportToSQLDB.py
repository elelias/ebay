
from insertIntoDB import *
from getConnectionToDB import *
import codecs




def exportToSQL():

	'''exports the information about laptops from the 
	text files to the SQL database'''


	con=getConnectionToDataBase()

	laptopInfoFile='newDatabase.txt'
	sellerInfoFile='sellerDatabase.txt'

	lfile=codecs.open(laptopInfoFile,'r','utf-8')
	sfile=codecs.open(sellerInfoFile,'r','utf-8')

	#CREATE THE PRODUCTS TABLE
	l=lfile.readlines()
	keys=['itemid','procspeed','screensize','harddrive','memory','price','brand','proctype']
	for line in l:
		words=line.strip().split('\t')

		sqlDict=dict(zip(keys,words))
		try:
			insertIntoTable('products',sqlDict,con,False)
		except:
			pass


	#CREATE THE SELLERS TABLE
	s=sfile.readlines()
	keys=['itemid','sellerid','feedback','aboutme','fcolor']
	for line in s:
		words=line.strip().split('\t')
		if words[3]=='false':
			words[3]=0
		elif words[3]=='true':
			words[3]=1


		sqlDict=dict(zip(keys,words))
		try:
			insertIntoTable('seller',sqlDict,con,False)
		except:
			pass


	#CREATE THE LAPTOP TABLE

	sqlstring='CREATE TABLE IF NOT EXISTS laptops '+\
	'AS (select products.*,sellerid from products,seller '+\
	'WHERE products.itemid=seller.itemid) ;'
	executeQuery(con,sqlstring)


	#CREATE THE UNIQUE SELLERS TABLE
	sqlstring='CREATE TABLE IF NOT EXISTS vendors '+\
	'AS (select distinct sellerid,feedback,aboutme,fcolor from seller);'
	executeQuery(con,sqlstring)




if __name__=='__main__':

	exportToSQL()