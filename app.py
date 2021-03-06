import os,time,jwt,json,datetime
from flask import Flask, jsonify, request, abort, g, url_for, session
from api import get_mock, post_mock
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

auth = HTTPBasicAuth()

def agent_object():
    response = get_mock('agent')

    if response["error"] > 0:
        print(response)
        return False
    else:
        list_json   = json.dumps(response["json"])
        list_object = json.loads(list_json)

        return list_object

class Agent():

    def get_agent(self,username):

        json_object = agent_object()

        if not json_object:
            return False
        else:

            for element in json_object:
                if element['userName'].strip() == username.strip():

                    self.id_aux         = element['id']
                    self.username_aux   = element['userName']
                    self.password_hash  = element['password']
                    session.pop('username', None)
                    session['username'] = self.username_aux

                    return True

            return False

    def verify_agent_exits(self,username):
        
        json_object = agent_object()

        if not json_object:
            return False
        else:

            for element in json_object:
                if element['userName'].strip() == username.strip():
                    return True
        
            return False
    
    def hash_password(self,password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self,password):

        validate = check_password_hash(self.password_hash, password)

        if validate is True:
            return True
        else:
            session.pop('username', None)
            return False

    def generate_issue(self,title,description):

        now         = datetime.datetime.now() 
        date_time   = now.strftime('%m-%d-%Y %H:%M:%S')

        json_aux    = { 'date': date_time,
                        'title': title,
                        'description': description,
                        'agent': session['username']}
        
        return json_aux
    
    def generate_auth_token(self, expires_in=600):
        return jwt.encode({'exp': time.time() + expires_in},app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])
            print(data)
            return True
        except:
            return False

@auth.verify_password
def verify_password(username_or_token, password):
    agent    = Agent()
    response = agent.verify_auth_token(username_or_token)

    if response is True:
        return True
    else:
        response_aux = agent.get_agent(username_or_token)
        if response_aux is True:

            if not agent or not agent.validate_password(password):
                return False
            return True
        else:
            return False

@app.route('/token')
@auth.login_required
def get_auth_token():
    agent = Agent()
    token = agent.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/issues', methods=['GET'])
def get_issues():
    return jsonify(get_mock('issue'))

@app.route('/issues/<string:orden_filter>')
def get_issue_s(orden_filter):

    url_aux = 'issue?'+orden_filter
    print(url_aux)
    return get_mock(url_aux)

@app.route('/issue', methods=['POST'])
@auth.login_required
def add_issue():

    agent       = Agent()
    title       = request.json.get('title')
    description = request.json.get('description')
    
    json     = agent.generate_issue(title,description)
    response = post_mock('issue',json)

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
            return {'error':0,'menssage':'agent registered Successfully'}

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=4000)