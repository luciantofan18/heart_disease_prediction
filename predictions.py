import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_project.settings')

import django
django.setup()
import gc
import joblib
import pandas as pd
from accounts.models import ParamConsult
from utils.email_alert import send_alert_email
from accounts.models import Doctor,Pacient
model = joblib.load('prediction_models/random_forest_model.joblib')
Consultatii = ParamConsult.objects.filter(Verified=False)

for consultatie in Consultatii:
    data = pd.DataFrame([{
        'Age': consultatie.age,
        'Sex':  consultatie.sex,
        'RestingBP': consultatie.RestingBP,
        'Cholesterol': consultatie.Cholesterol,
        'FastingBS': consultatie.FastingBS,
        'MaxHR': consultatie.MaxHR,
        'ExerciseAngina': 1 if consultatie.ExerciseAngina == 'True' else 0,
        'Oldpeak': consultatie.Oldpeak,
        'ChestPainType_ASY': 1 if consultatie.ChestPainType == 'Asymptomatic' else 0,
        'ChestPainType_ATA': 1 if consultatie.ChestPainType == 'Atypical Angina' else 0,
        'RestingECG_LVH': 1 if consultatie.RestingECG == 'Left Ventricular Hypertrophy' else 0,
        'RestingECG_Normal': 1 if consultatie.RestingECG == 'Normal' else 0,
        'RestingECG_ST': 1 if consultatie.RestingECG == 'ST-T Wave Abnormality' else 0,
        'ST_Slope_Flat': 1 if consultatie.ST_slope == 'Flat' else 0,
        'ST_Slope_Up': 1 if consultatie.ST_slope == 'Up' else 0,
    }])

    pred = model.predict(data)


    #print(pred)
    consultatie.Risk = True if pred[0] == 1 else False
    if consultatie.Risk:
        subject = "Alertă: pacient cu risc detectat"
        message = f"Pacientul {consultatie.pacient} a fost identificat cu risc crescut. Verificați dosarul medical în platformă."
        send_alert_email([consultatie.pacient.email,"lucian.tofan.56@gmail.com"], subject, message)
    else:
        subject = "Verificare Periodica Efectuata"
        message = f"Pacientul {consultatie.pacient} a fost rulat prin modelul de detectie, iar riscul de boala este scazut."
        send_alert_email([consultatie.pacient.email, "lucian.tofan.56@gmail.com"], subject, message)
    consultatie.Verified = True

    consultatie.save()
del model
gc.collect()