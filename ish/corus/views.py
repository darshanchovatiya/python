from django.shortcuts import *
from .models import item,Uregiser,eregiser
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from django.template import RequestContext
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from corus.forms import *
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from .utils import *
from django.views.generic import View
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.db.models import Avg, Count, Min, Sum
from twilio.rest import Client
#index View
def index(request):
    items = item.objects.all()
    videos =video.objects.all()
    context = {'item' : items,
                'video':videos
    }  
    return render(request,'index.html',context)

#product view
def prod(request):    
    items = item.objects.all()
    cam = camera.objects.all()
    return render(request, 'product.html', locals())

#view for the upload product
def prod_view(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = productu(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Product Upload Successfully!')
            return render(request,'upload.html')
    else:
        form = productu()
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'upload.html',{'form':form})

#view for the Shoping cart
def scart(request,id):
    request.session["cnt"] = 0
    istekler = cart.objects.filter(u_id=request.session["nm"])  
    request.session["gtotal"]=0   
    d=0
    for i in istekler:        
        if i == 0:
            request.session["cnt"] = 0
            request.session["mm"]=1           
        else:
            request.session["cnt"] =request.session["cnt"] + 1
            request.session["gtotal"]=0  
            d = d + i.total
    request.session["gtotal"]=d  
    if request.method=="POST": 
        qty = request.POST.get('quantity','')
        ii = request.POST.get('ii','')
        pid = request.POST.get('pid','')
        dr = cart.objects.get(i_id=ii)
        stk = dr.p_id
        st = item.objects.get(p_id = stk)
        dq = dr.quantity
        ds = st.stock  
        fqty = int(dq) + int(qty)
        ft = dr.price * fqty
        if ds < fqty:
            messages.warning(request,'Product Out Of Stock! only '+str(ds) +' in Stock')
            return render(request,'cart.html',locals())
        else:
            cart.objects.filter(i_id=ii).update(quantity=fqty,total=ft)
            messages.success(request,'Quantity Updated Successfully!')
            istekler = cart.objects.filter(u_id=request.session["nm"])
            x=0
            for i in istekler:
                if i == 0:
                    request.session["mm"]=1
                    del request.session["gtotal"]                    
                else:
                    del request.session["gtotal"]
                    request.session["gtotal"]=0
                    x = x + i.total
            request.session["gtotal"]=x
                #messages.success(request,'Product added Successfully!')
            return render(request,'cart.html',locals())
        return render(request,'cart.html',locals())
    else: 
        for i in istekler:
            if i == 0:
                request.session["mm"]=1
                del request.session["gtotal"]       
        return render(request,'cart.html',locals())
    
#View For Quick View
def quickview(request,id):
    ist = item.objects.filter(p_id=id)
    if cart.objects.filter(p_id = id,u_id = request.session["nm"]).exists() :
        request.session["dis"]=1
        messages.warning(request,'Product alrady in to cart!')
        return render(request,'qv.html',locals())
    else:
        request.session["dis"]=""         
        storage = messages.get_messages(request)
        storage.used = True
        if request.method == 'POST':
            form = product(request.POST,request.FILES)
            if form.is_valid():                
                pd = item.objects.get(p_id = id)               
                p_nm = pd.p_name
                p_pr = pd.price
                pst = pd.stock
                #request.session["chk"]=item.objects.get(p_id = id)
                quickview=form.save(commit=False)
                quickview.p_id=id
                quickview.u_id=request.session["nm"]
                quickview.p_name=p_nm
                quickview.quantity=1
                quickview.price=p_pr
                quickview.stock = pst
                quickview.total=p_pr
                quickview.save()
                messages.success(request,'Product added in to cart!')
                return render(request,'qv.html',locals())
            else:
                form = product()   
                return render(request, 'qv.html',  locals(), {'form':form})
        cam = camera.objects.filter(m_id = id)        
        return render(request, 'qv.html',  locals())

#View For Camara Quick View 
def cquickview(request,id):
    cam = camera.objects.filter(m_id=id)
    return render(request, 'qvc.html',  locals())

#view for checkout
def checkout(request,id):
    request.session['sa'] = ''
    storage = messages.get_messages(request)
    storage.used = True
    udata=Uregiser.objects.get(u_id=request.session["nm"])
    u_name = udata.u_name
    email = udata.email
    address = udata.area
    request.session["cnm"] = u_name
    request.session["ceml"] = email   
    pdata=cart.objects.filter(u_id =id)    
    name = ''      
    if request.method == 'POST':
        form = ord(request.POST,request.FILES)
        if form.is_valid():
            popt = request.POST.get('pay','')
            checkout=form.save(commit=False)
            for i in pdata:
                checkout.pk = None 
                checkout.p_id = i.p_id               
                checkout.u_id = request.session["nm"]
                checkout.i_id = id
                checkout.p_name=i.p_name
                checkout.u_name=u_name
                checkout.email=email
                checkout.pay = popt
                checkout.price=request.session["gtotal"] 
                checkout.save() 
                dst=item.objects.get(p_id =i.p_id)  
                request.session['rat'] =  dst.p_id
                stk = dst.stock
                fstk = stk - i.quantity       
                item.objects.filter(p_id = i.p_id).update(stock = fstk)
            cart.objects.filter(u_id = request.session["nm"]).delete()
            del request.session["gtotal"]
            request.session['sa'] = 1
            messages.success(request,'Your Order Placed!')
            return render(request,'checkout.html')
        return render(request,'checkout.html',{'form':form})
    else:
        form = ord()
        del request.session['sa'] 
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'checkout.html',{'form':form})
    #return HttpResponse("This Is our checkout.")

