# coding=utf-8
"""
A first simple Cloud Foundry Flask app

Author: Ian Huston
License: See LICENSE.txt

"""
from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))
precire_api_key = str(os.getenv("PRECIRE_API", ""))

@app.route('/')
def hello_world():
    return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0))

#summarize the vaue for paramete
@app.route('/summary')
def precire():

    assert precire_api_key != ""

    text = request.args.get('text', "")
    assert text != ""

    import requests

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

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)

