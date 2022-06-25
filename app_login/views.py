from cProfile import Profile
from django import shortcuts
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate,logout
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from prometheus_client import instance_ip_grouping_key
from traitlets import Instance
from app_login.forms import ProfilePic,SignUpForm,ProfilePic, UserProfileChange


def sign_up(request):
    form = SignUpForm()
    registered = False

    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict= {
        'form':form,
        'registered':registered,
        'title':'Signup'
    }
    return render(request,'app_login/signup.html',dict)


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username= form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
                # return HttpResponse("Login succesfull")
    return render(request,'app_login/login.html',context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@login_required
def profile(request):
    return render(request,'app_login/profile.html',context={})

@login_required
def user_change(request):
    current_user= request.user
    form = UserProfileChange(Instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST,Instance=current_user)
        if form.is_valid():
            form.save()
            form= UserProfileChange(Instance=current_user)
    return render(request,'app_login/change_profile.html',context={'form':form})

@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            changed= True
    return render(request,'app_login/pass_change.html',context={'form':form,'changed':changed})

@login_required
def add_pro_pic(request):
    form= ProfilePic()
    if request.method=='POST':
        form = ProfilePic(request.POST,request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.user =request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'app_login/pro_pic_add.html',context={'form':form})

@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST,request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request,'app_login/pro_pic_add.html',context={'form':form})


