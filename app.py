from flask import Flask, render_template, request, session, redirect, url_for
import os
from dotenv import load_dotenv
import random

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'a-fallback-key-for-dev')  # Provides a fallback for development

# A simple list of math question templates.
question_templates = [
    "What is {a} + {b}?",
    "What is {a} * {b}?",
    "What is {a} - {b}?",
]

def generate_question():
    """Generates a random math question and its answer."""
    template = random.choice(question_templates)
    a = random.randint(1, 12)
    b = random.randint(1, 12)
    
    question_text = template.format(a=a, b=b)
    
    # Calculate the correct answer based on the template
    if "+" in template:
        correct_answer = a + b
    elif "*" in template:
        correct_answer = a * b
    elif "-" in template:
        correct_answer = a - b
    else:
        correct_answer = None
        
    return question_text, correct_answer

@app.route('/')
def index():
    """Renders the homepage."""
    # Clear any old question data when starting fresh
    session.pop('current_question', None)
    session.pop('correct_answer', None)
    return render_template('index.html')

@app.route('/start_practice', methods=['POST'])
def start_practice():
    """Starts a practice session by generating a question and storing it."""
    question_text, correct_answer = generate_question()
    # Store the question and answer in the user's session
    session['current_question'] = question_text
    session['correct_answer'] = str(correct_answer) # Store as string to compare easily later
    return redirect(url_for('practice'))

@app.route('/practice')
def practice():
    """Displays the practice question."""
    question_text = session.get('current_question')
    if not question_text:
        # If for some reason there's no question, send them back to start
        return redirect(url_for('index'))
    return render_template('practice.html', question=question_text)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    """Checks the user's answer against the correct one."""
    user_answer = request.form.get('answer', '').strip()
    correct_answer = session.get('correct_answer')
    
    # Basic validation and feedback
    if not user_answer:
        feedback = "Please enter an answer."
        is_correct = False
    else:
        # Compare the user's input (string) to the stored correct answer (string)
        is_correct = (user_answer == correct_answer)
        if is_correct:
            feedback = "✅ Correct! Well done!"
        else:
            feedback = f"❌ Incorrect. The correct answer was {correct_answer}."
            
    return render_template('results.html', feedback=feedback, correct=is_correct)

if __name__ == '__main__':
    app.run(debug=True)