# view for contect page
def contect(request):
    return render(request,'contact.html')

# View For Product Rating
def rating(request,id):
    if request.method == 'POST':
        pid = request.POST.get('pid','')
        rat = request.POST.get('stars','')
        dr=item.objects.get(p_id = id)
        rate = dr.rating 
        if rate != 0:             
            crat = dr.crating + 1
            frat = float(rat) + float(rate)
            lrate = frat/2        
        else:
            crat = 1 
            lrate = rat 
        item.objects.filter(p_id = id).update(rating=lrate,crating = crat )
        messages.success(request,'Thanks For Ratting!')
        messages.success(request,'Thanks For Ratting!')
        return redirect('product.html')
    return render(request,'rating.html')

# View For Payment
def pay(request):
    d = item.objects.all()
    return render(request,'pay.html',locals())

#view for about pages
def about(request):
    return render(request,'about.html')

#view for registration of user
def regu(request):
    if request.method=="POST":
        name = request.POST.get('myName','')
        City = request.POST.get('City','')
        Pincode = request.POST.get('Pincode','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address','')
        email = request.POST.get('email','')
        Password = request.POST.get('Password','')
        if Uregiser.objects.filter(email = email).exists():            
            if eregiser.objects.filter(contect = phone).exists():
                messages.warning(request,f'Your Email and Phone Number Alrady Exists! Please Try Using Another')
            else:
                messages.warning(request,f'Your Email Alrady Exists! Please Try Using Another')
            return render(request,'regu.html')

        elif eregiser.objects.filter(email = email).exists():
            if eregiser.objects.filter(contect = phone).exists():
                messages.warning(request,f'Your Email and Phone Number Alrady Exists as a engineer! Please Try Using Another')
            else:
               messages.warning(request,f'Your Email Alrady Exists in Engineer! Please Try Using Another')
            return render(request,'regu.html')
        elif head.objects.filter(email = email).exists():
            messages.warning(request,f'This email alrady reserverd for admin! Please Try Using Another')
            return render(request,'rege.html')
        elif Uregiser.objects.filter(contect = phone).exists():
            messages.warning(request,f'Your Mobile Number Alrady Registered!')
            return render(request,'regu.html')
        elif eregiser.objects.filter(contect = phone).exists():
            messages.warning(request,f'Your Mobile Number Alrady Registered!')
            return render(request,'regu.html')
        else:    
            reg = Uregiser(u_name=name,city=City,area=address,contect=phone,pincode=Pincode,email=email,password=Password)
            reg.save()
            messages.success(request,'Account is Created !'+name)
            subject = 'IT SOLUTION HUB'
            message = ' Thanks For Registeation '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'regu.html')
    else:
        #messages.warning(request,f'Somthing Might Be Wrong Please Tray Again Later!')
        return render(request,'regu.html')
    return render(request,'regu.html')

