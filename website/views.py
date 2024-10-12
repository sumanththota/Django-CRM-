from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import AddRecordForm

def home(request):
    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"you have been logged in")
            return redirect('home')
        else:
            messages.success(request,"There was an error loggining")
            return redirect('home')
    else:
        return render(request, 'home.html',{'records':records})
# Authencticate

def logout_user(request):
    logout(request)
    messages.success(request,"you have been logged out")
    return redirect('home')
def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"There you must be logged in to access this page")
        return redirect('home')
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,"Delete record Succesfully")
        return redirect('home')
    else:
        messages.success(request,"There you must be logged in to delete the record ")
        return redirect('home')
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')

        return render(request, 'add_record.html',{'form':form})
    else:
        messages.success(request, "You must Be loggedIN...")
        return redirect('home')
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated")
            return redirect('home')
        return render(request, 'update_record.html',{'form':form})
    else:
        messages.success(request, "You must Be loggedIN...")
        return redirect('home')


         

    


