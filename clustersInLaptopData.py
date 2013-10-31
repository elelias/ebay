

import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

from getConnectionToDB import *
from insertIntoDB import *

con=getConnectionToDataBase()

def getAllBrands():

	'''retrieves all the different brands in the database and assigns a 
	normalised number in the rank 0-1 to each one'''


	sqlQuery='SET @rank=0;'
	sqlResult=executeQuery(con,sqlQuery)

	sqlQuery='SELECT @rank:=@rank+1 AS rank, A.brand '+\
	'FROM (SELECT brand FROM laptops GROUP BY brand) AS A '+\
	'ORDER BY rank;'

	sqlResult=executeQuery(con,sqlQuery)

	#BUILD UP THE LIST OF BRANDS
	brandList=[]
	for res in sqlResult:

		#CLEAN THE LIST FROM DUPLICATES
		if  not res[1] in ['Custom/Unbranded','Dell Computers','IBM, Lenovo','unknown']:
			brandList.append(res[1])
		#
	#

	#BUILD A DICTIONARY WITH THE NUMERIC VALUE ASSOCIATED
	#TO A CERTAIN BRAND
	brandDict={}
	for i,brand in enumerate(brandList):
		brandDict[brand] = float(i)/(len(brandList) - 1) 

	print brandDict
	return brandDict



def sanitizeProcessorType(procInput):

	'''Sanitizes the different possible ways of writing a processor 
	type. It cannot handle all the cases, but it is inclusive enough'''

	val=procInput.lower()

	if 'amd' in val:
		if 'dual' in val:
			proctype='AMD-DUAL'
		elif 'quad' in val:
			proctype='AMD-QUAD'
	elif 'intel' in val:
		if 'quad' in val:
			proctype='INTEL-QUAD'

		elif 'duo' in val or 'core 2' in val:
			proctype='INTEL-DUO'

	if 'i3' in val:
		proctype='INTEL-i3'
	elif 'i5' in val:
		proctype='INTEL-i5'
	elif 'i7' in val:
		proctype='INTEL-i7'
	elif 'pentium' in val:
		proctype='INTEL-pentium'
	else:
		proctype='unknown'

	return proctype

def normalize(numInput, colName):

	sqlQuery='SELECT max('+colName+') FROM laptops;'
	maxValue = executeQuery(con,sqlQuery)[0]

	try:
		maxValue=float(maxValue[0])
	except:
		print 'this is not a numeric value,maxValue'
		print maxValue
		assert False

	sqlQuery='SELECT min('+colName+') FROM laptops;'
	minValue = executeQuery(con,sqlQuery)

	try:
		minValue=float(minValue[0][0])
	except:
		print 'this is not a numeric value, minValue'
		print minValue
		assert False


	normalised=(numInput - minValue)/(maxValue-minValue)
	return normalised





def laptopDataQuery(sqlQuery):

	'''the sqlQuery that retrieves the info to cluster'''

	#sqlQuery='SELECT * FROM laptops;'
	sqlResult = executeQuery(con,sqlQuery)

	#
	dataLines=[]
	itemid=[]
	#
	for row in sqlResult:
		#print row
		newRow=[]

		#GET THE NORMALISED VALUE FOR THE BRAND
		n_brand = brandDict.get(row[6],None)
		if n_brand==None: continue

		#GET THE NORMALISED VALUE FOR THE PROCESSOR TYPE
		sanitProcType=sanitizeProcessorType(row[7])
		n_proctype=procTypeDict.get(sanitProcType,None)
		if n_proctype==None: continue

		#GET THE NORMALISED VALUE FOR THE NUMERIC VARIABLES
		n_procspeed=normalize(row[1],'procspeed')
		n_screensize=normalize(row[2],'screensize')
		n_harddrive=normalize(row[3],'harddrive')
		n_memory=normalize(row[4],'memory')
		#n_price=row[5]
		#CREATE A NEW LIST WITH THE NORMALISED VALUES
		newRow.append(n_procspeed)
		newRow.append(n_screensize)
		newRow.append(n_harddrive)
		newRow.append(n_memory)

		#print 'n_brand is ',n_brand
		newRow.append(n_brand)
		newRow.append(n_proctype)
		#newRow.append(n_price)
		dataLines.append(newRow)

		itemid.append(row[5])
	return dataLines,itemid



