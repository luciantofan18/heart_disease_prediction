from django.contrib import admin
from .models import Pacient
from .models import Doctor
from .models import ParamConsult
# Register your models here.
admin.site.register(Pacient)
admin.site.register(Doctor)
admin.site.register(ParamConsult)