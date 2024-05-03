
from flask import Flask, request, jsonify, render_template,redirect,url_for
import sqlite3

app = Flask(__name__)

# Create a basic SQLite database for storing course_tab
def init_db():
    with sqlite3.connect('course.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS course_tab
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         title TEXT, 
                         instructor TEXT, 
                         price INTEGER)''')
@app.route('/')
def home():
    # Fetch all course_tab from the database
    with sqlite3.connect('course.db') as conn:
        course_tab = conn.execute('SELECT * FROM course_tab').fetchall()
    return render_template('course.html', course_tab=course_tab)

@app.route('/add', methods=['POST'])
def add_course():
    title = request.form['title']
    instructor = request.form['instructor']
    price = int(request.form['price'])
    with sqlite3.connect('course.db') as conn:
        conn.execute('INSERT INTO course_tab (title, instructor, price) VALUES (?, ?, ?)', (title, instructor, price))
    return redirect(url_for('home'))

@app.route('/update', methods=['POST'])
def update_course():
    course_id = int(request.form['id'])
    title = request.form['title']
    instructor = request.form['instructor']
    price = int(request.form['price'])
    with sqlite3.connect('course.db') as conn:
        conn.execute('UPDATE course_tab SET title = ?, instructor = ?, price = ? WHERE id = ?', (title, instructor, price, course_id))
    return 'course updated successfully!'

@app.route('/delete', methods=['POST'])
def delete_course():
    course_id = int(request.form['id'])
    with sqlite3.connect('course.db') as conn:
        conn.execute('DELETE FROM course_tab WHERE id = ?', (course_id,))
    return 'course deleted successfully!'

@app.route('/search', methods=['GET'])
def search_course_tab():
    search_query = request.args.get('query', '')
    with sqlite3.connect('course.db') as conn:
        results = conn.execute('SELECT * FROM course_tab WHERE title LIKE ? OR instructor LIKE ?', (f'%{search_query}%', f'%{search_query}%')).fetchall()
    return jsonify(results)

if __name__ == '__main__':
    init_db()
    app.run(port=9001)
