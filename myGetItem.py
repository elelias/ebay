
import cgi, os
#import the HTTP, DOM and ConfigParser modules needed
import httplib, ConfigParser
from xml.dom.minidom import parse, parseString
from getIDs import get_id
import time


def getSingleValue(node,tag):
    nl=node.getElementsByTagName(tag)
    if len(nl)>0:
        tagNode=nl[0]
        if tagNode.hasChildNodes():
           return tagNode.firstChild.nodeValue
    return '-1'


def buildHttpHeaders():

    appID,devID,certID,userToken=get_id("production")
    compatabilityLevel="679"
    siteID=0
    verb="GetItem"
    httpHeaders = {"X-EBAY-API-COMPATIBILITY-LEVEL": compatabilityLevel,    
               "X-EBAY-API-DEV-NAME": devID,
               "X-EBAY-API-APP-NAME": appID,
               "X-EBAY-API-CERT-NAME": certID,
               "X-EBAY-API-CALL-NAME": verb,
               "X-EBAY-API-SITEID": siteID,
               "Content-Type": "text/xml"}
    return httpHeaders

# FUNCTION: buildRequestXml
# Build the body of the call (in XML) incorporating the required parameters to pass
def buildRequestXml(itemID):

    appID,devID,certID,userToken=get_id("production")    
    requestXml = "<?xml version='1.0' encoding='utf-8'?>"+\
              "<GetItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
              "<RequesterCredentials><eBayAuthToken>" + userToken + "</eBayAuthToken></RequesterCredentials>" + \
              "<IncludeItemSpecifics>True</IncludeItemSpecifics>"+\
              "<DetailLevel>ItemReturnAttributes</DetailLevel>"+\
              "<ItemID>" + itemID + "</ItemID>"+\
              "<WarningLevel>High</WarningLevel>"+\
              "</GetItemRequest>"
    return requestXml


def get_itemId(itemID):
    #get itemID
    

    # open config file
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    #get the server details from the config file
    serverUrl = config.get("Server", "URL")
    serverDir = config.get("Server", "Directory")
    #
    #
    # specify the connection to the eBay Sandbox environment
    connection = httplib.HTTPSConnection(serverUrl)

    # specify a POST with the results of generateHeaders and generateRequest
    connection.request("POST", serverDir, buildRequestXml(itemID), buildHttpHeaders())
    response = connection.getresponse()

    # if response was unsuccessful, output message
    if response.status != 200:
        print "Error sending request:" + response.reason
        
    else: #response successful
        # store the response data and close the connection
        data = response.read()
        connection.close()
        
        # parse the response data into a DOM
        response = parseString(data)

        # check for any Errors
        errorNodes = response.getElementsByTagName('Errors')
        if (errorNodes != []): #there are errors
            print "<P><B>eBay returned the following errors</B>"
            #Go through each error:
            for error in errorNodes:
                #output the error code and short message (with special characters replaces)
                print "<P>" + ((error.getElementsByTagName('ErrorCode')[0]).childNodes[0]).nodeValue
                print " : " + ((error.getElementsByTagName('ShortMessage')[0]).childNodes[0]).nodeValue.replace("<", "&lt;")
                #output Long Message (with special characters replaces) if it exists (depends on ErrorLevel setting)
                if (error.getElementsByTagName('LongMessage')!= []):
                    print "<BR>" + ((error.getElementsByTagName('LongMessage')[0]).childNodes[0]).nodeValue.replace("<", "&lt;")

        else: #eBay returned no errors - output results
            


            return response            

            # cat=((primaryCategoryNode.getElementsByTagName('CategoryName')[0]).childNodes[0]).nodeValue
            # sta= ((listingDetailsNode.getElementsByTagName('StartTime')[0]).childNodes[0]).nodeValue
            # end=((listingDetailsNode.getElementsByTagName('EndTime')[0]).childNodes[0]).nodeValue

            # # get the item's details and output them
            # print "<P><B>" + ((response.getElementsByTagName('Title')[0]).childNodes[0]).nodeValue + " (" + itemID + ")</B>"
            # primaryCategoryNode = response.getElementsByTagName('PrimaryCategory')[0];
            # print "<BR>Category: " + ((primaryCategoryNode.getElementsByTagName('CategoryName')[0]).childNodes[0]).nodeValue
            # listingDetailsNode = response.getElementsByTagName('ListingDetails')[0];
            # print "<BR>Started: " + ((listingDetailsNode.getElementsByTagName('StartTime')[0]).childNodes[0]).nodeValue
            # print "<BR>Ends: " + ((listingDetailsNode.getElementsByTagName('EndTime')[0]).childNodes[0]).nodeValue


            # # get the item's price/bid details and output them
            # sellingStatusNode = response.getElementsByTagName('SellingStatus')[0];
            # currency = (sellingStatusNode.getElementsByTagName('CurrentPrice')[0]).getAttribute('currencyID');
            # print "<P>Current Price: " + ((sellingStatusNode.getElementsByTagName('CurrentPrice')[0]).childNodes[0]).nodeValue + currency
            # print "<BR>Start Price: " + ((response.getElementsByTagName('StartPrice')[0]).childNodes[0]).nodeValue + currency
            # print "<BR>BuyItNow Price: " + ((response.getElementsByTagName('BuyItNowPrice')[0]).childNodes[0]).nodeValue + currency
            # print "<BR>Bid Count: " + ((sellingStatusNode.getElementsByTagName('BidCount')[0]).childNodes[0]).nodeValue
            # #
            # #
            # cPrice=((sellingStatusNode.getElementsByTagName('CurrentPrice')[0]).childNodes[0]).nodeValue
            # startP=((response.getElementsByTagName('StartPrice')[0]).childNodes[0]).nodeValue 
            # buyNowP=((response.getElementsByTagName('BuyItNowPrice')[0]).childNodes[0]).nodeValue
            # bidC=((sellingStatusNode.getElementsByTagName('BidCount')[0]).childNodes[0]).nodeValue
            # sellId=None
            # sellRegDate=None
            # sellFeedBackScore=None



            # #Get and output seller details if there
            # seller = response.getElementsByTagName('Seller')
            # if (seller!=[]):
            #     print "<P><B>Seller</B>"
            #     print "<BR>UserID: " + (((seller[0]).getElementsByTagName('UserID')[0]).childNodes[0]).nodeValue
            #     print "<BR>Registered: " + (((seller[0]).getElementsByTagName('RegistrationDate')[0]).childNodes[0]).nodeValue
            #     print "<BR>Feebback Score: " + (((seller[0]).getElementsByTagName('FeedbackScore')[0]).childNodes[0]).nodeValue

            #     #sell



             
        # force garbage collection of the DOM object
        #response.unlink()

