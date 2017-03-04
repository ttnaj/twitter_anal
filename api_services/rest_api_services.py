import base64
import json
import warnings
import oauth2

import requests

try:

    from settings.settings import TWITTER_KEY, TWITTER_SECRET, CONNECTION_URL

except ImportError:
    warnings.warn('Twitter Api username and key are missing !')

__author__ = 'taha'

RESPONSE_OK = 200


class AuthenticationFailed(Exception):
    def __init___(self):
        Exception.__init__(self,"Authentication with twitter Failed ! Check the API Key.")


class GetQueryFailed(Exception):
    def __init___(self):
        Exception.__init__(self,"Get Query with params failed !")


class PostQueryFailed(Exception):
    def __init___(self):
        Exception.__init__(self,"Post Query with params failed !")


class DeleteQueryFailed(Exception):
    def __init___(self):
        Exception.__init__(self,"Delete Query with params failed !")


class NotEnoughParamsForApiQuery(Exception):
    def __init___(self):
        Exception.__init__(self,"Method get deals or update deals needs more params !")

class ApiServices:

    def __init__(self):
        self.oAuth_key = None
        self.connection_url = CONNECTION_URL
        self.base_url = 'base url here'
        self.remove_base_url = ''
        self.post_base_url = ''

        try:
            self.oAuth_key = self.handle_connection()
        except:
            raise
        self.headers = {'Authorization': 'Bearer '+ self.oAuth_key}


    def handle_connection(self):
        try:
            consumer = oauth2.Consumer(key=TWITTER_KEY, secret=TWITTER_SECRET)
            token = oauth2.Token(key=TWITTER_KEY, secret=TWITTER_SECRET)
            client = oauth2.Client(consumer, token)

            # params = {'username': TWITTER_USERNAME, 'key': TWITTER_API_KEY}
            # connection_headers = {'Content-Type':'application/json; charset=utf-8'}
            # r = requests.post(self.connection_url, data=json.dumps(params), headers=connection_headers)
            # result = json.loads(r.text)

            resp, content = client.request(CONNECTION_URL, method="GET", body=bytes("", "utf-8"),
                                           headers=None)

            # if result["responseCode"] != RESPONSE_OK:
            #     raise AuthenticationFailed
            # else:
            #     return result['data']['accessToken']

            params = {'grant_type': 'client_credentials'}
            to_encode = str(TWITTER_KEY)+':'+str(TWITTER_SECRET)
            basic_auth_token = base64.b64encode(to_encode)
            connection_headers = {'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8', 'Authorization':'Basic %s' % str(basic_auth_token)}
            r = requests.post(self.connection_url, data=json.dumps(params), headers=connection_headers)
            result = json.loads(r.text)
            print result
            if result["responseCode"] != RESPONSE_OK:
                raise AuthenticationFailed

        except:
            raise AuthenticationFailed

    def get_base(self):
        url = self.base_url+'get suffixe'

        r = requests.get(url, headers=self.headers)
        result = json.loads(r.text)

        if result["responseCode"] != RESPONSE_OK:
            raise GetQueryFailed
        else:
            return result

    def post_base(self, param_dict):

        headers = self.headers
        headers['Content-Type'] = 'application/json; charset=utf-8'
        r = requests.put(self.post_base_url, data=json.dumps(param_dict), headers=headers)
        result = json.loads(r.text)


    def remove_base(self, params_dict):

        headers = self.headers
        headers['Content-Type'] = 'application/json; charset=utf-8'
        r = requests.delete(self.remove_base_url, data=json.dumps(params_dict), headers=headers)
        result = json.loads(r.text)
        if result["responseCode"] != RESPONSE_OK:
            raise DeleteQueryFailed