#view for engineer register
def rege(request):
    if request.method=="POST":
        name = request.POST.get('myName','')
        City = request.POST.get('City','')
        etype = request.POST.get('type','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        Password = request.POST.get('Password','')
        if eregiser.objects.filter(email = email).exists():
            if eregiser.objects.filter(contect = phone).exists():
                messages.warning(request,f'Your Email and Phone Number Alrady Exists! Please Try Using Another')
            else:
                messages.warning(request,f'Your Email Alrady Exists! Please Try Using Another')
            return render(request,'rege.html')
        elif Uregiser.objects.filter(email = email).exists():
            if Uregiser.objects.filter(contect = phone).exists():
                messages.warning(request,f'Your Email and Phone Number Alrady Exists as a user! Please Try Using Another')
            else:
                messages.warning(request,f'Your Email Alrady Exists as a ! Please Try Using Another')
            return render(request,'rege.html')
        elif head.objects.filter(email = email).exists():
            messages.warning(request,f'This email alrady reserverd for admin! Please Try Using Another')
            return render(request,'rege.html')
        elif eregiser.objects.filter(contect = phone).exists():
            messages.warning(request,f'Your Mobile Number Alrady Registered!')
            return render(request,'rege.html')
        elif Uregiser.objects.filter(contect = phone).exists():
            messages.warning(request,f'Your Mobile Number Alrady Registered as a !')
            return render(request,'rege.html')
        else:    
            reg = eregiser(e_name=name,city=City,e_type=etype,contect=phone,email=email,password=Password)
            reg.save()            
            messages.success(request,'your account created! Wait For Approval to Login '+name)
            subject = 'IT SOLUTION HUB'
            message = ' Thanks For Registeation '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'rege.html')
    else:
        #messages.warning(request,f'Somthing Might Be Wrong Please Tray Again Later!')
        return render(request,'rege.html')
    return render(request,'rege.html')

#view for login. login for everyone
def login(request):
    if request.method == 'POST':
        if eregiser.objects.filter(email=request.POST['email'],password=request.POST['Password']).exists():
            loge = eregiser.objects.get(email=request.POST['email'],password=request.POST['Password'])
            if loge.status == 0:
                messages.warning(request,'Your approval is panding')
                return render(request,'login.html',{'dae':loge})
            else:
                request.session["lgne"] ='Welcome' + loge.e_name    
                request.session["prof"] = loge.email 
                request.session["type"] = loge.e_type
                request.session["acc"] = loge.e_name 
                request.session["eid"] = loge.e_id   
                return redirect('index.html')
        elif Uregiser.objects.filter(email=request.POST['email'],password=request.POST['Password']).exists():
            loge = Uregiser.objects.get(email=request.POST['email'],password=request.POST['Password'])
            request.session["lgnu"] ='Welcome' + loge.u_name    
            request.session["prof"] = loge.email  
            request.session["nm"] = loge.u_id 
            request.session["unm"] = loge.u_name  
            return redirect('index.html') 
        elif head.objects.filter(email=request.POST['email'],password=request.POST['Password']).exists():
            loge = head.objects.get(email=request.POST['email'],password=request.POST['Password'])
            request.session["lgna"] ='Welcome' + loge.a_name 
            request.session["prof"] = loge.email   
            request.session["cont"] = loge.email    
            request.session['contt'] = loge.contect       
            return redirect('index.html') 
        else:
            request.session.modified = True
            messages.warning(request,'Invalid Username Or Password')
            return render(request,'login.html')
    return render(request,'login.html')

#view for logout
def logout(request):
    request.session.modified = True
    request.session.flush()
    request.session.modified = True
    return redirect('index.html')

