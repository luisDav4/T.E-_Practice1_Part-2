from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Univalle'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/studentlist', methods=['GET'])
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return render_template('list.html', students=data)

@app.route('/studentcreate', methods=['GET', 'POST'])
def student_create():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        semester = request.form['semester']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO student (first_name, last_name, city, semester) VALUES (%s, %s, %s, %s)',
                       (first_name, last_name, city, semester))
        
        mysql.connection.commit()
        cursor.close()
        
        return redirect('/studentlist')
    
    return render_template('create.html')


@app.route('/studentedit/<int:id>', methods=['GET', 'POST'])
def student_edit(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        semester = request.form['semester']
        
        cursor.execute('UPDATE student SET first_name = %s, last_name = %s, city = %s, semester = %s WHERE id = %s',
                       (first_name, last_name, city, semester, id))
        
        mysql.connection.commit()
        cursor.close()
        
        return redirect('/studentlist')
    
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student WHERE id = %s', (id,))
    student = cursor.fetchone()
    cursor.close()
    
    return render_template('edit.html', student=student)

@app.route('/studentdelete/<int:id>', methods=['GET'])
def student_delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM student WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    
    return redirect('/studentlist')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
