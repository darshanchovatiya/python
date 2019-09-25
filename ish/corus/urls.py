from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls import url
from .views import *
app_name = 'corus'
urlpatterns = [
   path('',views.index,name='Index'),
   path('index.html',views.index,name='Index'),
   path('product',views.prod,name='Product'),
   path('product.html',views.prod,name='Product'),   
   path('cart<int:id>',views.scart,name='Product'),
   path('pay',views.pay,name='Product'),
   path('histry',views.histry,name='Histry'),
   path('checkout<int:id>',views.checkout,name='Product'),
   path('cart<int:id>.html',views.scart,name='Product'),
   path('pri<int:id>',views.delee,name='Product'),
   path('qv<int:id>',views.quickview,name='Product'),
   path('qvc<int:id>',views.cquickview,name='Product'),
   path('checkout',views.checkout,name='checkout'),
   path('contact',views.contect,name='Contect'),
   path('about',views.about,name='About Us'),
   path('rating<int:id>',views.rating,name='rating Us'),
   path('regu',views.regu,name='User Reg'),
   path('fp',views.fp,name='Forgot Password'),
   path('rege',views.rege,name='Engineer Reg'),
   path('edit_profile',views.edit_profile,name='User Login'),
   path('login',views.login,name='Engineer Login'),
   path('upload',views.prod_view,name='Product Upload'),
   path('cstatus.html',views.cstatus,name='Complaint status'),
   path('logout',views.logout,name='Logout'),
   #path('engliste',views.engliste,name='engineer list'),
   path('englist.html',views.englist,name='engineer list'),
   path('camord.html',views.camlist,name='engineer list'),
   path('reqe<int:e_id>',views.reqe,name='engineer list'),
   path('englist<int:e_id>',views.dele,name='engineer list'),
   path('videos.html',views.showvideo,name='Video Upload'),
   path('videos<int:id>',views.delee,name='Video Upload'),
   path('compl',views.Comp_view,name='Complaint Page'),
   path('complc<int:id>',views.Comp_cview,name='Complaint Page'),
   path('cmplist.html',views.cmplist,name='Complaint Page'),
   path('vid',views.videolist,name='Complaint Page'),
   path('clist',views.clist,name='Complaint Page for bill'),
   path('bill<int:id>',views.bill,name='Page for bill'),
   path('cbill',views.cbill,name='Page for bill'),
   #path('pri<int:id>',GeneratePDF.as_view(),name='Page for bill'),
   path('aplist<int:id>.html',views.aplist,name='Page for list button'),
   path('aplist<int:id>',views.delprod,name='Page for list button'),
   path('cs',views.serv,name='Page for list camera'),
   path('csc',views.cam,name='Page for list camera'),
   path('slist',views.slist,name='Page for list server'),
   path('csbill<int:id>',views.csbill,name='engineer list'),
   path('csblist',views.csblist,name='engineer list'),
   path('camserbill',views.csblistu,name='engineer list'),
   path('serbill<int:id>',views.serbill,name='engineer list'),
   path('csblist.html',views.csblist,name='engineer list'),
   path('slist.html',views.slist,name='Page for list server'),
   path("GeneratePDF<int:id>", views.GeneratePDF),
   path("BillPrint<int:id>", views.BillPrint),
   path("OrderBill<int:id>", views.OrderBill),
   path("edit_prod<int:id>", views.editp),
   path("location", views.location),
   path("email_check", views.email_check),
   path("mult.html", views.mult),
]