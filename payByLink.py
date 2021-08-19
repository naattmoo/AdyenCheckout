import uuid
import json
import requests

def adyen_pay_by_link(merchant, apiKey):

	order_ref = str(uuid.uuid4())

	paybylink_request = {
		'amount': {
			'value': 1000,
			'currency': 'EUR'
		},
		'reference': order_ref,
		'countryCode': 'PT',
		'merchantAccount': merchant
	}
	print("/payByLink request:\n" + str(paybylink_request))
	url = 'https://checkout-test.adyen.com/v67/paymentLinks'
	headers = {'x-API-key': apiKey,'content-type': 'application/json'}
	response = requests.post(url, headers=headers, data=json.dumps(paybylink_request))
	print(response)
	formatted_response = json.dumps((json.loads(response.content)))
	print("/payments response:\n" + response.json()['url'])
	return response.json()['url']
