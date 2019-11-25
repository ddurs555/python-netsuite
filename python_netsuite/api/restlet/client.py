from python_netsuite.api.common.utils import get_app_by_id
import oauth2 as oauth
import requests
import time
import json
try:
    import ns_config
except ImportError:
    raise ImportError('Please review README.rst for python_netsuite package: ns_config.py required on path')




SIG_METHOD = oauth.SignatureMethod_HMAC_SHA1()


def _get_params(token, consumer):
    return {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': str(int(time.time())),
        'oauth_token': token.key,
        'oauth_consumer_key': consumer.key,
    }


def _get_oauth_request(app, method, url):
    return oauth.Request(
        method=method,
        url=url,
        parameters=_get_params(token=app['token'], consumer=app['consumer'])
    )

def _generate_headers(app, method, url):
    req = _get_oauth_request(app=app, method=method, url=url)
    req.sign_request(SIG_METHOD, app['consumer'], app['token'])
    header = req.to_header(app['account'])
    headery = header['Authorization'].encode('ascii', 'ignore')
    return {
        "Authorization": headery,
        "Content-Type": "application/json",
    }


def get(app_id, payload):
    method = 'GET'
    app = get_app_by_id(app_id)
    url = requests.Request(method,
                           app['url'],
                           params=payload).prepare().url

    conn = requests.get(url,
                        headers=_generate_headers(app, method, url),)
    return json.loads(conn.text)


def post(app_id, payload):
    method = 'POST'
    app = get_app_by_id(app_id)
    conn = requests.post(app['url'],
                         headers=_generate_headers(app, method, app['url']),
                         data=json.dumps(payload))
    return json.loads(conn.text)


def put(app_id, payload):
    method = 'PUT'
    app = get_app_by_id(app_id)
    conn = requests.post(app['url'],
                         headers=_generate_headers(app, method, app['url']),
                         data=json.dumps(payload))
    return json.loads(conn.text)


def delete(app_id, payload):
    method = 'DELETE'
    app = get_app_by_id(app_id)
    url = requests.Request(method,
                           app['url'],
                           params=payload).prepare().url

    conn = requests.get(url, headers=_generate_headers(app, method, url), )
    return json.loads(conn.text)


