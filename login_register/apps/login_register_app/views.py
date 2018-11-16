# By Andy Nguyen
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect('/success')
    else:
        return render(request, 'login_register_app/index.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.add_message(request, messages.ERROR, value, extra_tags='register')
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect("/success")
    else:
        return redirect("/")


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.add_message(request, messages.ERROR, value, extra_tags='login')
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id
            return redirect("/wall")


def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id=request.session['user_id'])
        }
        return render(request,'login_register_app/dash.html', context)


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'login_register_app/success.html', context)


def reset(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        print("session has been cleared")
        return redirect("/")