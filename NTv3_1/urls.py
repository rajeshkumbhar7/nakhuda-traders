"""NTv3_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from shopapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', adminLogin, name="admin_login"), 
    path('index/', index, name="index"), 
    path('about/', about, name="about"), 
    path('logout/', logoutuser, name="logout"),
  
    path('adminhome/', adminHome, name="adminhome"), 
    path('admin-dashboard/', admin_dashboard, name="admin_dashboard"),  
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
  
    path('add-category/', add_category, name="add_category"),  
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),  

  
    path('add-product/', add_product, name='add_product'),   
    path('view-product/', view_product, name='view_product'),  
    path('edit-product/<int:pk>', edit_product, name="edit_product"),  
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),

    path('notifications/', notification_list, name='notification_list'),
    path('add_stock/<int:pk>/', add_stock, name='add_stock'),
  
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('remove-from-cart/<int:pk>', remove_from_cart, name='remove_from_cart'),

    path('invoice-history/', view_invoice_history, name='view_invoice_history'),
    
  
  

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


