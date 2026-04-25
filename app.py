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
    stats = [
        {"label": "Accuracy", "value": "92", "unit": "%"},
        {"label": "Solved", "value": "1,240", "unit": ""},
        {"label": "Streak", "value": "5", "unit": "Days"}
    ]
    mastery = [
        {
            "title": "Algebraic Foundations",
            "percentage": 85,
            "description": "Excelling in Quadratic Equations and Polynomial Identities."
        },
        {
            "title": "Calculus & Limits",
            "percentage": 60,
            "description": "Focus recommended on Integration by Parts."
        }
    ]
    focus_areas = [
        {
            "label": "Critical Deficit",
            "title": "Implicit Differentiation",
            "description": "Requires practice on chain rule applications within non-linear functions."
        },
        {
            "label": "Technical Error Path",
            "title": "Logarithmic Transformation",
            "description": "Frequent sign errors observed in base-10 conversion steps."
        }
    ]
    return render_template('pages/dashboard.html', 
                           active_page='dashboard', 
                           page_title='Progress & Mastery',
                           stats=stats,
                           mastery=mastery,
                           focus_areas=focus_areas)

@app.route('/practice')
def practice():
    flashcards = load_json(FLASHCARDS_FILE)
    session_info = {
        "subject": "Calculus II",
        "step": 4,
        "total_steps": 12,
        "timer": "14:02"
    }
    return render_template('pages/practice.html', 
                           flashcards=flashcards, 
                           active_page='practice', 
                           page_title='Practice Mode',
                           session_info=session_info,
                           progress_percent=33)

@app.route('/exam')
def exam():
    session_info = {
        "subject": "Calculus I: Differentiation",
        "topic": "Section 4.2: The Chain Rule Evaluation",
        "question_num": 3,
        "total_questions": 10,
        "timer": "14:22"
    }
    return render_template('pages/exam.html', 
                           active_page='exam', 
                           page_title='Test Mode',
                           session_info=session_info,
                           progress_percent=30)

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
