import threading
from time import sleep
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG)


class AuthenticationDaemon(threading.Thread):
    logger = logging.getLogger('auth_daemon')
    AUTH_URL = 'https://myaussie-auth.aussiebroadband.com.au/'
    token = None
    expiration = None  # TODO: Implement expiration monitor for token refresh
    cookie = None

    username = ''
    password = ''

    def __init__(self, *args, **kwargs):
        self.logger.debug('Initializing')
        super().__init__(args=args, kwargs=kwargs)

    def login(self):
        self.logger.debug('Logging user in')
        auth = requests.post(self.AUTH_URL + 'login', json={'username': self.username, 'password': self.password})

        response_data = json.loads(auth.content)

        if auth.status_code != 200:
            self.logger.critical('Auth failed')
            raise Exception('Failed to auth user')

        self.token = response_data['refreshToken']
        self.expiration = response_data['expiresIn']
        self.cookie = auth.headers['Set-Cookie'].split(';')[0]


class Client:
    logger = logging.getLogger('client')
    API_URL = 'https://myaussie-api.aussiebroadband.com.au/'

    customer = None
    header = None

    def __init__(self):
        self.logger.debug('Initializing')
        self.authentication = AuthenticationDaemon(daemon=True)
        self.authentication.login()
        while not self.authentication.token:
            pass
        self.logger.debug('Authed user and initialized Client')
        self.header = {'Cookie': self.authentication.cookie}

    def get_customer(self):
        response = requests.get(self.API_URL + 'customer', headers=self.header)
        self.logger.info('Refreshed Customer info')
        self.customer = json.loads(response.content)


client = Client()
client.get_customer()
print(client.customer['services'])
sleep(5)
