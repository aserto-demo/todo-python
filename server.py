
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from .directory import resolve_user_by_identity, resolve_user_by_user_id
from .db import list_todos, insert_todo, update_todo, delete_todo

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

CORS(app, headers=["Content-Type", "Authorization"])

@app.route('/todos', methods=['GET'])
def get_todos():
    results = list_todos()
    return jsonify(results)

@app.route('/todo', methods=['POST'])
def post_todo():
    todo = request.get_json()
    insert_todo(todo)
    return jsonify(todo)


@app.route('/todo/<oid>', methods=['PUT'])
def put_todo(oid):
    todo = request.get_json()
    update_todo(todo)
    return todo

@app.route('/todo/<oid>', methods=['DELETE'])
def remove_todo(oid):
    todo = request.get_json()
    delete_todo(todo)
    resp = jsonify(success=True)
    resp.status_code = 200
    return resp

@app.route('/user/<uid>', methods=['GET'])
def get_user(uid):
    uid = resolve_user_by_identity(uid)
    user = resolve_user_by_user_id(uid)
    return jsonify(user)

if __name__ == '__main__':
    app.run(host="localhost", port=3001, debug=True)