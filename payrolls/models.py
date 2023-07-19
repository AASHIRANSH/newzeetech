from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    address = models.CharField(max_length=150)
    date_joined = models.DateField(auto_now=False, auto_now_add=False)
    date_resigned = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

class Advance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    amount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee} {self.amount}"

# class Punch(models.Model):
#     punched_at = 
