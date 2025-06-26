# Heart Disease Risk Detection System

Acest proiect reprezintă o aplicație web autonomă dezvoltată pentru detecția timpurie a riscurilor cardiace, adresată medicilor și specialiștilor în domeniul sănătății. Sistemul integrează algoritmi AI pentru a analiza datele medicale ale pacienților și a genera predicții automat, cu notificări trimise medicilor în cazurile de risc ridicat.

## Scopul proiectului

Proiectul urmărește crearea unui suport decizional inteligent pentru personalul medical, automatizând evaluarea riscurilor pe baza analizelor clinice. Prin utilizarea inteligenței artificiale, aplicația contribuie la o medicină preventivă, intervenții timpurii și o mai bună gestionare a pacienților.

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

## Modele AI utilizate

- **Random Forest** (principal): antrenat pe datasetul Heart Failure Prediction de pe Kaggle.
- **Neural Network (MLP)**: rulat manual de medic pentru o verificare suplimentară.

---

## Exemplu flux aplicație

1. Medicul se autentifică și adaugă un pacient.
2. Introduce manual date sau încarcă un PDF.
3. Sistemul extrage datele și rulează predicția.
4. Dacă există risc - email de alertă.
5. Dacă nu - mesaj informativ către pacient.
6. Istoricul este salvat în dashboard.

---

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

##

Lucrare de licență – Universitatea Națională de Știință și Tehnologie POLITEHNICA București, 2025  
Autor: Ionuț Lucian Tofan  
Coordonator: Conf. dr. ing. Radu Hobincu

---


