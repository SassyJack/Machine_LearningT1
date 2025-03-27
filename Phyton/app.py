import datetime
import re
from flask import Flask, render_template, request
import RegresionLin

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello world"

@app.route("/hello/<name>")
def hello(name):
    now = datetime.datetime.now()

    match_object = re.match(r"([a-zA-Z]+)", name)
    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "friend"

    content = f"Hello there {clean_name}! Hour: {now}"

    return content

@app.route("/exampleHTML/")
def exampleHTML():
    return render_template("example.html")

@app.route("/RegresionLin/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == 'POST':
        investment = float(request.form['investment'])
        prediction = RegresionLin.calculate_prediction(investment) 
    plot_url = RegresionLin.generate_plot()
    return render_template('RegresionLin.html', prediction=prediction, plot_url=plot_url)

@app.route("/RegresionLog/")
def RegresionLog():
    return render_template("RegresionLog.html")

