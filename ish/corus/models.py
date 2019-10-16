from django.db import models
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import *
from django.core.validators import *
from django import forms
# Create your models here.
# Product Table
pc = [('LG','LG'),('HP','HP'),('DELL','DELL'),('LENOVO','LENOVO'),('ACER','ACER'),('ASUS','ASUS')]
class item(models.Model):
    p_id=models.AutoField(primary_key=True)
    p_name=models.CharField(max_length=50)
    price=models.IntegerField(default="")
    company = models.CharField(max_length=30,choices=pc)
    stock=models.IntegerField(default="")
    rating=models.FloatField(default=0)
    crating=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    warranty = models.IntegerField(default="")    
    image=models.ImageField(upload_to="image",default="")
    idate = models.DateField(default=datetime.now())
    def __str__(self):
        return self.p_name
    
#Register table For User
class Uregiser(models.Model):
    u_id     = models.AutoField(primary_key=True)
    u_name   = models.CharField(max_length=50)
    city     = models.CharField(max_length=50)
    area     = models.CharField(max_length=50)
    contect  = models.CharField(max_length=13)
    pincode  = models.IntegerField(default=0)
    email    = models.CharField(max_length=30,unique = True)
    password = models.CharField(max_length=15)
    def __str__(self):
        return self.u_name

engtype = [('Os','Os'),('Cameras','Cameras'),('Hardware','Hardware'),('Server','Server'),('Other','other')]
#engineer Register Tabel
class eregiser(models.Model):
    e_id     = models.AutoField(primary_key=True)
    e_name   = models.CharField(max_length=50)
    contect  = models.CharField(max_length=10)
    e_type   = models.CharField(max_length=30,choices=engtype)
    city     = models.CharField(max_length=30)
    email    = models.CharField(max_length=30,unique = True)
    password = models.CharField(max_length=15)
    feedback = models.FloatField(default=0.0)
    status   = models.IntegerField(default=0)
    def __str__(self):
        return self.e_name

#For Server Order Tabel
companytype = [('LG','LG'),('HP','HP'),('DELL','DELL'),('LENOVO','LENOVO')]
class server(models.Model):
    s_id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(default=0)
    company = models.CharField(max_length=30,choices=companytype,default='')
    u_name = models.CharField(max_length=20,default='')
    switch = models.IntegerField(default=8)
    contact = models.CharField(max_length=13,default='')
    status   = models.IntegerField(default=0)
    def __str__(self):
        return self.company

#Model For Camara Modual
camtype = [('Hikvision','Hikvision'),('CP Plus','CP Plus'),('Zicom','Zicom'),('Sony','Sony'),('Samsung','Samsung'),('AVtech','AVtech')]
vis = [('Day','Day'),('Night','Night')]
class camera(models.Model):
    m_id = models.AutoField(primary_key=True)    
    company = models.CharField(max_length=30,choices=camtype)
    Megapixel = models.IntegerField(default=0)    
    cprice = models.IntegerField(default=0)
    vision = models.CharField(max_length=30,choices=vis,default='') 
    image=models.ImageField(upload_to="image",default="")   
    status   = models.IntegerField(default=0)
    def __str__(self):
        return self.company

#tabel for admin
class head(models.Model):
    a_id = models.AutoField(primary_key=True)
    a_name = models.CharField(max_length=30)
    contect = models.CharField(max_length=10,default="")
    email = models.CharField(max_length=30,unique = True)
    password = models.CharField(max_length=15)  
    def __str__(self):
        return self.a_name

#complain table for complain
cmptype = [('Os','Os'),('Cameras','Cameras'),('Hardware','Hardware'),('Server','Server'),('Other','other')]
class complain(models.Model):
    c_id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(default=0)
    e_id = models.IntegerField(default=0)
    m_id = models.IntegerField(default=0)
    u_name = models.CharField(max_length=30)
    e_name = models.CharField(max_length=30,default="")
    c_type = models.CharField(max_length=30,choices=cmptype)
    company = models.CharField(max_length=30,default="")
    creq = models.IntegerField(default=0)
    c_desc = models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    contect = models.CharField(max_length=10,default="")
    rstatus = models.IntegerField(default=0)
    e_email = models.CharField(max_length=30,null=True)
    image = models.ImageField(upload_to="image",default="")
    cdate = models.DateField(default=datetime.now())
    def __str__(self):
        return self.u_name
    

#transection tabel for report and bills
class transection(models.Model):
    b_id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(default=0)
    c_id = models.IntegerField(default=0)
    e_id = models.IntegerField(default=0)
    m_id = models.IntegerField(default=0)
    s_id = models.IntegerField(default=0)
    u_name = models.CharField(max_length=30)
    company = models.CharField(max_length=30,default="")
    c_desc = models.CharField(max_length=200)
    status = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    tdate = models.DateField(default=datetime.now())
    def __str__(self):
        return self.u_name
   
#order table for store order data
class order(models.Model):
    o_id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(default=0)
    i_id = models.IntegerField(default=0)
    p_id = models.IntegerField(default=0)
    p_name = models.CharField(max_length=30)
    u_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    pay = models.CharField(max_length=128)
    address = models.CharField(max_length=300,default='')
    landmark = models.CharField(max_length=300,default='')
    pincode = models.IntegerField(default=0)
    odate = models.DateField(default=datetime.now())
    unumber = models.IntegerField(default=0)
    def __str__(self):
        return self.u_name

#Model For Video 
class video(models.Model):
    v_id = models.AutoField(primary_key=True)
    v_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="image",default="" ,null=True)
    video = models.FileField(upload_to='videos', null=True, verbose_name="")
    discr = models.CharField(max_length=200)
    def __str__(self):
        return self.v_name

#Model For Cart       
class cart(models.Model):
    i_id = models.AutoField(primary_key=True)
    u_id = models.IntegerField(default=0)
    p_id = models.IntegerField(default=0)
    p_name = models.CharField(max_length=30)    
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    def __str__(self):
        return self.p_name

