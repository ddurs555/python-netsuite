Python Netsuite
===============
LICENSE: MIT


Netsuite Python Toolkit for SuiteTalk SOAP API.


Example usage
-------------
Copy :code:`ns_config.py.txt` into :code:`ns_config.py` and update with your credentials.

.. code:: python

    from netsuite.api.item
    record = item.get_item('1234')


NetSuite Documentation
----------------------
* `SuiteTalk Documentation <http://www.netsuite.com/portal/developers/resources/suitetalk-documentation.shtml>`_
* `Schema Browser (CashSale example) <http://www.netsuite.com/help/helpcenter/en_US/srbrowser/Browser2019_1/schema/record/cashsale.html?mode=package>`_

Development
-----------

* Get Netsuite WSDL export to look at

.. code:: bash

    mkdir archive
    python3 -mzeep https://webservices.sandbox.netsuite.com/wsdl/v2019_1_0/netsuite.wsdl > archive/wsdl.txt
    # improve formatting
    sed -i -e 's/, /, \n          /g' archive/wsdl.txt
    less archive/wsdl.txt

* Add Netsuite models you need to work with based on WSDL to :code:`netsuite/service.py`.
* Add functions to get, create, lookup... these model instances to :code:`netsuite/api/[model].py`.
* Add tests to :code:`tests.py`. Run tests using :code:`./tests.py`
