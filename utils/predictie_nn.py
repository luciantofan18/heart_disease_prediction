import numpy as np
import os
import pickle
from tensorflow.keras.models import load_model

# Încarcă modelul Keras
MODEL_PATH = os.path.join('prediction_models', 'model_complex_NN.keras')
neural_net_model = load_model(MODEL_PATH)

# Încarcă scalerul
SCALER_PATH = os.path.join('prediction_models', 'scaler1.pkl')
with open(SCALER_PATH, 'rb') as f:
    scaler = pickle.load(f)

def predict_with_neural_net(consult):
    raw_input = np.array([[
        consult.age,
        consult.sex,
        consult.RestingBP,
        consult.Cholesterol,
        1 if consult.FastingBS > 120 else 0,
        consult.MaxHR,
        1 if consult.ExerciseAngina == 'True' else 0,
        consult.Oldpeak,
        1 if consult.ChestPainType == 'ASY' else 0,
        1 if consult.ChestPainType == 'ATA' else 0,
        1 if consult.RestingECG == 'LVH' else 0,
        1 if consult.RestingECG == 'Normal' else 0,
        1 if consult.RestingECG == 'ST' else 0,
        1 if consult.ST_slope == 'Flat' else 0,
        1 if consult.ST_slope == 'Up' else 0,
    ]], dtype=np.float32)

    scaled_input = scaler.transform(raw_input)
    rezultat = neural_net_model.predict(scaled_input)
    scor = rezultat[0][0]
    return int(scor > 0.4), scor

