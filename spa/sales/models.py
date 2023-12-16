from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True, null=True)
    gstin = models.CharField(max_length=15)
    

    def __str__(self):
        return f"{self.name} {self.company}"


class Referrer(models.Model):
    phone = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.company})"


class Item(models.Model):#NOT BEING USED
    name = models.CharField(max_length=100)
    moc = models.CharField(max_length=10, default=None)
    rate = models.IntegerField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.moc+" "+self.name


class Sale(models.Model):
    '''reference'''
    '''for admin'''
    created_at = models.DateTimeField(auto_now_add=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    mode = models.IntegerField()
    promise = models.IntegerField()

    payments = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    despatched = models.BooleanField(default=False)
    

    '''for all'''
    date = models.DateField()
    order_id = models.CharField(max_length=15)
    invoice_id = models.CharField(max_length=20, blank=True, null=True)
    referrer = models.ForeignKey(Referrer, on_delete=models.CASCADE)


    '''client bill to'''
    phone = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=200, default=None)
    company = models.CharField(max_length=200, default=None)
    email = models.EmailField(max_length=200, default=None, blank=True, null=True)
    address = models.CharField(max_length=1000, default=None)
    gstin = models.CharField(max_length=15, default=None)


    '''client ship to'''
    phones = models.CharField(max_length=50, default="", blank=True, null=True)
    names = models.CharField(max_length=200, default="", blank=True, null=True)
    companys = models.CharField(max_length=200, default="", blank=True, null=True)
    emails = models.EmailField(max_length=200, default="", blank=True, null=True)
    addresss = models.CharField(max_length=1000, default="", blank=True, null=True)
    gstins = models.CharField(max_length=15, default="", blank=True, null=True)
    

    '''item1'''
    item_1 = models.CharField(max_length=50)
    desc_1 = models.CharField(max_length=200)
    qty_1 = models.IntegerField(default=1)
    rate_1 = models.IntegerField(default=1)

    '''item2'''
    item_2 = models.CharField(max_length=50, null=True, blank=True)
    desc_2 = models.CharField(max_length=200, null=True, blank=True)
    qty_2 = models.IntegerField(null=True, blank=True)
    rate_2 = models.IntegerField(null=True, blank=True)

    '''item3'''
    item_3 = models.CharField(max_length=50,null=True, blank=True)
    desc_3 = models.CharField(max_length=200,null=True, blank=True)
    qty_3 = models.IntegerField(null=True, blank=True)
    rate_3 = models.IntegerField(null=True, blank=True)

    '''item4'''
    item_4 = models.CharField(max_length=50, null=True, blank=True)
    desc_4 = models.CharField(max_length=200, null=True, blank=True)
    qty_4 = models.IntegerField(null=True, blank=True)
    rate_4 = models.IntegerField(null=True, blank=True)

    '''item5'''
    item_5 = models.CharField(max_length=50,null=True, blank=True)
    desc_5 = models.CharField(max_length=200,null=True, blank=True)
    qty_5 = models.IntegerField(null=True, blank=True)
    rate_5 = models.IntegerField(null=True, blank=True)

    '''item6'''
    item_6 = models.CharField(max_length=50,null=True, blank=True)
    desc_6 = models.CharField(max_length=200,null=True, blank=True)
    qty_6 = models.IntegerField(null=True, blank=True)
    rate_6 = models.IntegerField(null=True, blank=True)

    '''item7'''
    item_7 = models.CharField(max_length=50,null=True, blank=True)
    desc_7 = models.CharField(max_length=200,null=True, blank=True)
    qty_7 = models.IntegerField(null=True, blank=True)
    rate_7 = models.IntegerField(null=True, blank=True)

    '''item8'''
    item_8 = models.CharField(max_length=50,null=True, blank=True)
    desc_8 = models.CharField(max_length=200,null=True, blank=True)
    qty_8 = models.IntegerField(null=True, blank=True)
    rate_8 = models.IntegerField(null=True, blank=True)
    '''item9'''
    item_9 = models.CharField(max_length=50,null=True, blank=True)
    desc_9 = models.CharField(max_length=200,null=True, blank=True)
    qty_9 = models.IntegerField(null=True, blank=True)
    rate_9 = models.IntegerField(null=True, blank=True)
    '''item10'''
    item_10 = models.CharField(max_length=50,null=True, blank=True)
    desc_10 = models.CharField(max_length=200,null=True, blank=True)
    qty_10 = models.IntegerField(null=True, blank=True)
    rate_10 = models.IntegerField(null=True, blank=True)

    grand_total = models.FloatField()

    note = models.TextField()


    def __str__(self):
        return f"{self.order_id} {self.item_1}"




# class Orders(models.Model):
#     order_id = models.CharField(max_length=10)
#     phone = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     company = models.CharField(max_length=200)