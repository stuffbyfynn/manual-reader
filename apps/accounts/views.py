from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import User, Device
from apps.invitations.models import Invitation
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if user.status == 'blocked':
                messages.error(request, 'Ihr Account wurde gesperrt.')
                return render(request, 'accounts/login.html')
            
            login(request, user)
            return redirect('manuals:brand_list')
        else:
            messages.error(request, 'Ungültige E-Mail oder Passwort.')
            
    return render(request, 'accounts/login.html')

def register_view(request, code=None):
    # Wenn Code im URL-Pfad fehlt, versuche aus POST zu lesen
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            invitation = Invitation.objects.get(code=code)
            if not invitation.is_valid():
                messages.error(request, 'Dieser Einladungscode ist ungültig oder abgelaufen.')
                return render(request, 'accounts/register.html', {'code': code})
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Diese E-Mail wird bereits verwendet.')
                return render(request, 'accounts/register.html', {'code': code})
            
            user = User.objects.create_user(email=email, password=password)
            user.status = 'pending'
            user.save()
            
            invitation.used_by = user
            invitation.save()
            
            messages.success(request, 'Registrierung erfolgreich. Ihr Account wird geprüft.')
            return redirect('accounts:login')
            
        except Invitation.DoesNotExist:
            messages.error(request, 'Einladungscode nicht gefunden.')
            
    return render(request, 'accounts/register.html', {'code': code})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def pending_view(request):
    return render(request, 'accounts/pending.html')
