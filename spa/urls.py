from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.sales_table, name="spa"),
    # path('', views.sale_entry, name="sale_entry"),
    path('receipt/', views.account.receipt, name="receipt"),
    path('salentry/', views.sale.sale_entry, name="sale_entry"),
    path('clients/', views.clients, name="client_page"),
    path('json/', views.json_response, name="json_response"),

    #
    path('ongoing/', views.sale.ongoing, name="ongoing"),
    path('outstandings/', views.sale.outstanding, name="outstandings"),

    # Editors
    path('clientedit/', views.client_edit, name="client_edit"),
    path('saledit/', views.sale.sale_edit, name="sale_edit"),
]