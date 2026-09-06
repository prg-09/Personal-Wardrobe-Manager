"""
URL configuration for Wardrobe_Manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from wardrobe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    path('closet/', views.closet, name = 'closet'),
    path('outfit/', views.outfit, name = 'outfit'),
    path('register/', views.register, name= 'register'),
    path('login/',views.user_login, name = 'login'),
    path('logout/',views.user_logout,name='logout'),
    path("add-clothing/", views.add_clothing, name="add_clothing"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)