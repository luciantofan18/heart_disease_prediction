from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.serializers.json import DjangoJSONEncoder
import json



class Pacient(models.Model):
    SEX_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Feminin')
    ]

    nume = models.CharField(max_length=100)
    prenume = models.CharField(max_length=100)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    email = models.EmailField()
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    stare = models.IntegerField( default=0)
    @property
    def age(self):
        today = date.today()
        return (today.year - self.birth_date.year) - ((self.birth_date.month, self.birth_date.day)>(today.month, today.day))


    def __str__(self):
        return f"{self.nume} {self.prenume}"


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ParamConsult(models.Model):
    ST_slope_choices = [
        ('Up', 'Up'),
        ('Down', 'Down'),
        ('Flat', 'Flat')
    ]

    ChestPainType_choices = [
        ('TA', 'Typical Angina'),
        ('NAP', 'Non-Anginal Pain'),
        ('ASY', 'Asymptomatic'),
        ('ATA', 'Atypical Angina')
    ]

    RestingECG_choices = [
        ('Normal', 'Normal'),
        ('ST', 'ST-T wave abnormality'),
        ('LVH', 'Left Ventricular Hypertrophy')
    ]

    ExerciseAngina_choices = [
        ('True', 'Yes'),
        ('False', 'No')
    ]

    pacient=models.ForeignKey(Pacient, on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    age=models.IntegerField()
    sex=models.IntegerField()
    ChestPainType = models.CharField(max_length=3, choices=ChestPainType_choices)
    RestingBP=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    Cholesterol=models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(600)])
    FastingBS=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(250)])
    RestingECG = models.CharField(max_length=10, choices=RestingECG_choices)
    MaxHR=models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(250)])
    ExerciseAngina = models.CharField(max_length=5, choices=ExerciseAngina_choices)
    Oldpeak=models.FloatField(validators=[MinValueValidator(-4.0), MaxValueValidator(7.0)])
    ST_slope=models.CharField(max_length=5,choices=ST_slope_choices)
    data=models.DateField(auto_now_add=True)
    Verified=models.BooleanField(default=False)
    Risk=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.age = self.pacient.age
        self.sex = 1 if self.pacient.sex == 'M' else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consultatia lui {self.pacient.nume} {self.pacient.prenume} - data {self.data}"

class PacientFile(models.Model):
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE, related_name="fisiere")
    uploaded_file = models.FileField(upload_to='fisiere_pacienti/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fișier pentru {self.pacient.nume} - {self.uploaded_file.name}"


class PredictieFinala(models.Model):
    pacient = models.OneToOneField(Pacient, on_delete=models.CASCADE)
    rezultat = models.CharField(max_length=10)  # 'risc' / 'fara risc'
    probabilitate_risc = models.FloatField()
    probabilitate_nu_risc = models.FloatField()
    procent_voturi = models.FloatField()
    data = models.DateTimeField(auto_now=True)

    caracteristici_folosite = models.JSONField()
    importanta_caracteristici = models.JSONField()
