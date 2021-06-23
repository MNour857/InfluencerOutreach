from flask import Flask, render_template,request, send_from_directory,Response,session,redirect
import os
from hashlib import md5
import mysql.connector
import io
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import json
from instascrape import *
import csv
import numpy as np
import statistics
from datetime import timedelta  
from datetime import datetime
import urllib.request




def getCurrentDate():
	return datetime.today().strftime('%Y-%m-%d')

def fileExists(filename):
	return os.path.isfile(filename)

def toPrefix(i):
	res = ""
	if i>=1000  and i< 1000000:
		res = str(round(i/1000,1))+"K"
	elif i >= 1000000:
		res = str(round(i/1000000,1))+"M"
	else:
		res = str(i)
	return res

os.system("cls")
try:
	app = Flask(__name__)
	app.config['SECRET_KEY'] = "alZeeshan1895"

	mydb = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  password="",
	  database="dash"
	)

	c = mydb.cursor()
except:

	print("[ Server Not Found ]")
	exit(1)
# CHECK



def getPlot(p):
	data = getCsv(p)
	plot_data = []
	for i in data:
		score = getScore(i)/10
		t = tuple([i[0],score])
		plot_data.append(t)
	return plot_data


def getScore(a):
	score = statistics.mean([int(a[2]),int(a[3]),int(a[4])])	
	return score

def getCsv(fileName):
	data = []
	with open(fileName+".csv", "r", encoding="utf-8", errors="ignore") as scraped:
		reader = csv.reader(scraped, delimiter=',')
		for row in reader:
			if row:
				columns = [row[0], row[1], row[2], row[3],row[4]]
				data.append(columns)
	return data


#

@app.route("/session/set/<key>/<value>")
def setSession(key,value):
	session[key] = value
	return "session inserted"

@app.route("/session/get/<key>")
def getSession(key):
	d = session.get(key)
	if d:
		return d
	else:
		return "0"

@app.route("/addUser")
def addUser():
	return send_html("addUser.html")


@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

@app.route("/")
def home():
    return render_template('home.html')

def replicateData(un):
	data = getCsv(un)
	f = open(un+"1.csv",'w')
	f.write("date,followers\n")
	for i in data:
		new_data = i[0]+","+i[3]+"\n"
		f.write(new_data)
	f.close()


def calculatePrediction(un):
	from pandas import read_csv
	from pandas import DataFrame
	from pandas import datetime
	from matplotlib import pyplot
	from pandas.plotting import autocorrelation_plot
	from statsmodels.tsa.arima.model import ARIMA
	from sklearn.metrics import mean_squared_error
	from math import sqrt
	replicateData(un)
	predicted = []
	series = read_csv(un+'1.csv', header=0, parse_dates=[0], index_col=0, squeeze=True)
	series.index = series.index.to_period('M')
	# split into train and test sets
	X = series.values
	size = int(len(X) * 0.66)
	train, test = X[0:size], X[size:len(X)]
	history = [x for x in train]
	predictions = list()
	# walk-forward validation
	for t in range(len(test)):
		model = ARIMA(history, order=(5,1,0))
		model_fit = model.fit()
		output = model_fit.forecast()
		yhat = output[0]
		predictions.append(yhat)
		obs = test[t]
		history.append(obs)
		#print('predicted=%f, expected=%f' % (yhat, obs))
		predicted.append(tuple([yhat,obs]))
	# evaluate forecasts
	rmse = sqrt(mean_squared_error(test, predictions))
	#print('Test RMSE: %.3f' % rmse)
	return predicted;

def getDatesByDifference(i,n):
	from datetime import date as d
	from datetime import timedelta as td
	dates =[]
	for k in range(1,n+1):
		s = d.today() + td(days=i)
		st = d.strftime(s,"%Y-%m-%d")
		dates.append(st)
		i += i
	return dates

