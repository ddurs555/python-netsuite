"""
Product search
"""
from netsuite.client import client, passport, app_info
from netsuite.service import (ItemSearchBasic,
                              SearchBooleanField,
                              SearchPreferences)
from netsuite.utils import get_record_by_type
from lxml import etree


def get_product(internal_id):
    return get_record_by_type('inventoryItem', internal_id)


def find_products():
    item_search = ItemSearchBasic(isInactive=SearchBooleanField(searchValue=True))
    search_preferences = SearchPreferences(bodyFieldsOnly=False,
                                           returnSearchColumns=True,
                                           pageSize=20)
    print('raw xml')
    print(etree.tostring(client.service._binding.create_message('search', item_search, _soapheaders={
        'searchPreferences': search_preferences,
        'applicationInfo': app_info,
        'passport': passport
    })))

    result = client.service.search(searchRecord=item_search, _soapheaders={
        'searchPreferences': search_preferences,
        'applicationInfo': app_info,
        'passport': passport,
    })
    print('result:')
    print(result)
