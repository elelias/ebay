

import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets




def get_latop_data():

	print 'hello'
	inFile="laptopData.txt"
	a=[]
	f=open(inFile).readlines()
	for line in f[1:]:
		myl=line.strip().split('\t')
		newmyl=[]
		for element in myl:
			newmyl.append(float(element))
		a.append(newmyl)


	#nparray=np.array(a)
	return a



a=get_latop_data()
X=np.array(a)#
print 'the size ',X.shape
#
#
np.random.seed(5)
#
#
centers=[[1,1],[-1,1],[1,-1]]#???????


#X=data
#print X
#raw_input("")

#print X[:, 3]
#raw_input('')
#y=iris.target


estimators={'ebay_laptop_data': KMeans(n_clusters=3)}

fignum=1

for name,est in estimators.iteritems():


	est.fit(X) #this computes the k-means clustering


	p=[]
	p.append((0,'speed'))
	p.append((1,'screen size'))
	p.append((2,'hard drive'))
	p.append((3,'memory'))
	p.append((4,'price'))
	p.append((5,'bid count'))


	plotDict=[]
	for i in range(0,4):
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
		print X[:,fAxis]
		print X[:,sAxis]
		print X[:,tAxis]				

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





