#view for forgot password for all users.
def fp(request):
    if request.method == 'POST':  
         email= request.POST.get('email','')
         if eregiser.objects.filter(email=request.POST['email']).exists():
            u = eregiser.objects.get(email=request.POST['email'])
            password=u.password
            subject = 'Recover your password'
            message = 'Your Password is :'+ password
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request,'Your Password Sent Successfully')
            return render(request,'fp.html')
         elif Uregiser.objects.filter(email=request.POST['email']).exists():
              u = Uregiser.objects.get(email=request.POST['email'])
              password=u.password
              subject = 'Recover your password'
              message = 'Your Password is :'+ password
              email_from = settings.EMAIL_HOST_USER
              recipient_list = [email]
              send_mail( subject, message, email_from, recipient_list )
              messages.success(request,'Your Password Sent Successfully')
              return render(request,'fp.html')
         elif head.objects.filter(email=request.POST['email']).exists():
              u = head.objects.get(email=request.POST['email'])
              password=u.password
              subject = 'Recover your password'
              message = 'Your Password is :'+ password  
              email_from = settings.EMAIL_HOST_USER
              recipient_list = [email]
              send_mail( subject, message, email_from, recipient_list )
              messages.success(request,'Your Password Sent Successfully')
              return render(request,'fp.html')
         else:
             messages.warning(request,'Your email is not exists.')
             return render(request,'fp.html')
    else:
       return render(request,'fp.html')

