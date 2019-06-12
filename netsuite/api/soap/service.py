from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from hashlib import sha1 as SHA1
from netsuite.api.common.utils import get_next_soap_app
import time
import urllib.parse
import hmac
import oauth2 as oauth
import ns_config
import base64
import itertools


cache = SqliteCache(timeout=606024*365)
transport = Transport(cache=cache)
client = Client(ns_config.WSDL_URL, transport=transport)
applications = itertools.cycle(ns_config.NS_APPS)

def hmac_sha1(key, data):
    hashed = hmac.new(bytes(key,'utf-8'), bytes(data,'utf-8'), SHA1)
    return base64.b64encode(hashed.digest())

def generate_signature(account_id, consumer_key, consumer_secret, token_key, token_secret, nonce, timestamp):
    # create base string

    basestring = urllib.parse.quote(account_id) + "&" +\
                 urllib.parse.quote(consumer_key) + "&" +\
                 urllib.parse.quote(token_key) + "&" +\
                 urllib.parse.quote(nonce) + "&" +\
                 urllib.parse.quote(timestamp)

    # create signing key
    signingkey = urllib.parse.quote(consumer_secret) + "&" + urllib.parse.quote(token_secret)
    # compute signature
    return hmac_sha1(signingkey, basestring)

#ns0:TokenPassportSignature(xsd:string, algorithm: xsd:string)
#ns0:TokenPassport(account: xsd:string, consumerKey: xsd:string, token: xsd:string, nonce: xsd:string, timestamp: xsd:long, signature: ns0:TokenPassportSignature)
def make_token_passport():
    nonce = oauth.generate_nonce()
    timestamp = str(int(time.time()))
    application = get_next_soap_app(applications)

    if ns_config.DEBUG:
        print("Application ID: "+application['application_id'])

    signature = generate_signature(
        account_id=ns_config.NS_ACCOUNT,
        consumer_key=application['consumer'].key,
        consumer_secret=application['consumer'].secret,
        token_key=application['token'].key,
        token_secret=application['token'].secret,
        nonce=nonce,
        timestamp=timestamp
    )
    token_signature = TokenPassportSignature(signature, algorithm="HMAC-SHA1")
    return TokenPassport(
        account=ns_config.NS_ACCOUNT,
        consumerKey=application['consumer'].key,
        token=application['token'].key,
        nonce=nonce, timestamp=timestamp,
        signature=token_signature
    )

def get_soapheaders():
    soapheaders = {
        'tokenPassport': make_token_passport()
    }
    return soapheaders

def get_service():
    base_url = client.service.getDataCenterUrls(account=ns_config.NS_ACCOUNT).body.getDataCenterUrlsResult.dataCenterUrls.webservicesDomain
    return client.create_service('{urn:platform_2019_1.webservices.netsuite.com}NetSuiteBinding', base_url+'/services/NetSuitePort_2019_1')

model = client.get_type

Passport = model('ns0:Passport')
TokenPassport = model('ns0:TokenPassport') #ns0:TokenPassport(account: xsd:string, consumerKey: xsd:string, token: xsd:string, nonce: xsd:string, timestamp: xsd:long, signature: ns0:TokenPassportSignature)
TokenPassportSignature = model('ns0:TokenPassportSignature') #ns0:TokenPassportSignature(xsd:string, algorithm: xsd:string)
RecordRef = model('ns0:RecordRef')
ListOrRecordRef = model('ns0:ListOrRecordRef')
SearchBooleanField = model('ns0:SearchBooleanField')
SearchStringField = model('ns0:SearchStringField')
SearchMultiSelectField = model('ns0:SearchMultiSelectField')

SearchStringFieldOperator = model('ns1:SearchStringFieldOperator')

ApplicationInfo = model('ns4:ApplicationInfo')
SearchPreferences = model('ns4:SearchPreferences')

CustomerSearchBasic = model('ns5:CustomerSearchBasic')
ItemSearchBasic = model('ns5:ItemSearchBasic')
Address = model('ns5:Address')
Country = model('ns6:Country')

Customer = model('ns13:Customer')
Contact = model('ns13:Contact')

Account = model('ns17:Account')
Subsidiary = model('ns17:Subsidiary')
Currency = model('ns17:Currency')
InventoryItem = model('ns17:InventoryItem')
InventoryItemBinNumber = model('ns17:InventoryItemBinNumber')
InventoryItemBinNumberList = model('ns17:InventoryItemBinNumberList')
ItemVendor = model('ns17:ItemVendor')
ItemVendorList = model('ns17:ItemVendorList')
Price = model('ns17:Price')
PriceList = model('ns17:PriceList')
Pricing = model('ns17:Pricing')
PriceLevel = model('ns17:PriceLevel')

PricingMatrix = model('ns17:PricingMatrix')

CashSale = model('ns19:CashSale')
CashSaleItem = model('ns19:CashSaleItem')
CashSaleItemList = model('ns19:CashSaleItemList')

SalesOrder = model('ns19:SalesOrder')
SalesOrderItem = model('ns19:SalesOrderItem')
SalesOrderItemList = model('ns19:SalesOrderItemList')

#app_info = ApplicationInfo(applicationId=ns_config.NS_APPID)
