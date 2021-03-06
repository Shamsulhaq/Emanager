"""fastpick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import create_order

urlpatterns = [
    path('service/hire/<id>', create_order, name='service-hire-view-url'),
    # path('account/login/', login_page, name='login-url'),
    # # path('account/guest/', guest_register_view, name='guest_access'),
    # path('account/logout/', LogoutView.as_view(), name='get_logout'),
    # path('account/register/', register_page, name='register-url'),
]
