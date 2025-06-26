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
from accounts.models import PredictieFinala
from utils.formatari import formateaza_caracteristici


model = joblib.load('prediction_models/random_forest_model.joblib')
Consultatii = ParamConsult.objects.filter(Verified=False)

for consultatie in Consultatii:
    data = pd.DataFrame([{
        'Age': consultatie.age,
        'Sex':  consultatie.sex,
        'RestingBP':1 if (consultatie.RestingBP>120) else 0,
        'Cholesterol': consultatie.Cholesterol,
        'FastingBS': consultatie.FastingBS,
        'MaxHR': consultatie.MaxHR,
        'ExerciseAngina': 1 if consultatie.ExerciseAngina == 'True' else 0,
        'Oldpeak': consultatie.Oldpeak,
        'ChestPainType_ASY': 1 if consultatie.ChestPainType == 'ASY' else 0,
        'ChestPainType_ATA': 1 if consultatie.ChestPainType == 'ATA' else 0,
        'RestingECG_LVH': 1 if consultatie.RestingECG == 'Left Ventricular Hypertrophy' else 0,
        'RestingECG_Normal': 1 if consultatie.RestingECG == 'Normal' else 0,
        'RestingECG_ST': 1 if consultatie.RestingECG == 'ST-T Wave Abnormality' else 0,
        'ST_Slope_Flat': 1 if consultatie.ST_slope == 'Flat' else 0,
        'ST_Slope_Up': 1 if consultatie.ST_slope == 'Up' else 0,
    }])

    X_np = data.values
    pred = model.predict(data)

    proba = model.predict_proba(data)[0]
    votes = [tree.predict(X_np)[0] for tree in model.estimators_]
    vote_percentage = votes.count(pred[0]) / len(votes) * 100
    importances = model.feature_importances_
    feature_names = list(data.columns)

    predictie, _ = PredictieFinala.objects.update_or_create(
        pacient=consultatie.pacient,
        defaults={
            "rezultat": "risc" if pred[0] == 1 else "fara risc",
            "probabilitate_risc": float(proba[1]) * 100,
            "probabilitate_nu_risc": float(proba[0]) * 100,
            "procent_voturi": vote_percentage,
            "caracteristici_folosite": formateaza_caracteristici(data.iloc[0]),
            "importanta_caracteristici": {
                name: float(val) * 100 for name, val in zip(feature_names, importances)
            },
        }
    )


    consultatie.Risk = True if pred[0] == 1 else False
    if consultatie.Risk:
        consultatie.pacient.stare = 2

        subject = f"[Alertă AI] Risc detectat pentru pacientul {consultatie.pacient.nume} {consultatie.pacient.prenume}"
        message = (
            f"Stimate medic,\n\n"
            f"Modelul AI a identificat un risc crescut pentru pacientul {consultatie.pacient}.\n\n"
            f"Detalii predicție:\n"
            f" - Probabilitate risc: {predictie.probabilitate_risc:.1f}%\n"
            f" - Voturi obținute de model pentru a sustine decizia: {predictie.procent_voturi:.1f}%\n\n"
            f"Puteți consulta explicația completă a deciziei în platformă.\n"
            f"Vă recomandăm revizuirea dosarului medical cât mai curând.\n\n"
            f"\n"
            f"Sistemul autonom de detecție a bolilor cardiovasculare"
        )

        send_alert_email(
            [consultatie.doctor.user.email, "lucian.tofan.56@gmail.com"],
            subject,
            message
        )

    else:
        consultatie.pacient.stare = 1

        subject = f"[Evaluare AI] Pacientul {consultatie.pacient.nume} {consultatie.pacient.prenume} nu prezintă risc"
        message = (
            f"Stimate pacient,\n\n"
            f"A fost efectuată o evaluare periodică automată folosind sistemul AI.\n"
            f"Rezultatul obținut indică un risc scăzut de afecțiuni cardiovasculare.\n\n"
            f"Detalii predicție:\n"
            f" - Probabilitate risc: {predictie.probabilitate_risc:.1f}%\n"
            f" - Voturi obținute de model pentru a sustine decizia: {predictie.procent_voturi:.1f}%\n\n"
            f"Vă rugăm să continuați monitorizarea stării de sănătate conform recomandărilor medicului .\n\n"
            f"Sistem autonom de detecție a bolilor cardiovasculare"
        )

        send_alert_email(
            [consultatie.pacient.email, "lucian.tofan.56@gmail.com"],
            subject,
            message
        )
    consultatie.Verified = True
    consultatie.pacient.save()
    consultatie.save()
del model
gc.collect()