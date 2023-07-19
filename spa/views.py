'''----------- Path Resolve Stable -----------'''
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
'''-------------------------------------------'''
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from .sales.models import Client, Sale, Item
from .accounts.models import Receipt
from . import forms

#MODEL SERIALIZE
from django.core import serializers
from django.http import JsonResponse
import json


def jsonToModel(request):
    model = Client
    file = "clients"
    file_path = f"spa/sales/data/{file}.json"

    with open(file_path, "r") as json_file:
        x = json.load(json_file)

    for entry in x:
        fields = entry.get("fields")

        phone = fields.get("phone")
        name = fields.get("name")
        company = fields.get("company")
        address = fields.get("address")
        email= fields.get("email")
        gstin = fields.get("gstin")
        # item_1 = fields.get("item_1")
        # desc_1 = fields.get("desc_1")
        # qty_1 = fields.get("qty_1")
        # rate_1 = fields.get("qty_1")
                
        model.objects.create(phone=phone,name=name,company=company,address=address,email=email,gstin=gstin)
    return HttpResponseRedirect('/')


def supplier(request):
    return render(request, "clients/supplier.html")


def clients(request):
    if request.user.is_authenticated:

        companies = Client.objects.values_list('company', flat=True) #returns list items as tuples if not given the argument flat=True
        
        if request.method == 'POST':
            form = forms.ClientEntry(request.POST) #this is a complete form with html code and predefined values came from the user or submitted form
            
            data_post = request.POST
            if data_post.get('company') in companies:
                messages.add_message(request, messages.ERROR, "An account is already exist with this company name")
                return redirect('client_page')
            
            if form.is_valid():
                cleaned_data = form.cleaned_data  #this dictionary contains all submitted input from user
                company=cleaned_data['company']
                entry = Client(
                    phone=cleaned_data['phone'],
                    name=str(cleaned_data['name']).lower(),
                    company=str(cleaned_data['company']).lower(),
                    email=cleaned_data['email'],
                    address=str(cleaned_data['address']).lower(),
                    gstin=str(cleaned_data['gstin']).upper(),
                )
                entry.save()
                messages.success(request,f'The client "{company}" has been added successfully!!')
                
                clients_json = serializers.serialize('json', Client.objects.all())
                with open(BASE_DIR/"spa/sales/data/clients.json","w") as ent:
                    ent.write(clients_json)
                return redirect('client_page')            #this can be used as well
        else:
            form = forms.ClientEntry()    #append "(auto_id='id_%s')" to use custom id behaviour, this example is set by default

        vars = {
            "title":"Clients",
            "clients_table":Client.objects.values(),
            "sales_form":form
        }
        return render(request, "sales/clients.html", vars)
    else:
        return redirect('sign_in')


def sales_table(request):
    vars = {
        "sales_table":Sale.objects.all().order_by("-date"),
    }
    return render(request,"sales/sales_table_page.html", vars)


def client_edit(request):
    with open(BASE_DIR/"spa/sales/data/clients.json","r") as cli:
        clients_json = json.load(cli)
        company_arr = [x['fields']['company'] for x in clients_json]

    id = request.GET.get('id')
    client = get_object_or_404(Client, pk=id)

    if request.method == "POST":
        form = forms.ClientEntry(request.POST or None, instance=client)

        '''deleting an entry'''
        if request.POST.get('delete'):
            if request.POST['delete'] == "yes":
                client.delete()
                messages.warning(request, "the client was deleted")
                return redirect("spa")
            '''----------------------------------------'''
        
        # you can put inputs here if you want to override the validation, it looks like hacking
        # it accepts the empty inputs as well even though the put was required
        # NOTE: it will throw errors however the inputs below will be saved
        # -------------inputs can be given as below--------------------
        # sale.phone = request.POST.get('phone')
        # sale.save()

        if form.is_valid():
            form.save()
            # cd = form.cleaned_data
            # client.name = cd['name']
            # client.company = cd['company']
            # client.save()
            messages.success(request,f'Details for "{client.company}" were Updated!!')
            return redirect('client_page')
        else:
            messages.error(request,"form is not valid")
    else:
        form = forms.ClientEntry(instance=client)
    
    vars = {
        "id":id,
        "sales_form": form,
        "company":json.dumps(company_arr)
    }
    return render(request,"sales/forms/client.html", vars)

