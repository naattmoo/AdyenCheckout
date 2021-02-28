import requests
import config

def makeCall(uri, body):
    url = 'https://checkout-test.adyen.com/v66/'+uri
    headers = {
        'x-API-key': config.API_KEY,
        'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=body)
    return response