def get_response(itemID):

    notOK=True
    for _ in range(5):
        response=get_itemId(itemID)

        if response==None:
            print 'No Response. Trying again in 3 seconds...'
            print 'I am trying with the itemID = ',itemID
            time.sleep(3)
        else:
            return response

    return 'NoResponse'





def getSellingStatus(response):


    #response=get_itemId(itemID)
    if response=='NoResponse':
        print 'Cant get a response!'
        return {}

    if response==None:
        print 'Response is None. Calling with itemID= ',itemID
        return {}

    sellingStatus = response.getElementsByTagName('SellingStatus')
    #currency = (sellingStatusNode.getElementsByTagName('CurrentPrice')[0]).getAttribute('currencyID');
    #print "<P>Current Price: " + ((sellingStatusNode.getElementsByTagName('CurrentPrice')[0]).childNodes[0]).nodeValue + currency
    #print "<BR>Start Price: " + ((response.getElementsByTagName('StartPrice')[0]).childNodes[0]).nodeValue + currency
    #print "<BR>BuyItNow Price: " + ((response.getElementsByTagName('BuyItNowPrice')[0]).childNodes[0]).nodeValue + currency
    #print "<BR>Bid Count: " + ((sellingStatusNode.getElementsByTagName('BidCount')[0]).childNodes[0]).nodeValue

    sellDict={}
    try:
        sellNode=sellingStatus[0]
    except IndexError:
        return {}

    for c in sellNode.childNodes:
        #getSellingStatus
        nodeName=c.nodeName
        nodeValue=c.childNodes[0].nodeValue
        sellDict[nodeName]=nodeValue

    return sellDict









def getItemProperties(response):

    #response=get_itemId(itemID)
    if response=='NoResponse':
        print 'Cant get a response!'
        return {}

    if response==None:
        print 'No Reponse. Calling with itemID= ',itemID
        return {}


    attributeSet=response.getElementsByTagName('ItemSpecifics')
    if attributeSet==None:
        return {}
    try:
        attributeNode=attributeSet[0]
    except IndexError:
        #print 'out of bounds error',attributeSet
        return {}
    #if not type(attributeSet)==list: return {}
    #attributeNode=attributeSet[0]
    attDict={}    
    for c in attributeNode.childNodes:

        detail=[]        
        for g in c.childNodes:


            for k in g.childNodes:
                if not 'ItemSpecific' in k.nodeValue:
                    detail.append(k.nodeValue)
                    #print ''
                    #print k
                    #print k.nodeValue
                    #print ''
        #print detail
        if len(detail)>1:
            attDict[detail[0]]=detail[1]

    return attDict



def get_info_from_item(itemID):

    response=get_response(itemID)
    itemSpecs=getItemProperties(response)
    sellInfo=getSellingStatus(response)


    return itemSpecs,sellInfo



if __name__=='__main__':


    itemSpecs,sellInfo=get_info_from_item("350865067425")
    print itemSpecs
    print sellInfo


    #print getItemProperties("350865067425")
    #print getSellingStatus("350865067425")    
    # response=get_itemId("350865067425")
    # primaryCategoryNode = ((response.getElementsByTagName('PrimaryCategory')[0]).childNodes[0]).nodeValue
    # #sellerContactDetails = ((response.getElementsByTagName("SellerContactDetails")[0]).childNodes[0]).nodeValue
    # #sellerNode=response.getElementsByTagName("Seller")[0]
    # #feedback=getSingleValue(sellerNode,"UserID")
    # attributeSet=response.getElementsByTagName('ItemSpecifics')
    # #brand=getSingleValue(attributeSet[0],'Brand')

    # attributeNode=attributeSet[0]
    # attDict={}    
    # for c in attributeNode.childNodes:

    #     detail=[]        
    #     for g in c.childNodes:


    #         for k in g.childNodes:
    #             if not 'ItemSpecific' in k.nodeValue:
    #                 detail.append(k.nodeValue)
    #                 #print ''
    #                 #print k
    #                 #print k.nodeValue
    #                 #print ''
    #     print detail
    #     if len(detail)>1:
    #         attDict[detail[0]]=detail[1]

    # print 'the properties are ',attDict