#view for edit profile for all users
def edit_profile(request):
    if Uregiser.objects.filter(email=request.session["prof"]).exists():
            user = Uregiser.objects.get(email=request.session["prof"])
            form = editprofile(instance=user)
            if request.method == "POST":
                form = editprofile(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    update = form.save(commit=False)               
                    update.user = user
                    update.save()
                    messages.success(request,'Profile Update Successfully')
    elif eregiser.objects.filter(email=request.session["prof"]).exists():
            user = eregiser.objects.get(email=request.session["prof"])
            form = engprofile(instance=user)
            if request.method == "POST":
                form = engprofile(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    update = form.save(commit=False)               
                    update.user = user
                    update.save()
                    messages.success(request,'Profile Update Successfully')
                    #return render(request, 'profileu.html')
    elif head.objects.filter(email=request.session["prof"]).exists():
            user = head.objects.get(email=request.session["prof"])
            form = headprofile(instance=user)
            if request.method == "POST":
                form = headprofile(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    update = form.save(commit=False)               
                    update.user = user
                    update.save()
                    messages.success(request,'Profile Update Successfully')
                    #return render(request, 'profileu.html')
    return render(request, 'edit_profile.html', {'form': form})
   
#view for engineer list
def englist(request):  
    istekler = eregiser.objects.all()
    return render(request, 'englist.html', locals())

#view for delete engineer request
def dele(request, e_id):    
    if video.objects.filter(v_id=e_id).exists():
        video.objects.get(v_id=e_id).delete()
        messages.success(request,'Video Deleted')
        return redirect('videos.html') 
    elif server.objects.filter(s_id=e_id).exists():
        server.objects.get(s_id=e_id).delete()
        messages.warning(request,'Order Rejected')
        return redirect("slist.html")
    elif eregiser.objects.filter(e_id=e_id).exists():
        eregiser.objects.get(e_id=e_id).delete()
        messages.warning(request,'Rejected Successfully')
        return redirect('englist.html')
    
#view for accept engineer, Complaint and Server Order
def reqe(request,e_id):    
    if complain.objects.filter(c_id=e_id).exists():
        d= complain.objects.get(c_id = e_id)
        if d.m_id == 0:
            complain.objects.filter(c_id=e_id).update(status=1,e_email=request.session["prof"],e_id=request.session["eid"],e_name=request.session["acc"])
            messages.success(request,'Complaint accepted')
        else:
            complain.objects.filter(c_id=e_id).update(status=1,contect=request.session['contt'])
            messages.success(request,'Oreder accepted')
        return redirect('cmplist.html')
    elif eregiser.objects.filter(e_id=e_id).exists():
        eregiser.objects.filter(e_id=e_id).update(status=1)
        el = eregiser.objects.get(e_id=e_id)
        email = el.email
        subject = 'IT SOLUTION HUB'
        message = ' You are apporve by IT solution hub Now you can login in our site '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,'Engineer Approved Successfully')
        return redirect('englist.html')
    elif server.objects.filter(s_id = e_id).exists():
        server.objects.filter(s_id = e_id).update(status=1)
        messages.success(request,'Oreder accepted')
        return redirect('slist.html')

#View For Video Upload For Home Page
def showvideo(request): 
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form= VideoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()    
            messages.success(request,'Product Upload Successfully!')
            return render(request,'videos.html') 
    else:
        form = VideoForm()
        #messages.error(request,f'Somthing might be wrong!')
        ist = video.objects.all()
        return render(request,'videos.html',locals())
    return render(request,'videos.html',{'form':form})  

#View For Video List
def videolist(request):  
    ist = video.objects.all()
    return render(request, 'vid.html', locals())    

#view for delete Product into the cart and video delete. 
def delee(request,id):    
    if cart.objects.filter(i_id = id).exists():
        cart.objects.get(i_id=id).delete()
        del request.session["gtotal"]
        messages.warning(request,' Product Removed')
        return redirect('cart0.html')
    elif video.objects.filter(v_id=id).exists():
        video.objects.get(v_id=id).delete()
        messages.warning(request,' Video Deleted')
        return redirect('videos.html')
    elif complain.objects.filter(c_id=id).exists():
        complain.objects.get(c_id=id).delete()
        messages.warning(request,' Contacetet Deleted')
        return redirect('camord.html')
    

#Complain Interfase
def Comp_view(request):
    request.session["cmpl"] = 0
    storage = messages.get_messages(request)
    storage.used = True
    ctype = request.POST.get('type','')
    if request.method == 'POST':
        form = comp(request.POST,request.FILES)                
        if form.is_valid():
            Comp_view = form.save(commit=False)
            Comp_cview.c_type = ctype
            Comp_view.u_id =request.session["nm"]
            Comp_view.u_name = request.session["unm"]
            Comp_view.save()
            request.session["cmpl"] = 1
            #client = Client("ACxxxxxxxxxxxxxx", "zzzzzzzzzzzzz")
            #recipients = eregiser.objects.filter(e_type=ctype)
            #for i in recipients:
            #    client.messages.create(to="+919429292340", 
            #           from_="+916355037177", 
            #           body="Hello My Love!")
            messages.success(request,'Complaint Sent Successfully!')
            return render(request,'compl.html')
    else:
        form = comp()
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'compl.html',{'form':form})

#View For Camara Order
def Comp_cview(request,id):
    storage = messages.get_messages(request)
    storage.used = True
    dr = camera.objects.get(m_id = id)
    if request.method == 'POST':
        form = compc(request.POST,request.FILES)                
        if form.is_valid():
            Comp_cview = form.save(commit=False)
            Comp_cview.u_id =request.session["nm"]
            Comp_cview.u_name = request.session["unm"]
            Comp_cview.m_id = id
            Comp_cview.company = dr.company
            Comp_cview.save()
            messages.success(request,'Your order For camara is sent!')
            return render(request,'complc.html')
    else:
        form = compc()
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'complc.html',{'form':form})


def camlist(request):
    istekler = complain.objects.all() 
    drc = Uregiser.objects.all()  
    return render(request,'camord.html',locals())

#View Fro Complaint List
def cmplist(request):  
    istekler = complain.objects.all()
    return render(request, 'cmplist.html', locals()) 

#View For Video List
def videolist(request):  
    istekler = video.objects.all()
    return render(request, 'videos.html', locals())

#View For Complaint Status And Engineer Feedback
def cstatus(request):
    istekler = complain.objects.filter(u_id = request.session["nm"])
    if request.method == 'POST':
        rat = request.POST.get('stars','')
        cid = request.POST.get('cid','')
        dr=complain.objects.get(c_id = cid)
        eid = dr.e_id
        ds=eregiser.objects.get(e_id = eid)        
        rate = ds.feedback        
        frat = float(rat) + float(rate)
        lrate = frat/2
        request.session['lrat']=lrate
        eregiser.objects.filter(e_id = eid).update(feedback=lrate)
        complain.objects.filter(c_id = cid).update(rstatus=1)
        messages.success(request,'Thanks For Ratting!')
        return redirect('cstatus.html')    
    return render(request,'cstatus.html',locals())

