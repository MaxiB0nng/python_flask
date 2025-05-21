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
        return redirect('/q2/')
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
        return redirect ('/q3/')
    return render_template('q2.html', title="Spørgsmål 2")

@app.route('/q3/', methods= ['GET', 'POST'])
def q3():
    if request.method == 'POST':
        selected = request.form.getlist('checkboxes')
        svar_text = ', '.join(selected)


        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO q3_responses (svar_3) VALUES (?)", (svar_text,))
        conn.commit()
        conn.close()

        print("Indsendt svar:", svar_text)
        return redirect ('/q4/')
    return render_template('q3.html', title="Spørgsmål 3")

@app.route('/q4/', methods= ['GET', 'POST'])
def q4():
    if request.method == 'POST':
        selected = request.form.getlist('checkboxes')
        svar_text = ', '.join(selected)


        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO q4_responses (svar_4) VALUES (?)", (svar_text,))
        conn.commit()
        conn.close()

        print("Indsendt svar:", svar_text)
        return redirect ('/')
    return render_template('q4.html', title="Spørgsmål 4")




@app.route('/results/', methods=['GET', 'POST'])
def results():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # --- Q1 ---
    labels_q1 = ["Billigt", "Acceptabelt", "Dyrt"]
    cursor.execute("SELECT svar, COUNT(*) FROM q1_responses GROUP BY svar")
    rows_q1 = cursor.fetchall()
    dict_q1 = {label: 0 for label in labels_q1}
    for row in rows_q1:
        if row[0] is None:
            continue
        for val in row[0].split(", "):  # Handle multiple selections
            if val in dict_q1:
                dict_q1[val] += row[1]
    data_q1 = [dict_q1[label] for label in labels_q1]

    # --- Q2 ---
    labels_q2 = ["Dagens ret", "Sandwich", "Pizza", "pølsehorn", "Kage", "Sodavand"]
    cursor.execute("SELECT svar_2, COUNT(*) FROM q2_responses GROUP BY svar_2")
    rows_q2 = cursor.fetchall()
    dict_q2 = {label: 0 for label in labels_q2}
    for row in rows_q2:
        if row[0] is None:
            continue
        for val in row[0].split(", "):
            if val in dict_q2:
                dict_q2[val] += row[1]
    data_q2 = [dict_q2[label] for label in labels_q2]

    # --- Q3 ---
    labels_q3 = ["Det er nemt og hurtigt.", "God stemning"]
    cursor.execute("SELECT svar_3, COUNT(*) FROM q3_responses GROUP BY svar_3")
    rows_q3 = cursor.fetchall()
    dict_q3 = {label: 0 for label in labels_q3}
    for row in rows_q3:
        if row[0] is None:
            continue
        for val in row[0].split(", "):
            if val in dict_q3:
                dict_q3[val] += row[1]
    data_q3 = [dict_q3[label] for label in labels_q3]

    # --- Q4 ---
    labels_q4 = [
        "Der er for få fritidsaktiviteter",
        "Passende mængde aktiviteter",
        "Der er for mange aktiviteter"
    ]
    cursor.execute("SELECT svar_4, COUNT(*) FROM q4_responses GROUP BY svar_4")
    rows_q4 = cursor.fetchall()
    dict_q4 = {label: 0 for label in labels_q4}
    for row in rows_q4:
        if row[0] is None:
            continue
        for val in row[0].split(", "):
            if val in dict_q4:
                dict_q4[val] += row[1]
    data_q4 = [dict_q4[label] for label in labels_q4]


    conn.close()

    return render_template(
        'results.html',
        labels_q1=json.dumps(labels_q1), data_q1=json.dumps(data_q1),
        labels_q2=json.dumps(labels_q2), data_q2=json.dumps(data_q2),
        labels_q3=json.dumps(labels_q3), data_q3=json.dumps(data_q3),
        labels_q4=json.dumps(labels_q4), data_q4=json.dumps(data_q4)
    )


if __name__ == '__main__':
    app.debug = True
    #app.run(debug=True) #Koer kun paa localhost
    app.run(host='0.0.0.0', port=5000)
