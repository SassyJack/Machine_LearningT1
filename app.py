import datetime
from pyexpat import model
import re
from flask import Flask, render_template, request
import numpy as np
import RegresionLin
import RegresionLog
import Modelos
from Modelos import obtener_modelo_por_id, obtener_modelos
from RegresionLog import generate_plot, scaler


app = Flask(__name__)

@app.route('/')
def index():
    modelos = obtener_modelos()
    return render_template('index.html', modelos=modelos)


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
def RegresionLin():
    prediction = None
    if request.method == 'POST':
        investment = float(request.form['investment'])
        prediction = RegresionLin.calculate_prediction(investment) 
    plot_url = RegresionLin.generate_plot()
    return render_template('RegresionLin.html', prediction=prediction, plot_url=plot_url)

@app.route("/RegresionLogHTML/")
def RegresionLog():
    return render_template("RegresionLog.html")

@app.route("/RegresionLog/", methods=["GET", "POST"])
def RegresionLog2():
    prediction = None
    plot_url = generate_plot()
    
    if request.method == 'POST':
        try:
            historial_compras = float(request.form['historial_compras'])
            frecuencia = float(request.form['frecuencia'])
            gasto_promedio = float(request.form['gasto_promedio'])
            
            user_data = np.array([[historial_compras, frecuencia, gasto_promedio]])
            user_data_scaled = scaler.transform(user_data)
            prediction = model.predict(user_data_scaled)[0]
        except Exception as e:
            prediction = f"Error en la predicción: {e}"
    
    return render_template('RegresionLogEj.html', prediction=prediction, plot_url=plot_url)


@app.route('/Modelos/<int:modelo_id>')
def modelo(modelo_id):
    modelo = obtener_modelo_por_id(modelo_id)
    modelos = obtener_modelos()  # Para que aparezcan en el nav
    if modelo:
        return render_template('modelo.html', modelo=modelo, modelos=modelos)
    else:
        return "Modelo no encontrado", 404

