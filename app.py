import json
from flask import Flask, render_template, request
from flask_caching import Cache
import config
import pycountry
import ccy
from makeCall import makeCall

app = Flask(__name__)
cache = Cache(app)

paymentData=''
currency='EUR'


@app.route('/',methods=['GET','POST'])
def uplaodCheckout():

    global currency
    countrycode='NL'


    if('country' in request.args.keys()):
        countrycode=pycountry.countries.search_fuzzy(request.args.get('country'))[0].alpha_2
        currency=ccy.countryccy(countrycode)

    body = {
        "merchantAccount": config.MERCHANT_ACCOUNT,
        "countryCode": countrycode,
        "allowedPaymentMethods": ["visa", "mc", "ideal"],
        "amount": {
            "currency": currency,
            "value": 1000
        },
        "channel": "Web"
    }
    resp = makeCall('paymentMethods', json.dumps(body))
    print(resp.json())
    return render_template("app.html", payments=resp.text, clientKey=config.CLIENT_KEY)

@cache.cached(timeout=300)
@app.route('/makePayment', methods=['GET','POST'])
def makePayment():
        data = request.json
        print(data)

        infoBody='"paymentMethod": ' + json.dumps(data['paymentMethod']) + ','
        if('browserInfo' in data):
            infoBody+='"browserInfo":'+ json.dumps(data['browserInfo']) +','
        if ('billingAddress' in data):
         infoBody += '"billingAddress":' + json.dumps(data['billingAddress']) + ','

        returnUrl= data['origin']+'/checkout?shopperOrder=12xy..'

        body_string = """{
                   "merchantAccount": \""""+config.MERCHANT_ACCOUNT+"""\",
                   "amount": {
                       "currency": \""""+currency+"""\",
                       "value": 1000
                   },"""+infoBody+"""
                  "additionalData":{
                     "allow3DS2":true
                  },
                  "shopperEmail":"s.hopper@example.com",
                  "shopperIP":"192.0.2.1",
                  "channel":"web",
                  "origin":"""+json.dumps(data['origin'])+""",
                  "reference": \""""+config.REFERENCE+"""\",
                  "returnUrl": \""""+returnUrl+"""\"
               }"""
        
        print(body_string)
        body = json.loads(body_string)
        
        resp = makeCall('payments', json.dumps(body))


        if('action' in resp.json()):
            if(resp.json()['action']['type']== "redirect"):
                global paymentData
                paymentData=resp.json()['action']['paymentData']

        return resp.text

@app.route('/makeDetailsCall', methods=['GET','POST'])
def makeDetailsCall():

        data = request.json
        resp = makeCall('payments/details', json.dumps(data))
        print(resp.text)
        return resp.text

@app.route('/checkout', methods=['GET'])
def checkout():
    if request.method == "GET":
        data = request.args.get('redirectResult')
        print(data)
        global paymentData
        print(paymentData)
        body={ "details" : { "redirectResult": data },  "paymentData": paymentData }
        resp = makeCall('payments/details', json.dumps(body))
        print(resp.text)
        return render_template("result.html", result=resp.json()['resultCode'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
