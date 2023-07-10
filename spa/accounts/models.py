from django.db import models
from spa.sales.models import Client, Sale

class Receipt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    amount = models.CharField(max_length=1000)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.amount} ({self.sale})"

# class Payment(models.Model):
#     remitted_at = models.DateTimeField(auto_now_add=True)
#     date = models.DateField()
#     amount = models.CharField(max_length=1000)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     sale = models.ForeignKey(Sale, on_delete=models.CASCADE)