#View For Complaint List For Engineer
def clist(request):
    istekler = complain.objects.filter(e_email = request.session["prof"])
    return render(request, 'clist.html', locals()) 

#View For Bill of complaint
def bill(request,id):
    storage = messages.get_messages(request)
    storage.used = True
    dd = complain.objects.get(c_id=id)
    unm = dd.u_name
    eml = dd.e_email
    uid = dd.u_id
    #de = Uregiser.objects.get(u_id=uid)
    #eml = de.email
    if request.method == 'POST':
            form = compbill(request.POST,request.FILES)
            if form.is_valid():
                complain.objects.filter(c_id=id).update(status=2)
                bill=form.save(commit=False)                  
                bill.c_id = id
                bill.u_name = unm
                bill.email = eml
                bill.u_id = uid
                bill.e_id = request.session["eid"]
                bill.save()
                messages.success(request,'Bill Sent Successfully!')
                return render(request,'bill.html')
    else:
        form = compbill()
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'bill.html',{'form':form})

#View For Camara and Server Bills
def csbill(request,id):
    prc = request.POST.get('prc','')
    request.session['disp'] = 1
    cqt = request.POST.get('cqt','')
    storage = messages.get_messages(request)
    storage.used = True
    if camera.objects.filter(m_id = id).exists(): 
        dd = camera.objects.get(m_id = id)
        dr = complain.objects.filter(m_id = id)
        for i in dr:
            if dd.m_id == i.m_id:
                unm = i.u_name
                uid = i.u_id
                tpric = i.creq * dd.cprice
        if request.method == 'POST':
                form = cobill(request.POST,request.FILES)
                if form.is_valid():
                    csbill=form.save(commit=False) 
                    csbill.u_id = uid 
                    csbill.m_id = id 
                    csbill.company = dd.company 
                    csbill.u_name = unm 
                    csbill.total = int(prc)+int(tpric)
                    csbill.save()  
                    complain.objects.filter(m_id = id).update(status = 2)
                    request.session['disp'] = 0           
                    messages.success(request,'Bill Sent Successfully!')
                    return render(request,'csbill.html')
        else:
            form = cobill()   
            #messages.error(request,f'Somthing might be wrong!')
        return render(request,'csbill.html',{'form':form})
    

def serbill(request,id):
    if server.objects.filter(s_id = id).exists():
        uu=server.objects.get(s_id = id)
        if request.method == 'POST':
                form = csobill(request.POST,request.FILES)
                if form.is_valid():
                    csbill=form.save(commit=False)
                    csbill.u_id=uu.u_id  
                    csbill.u_name=uu.u_name
                    csbill.company=uu.company
                    csbill.s_id=uu.s_id 
                    csbill.save()    
                    server.objects.filter(s_id = id).update(status=2)            
                    messages.success(request,'Bill Sent Successfully!')
                    return render(request,'csbill.html')
        else:
            form = csobill()
            #messages.error(request,f'Somthing might be wrong!')
        return render(request,'csbill.html',{'form':form})
#View For Camara And Server bill list
def csblist(request):
    istekler = complain.objects.all()
    ser = server.objects.all()
    use = Uregiser.objects.all()
    return render(request, 'csblist.html', locals()) 

def csblistu(request):
    istekler = transection.objects.filter(u_id=request.session["nm"])
    ser = server.objects.filter(u_id=request.session["nm"])
    use = Uregiser.objects.get(u_id=request.session["nm"])
    return render(request, 'camserbill.html', locals()) 
#View For List Bill For Customer
def cbill(request):
    istekler = transection.objects.filter(u_id = request.session["nm"])
    dr = camera.objects.all()
    return render(request, 'cbill.html', locals()) 

