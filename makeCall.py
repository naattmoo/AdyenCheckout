import requests

def makeCall(uri, body, apiKey):
    url = 'https://checkout-test.adyen.com/v67/'+uri
    headers = {
        'x-API-key': apiKey,
        'content-type': 'application/json'}
    print("/request:\n" + body)
    response = requests.post(url, headers=headers, data=body)
    print("/response:\n" + response.text)
    return response