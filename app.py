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
@app.route('/')
def dashboard():
    mistakes = load_json(MISTAKES_FILE)
    flashcards = load_json(FLASHCARDS_FILE)
    
    solved_count = len(mistakes)
    mistake_count = len([m for m in mistakes if not m.get('correct', True)])
    accuracy = int(((solved_count - mistake_count) / solved_count * 100)) if solved_count > 0 else 0
    
    stats = [
        {"label": "Accuracy", "value": str(accuracy), "unit": "%"},
        {"label": "Solved", "value": str(solved_count), "unit": ""},
        {"label": "Mistakes", "value": str(mistake_count), "unit": ""}
    ]
    
    # Placeholder mastery/focus until AI generates them
    mastery = []
    focus_areas = []
    
    return render_template('pages/dashboard.html', 
                           active_page='dashboard', 
                           page_title='Progress & Mastery',
                           stats=stats,
                           mastery=mastery,
                           focus_areas=focus_areas,
                           mistakes=mistakes)


@app.route('/practice')
def practice():
    flashcards = load_json(FLASHCARDS_FILE)
    q_idx = int(request.args.get('q_idx', 0))
    
    if not flashcards:
        return "No flashcards found", 404
        
    # Ensure q_idx is within bounds
    q_idx = max(0, min(q_idx, len(flashcards) - 1))
    current_card = flashcards[q_idx]
    
    total = len(flashcards)
    progress = int(((q_idx + 1) / total) * 100)
    
    session_info = {
        "subject": "Calculus II",
        "step": q_idx + 1,
        "total_steps": total,
        "timer": "14:02"
    }
    return render_template('pages/practice.html', 
                           flashcards=flashcards,
                           current_card=current_card,
                           q_idx=q_idx,
                           active_page='practice', 
                           page_title='Practice Mode',
                           session_info=session_info,
                           progress_percent=progress)

@app.route('/exam')
def exam():
    flashcards = load_json(FLASHCARDS_FILE)
    mcq_questions = [q for q in flashcards if q.get('type') == 'mcq']
    q_idx = int(request.args.get('q_idx', 0))
    
    if not mcq_questions:
        return render_template('pages/exam.html', 
                               active_page='exam', 
                               page_title='Test Mode',
                               session_info={"total_questions": 0},
                               question_data=None,
                               progress_percent=0)
        
    q_idx = max(0, min(q_idx, len(mcq_questions) - 1))
    current_question = mcq_questions[q_idx]
    
    total = len(mcq_questions)
    progress = int(((q_idx + 1) / total) * 100)
    
    session_info = {
        "subject": "Calculus I: Differentiation",
        "topic": current_question.get('topic') if current_question else "General",
        "question_num": q_idx + 1,
        "total_questions": total,
        "timer": "15:00"
    }
    return render_template('pages/exam.html', 
                           active_page='exam', 
                           page_title='Test Mode',
                           session_info=session_info,
                           question_data=current_question,
                           q_idx=q_idx,
                           progress_percent=progress)



@app.route('/review')
def review_mistakes():
    mistakes = load_json(MISTAKES_FILE)
    flashcards = load_json(FLASHCARDS_FILE)
    
    # Map question IDs to question content for display
    card_map = {q['id']: q for q in flashcards}
    
    # Enrich mistakes with question content
    enriched_mistakes = []
    for m in mistakes:
        card = card_map.get(m['question_id'])
        if card:
            m['question_text'] = card.get('question')
            m['latex'] = card.get('latex')
            enriched_mistakes.append(m)
            
    return render_template('pages/review_mistakes.html', 
                           active_page='review', 
                           page_title='Review Mistakes',
                           mistakes=enriched_mistakes)

@app.route('/feedback')
def feedback():
    status = request.args.get('status', 'correct')
    user_answer = request.args.get('user_answer', '')
    correct_answer = request.args.get('correct_answer', '')
    q_idx = int(request.args.get('q_idx', 0))
    source = request.args.get('source', 'practice')
    
    flashcards = load_json(FLASHCARDS_FILE)
    if source == 'exam':
        flashcards = [q for q in flashcards if q.get('type') == 'mcq']
        
    current_question = flashcards[q_idx] if q_idx < len(flashcards) else None
    
    next_idx = q_idx + 1 if q_idx + 1 < len(flashcards) else None
    
    return render_template('pages/feedback.html', 
                           status=status, 
                           user_answer=user_answer, 
                           correct_answer=correct_answer, 
                           q_idx=q_idx,
                           next_idx=next_idx,
                           source=source,
                           question=current_question,
                           active_page=source, 
                           page_title='Result')


@app.route('/add')
def add_question():
    return render_template('pages/add_question.html', active_page='add', page_title='Add Question')

@app.route('/api/add_question', methods=['POST'])
def api_add_question():
    data = request.json
    flashcards = load_json(FLASHCARDS_FILE)
    
    # Generate ID
    last_id = "q0"
    if flashcards:
        # Sort by ID to find the highest number
        ids = [int(q['id'][1:]) for q in flashcards if q['id'].startswith('q')]
        if ids:
            last_id = f"q{max(ids)}"
    
    new_id_num = int(last_id[1:]) + 1
    new_id = f"q{new_id_num}"
    
    new_question = {
        "id": new_id,
        "topic": data.get('topic'),
        "type": data.get('type', 'text'),
        "question": data.get('question'),
        "latex": data.get('latex'),
        "answer": data.get('answer'),
        "explanation": data.get('explanation', [])
    }
    
    if new_question['type'] == 'mcq':
        new_question['options'] = data.get('options', [])
        
    flashcards.append(new_question)
    save_json(FLASHCARDS_FILE, flashcards)
    
    return jsonify({"status": "success", "message": f"Question {new_id} added successfully", "id": new_id})

@app.route('/api/mistake', methods=['POST'])

def record_mistake():
    mistake_data = request.json
    mistakes = load_json(MISTAKES_FILE)
    mistakes.append(mistake_data)
    save_json(MISTAKES_FILE, mistakes)
    return jsonify({"status": "success", "message": "Mistake recorded"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

