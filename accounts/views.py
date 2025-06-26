from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Pacient
from .forms import PacientForm
from .models import Doctor
from .forms import RegisterForm
from .forms import ParamConsultForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import ParamConsult
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.core.mail import EmailMessage
import os
from django.conf import settings
from pdfminer.high_level import extract_text
import os
from django.conf import settings
from django.contrib import messages
from utils.extrage_parametri_din_text import extrage_parametri_din_text
from utils.llm_helper import parseaza_valori_llm,consulta_mistral_formatat
from .forms import PacientFileForm
from .models import PacientFile
from utils.text_extraction import extract_text_bun
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # contul trebuie aprobat
            user.save()
            Doctor.objects.create(user=user)

            # salvează documentul
            document = form.cleaned_data['upload_document']
            file_path = f'media/doctor_docs/{user.username}_{document.name}'
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb+') as destination:
                for chunk in document.chunks():
                    destination.write(chunk)

            email = EmailMessage(
                subject='New Doctor Registration Request',
                body=f'Username: {user.username}\nEmail: {user.email}\n\nCheck uploaded document.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['lucian.tofan.56@gmail.com']
            )
            with open(file_path, 'rb') as f:
                email.attach(document.name, f.read(), document.content_type)
            email.send()
            if os.path.exists(file_path):
                os.remove(file_path)
            return render(request, 'accounts/registration_pending.html')

    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    pacienti = Pacient.objects.filter(doctor=request.user)

    cu_risc = pacienti.filter(stare=2).count()
    fara_risc = pacienti.filter(stare=1).count()
    neverificati = pacienti.filter(stare=0).count()

    context = {
        'cu_risc': cu_risc,
        'fara_risc': fara_risc,
        'neverificate': neverificati,
        'total': pacienti.count(),
    }
    return render(request, 'accounts/dashboard.html', context)
@login_required
def adauga_pacient(request):
    if request.method == 'POST':
        form = PacientForm(request.POST)
        if form.is_valid():
            pacient = form.save(commit=False)
            pacient.doctor=request.user
            form.save()
            return redirect('dashboard')
    else:
        form = PacientForm()
    return render(request, 'accounts/adauga_pacient.html', {'form': form})

@login_required
def pacienti_doctor(request):
    pacienti = Pacient.objects.filter(doctor=request.user)
    return render(request, 'pacienti_doctor.html', {'pacienti': pacienti})

def dashboard(request):
    pacienti = Pacient.objects.filter(doctor=request.user)
    return render(request, 'dashboard.html', {'Pacients': pacienti})

from django.db.models import Q
from accounts.models import ParamConsult

@login_required
def vizualizeaza_pacienti(request):
    query = request.GET.get('q')
    pacienti = Pacient.objects.filter(doctor=request.user)

    if query:
        pacienti = pacienti.filter(
            Q(nume__icontains=query) | Q(prenume__icontains=query)
        )

    # Adaugăm un atribut temporar fiecărui pacient: .risc
    for pacient in pacienti:
        consult = ParamConsult.objects.filter(pacient=pacient).order_by('-id').first()
        pacient.risc = consult.Risk if consult else False
        pacient.verified = consult.Verified if consult else False

    return render(request, 'accounts/vizualizeaza_pacienti.html', {
        'Pacients': pacienti,
        'query': query
    })


