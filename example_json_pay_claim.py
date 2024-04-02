payload = {
    "In": {
        "Amount": amount,
        "Description": "Greiðsla",
        "BookingId": claim_account[:6],
        "PaymentClaim": {
            "Account": claim_account,
            "Claimant": claim_claimant,
            "PayorId": claim_claimant,
            "DueDate": claim_due_date,
            "IsDeposit": False
        },
    },
    "Out": {
        "Account": str(from_account).replace('-', ''),
        "AccountOwnerId": registration_id,
        "CategoryCode": "03",
        "Reference": registration_id,
        "BillNumber": claim_account[:6],
    },
    "DateOfForwardPaymentSpecified": False
}
