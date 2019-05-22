from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
import time
import urllib.parse
import hmac
from hashlib import sha1 as SHA1
import oauth2 as oauth
import ns_config
import base64


cache = SqliteCache(timeout=606024*365)
transport = Transport(cache=cache)
client = Client(ns_config.WSDL_URL, transport=transport)

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

def make_passport():
    role = RecordRef(internalId=ns_config.NS_ROLE)
    return Passport(email=ns_config.NS_EMAIL,
    password=ns_config.NS_PASSWORD,
    account=ns_config.NS_ACCOUNT,
    role=role)

#ns0:TokenPassportSignature(xsd:string, algorithm: xsd:string)
#ns0:TokenPassport(account: xsd:string, consumerKey: xsd:string, token: xsd:string, nonce: xsd:string, timestamp: xsd:long, signature: ns0:TokenPassportSignature)
def make_token_passport():
    nonce = oauth.generate_nonce()
    timestamp = str(int(time.time()))
    signature = generate_signature(
        account_id=ns_config.NS_ACCOUNT,
        consumer_key=ns_config.OAUTH_KEYS['consumer'].key,
        consumer_secret=ns_config.OAUTH_KEYS['consumer'].secret,
        token_key=ns_config.OAUTH_KEYS['token'].key,
        token_secret=ns_config.OAUTH_KEYS['token'].secret,
        nonce=nonce,
        timestamp=timestamp
    )
    token_signature = TokenPassportSignature(
        signature,
        algorithm="HMAC-SHA1"
    )
    return TokenPassport(
        account=ns_config.NS_ACCOUNT,
        consumerKey=ns_config.OAUTH_KEYS['consumer'].key,
        token=ns_config.OAUTH_KEYS['token'].key,
        nonce=nonce, timestamp=timestamp,
        signature=token_signature
    )

def get_soapheaders():
    soapheaders = None
    if ns_config.AUTH == 'simple':
        soapheaders = {
            'passport': make_passport()
        }
    elif ns_config.AUTH == 'tba':
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
Account = model('ns17:Account')

Subsidiary = model('ns17:Subsidiary')
ListOrRecordRef = model('ns0:ListOrRecordRef')
ApplicationInfo = model('ns4:ApplicationInfo')
CustomerSearchBasic = model('ns5:CustomerSearchBasic')
ItemSearchBasic = model('ns5:ItemSearchBasic')
SearchPreferences = model('ns4:SearchPreferences')
SearchBooleanField = model('ns0:SearchBooleanField')
SearchStringField = model('ns0:SearchStringField')
SearchStringFieldOperator = model('ns1:SearchStringFieldOperator')
SearchMultiSelectField = model('ns0:SearchMultiSelectField')
Customer = model('ns13:Customer')

Contact = model('ns13:Contact')
Address = model('ns5:Address')
Country = model('ns6:Country')

InventoryItem = model('ns17:InventoryItem')
InventoryItemBinNumber = model('ns17:InventoryItemBinNumber')
InventoryItemBinNumberList = model('ns17:InventoryItemBinNumberList')

ItemVendor = model('ns17:ItemVendor')
ItemVendorList = model('ns17:ItemVendorList')

CashSale = model('ns19:CashSale')
CashSaleItem = model('ns19:CashSaleItem')
CashSaleItemList = model('ns19:CashSaleItemList')

SalesOrder = model('ns19:SalesOrder')
SalesOrderItem = model('ns19:SalesOrderItem')
SalesOrderItemList = model('ns19:SalesOrderItemList')

app_info = ApplicationInfo(applicationId=ns_config.NS_APPID)
