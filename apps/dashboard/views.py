from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from apps.accounts.models import User
from apps.invitations.models import Invitation
from apps.manuals.models import Manual, Brand
import string
import random
from django.utils import timezone
from datetime import timedelta

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def dashboard_home(request):
    context = {
        'total_users': User.objects.count(),
        'pending_users': User.objects.filter(status='pending').count(),
        'active_users': User.objects.filter(status='active').count(),
        'total_manuals': Manual.objects.count(),
        'recent_users': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'dashboard/home.html', context)

@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/user_list.html', {'users': users})

@user_passes_test(is_admin)
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'active'
    user.save()
    return redirect('dashboard:user_list')

@user_passes_test(is_admin)
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 'blocked'
    user.save()
    return redirect('dashboard:user_list')

@user_passes_test(is_admin)
def create_invitation(request):
    if request.method == 'POST':
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        Invitation.objects.create(
            code=code,
            created_by=request.user,
            expires_at=timezone.now() + timedelta(days=7)
        )
    return redirect('dashboard:invitation_list')

@user_passes_test(is_admin)
def invitation_list(request):
    invitations = Invitation.objects.all().order_by('-created_at')
    return render(request, 'dashboard/invitation_list.html', {'invitations': invitations})
