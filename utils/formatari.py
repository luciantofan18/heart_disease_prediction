def formateaza_caracteristici(data_row):
    print(data_row)
    caracteristici = {
        "Vârstă": int(data_row["Age"]),
        "Sex": "Masculin" if data_row["Sex"] == 1 else "Feminin",
        "Tensiune arterială (RestingBP)": int(data_row["RestingBP"]),
        "Colesterol": round(float(data_row["Cholesterol"]), 2),
        "Glicemie (FastingBS)": int(data_row["FastingBS"]),
        "Puls maxim (MaxHR)": int(data_row["MaxHR"]),
        "Oldpeak": round(float(data_row["Oldpeak"]), 2),
        "Angină la efort": "Da" if data_row["ExerciseAngina"] == 1 else "Nu"
    }

    # Tip durere toracică
    if data_row.get("ChestPainType_ASY") == 1:
        caracteristici["Tip durere toracică"] = "ASY"
    elif data_row.get("ChestPainType_ATA") == 1:
        caracteristici["Tip durere toracică"] = "ATA"
    else:
        caracteristici["Tip durere toracică"] = "TA sau NAP - nu ne interesează"

    # ECG în repaus
    if data_row.get("RestingECG_LVH") == 1:
        caracteristici["ECG în repaus"] = "LVH"
    elif data_row.get("RestingECG_Normal") == 1:
        caracteristici["ECG în repaus"] = "Normal"
    elif data_row.get("RestingECG_ST") == 1:
        caracteristici["ECG în repaus"] = "ST-T"


    # Panta ST
    if data_row.get("ST_Slope_Flat") == 1:
        caracteristici["Panta ST"] = "Flat"
    elif data_row.get("ST_Slope_Up") == 1:
        caracteristici["Panta ST"] = "Up"
    else:
        caracteristici["Panta ST"] = "Down - ignorat"

    return caracteristici
