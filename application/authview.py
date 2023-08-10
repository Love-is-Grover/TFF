from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .forms import CustomUserForm , PasswordChangeCustomForm
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_str,force_bytes
from .tokens import generate_token
from home import settings

def register(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged In")
        return redirect("home")
    else:
        form = CustomUserForm()
        if request.method == "POST":
            form = CustomUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                messages.success(request,"Account created successfully")
                return redirect(login)
        content = {
            'form' : form,
            'title' : "Register",
        }
        return render(request,"register.html",content)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already Logged In")
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password= password)
            if user is not None:
                auth_login(request,user)
                messages.success(request,"Logged In Successfully")
                return redirect("home")
            else:
                messages.error(request,"Invalid Username and Password")
                return redirect('login')
        content = {
            "title" : "Log-In"
        }
        return render(request,"login.html",content)
    
    
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request,"Logged Out Successfully")
    return redirect("home")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        auth_login(request,user)
        messages.success(request,"Registered Successfully")
        return redirect('home')
    

def changepass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeCustomForm(user=request.user, data= request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request,fm.user)
                messages.success(request,"Password Changed Successfully.")
                return redirect('home')
        else:
            fm = PasswordChangeCustomForm(user=request.user)
        return render(request,"changepass.html",{"title" : "change-password", 'form':fm})
    else:
        messages.error(request,"Please Log-In first")
        return redirect('home')