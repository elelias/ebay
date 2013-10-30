
from testFinding import *
from processResult import process_query_result,get_header
import codecs

def make_dataset(findQuery,outFile):

	#find them and save them to a file
	(opts, args) = init_options()
	dict1=run(opts,findQuery)
	result=dict1['searchResult']
	items=result['item']

	print 'there are ',len(items),'items here'
	for element in items:

		categoryId=element['primaryCategory']['categoryId']['value'] 
		line=process_query_result(element)
		outFile.write(line+'\n')


if __name__=='__main__':


	outFile=codecs.open('newLaptops.txt','a','utf-8')
	line=get_header()
	outFile.write(line+'\n')
	#
	#	
	for pageNum in range(100):
		findQuery= {'keywords': "laptop" ,'categoryId':['177','111422'],
			'itemFilter': [{'name': "LocatedIn",'value': "US"}],	    	
	    	'paginationInput':{'entriesPerPage':100,'pageNumber':pageNum+1}
		}  


		make_dataset(findQuery,outFile)

		print pageNum

