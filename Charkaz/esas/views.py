from django.shortcuts import render,HttpResponse,HttpResponseRedirect,reverse
from django.contrib.auth.models import User
from django.contrib import messages
from start.models import userProfile
from .models import mehsulkat,vahid,mehsul,qaime,musteri
from .models import satis as satis_
from django import template
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse
from datetime import datetime

def qrafikler():
    return []

@login_required(login_url=reverse_lazy('login'))
def dashboard(request):
    return render(request,'soft/dashboard.html')

@login_required(login_url=reverse_lazy('login'))
def userProfile(request):
    return render(request,'soft/user.html')

@login_required(login_url=reverse_lazy('login'))
def mehsullar(request):
    page = request.GET.get('page',1)
    user = request.user
    vahidler = vahid.objects.filter(useri=user)
    kateqoriyalar = mehsulkat.objects.filter(useri=user)
    mehsullarim = mehsul.objects.filter(useri=user)
    katim = request.GET.get('kat')
    try:
        if request.method == "GET":

            if katim == 'Hamisi' or katim == "":
                    mehsullarim = mehsul.objects.filter(useri=user)
            else:
                if katim:
                    mehsulkatim = mehsulkat.objects.get(useri=user,ktad=katim)
                    mehsullarim = mehsul.objects.filter(useri=user,kateqoriya=mehsulkatim)
    except:
        messages.success(request,'Zehmet olmasa duzgun kateqoriya secin.',extra_tags='danger')
        return HttpResponseRedirect(reverse('mehsullar'))
    
    if request.GET.get('axtar'):
        mehsullarim = mehsul.objects.filter(useri=user,mehsulad__icontains = request.GET.get('axtar'))

    paginator = Paginator(mehsullarim,4)
    try:
        mehsullarim = paginator.page(page)
    except EmptyPage:
        mehsullarim = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        mehsullarim = paginator.page(1)
    

    context = {
        'vahidler':vahidler,
        'kateqoriyalar':kateqoriyalar,
        'mehsullar':mehsullarim

    }


    return render(request, 'soft/mehsullar.html',context)

@login_required(login_url=reverse_lazy('login'))
def mehsulkatqeyd(request):
    if request.method == "POST":
        user = request.user
        kat = request.POST['mehsulkat']
        if kat:
            try:
                mehsulkateqoriya = mehsulkat(ktad=kat,useri = user)
                mehsulkateqoriya.save()
                messages.success(request,"Mehsul kateqoriyasi ugurla qeyd edildi .",extra_tags='success')
                return HttpResponseRedirect(reverse('mehsullar'))
            except Exception as e:
                messages.success(request,"Mehsul kateqoriyasi uyaradilarken problem yarandi . "+str(e),extra_tags='danger')
                return HttpResponseRedirect(reverse('mehsullar'))
        else:
            messages.success(request,"zehmet olmasa kateqoriya adini yazin.",extra_tags='danger')
            return HttpResponseRedirect(reverse('mehsullar'))

@login_required(login_url=reverse_lazy('login'))
def mehsulqeyd(request):
    if request.method == "POST":
        #print(mehsulad,mehsulkod,barkod,alisqiymet,satisqiymet,boyukinkicik,boyukolcu,kicikolcu,kateqoriya,kritikstok)
        try:
            user = request.user
            mehsulad = request.POST['mehsuladi']
            mehsulkod = request.POST['mehsulkodu']
            barkod = request.POST['barkod']
            alisqiymet = request.POST['alisqiymet']
            satisqiymet = request.POST['satisqiymet']
            standart    = vahid.objects.filter(vahidad = request.POST['standart']).first()
            stok = request.POST['stok']
            kritikstok = request.POST['kritikstok']
            kateqoriya = mehsulkat.objects.get(ktad = request.POST['kateq']) 
            mehsulsekil = None
            if request.FILES:
                mehsulsekil = request.FILES['sekil']
            print(mehsulad,mehsulkod,barkod,alisqiymet,satisqiymet,kateqoriya,kritikstok)
        
            yeniMehsul = mehsul(mehsulad=mehsulad,mehsulkod=mehsulkod,barkod=barkod,alisqiymet=float(alisqiymet),satisqiymet=float(satisqiymet),standart=standart,stok=stok,kritiksay=kritikstok,kateqoriya=kateqoriya,mehsulFoto = mehsulsekil,useri=user )
            yeniMehsul.save()
            messages.success(request,"Mehsul melumat bazasina ugurla qeyd edildi . ",extra_tags='success')
            return HttpResponseRedirect(reverse('mehsullar'))
        except Exception as e:
            messages.success(request,"Mehsul melumat bazasina yazilarken  problem yarandi . "+str(e),extra_tags='danger')
            return HttpResponseRedirect(reverse('mehsullar'))
        return HttpResponse("ads")
    else:
        pass


