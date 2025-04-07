from sqlalchemy import create_engine, text

# Formato de conexión con pytds
DATABASE_URL = "mssql+pytds://SassyJack_SQLLogin_1:8p2yantucr@MachineLearning.mssql.somee.com/MachineLearning"

engine = create_engine(DATABASE_URL)

def obtener_modelos():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT Id, Nombre, Descripcion, FuenteInformacion, ContenidoGrafico FROM dbo.Modelo"))
        modelos = result.mappings().all()  # Convierte filas a diccionarios
        return modelos

def obtener_modelo_por_id(modelo_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT Id, Nombre, Descripcion, FuenteInformacion, ContenidoGrafico FROM dbo.Modelo WHERE Id = :id"),
            {"id": modelo_id}
        )
        modelo = result.mappings().first()  # Devuelve una sola fila como dict-like
        return dict(modelo) if modelo else None
