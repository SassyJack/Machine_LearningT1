import pyodbc

# Conexión a la base de datos en Somee
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=MachineLearning.mssql.somee.com;"
    "Database=MachineLearning;"
    "UID=SassyJack_SQLLogin_1;PWD=8p2yantucr;"
)
cursor = conn.cursor()

# Diccionario de imágenes
imagenes = {
    'Regresión Logística': 'imagenes/regresion_logistica.jpg',
    'K-Nearest Neighbors (KNN)': 'imagenes/knn.jpg',
    'Árboles de Decisión': 'imagenes/arbol_decision.jpg',
    'Random Forest': 'imagenes/random_forest.jpg',
    'Support Vector Machine (SVM)': 'imagenes/svm.jpg',
    'Gradient Boosting (XGBoost, AdaBoost)': 'imagenes/gradient_boosting.jpg',
    'Naive Bayes': 'imagenes/naive_bayes.jpg'
}

# Actualizar imágenes en la base de datos
for nombre, ruta in imagenes.items():
    with open(ruta, 'rb') as img_file:
        imagen_binaria = img_file.read()
        cursor.execute("""
            UPDATE Modelo
            SET ContenidoGrafico = ?
            WHERE Nombre = ?
        """, imagen_binaria, nombre)
        print(f"Imagen para '{nombre}' actualizada correctamente.")

conn.commit()
conn.close()
