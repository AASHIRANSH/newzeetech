from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Employee
from . import forms

# Create your views here.
def employees(request):
    if request.user.is_authenticated:
        employee_model = Employee.objects.exclude(name="muhammad")
        
        #submitted form
        if request.method == 'POST':
            form = forms.EmployeeEntry(request.POST)
            
            if form.is_valid():
                form.save()
                # entry = Receipt()
                # entry.save()

                messages.success(request,'Employee was Added!!')
                return redirect('payroll')
        else:
            form = forms.EmployeeEntry()
        vars = {
            "title":"Employees",
            "employees":employee_model,
            "form":form
        }
        return render(request, "employees.html", vars)
    else:
        return redirect('sign_in')