import requests
import json

def _url(path):
    return 'https://5ef62e652c0f2c0016949867.mockapi.io/' + path

def get_mock(path):
    reply = requests.get(_url(path))
    if reply.status_code != 200:
        return {'error':1,'menssage':'status code '+str(reply.status_code)}
    else:
        return {'error':0,'json':reply.json()}

def post_mock(path,json):
    return requests.post(_url(path),json)

def authorized_agent(user,password):
    return 0