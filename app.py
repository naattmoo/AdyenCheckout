import json
import os
from flask import Flask, render_template, request, abort, send_from_directory, redirect, url_for
from flask_caching import Cache
import config as config
from makeCall import makeCall
import uuid
from config import read_config
from payByLink import adyen_pay_by_link

app = Flask(__name__)
cache = Cache(app)

authonly = False


def page_not_found(error):
    return render_template('error.html'), 404


# Register 404 handler
app.register_error_handler(404, page_not_found)

# read in values from config.ini file and load them into project
read_config()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/cart/<integration>')
def cart(integration):
    return render_template('cart.html', method=integration)


@app.route('/checkout/<integration>')
def checkout(integration):
    if integration in config.supported_integrations:

        body = {
            "merchantAccount": config.merchant_account,
            "amount": {
                "currency": "EUR",
                "value": 5808
            },
            "shopperReference": "prueba"
            #"splitCardFundingSources": "true"
            #"shopperReference": "shopperNoExistente"
        }
        # "shopperReference": "xee6f62b4-9a22-4860-b6c9-e69de062ba61"
        resp = makeCall('paymentMethods', json.dumps(body), config.checkout_apikey)
        return render_template('component.html', method=integration, client_key=config.client_key, payments=resp.text)
    elif integration == 'paymentLink':
        payUrl = adyen_pay_by_link(config.merchant_account, config.checkout_apikey)
        return redirect(payUrl, code=302)
    else:
        abort(404)


# @cache.cached(timeout=300)
@app.route('/makePayment', methods=['GET', 'POST'])
def makePayment():
    data = request.json

    if ('storedPaymentMethodId' in data['paymentMethod']):
        data['shopperInteraction'] = 'ContAuth'
        data['recurringProcessingModel'] = 'CardOnFile'
        data['shopperReference'] = "xee6f62b4-9a22-4860-b6c9-e69de062ba61"
        #if(data['paymentMethod']['brand']=='maestro'):
        #    data['shopperInteraction'] = 'Ecommerce'
    if ('storePaymentMethod' in data) and (data['storePaymentMethod'] == True):
        data['shopperInteraction'] = 'Ecommerce'
        data['recurringProcessingModel'] = 'CardOnFile'
        data['shopperReference'] = "xee6f62b4-9a22-4860-b6c9-e69de062ba61"

    if (authonly):
        data['threeDSAuthenticationOnly'] = 'true'

    reference = str(uuid.uuid4())
    returnUrl = data['origin'] + '/handleShopperRedirect?orderRef=' + reference

    body_string = """{
                "enablePayOut" : false,
               "merchantAccount": \"""" + config.merchant_account + """\",
               "amount": {
                       "currency": "EUR",
                   "value": 6000
               },""" + json.dumps(data).replace('\'', '\"')[1: -1] + """,
              "reference": \"""" + reference + """\",
              "shopperLocale": "es_ES",
              "countryCode": "ES",
              "shopperIP":"192.0.2.1",
              "channel":"web",
              "telephoneNumber": "+346763507s90",
              "additionalData": {
                      "allow3DS2": true
              },
               "shopperEmail":"youremail@email.com",
               "shopperName":{
                  "firstName":"Testperson-es",
                  "gender":"UNKNOWN",
                  "lastName":"Approved"
               },
               "shopperStatement":"prueba de Shopper Statement",
               "shopperReference": "prueba",
               "billingAddress": {
                      "country": "ES",
                      "city": "Madrid",
                      "street": "Atocha",
                      "houseNumberOrName": "1",
                      "stateOrProvince": "N/A",
                      "postalCode": "28002"
               },
               "lineItems":[
                  {
                     "quantity":"1",
                     "amountExcludingTax":"5000",
                     "taxPercentage":"0",
                     "description":"Test item 1",
                     "id":"item1",
                     "taxAmount":"0",
                     "amountIncludingTax":"5000"
                  },
                  {
                     "quantity":"1",
                     "amountExcludingTax":"10000",
                     "taxPercentage":"0",
                     "description":"Test item 2",
                     "id":"item2",
                     "taxAmount":"0",
                     "amountIncludingTax":"10000"
                  }
               ],
               "returnUrl": \"""" + returnUrl + """\"    
            }"""

    # "threeDSAuthenticationOnly":true, //Flujo autenticacion y autorizacion por separado.
    # "additionalData": {
    #    "allow3DS2": true
    # },
    # "shopperReference": "xee6f62b4-9a22-4860-b6c9-e69de062ba61",
    #"customRoutingFlag": "mcDebit"
    #"riskData":{
    #"riskProfileReference":"8016358411114661"
    #},

    body = json.loads(body_string)

    resp = makeCall('payments', json.dumps(body), config.checkout_apikey)

    '''if('action' in resp.json()):
        if(resp.json()['action']['type']== "redirect"):
            global paymentData
            paymentData=resp.json()['action']['paymentData']'''
    print(resp)
    return resp.text


