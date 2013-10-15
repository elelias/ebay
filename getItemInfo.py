

import httplib, ConfigParser, codecs
from xml.dom.minidom import parse, parseString


# FUNCTION: buildHttpHeaders
# Build together the required headers for the HTTP request to the eBay API
def buildHttpHeaders():
    global devID,appID,certID,serverUrl,serverDir,userToken  
    global verb,siteID, compatabilityLevel
    httpHeaders = {"X-EBAY-API-COMPATIBILITY-LEVEL": compatabilityLevel,
               "X-EBAY-API-DEV-NAME": devID,
               "X-EBAY-API-APP-NAME": appID,
               "X-EBAY-API-CERT-NAME": certID,
               "X-EBAY-API-CALL-NAME": verb,
               "X-EBAY-API-SITEID": siteID,
               "Content-Type": "text/xml"}
    print httpHeaders
    return httpHeaders

# FUNCTION: buildRequestXml
# Build the body of the call (in XML) incorporating the required parameters to pass
def buildRequestXml(detailLevel, viewAllNodes,ItemID):

    global devID,appID,certID,serverUrl,serverDir,userToken
    requestXml = "<?xml version='1.0' encoding='utf-8'?>"+\
              "<GetItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
              "<RequesterCredentials><eBayAuthToken>" + userToken + "</eBayAuthToken></RequesterCredentials>"
    
    if (detailLevel != ""):
        requestXml = requestXml + "<DetailLevel>" + detailLevel + "</DetailLevel>"
     
    requestXml = requestXml + "<ItemID>"+str(ItemID)+ "</ItemID>"
    #requestXml = requestXml + "<Item><Site>" + str(siteID) + "</Site></Item>"+\
     #x         "<ViewAllNodes>" + str(viewAllNodes) + "</ViewAllNodes>"
    requestXml = requestXml+  "</GetItemRequest>"

    print 'the request is ',requestXml
    return requestXml



def getItemInfo(ItemID):




  #Setup the HTML Page with name of call as title
  verb='GetItem'
  print "<HTML>"
  print "<HEAD><TITLE>", verb, "</TITLE></HEAD>"
  print "<BODY>"


  #Send Content-type header to browser
  print "Content-type: text/html"
  print

  #import the HTTP, DOM and ConfigParser modules needed


  global devID,appID,certID,serverUrl,serverDir,userToken
  # open config file
  config = ConfigParser.ConfigParser()
  config.read("config.ini")

  # specify eBay API dev,app,cert IDs
  devID = config.get("Keys", "Developer")
  appID = config.get("Keys", "Application")
  certID = config.get("Keys", "Certificate")

  #get the server details from the config file
  serverUrl = config.get("Server", "URL")
  serverDir = config.get("Server", "Directory")


  # specify eBay token
  # note that eBay requires encrypted storage of user data
  userToken = config.get("Authentication", "Token")



  #eBay Call Variables
  #siteID specifies the eBay international site to associate the call with
  #0 = US, 2 = Canada, 3 = UK, ....
  global siteID,verb,compatabilityLevel  
  siteID = "0"
  #verb specifies the name of the call
  verb = "GetItem"
  #The API level that the application conforms to
  compatabilityLevel = "719"






 # specify the connection to the eBay environment
  print 'the fucking serverUrl is ',serverUrl
  print 'the fkcing serverDir is ',serverDir
  connection = httplib.HTTPSConnection(serverUrl)
  # specify a POST with the results of generateHeaders and generateRequest
  # detailLevel = 1, ViewAllNodes = 1  - this gets the entire tree
  connection.request("POST", serverDir, buildRequestXml("ItemReturnAttributes", "1",ItemID), buildHttpHeaders())
  response = connection.getresponse()
  if response.status != 200:
      print "Error sending request for entire tree: " + response.reason
      exit
  else: #response successful
      # store the response data
      data = response.read()
      #print data
      # parse the response data into a DOM
      catTree = parseString(data)
      #uData = unicode(data)
      catTreeFile='someFile.txt'
      print data      
      if not "This item cannot be accessed" in str(data):

        fileObj = open( catTreeFile, "a")
        fileObj.write(data)
        fileObj.close()
  # close the connection
  connection.close()


if __name__=='__main__':


  ItemID='261285565259'
  getItemInfo(ItemID)

