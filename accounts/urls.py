from django.urls import path

from health_project import settings
from . import views
from .views import login_view, register_view, dashboard_view
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .views import countdown_view
from .views import detalii_predictie

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('adauga-pacient/', views.adauga_pacient, name='adauga_pacient'),
    path('vizualizeaza-pacienti/', views.vizualizeaza_pacienti, name='vizualizeaza_pacienti'),
    path('pacient/<int:pacient_id>/adauga-parametri/', views.adauga_parametri, name='adauga_parametri'),
    path('consultatii/<int:pacient_id>/', views.consultatii_pacient, name='consultatii_pacient'),
    path('delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('pacient/<int:pacient_id>/consultatii/', views.consultatii_pacient, name='consultatii_pacient'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('pacient/<int:pacient_id>/upload-file/', views.upload_file, name='upload_file'),
    path('fisier/<int:fisier_id>/sterge/', views.sterge_fisier, name='sterge_fisier'),
    path("countdown/", countdown_view, name="countdown"),
    path('pacient/<int:pacient_id>/predictie/', detalii_predictie, name='detalii_predictie'),
    path("istoric-model/", views.model_history, name="model_history"),
    path('predictie_nn/<int:pacient_id>/', views.predictie_nn, name='predictie_nn'),

]