@app.route("/detail/<un>")
def analy(un):
	data = []
	data_posts=[]
	data_followres = []
	data_followings = []

	post = "0"
	follower = "0"
	follow = "0"
	with open(un+".csv", "r", encoding="utf-8", errors="ignore") as scraped:
		reader = csv.reader(scraped, delimiter=',')
		for row in reader:
			if row:
				columns = [row[0], row[1], row[2], row[3],row[4]]
				data.append(columns)
				data_posts.append(tuple([row[0],int(row[2])]))
				data_followres.append(tuple([row[0],int(row[3])]))
				data_followings.append(tuple([row[0],int(row[4])]))
	user = data[-1]
	post = toPrefix(int(user[2]))
	follower = toPrefix(int(user[3]))
	follow = toPrefix(int(user[4]))

	labels_posts = [row[0] for row in data_posts]
	values_posts = [row[1] for row in data_posts]

	labels_follow = [row[0] for row in data_followres]
	values_follow = [row[1] for row in data_followres]

	labels_following = [row[0] for row in data_followings]
	values_following = [row[1] for row in data_followings]

	predictionData = calculatePrediction(un);
	values_pre = [row[0] for row in predictionData]
	values_pre_exp = [row[1] for row in predictionData]
	
	labels_pre = getDatesByDifference(1,3)
	return render_template("analysis.html",un=un,posts=post,followers = follower,following = follow,labels_posts=labels_posts,values_posts=values_posts,labels_follow=labels_follow,values_follow=values_follow,labels_following=labels_following,values_following=values_following,values_pre=values_pre,values_pre_exp=values_pre_exp,labels_pre=labels_pre)

@app.route("/search/<un>/")
def search(un):
	data = []
	post = "0"
	follower = "0"
	follow = "0"
	with open(un+".csv", "r", encoding="utf-8", errors="ignore") as scraped:
		reader = csv.reader(scraped, delimiter=',')
		for row in reader:
			if row:
				columns = [row[0], row[1], row[2], row[3],row[4]]
				data.append(columns)
	user = data[-1]
	post = toPrefix(int(user[2]))
	follower = toPrefix(int(user[3]))
	follow = toPrefix(int(user[4]))
	o = session.get("user")
	statistic = ""
	if o:
		statistic = ""
	else:
		statistic = "You are Not Logged In"
	plot_data = getPlot(un)
	labels = [row[0] for row in plot_data]
	values = [row[1] for row in plot_data]
	return render_template("search.html",un=un,posts=post,followers = follower,following = follow,stats = statistic,labels=labels,values=values)

@app.route("/auth/login",methods = ['POST', 'GET'])
def makeLogin():
	username = ""
	password = ""
	if request.method == 'POST':
		passv1 = request.form['password']
		username = request.form['username']
		password = getHash(passv1)
	elif request.method == 'GET':
		return Response(status = 404)
		passv1 = request.args.get('password')
		username = request.args.get('username')
		password = getHash(passv1)
	else:
		status_code = Response(status=201)
		return status_code
	SQL = "SELECT * FROM user where username='"+username+"' and password='"+password+"'"
	c.execute(SQL)
	r = c.fetchall()
	res = []	
	for i in r:
		_t = {
		"id":i[0],
		"username":i[1],
		"email":i[2],
		"admin":i[3]
		}
		res.append(_t)

	if res:
		return json.dumps(res);
	else:
		return '301'

@app.route("/auth/register",methods = ['POST', 'GET'])
def makeRegistration():
	username = ""
	password = ""
	email =""
	if request.method == 'POST':
		passv1 = request.form['password']
		username = request.form['username']
		email = request.form['email']
		password = getHash(passv1)

	elif request.method == 'GET':
		passv1 = request.args.get('password')
		username = request.args.get('username')
		email = request.args.get('email')
		password = getHash(passv1)
	else:
		status_code = Response(status=201)
		return status_code
	
	try:
		SQL = "INSERT INTO user VALUES('?','"+username+"','"+email+"',0,'"+password+"')";
		c.execute(SQL)
		mydb.commit()
		return '200'
	except:
		return 'User exists'


@app.route("/auth/get/users",methods=['GET'])
def getUsers():
	SQL = "SELECT * FROM user"
	c.execute(SQL)
	r = c.fetchall()
	res = []	
	for i in r:
		_t = {
		"id":i[0],
		"username":i[1],
		"email":i[2],
		"admin":i[3]
		}
		res.append(_t)

	return json.dumps(res);


@app.route("/auth/add/user",methods=['POST','GET'])
def adduser():
	username = ""
	password = ""
	email =""
	is_Admin = False
	if request.method == 'POST':
		passv1 = request.form['password']
		username = request.form['username']
		email = request.form['email']
		password = getHash(passv1)
		is_Admin = request.form['admin']

	elif request.method == 'GET':
		passv1 = request.args.get('password')
		username = request.args.get('username')
		email = request.args.get('email')
		password = getHash(passv1)
		is_Admin = request.args.get('admin')
	else:
		status_code = Response(status=201)
		return status_code
	
	try:
		SQL = "INSERT INTO user VALUES('?','"+username+"','"+email+"',"+is_Admin+",'"+password+"')";
		c.execute(SQL)
		mydb.commit()
		return '200'
	except:
		return 'User exists'

@app.route("/error")
def error():
	return Response(status = 404)

@app.route("/login")
def login():
	return send_html("login.html")

