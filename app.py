from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from api import get_mock, post_mock
import json

app = Flask(__name__)

auth = HTTPBasicAuth()

class Agent():

    def verify_agent_exits(self,username):
        json_list   = json.dumps(get_mock('agent'))
        json_object = json.loads(json_list)

        for element in json_object:
            if element['userName'].strip() == username.strip():
                aux = True
            else:
                aux = False
        return aux
    
    def hash_password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password_hash,password):
        return check_password_hash(password_hash, password)


@app.route('/issues', methods=['GET'])
def get_issues():
    return jsonify(get_mock('issue'))

@app.route('/issue', methods=['POST'])
def add_issue():
    response = post_mock('issue',request.json)

    if response.status_code != 201:
        return {'error':1,'menssage':'status code '+response.status_code}
    else:
        return {'error':0,'menssage':'issue registered Successfully'}

@app.route('/agent', methods=['POST'])
def add_agent():

    username    = request.json.get('username')
    password    = request.json.get('password')
    agent       = Agent()

    if username is None or password is None or username == "" or password == "":
        return {'error':2,'menssage':'you must enter your username and password'}

    if agent.verify_agent_exits(username) is True:
        return {'error':3,'menssage':'the user entered already exists enter another'}
    else:
        agent.hash_password(password)

        json_aux = {'userName':username,'password':agent.password_hash}

        response = post_mock('agent',json_aux)

        if response.status_code != 201:
            return {'error':1,'menssage':'status code '+response.status_code}
        else:
            return {'error':0,'menssage':'issue registered Successfully'}

if __name__ == '__main__':
    app.run(debug=True, port=4000)