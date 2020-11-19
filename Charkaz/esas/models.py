from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.core.exceptions import ValidationError
from datetime import datetime


class logdata(models.Model):
    log_ad = models.CharField(max_length=50,null=True,blank=True)
    tarix  = models.DateTimeField(auto_now_add=True) 


class mehsulkat(models.Model):
    ktad = models.CharField(max_length=50,null=False,blank=False,unique=True)
    useri = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.ktad,self.useri)

class vahid(models.Model):
    vahidad = models.CharField(max_length=50,null=False,blank=False,unique=True)
    useri = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.vahidad,self.useri)


class mehsul(models.Model):
    mehsulad = models.CharField(max_length=60,null=False,blank=False)
    mehsulkod = models.CharField(max_length=50,null=True,blank=True)
    barkod = models.CharField(max_length=50,null=True,blank=True,unique=True)
    alisqiymet = models.FloatField(null=False,blank=False)
    satisqiymet = models.FloatField(null=False,blank=False)
    stok = models.FloatField(null=True,blank=True)
    kateqoriya = models.ForeignKey(mehsulkat,on_delete=models.CASCADE)
    standart  = models.ForeignKey(vahid, null=True,blank=True ,on_delete = models.DO_NOTHING,related_name='standart',db_column='standart')
    ikinci = models.ForeignKey(vahid,null=True,blank=True,on_delete=models.DO_NOTHING,related_name='ikinci',db_column='ikinci')
    boyukinkicik = models.FloatField(null=True,blank=True)
    kritiksay = models.FloatField(null=True,blank=True)
    mehsulFoto = models.ImageField(null = True,blank = True)
    qeydtarix = models.DateTimeField(auto_now_add=True)
    useri = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.mehsulad,self.useri)


def mehsul_update_to_log(sender,instance,created,*args,**kwargs):
    datam = logdata.objects.create(log_ad="mehsul  melumati deyisdirildi")


post_save.connect(mehsul_update_to_log,sender = mehsul)



def mehsul_ikinci_olcu_qeyd(sender,instance,created,*args,**kwargs):
    if created:
        if not instance.ikinci:
            instance.ikinci = instance.standart
            instance.boyukinkicik = 1
            instance.save()
        else:
            print("problem")

post_save.connect(mehsul_ikinci_olcu_qeyd,sender = mehsul)

class musteri(models.Model):
    adsoyad = models.CharField(max_length=150,null=False,blank=False)
    hesab = models.FloatField(null=True,blank=True)
    useri = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.adsoyad


class qaime(models.Model):
    aciqlama              = models.CharField(max_length=250 ,null=True,blank= True)
    toplam_tutar          = models.FloatField(null=True,blank=True,default=0)
    toplam_endrim         = models.FloatField(null=True,blank=True,default=0)
    son_odenis_tarixi     = models.DateField(auto_now_add=True)
    tarix                 = models.DateTimeField(auto_now_add=True)
    status                = models.BooleanField(default=True)
    odenis                = models.FloatField(null=True , blank=True,default=0)
    toplam_endrim_faizle  = models.FloatField(null=True,blank=True,default=0)
    toplam_endrim_aznle   = models.FloatField(null=True,blank=True,default=0)
    musteri           = models.ForeignKey(musteri,on_delete = models.CASCADE,null=True,blank=False)
    useri             = models.ForeignKey(User,on_delete= models.CASCADE,null=True,blank=False)

    def __str__(self):
        return str(self.pk)
 

class satis(models.Model):
    s_qaime   = models.ForeignKey(qaime,on_delete=models.CASCADE,null=True,blank=True)
    s_musteri = models.ForeignKey(musteri,on_delete=models.PROTECT , null=False,blank=False)
    mehsuladi = models.ForeignKey(mehsul,on_delete=models.PROTECT , null=False,blank=False)
    satissay  = models.FloatField(null= False,blank=False)
    vahidi    = models.ForeignKey(vahid,on_delete=models.PROTECT,null=True,blank=True)
    endrim    = models.FloatField(null=True,blank=True)
    tarix     = models.DateTimeField(auto_now_add=True)
    useri     = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=False)

    def __str__(self):
        return "{}-{}-{}".format(self.s_qaime,self.s_musteri,self.mehsuladi)


    def clean(self):
        mehsulum_say  = self.mehsuladi.stok
        if mehsulum_say < self.satissay:
            raise ValidationError("Bazada lazimi miqdarda mehsul yoxdur")
        elif not ((self.vahidi == self.mehsuladi.standart) or (self.vahidi == self.mehsuladi.ikinci)):
            raise ValidationError("Secilen olcu vahidi sizin mehsulunuz ucun uygun deyil")



def satis_to_log(sender,instance,created,*args,**kwargs):
    if created:
        datam = logdata.objects.create(log_ad="satis melumati")


post_save.connect(satis_to_log,sender = satis)


def satis_to_qaime(sender,instance,created,*args,**kwargs):
    if created:
            if not instance.s_qaime:
                qaimem = qaime()
                qaimem.toplam_tutar =  qaimem.toplam_tutar + (instance.satissay * instance.mehsuladi.satisqiymet)
                qaimem.musteri = instance.s_musteri
                qaimem.useri = instance.useri
                qaimem.toplam_endrim_aznle += instance.endrim
                qaimem.toplam_tutar -= qaimem.toplam_endrim_aznle
                qaimem.save()
                instance.s_qaime = qaimem       
                instance.save()
                mehsulum = instance.mehsuladi
                mehsulum.stok -= instance.satissay
                mehsulum.save() 
                print("method1")
            else:
                qaimem = instance.s_qaime
                qaimem.useri = instance.useri
                qaimem.toplam_tutar =  qaimem.toplam_tutar + (instance.satissay * instance.mehsuladi.satisqiymet)
                qaimem.toplam_endrim_aznle += instance.endrim
                qaimem.toplam_tutar -= qaimem.toplam_endrim_aznle
                qaimem.save()
                instance.s_qaime = qaimem   
                instance.save()
                mehsulum = instance.mehsuladi
                mehsulum.stok -= instance.satissay
                mehsulum.save() 
                print("method2")



post_save.connect(satis_to_qaime,sender = satis)