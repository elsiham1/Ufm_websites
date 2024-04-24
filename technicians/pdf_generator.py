import os
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from .models import Task

def generate_pdf_report(tasks):
    # Chemin de sauvegarde du fichier PDF
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, "rapport.pdf")

    # Définition des styles de paragraphe et de tableau
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    body_style = styles["BodyText"]

    # Création du document PDF avec reportlab
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    elements = []

    # Ajout du titre
    elements.append(Paragraph("Rapport de Tâches", title_style))
    elements.append(Paragraph("<br/><br/>", body_style))  # Saut de ligne

    # Création des données du tableau
    table_data = [["Start-time", "Date", "Description", "Technician Name", "Location", "Equipment/Lot"]]

    for task in tasks:
        table_data.append([
            str(task.start_time),
            str(task.date),
            task.description,
            task.technician_name,
            task.location,
            task.equipment_lot
        ])

    # Création et configuration du tableau
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (65/255, 105/255, 225/255)),  # Couleur de fond de l'en-tête
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Couleur du texte de l'en-tête
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Alignement du texte
        ('INNERGRID', (0, 0), (-1, -1), 0.25, (0, 0, 0)),  # Lignes de la grille intérieure
        ('BOX', (0, 0), (-1, -1), 0.25, (0, 0, 0)),  # Bordure
    ]))

    elements.append(table)
    doc.build(elements)

    return pdf_file_path

def download_pdf_report(request):
    try:
        # Récupérer toutes les tâches depuis la base de données
        tasks = Task.objects.all()

        # Générer le rapport PDF
        pdf_file_path = generate_pdf_report(tasks)

        # Lire le fichier PDF en tant que réponse HTTP
        with open(pdf_file_path, "rb") as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'
            return response

    except Exception as e:
        return HttpResponse(f"Erreur lors de la génération du PDF : {str(e)}", status=500)

    finally:
        # Supprimer le fichier PDF après l'avoir servi
        if os.path.exists(pdf_file_path):
            os.remove(pdf_file_path)
