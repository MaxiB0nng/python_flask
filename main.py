import sqlite3
import json
from flask import Flask, render_template, request, redirect
from app.config import Config
from app.forms import Q1_Form, Q2_Form, Q3_Form
db = 'database.db'
app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def home():
    # Her kan fx hentes data og sættes ind i html-koden
    txt = "spørgsmåls hjemmeside"
    return render_template('index.html', title=txt)


@app.route('/q1/', methods=['GET', 'POST'])
def q1():
    if request.method == 'POST':
        selected = request.form.getlist('checkboxes')  # Get selected values as a list
        svar_text = ', '.join(selected)  # Convert list to comma-separated string

        # Save to database
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO q1_responses (svar) VALUES (?)", (svar_text,))
        conn.commit()
        conn.close()

        print("Indsendt svar:", svar_text)
        return redirect('/')
    return render_template('q1.html', title="Spørgsmål 1")


@app.route('/q2/', methods= ['GET', 'POST'])
def q2():
    if request.method == 'POST':
        selected = request.form.getlist('checkboxes')
        svar_text = ', '.join(selected)


        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO q2_responses (svar_2) VALUES (?)", (svar_text,))
        conn.commit()
        conn.close()

        print("Indsendt svar:", svar_text)
        return redirect ('/')
    return render_template('q2.html', title="Spørgsmål 2")




@app.route('/results/', methods=['GET', 'POST'])
def results():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Fetch count of each unique text response
    cursor.execute("SELECT svar, COUNT(*) FROM q1_responses GROUP BY svar")
    rows = cursor.fetchall()
    conn.close()

    # Ensure consistent order: Billigt, Acceptabelt, Dyrt
    labels = ["Billigt", "Acceptabelt", "Dyrt"]
    data_dict = dict(rows)
    counts = [data_dict.get(label, 0) for label in labels]

    return render_template('results.html',data_1=json.dumps(counts))

def setup_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS q2_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    svar_2 TEXT
    );

    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.debug = True
    #app.run(debug=True) #Koer kun paa localhost
    app.run(host='0.0.0.0', port=5000)
