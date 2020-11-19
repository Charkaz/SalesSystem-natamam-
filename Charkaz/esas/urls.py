
from django.urls import path
from .views import dashboard,userProfile,updateprofile,insanlar,etiketqeyd,mehsullar,mehsulkatqeyd,vahidqeyd
from .views import mehsulqeyd,mehsuldata,mehsulsil,mehsulupdate,satispage,qiymetMehsul,satis,musterisatislar
from .views import satisiyekunlasdir,qiymetMehsulikinci,qrafikler

urlpatterns = [
    path('', dashboard , name = 'dashboard'),
    path('profile', userProfile , name = 'profil'),
    path('updateprofile',updateprofile,name="updateprofile"),
    path('insanlar',insanlar , name = 'insanlar'),
    path('etiketqeyd',etiketqeyd, name = 'etiketqeyd'),
    path('mehsullar',mehsullar,name='mehsullar'),
    path('mehsulkatqeyd',mehsulkatqeyd,name = 'mehsulkatqeyd'),
    path('vahidqeyd',vahidqeyd,name='vahidqeyd'),
    path('mehsulqeyd', mehsulqeyd,name='mehsulqeyd'),
    path('mehsuldata/<str:id>',mehsuldata,name='mehsuldata'),
    path('mehsulsil/<str:id>',mehsulsil,name='mehsulsil'),
    path('mehsulupdate/<str:id>',mehsulupdate,name='mehsulupdate'),
    path('satislar',satispage,name='satislar'),
    path('qiymetmehsul',qiymetMehsul,name='qiymetmehsul'),
    path('satis',satis,name="satis"),
    path('musterisatislar',musterisatislar,name="musterisatislar"),
    path('satisiyekunlasdir',satisiyekunlasdir,name = "satisiyekunlasdir"),
    path('qiymetmehsulikinci',qiymetMehsulikinci,name = 'qiymetmehsulikinci'),
 


]