def kMeansCluster():

	'''clusters in the space of laptop parameters'''

	sqlQuery='SELECT * FROM laptops;'
	rowData,pList=laptopDataQuery(sqlQuery)
	X=np.array(rowData)
	np.random.seed(5)

	fignum=1


	estimators={'ebay_laptop_data': KMeans(n_clusters=4)}

	for name,est in estimators.iteritems():


		est.fit(X) #this computes the k-means clustering


		p=[]
		p.append((0,'processor speed'))
		p.append((1,'screen size'))
		p.append((2,'hard drive'))
		p.append((3,'memory'))
		p.append((4,'brand'))
		p.append((5,'processor Type'))


		plotDict=[]
		for i in range(0,3):
			for j in range(i+1,5):
				for k in range(j+1,6):
					print 'currently on ',i,j,k
					plotDict.append({'fLabel':p[i][1],'sLabel':p[j][1],'tLabel':p[k][1],'fAxis':p[i][0],'sAxis':p[j][0],'tAxis':p[k][0]})


		for plot in plotDict:

				print ' a new figure!'

				fig=pl.figure(fignum,figsize=(4,3))
				pl.clf() #this clears the current figure
				ax=Axes3D(fig,rect=[0,0,.95,1],elev=98,azim=134)
				pl.cla()#this clears the current axes
				fAxis=plot['fAxis']
				sAxis=plot['sAxis']		
				tAxis=plot['tAxis']
				fLabel=plot['fLabel']
				sLabel=plot['sLabel']		
				tLabel=plot['tLabel']				

				print 'axes ',fAxis,sAxis,tAxis
				#print X[:,fAxis]
				#print X[:,sAxis]
				#print X[:,tAxis]				

				labels=est.labels_ #labels of each point
				ax.scatter(X[:, fAxis], X[:, sAxis], X[:, tAxis], c=labels.astype(np.float))
				ax.w_xaxis.set_ticklabels([])
				ax.w_yaxis.set_ticklabels([])
				ax.w_zaxis.set_ticklabels([])
				ax.set_xlabel(fLabel)
				ax.set_ylabel(sLabel)
				ax.set_zlabel(tLabel)
				fignum = fignum + 1
				pl.show()
				pl.close(fig)
				raw_input('')



def hierarchicalCluster():

	import pandas as pd
	from scipy.spatial.distance import pdist, squareform
	from scipy.cluster.hierarchy import linkage, dendrogram
	import matplotlib as mp

	p=[]
	p.append((0,'processor speed'))
	p.append((1,'screen size'))
	p.append((2,'hard drive'))
	p.append((3,'memory'))
	p.append((4,'brand'))	
	p.append((5,'processor Type'))


	sqlQuery='SELECT * FROM laptops;'
	rowData,pList=laptopDataQuery(sqlQuery)
	X=np.array(rowData)
	distanceMatrix=pdist(X)
	f=pl.gcf()	
	d=dendrogram(linkage(distanceMatrix,method='complete'),color_threshold=0.8)
	pl.show()
	pl.savefig('dendrogram.pdf')
	raw_input('')	

	f.set_size_inches(8,4)


