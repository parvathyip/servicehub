from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import datetime,date
from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def users_login(request):
    if request.POST:
        uname=request.POST['uname']
        password=request.POST['password']
        user=authenticate(username=uname,password=password)
        if user is not None:
            if user.user_type=='admin':
                msg=messages.success(request,'Welcome to admin dashboard')
                return redirect('/admin-dashboard')
            elif user.user_type=='user':
                msg=messages.success(request,'Welcome to user dashboard')
                userregid=user
                userid=UserReg.objects.get(user_login=userregid).id
                request.session['uid']=userid
                return redirect('/user-dashboard')
            elif user.user_type=='hub':
                msg=messages.success(request,'Welcome to Servicehub dashboard')
                hubregid=user
                hubid=ServicehubReg.objects.get(hub_login=hubregid).id
                request.session['hid']=hubid
                return redirect('/hub-dashboard')
        else:
            msg=messages.success(request,'Invalid Login again')
            return redirect('/users-login')
    return render(request,'users_login.html')

#admin
def admin_dashboard(request):
    hubs=ServicehubReg.objects.filter(hub_login__is_active=1)
    return render(request,'admin/admin_dashboard.html',{"hubs":hubs})

def admin_addbrand(request):
    if request.POST:
        bname=request.POST['brandname']
        if Brand.objects.filter(brandname__iexact=bname).exists():
            msg=messages.success(request,'Brandname already added')
            return redirect('/admin-addbrand')
        else:
            brand=Brand.objects.create(brandname=bname)
            brand.save()
            msg=messages.success(request,'Brandname added sucessfully')
            return redirect('/admin-addbrand')
    brands=Brand.objects.all()
    return render(request,'admin/admin_addbrand.html',{"brands":brands})

def admin_updatebrand(request):
    brandid=request.GET.get('brandid')
    # print(brandid)
    brand=Brand.objects.get(id=brandid)
    if request.POST:
        bname=request.POST['brandname']
        brand=Brand.objects.filter(id=brandid).update(brandname=bname)
        msg=messages.success(request,'Brandname updated sucessfully')
        return redirect('/admin-addbrand')
    return render(request,'admin/admin_updatebrand.html',{"brand":brand})

def admin_deletebrand(request):
    brandid=request.GET.get('brandid')
    # print(brandid)
    brand=Brand.objects.filter(id=brandid).delete()
    msg=messages.success(request,'Brandname deleted sucessfully')
    return redirect('/admin-addbrand')
        
def admin_approvehub(request):
    hubs=ServicehubReg.objects.filter(hub_login__is_active=0)
    # print(hubs)
    hubbrands=HubBrands.objects.all()
    return render(request,'admin/admin_approvehub.html',{"hubs":hubs,"hubbrands":hubbrands})

def admin_approveeachhub(request):
    hubid=request.GET.get('hid')
    hub=ServicehubReg.objects.get(id=hubid).hub_login.id
    hublogin=Login.objects.filter(id=hub).update(is_active=1)
    # print(hubid)
    msg=messages.success(request,'Servicehub approved sucessfully')
    return redirect('/admin-viewapprovedhubs')

def admin_rejecteachhub(request):
    # print('reject')
    hubid=request.GET.get('hid')
    # print(hubid)
    hub=ServicehubReg.objects.get(id=hubid).hub_login.id
    hublogin=Login.objects.filter(id=hub).update(is_active=0)
    msg=messages.success(request,'Servicehub rejected sucessfully')
    return redirect('/admin-viewapprovedhubs')

def admin_viewapprovedhubs(request):
    hubs=ServicehubReg.objects.filter(hub_login__is_active=1)
    # print(hubs)
    return render(request,'admin/admin_viewapprovedhubs.html',{"hubs":hubs})

def admin_viewsinglehub(request):
    hubid=request.GET.get('hid')
    # print(hubid)
    hub=ServicehubReg.objects.get(id=hubid)
    services=Serviceproducts.objects.filter(hubbrands__hub_id=hubid).order_by("productname")
    # print(services)
    hubbrands=HubBrands.objects.all()
    return render(request,'admin/admin_viewsinglehub.html',{"hub":hub,"hubbrands":hubbrands,"services":services})