class account():
    def receipt(request):
        if request.user.is_authenticated:
            company_arr = Client.objects.all().values_list('company')

            #submitted form
            if request.method == 'POST':
                form = forms.ReceiptEntry(request.POST)
                
                if form.is_valid():
                    cd = form.cleaned_data

                    form.save()
                    # entry = Receipt()
                    # entry.save()

                    messages.success(request,'Receipt Entry was Added!!')
                    return redirect('receipt')
            else:
                form = forms.ReceiptEntry()


            companies = []
            for x in company_arr:
                companies.append(x[0])

            vars = {
                "title":"Receipt Entry",
                "form":form,
                "company":json.dumps(companies),
            }
            return render(request, "accounts/receipt.html", vars)
        else:
            return HttpResponseRedirect('/users/signin')

class sale():

    def sale_entry(request):
        if request.user.is_authenticated:

            with open(BASE_DIR/"spa/sales/data/items.json","r") as items:
                items_json = json.load(items)
                items_arr = [x['name'] for x in items_json]

            # with open(BASE_DIR/"spa/sales/data/clients.json","r") as cli:
            #     clients_json = json.load(cli)
            #     company_arr = [x['fields']['company'] for x in clients_json]
            comp_qd = Client.objects.values_list('company', flat=True)
            companies = []
            for x in comp_qd:
                companies.append(x)
            # sales_entry_form = SaleEntry(auto_id='sale_%s',label_suffix=' - ', initial={'item':'conveyor','rate':30000})

            # sales_entry_form = SaleEntry(auto_id=False)    # use it to remove the 'label' tag and 'id' attribute

            # sales_entry_form.order_fields(field_order=['rate','item']) #Custom order

            if request.method == 'POST':
                req_post = request.POST.copy()
                req_post.update({'operator':request.user})
                sales_entry_form = forms.SaleEntry(req_post) #this is a complete form with html code and predefined values came from the user or submitted form
                
                if sales_entry_form.is_valid():
                    sales_entry_form.save()
                    
                    # cd = sales_entry_form.cleaned_data
                    
                    # if cd.get("same") == "yes":
                    #     phones=''
                    #     names=''
                    #     companys=''
                    #     emails=''
                    #     addresss=''
                    #     gstins=''
                    # else:
                    #     phones=cd['phones']
                    #     names=cd['names']
                    #     companys=cd['companys']
                    #     emails=cd['emails']
                    #     addresss=cd['addresss']
                    #     gstins=cd['gstins']

                    # entry = Sale(
                    #     #reference
                    #     mode=cd['mode'],
                    #     final=cd['final'],
                    #     note=cd['note'],

                    #     date=cd['date'],
                    #     order_id=cd['order_id'],
                    #     invoice_id=cd['invoice_id'],
                    #     referrer=cd['referrer'],
                    #     operator=request.user,
                    #     #client bill to
                    #     phone=cd['phone'],
                    #     name=cd['name'],
                    #     company=cd['company'],
                    #     email=cd['email'],
                    #     address=cd['address'],
                    #     gstin=cd['gstin'],
                    #     #client ship to
                    #     phones=phones,
                    #     names=names,
                    #     companys=companys,
                    #     emails=emails,
                    #     addresss=addresss,
                    #     gstins=gstins,
                    #     #item_1
                    #     item_1=cd['item_1'],
                    #     desc_1=cd['desc_1'],
                    #     qty_1=cd['qty_1'],
                    #     rate_1=cd['rate_1'],
                    #     #item_2
                    #     item_2 = cd.get('item_2'),
                    #     desc_2 = cd.get('desc_2'),
                    #     qty_2 = cd.get('qty_2'),
                    #     rate_2 = cd.get('rate_2'),
                    #     #item_3
                    #     item_3 = cd.get('item_3'),
                    #     desc_3 = cd.get('desc_3'),
                    #     qty_3 = cd.get('qty_3'),
                    #     rate_3 = cd.get('rate_3'),
                    #     #item_4
                    #     item_4 = cd.get('item_4'),
                    #     desc_4 = cd.get('desc_4'),
                    #     qty_4 = cd.get('qty_4'),
                    #     rate_4 = cd.get('rate_4'),
                    #     #item_5
                    #     item_5 = cd.get('item_5'),
                    #     desc_5 = cd.get('desc_5'),
                    #     qty_5 = cd.get('qty_5'),
                    #     rate_5 = cd.get('rate_5'),
                    # )
                    # entry.save()
                    messages.success(request,'Sale Added!!')
                    return redirect('spa')
                else:
                    messages.error(request,'Please check below for any mistakes')
            else:
                sales_entry_form = forms.SaleEntry()    #append "(auto_id='id_%s')" to use custom id behaviour, this example is set by default

            vars = {
                "title":"Sale Entry",
                "sales_form":sales_entry_form,
                "items":json.dumps(items_arr),
                "company":json.dumps(companies),
            }
            return render(request, "sales/sales_entry.html", vars)
        else:
            return HttpResponseRedirect('/users/signin')


    def sale_edit(request):
        # if request.user.is_authenticated:

        with open(BASE_DIR/"spa/sales/data/items.json","r") as items:
                items_json = json.load(items)
                items_arr = [x['name'] for x in items_json]

        with open(BASE_DIR/"spa/sales/data/clients.json","r") as cli:
            clients_json = json.load(cli)
            company_arr = [x['fields']['company'] for x in clients_json]

        id = request.GET.get('id')
        sale = Sale.objects.get(id=id)

        if request.method == "POST":
            req_post = request.POST.copy()
            req_post.update({'operator':sale.operator})
            
            form = forms.SaleEntry(req_post or None, instance=sale)

            '''deleting an entry'''
            if request.POST.get('delete'):
                if request.POST['delete'] == "yes":
                    sale.delete()
                    messages.warning(request, "the sale was deleted")
                    return redirect('spa')
                '''----------------------------------------'''

            #override
            # odd = request.POST
            # od = request.GET
            # if od.get('admin'):
            #     sale.order_id = odd.get('order_id')
            #     sale.save()
            # you can put inputs here if you want to override the validation, it looks like hacking
            # it accepts the empty inputs as well even though the value was required
            # NOTE: it will throw errors however the inputs below will be saved
            # -------------inputs can be given as below--------------------
            # sale.phone = request.POST.get('phone')
            # sale.save()

            if form.is_valid():
                form.save()
                cd = form.cleaned_data

                # sale.company = cd['company']
                # sale.name = cd['name']
                # sale.phone = cd['phone']
                # sale.gstin = cd['gstin']
                # sale.address = cd['address']
                # sale.save()

                messages.success(request,f'Sale of Order No. "{sale.order_id}" was Updated!!')
                return redirect('spa')
            else:
                messages.error(request,"form is not valid")
        else:
            form = forms.SaleEntry(instance=sale)

        company = request.POST.get('company')
        
        vars = {
            "edit":True,
            "title":"sale edit",
            "num":company,
            "sales_form":form,
            "items":json.dumps(items_arr),
            "company":json.dumps(company_arr),
        }

        return render(request,"sales/sales_entry.html", vars)
    
    
    def ongoing(request):
        vars = {
            "title":"Ongoing Orders",    
            "sales_table":Sale.objects.filter(final=False),
            "payments":Receipt.objects.all()
        }
        return render(request, "sales/ongoing.html", vars)


def json_response(request):
    data = request.GET
    if data.get("action") == "adv":
        adv_sale = Sale.objects.get(id=data.get("id"))
        adv_model = serializers.serialize("json",Receipt.objects.filter(sale=adv_sale))
        adv_model = json.loads(adv_model)

        return JsonResponse(adv_model, safe=False)

    if data.get("action") == "company":
        company = data.get('company')
        # item = data.get('item')

        sale_model = serializers.serialize("json",Client.objects.filter(company=company))
        sale_model = json.loads(sale_model)
        return JsonResponse(sale_model, safe=False)