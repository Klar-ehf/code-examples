# Openbanking example code
We offer example in dotnet and Python.



# Create claims
```PYTHON
def create_claim(company_key, section, claimant, identifier, claim_no, payor_id, due_date,
                 final_due_date, cancellation_date, other_cost, interest_rule, amount, reference):
    payload_item = {
        "Key": {
            "Claimant": claimant,
            "Account": claim_no, # <kröfubanki:4>66<Kröfunúmer>:6
            "DueDate": due_date
        },
        "PayorID": payor_id,
        "CancellationDate": cancellation_date,
        "Identifier": identifier,
        "Amount": amount,
        "Reference": reference,
        "FinalDueDate": final_due_date,
        "BillNumber": "",
        "CustomerNumber": str(payor_id),
        "NoticeAndPaymentFee": {
            "Printing": 0,
            "Paperless": 0
        },
        "OtherCosts": other_cost,
        "OtherDefaultCosts": 0,
        "DefaultInterest": {
            "Rule": interest_rule,
            "Percentage4": 0,
            "SpecialCode": ""
        },
        "PermitOutOfSequencePayment": False,
        "IsPartialPaymentAllowed": False
    }
    if self.headers is None:
        self.headers = get_api_auth_header(company_key, self.token)
    else:
        self._update_header(company_key)
    _temp_url = self.get_bank_blank_url(section)
    url = '{}/claims'.format(_temp_url)
    response = self._post_result(url, json.dumps(payload))
    return response


def get_claim_status(self, company_key, section, claim_id):
    if self.headers is None:
        self.headers = get_api_auth_header(company_key, self.token)
    else:
        self._update_header(company_key)
    _temp_url = self.get_bank_blank_url(section)
    url = '{}/claims/{}'.format(_temp_url, claim_id)
    response = self._get_result(url)
    return response


company_key = '293c1838-6541-498c-8288-6b886477293e'
section = 'arionbanki' # islandsbanki, arionbanki, landsbankinn
claimant = '5205161230'
identifier = '001'
bank = '0301'
next_claim_id = '{}'.format(1).zfill(6)
claim_no = '{}66{}'.format(bank, next_claim_id)
payor_id = '0208779999'
due_date = '2023-10-30'
final_due_date = '2023-11-10'
cancellation_date = '2025-10-30'
other_cost = 0
interest_rule = 'DefaultInterestAmount'
amount= 100
reference="0208779999"
claim_create_response = create_claim(company_key, section, claimant, identifier, claim_no, payor_id, due_date,
                 final_due_date, cancellation_date, other_cost, interest_rule, amount, reference)
claim_create_status_id = claim_create_response['data']
claim_status_response = claim_status(company_key, section, claim_create_status_id)
print(claim_status_response)


```
