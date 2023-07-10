# from spa.sales.models import Sale
import json

x = open("spa/sales/data/clients.json")
data = json.load(x)

y = json.dumps(data, indent=4)

print(y)

# for i in data:
#     entry = Sale(date=i['DATE'],order_id=i['OD NO'],invoice_id=i['BILL NO'],name=i['NAME'],phone=i['PHONE'],address=i['ADDRESS'],company=i['COMPANY'],email='',gstin='',item_1=i['ITEM'],qty_1=1,rate_1=1,item_2=i['ITEM 2'],qty_2=1,rate_2=1,item_3=i['ITEM3'],qty_3=1,rate_3=1,item_4=i['ITEM4'],qty_4=1,rate_4=1,item_5=i['ITEM5'],qty_5=1,rate_5=1,item_6=i['ITEM6'],qty_6=1,rate_6=1,item_7=i['ITEM7'],qty_7=1,rate_7=1,item_8='',qty_8=1,rate_8=1,item_9='',qty_9=1,rate_9=1,item_10='',qty_10=1,rate_10=1)
#     break
  
x.close()
