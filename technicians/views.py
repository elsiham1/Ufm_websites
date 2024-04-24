# technicians/views.py
from django.shortcuts import render, redirect
from .form import TaskForm
from .models import Task

# views.py

from django.shortcuts import render, redirect
from .models import Task
from .form import TaskForm

def task_form(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('monthly_reports')  # Redirect to monthly reports page
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

def monthly_reports(request):
    tasks = Task.objects.all()  # Retrieve all tasks from the database
    return render(request, 'monthly_reports.html', {'tasks': tasks})
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Task

import csv
from django.http import HttpResponse
from .models import Task

def download_monthly_report_csv(request):
    # Fetch monthly report data (e.g., tasks)
    tasks = Task.objects.all()

    # Prepare CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="monthly_report.csv"'

    # Define CSV writer
    writer = csv.writer(response)
    
    # Write CSV header
    writer.writerow(['Description', 'Date', 'Technician Name', 'Location','start time'])

    # Write CSV rows
    for task in tasks:
        writer.writerow([task.description, task.date, task.technician_name, task.location,task.start_time])

    return response
# views.py
import os
from django.http import HttpResponse
from django.conf import settings
from .models import Task
from .pdf_generator import generate_pdf_report

def download_pdf_report(request):
    try:
        # Retrieve tasks from the database
        tasks = Task.objects.all()

        # Generate the PDF report
        pdf_file_path = generate_pdf_report(tasks)

        # Serve the generated PDF file as a download
        with open(pdf_file_path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'
            return response

    except Task.DoesNotExist:
        return HttpResponse("No tasks found.", status=404)

    except Exception as e:
        return HttpResponse(f"Error generating or serving PDF: {str(e)}", status=500)

    finally:
        # Clean up: Remove the generated PDF file after serving
        if pdf_file_path and os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
from django.shortcuts import render

def menu_view(request):
    return render(request, 'menu.html')