@app.route('/makeDetailsCall', methods=['GET', 'POST'])
def makeDetailsCall():
    print(request.json)

    data = request.json
    if (authonly):
        data['threeDSAuthenticationOnly'] = 'true'  # solo para flujo Auth Only

    resp = makeCall('payments/details', json.dumps(data), config.checkout_apikey)
    if resp.json()["resultCode"] == 'AuthenticationFinished':
        reference = str(uuid.uuid4())
        body = {
            "amount": {
                "currency": "EUR",
                "value": 50000
            },
            "reference": reference,
            "paymentMethod": {
                "type": "scheme",
                "encryptedCardNumber": "test_5201285093823592",
                "encryptedExpiryMonth": "test_03",
                "encryptedExpiryYear": "test_2030",
                "encryptedSecurityCode": "test_737"
            },
            "mpiData": {
                "cavv": resp.json()['threeDS2Result']["threeDSServerTransID"],
                "eci": resp.json()['threeDS2Result']["eci"],
                "dsTransID": resp.json()['threeDS2Result']["threeDSServerTransID"],
                "authenticationResponse": resp.json()['threeDS2Result']['transStatus'],
                "threeDSVersion": resp.json()['threeDS2Result']["messageVersion"]
            },
            "channel": "web",
            "merchantAccount": "MerchantTestNatalia"
        }
        resp_authorise = makeCall('payments', json.dumps(body), config.checkout_apikey)
        print(resp_authorise.json()["resultCode"])
        resp = resp_authorise

    return resp.text


@app.route('/handleShopperRedirect', methods=['GET', 'POST'])
def handleShopperRedirect():
    details = {}
    if request.method == "GET":
        redirectResult = ''
        if ('redirectResult' in request.args.keys()):
            redirectResult = request.args.get('redirectResult')
        details = {"redirectResult": redirectResult}

    if request.method == "POST":
        md = request.form['MD']
        pares = request.form['PaRes']
        details = {"MD": md,
                   "PaRes": pares}

    '''global paymentData
    print(paymentData)
    body={ "details" : details, "paymentData": paymentData }'''
    body = {"details": details}
    resp = makeCall('payments/details', json.dumps(body), config.checkout_apikey)
    print(resp)

    if resp.json()["resultCode"] == 'Authorised':
        return redirect(url_for('checkout_success'))
    elif resp.json()["resultCode"] == 'Received' or resp.json()["resultCode"] == 'Pending':
        return redirect(url_for('checkout_pending'))
    else:
        return redirect(url_for('checkout_failure'))

@app.route('/process_payment', methods=['GET', 'POST'])
def process_payment():
    print(request.args.keys())
    if request.method == "GET":
        if ('amazonCheckoutSessionId' in request.args.keys()):
            amazonSessionId = request.args.get('amazonCheckoutSessionId')
        print(amazonSessionId)
        body = {
            "merchantAccount": config.merchant_account,
            "amount": {
                "currency": "EUR",
                "value": 5808
            },
            "shopperReference": "prueba"
            # "splitCardFundingSources": "true"
            # "shopperReference": "shopperNoExistente"
        }
        # "shopperReference": "xee6f62b4-9a22-4860-b6c9-e69de062ba61"
        resp = makeCall('paymentMethods', json.dumps(body), config.checkout_apikey)
        return render_template('amazon.html', amazonSessionId=amazonSessionId, client_key=config.client_key, payments=resp.text)
    else:
        return redirect(url_for('checkout_failure'))

@app.route('/result/success', methods=['GET'])
def checkout_success():
    return render_template('checkout-success.html')


@app.route('/result/failed', methods=['GET'])
def checkout_failure():
    return render_template('checkout-failed.html')


@app.route('/result/pending', methods=['GET'])
def checkout_pending():
    return render_template('checkout-success.html')


@app.route('/result/error', methods=['GET'])
def checkout_error():
    return render_template('checkout-failed.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


if __name__ == '__main__':
    #ssl_context='adhoc',
    app.run(debug=True, host='0.0.0.0',port=8000)
