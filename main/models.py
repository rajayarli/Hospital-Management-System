
from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import MaxLengthValidator

class SafeMultiSelectField(MultiSelectField):
    def __init__(self, *args, **kwargs):
        # Calculate maximum possible length if not provided
        if 'choices' in kwargs and 'max_length' not in kwargs:
            max_length = sum(len(choice[0]) for choice in kwargs['choices']) * 2
            kwargs['max_length'] = max_length  # Set a sufficiently large max_length
        
        # Call the superclass constructor with all kwargs including max_length
        super(SafeMultiSelectField, self).__init__(*args, **kwargs)
        
        # Make sure validators include MaxLengthValidator
        self.validators = [MaxLengthValidator(kwargs['max_length'])]

class Patient(models.Model):
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=15)
    patient_relative_name = models.CharField(max_length=50, null=True)
    patient_relative_contact = models.CharField(max_length=15, null=True)
    address = models.TextField()
    
    SYMPTOMS = (
        ('Fever', 'Fever'),
        ('Dry cough', 'Dry cough'),
        ('Tiredness', 'Tiredness'),
        ('Aches and pains', 'Aches and pains'),
        ('Sore throat', 'Sore throat'),
        ('Diarrhoea', 'Diarrhoea'),
        ('Loss of taste or smell', 'Loss of taste or smell'),
        ('Difficulty in breathing or shortness of breath', 'Difficulty in breathing or shortness of breath'),
        ('Chest pain or pressure', 'Chest pain or pressure'),
        ('Loss of speech or movement', 'Loss of speech or movement'),
    )
    symptoms = SafeMultiSelectField(choices=SYMPTOMS, null=True)
    prior_ailments = models.TextField()
    bed_num = models.ForeignKey("Bed", on_delete=models.CASCADE)
    dob = models.DateField(null=True)
    doctor = models.ForeignKey("Doctor", on_delete=models.CASCADE, null=True)
    doctors_notes = models.TextField(null=True, blank=True)
    doctors_visiting_time = models.CharField(null=True, max_length=50, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Bed(models.Model):
    bed_number = models.CharField(max_length=50)
    occupied = models.BooleanField()
    def __str__(self):
        return self.bed_number


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name




