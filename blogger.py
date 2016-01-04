import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing
import datetime
from extensions import anglicize

#config
DATABASE = 'sunburn.db'
DEBUG = True
SECRET_KEY = 'hotline bling'
USERNAME = 'admin'
PASSWORD = 'default'

#create application
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('shape.sql', mode='r') as j:
			db.cursor().executescript(j.read())
		db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text, month, day, year from entries order by id desc')
	entries = [dict(title = row[0], text = row[1],  month = row[2],  day = row[3], year = row[4]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries = entries)

@app.route('/virgosupercluster', methods = ['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	today = datetime.datetime.now()
	g.db.execute('insert into entries (title, text, month, day, year) values (?, ?, ?, ?, ?)', 
		[request.form['title'], request.form['text'], anglicize(today.month), today.day, today.year])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))


@app.route('/orionsbelt', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username or password'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid username or password'
		else:
			session['logged_in'] = True
			flash('You were logged in.')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error = error)

@app.route('/ultradeepfield')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out.')
	return redirect(url_for('show_entries'))



if __name__ == '__main__':
	app.run()