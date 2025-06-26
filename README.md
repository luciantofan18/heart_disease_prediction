# Heart Disease Risk Detection System

Acest proiect reprezintă o aplicație web autonomă dezvoltată pentru detecția timpurie a riscurilor cardiace, adresată medicilor și specialiștilor în domeniul sănătății. Sistemul integrează algoritmi AI pentru a analiza datele medicale ale pacienților și a genera predicții automat, cu notificări trimise medicilor în cazurile de risc ridicat.

## Scopul proiectului

Acest proiect reprezintă o aplicație web autonomă destinată detecției timpurii a riscurilor cardiovasculare. Sistemul este conceput pentru a sprijini cadrele medicale prin analiză automată a datelor clinice și generarea de predicții bazate pe inteligență artificială. În cazurile în care este detectat un risc major, medicii sunt notificați automat prin email.
---

##  Tehnologii utilizate

- **Python 3.10**
- **Django 5.2**
- **HTML5 & CSS3** – pentru interfața web (fără framework-uri externe)
- **Scikit-learn** – model Random Forest
- **TensorFlow / Keras** – rețea neuronală de tip MLP
- **PyMuPDF** – extragerea textului din PDF-uri
- **Ollama + Mistral (LLM local)** – interpretarea inteligentă a fișierelor medicale
- **SQLite** – baza de date
- **Email Backend Django** – notificări automate

---

## Structură aplicație

- `accounts/` – modele, formulare, logica de utilizator și consultații
- `utils/` – conține:
  - `predictions.py` – rularea automată a predicțiilor Random Forest
  - `predictie_nn.py` – rulare manuală rețea neuronală
  - `email_alert.py` – trimitere notificări pe email
  - `text_extraction.py` – extragerea textului din PDF
  - `llm_helper.py` – interfață cu modelul Mistral
- `templates/` – pagini HTML
- `static/` – fișiere CSS
- `scheduler.py` – thread care rulează predicțiile la fiecare 2 minute
## 📓 Notebook disponibil

- [`Copy_of_Preprocesare_date_selectare_model(2).ipynb`](notebook/Copy_of_Preprocesare_date_selectare_model(2).ipynb):  
  Acest notebook conține întregul pipeline AI/ML: preprocesarea datelor, selecția trăsăturilor, antrenarea și compararea modelelor Random Forest, Support Vector Classifier și rețele neuronale.  
  Este util pentru reproducerea experimentelor și înțelegerea logicii din spatele modelului integrat în aplicația web.

---

##  Funcționalități

- Autentificare/înregistrare conturi de medici (cu validare manuală)
- Adăugare pacienți și parametri clinici
- Încărcare fișiere PDF cu analize medicale
- Extragere automată a valorilor medicale din PDF și interpretare cu LLM
- Rulare automată a modelului Random Forest
- Rulare opțională a unei rețele neuronale pentru verificare suplimentară
- Trimitere automată a emailurilor de alertă către medici/pacienți
- Dashboard cu vizualizare starea pacienților

---

## Mecanism de predicție periodică

Aplicația lansează la fiecare 2 minute un thread (`scheduler.py`) care:
1. Verifică pacienții neverificați.
2. Rulează `predictions.py` pentru a genera o predicție AI.
3. Marchează pacienții ca verificați.
4. Trimite automat email de alertă dacă se detectează risc crescut.

---

Aplicația integrează un pipeline AI complet:

Random Forest
Model principal, antrenat pe datasetul Heart Failure Prediction (Kaggle), oferă predicții automate la fiecare 2 minute pentru toți pacienții noi.

SVM (Support Vector Machine)
Model folosit pentru comparație în analiza offline, evaluat în faza de testare a performanței.

Rețea neuronală (MLP)
Model de tip Multi-Layer Perceptron, rulat manual pentru a oferi o a doua opinie AI în cadrul platformei.
---

Pentru interpretarea automată a analizelor medicale încărcate în format PDF, aplicația folosește modelul Mistral (rulat local prin Ollama). Acesta:

Primește textul extras din PDF prin PyMuPDF;

Recunoaște valorile medicale relevante (colesterol, tensiune, glicemie etc.) folosind înțelegerea contextuală;

Returnează un dicționar cu parametrii extrași, care sunt integrați automat în formularul pacientului;

Permite completarea rapidă și fără erori umane a datelor clinice.


## Exemplu flux aplicație

1. Medicul se autentifică și adaugă un pacient.
2. Introduce manual date sau încarcă un PDF.
3. Sistemul extrage datele și rulează predicția.
4. Dacă există risc - email de alertă.
5. Dacă nu - mesaj informativ către pacient.
6. Istoricul este salvat în dashboard.

---
## Mecanism de rulare automată
Scriptul scheduler.py pornește un thread care la fiecare 2 minute:
Găsește pacienții neverificați;
Rulează predictions.py (model Random Forest);
Salvează scorul și marcarea;
Trimite email dacă scorul depășește pragul.


## Testare

Aplicația a fost testată cu:
- Introducere manuală a datelor
- Încărcare PDF-uri cu formate variate
- Validare comportament în caz de predicții multiple
- Verificare emailuri automate și flux asincron

---

## Securitate și confidențialitate

- Acces restricționat pe bază de rol
- Validare manuală conturi de medic
- Datele sensibile nu se salvează local (ex: documentele de validare)
- Sistem de logare și logout sigur
- Interfață minimalistă, adaptată uzului medical

---
Limitări actuale
PDF-uri foarte neclare sau scanate slab pot da erori la extragerea textului
Modelul LLM este generalist, nu specializat pe medicină
Datele de antrenare sunt limitate la seturi publice, nu din spitale locale
Sistemul nu este certificat pentru uz clinic real – este un demo academic
##
## Considerații etice
Proiectul nu înlocuiește diagnosticul medical. AI-ul este folosit strict ca asistent pentru triere și alertare rapidă. Toate deciziile finale trebuie luate de către personal calificat. Datele sensibile sunt procesate local, fără expunere online.


## Lucrare de licență 
Universitatea Națională de Știință și Tehnologie POLITEHNICA București, 2025  
Autor: Ionuț Lucian Tofan  
Coordonator: Conf. dr. ing. Radu Hobincu

---
