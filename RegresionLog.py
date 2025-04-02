import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix

# Generación del dataset
np.random.seed(42)
n_samples = 1000
historial_compras = np.random.randint(0, 100, n_samples)
frecuencia = np.random.randint(1, 30, n_samples)
gasto_promedio = np.random.uniform(5, 500, n_samples)
abandono = np.where((historial_compras < 20) & (frecuencia < 5) & (gasto_promedio < 50), 1, 0)

df = pd.DataFrame({
    'historial_compras': historial_compras,
    'frecuencia': frecuencia,
    'gasto_promedio': gasto_promedio,
    'abandono': abandono
})

# División en conjunto de entrenamiento y prueba
X = df[['historial_compras', 'frecuencia', 'gasto_promedio']]
y = df['abandono']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Escalado de los datos
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Ajuste del modelo de Regresión Logística
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Evaluación del modelo
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

def generate_plot():
    plt.figure(figsize=(5, 4))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['No Abandona', 'Abandona'], 
                yticklabels=['No Abandona', 'Abandona'])
    plt.xlabel('Predicción')
    plt.ylabel('Real')
    plt.title('Matriz de Confusión')
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    return plot_url 