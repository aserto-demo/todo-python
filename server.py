
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from .directory import resolve_user_by_identity, resolve_user_by_user_id
from .db import list_todos, insert_todo, update_todo, delete_todo
from flask_aserto import AsertoMiddleware, AuthorizationError
from .aserto_options import load_aserto_options_from_environment

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(app, headers=["Content-Type", "Authorization"])

aserto_options = load_aserto_options_from_environment()
aserto = AsertoMiddleware(**aserto_options)

@app.errorhandler(AuthorizationError)
def authorization_error(e):
    return "Authorization Error", 403

@app.route('/todos', methods=['GET'])
@aserto.authorize
def get_todos():
    results = list_todos()
    return jsonify(results)

@app.route('/todo', methods=['POST'])
@aserto.authorize
def post_todo():
    todo = request.get_json()
    insert_todo(todo)
    return jsonify(todo)


@app.route('/todo/<oid>', methods=['PUT'])
@aserto.authorize
def put_todo(oid):
    todo = request.get_json()
    update_todo(todo)
    return todo

@app.route('/todo/<oid>', methods=['DELETE'])
@aserto.authorize
def remove_todo(oid):
    todo = request.get_json()
    delete_todo(todo)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route('/user/<uid>', methods=['GET'])
@aserto.authorize
def get_user(uid):
    uid = resolve_user_by_identity(uid)
    user = resolve_user_by_user_id(uid)
    return jsonify(user)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host="localhost", port=3001, debug=True)