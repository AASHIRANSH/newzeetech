from django.contrib import admin
from payrolls.models import Employee, Advance

# Register your models here.
@admin.register(Employee)
class EmployeeView(admin.ModelAdmin):
    list_display = ('name','salary')

@admin.register(Advance)
class AdvanceView(admin.ModelAdmin):
    list_display = ('employee','amount')