#View For List All Tabels For Admin
def aplist(request,id):
    fdate = request.POST.get('fdate','')
    ldate = request.POST.get('ldate','')
    if id == 1:
        request.session["lstad"]="englist" 
        istekler = eregiser.objects.all()           
    elif id ==2:
        request.session["lstad"]="userlist" 
        ulist = Uregiser.objects.all()  
    if fdate == '' and ldate == '':                     
        if id == 3:                  
            request.session["lstad"]="itemlist" 
            ilist = item.objects.all()
            if request.method=="POST": 
                qty = request.POST.get('add','')
                pid = request.POST.get('pid','')
                if pid !='' and qty != '':
                    st = item.objects.get(p_id = pid)
                    ds = st.stock  
                    fqty = int(ds) + int(qty)
                    item.objects.filter(p_id=pid).update(stock = fqty)
                    ilist = item.objects.all()
                    messages.success(request,'Stock Added!')
                return render(request, 'aplist.html',locals())              
        elif id == 4:
            request.session["lstad"]="cmplist"
            clist = complain.objects.all()        
        elif id == 5:
            request.session["lstad"]="tralist"
            tlist = transection.objects.all()   
        elif id == 6:
            request.session["lstad"]="ordlist"
            olist = order.objects.all()   
        return render(request, 'aplist.html',locals()) 
    else: 
        request.session["dsp"]="1"              
        if id == 3:
            request.session["lstad"]="itemlist" 
            ilist = item.objects.filter(idate__range=(fdate,ldate))
            if request.method=="POST": 
                qty = request.POST.get('add','')
                pid = request.POST.get('pid','')
                if pid !='' and qty != '':
                    st = item.objects.get(p_id = pid)
                    ds = st.stock  
                    fqty = int(ds) + int(qty)
                    item.objects.filter(p_id=pid).update(stock = fqty)
                    ilist = item.objects.all()
                    messages.success(request,'Stock Added!')
                return render(request, 'aplist.html',locals())           
        elif id == 4:
            request.session["lstad"]="cmplist"
            clist = complain.objects.all(cdate__range=(fdate,ldate))        
        elif id == 5:
            request.session["lstad"]="tralist"
            tlist = transection.objects.all(tdate__range=(fdate,ldate))   
        elif id == 6:
            request.session["lstad"]="ordlist"
            olist = order.objects.filter(odate__range=(fdate,ldate))   
        return render(request, 'aplist.html',locals()) 

