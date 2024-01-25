from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def letter_grade(percentage):
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'Fail'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        category = request.form['category']
        weight = float(request.form['weight'])
        grade = float(request.form['grade'])

        if 'grades' not in session:
            session['grades'] = {}
            session['total_weight'] = 0

        # Preventing the total weight from exceeding 100%.
        if session['total_weight'] + weight > 100:
            error_message = "Total weight cannot exceed 100%. Please adjust the weights."
            return render_template('index.html', error_message=error_message, grades=session['grades'])

        session['grades'][category] = {'weight': weight, 'grade': grade}
        session['total_weight'] += weight
        session.modified = True

        return redirect(url_for('index'))

    return render_template('index.html', grades=session.get('grades', {}))

@app.route('/result')
def result():
    if 'grades' not in session or session['total_weight'] != 100:
        error_message = "Incomplete data: Make sure the total weight adds up to 100."
        return render_template('result.html', error_message=error_message)

    total_score = sum(item['weight'] / 100 * item['grade'] for item in session['grades'].values())
    final_grade = letter_grade(total_score)
    session.clear()

    return render_template('result.html', result=final_grade)

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
