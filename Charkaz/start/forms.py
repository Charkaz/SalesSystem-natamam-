from django import forms



class registerForm(forms.Form):
    ad = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'ad'}), label='fas fa-user' ,max_length=50,required= True)
    soyad = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'soyad'}),max_length = 50,required= True)
    telefon = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'telefon'}),max_length=50 ,label='fas fa-mobile' ,required= True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'email'}),max_length=100,required= True)
    istifadeciadi = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'istifadeci adi'}),max_length=100,required= True)
    sirket = forms.CharField(widget=forms.TextInput(attrs={'class':'input100','placeholder':'sirket adi'}),max_length=50,required=True)
    sifre = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'sifre'}),max_length=50,required= True)
   
class loginForm(forms.Form):
    istifadeci = forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'class':'input100','placeholder':'istifadeci adi'}))
    sifre = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'sifre'}))