from uuid import uuid4

import requests


class BaseOpenbankingApi(object):

    def __init__(self, username, password, client_id, client_secret):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

    def get_token(self):
        auth_url = 'https://openbanking-iceland.eu.auth0.com/oauth/token'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': 'password',
            'username': '<Your username>',
            'password': '<Your password>',
            'audience': 'https://openbankingapi.module',
            'scope': 'email',
            'client_id': '<Your client id>',
            'client_secret': '<Your client secret>'
        }
        r = requests.post(url=auth_url, data=payload, headers=headers, verify=True)
        return r.json()['access_token']

    def get_header(self, company_key, token=None):
        if token is None:
            token = self.get_token()
        data_header = {
            'content-type': 'application/json',
            'company-key': str(company_key),
            'companyId': str(company_key),
            'authorization': 'Bearer ' + token,
            'appId': '<your app id>'
        }
        return data_header

    def _correlation(self, headers):
        self.x_request_id = uuid4()
        headers.update({'X-Request-ID': str(self.x_request_id)})

    def _get_result(self, headers, url):
        success = False
        json_data = None
        error = None
        try:
            self._correlation(headers)

            r = requests.get(url, headers=headers, verify="localhost" not in url)
            r.raise_for_status()
            json_data = r.json()
            success = True
        except requests.exceptions.HTTPError as errh:
            error = "Http Error: {}".format(errh)
        except requests.exceptions.ConnectionError as errc:
            error = "Error Connecting: {}".format(errc)
        except requests.exceptions.Timeout as errt:
            error = "Http Error: {}".format(errt)
        except requests.exceptions.RequestException as err:
            error = "Error: {}".format(err)
        return {
            "success": success,
            "data": json_data,
            "error": error
        }

    def _put_result(self, headers, url, payload):
        success = False
        json_data = None
        error = None
        try:
            self._correlation()

            r = requests.put(url, data=payload, headers=headers, verify="localhost" not in url)
            r.raise_for_status()
            json_data = r.json()
            success = True
        except requests.exceptions.HTTPError as errh:
            error = "Http Error: {}".format(errh)
        except requests.exceptions.ConnectionError as errc:
            error = "Error Connecting: {}".format(errc)
        except requests.exceptions.Timeout as errt:
            error = "Http Error: {}".format(errt)
        except requests.exceptions.RequestException as err:
            error = "Error: {}".format(err)
        return {
            "success": success,
            "data": json_data,
            "error": error
        }

    def _post_result(self, headers, url, payload):
        success = False
        json_data = None
        error = None
        try:
            self._correlation()

            r = requests.post(url, data=payload, headers=headers, verify="localhost" not in url)
            r.raise_for_status()
            json_data = r.json()
            success = True
        except requests.exceptions.HTTPError as errh:
            error = "Http Error: {}".format(errh)
        except requests.exceptions.ConnectionError as errc:
            error = "Error Connecting: {}".format(errc)
        except requests.exceptions.Timeout as errt:
            error = "Http Error: {}".format(errt)
        except requests.exceptions.RequestException as err:
            error = "Error: {}".format(err)
        return {
            "success": success,
            "data": json_data,
            "error": error
        }

    def _del_result(self, headers, url):
        success = False
        json_data = None
        error = None
        try:
            self._correlation()

            r = requests.delete(url, headers=headers, verify="localhost" not in url)
            r.raise_for_status()
            json_data = r.json()
            success = True
        except requests.exceptions.HTTPError as errh:
            error = "Http Error: {}".format(errh)
        except requests.exceptions.ConnectionError as errc:
            error = "Error Connecting: {}".format(errc)
        except requests.exceptions.Timeout as errt:
            error = "Http Error: {}".format(errt)
        except requests.exceptions.RequestException as err:
            error = "Error: {}".format(err)
        return {
            "success": success,
            "data": json_data,
            "error": error
        }


class OpenbankingApi(BaseOpenbankingApi):

    def __init__(self):
        username = '<your openbanking user>'
        password = '<your openbanking password>'
        client_id = '<your openbanking client id>'
        client_secret = '<your openbanking client secret>'
        self.blank_url = 'https://{}.openbankingapi.is/DataPlato/Banks/1.0'
        super().__init__(username, password, client_id, client_secret)

    def get_currencies(self, company_key, provider):
        headers = self.get_header(company_key)        
        base_url = self.blank_url.format(provider)
        url = '{}/currencies/2022-11-03'.format(base_url)
        return self._get_result(headers, url)


if __name__ == "__main__":

    company_key = 'f745366f-2cab-4ca4-8c67-40dd1dee209f'
    provider = 'arionbanki'

    print('\n------------------------------------------------------------------------------------------')
    openbanking_api = OpenbankingApi()
    currencies = openbanking_api.get_currencies(company_key, provider)
    
    for currency in currencies['data']:
        print(currency)
    