@login_required(login_url=reverse_lazy('login'))
def vahidqeyd(request):
    if request.method == "POST":
        user = request.user
        vahidi = request.POST['vahid']
        if vahidi:
            try:
                yeniVahid = vahid(vahidad=vahidi,useri = user)
                yeniVahid.save()
                messages.success(request,"Mehsula aid olan olcu vahidi ugurla yaradildi .",extra_tags='success')
                return HttpResponseRedirect(reverse('mehsullar'))
            except Exception as e:
                messages.success(request,"Mehsula aid olan olcu vahidi uyaradilarken problem yarandi . "+str(e),extra_tags='danger')
                return HttpResponseRedirect(reverse('mehsullar'))
        else:
            messages.success(request,"zehmet olmasa olcu vahidi  yazin.",extra_tags='danger')
            return HttpResponseRedirect(reverse('mehsullar'))


@login_required(login_url=reverse_lazy('login'))
def insanlar(request):
 
    return render(request,'soft/insanlar.html')

@login_required(login_url=reverse_lazy('login'))
def updateprofile(request):
    if request.method == "POST":
        email = request.POST['email']
        ad = request.POST['ad']
        soyad = request.POST['soyad']
        telefon =request.POST['telefon']
        adres = request.POST['adres']
        sekil = None
        dogumtarix = request.POST['dogumtarix']
        if request.FILES:
            sekil = request.FILES['sekil']
            print(sekil)
        
        try:
            user = User.objects.get(username=request.user.username)
            user.first_name = ad
            user.last_name = soyad
            user.email = email
            user.save()
            userprof = user.userprofile
            userprof.adress = adres
            userprof.dogumtarixi = dogumtarix
            userprof.telefon = telefon
            userprof.profilsekli  = sekil
            userprof.save()
            messages.success(request,"profil ugurla tenzimlendi !",extra_tags='success')
            return HttpResponseRedirect(reverse('profil'))
            
        except Exception as e:
            messages.success(request,"profili tenzimlemek mumkun olmadi !"+" "+str(e),extra_tags='danger')
            return HttpResponseRedirect(reverse('profil'))

@login_required(login_url=reverse_lazy('login'))
def etiketqeyd(request):
    pass

@login_required(login_url=reverse_lazy('login'))
def mehsuldata(request,id):
    mehsulum = mehsul.objects.get(id = id)
    vahidler = vahid.objects.filter(useri=request.user)
    kateqoriyalar = mehsulkat.objects.filter(useri=request.user)
    context = {
        'mehsul':mehsulum,
        'vahidler':vahidler,
        'kateqoriyalar':kateqoriyalar,
        
    }
    return render(request,'soft/mehsuldata.html',context)

@login_required(login_url=reverse_lazy('login'))
def mehsulsil(request,id):
    mehsulum = mehsul.objects.get(id = id)
    mehsulum.delete()
    messages.success(request,'mehsul ugurla silindi !',extra_tags='success')
    return HttpResponseRedirect(reverse('mehsullar'))

@login_required(login_url=reverse_lazy('login'))
def mehsulupdate(request,id):
    user = request.user
    mehsulum = mehsul.objects.get(id = id)

    
    try:
        mehsulad = request.POST['mehsuladi']
        mehsulkod = request.POST['mehsulkodu']
        barkod = request.POST['barkod']
        alisqiymet = (request.POST['alisqiymet'])
        satisqiymet = (request.POST['satisqiymet'])
        boyukolcu = vahid.objects.get(vahidad = request.POST['boyukolcu'])
        kicikolcu =  vahid.objects.get(vahidad = request.POST['kicikolcu'])
        boyukinkicik = (request.POST['boyukinkicik'])
        kritikstok = (request.POST['kritikstok'])
        kateqoriya = mehsulkat.objects.get(ktad = request.POST['kateq']) 
        mehsulsekil = None
        print(mehsulad,mehsulkod,barkod,alisqiymet,satisqiymet,boyukolcu,kicikolcu,boyukinkicik,kritikstok,kateqoriya)
        if request.FILES:
            mehsulsekil = request.FILES['sekil']

        if ',' in alisqiymet:
            alisqiymet = float(alisqiymet.replace(',','.'))
        if ',' in satisqiymet:
            satisqiymet = float(satisqiymet.replace(',','.'))
        if ',' in boyukinkicik:
            boyukinkicik = float(boyukinkicik.replace(',','.'))
        if ',' in kritikstok:
            kritikstok = float(kritikstok.replace(',','.'))
            
        #-----------------------------
        mehsulum.mehsulad = mehsulad
        mehsulum.mehsulkod = mehsulkod
        mehsulum.barkod = barkod
        mehsulum.alisqiymet = alisqiymet
        mehsulum.satisqiymet = satisqiymet
        mehsulum.standart = boyukolcu
        mehsulum.ikinci = kicikolcu
        mehsulum.boyukinkicik = boyukinkicik
        mehsulum.kritiksay = kritikstok
        mehsulum.kateqoriya = kateqoriya
        mehsulum.mehsulFoto = mehsulsekil
        mehsulum.save()
        messages.success(request,"secilen mehsulun parametrleri ugurla deyisdirildi ." ,extra_tags='success')
        return HttpResponseRedirect(reverse('mehsullar'))
    except Exception as e:
        messages.success(request,"mehsulu parametrlerinde problem var ."+" "+str(e) ,extra_tags='danger')
        return HttpResponseRedirect(reverse('mehsullar'))
    return HttpResponseRedirect(reverse('mehsullar'))

