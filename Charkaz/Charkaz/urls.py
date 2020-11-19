
from django.contrib import admin
from django.urls import path,include
from start.views import login,register,logout_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login , name = 'login'),
    path('register', register , name = "register"),
    path('logout',logout_user,name='logout'),
    path('system/',include('esas.urls')),
   
]

urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)
