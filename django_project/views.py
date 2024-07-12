from django.http import HttpResponse, request
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from issues.models import Issue
def home(request):
  return render(request,'website/index.html')

def signup_view(request):
  if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
          user = form.save()
          login(request, user)
          return redirect('home')
  else:
      form = UserCreationForm()
  return render(request, 'website/signup.html', {'form': form})   

def login_view(request):
  if request.method == 'POST':
      form = AuthenticationForm(request, data=request.POST)
      if form.is_valid():
          username = form.cleaned_data.get('username')
          password = form.cleaned_data.get('password')
          user = authenticate(username=username, password=password)
          if user is not None:
              login(request, user)
              return redirect('issue_list')  # Redirect to your desired page after login
      else:
          print(form.errors)  # Check form errors in the console
  else:
      form = AuthenticationForm()
  return render(request, 'website/login.html', {'form': form}) 

def logout_view(request):
  logout(request)
  return redirect('home')

@login_required
def profile(request):
  current_user=request.user;
  issues_assigned_to_user=Issue.objects.filter(assignee=current_user)
  context = {
    'issues': issues_assigned_to_user
  }
  return render(request, 'website/profile.html', context)

def pricing(request):
  return render(request, 'website/pricing.html')
