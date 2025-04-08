"""
URL configuration for slavichoney_back project.

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
from django.urls import path

from slavichoney_app.views import save_user, get_all_products, update_basket, place_order, confirm_order, cancel_order

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('save_user/', save_user, name='save_user'),
                  path('products/', get_all_products, name='products'),
                  path('update_basket/', update_basket, name='update_basket'),
                  path('place_order/', place_order, name='place_order'),
                  path('confirm_order/', confirm_order, name='confirm_order'),
                  path('cancel_order/', cancel_order, name='cancel_order')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
