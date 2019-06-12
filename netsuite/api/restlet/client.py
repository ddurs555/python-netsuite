from netsuite.api.common.utils import get_next_restlet_app
import oauth2 as oauth
import requests
import time
import json
import ns_config



SIG_METHOD = oauth.SignatureMethod_HMAC_SHA1()


def _get_params(token, consumer):
    return {
        'oauth_version': "1.0",
        'oauth_nonce': oauth.generate_nonce(),
        'oauth_timestamp': str(int(time.time())),
        'oauth_token': token.key,
        'oauth_consumer_key': consumer.key,
    }


def _get_oauth_request(app,method, url):
    return oauth.Request(
        method=method,
        url=url,
        parameters=_get_params(token=app.token, consumer=app.consumer)
    )


def _generate_headers(app, method, url):
    req = _get_oauth_request(app=app, method=method, url=url)
    req.sign_request(SIG_METHOD, app.consumer, app.token)
    header = req.to_header(app.account)
    headery = header['Authorization'].encode('ascii', 'ignore')
    return {
        "Authorization": headery,
        "Content-Type": "application/json",
    }


def get(payload):
    method = 'GET'
    app = get_next_restlet_app()
    url = requests.Request(method,
                           app.url,
                           params=payload).prepare().url

    conn = requests.get(url,
                        headers=_generate_headers(app, method, url),)
    return json.loads(conn.text)


def post(payload):
    method = 'POST'
    app = get_next_restlet_app()
    conn = requests.post(app.url,
                         headers=_generate_headers(app, method, app.url),
                         data=json.dumps(payload))
    return json.loads(conn.text)


def put(payload):
    method = 'PUT'
    app = get_next_restlet_app()
    conn = requests.post(app.url,
                         headers=_generate_headers(app, method, app.url),
                         data=json.dumps(payload))
    return json.loads(conn.text)


def delete(payload):
    method = 'DELETE'
    app = get_next_restlet_app()
    url = requests.Request(method,
                           app.url,
                           params=payload).prepare().url

    conn = requests.get(url, headers=_generate_headers(app, method, url), )
    return json.loads(conn.text)


def main():
    payload = {
        'custrecord_cc_image':'https://mrosupply2-dyn-images.s3.amazonaws.com/category_image/872_na6KdbH_Eahra48.jpg',
        'name':'davids API test',
        'custrecord_cc_description':'Take me down to the paradise city where the grass is green',
        'custrecord_cc_short_description':'ooooh wont you please take me home',
    }
    get(payload={'id':'38'})
    post(payload=payload)
    put(payload=payload)
    delete(payload=payload)

if __name__ == "__main__":
    main()