@app.route("/signup")
def signup():
	return send_html("register.html")

#for API
API_ROUTE = "/api/v2/"

#for css,js and html files	
@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory('templates/js', path)

@app.route("/crawl/insta/<un>")
def crawlUn(un):
	username = un
	insta = Profile('https://www.instagram.com/'+username+'/')
	insta.scrape()
	fieldnames = {"date","username","posts","followers","following"}
	details = {
		"date":getCurrentDate(),
		"username":username,
		"posts":str(insta.posts),
		"followers":str(insta.followers),
		"following":str(insta.following)
		}
	fileName = username+".csv"
	f = open(fileName, "a")
	if fileExists(fileName) == False:
		f.write("Date,UserName,Post,Followers,Following\n")
	row = details['date']+","+details['username']+","+details['posts']+","+details['followers']+","+details['following']+"\n"
	f.write(row)
	f.close()
	return redirect("/search/"+un)
	
@app.route("/yt-search/<un>")
def yt_search(un):
	data = []
	views = "0"
	subs = "0"
	videos = "0"
	with open(un+".csv", "r", encoding="utf-8", errors="ignore") as scraped:
		reader = csv.reader(scraped, delimiter=',')
		for row in reader:
			if row:
				columns = [row[0], row[1], row[2], row[3],row[4]]
				data.append(columns)
	user = data[-1]
	videos = toPrefix(int(user[2]))
	subs = toPrefix(int(user[3]))
	views = toPrefix(int(user[4]))
	o = session.get("user")
	plot_data = getPlot(un)
	labels = [row[0] for row in plot_data]
	values = [row[1] for row in plot_data]
	return render_template("yt-search.html",un=un,views=views,videos=videos,subs=subs,labels=labels,values=values)

@app.route("/yt-detail/<un>")
def predict_yt(un):
	data = []
	data_subs=[]
	data_views = []
	data_videos = []

	with open(un+".csv", "r", encoding="utf-8", errors="ignore") as scraped:
		reader = csv.reader(scraped, delimiter=',')
		for row in reader:
			if row:
				columns = [row[0], row[1], row[2], row[3],row[4]]
				data.append(columns)
				data_subs.append(tuple([row[0],int(row[3])]))
				data_views.append(tuple([row[0],int(row[4])]))
				data_videos.append(tuple([row[0],int(row[2])]))
	user = data[-1]
	videos = toPrefix(int(user[2]))
	subs = toPrefix(int(user[3]))
	views = toPrefix(int(user[4]))

	labels_subs = [row[0] for row in data_subs]
	values_subs = [row[1] for row in data_subs]

	labels_views = [row[0] for row in data_views]
	values_views = [row[1] for row in data_views]

	labels_videos = [row[0] for row in data_videos]
	values_videos = [row[1] for row in data_videos]

	predictionData = calculatePrediction(un);

	values_pre = [row[0] for row in predictionData]
	values_pre_exp = [row[1] for row in predictionData]
	labels_pre = getDatesByDifference(1,3)

	return render_template("yt-detail.html",un=un,views=views,subs = subs,videos = videos,labels_views=labels_views,values_views=values_views,labels_videos=labels_videos,values_videos=values_videos,labels_subs=labels_subs,values_subs=values_subs,values_pre=values_pre,values_pre_exp=values_pre_exp,labels_pre=labels_pre)



@app.route("/crawl/yt/<un>")
def crawlyt(un):
	name =un
	key = "AIzaSyCNKbskF4y7yNcVaT-EKqm3Kdac7T6dAv4"
	data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+name+"&key="+key).read()
	details = {
		"date":getCurrentDate(),
		"_id" : json.loads(data)["items"][0]['id'],
		"videos" : json.loads(data)["items"][0]["statistics"]['videoCount'],
		"subs" : json.loads(data)["items"][0]["statistics"]['subscriberCount'],
		"views" : json.loads(data)["items"][0]["statistics"]['viewCount']
	}
	heading = ["date","_id","videos","views","subs"]
	fileName = un+".csv"
	f = open(fileName, "a")
	if fileExists(fileName) == False:
		f.write("Date,Id,videos,subs,views\n")
	row = details['date']+","+details['_id']+","+details['videos']+","+details['subs']+","+details['views']+"\n"
	f.write(row)
	f.close()
	return redirect("/yt-search/"+un)


@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory('templates/css',path)

@app.route('/img/<path:path>')
def send_image(path):
	return send_from_directory('assets',path)

def send_html(path):
	return send_from_directory('templates/',path)

#Other functionss
def getHash(s):
	return md5(s.encode()).hexdigest()

app.run(debug=True, port=3000)


