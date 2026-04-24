from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

# Mock Data
DATA_DIR = 'data'
FLASHCARDS_FILE = os.path.join(DATA_DIR, 'flashcards.json')
MISTAKES_FILE = os.path.join(DATA_DIR, 'mistakes.json')

def load_json(filepath, default=[]):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def dashboard():
    return render_template('pages/dashboard.html', active_page='dashboard', page_title='Mathematics')

@app.route('/practice')
def practice():
    flashcards = load_json(FLASHCARDS_FILE)
    return render_template('pages/practice.html', flashcards=flashcards, active_page='practice', page_title='Practice Mode')

@app.route('/exam')
def exam():
    return render_template('pages/exam.html', active_page='exam', page_title='Test Mode')

@app.route('/feedback')
def feedback():
    status = request.args.get('status', 'correct')
    user_answer = request.args.get('user_answer', '28')
    correct_answer = request.args.get('correct_answer', '28')
    return render_template('pages/feedback.html', status=status, user_answer=user_answer, correct_answer=correct_answer, active_page='practice', page_title='Result')

@app.route('/api/mistake', methods=['POST'])
def record_mistake():
    mistake_data = request.json
    mistakes = load_json(MISTAKES_FILE)
    mistakes.append(mistake_data)
    save_json(MISTAKES_FILE, mistakes)
    return jsonify({"status": "success", "message": "Mistake recorded"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
