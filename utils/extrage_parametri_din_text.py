import re

def extrage_parametri_din_text(text):
    rezultat = {}

    # Dicționar cu regex
    regex_parametri = {
        'RestingBP': r'RestingBP\s*:\s*(\d+)',
        'Cholesterol': r'Cholesterol\s*:\s*(\d+(\.\d+)?)',
        'FastingBS': r'FastingBS\s*:\s*(\d+)',
        'MaxHR': r'MaxHR\s*:\s*(\d+)',
        'Oldpeak': r'Oldpeak\s*:\s*(-?\d+(\.\d+)?)',
        'ChestPainType': r'ChestPainType\s*:\s*(ATA|NAP|ASY|TA)',
        'RestingECG': r'RestingECG\s*:\s*(Normal|ST|LVH)',
        'ST_slope': r'ST_slope\s*:\s*(Up|Down|Flat)',
        'ExerciseAngina': r'ExerciseAngina\s*:\s*(Yes|No)'
    }

    for cheie, pattern in regex_parametri.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rezultat[cheie] = match.group(1).capitalize()

    return rezultat
