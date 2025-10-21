from flask import Flask, request, jsonify, send_from_directory
import json
import os
import time
import random
import string

app = Flask(__name__)

# Percorso del database
DB_PATH = os.path.join(os.path.dirname(__file__), 'db_python.json')

def read_db():
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def write_db(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def uid():
    timestamp = hex(int(time.time() * 1000))[2:]
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{timestamp}{random_str}"

# Serve i file statici
@app.route('/')
def home():
    return send_from_directory(os.path.dirname(__file__), 'home.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

# API endpoints
@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(read_db())

@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    text = str(data.get('text', '')).strip()
    
    if not text:
        return jsonify({'error': 'text required'}), 400
    
    todos = read_db()
    item = {
        'id': uid(),
        'text': text,
        'done': False,
        'created': int(time.time() * 1000)
    }
    todos.insert(0, item)
    write_db(todos)
    return jsonify(item), 201

@app.route('/api/todos/<id>', methods=['PUT'])
def update_todo(id):
    todos = read_db()
    todo = next((item for item in todos if item['id'] == id), None)
    
    if not todo:
        return jsonify({'error': 'not found'}), 404
    
    data = request.get_json()
    if 'text' in data:
        todo['text'] = str(data['text'] or '')
    if 'done' in data:
        todo['done'] = bool(data['done'])
    
    write_db(todos)
    return jsonify(todo)

@app.route('/api/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    todos = read_db()
    todos = [t for t in todos if t['id'] != id]
    write_db(todos)
    return '', 204

@app.route('/api/todos', methods=['DELETE'])
def delete_all():
    write_db([])
    return '', 204

@app.route('/api/import', methods=['POST'])
def import_todos():
    data = request.get_json()
    if not isinstance(data, list):
        data = []
    
    todos = read_db()
    normalized = []
    
    for item in data:
        text = str(item.get('text', '')).strip()
        if text:
            normalized.append({
                'id': item.get('id', uid()),
                'text': text,
                'done': bool(item.get('done', False)),
                'created': item.get('created', int(time.time() * 1000))
            })
    
    merged = normalized + todos
    write_db(merged)
    return jsonify({
        'imported': len(normalized),
        'total': len(merged)
    })

if __name__ == '__main__':
    app.run(port=3001, debug=True)