def admin_message(request):
    hubs=ServicehubReg.objects.filter(hub_login__is_active=1)
    # print(hubs)
    return render(request,'admin/admin_message.html',{"hubs":hubs})

def admin_hubchat(request):
    hubid=request.GET.get('hid')
    hub=ServicehubReg.objects.get(id=hubid)
    if request.POST:
        adminmsg=request.POST['umsg']
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        msgadd=Message.objects.create(hub=hub,message=adminmsg,chatdate=dt_string)
        msgadd.save()
    chats=Message.objects.filter(hub=hub)
    return render(request,'admin/admin_hubchat.html',{"hub":hub,"chats":chats})

def admin_viewusers(request):
    users=UserReg.objects.all()
    return render(request,'admin/admin_viewusers.html',{'users':users})

def admin_viewsingleuser(request):
    userid=request.GET.get('uid')
    udata=UserReg.objects.get(id=userid)
    return render(request,'admin/admin_viewsingleuser.html',{'udata':udata})

def admin_deleteuser(request):
    userid=request.GET.get('uid')
    udata=UserReg.objects.get(id=userid).user_login.id
    userdelete=Login.objects.filter(id=udata).delete()
    msg=messages.success(request,'User deleted sucessfully')
    return redirect('/admin-viewusers')

def admin_viewpayments(request):
    complaints=Complaint.objects.filter(complaint_status='Completed',payment_status='Paid')   
    return render(request,'admin/admin_viewpayments.html',{"complaints":complaints})

def admin_viewmorecomplaintdetail(request):
    subtotal=0
    complaintid=request.GET.get('cid')
    complaint=Complaint.objects.get(id=complaintid)
    scharge=complaint.total
    requirecharges=ComplaintRequire.objects.filter(complaint=complaint)
    for charge in requirecharges:
        amt=charge.require_price
        subtotal+=int(amt)
    ftotal=subtotal+int(scharge)
    print(scharge,ftotal)
    return render(request,'admin/admin_viewmorecomplaintdetail.html',{"complaint":complaint,"scharge":scharge,"ftotal":ftotal,"requirecharges":requirecharges})

#servicehub
def servicehub_signup(request):
    brands=Brand.objects.all().order_by('brandname')
    if request.POST:
        name=request.POST['hubname']
        brands=request.POST.getlist('brand')
        himage=request.FILES['hubimage']
        uname=request.POST['uname']
        password=request.POST['password']
        hphone=request.POST['hubphone']
        hemail=request.POST['hubemail']
        district=request.POST['district']
        hubaddress=request.POST['hubaddress']
        hubpin=request.POST['hubpin']
        hublicence=request.FILES['hublicence']
        if Login.objects.filter(username=uname,password=password).exists():
            msg=messages.success(request,'Already Taken')
            return redirect('/')
        else:
            hub_login=Login.objects.create_user(user_type='hub',view_password=password,username=uname,password=password,is_active=0)
            hub_login.save()
            hubadd=ServicehubReg.objects.create(hub_login=hub_login,hub_name=name,hub_image=himage,hub_phone=hphone,
                                                hub_email=hemail,district=district,hub_address=hubaddress,hub_pin=hubpin,
                                                hub_licence=hublicence)
            hubadd.save()
            for brand in brands:
                brandadd=HubBrands.objects.create(hub=hubadd,brand_id=brand)
                brandadd.save()
            msg=messages.success(request,'Servicehub added sucessfully, Wait for approval')
            return redirect('/')
    return render(request,'servicehub_signup.html',{"brands":brands})

def hub_dashboard(request):
    hubs=ServicehubReg.objects.filter(hub_login__is_active=1)
    return render(request,'hub/hub_dashboard.html',{"hubs":hubs})

def hub_addserviceproducts(request):
    hubid=request.session['hid']
    brands=HubBrands.objects.filter(hub_id=hubid)
    if request.POST:
        pname=request.POST['productname']
        brand=request.POST['brand']
        if Serviceproducts.objects.filter(productname__iexact=pname,hubbrands_id=brand).exists():
            msg=messages.success(request,'Productname already added')
            return redirect('/hub-addserviceproducts')
        else:
            product=Serviceproducts.objects.create(hubbrands_id=brand,productname=pname)
            product.save()
            msg=messages.success(request,'Productname added sucessfully')
            return redirect('/hub-addserviceproducts')
    services=Serviceproducts.objects.filter(hubbrands__hub_id=hubid).order_by("productname")
    return render(request,'hub/hub_addserviceproducts.html',{"brands":brands,"services":services})

