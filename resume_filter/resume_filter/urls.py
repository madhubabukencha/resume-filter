"""
URL configuration for resume_filter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from allauth.account.views import LoginView


# Custom 404 error handler
def custom_404(request, exception=None):
    """
    This function redirects user to respective page
    based on user's login. It when only works when
    DEBUG=False
    """
    if request.user.is_authenticated:
        # Redirect authenticated users to home page
        return redirect('resume-filter-home')
    # else redirect to login page
    return redirect('custom_login')


# Add the custom 404 handler here in the root urls.py
handler404 = 'resume_filter.urls.custom_404'

urlpatterns = [
    path('resume-filter-db/', admin.site.urls),
    path('', LoginView.as_view(), name="custom_login"),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("allauth.socialaccount.urls")),
    path("home/", include("resume_parser.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
