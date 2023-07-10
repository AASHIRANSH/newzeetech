from django.shortcuts import render

def index(request):

    return render(request, "index.html")

'''cookies'''
import datetime
def setcookie(request):
    response = render(request,"setcookie.html")
    response.set_cookie('name', 'Muhammad', expires=datetime.datetime.utcnow()+datetime.timedelta(days=2)) #
    return response

def getcookie(request):
    # name = request.COOKIES['name']
    name = request.COOKIES.get('name')
    return render(request, "getcookie.html", {'name':name})