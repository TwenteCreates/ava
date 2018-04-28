# coding=utf-8
"""
A first simple Cloud Foundry Flask app

Author: Ian Huston
License: See LICENSE.txt

"""
from flask import Flask, jsonify, request
from googletrans import Translator

import os
import requests

app = Flask(__name__)
translator = Translator()
# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))
precire_api_key = str(os.getenv("PRECIRE_API", ""))
optiopay_token = str(os.getenv("OPTIOPAY_TOKEN", ""))
optiopay_profileid = str(os.getenv("OPTIOPAY_PROFILEID", ""))
OPTIOPAY_BASE_URL = 'https://api.sandbox.optest.de/issuer/v1/'

@app.route('/')
def hello_world():
    return 'Hello World! I am instance ' + str(os.getenv('CF_INSTANCE_INDEX', 0))

#
@app.route('/translate')
def translate():
    text = request.args.get('text', "")
    assert text != ""

    dest = request.args.get('dest', "de")  #destination language

    resp = translator.translate(text, dest=dest)
    return jsonify({'value': resp.text})

#summarize the vaue for paramete
@app.route('/summary')
def precire():

    assert precire_api_key != ""

    text = request.args.get('text', "")
    assert text != ""

    headers = {
        'Ocp-Apim-Subscription-Key': precire_api_key,
        'Content-Type': 'application/json',
        'Content-Language': 'de',
    }
    body = {
        'document': {
            'text': text,
            'type': 'default',
        },
        'results': ['friendly'],
        'patterns': True,
    }
    response = requests.post('https://api.precire.ai/v0.9/',
                        json=body,
                        headers=headers)

    assert response.status_code == 200
    return jsonify(response.json())
#
@app.route('/optiopay', methods=['GET'])
def optiopay():

    assert optiopay_token != ""
    # assert optiopay_payment_profile_id != ""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' %(optiopay_token)
    }
    response = requests.get(OPTIOPAY_BASE_URL + 'payment-jobs', headers=headers)
    # import pdb; pdb.set_trace()
    assert response.status_code == 200
    return jsonify(response.json())

@app.route('/optiopay', methods=['POST'])
def optiopay_pay():

    assert optiopay_token != ""
    assert optiopay_profileid != ""
    body = {
        "paymentProfileId": optiopay_profileid,
        "amount": {
            "amount": "1.00",
            "currency": "EUR"
        },
        "dueAt": "2019-02-08T14:35:33.274740859Z",
        "language": "de",
        "contactMethod": "Export",
        "recipientDetails": {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.org",
            "address": "Test Street 123",
            "additionalAddress": "",
            "postalCode": "12345",
            "city": "TestCity",
            "country": "DE",
            "telephone": "+4912312345678"
        },
        "fallbackBankAccount": {
            "accountHolder": "John",
            "iban": "DE89370400440532013000",
            "bic": "BIWYYYYYXXX"
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' %(optiopay_token)
    }
    response = requests.post(OPTIOPAY_BASE_URL + 'payment-jobs', json=body, headers=headers)
    # import pdb; pdb.set_trace()
    print response.json()
    print response.status_code
    assert response.status_code == 201
    return jsonify(response.json())

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)

