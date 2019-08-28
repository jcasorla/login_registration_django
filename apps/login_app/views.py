from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.contrib import messages

from time import gmtime, strftime
from datetime import datetime
import random
import bcrypt
from django.contrib.auth.decorators import login_required
from . models import *


def index(request):

   return render(request, "login_app/index.html")


def show(request):

   return render(request, "login_app/show.html")

def register(request):
   if request.method=="POST":
      # print(request.POST['username'])
      print(request.POST['first_name'])
      print(request.POST['last_name'])
      print(request.POST['email'])
      print(request.POST['password'])
      print(request.POST['password2'])

      # request.session['username'] = request.POST.get('username')
      request.session['first_name'] = request.POST.get('first_name')
      request.session['last_name'] = request.POST.get('last_name')
      request.session['email'] = request.POST.get('email')
      request.session['id'] = request.POST.get('id')
      #print("whats in session:", request.session['username'])

      errors = User.objects.basic_validator(request.POST)
      #print(errors, request.POST)
      if len(errors) > 0:
         for key, value in errors.items():
            print(key, value + '\n')
            messages.add_message(request, messages.INFO,  value)
         return redirect('/')
      
   password=request.POST['password']
   mypassstring = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

   try:
      checkemail = User.objects.get(email = request.POST['email'])
      if request.POST['email'] == checkemail.email:
         messages.add_message(request, messages.INFO, "YOU ARE ALREADY REGISTERED!")
         return redirect('/')
   except User.DoesNotExist:       
      User.objects.create(
         # username=request.POST['username'],\
         first_name=request.POST['first_name'],\
         last_name=request.POST['last_name'], \
         email=request.POST['email'],\
         password = mypassstring, 
         )
      messages.add_message(request, messages.INFO, "You have successfully registered!")
      # return redirect('/index')

      return redirect("/show")

def login(request):
   if request.method=="POST":
    
      print("I am in login!")
      # checking if password or email fields are empty
      if not request.POST['email'] or not request.POST['password']:
         messages.add_message(request, messages.INFO, "Email and Password are required!")
         return redirect ("/")

      print(request.POST['email'])
      print(request.POST['password'])

      password=request.POST['password']
      getinfo = User.objects.get(email = request.POST['email'])
      
      request.session['id'] = getinfo.id
      print(getinfo.email, getinfo.password)

      val = bcrypt.checkpw(password.encode('utf8'), getinfo.password.encode('utf8'))
      print(val)

      if val:
         request.session['first_name'] = getinfo.first_name
         return redirect("/show")

      messages.add_message(request, messages.INFO, "Email or password does not match!")
   # return redirect ("/logmein/login")

   # return redirect("/show")


def logout(request):
    request.session.clear() 
    return redirect ("/")



