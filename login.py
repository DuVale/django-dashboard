from django.forms import CharField, ValidationError
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response

#------------------------------------------------------------------------------

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

#------------------------------------------------------------------------------

def login_user(request, next= ''):
    message = 'User Login'
    lForm = LoginForm()
    
    if request.GET.has_key('next'):
        next = request.GET['next']

    if request.method == 'POST':
        if request.POST['submit'] == 'Login':
            postDict = request.POST.copy()
            lForm = LoginForm(postDict)
            if lForm.is_valid():
                uName = request.POST['username']
                uPass = request.POST['password']
                user = authenticate(username=uName, password=uPass)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(next)
                    else:
                        message = 'Account Deactivated'
                else:
                    message = 'Login Incorrect'
    
    return render_to_response('login.html',{'lForm': lForm,'message': message})

#------------------------------------------------------------------------------

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

#------------------------------------------------------------------------------

def no_rights(request):
    return render_to_response('no_rights.html',{})

#------------------------------------------------------------------------------