def pricePredictor():

	from sklearn import svm


	#TRAIN THE SVM
	sqlQuery='SELECT * FROM laptops WHERE itemid<331054210033;'	
	rowData,pList=laptopDataQuery(sqlQuery)

	print 'length rowData',len(rowData)
	X=np.array(rowData)

	clf=svm.SVR(kernel='linear',C=1e3,gamma=0.1)
	clf.fit(X,pList)


	#PREDICT ON A INDEPENDENT SAMPLE
	sqlQuery='SELECT * FROM laptops WHERE itemid>331054210033;'	
	rowData,actualPrice=laptopDataQuery(sqlQuery)
	Z=np.array(rowData)
	aP=np.array(actualPrice)

	prediction=clf.predict(Z)


	#print 'the prediction is ',prediction
	#print 'the actual numbers are ',actualPrice
	Y=(abs(prediction-aP))/aP
	print Y


	n,bins,patches = pl.hist(Y,10,(0,4),label='what?')
	pl.show()
	raw_input('')



def elbowCurve():


	from scipy.cluster.vq import kmeans,vq
	import matplotlib.pyplot as plt
	from scipy.spatial.distance import cdist,pdist
	from matplotlib import cm


	sqlQuery='SELECT * FROM laptops;'
	rowData,pList=laptopDataQuery(sqlQuery)
	X=np.array(rowData)
	#K=range(1,10)

	K_MAX = 8
	KK = range(1,K_MAX+1)


	KM = [kmeans(X,k) for k in KK]
	centroids = [cent for (cent,var) in KM]



	# alternative: scipy.spatial.distance.cdist
	D_k = [cdist(X, cent, 'euclidean') for cent in centroids]
	cIdx = [np.argmin(D,axis=1) for D in D_k]
	dist = [np.min(D,axis=1) for D in D_k]
	avgWithinSS = [sum(d)/X.shape[0] for d in dist]

	tot_withinss = [sum(d**2) for d in dist]  # Total within-cluster sum of squares
	totss = sum(pdist(X)**2)/X.shape[0]       # The total sum of squares
	betweenss = totss - tot_withinss          # The between-cluster sum of squares

	#kIdx=4
	kIdx = 3       # K=10
	clr = cm.spectral( np.linspace(0,1,10) ).tolist()
	mrk = 'os^p<dvh8>+x.'

# elbow curve
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(KK, betweenss/totss*100, 'b*-')
	ax.plot(KK[kIdx], betweenss[kIdx]/totss*100, marker='o', markersize=12, 
	    markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
	ax.set_ylim((0,100))
	plt.grid(True)
	plt.xlabel('Number of clusters')
	plt.ylabel('Percentage of variance explained (%)')
	plt.title('Elbow for KMeans clustering')
	pl.show()
	raw_input('done')
	# fig =  plt.figure()
	# ax = fig.add_subplot(111)
	# ax.plot(K,avgWithinSS,'b*-')
	# ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
	#     markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
	# plt.grid(True)
	# plt.xlabel('Number of clusters')
	# plt.ylabel('Average within-cluster sum of squares')
	# plt.title('Elbow for KMeans clustering')
	# plt.show()
	# raw_input('done')


if __name__=='__main__':

	global procTypeDict,brandDict

	brandDict=getAllBrands()
	procTypeList=['AMD-QUAD', 'AMD-DUAL', 'INTEL-i5', 'INTEL-i7', 'INTEL-DUO', 'INTEL-QUAD', 'INTEL-pentium']
	procTypeValues=[float(i)/len(procTypeList) for i in range(len(procTypeList))]
	procTypeDict=dict(zip(procTypeList,procTypeValues))
	#kMeansCluster()
	#hierarchicalCluster()
	pricePredictor()
	#elbowCurve()






















# def getProcessorType():

# 	'''returns a normalised numeric value for each processor type'''

# 	sqlQuery='SELECT proctype FROM laptops GROUP BY proctype;'
# 	sqlResult=executeQuery(con,sqlQuery)

# 	procTypeList=[]
# 	for res in sqlResult:
# 		val=res[0].lower()

# 		if proctype!='unknown' and proctype not in procTypeList:
# 			procTypeList.append(proctype)

# 	print procTypeList


# 	return {}

