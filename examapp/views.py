from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Users, Travels


# Create your views here.
def home(request):
    if 'loggedin' not in request.session:
        return render(request,'login.html')
    else:
        return redirect('/travels')
        


def login(request):
    validation=Users.objects.loginvalidator(request.POST)
    if len(validation)>0:
        for key, value in validation.items():
            messages.error(request, value)
        return redirect('/')
    loguser=Users.objects.filter(email= request.POST['em'])
    request.session['loggedin']=loguser[0].id
    return redirect('/travels')    
    

def register(request):
    validation=Users.objects.registrationValidator(request.POST)
    if len(validation)>0:
        for key, value in validation.items():
            messages.error(request, value)
        return redirect('/')
    newuser=Users.objects.create(fname=request.POST['first'],lname=request.POST['last'],email=request.POST['email'],pword=request.POST['pw'])
    request.session['loggedin']=newuser.id
    return redirect('/travels')    


def travels(request):
    if 'loggedin' not in request.session:
        return redirect('/')
    
    context={
        'loggedinuser': Users.objects.get(id=request.session['loggedin']),
        'all_trips':Travels.objects.all(),
        'my_trips':Travels.objects.filter(people=Users.objects.get(id=request.session['loggedin'])),
        'other_trips':Travels.objects.exclude(people=Users.objects.get(id=request.session['loggedin']))
    }
    return render(request, 'travels.html', context)


def addtrip(request):
    return render(request, 'addTrip.html')

def add(request):
    Travels.objects.create(place=request.POST['place'],desc=request.POST['desc'],
    travel_from=request.POST['from'],  travel_to=request.POST['to'],created_by=request.session['loggedin'])
    Travels.objects.last().people.add(Users.objects.get(id=request.session['loggedin']))
    return redirect('/')

def join(request,tripid):
    Travels.objects.get(id=tripid).people.add(request.session['loggedin'])
    return redirect('/travels')


def logout(request):
    request.session.clear()
    return redirect('/')


def view(request,tripid):
    creator=Travels.objects.get(id=tripid).created_by
    context={
        'signedin':Users.objects.get(id=request.session['loggedin']),
        'trip':Travels.objects.get(id=tripid),
        'name':Users.objects.get(id=creator),
        'other':Travels.objects.get(id=tripid).people.exclude(id=Users.objects.get(id=request.session['loggedin']).id),
        'creator':request.session['loggedin']
    }
    return render(request, 'views.html',context)



def cancel(request,tripid):
    Travels.objects.get(id=tripid).people.remove(request.session['loggedin'])
    return redirect('/')

def delete(request,tripid):
    Travels.objects.get(id=tripid).delete()
    return redirect('/')