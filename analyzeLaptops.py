import codecs
import myGetItem as gi
import pickle



def sanitize(mylist):

	newlist=[]
	for a in mylist:
		b=a.strip()

		if not type(b)==str:
			b=unicode(b)
		try:
			float(b)
		except ValueError:
			return None
		#
		#
		#
		newlist.append(b)

	return newlist


def get_laptop_info(specsInfo,sellInfo,itemID):


	#BRAND
	brand=specsInfo.get('Brand','unknown')


	
	#PROCESSOR SPEED
	procSpeed=specsInfo.get('Processor Speed',None)
	if procSpeed==None:
		return None
	else:
		if "ghz" in procSpeed.lower():
			where=procSpeed.lower().find("ghz")
			procSpeed=procSpeed[:where]
		elif "mhz" in procSpeed.lower():
			where=procSpeed.lower().find('mhz')
			procSpeed=procSpeed[:where]
			try:
				procSpeed=float(procSpeed)/1000.0
			except ValueError:
				return None

			procSpeed=unicode(int(procSpeed))
		else:
			print 'unknown specification of processor speed'
			print 'the whole line is:'
			print specsInfo['Processor Speed']
			return None

	#
	#PROCESSOR TYPE
	procType=specsInfo.get('Processor Type','unknown')
	#
	#
	screenSize=specsInfo.get('Screen Size',None)
	if screenSize==None: return None
	if '\"' in screenSize:
		where=screenSize.find('\"')
		screenSize=screenSize[:where]
	elif 'in' in screenSize:
		where=screenSize.find('in')
		screenSize=screenSize[:where]

	#		
	#
	timeLeft=sellInfo.get('timeLeft','unknown')
	#
	listingType=sellInfo.get('listingType','unknown')
	#
	#=================================

	#=================================
	#print 'screenSize is ',screenSize
	#
	#
	#
	#
	hardDrive=None
	for key in specsInfo.keys():
		if 'hard' in key.lower() and 'drive' in key.lower():
			hardDrive=specsInfo[key]

			if hardDrive.lower()=='none':return None
			if 'included' in hardDrive.lower():return None			
			if 'unknown' in hardDrive.lower(): return None
			#if not hardDrive.isdigit(): return None
			hDriveLine=hardDrive
			if 'gb' in hardDrive.lower():
				where=hardDrive.lower().find('gb')
				hardDrive=hardDrive[:where]
			elif 'tb' in hardDrive.lower():
				where=hardDrive.lower().find('tb')
				hardDrive=hardDrive[:where]
				try:
					hardDrive=float(hardDrive)*1000.
				except ValueError:
					return None
				hardDrive=unicode(int(hardDrive))
			else:
				print 'unknown input format in hard drive'
				print 'the whole line is',hDriveLine
				return None
				#a=raw_input('hard drive?')
				#if a=='yes':
				#hardDrive=a
				#else: 
				#	return None
			#
		#
	#
	if hardDrive==None: return None
	#print 'hardDrive==',hardDrive
	#
	#
	#
	#
	memory=specsInfo.get('memory',None)
	if memory==None:
		memory=specsInfo.get('Memory',None)
		if memory==None:
			return None
		#
	#
	if 'gb' in memory.lower():
		where=memory.lower().find('gb')
		memory=memory[:where]
	elif 'mb' in memory.lower():
		where=memory.lower().find('mb')
		try:
			memory=float(memory[:where])
		except ValueError:
			return None

		memory = int(memory/1000.)
		memory=unicode(memory)

	else:
		print 'unknown memory input format ',memory
		return None
	#
	#
	#

	#
	#
	#=========CURRENT PRICE================
	currentPrice=sellInfo.get('ConvertedCurrentPrice',None)
	if currentPrice==None:
		print 'No converted price!'
		return None
	#print 'currentPrice = ',currentPrice

	bidCount=sellInfo.get('BidCount',None)
	if bidCount==None:return None



	#print ' bidCount ',bidCount

	retList=[itemID,procSpeed,screenSize,hardDrive,memory,currentPrice]
	outList=sanitize(retList)
	if outList==None:
		print retList
	else:
		outList.append(brand)
		outList.append(procType)
		outList.append(timeLeft)
		outList.append(listingType)
	return outList

def get_seller_info(sellerInfo,itemID):
	#
	#
	sellerId=sellerInfo.get('UserID','unknown')
	feedBack=sellerInfo.get('PositiveFeedbackPercent','unknown')
	aboutMe=sellerInfo.get('AboutMePage',False)
	#name=sellerInfo.get('name','unknown')
	feedBackRating=sellerInfo.get('FeedbackRatingStar','unknown')

	retList=[itemID,sellerId,feedBack,aboutMe,feedBackRating]
	return retList




def write_header(outFile):

	header='procSpeed'+'\t'
	header+='screenSize'+'\t'
	header+='hardDrive'+'\t'
	header+='memory'+'\t'
	header+='currentPrice'+'\t'
	header+='Brand'+'\t'
	header+='procType'


	outFile.write(header+'\n')

def write_info(info,outFile):

	line=''
	for element in info:
		line+=element+'\t'
	#
	outFile.write(line+'\n')



def get_data_from_file(inFileName,outFileName):



	outFile=codecs.open(outFileName,'a','utf-8')
	outSellerInfoFile=codecs.open('sellerDatabase.txt','a','utf-8')
	raw_input('the file is now on append mode. Is this OK?')
	f=codecs.open(inFileName,'r','utf-8')
	l=f.readlines()

	for i,line in enumerate(l[1:]):

		if i<1380:
			continue
			
		print 'iteration ',i
		splitLine=line.split('\t')
		itemID=splitLine[0]
		itemSpecs,sellInfo,sellerInfo=gi.get_info_from_item(itemID)
		if len(itemSpecs)==0:
			continue
		if len(sellInfo)==0:
			continue
		if len(sellerInfo)==0:
			continue
	

		info=get_laptop_info(itemSpecs,sellInfo,itemID)
		if not info==None:
			write_info(info,outFile)

		sellerinfo=get_seller_info(sellerInfo,itemID)
		write_info(sellerinfo,outSellerInfoFile)

		#raw_input('')
	outFile.close()


if __name__=='__main__':

	get_data_from_file('newLaptops.txt','newDatabase.txt')
