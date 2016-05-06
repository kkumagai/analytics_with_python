# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request
import wordlist
import weblio_parser
from werkzeug.routing import BaseConverter

app = Flask(__name__, static_url_path = '')

@app.route("/")

def index():
	return """
	Hello
	"""
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter

@app.route("/<regex('[a-z]+'):user>", methods = ["GET", "POST"])
def uesr(user):
	if request.method == "POST":
		wordlist.words(user).add_memo(request.form["word"], request.form["memo"])

	temp = wordlist.words(user)
	return render_template("quiz.html"
			, user = user, word = temp.cursor)

@app.route("/<user>/completed")
def completed(user):
	words = wordlist.words(user).completed()
	return render_template("list.html"
		,user = user , words = words)

@app.route("/<user>/<word>", methods = ["GET", "POST"])
def meaning(user, word):
	if request.method == "POST":

		wordlist.words(user).add_recent(request.form["word"]
			, 1 if request.form["result"] == "known" else 0 )

		wordlist.words(user).counter(request.form["word"], "appearance" )

	try:
		return render_template("answer.html"
			,user = user , word = wordlist.words(user).select(word))
	except:
		return redirect("/{}/add/{}".format(user, word))

# @app.route("/<user>/weak")
# def completed(user):
# 	return wordlist.words(user).completed()

@app.route("/<user>/list/recent")
def recent(user):

	return render_template("recent.html", user = user, words = wordlist.wordlist(user).list)

@app.route("/<user>/add/<word>", methods = ["GET", "POST"])
def add(user, word):
	if request.method == "POST":
		wordlist.words(user).create(request.form["word"], request.form["meaning"])
		return redirect("/{}/{}".format(user,request.form["word"]))
	else:
		try:
			weblio = weblio_parser.parse(word)
			return render_template("add.html", user = user, word = weblio["word"], meaning = weblio["meaning"])
		except:
			return render_template("add.html", user = user, word = "", meaning = "")

@app.route("/<user>/update/<word>", methods = ["GET", "POST"])
def update(user, word):
	if request.method == "POST":
		wordlist.words(user).update(request.form["word"], request.form["meaning"])
		return redirect("/{}/{}".format(user,request.form["word"]))
	else:
		
		return render_template("update.html", user = user, word = wordlist.words(user).select(word))
		
if __name__ == '__main__':
    app.run(host = "0.0.0.0", debug  = True)
