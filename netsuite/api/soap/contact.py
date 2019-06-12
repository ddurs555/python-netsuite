from netsuite.api.soap.utils import (
    add,
    get,
    update,
    delete
)
from netsuite.api.soap.service import (
    RecordRef,
    Contact,
)

"""
ns13:Contact(nullFieldList: ns0:NullField, 
            customForm: ns0:RecordRef, 
            entityId: xsd:string, 
            contactSource: ns0:RecordRef, 
            company: ns0:RecordRef, 
            salutation: xsd:string, 
            firstName: xsd:string, 
            middleName: xsd:string, 
            lastName: xsd:string, 
            title: xsd:string, 
            phone: xsd:string, 
            fax: xsd:string, 
            email: xsd:string, 
            defaultAddress: xsd:string, 
            isPrivate: xsd:boolean, 
            isInactive: xsd:boolean, 
            subsidiary: ns0:RecordRef, 
            phoneticName: xsd:string, 
            categoryList: ns13:CategoryList, 
            altEmail: xsd:string, 
            officePhone: xsd:string, 
            homePhone: xsd:string, 
            mobilePhone: xsd:string, 
            supervisor: ns0:RecordRef, 
            supervisorPhone: xsd:string, 
            assistant: ns0:RecordRef, 
            assistantPhone: xsd:string, 
            comments: xsd:string, 
            globalSubscriptionStatus: ns6:GlobalSubscriptionStatus, 
            image: ns0:RecordRef, 
            billPay: xsd:boolean, 
            dateCreated: xsd:dateTime, 
            lastModifiedDate: xsd:dateTime, 
            addressbookList: ns13:ContactAddressbookList, 
            subscriptionsList: ns13:SubscriptionsList, 
            customFieldList: ns0:CustomFieldList, 
            internalId: xsd:string, 
            externalId: xsd:string)
"""
MODULE_TYPE = 'contact'


def contact_from_dictionary(field_dictionary):
    return Contact(**field_dictionary)

def get_contact(internal_id):
    return get(RecordRef(type=MODULE_TYPE, internalId=internal_id))


def add_contact(contact):
    return add(contact)


def update_contact(internal_id, field_dictionary):
    contact = Contact(internalId=internal_id, **field_dictionary)
    response = update(contact)
    r = response.body.writeResponse
    if r.status.isSuccess:
        return True
    return False

def delete_contact(internal_id):
    return delete(RecordRef(type=MODULE_TYPE, internalId=internal_id))