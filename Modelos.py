import pyodbc

# Configura la cadena de conexión a SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=MachineLearning.mssql.somee.com;"
    "DATABASE=MachineLearning;"
    "UID=SassyJack_SQLLogin_1;"
    "PWD=8p2yantucr;"  # Reemplaza con tu contraseña real
)

def obtener_modelos():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT id, Nombre FROM dbo.Modelo")  # ← Cambio aquí
    modelos = cursor.fetchall()
    conn.close()
    return [(fila.id, fila.Nombre) for fila in modelos]

def obtener_modelo_por_id(modelo_id):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, Nombre, Descripcion, FuenteInformacion, ContenidoGrafico FROM dbo.Modelo WHERE id = ?",
        (modelo_id,)
    )
    fila = cursor.fetchone()
    conn.close()
    if fila:
        return {
            'id': fila.id,
            'nombre': fila.Nombre,
            'descripcion': fila.Descripcion,
            'fuente': fila.FuenteInformacion,
            'imagen_url': fila.ContenidoGrafico
        }
    return None