@login_required(login_url=reverse_lazy('login'))
def satispage(request):
    page = request.GET.get('page',1)
    user = request.user
    qaimeler = qaime.objects.filter().order_by("-tarix")
    musterilerim = musteri.objects.filter(useri=request.user)
    mehsullarim = mehsul.objects.filter(useri = request.user)
    satislarim = satis_.objects.filter(useri = request.user)
    paginator = Paginator(qaimeler,15)
    try:
        qaimeler = paginator.page(page)
    except EmptyPage:
        qaimeler = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        qaimeler = paginator.page(1)
    context = {
        'qaimeler':qaimeler,
        'musteriler':musterilerim,
        'mehsullar':mehsullarim,
        'satislar':satislarim,
        }

    return render(request,'soft/satislar.html',context)


@login_required(login_url=reverse_lazy('login'))
def qiymetMehsul(request):
    if request.POST:
        mehsulid = request.POST['mehsulid']
        mehsulum = mehsul.objects.get(id = int(mehsulid))

        qiymet = {
            'qiymeti':mehsulum.satisqiymet,
            'standart':mehsulum.standart.vahidad,
            'ikinci':mehsulum.ikinci.vahidad,

        }
        return JsonResponse(qiymet)

@login_required(login_url=reverse_lazy('login'))
def qiymetMehsulikinci(request):
    if request.POST:
        mehsulid = request.POST['mehsulid']
        vahiddim = request.POST['vhd']
        mehsulum = mehsul.objects.get(id = int(mehsulid))
        qiymeti = mehsulum.satisqiymet
        boyukinkicik = mehsulum.boyukinkicik
        print(qiymeti,boyukinkicik)
        if mehsulum.standart.vahidad == vahiddim:
            qiymet = {
                'qiymeti':mehsulum.satisqiymet,
                'secilenvhd':vahiddim,
                
            }
            return JsonResponse(qiymet)
        elif mehsulum.ikinci.vahidad == vahiddim:
            qiymet = {
                'qiymeti':mehsulum.satisqiymet * boyukinkicik,
                'secilenvhd':vahiddim,
            }
            return JsonResponse(qiymet)

@login_required(login_url=reverse_lazy('login'))
def musterisatislar(request):
    if request.POST:
        try:
            musteriid = request.POST["musteriid"]
            musterisatis = musteri.objects.get(id  =musteriid )
            qaimelerim  = qaime.objects.filter(musteri=musterisatis,status=True).first()
            satislarim = satis_.objects.filter(useri=request.user , s_musteri = musterisatis,s_qaime=qaimelerim)
            mehsuladlari  = [i.mehsuladi.mehsulad for i in satislarim ]
            satismiqdarlari = [i.satissay for i in satislarim]
            satisvahidleri = [i.vahidi.vahidad for i in satislarim]
            satisqiymetleri = [i.mehsuladi.satisqiymet for i in satislarim]
            endrimler = [i.endrim for i in satislarim]
            if qaime.objects.filter(useri = request.user,musteri=musterisatis,status=True ).first():
                toplam_mebleg = qaime.objects.filter(useri = request.user,musteri=musterisatis,status=True ).first().toplam_tutar
            else:
                toplam_mebleg = 0
            qiymet = {
                'mehsuladlari':mehsuladlari,
                'satismiqdarlari':satismiqdarlari,
                'vahidlerim':satisvahidleri,
                'satisqiymetleri':satisqiymetleri,
                'endrimler':endrimler,
               'toplam_mebleg':toplam_mebleg,
               'musteriadi':musterisatis.adsoyad,
            }
            return JsonResponse(qiymet)
        except Exception as e:
            print(e)
            qiymet = {
                'mehsuladlari':0,
            }
            return JsonResponse(qiymet)

