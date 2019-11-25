try:
    import ns_config
except ImportError:
    raise ImportError('Please review README.rst for python_netsuite package: ns_config.py required on path')

def get_next_soap_app():
    return _get_next_app('soap')

def get_next_restlet_app():
    return _get_next_app('restlet')

def _get_next_app(type):
    count = 1
    size = len(ns_config.NS_APPS)

    for app in next(iter(ns_config.NS_APPS)):
        if app.type == type:
            return app
        if count == size:
            raise IndexError('No '+type+' app found')
        count += 1


