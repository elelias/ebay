
from testFinding import *
from processResult import process_query_result,get_header
import codecs

def make_dataset(findQuery,outFile,categoryIdList):

	#find them and save them to a file
	(opts, args) = init_options()
	dict1=run(opts,findQuery)
	result=dict1['searchResult']
	items=result['item']

	#outFile=open(fileName,'w')

	print 'there are ',len(items),'items here'
	for element in items:

		categoryId=element['primaryCategory']['categoryId']['value'] 

		#print 'the type is ',type(categoryId)
		if len(categoryIdList) > 0:
			if categoryId not in categoryIdList:
				continue

		line=process_query_result(element)
		print outFile 
		print 'line is'+line+'line ends'		
		#print type(line)

		outFile.write(line+'\n')


		#print 'trying this shit ',itemId
		#
		#print element
		#raw_input('')
		#info=getItemInfo(itemId)
		#print info

		#raw_input('')	


if __name__=='__main__':


	#outFile=open('testFile.txt','a')
	outFile=codecs.open('newLaptops.txt','a','utf-8')
	line=get_header()
	outFile.write(line+'\n')
	#
	#	
	for pageNum in range(100):
		findQuery= {'keywords': "laptop" ,#'categoryId':[{"170083}]
	    	#'itemFilter': [{'name': "Condition",'value': "New"},{'name': "LocatedIn",'value': "US"}],
			'itemFilter': [{'name': "LocatedIn",'value': "US"}],	    	
	    	'paginationInput':{'entriesPerPage':100,'pageNumber':pageNum+1}
		}  


		categoryIdList=['177','111422']


		make_dataset(findQuery,outFile,categoryIdList)



