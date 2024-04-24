# technicians/urls.py
from django.urls import path
from . import views

urlpatterns = [
   path('', views.menu_view, name='menu'),
    path('task-form/', views.task_form, name='task_form'),
    path('monthly-reports/', views.monthly_reports, name='monthly_reports'),
     path('download-csv/', views.download_monthly_report_csv, name='download_csv'),
     path('download-pdf/', views.download_pdf_report, name='download_pdf'),


]
