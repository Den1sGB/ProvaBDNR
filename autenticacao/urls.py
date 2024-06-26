# urls.py (Django)

from django.contrib import admin
from django.urls import path, include
from crud import views  
from rest_framework.authtoken.views import obtain_auth_token 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crud/', include('crud.urls')),  # Inclui URLs da aplicação CRUD
    path('accounts/', include('django.contrib.auth.urls')),  # Inclui URLs de autenticação padrão do Django
    path('chat/<int:evento_id>/', views.chat_view, name='chat'),
    path('api/token/', views.obtain_token, name='api_token'),  # Rota para obtenção do token
    path('api/validate_token/', views.validate_token, name='validate_token'),

]