def hub_deleteservice(request):
    serviceid=request.GET.get('serviceid')
    servicedelete=Serviceproducts.objects.filter(id=serviceid).delete()
    msg=messages.success(request,'Repair Servicename deleted sucessfully')
    return redirect('/hub-addserviceproducts')

def hub_viewtroubleshoots(request):
    hub=request.session['hid']
    complaints=Complaint.objects.filter(hub_id=hub)
    return render(request,'hub/hub_viewtroubleshoots.html',{"complaints":complaints})

def hub_chat(request):
    hub=request.session['hid']
    complaintid=request.GET.get('cid')
    complaint=Complaint.objects.get(id=complaintid)
    user=complaint.user
    if request.POST:
        usermsg=request.POST['umsg']
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        chatadd=Troubleshoot.objects.create(user=user,hub_id=hub,message=usermsg,chatdate=dt_string,sendby="hub")
        chatadd.save()
    chats=Troubleshoot.objects.filter(user_id=user,hub=hub)
    return render(request,'hub/hub_chat.html',{"complaint":complaint,"chats":chats})

def hub_viewcomplaints(request):
    hub=request.session['hid']
    complaints=Complaint.objects.filter(hub_id=hub).exclude(complaint_status='Completed')
    has_pending_complaints = any(complaint.complaint_status == 'Pending' for complaint in complaints)
    has_product_inrepair_complaints = any(complaint.complaint_status == 'Product Inrepair' for complaint in complaints)
    return render(request,'hub/hub_viewcomplaints.html',{"complaints":complaints,'has_pending_complaints':has_pending_complaints,'has_product_inrepair_complaints':has_product_inrepair_complaints})

def hub_acceptcomplaint(request):
    complaintid=request.GET.get('cid')
    if request.POST:
        sdate=request.POST['submitdate']
        addsubmitdate=Complaint.objects.filter(id=complaintid).update(submitdate=sdate,complaint_status='Date Added')
        msg=messages.success(request,'Product Submissiondate added Wait for approval from user')
        return redirect('/hub-viewcomplaints')
    return render(request,'hub/hub_addprodsubmitdate.html',{"complaintid":complaintid})

def hub_addcharge(request):
    complaintid=request.GET.get('cid')
    print(complaintid)
    if request.POST:
        desc=request.POST.getlist('desc')
        price=request.POST.getlist('price')
        charge=request.POST['servicecharge']
        for f,l in zip(desc,price):
            if f=='' and l == '':
                pass
            else:
                addrequire=ComplaintRequire.objects.create(complaint_id=complaintid,require_desc=f,require_price=l)
                addrequire.save()
        addtotal=Complaint.objects.filter(id=complaintid).update(total=charge,complaint_status='Charged')
        msg=messages.success(request,'Complaint Product accepted and charged')
        return redirect('/hub-viewcomplaints')
    return render(request,'hub/hub_addcomplaintrequirements.html',{"complaintid":complaintid})

def hub_rejectcomplaint(request):
    complaintid=request.GET.get('cid')
    rejectcomplaint=Complaint.objects.filter(id=complaintid).update(complaint_status='Rejected')
    msg=messages.success(request,'Complaint Product rejected')
    return redirect('/hub-viewcomplaints')

def hub_viewmorecomplaintdetail(request):
    subtotal=0
    complaintid=request.GET.get('cid')
    complaint=Complaint.objects.get(id=complaintid)
    scharge=complaint.total
    requirecharges=ComplaintRequire.objects.filter(complaint=complaint)
    for charge in requirecharges:
        amt=charge.require_price
        subtotal+=int(amt)
    if subtotal:
        ftotal=subtotal+int(scharge)
    else:
        ftotal=0
    return render(request,'hub/hub_viewmorecomplaintdetail.html',{"complaint":complaint,"scharge":scharge,"ftotal":ftotal,"requirecharges":requirecharges})

