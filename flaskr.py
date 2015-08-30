# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
      """
      Connects to the DATABASE db
      """
      return sqlite3.connect(app.config['DATABASE'])

def init_db():
      """
      Initializes the db -> creates the table
      """
      with closing(connect_db()) as db:
            with app.open_resource('schema.sql', mode='r') as f:
                  db.cursor().executescript(f.read())
            db.commit()

@app.before_request
def before_request():
      """
      Connect to the DB before aneveryy request
      """
      g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
      """
      Disconnect after every request
      """
      db = getattr(g, 'db', None)
      if db is not None:
            db.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
      """
      Login View-
      If method is GET- Returns the login page
      If method is POST- Submits the login credentials
      """
      error = None
      if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                  error = 'Invalid username'
            elif request.form['password'] != app.config['PASSWORD']:
                  error = 'Invalid password'
            else:
                  session['logged_in'] = True
                  flash('You were logged in')
                  return redirect(url_for('show_entries'))
      return render_template('login.html', error=error)

@app.route('/logout')
def logout():
      """
      Logs out the currently logged in user
      """
      session.pop('logged_in', None)
      flash('You were logged out')
      return redirect(url_for('show_entries'))

@app.route('/')
def show_entries():
      """
      Returns the view with all the entries from the db
      """
      cur = g.db.execute('select title, text from entries order by id desc')
      entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
      return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
      """
      Adds new entry in the db
      """
      if not session.get('logged_in'):
            abort(401)
      g.db.execute('insert into entries (title, text) values (?, ?)',
      [request.form['title'], request.form['text']])
      g.db.commit()
      flash('New entry was successfully posted')
      return redirect(url_for('show_entries'))

if __name__ == '__main__':
      """
      Runs the application on http://127.0.0.1:5000/
      """
      app.run()
