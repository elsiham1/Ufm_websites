from django.db import models

class Task(models.Model):
    start_time = models.TimeField()
    description = models.TextField()
    equipment_lot = models.CharField(max_length=100)
    technician_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"Task #{self.id} - {self.description}"

    class Meta:
        app_label = 'technicians'  # Specify the app_label for this model