def hub_completecomplaint(request):
    complaintid=request.GET.get('cid')
    completed_date=date.today()
    complaint=Complaint.objects.filter(id=complaintid).update(completed_on=completed_date,complaint_status='Completed')
    msg=messages.success(request,'Complaint resolved sucessfully')
    return redirect('/hub-viewcompletedworks')

def hub_viewcompletedworks(request):
    hub=request.session['hid']
    complaints=Complaint.objects.filter(hub_id=hub,complaint_status='Completed')
    return render(request,'hub/hub_viewcompletedworks.html',{"complaints":complaints})

def hub_addfaq(request):
    hub=request.session['hid']
    if request.POST:
        fque=request.POST['fque']
        fans=request.POST['fans']
        fadd=Faq.objects.create(hub_id=hub,question=fque,answer=fans)
        fadd.save()
        msg=messages.success(request,'FAQ added sucessfully')
        return redirect('/hub-addfaq')
    return render(request,'hub/hub_addfaq.html')

def hub_viewfaq(request):
    hub=request.session['hid']
    faqs=Faq.objects.filter(hub_id=hub)
    return render(request,'hub/hub_viewfaq.html',{"faqs":faqs})

def hub_deletefaq(request):
    faqid=request.GET.get('faqid')
    fdelete=Faq.objects.filter(id=faqid).delete()
    return redirect('/hub-viewfaq')

def hub_viewprofile(request):
    hubid=request.session['hid']
    hub=ServicehubReg.objects.get(id=hubid)
    services=Serviceproducts.objects.filter(hubbrands__hub_id=hubid).order_by("productname")
    hubbrands=HubBrands.objects.all()
    return render(request,'hub/hub_viewprofile.html',{"hub":hub,"hubbrands":hubbrands,"services":services})

def hub_updateprofile(request):
    hub=request.session['hid']
    hubdata=ServicehubReg.objects.get(id=hub)
    if request.POST:
        name=request.POST['hubname']
        if 'hubimage' in request.FILES:
            himage=request.FILES['hubimage']
        else:
            himage=hubdata.hub_image
        hphone=request.POST['hubphone']
        hemail=request.POST['hubemail']
        if 'district' in request.POST:
            district=request.POST['district']
        else:
            district=hubdata.district
        hubaddress=request.POST['hubaddress']
        hubpin=request.POST['hubpin']
        hubadd=ServicehubReg.objects.filter(id=hub).update(hub_name=name,hub_image=himage,hub_phone=hphone,
                                            hub_email=hemail,district=district,hub_address=hubaddress,hub_pin=hubpin,
                                            )
        msg=messages.success(request,'Servicehub updated sucessfully')
        return redirect('/hub-viewprofile')
    return render(request,'hub/hub_updateprofile.html',{"hub":hubdata})

# def hub_deleteprofile(request):
#     hub=request.session['hid']
#     hubdata=ServicehubReg.objects.get(id=hub).hub_login.id
#     # print(hubdata)
#     hubdelete=Login.objects.filter(id=hubdata).delete()
#     msg=messages.success(request,'Servicehub deleted sucessfully')
#     return redirect('/')

def hub_adminchat(request):
    hubid=request.session['hid']
    hub=ServicehubReg.objects.get(id=hubid)
    if request.POST:
        hubmsg=request.POST['umsg']
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        msgadd=Message.objects.create(hub=hub,message=hubmsg,chatdate=dt_string,sendby='hub')
        msgadd.save()
    chats=Message.objects.filter(hub=hub)
    return render(request,'hub/hub_adminchat.html',{"hub":hub,"chats":chats})

#user
def user_signup(request):
    if request.POST:
        fname=request.POST['firstname']
        lastname=request.POST['lastname']
        uname=request.POST['uname']
        password=request.POST['password']
        userphone=request.POST['userphone']
        useremail=request.POST['useremail']
        district=request.POST['district']
        if Login.objects.filter(username=uname,password=password).exists():
            msg=messages.success(request,'Already Taken')
            return redirect('/')
        else:
            user_login=Login.objects.create_user(user_type='user',view_password=password,username=uname,password=password)
            user_login.save()
            useradd=UserReg.objects.create(user_login=user_login,first_name=fname,last_name=lastname,user_phone=userphone,
                                                user_email=useremail,district=district)
            useradd.save()
            msg=messages.success(request,'User added sucessfully, Login to access')
            return redirect('/users-login')
    return render(request,'user_signup.html')

