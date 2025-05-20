import sqlite3
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


@app.route('/q1/', methods=['POST', 'GET'])
def q1():
    q1_form = Q1_Form()
    if q1_form.validate_on_submit():
        selected_options = request.form.getlist('checkbox')
        print(f'Selected options: {", ".join(selected_options)}')
        return redirect('/q2/')
    return render_template('q1.html', q1_form = q1_form)

@app.route('/q2/', methods=['POST', 'GET'])
def q2():
    txt = "spørgsmål 2"
    q2_form = Q2_Form()
    if q2_form.validate_on_submit():
        if q2_form.valg.data:
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            valg = q2_form.valg.data
            print(valg)
            cursor.execute('INSERT INTO driver(result_2) VALUES ('+valg+')')
            conn.commit()
            conn.close()
            """
            Ekstra-opgave:
            En måde at sikre sig at brugeren ikke kan stemme to
            gange, er ved at sætte en cookie her v.hj.a.javascript.
            https://www.w3schools.com/js/js_cookies.asp

            """
            return redirect('/q3/')
    return render_template('q2.html', q2_form = q2_form, title=txt)


if __name__ == '__main__':
    app.debug = True
    #app.run(debug=True) #Koer kun paa localhost
    app.run(host='0.0.0.0', port=5000)
