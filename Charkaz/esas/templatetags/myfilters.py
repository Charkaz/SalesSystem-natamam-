from django import template
from ..models import  mehsul,qaime

register = template.Library()

def mehsulsay(value):
    mehsulum = mehsul.objects.get(pk = value)
    stok = mehsulum.stok
    boyukinkicik = mehsulum.boyukinkicik
    if not boyukinkicik:
        cavab = 0
    else:
        cavab = stok / boyukinkicik

    return '{}-{}'.format(cavab,mehsulum.ikinci.vahidad)



def mehsulsay2(value):
    mehsulum = mehsul.objects.get(pk = value)
    stok = mehsulum.stok
    boyukinkicik = mehsulum.boyukinkicik
    if not boyukinkicik:
        cavab = 0
    else:
        cavab = stok * boyukinkicik

    return '{}'.format(cavab)


    
def mehsulqiymetdiger(value):
    mehsulum = mehsul.objects.get(pk = value)
    qiymeti = mehsulum.satisqiymet
    boyukinkicik = mehsulum.boyukinkicik
    if not boyukinkicik:
        qiymetim = 0
    else:
        
        qiymetim = round((qiymeti * boyukinkicik),2)
    return qiymetim

def mehsulqiymetdigeralis(value):
    mehsulum = mehsul.objects.get(pk = value)
    qiymeti = mehsulum.alisqiymet
    boyukinkicik = mehsulum.boyukinkicik
    if not boyukinkicik:
        qiymetim = 0
    else:
        #cavab = stok * boyukinkicik
        qiymetim = round((qiymeti / boyukinkicik),2)
    return qiymetim

def qaimeQaliq(value):
    qaimem = qaime.objects.get(id = value)
    toplam = qaimem.toplam_tutar
    odenilen = qaimem.odenis
    yekun = toplam - odenilen
    return yekun

def vurma(miqdar,qiymet):
    return miqdar * qiymet


register.filter('Tutar',vurma)
register.filter('Qaliq',qaimeQaliq)
register.filter('myfil',mehsulsay)
register.filter('myfil2',mehsulsay2)
register.filter('ikinciqiymet',mehsulqiymetdiger)
register.filter('ikinciqiymetalis',mehsulqiymetdigeralis)