def user_dashboard(request):
    hubs=ServicehubReg.objects.filter(hub_login__is_active=1)
    return render(request,'user/user_dashboard.html',{"hubs":hubs})

def user_viewcompany(request):
    companies=Brand.objects.all()
    return render(request,'user/user_viewcompany.html',{'companies':companies})

def user_viewhubs(request):
    brands=Brand.objects.all().order_by('brandname')
    brandid=request.GET.get('brand')
    if brandid:
        hubs=ServicehubReg.objects.filter(brand_id=brandid,hub_login__is_active=1)
    else:
        hubs=ServicehubReg.objects.filter(hub_login__is_active=1)
    return render(request,'user/user_viewhubs.html',{'brands':brands,'hubs':hubs})

def user_viewhubsbybrand(request):
    brandid=request.GET.get('brandid')
    if brandid:
        return redirect('/user-viewhubs?brand='+str(brandid))
    else:
        pass
        # print(brandid)
        return redirect('/user-viewhubs')
    
def user_viewsinglehub(request):
    user=request.session['uid']
    hubid=request.GET.get('hubid')
    hub=ServicehubReg.objects.get(id=hubid)
    hubbrands=HubBrands.objects.filter(hub_id=hubid)
    services=Serviceproducts.objects.filter(hubbrands__hub_id=hubid).order_by("productname")
    if request.POST:
        brand=request.POST['brand']
        product=request.POST['sproduct']
        model=request.POST['cmodel']
        text=request.POST['ctext']
        print(brand,product,model,text)
        addcomplaint=Complaint.objects.create(user_id=user,hub_id=hubid,serviceproduct_id=product,model=model,complaint_text=text)
        addcomplaint.save()
        msg=messages.success(request,'Request send sucessfully, Please Wait for ServiceHub Reply')
        return redirect('/users-viewtroubleshootchat')
    return render(request,'user/user_viewsinglehub.html',{"hub":hub,"services":services,"hubbrands":hubbrands})

def getproductname(request):
    hubbrandid = request.GET.get('brand')
    # print(hubbrandid, 'Received hubbrandid')  # Debug print
    try:
        hubbrand = HubBrands.objects.get(id=hubbrandid)
        # print(hubbrand, 'Retrieved hubbrand')  # Debug print
        productnames = Serviceproducts.objects.filter(hubbrands=hubbrand)
        productnameslist = [{'id': product.id, 'productname': product.productname} for product in productnames]
        return JsonResponse({'productnames': productnameslist})
    except HubBrands.DoesNotExist:
        # print('HubBrands with given ID does not exist')  # Debug print
        return JsonResponse({'productnames': []})  # Return empty list if the HubBrands does not exist


def user_viewfaq(request):
    hubid=request.GET.get('hubid')
    faqs=Faq.objects.filter(hub__id=hubid)
    return render(request,'user/user_viewfaq.html',{"faqs":faqs})

def users_viewtroubleshootchat(request):
    user=request.session['uid']
    complaints=Complaint.objects.filter(user_id=user)
    return render(request,'user/users_viewtroubleshootchat.html',{"complaints":complaints})

def user_deletecomplaint(request):
    complaintid=request.GET.get('cid')
    complaintdelete=Complaint.objects.filter(id=complaintid).delete()
    msg=messages.success(request,'Your Registered troubleshoot complaint has been deleted sucessfully')
    return redirect('/users-viewtroubleshootchat')

def user_chat(request):
    user=request.session['uid']
    complaintid=request.GET.get('cid')
    complaint=Complaint.objects.get(id=complaintid)
    hub=complaint.hub
    if request.POST:
        usermsg=request.POST['umsg']
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        chatadd=Troubleshoot.objects.create(user_id=user,hub=hub,message=usermsg,chatdate=dt_string)
        chatadd.save()
    chats=Troubleshoot.objects.filter(user_id=user,hub=hub)
    return render(request,'user/user_chat.html',{"complaint":complaint,"chats":chats})

