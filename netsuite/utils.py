import ns_config
from netsuite.service import (
    RecordRef,
    SearchPreferences,
    app_info,
    get_soapheaders,
    get_service
)


class obj(object):

    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x)
                   if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b)
                   if isinstance(b, dict) else b)

def _call(record, function):
    soapheaders = get_soapheaders()
    if not record:
        return None
    if not soapheaders:
        return None

    response = function(
        record,
        _soapheaders=soapheaders
    )
    return response


def get(record):
    return _call(record, get_service().get)


def add(record):
    return _call(record, get_service().add)


def update(record):
    return _call(record, get_service().update)


def delete(record):
    return _call(record, get_service().delete)


def get_multiple(array_of_record_references):
    soapheaders = get_soapheaders()
    if not array_of_record_references:
        return None
    if len(array_of_record_references) <= 0:
        return None
    if not soapheaders:
        return None
    response = get_service().getList(
        array_of_record_references,
        _soapheaders=soapheaders
    )
    return response

def add_multiple(array_of_records):
    pass


def update_multiple(array_of_records):
    pass


def delete_multiple(array_of_record_references):
    pass


def get_record_by_type(internal_id, type):
    return get(RecordRef(internalId=internal_id, type=type))


def search_records_using(searchtype):
    soapheaders = get_soapheaders()
    if soapheaders:
        soapheaders['searchPreferences'] = SearchPreferences(
            bodyFieldsOnly=False,
            returnSearchColumns=True,
            pageSize=20
        )
        return get_service().search(
            searchRecord=searchtype,
            _soapheaders=soapheaders
        )
