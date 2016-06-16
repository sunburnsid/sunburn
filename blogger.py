from flask import Flask, request, session, redirect, url_for, \
abort, render_template, flash
from contextlib import closing
import datetime
from extensions import anglicize, linkify
from flask_pymongo import PyMongo


#create application
app = Flask(__name__)
mongo = PyMongo(app)

def gen_all_entries():
	all_posts = mongo.db.blog.find()
	print all_posts
	return all_posts

@app.route('/')
def show_entries():
	entries = gen_all_entries()
	return render_template('show_entries.html', entries = entries)

@app.route('/virgosupercluster', methods = ['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	today = datetime.datetime.today()
	mongo.db.blog.insertOne({"title":request.form['title'], "text":request.form['text'],
	 "date":today, "link":linkify(request.form['title']), comments:[], "likes":0})
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

@app.route('/articles/<post_name>')
def display_post(post_name):
	entries = gen_all_entries()
	nuts = []
	for post in entries:
		nuts.append(post['link'])
	if post_name in nuts:
		content = entries[nuts.index(post_name)]
		return render_template('show_article.html', content = content)
	else:
		return 'Oops, looks like the article you\'re looking for doesn\'t exist.'


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