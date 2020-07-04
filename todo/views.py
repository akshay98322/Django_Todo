from django.shortcuts import render, redirect,get_object_or_404 #redirect added
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm#for built in login
from django.contrib.auth.models import User #for user
from django.contrib.auth import login , logout, authenticate#for log in after create user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError #if the usr name already exists
from django.utils import timezone
from .forms import TodoForm
from .models import Todo
# home
def home(request):
    return render(request,'todo/home.html')
# sign Up
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        #Create User

        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError as e:
                return render(request, 'todo/signupuser.html',{'form':UserCreationForm(), 'error' : 'User name already taken'})


        else:
            # Let user know password didnt match
            return render(request, 'todo/signupuser.html',{'form':UserCreationForm(), 'error' : 'Password didnt match'})
# Log in
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',{'form':AuthenticationForm(), 'error' : 'User not authenticated '})
        else:
            login(request, user)
            return redirect('currenttodos')
@login_required
# completedtodos
def completedtodos(request):
    todos =Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html',{'todos':todos})
@login_required
# current
def currenttodos(request):
    todos =Todo.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-created')
    return render(request, 'todo/currenttodos.html',{'todos':todos})
@login_required
# viewtodo
def viewtodo(request,todo_pk):
    todo =get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html',{'todo':todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html',{'form':TodoForm(),'error' : 'bad data passed In'})
@login_required
# comeplete
def completetodo(request,todo_pk):
    todo =get_object_or_404(Todo,pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect('currenttodos')
@login_required
# deletetodo
def deletetodo(request,todo_pk):
        todo =get_object_or_404(Todo,pk=todo_pk, user=request.user)
        if request.method == 'POST':
            todo.delete()
            return redirect('currenttodos')
@login_required
# create todo
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',{'form':TodoForm(),'error' : 'bad data passed In'})


@login_required
# Logout
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