@login_required(login_url=reverse_lazy('login'))
def satis(request):
    qiymet = None
    mehsulum = None
  
    if request.POST:
        try:
            mehsulid = request.POST['mehsulid']
            vahidim = vahid.objects.filter(vahidad=request.POST['vhd']).first()
            musteriid = request.POST['musteriid']
            mehsulum = mehsul.objects.get(id = int(mehsulid))
            musterim = musteri.objects.get(id = int(musteriid))
            miqdarim   = float(request.POST['miqdar'])
            endrim   = float(request.POST['endrim'])
            print(musterim.adsoyad,mehsulum.mehsulad,miqdarim,endrim)
            musterim = musteri.objects.get(id = int(musteriid))  
            print(musteriid)
            print(musterim.adsoyad)
            if mehsulum.stok >= miqdarim:
                if not qaime.objects.filter(useri=request.user , status=True,musteri=musterim):
                    yeni_satis = satis_()
                    yeni_satis.s_musteri = musterim
                    yeni_satis.mehsuladi = mehsulum
                    yeni_satis.satissay = miqdarim
                    yeni_satis.vahidi = vahidim
                    yeni_satis.endrim = endrim
                    yeni_satis.useri = request.user
                    yeni_satis.save()
                else:
                    yeni_satis = satis_()
                    yeni_satis.s_qaime = qaime.objects.filter(useri=request.user , status=True,musteri=musterim).first()
                    yeni_satis.s_musteri = musterim
                    yeni_satis.mehsuladi = mehsulum
                    yeni_satis.satissay = miqdarim
                    yeni_satis.vahidi = vahidim
                    yeni_satis.endrim = endrim
                    yeni_satis.useri = request.user
                    yeni_satis.save()
                if  qaime.objects.filter(useri=request.user,musteri=musterim,status = True).first():
                    toplam_mebleg = qaime.objects.filter(useri = request.user,musteri=musterim,status=True ).first().toplam_tutar
                    print(toplam_mebleg)
            
                qiymet = {
                        'qiymeti':mehsulum.satisqiymet,
                        'yenimehsuladi':yeni_satis.mehsuladi.mehsulad,
                        'yenimehsulmiqdar':yeni_satis.satissay,
                        'yenimehsulvahid':yeni_satis.vahidi.vahidad,
                        'yenimehsulqiymeti':yeni_satis.mehsuladi.satisqiymet,
                        'yenimehsulendrim':yeni_satis.endrim,
                        'toplam_mebleg':toplam_mebleg,
                        
                        }
                return JsonResponse(qiymet)
            else:
                qiymet = {
                'qiymeti':"Bos",       
                }
                return JsonResponse(qiymet)

        except Exception as e:
            print(e)
            qiymet = {
                'qiymeti':0,
            }
            return JsonResponse(qiymet)


@login_required(login_url=reverse_lazy('login'))
def satisiyekunlasdir(request):
    if request.method == 'POST':
        
        try:
            
            sontarix = request.POST['qaimesontarix']
            if  sontarix:
                dateson = datetime.strptime(sontarix, '%Y-%m-%d')
            else:
                dateson = datetime.now()
            aciqlama = request.POST['qaimeaciqlama']            
            print(aciqlama,sontarix)
            musteriid = request.POST['musteriidsi']
            mebleg = float(request.POST['mebleg'])
            musterim = musteri.objects.get(id = musteriid)
            secilen_qaime = qaime.objects.filter(useri= request.user , status = True,musteri=musterim).first()
            secilen_qaime.odenis = mebleg
            if secilen_qaime.toplam_tutar - mebleg == 0:
                secilen_qaime.status = False
            elif secilen_qaime.toplam_tutar - mebleg < 0:
                messages.success(request,"Odenis toplam meblegdencox olmamalidir.",extra_tags='danger')
                return HttpResponseRedirect(reverse('satislar'))
            secilen_qaime.status = False
            secilen_qaime.aciqlama = aciqlama
            secilen_qaime.son_odenis_tarixi = dateson
            secilen_qaime.save()
            messages.success(request,"Satis ugurla yekunlasdirildi.",extra_tags='success')
            satislarim = satis_.objects.filter(useri = request.user, s_qaime = secilen_qaime)
            tarix = datetime.now()
  
            context = {
                'musteri':musterim,
                'qaime':secilen_qaime,
                'satislar':satislarim,
                'indi':tarix,

            }
            return render(request,'soft/invoice.html',context)
        except Exception as e:
            print(e)
            messages.success(request,"Satis zamani problem yarandi."+" " +str(e),extra_tags='danger')
            return HttpResponseRedirect(reverse('satislar'))
       
        

