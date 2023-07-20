from django import forms
from .sales.models import Client, Sale
from .accounts.models import Receipt
import datetime
from django.core import validators #additional validator
# choices = (('ms conveyor','ms conveyor'),('rewinder','rewinder'))

class ClientEntry(forms.ModelForm):
    phone = forms.CharField(
        min_length=10,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
                'onchange':"window.location.assign('/sales?phone='+this.value)",
            }
        )
    )
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    company = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class':'form-control form-control-sm',
                'rows':'4',
            }
        )
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    gstin = forms.CharField(
        label="G.S.T. Number",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )


    class Meta:
        model = Client
        fields = '__all__'


def starts_with_s(value):#this is a custom validation function, can be used within fields
    if value[0] != 's':
        raise forms.ValidationError('name should start with s')


class SaleEntry(forms.ModelForm):
    today = datetime.date.today() #today's date only
    now = datetime.datetime.now() #today's date and time
    created_at = forms.DateTimeField(
        initial=now,
        widget=forms.DateTimeInput(
            attrs={
                'type':'hidden',
                'class':'form-control form-control-sm',
            }
        )
    )
    
    
    #REFERENCE
    mode = forms.IntegerField(initial=1,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'min':'0',
                'max':'1',
                'class':'form-control form-control-sm',
            }
        )
    )

    date = forms.DateField(
        initial=today,
        widget=forms.DateInput(
            attrs={
                'type':'date',
                'class':'form-control form-control-sm',
            }
        )
    )
    
    order_id = forms.CharField(
        initial=f"{Sale.objects.all().count()+1:03n}A{today.month}-{today.year}",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        ),
        error_messages={'required':'this is required'}
    )
    
    invoice_id = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )


    #BILL TO
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
                # 'onchange':"window.location.assign('/sales?phone='+this.value)",
            }
        )
    )
    
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    company = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
                'oninput':'loadDoc()',
            }
        )
    )
    
    address = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class':'form-control form-control-sm',
                'rows':'4',
            }
        )
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    gstin = forms.CharField(
        label="G.S.T. Number",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    
    #SHIP TO
    phones = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
                # 'onchange':"window.location.assign('/sales?phone='+this.value)",
            }
        )
    )
    
    names = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    companys = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    addresss = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class':'form-control form-control-sm',
                'rows':'4',
            }
        )
    )
    
    emails = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    gstins = forms.CharField(
        label="G.S.T. Number",
        required=False,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )

    
    #ITEMS
    item_1 = forms.CharField(
        label="Item/Product",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
                'list':'item_list',
            }
        )
    )
    desc_1 = forms.CharField(
        label="Description",
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    qty_1 = forms.IntegerField(
        label="Quantity",
        initial=1,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    rate_1 = forms.IntegerField(
        label="Price/Rate",
        initial=1,
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control form-control-sm',
            }
        )
    )
    
    
    class Meta:
        model = Sale
        fields = "__all__"
        # fields = ['sale_item','company']
        # widgets = {"referrer":"attrs"}
        # custom_item = forms.CharField(widget=forms.TextInput(attrs={'class':'btn','id':'anyid'}), label='Product', label_suffix=' | ', initial='Conveyor', max_length=100, required=False, disabled=True, help_text='this is the item field')


class ReceiptEntry(forms.ModelForm):
    date = forms.DateField(initial=datetime.date.today())
    class Meta:
        model = Receipt
        fields = "__all__"


class UserSignUpForm(forms.Form):
    error_css_class = 'error'
    error_required_class = 'error'

    username = forms.CharField(validators=[validators.MaxLengthValidator(10)], required=False, error_messages={'required':'Please enter a username','max_length':'Username cannot be greater than 50 chars'}, strip=True)
    name = forms.CharField(max_length=10, required=False, empty_value='User')
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, max_length=50, required=True)
    agree = forms.BooleanField(required=False) #checkbox field

    def custom_username_validator(self):
        value = self.cleaned_data['username']
        if len(value) < 5 :
            raise forms.ValidationError('username cannot be less than 5 chars')
        return value
    
    def password_validator(self):
        # cleaned_data = super().password_validator(self)
        pass1 = self.cleaned_data['pass1']
        pass2 = self.cleaned_data['pass2']
        if pass1 != pass2:
            raise forms.ValidationError('Password does not match')