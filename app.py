import datetime
from pyexpat import model
import re
from flask import Flask, render_template, request
import numpy as np
from RegresionLin import generate_plot, calculate_prediction
import RegresionLog
import Modelos
from Modelos import obtener_modelo_por_id, obtener_modelos
from RegresionLog import generate_plot, scaler
from ModeloXGBoost import cargar_modelo, procesar_excel
import os
from werkzeug.utils import secure_filename
from flask import send_file


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    plot_url = generate_plot()
    prediction = None
    if request.method == 'POST':
        investment = float(request.form['investment'])
        prediction = RegresionLin.calculate_prediction(investment) 
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


@app.route("/PrediccionDiabetes/", methods=["GET", "POST"])
def prediccion_diabetes():
    datos = None
    predicciones = None
    if request.method == 'POST':
        file = request.files['archivo']
        if file and file.filename.endswith(('.xls', '.xlsx')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            X, df_original = procesar_excel(filepath)
            model, scaler = cargar_modelo()

            X_scaled = scaler.transform(X)
            y_pred = model.predict(X_scaled)

            df_original['prediccion'] = y_pred
            datos = df_original.to_dict(orient='records')

            # Guardar el DataFrame a Excel y CSV
            df_original.to_excel(os.path.join(app.config['UPLOAD_FOLDER'], 'resultados_prediccion.xlsx'), index=False)
            df_original.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'resultados_prediccion.csv'), index=False)

    return render_template("prediccion_diabetes.html", datos=datos)

@app.route('/descargar_excel/')
def descargar_excel():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'resultados_prediccion.xlsx')
    return send_file(filepath, as_attachment=True)

@app.route('/descargar_csv/')
def descargar_csv():
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'resultados_prediccion.csv')
    return send_file(filepath, as_attachment=True)