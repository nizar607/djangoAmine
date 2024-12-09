# config/middleware/auth_middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware to ensure that only authenticated users can access the site's pages.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that don't require authentication
        allowed_paths = [
            reverse('auth-login-basic'),
            reverse('auth-register-basic'),
            reverse('auth-forgot-password-basic'),
            '/admin/',  # Admin path can be accessed based on user permissions
        ]
        
        # Allow access to static and media files in development
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Check if the user is authenticated or if the path is in allowed paths
        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('auth-login-basic')  # Redirect to login if not authenticated

        return self.get_response(request)
