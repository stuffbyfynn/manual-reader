from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            if request.user.last_session_key and request.user.last_session_key != current_session_key:
                # Invalidate the old session
                try:
                    s = Session.objects.get(session_key=request.user.last_session_key)
                    s.delete()
                except Session.DoesNotExist:
                    pass
                
                # Update to the new session key
                request.user.last_session_key = current_session_key
                request.user.save(update_fields=['last_session_key'])
            elif not request.user.last_session_key:
                request.user.last_session_key = current_session_key
                request.user.save(update_fields=['last_session_key'])

        response = self.get_response(request)
        return response

class ActiveStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_staff:
            # List of allowed URLs for non-active users
            allowed_urls = [
                reverse('accounts:pending'),
                reverse('accounts:logout'),
                reverse('accounts:login'), # In case they are logged in but stuck
            ]
            
            # Check if current path is allowed
            if request.path not in allowed_urls and request.user.status != 'active':
                return redirect('accounts:pending')

        return self.get_response(request)
