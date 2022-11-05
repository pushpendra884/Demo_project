from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage 
import time

from user import models as user_models
from . import models
from mydapp import models as mydapp_models

#middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
	def middleware(request):
		if request.path=='/myadmin/' or request.path=='/myadmin/addcategory/' or request.path=='/myadmin/addsubcategory/' or request.path=='/myadmin/manageusers/' or request.path=='/myadmin/manageuserstatus/':
			if request.session['sunm']==None or request.session['srole']!="admin":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.

def adminhome(request):
    #print(request.session['sunm'])
    return render(request,"adminhome.html",{"sunm":request.session['sunm']})

def manageusers(request):
    userDetails=mydapp_models.Register.objects.filter(role="user")
    return render(request,"manageusers.html",{"userDetails":userDetails,"sunm":request.session['sunm']})

def manageuserstatus(request):
    status=request.GET.get("status")
    regid=request.GET.get("regid")
    print(status,"-----",regid)

    if status=="block":
        mydapp_models.Register.objects.filter(regid=int(regid)).update(status=0)
    elif status=="verify":
        mydapp_models.Register.objects.filter(regid=int(regid)).update(status=1)
    else:
        mydapp_models.Register.objects.filter(regid=int(regid)).delete()
    
    return redirect("/myadmin/manageusers/")

def addcategory(request):
    if request.method=="GET":
        return render(request,"addcategory.html",{"output":"","sunm":request.session['sunm']})
    else:
        catnm=request.POST.get("catnm")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.Category(catnm=catnm,caticonnm=filename)  
        p.save() 
        return render(request,"addcategory.html",{"output":"Category added successfully....","sunm":request.session['sunm']})

def addsubcategory(request):
    clist=models.Category.objects.all()
    print()
    if request.method=="GET":
        return render(request,"addsubcategory.html",{"clist":clist,"output":"","sunm":request.session['sunm']})
    else:
        catnm=request.POST.get("catnm")
        subcatnm=request.POST.get("subcatnm")
        caticon=request.FILES["caticon"]
        fs = FileSystemStorage()
        filename = fs.save(caticon.name,caticon)
        p=models.SubCategory(catnm=catnm,subcatnm=subcatnm,subcaticonnm=filename)
        p.save() 
        return render(request,"addsubcategory.html",{"clist":clist,"output":"Sub Category added successfully....","sunm":request.session['sunm']})

def paymentdetails(request):
	paymentinfo=user_models.Payment.objects.all
	return render(request,"paymentdetails.html",{"sunm":request.session['sunm'],"paymentinfo":paymentinfo})

def cpmyadmin(request):
	sunm=request.session['sunm']
	if request.method=='GET':
		return render(request,"cpuser.html",{"sunm":sunm,"output":""})
	else:
		opass=request.POST.get("opass")
		npass=request.POST.get("npass")
		cnpass=request.POST.get("cnpass")

		userDetails=mydapp_models.Register.objects.filter(username=sunm,password=opass)
		#print(userDetails)
	if len(userDetails)>0:
		#msg="success"
		if npass==cnpass:
			mydapp_models.Register.objects.filter(username=sunm).update(password=cnpass)
			msg="Password changed successfully , please login again...."
		else:
			msg="New & Confirm new password not matched...."
	else:
		msg="Invalid old password, please try again..."

	return render(request,"cpuser.html",{"sunm":sunm,"output":msg})

def epmyadmin(request):
	sunm=request.session['sunm']
	userDetails=mydapp_models.Register.objects.filter(username=sunm)
	m,f="",""
	if userDetails[0].gender=="male":
		m="checked"
	else:
		f="checked"
	if request.method=="GET":
		return render(request,"epuser.html",{"sunm":sunm,"userDetails":userDetails[0],"f":f,"m":m})
	else:
		#recieve data on UI
		name=request.POST.get("name")
		username=request.POST.get("username")
		password=request.POST.get("password")
		mobile=request.POST.get("mobile")
		address=request.POST.get("address")
		city=request.POST.get("city")
		gender=request.POST.get("gender")   
		mydapp_models.Register.objects.filter(username=sunm).update(name=name,address=address,password=password,mobile=mobile,city=city,gender=gender)
		return redirect('/myadmin/epmyadmin')

def addproduct(request):
	clist=models.Category.objects.all()  
	if request.method=="GET":
		return render(request,"addproduct.html",{"sunm":request.session['sunm'],"clist":clist,"output":""})
	else:
		ptitle=request.POST.get("ptitle")
		pcategory=request.POST.get("pcategory")
		psubcategory=request.POST.get("psubcategory")
		pdescription=request.POST.get("pdescription")
		pprice=request.POST.get("pprice")
		info=time.asctime()
    
		p=models.Product(ptitle=ptitle,pcategory=pcategory,psubcategory=psubcategory,pdescription=pdescription,pprice=pprice,uid=request.session['sunm'],info=info)
		p.save()

		return render(request,"addproduct.html",{"sunm":request.session['sunm'],"clist":clist,"output":"Product Added Successfully...."})  

def scAJAX(request):
	catnm=request.GET.get("catnm")
	sclist=models.SubCategory.objects.filter(catnm=catnm)  
	sclist_options="<option>Select Sub Category</option>"
	for row in sclist:
		sclist_options+=("<option>"+row.subcatnm+"</option>")
	return HttpResponse(sclist_options);

	