def user_viewcomplaints(request):
    user=request.session['uid']
    complaintid=request.GET.get('cid')
    if complaintid:
        now = date.today()
        complaint=Complaint.objects.filter(id=complaintid).update(booked_on=now)
        msg=messages.success(request,'Your Complaint has been Registered Wait for service hub status')
    complaints=Complaint.objects.filter(user_id=user)
    return render(request,'user/user_viewcomplaints.html',{'complaints':complaints})

def user_acceptsubmitdate(request):
    complaintid=request.GET.get('cid')
    complaint=Complaint.objects.filter(id=complaintid).update(complaint_status='Product Inrepair')
    msg=messages.success(request,'You accepted the product submission date for repair work sucessfully')
    return redirect('/user-viewcomplaints')

def user_rejectsubmitdate(request):
    complaintid=request.GET.get('cid')
    if request.POST:
        sdate=request.POST['submitdate']
        addsubmitdate=Complaint.objects.filter(id=complaintid).update(submitdate=sdate,complaint_status='Product Inrepair')
        msg=messages.success(request,'Product Submissiondate updated')
        return redirect('/user-viewcomplaints')
    return render(request,'user/user_addprodsubmitdate.html',{"complaintid":complaintid})

def user_viewmorecomplaintdetail(request):
    subtotal=0
    complaintid=request.GET.get('cid')
    complaint=Complaint.objects.get(id=complaintid)
    scharge=complaint.total
    requirecharges=ComplaintRequire.objects.filter(complaint=complaint)
    for charge in requirecharges:
        amt=charge.require_price
        subtotal+=int(amt)
    if subtotal:
        ftotal=subtotal+int(scharge)
    else:
        ftotal=0
    return render(request,'user/user_viewmorecomplaintdetail.html',{"complaint":complaint,"scharge":scharge,"ftotal":ftotal,"requirecharges":requirecharges})

def user_payment(request):
    stotal=request.GET.get('stotal')
    complaintid=request.GET.get('cid')
    if request.POST:
        ptype=request.POST['flexRadioDefault']
        pdate=date.today()
        complaintupdate=Complaint.objects.filter(id=complaintid).update(paid_on=pdate,payment_status='Paid',payment_type=ptype)
        return redirect('/user-addcarddetails')
    return render(request,'user/user_payment.html',{"stotal":stotal})

def user_addcarddetails(request):
    if request.POST:
        msg=messages.success(request,'Payment sucessfull')
        return redirect('/user-viewhistory')
    return render(request,'user/user_addcarddetails.html')

def user_viewhistory(request):
    user=request.session['uid']
    complaints=Complaint.objects.filter(complaint_status='Completed',payment_status='Paid',user_id__id=user)   
    return render(request,'user/user_viewhistory.html',{"complaints":complaints})

def user_addfeedback(request):
    complaintid=request.GET.get('cid')
    if request.POST:
        ftext=request.POST['feedback_desc']
        frate=request.POST['rate']
        fadd=Complaint.objects.filter(id=complaintid).update(feedback_desc=ftext,rating=frate)
        msg=messages.success(request,'Feedback added sucessfully')
        return redirect('/user-viewhistory')
    return render(request,'user/user_addfeedback.html')

def user_viewprofile(request):
    user=request.session['uid']
    udata=UserReg.objects.get(id=user)
    return render(request,'user/user_viewprofile.html',{"udata":udata})

def user_updateprofile(request):
    user=request.session['uid']
    udata=UserReg.objects.get(id=user)
    if request.POST:
        fname=request.POST['firstname']
        lastname=request.POST['lastname']
        userphone=request.POST['userphone']
        useremail=request.POST['useremail']
        if 'district' in request.POST:
            district=request.POST['district']
        else:
            district=udata.district
        userupdate=UserReg.objects.filter(id=user).update(first_name=fname,last_name=lastname,user_phone=userphone,
                                            user_email=useremail,district=district)
        msg=messages.success(request,'User updated sucessfully')
        return redirect('/user-viewprofile')
    return render(request,'user/user_updateprofile.html',{"udata":udata})

