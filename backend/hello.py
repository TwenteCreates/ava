# coding=utf-8
"""
A first simple Cloud Foundry Flask app

Author: Ian Huston
License: See LICENSE.txt

"""
from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get port from environment variable or choose 9099 as local default
port = int(os.getenv("PORT", 9099))

@app.route('/')
def hello_world():
    return 'Hello World! I am instance ' + str(os.getenv("CF_INSTANCE_INDEX", 0))


@app.route('/precire')
def precire():

    import requests
    headers = {
        'Ocp-Apim-Subscription-Key': '$$$$',
        'Content-Type': 'application/json',
        'Content-Language': 'de',
    }
    body = {
            'document': {
                'text': ('Das PRECIRE Team wünscht viel Erfolg und vor allem viel Spaß beim Hack-It-Over 2018.'),
                'type': 'default',
    },
    'results': ['friendly'],
    'patterns': True,
    }
    response = requests.post('https://api.precire.ai/v0.9/',
                        json=body,
                        headers=headers)
    assert response.status_code == 200
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    # Run the app, listening on all IPs with our chosen port number
    app.run(host='0.0.0.0', port=port)

