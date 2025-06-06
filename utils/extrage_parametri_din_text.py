import re

def extrage_parametri_din_text (text):
    rezultat = {}

    # Regex pentru valorile numerice
    regex_numeric = {
        'RestingBP': r'RestingBP[^\d]{1,10}(\d+)',
        'Cholesterol': r'Cholesterol[^\d]{1,10}(\d+(\.\d+)?)',
        'FastingBS': r'FastingBS[^\d]{1,10}(\d+)',
        'MaxHR': r'MaxHR[^\d]{1,10}(\d+)',
        'Oldpeak': r'Oldpeak[^\d\-]{1,10}(-?\d+(\.\d+)?)'
    }

    for key, pattern in regex_numeric.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rezultat[key] = match.group(1)

    # Căutare pentru valorile categorice
    st_slope_vals = ['Up', 'Down', 'Flat']
    chest_pain_vals = ['ATA', 'NAP', 'ASY', 'TA']
    ecg_vals = ['Normal', 'ST', 'LVH']
    angina_vals = ['True', 'False']

    def gaseste_choice(valori, nume_camp):
        for val in valori:
            if re.search(rf'\b{val}\b', text, re.IGNORECASE):
                return val
        return None

    rezultat['ST_slope'] = gaseste_choice(st_slope_vals, 'ST_slope')
    rezultat['ChestPainType'] = gaseste_choice(chest_pain_vals, 'ChestPainType')
    rezultat['RestingECG'] = gaseste_choice(ecg_vals, 'RestingECG')
    rezultat['ExerciseAngina'] = gaseste_choice(angina_vals, 'ExerciseAngina')

    return rezultat
