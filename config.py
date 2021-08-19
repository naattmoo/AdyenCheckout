import configparser

'''
Read in variables from config.ini file. Store them as global variables

Make sure to fill out your config.ini file!!!
'''

MERCHANT_ACCOUNT = ""
MERCHANT_ACCOUNT2 = ""
API_KEY = ""
API_KEY2 = ""
CLIENT_KEY = ""
CLIENT_KEY2 = ""
supported_integrations = ['dropin', 'card', 'ideal', 'klarna', 'directEbanking', 'alipay', 'boletobancario',
                          'sepadirectdebit', 'dotpay', 'giropay', 'ach', 'paypal', 'applepay']


def read_config():
    global merchant_account, merchant_account2, checkout_apikey, client_key, checkout_apikey2, client_key2

    config = configparser.ConfigParser(interpolation=None)
    config.read('config.ini')

    merchant_account = config['DEFAULT']['MERCHANT_ACCOUNT']
    merchant_account2 = config['DEFAULT']['MERCHANT_ACCOUNT2']
    checkout_apikey = config['DEFAULT']['API_KEY']
    checkout_apikey2 = config['DEFAULT']['API_KEY2']
    client_key = config['DEFAULT']['CLIENT_KEY']
    client_key2 = config['DEFAULT']['CLIENT_KEY2']

    # Check to make sure variables are set
    if not merchant_account or not checkout_apikey or not client_key or not checkout_apikey2:
        raise Exception("Please fill out information in config.ini file")