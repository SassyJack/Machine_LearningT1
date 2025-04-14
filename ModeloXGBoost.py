import os
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

# Entrenamiento del modelo (esto puede ejecutarse una vez)
def entrenar_modelo():
    df = pd.read_excel("dataset_diabetes.xlsx")
    X = df[['glucosa', 'edad', 'IMC']]
    y = df['resultado']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    model.fit(X_scaled, y)

    joblib.dump(model, 'modelo_xgboost.pkl')
    joblib.dump(scaler, 'scaler_xgboost.pkl')
    
def cargar_modelo():
    base_dir = os.path.dirname(__file__)  # directorio donde está este script
    modelo_path = os.path.join(base_dir, 'modelo_xgboost.pkl')
    scaler_path = os.path.join(base_dir, 'scaler_xgboost.pkl')
    
    model = joblib.load(modelo_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def procesar_excel(file):
    df = pd.read_excel(file)
    return df[['glucosa', 'edad', 'IMC']], df  # X y dataframe original
