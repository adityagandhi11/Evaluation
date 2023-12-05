from flask import Flask, render_template, request, session, redirect
import sqlite3

app1 = Flask(__name__)

def attendence(atd1,atd2,atd3,atd4):
    tot = (atd1 + atd2 + atd3 + atd4)/4
    if tot >= 95:
        return 10
    elif tot >=90:
        return 9.75
    elif tot >=85:
        return 9.5
    elif tot >= 80:
        return 9.25
    elif tot >=75:
        return 9.0
    else:
        return 8.5

def cgp(cgpa):
    if cgpa >= 9.5:
        return 10
    elif cgpa >= 9.0:
        return 9.75
    elif cgpa >= 8.5:
        return 9.5
    elif cgpa >= 8.0:
        return 9.25
    elif cgpa >= 7.5:
        return 9.0
    else:
        return 8.75

def sessional(smark):
    if smark >= 95:
        return 10
    elif smark >=90:
        return 9.75
    elif smark >=85:
        return 9.5
    elif smark >= 80:
        return 9.25
    elif smark >=75:
        return 9.0
    else:
        return 8.5

def extra(eca):
    if eca == 5:
        return 10
    elif eca == 4:
        return 9.75
    elif eca == 3:
        return 9.5
    elif eca == 2:
        return 9.25
    else:
        return 9.0

def sgp(sgpa1,sgpa2,sgpa3,sgpa4):
    if sgpa4>=sgpa3>=sgpa2>=sgpa1:
        return 10
    elif sgpa4<sgpa3<sgpa2<sgpa1:
        return 5
    else:
        return 7.5


@app1.route('/')
def login():
    error = request.args.get('error')
    return render_template('login.html', error=error)

@app1.route('/home')
def home():
    username = request.args.get('username')
    password = request.args.get('password')

    conn = sqlite3.connect(r"evaluation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MYDB WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        student = {
            'name': user[2],
            'age': user[3],
            'gender': user[4],
            'address': user[5],
            'email': user[9],
            'father_name': user[10],
            'course': user[6],
            'semester': user[7],
            'section': user[8],
            'cgpa': user[11],
        }


        conn = sqlite3.connect(r"evaluation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Marks WHERE username=?", (user[0],))
        performance = cursor.fetchone()
        conn.close()

        sgpa1 = performance[1]
        sgpa2 = performance[2]
        sgpa3 = performance[3]
        sgpa4 = performance[4]
        cgpa = performance[5]
        smark = performance[6]
        eca = performance[7]
        atd1 = performance[8]
        atd2 = performance[9]
        atd3 = performance[10]
        atd4 = performance[11]


        total = 0.0

        total = total + attendence(atd1,atd2,atd3,atd4)
        total = total + cgp(cgpa)
        total = total + sessional(smark)
        total = total + extra(eca)
        total = total + sgp(sgpa1,sgpa2,sgpa3,sgpa4)
        total = total / 5

        if total>9.0:
            remarks = 'Improving Performance. Can do better.'
        elif total > 8.0:
            remarks = 'Constant Performance.Can do better than this.'
        else:
            remarks = 'Impairing Performance.Needs to work really hard.'

        conn = sqlite3.connect(r"evaluation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT sgpa1,sgpa2,sgpa3,sgpa4 FROM Marks WHERE username=?", (user[0],))
        perform = cursor.fetchone()
        conn.close()

        return render_template('homepage.html', student=student, performance=perform,remarks=remarks)
    else:
        error = 'Invalid Credentials'
        return redirect('/?error=' + error)

if __name__ == '__main__':
    app1.run(debug=True)