@login_required
def adauga_parametri(request, pacient_id):
    pacient = get_object_or_404(Pacient, id=pacient_id)
    doctor = None if request.user.is_staff else get_object_or_404(Doctor, user=request.user)
    extracted_data = None  # aici salvăm ce extragem din PDF
    valori_detectate = {}
    if request.method == 'POST':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            file_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)

            # Salvăm fișierul
            with open(file_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            # Extragere text
            try:
                extracted_data = extract_text_bun(file_path)
                extracted_data = '\n'.join([line.strip() for line in extracted_data.splitlines() if line.strip()])
                print(extracted_data)
                messages.success(request, "Fișa medicală a fost procesată cu succes.")
                raspuns_llm = consulta_mistral_formatat(extracted_data)
                valori_detectate = parseaza_valori_llm(raspuns_llm)
                print("VALORI DETECTATE DIN LLM:")
                for k, v in valori_detectate.items():
                    print(f"{k}: {v}")

            except Exception as e:
                messages.error(request, f"Eroare la procesarea fișei: {str(e)}")

            os.remove(file_path)  # ștergem fișierul temporar
            form = ParamConsultForm(initial=valori_detectate)
        else:
            form = ParamConsultForm(request.POST)
            if form.is_valid():
                param = form.save(commit=False)
                param.pacient = pacient
                param.doctor = doctor
                param.age = pacient.age
                param.sex = 1 if pacient.sex == 'M' else 0

                try:
                    ultimul = ParamConsult.objects.filter(pacient=pacient).latest('data')
                except ParamConsult.DoesNotExist:
                    ultimul = None

                campuri = ['ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
                           'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_slope']
                campuri_lipsa = [field for field in campuri if getattr(param, field) in [None, '']]

                if campuri_lipsa and not ultimul:
                    messages.error(request, "Nu există consultații anterioare. Trebuie completate toate câmpurile.")
                    return render(request, 'adauga_parametri.html', {'form': form, 'pacient': pacient})

                if ultimul:
                    for field in campuri:
                        if not getattr(param, field):
                            setattr(param, field, getattr(ultimul, field))

                param.save()
                return redirect('vizualizeaza_pacienti')
    else:
        form = ParamConsultForm()

    return render(request, 'adauga_parametri.html', {
        'form': form,
        'pacient': pacient,
        'extracted_data': extracted_data,
        'valori_detectate': valori_detectate
    })

def consultatii_pacient(request, pacient_id):
    pacient = get_object_or_404(Pacient, id=pacient_id, doctor=request.user)
    consultatii = ParamConsult.objects.filter(pacient=pacient).order_by('-data')
    return render(request, 'accounts/consultatii_pacient.html', {
        'pacient': pacient,
        'consultatii': consultatii
    })

def delete_patient(request, patient_id):
    patient = get_object_or_404(Pacient, pk=patient_id)
    patient.delete()
    return redirect('dashboard')


@login_required
def consultatii_pacient(request, pacient_id):
    pacient = get_object_or_404(Pacient, id=pacient_id)
    consultatii = ParamConsult.objects.filter(pacient=pacient).order_by('data')

    chart_data = {
        "labels": [c.data.strftime("%Y-%m-%d") for c in consultatii],
        "RestingBP": [c.RestingBP for c in consultatii],
        "Cholesterol": [c.Cholesterol for c in consultatii],
        "MaxHR": [c.MaxHR for c in consultatii],
        "FastingBS":[c.FastingBS for c in consultatii],
        "Oldpeak":[c.Oldpeak for c in consultatii],
    }

    context = {
        "pacient": pacient,
        "consultatii": consultatii,
        "chart_data": json.dumps(chart_data, cls=DjangoJSONEncoder),
    }

    return render(request, 'accounts/consultatii_pacient.html', context)

def upload_file(request, pacient_id):
    pacient = get_object_or_404(Pacient, id=pacient_id)
    fisiere = PacientFile.objects.filter(pacient=pacient).order_by('-uploaded_at')

    if request.method == 'POST':
        form = PacientFileForm(request.POST, request.FILES)
        if form.is_valid():
            fisiere_pacient = form.save(commit=False)
            fisiere_pacient.pacient = pacient
            fisiere_pacient.save()
            return redirect('upload_file', pacient_id=pacient.id)
    else:
        form = PacientFileForm()

    return render(request, 'accounts/upload_file.html', {
        'form': form,
        'pacient': pacient,
        'fisiere': fisiere
    })

def sterge_fisier(request, fisier_id):
    fisier = get_object_or_404(PacientFile, id=fisier_id)
    pacient_id = fisier.pacient.id

    fisier.uploaded_file.delete()

    fisier.delete()

    messages.success(request, "Fișierul a fost șters cu succes.")
    return redirect('upload_file', pacient_id=pacient_id)

from django.http import JsonResponse
from datetime import datetime, timedelta

def countdown_view(request):
    try:
        with open("last_run.txt", "r") as f:
            last_run = datetime.fromisoformat(f.read().strip())
    except FileNotFoundError:
        last_run = datetime.now()

    return JsonResponse({
        "last_run": last_run.isoformat()
    })


from .models import PredictieFinala

def detalii_predictie(request, pacient_id):
    pacient = get_object_or_404(Pacient, id=pacient_id)
    predictie = PredictieFinala.objects.filter(pacient=pacient).order_by('-data').first()

    context = {
        'pacient': pacient,
        'predictie': predictie,
    }
    return render(request, 'accounts/detalii_predictie.html', context)

from django.shortcuts import render

def model_history(request):
    return render(request, 'accounts/model_rf_history.html')


from django.shortcuts import render, get_object_or_404
from accounts.models import Pacient, ParamConsult
from utils.predictie_nn import predict_with_neural_net
from django.contrib.auth.decorators import login_required

@login_required
def predictie_nn(request, pacient_id):
    pacient = get_object_or_404(Pacient, id=pacient_id)
    consultatie = ParamConsult.objects.filter(pacient=pacient).order_by('-data').first()

    if not consultatie:
        return render(request, 'accounts/predictie_nn.html', {
            'eroare': "Nu există consultații pentru acest pacient."
        })

    try:
        rezultat_nn, scor = predict_with_neural_net(consultatie)

        rezultat_text = "Cu risc" if rezultat_nn == 1 else "Fără risc"
        scor_procente = scor * 100

        return render(request, 'accounts/predictie_nn.html', {
            'pacient': pacient,
            'rezultat': rezultat_text,
            'scor': scor_procente,
        })
    except Exception as e:
        return render(request, 'accounts/predictie_nn.html', {
            'eroare': f"Eroare la rularea rețelei neuronale: {str(e)}"
        })
