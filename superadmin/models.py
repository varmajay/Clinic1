
from random import choices
from django.db import models
from datetime import date

# Create your models here.


class User(models.Model):
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = ((GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'))
    ROLES = (

        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patients', 'Patients'),

    )
    roles = models.CharField(max_length=30,choices = ROLES)
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    clinic_name = models.CharField(max_length=30,default=None,blank=True,null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES,default=None,null=True,blank=True)
    specialty = models.CharField(max_length=30,default=None,blank=True,null=True)
    address = models.TextField(default=None,blank=True,null=True)
    profile = models.FileField(upload_to='user',default='profile.png')
    

    def __str__(self):
        return self.name+" "+self.email


class Doctor_availability(models.Model):
    WEEKS = {
        ('Mon','MONDAY'),
        ('Tue','TUESDAY'),
        ('Wed','WEDNESDAY'),
        ('Thu','THURSDAY'),
        ('Fri','FRIDAY'),
        ('Sat','SATURDAY'),
    }
    doctor = models.ForeignKey(User,on_delete=models.CASCADE)
    week = models.CharField(max_length=15,choices=WEEKS)
    start_time = models.TimeField('start time')
    end_time = models.TimeField('end time')

    def __str__(self):
        return self.week



class Appoinment(models.Model):
    STATUS = (
        (0,'Pending'),
        (1,'Completed'),
        (2,'Absent'),
        (3,'Canceled'),
    ) 
    doctor = models.ForeignKey(User,related_name='doctor_aap' ,on_delete=models.CASCADE)
    patient = models.ForeignKey(User,related_name='patient_app',on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField('start time')
    end_time = models.TimeField('end time')
    description = models.TextField( default=None)
    status = models.IntegerField(default=0,choices=STATUS)


    def __int__(self):
        return self.doctor.name

    def __str__(self):
        return self.patient.name