#View For Print Tabels
def GeneratePDF(request,id,*args, **kwargs):                
        if id == 1:           
            request.session["pf"]="englist" 
            x = request.session["pf"]
            d = eregiser.objects.all() 
            context = {
                'd':d,
                'x':x,                
            }
        elif id == 2:
            request.session["pf"]="userlist"
            x = request.session["pf"]
            d = Uregiser.objects.all() 
            context = {
                'd':d,
                'x':x
            }  
        elif id == 3:           
            x =  "itemlist"
            d = item.objects.all() 
            context = {
                'd':d,
                'x':x
            } 
        elif id == 4:
            x ="cmplist"             
            d = complain.objects.all() 
            context = {
                'd':d,
                'x':x
            } 
        elif id == 5:            
            x =  "tralist"
            d = transection.objects.all() 
            context = {
                'd':d,
                'x':x
            } 
        elif id == 6:           
            x =  "ordlist"
            d = order.objects.all() 
            context = {
                'd':d,
                'x':x
            }  
        
        template = get_template('invioce.html')      
        html = template.render(context)
        pdf = render_to_pdf('invioce.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

#View For Complaint Bill
def BillPrint(request,id,*args, **kwargs): 
        d = transection.objects.get(b_id = id)
        x = d.c_id
        y= 0
        c = 0
        
        if d.c_id != 0 and d.e_id != 0:
            x = 0
            y = complain.objects.get(c_id = d.c_id)
            c = eregiser.objects.get(e_id = d.e_id) 
        elif d.m_id != 0:
            x = 1
            y = camera.objects.get(m_id = d.m_id)
        elif d.s_id !=0:
            x = 2
            y =server.objects.get(s_id = d.s_id) 
        context = {
                    'd':d, 
                    'y':y,               
                    'c':c, 
                    'x':x,                   
                    'date':datetime.now()
        }
        template = get_template('BillPrint.html')      
        html = template.render(context)
        pdf = render_to_pdf('BillPrint.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

#VIew For Product BillS
def OrderBill(request,id,*args, **kwargs): 
        d = order.objects.get(o_id = id)
        context = {
                    'd':d,                                   
                    'date':datetime.now()
        }       
        template = get_template('OrderBill.html')      
        html = template.render(context)
        pdf = render_to_pdf('OrderBill.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

# VIew FOr History For Customer
def histry(request):
    olist = order.objects.filter(u_id=request.session["nm"]) 
    if request.method == 'POST':
        pid = request.POST.get('pid','')
        rat = request.POST.get('stars','')
        dr=item.objects.get(p_id = pid)
        rate = dr.rating              
        crat = dr.crating + 1
        frat = float(rat) + float(rate)
        lrate = frat/2        
        request.session['lrat']=lrate
        item.objects.filter(p_id = pid).update(rating=lrate,crating = crat )
        messages.success(request,'Thanks For Ratting!')
        return redirect('product.html')
    return render(request, 'histry.html',locals()) 

#View For Server Order
def serv(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = ser(request.POST,request.FILES)
        if form.is_valid():
            cam = form.save(commit=False)
            cam.u_id =  request.session["nm"]
            cam.u_name = request.session["unm"]
            cam.save()
            messages.success(request,'Order is Sent!')
            return render(request,'cs.html')
    else:
        form = ser()
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'cs.html',{'form':form})

#View For Camara Order
def cam(request):
    storage = messages.get_messages(request)
    storage.used = True
    if request.method == 'POST':
        form = came(request.POST,request.FILES)
        if form.is_valid():
            form.save()            
            messages.success(request,'Camera Price Uploaded!')
            return render(request,'csc.html')
    else:
        form = came()
        #messages.error(request,f'Somthing might be wrong!')
    return render(request,'csc.html',{'form':form})

#View For Server List
def slist(request):
    cdr = server.objects.all()
    cdg = Uregiser.objects.all()
    return render(request,'slist.html',locals())

def editp(request , id):
    if item.objects.filter(p_id=id).exists():
            user = item.objects.get(p_id=id)
            form = editprod(instance=user)
            if request.method == "POST":
                form = editprod(request.POST, request.FILES, instance=user)
                if form.is_valid():
                    update = form.save(commit=False)               
                    update.user = user
                    update.save()
                    messages.success(request,'Profile Update Successfully')
    else:
        form = editprod()
    return render(request, 'edit_profile.html', {'form': form})

def delprod(request , id):
    if item.objects.filter(p_id=id).exists():
        item.objects.get(p_id=id).delete()
        messages.warning(request,' Product Deleted')
        return redirect('aplist3.html')

def location(request):
    return render(request,'location.html')

def email_check(request):
    email = request.POST.get('email', False)
    if request.is_ajax():
        if email:
            query_email = Uregiser.objects.filter(email=email)
            e_email = eregiser.objects.filter(email=email)
            h_email = head.objects.filter(email=email)
            if query_email.exists():
                res = "{0} is already in use.".format(email)
            elif e_email.exists():
                res = "{0} is already in use.".format(email)
            elif h_email.exists():
                res = "{0} is already in use.".format(email)
            else:
                res = "This E-mail is ok."
            ajax_vars = {'response': res, 'email': email}
            json_data = json.dumps(ajax_vars)
        else:
            res = "This field is required."
            ajax_vars = {'response': res, 'email': email}
            json_data = json.dumps(ajax_vars)

        return HttpResponse(json_data, content_type='application/json')

def mult(request):
    d = complain.objects.filter(u_id=request.session["nm"])  
    storage = messages.get_messages(request)
    storage.used = True    
    if request.method == 'POST':
        form = mord(request.POST,request.FILES)
        if form.is_valid():   
            instance = form.save(commit=False)         
            for n in d:                
                instance.pk = None
                instance.save()
                messages.success(request,'Product Upload Successfully!')
            return render(request,'mult.html')
    else:
        form = mord()
                #messages.error(request,f'Somthing might be wrong!')
    return render(request,'mult.html',{'form':form})