import json
from _ast import operator
from uuid import uuid4

import requests


class BaseKlarApi(object):

    def __init__(self, username, password, client_id, client_secret, app_id):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
        self.app_id = app_id

    def _get_header(self, company_id, token=None):
        if token is None:
            token = self._get_token()
        data_header = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + token,
            'X-App-Id': self.app_id,
            'X-App-Email': self.username,
            'X-Company-Id': str(company_id),
            'X-Real-User': self.username
        }
        return data_header

    def _get_token(self, verify=True):
        auth_url = 'https://openbanking-iceland.eu.auth0.com/oauth/token'
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'audience': 'https://openbankingapi.module',
            'scope': 'email',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        r = requests.post(url=auth_url, data=payload, headers=headers, verify=verify)
        return r.json()['access_token']

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
            self._correlation(headers)

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
            self._correlation(headers)

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


class KlarApi(BaseKlarApi):

    def __init__(self):
        username = '<your username>'
        password = '<your password>'
        client_id = '<your client id>'
        client_secret = '<your client secret>'
        app_id = '<your developer app id>'
        self.blank_url = 'https://{}.openbankingapi.is/DataPlato/Banks/1.0'
        super().__init__(username, password, client_id, client_secret)

    def get_currencies(self, company_id, provider):
        headers = self._get_header(company_id)
        base_url = self.blank_url.format(provider)
        url = f"{base_url}/currencies/2024-08-08"
        return self._get_result(headers, url)

    def get_accounts(self, company_id, provider):
        headers = self._get_header(company_id)
        base_url = self.blank_url.format(provider)
        url = f"{base_url}/accounts"
        return self._get_result(headers, url)

    def get_statement(self, company_id, provider, account):
        headers = self._get_header(company_id)
        base_url = self.blank_url.format(provider)
        url = f"{base_url}/statements"
        payload = {
          "Account": account,
          "DateFrom": "2024-01-01",
          "DateTo": "2024-08-09",
          "RecordFrom": 0,
          "RecordFromSpecified": False,
          "RecordTo": 0,
          "RecordToSpecified": False
        }

        return self._post_result(headers, url, json.dumps(payload))


if __name__ == "__main__":

    _company_key = '<your company id>'
    _provider = 'arionbanki'
    # _provider = 'islandsbanki'
    # _provider = 'landsbankinn'

    print('\n------------------------------------------------------------------------------------------')
    klar_api = KlarApi()
    currencies_response = klar_api.get_currencies(_company_key, _provider)

    # Fetch currencies
    for currency in currencies_response['data']:
        print(currency)
        
    # Fetch accounts
    accounts_response = klar_api.get_accounts(_company_key, _provider)
    for account in accounts_response['data']:        
        print(_account)
        _account_no = f"{account['Bank']}{account['Ledger']}{account['AccountNumber']}"
        # Fetch account statement
        statement_response = klar_api.get_statement(_company_key, _provider, _account_no)
        for statement in statement_response['data']['Transactions']:
            print(statement)

