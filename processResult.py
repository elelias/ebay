



def get_header():

	line=unicode('itemId')+'\t'
	line+=unicode('categoryId')+'\t'
	line+=unicode('title')+'\t'
	line+=unicode('categoryName')+'\t'
	line+=unicode('country')+'\t'
	line+=unicode('postalCode')+'\t'
	line+=unicode('currentPrice')+'\t'
	line+=unicode('currencyId')	+'\t'						
	line+=unicode('convertedPrice')+'\t'								

	print 'the line ',line
	return line


def process_query_result(element):

	
	line=''
	itemId=element['itemId']['value']
	categoryId=element['primaryCategory']['categoryId']['value']
	title=element['title']['value']
	categoryName=element['primaryCategory']['categoryName']['value']
	country=element['country']['value']
	autoPay=element['autoPay']['value']
	postalCode=element.get('postalCode',{'value':'NoValue'})['value']
	sellingStatus=element['sellingStatus']
	currentPrice=sellingStatus['currentPrice']['value']
	currencyId=sellingStatus['currentPrice']['currencyId']['value']
	convertedPrice=sellingStatus['convertedCurrentPrice']['value']
	#
	#
	line+=unicode(itemId)+'\t'
	line+=unicode(categoryId)+'\t'
	line+=unicode(title)+'\t'
	line+=unicode(categoryName)+'\t'
	line+=unicode(country)+'\t'
	line+=unicode(postalCode)+'\t'
	line+=unicode(currentPrice)+'\t'
	line+=unicode(currencyId)+'\t'
	line+=unicode(convertedPrice)+'\t'
	#
	#
	#print 'the line is ',line

	#print categoryId,title,categoryName,country,autoPay,postalCode,currentPrice,currencyId,convertedPrice
	#raw_input('vamos')
	return line