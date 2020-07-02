from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from api import get_mock, post_mock
import json

app = Flask(__name__)

auth = HTTPBasicAuth()

@app.route('/issues', methods=['GET'])
def get_issues():
    return jsonify(get_mock('issue'))

@app.route('/issue', methods=['POST'])
def add_issue():
    post_mock('issue',request.json)
    return 'received'

@app.route('/agent', methods=['POST'])
def add_agent():

    username    = request.json.get('username')
    password    = request.json.get('password')
    exist       = 1

    if username is None or password is None:
        return {'error':2,'menssage':'you must enter your username and password'}
    
    json_list   = json.dumps(get_mock('agent'))
    json_object = json.loads(json_list)

    for element in json_object: 
        if element['userName'] == username:
            exist = 1

    if exist > 0:
        return {'error':3,'menssage':'the user entered already exists enter another'}

    #if(len(agentFound) > 0):
     #   print(agentFound)
      #  return 'received'
    #else:
     #   return 'no found'

    #post_mock('agent',request.json)

if __name__ == '__main__':
    app.run(debug=True, port=4000)