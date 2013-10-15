# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
from optparse import OptionParser
#from getItemInfo import *


sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

import ebaysdk
from ebaysdk import finding


def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='myebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")

    (opts, args) = parser.parse_args()
    return opts, args


def run(opts,findQuery):


    api = finding(siteid='EBAY-NLBE', debug=opts.debug, appid=opts.appid, config_file=opts.yaml,
                  warnings=True)

    #keywords=findQuery['keywords']
    #categoryId=findQuery['categoryId']
    #itemFilter=findQuery['itemFilter']


    api.execute('findItemsAdvanced',findQuery)
#    api.execute('findItemsAdvanced', {
#         'keywords': "laptop",
#         'categoryid': "51148",
#         'itemFilter': [
#             {'name': 'Condition',
#              'value': 'Used'},
#             {'name': 'LocatedIn',
#              'value': 'GB'}
#             
#         ],
#         'affiliate': {'trackingId': 1},
#         'sortOrder': 'CountryDescending',
#     })

    if api.error():
        raise Exception(api.error())

    if api.response_content():
        print "Call Success: %s in length" % len(api.response_content())

    print "Response code: %s" % api.response_code()
    print "Response DOM: %s" % api.response_dom()

    dictstr = "%s" % api.response_dict()
    return api.response_dict()
    #print "Response dictionary: %s..." % dictstr[:2500]


def run2(opts):
    api = finding(debug=opts.debug, appid=opts.appid, config_file=opts.yaml)
    api.execute('findItemsByProduct', '<productId type="ReferenceID">53039031</productId>')

    if api.error():
        raise Exception(api.error())

    if api.response_content():
        print "Call Success: %s in length" % len(api.response_content())

    print "Response code: %s" % api.response_code()
    print "Response DOM: %s" % api.response_dom()

    dictstr = "%s" % api.response_dict()
    print "Response dictionary: %s..." % dictstr[:500]




if __name__ == "__main__":
    print "Finding samples for SDK version %s" % ebaysdk.get_version()
    (opts, args) = init_options()

    findQuery= {'keywords': "laptop" ,#'categoryId': [{'value': "177"}],
        'itemFilter': [{'name': "Condition",'value': "New"},{'name': "LocatedIn",'value': "US"}],
        'paginationInput':{'entriesPerPage':100,'pageNumber':1}
    }      
    dict1=run(opts,findQuery)
    #for algo,val in dict1.iteritems():
    #    print algo
    #    raw_input('')
    #
    res=dict1['searchResult']
    items=res['item']#this is a list
    for element in items: 
      categoryId=element['primaryCategory']['categoryId']['value']     
      print element
      raw_input('')
      print categoryId






