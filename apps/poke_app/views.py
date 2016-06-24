from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from datetime import timedelta, datetime
from django.db.models import Count

from .models import User, Poke

# Create your views here.
def index(request):
    minage = datetime.now()-(timedelta(days=365)*13)+(timedelta(days=3))
    context = {
        "minage": minage
    }
    return render(request, 'index.html', context)

def registerUser(request):
    if request.method == "POST":
        validate = User.userManager.register(**request.POST)
        if validate[0]:
            newuser = validate[1]
            olduser = User.objects.filter(name=newuser['name'])
            for user in olduser:
                user.delete()
            newuser = User.objects.create(name=newuser['name'],
                alias=newuser['alias'], email=newuser['email'],
                password=newuser['password'], birthdate=newuser['birthdate'])
            request.session['id'] = newuser.id
            users = User.objects.all()
            return redirect(reverse('display-pokes'))

        else:
            errors = validate[1]
            for error_type in errors:
                messages.add_message(request, messages.INFO,
                    errors[error_type], extra_tags=error_type)

    return redirect(reverse('landing'))

def loginUser(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        val = User.userManager.login(email=email, password=password)
        if val[0]:
            user = val[1]
            request.session['id'] = user.id
            return redirect(reverse('display-pokes'))

        else:
            errors = val[1]
            for error_type in errors:
                messages.add_message(request, messages.INFO,
                    errors[error_type], extra_tags=error_type)

    return redirect(reverse('landing'))

def displayPokes(request):
    user = User.objects.get(id=request.session['id'])
    pokers = User.objects.filter(poke_set__poked=user)

    context = {
        'user': user,
        'pokers': pokers,
        'users': User.objects.all()
            }
    return render(request, 'pokes.html', context)

def poke(request):
    if request.method == "POST":
        poker = User.objects.get(id=request.session['id'])
        poked = User.objects.get(id=request.POST['poked'])
        Poke.objects.create(poker=poker, poked=poked)

    return redirect(reverse('display-pokes'))

def logout(request):
    request.session.clear()
    return redirect(reverse('landing'))
