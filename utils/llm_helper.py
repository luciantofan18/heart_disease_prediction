import requests

def consulta_mistral_formatat(text_pdf):
    prompt = f"""
    You have received a medical report. Please extract the following medical parameters if they appear in the text and return them exactly in the following format, without using measuring units:

    ChestPainType:<value> , RestingBP:<value> , Cholesterol:<value> , FastingBS:<value> , RestingECG:<value> , MaxHR:<value> , ExerciseAngina:<value> , Oldpeak:<value> , ST_slope:<value>

     Rules:
    - If a parameter is missing from the report, write `None`.
    - Do not add any extra explanations.
    - The possible values for categorical fields are:
      • ChestPainType: ASY, NAP, ATA, TA  
      • RestingECG: Normal, ST, LVH  
      • ExerciseAngina: True, False
      • ST_slope: Up, Flat, Down

    To help you identify them, here is what the categorical fields mean:
    ASY = Asymptomatic, NAP = Non-Anginal Pain, ATA = Atypical Angina, TA = Typical Angina.  
    LVH = Left Ventricular Hypertrophy  
    Yes = true, No = false.

    The content of the medical report is:
    {text_pdf}
    """.strip()
    url = 'http://localhost:11434/api/generate'
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.RequestException as e:
        return f"Eroare la model: {e}"


def parseaza_valori_llm(raspuns):
    valori = {}
    perechi = raspuns.split(',')
    for pereche in perechi:
        if ':' in pereche:
            cheie, valoare = pereche.strip().split(':', 1)
            valori[cheie.strip()] = None if valoare.strip().lower() == 'none' else valoare.strip()
    return valori
