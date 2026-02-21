from flask import Flask,render_template,url_for,redirect,request

import sqlite3

def init_db():
    conn=sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXt,course TEXT)
                   """)
    
    conn.commit()
    conn.close()
init_db()

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add',methods=["GET","POST"])
def add_student():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']

        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()

        cursor.execute("INSERT INTO students(name,email,course)VALUES( ?, ?, ?)",(name,email,course))

        conn.commit()
        conn.close()

        return redirect('/')
    
    return render_template('add_student.html')

@app.route('/students')
def students():
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()

    cursor.execute("SELECT * from students")
    data=cursor.fetchall()
    conn.close()

    return render_template("student.html",students=data)

@app.route('/delete/<int:id>')
def delete(id):
     conn=sqlite3.connect("database.db")
     cursor=conn.cursor()

     cursor.execute("DELETE FROM students WHERE id=?",(id,))

     conn.commit()
     conn.close()

     return redirect('/students')


@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()

    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']
        
        course.execute("UPDATE students SET name=?,email=?,course=? WHERE id=?",(name,email,course,id))

        conn.commit()
        conn.close()

        return redirect('/students')
    
    cursor.execute("SELECT * FROM students WHERE id=?",(id,))
    student=cursor.fetchone()
    conn.close()

    return render_template("edit_student.html",students=student)

if __name__=='__main__':
    app.run(debug=True)