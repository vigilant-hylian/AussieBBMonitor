import threading
from time import sleep
import requests

class AuthenticationDaemon(threading.Thread):
    AUTH_URL = 'https://myaussie-auth.aussiebroadband.com.au/'

    username = 'username'
    password = 'password'

    def login(self):
        auth = requests.post(self.AUTH_URL + 'login', json={'username': self.username, 'password': self.password})
        print(auth.content)

class Client:
    API_URL = 'https://myaussie-api.aussiebroadband.com.au/'
    def __init__(self):
        self.authentication = AuthenticationDaemon(daemon=True)
        self.authentication.login()

client = Client()
sleep(5)