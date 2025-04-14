# entrenar_modelo.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

# Cargar tu dataset
df = pd.read_csv(r"D:\UNIVERSIDAD\TRABAJOS U\6 SEMESTRE\MACHINE LEARNING I\Machine_LearningT1\diabetes.csv", sep=';')


# Separar características y variable objetivo
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Entrenar el modelo
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
model.fit(X_scaled, y)

# Guardar el modelo y el scaler
joblib.dump(model, 'modelo_xgboost.pkl')
joblib.dump(scaler, 'scaler_xgboost.pkl')

print("✅ Modelo y scaler guardados correctamente.")
