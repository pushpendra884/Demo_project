from django.shortcuts import render,redirect
from django.http import HttpResponse

from myadmin import models as myadmin_models
from mydapp import models as mydapp_models

from django.conf import settings
MEDIA_URL=settings.MEDIA_URL

from . import models
import time

#middleware to check session for user routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/':
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware

# Create your views here.

def userhome(request):
    return render(request,"userhome.html",{"sunm":request.session['sunm']})

def funds(request):
	paypalURL="https://www.sandbox.paypal.com/cgi-bin/webscr"
	paypalID="sb-gvylo18057653@business.example.com"
	price=100
	#sb-gv3gj18654400@personal.example.com
	return render(request,"funds.html",{"sunm":request.session['sunm'],"paypalURL":paypalURL,"paypalID":paypalID,"price":price})

def payment(request):
	sunm=request.GET.get("sunm")
	price=request.GET.get("price")
	info=time.asctime()
	p=models.Payment(uid=sunm,price=price,info=info)
	p.save()
	return redirect("/user/success/")
	
def success(request):
	return render(request,"success.html",{"sunm":request.session['sunm']})

def cancel(request):
	return render(request,"cancel.html",{"sunm":request.session['sunm']})

def paymentdetails(request):
	paymentinfo=models.Payment.objects.filter(uid=request.session['sunm'])	
	return render(request,"paymentdetails.html",{"sunm":request.session['sunm'],"paymentinfo":paymentinfo})

def cpuser(request):
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

def epuser(request):
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
		mobile=request.POST.get("mobile")
		address=request.POST.get("address")
		city=request.POST.get("city")
		gender=request.POST.get("gender")   
		mydapp_models.Register.objects.filter(username=sunm).update(name=name,address=address,mobile=mobile,city=city,gender=gender)
		return redirect('/user/epuser')

def showcategory(request):
	clist=myadmin_models.Category.objects.all()
	return render(request,"showcategory.html",{"sunm":request.session['sunm'],"clist":clist,"MEDIA_URL":MEDIA_URL})

def showsubcategory(request):
  catnm=request.GET.get("catnm")
  clist=myadmin_models.Category.objects.all()
  sclist=myadmin_models.SubCategory.objects.filter(catnm=catnm)
  return render(request,"showsubcategory.html",{"sunm":request.session['sunm'],"sclist":sclist,"MEDIA_URL":MEDIA_URL,"catnm":catnm,"clist":clist})

def showproduct(request):
	catnm=request.GET.get("catnm")
	subcatnm=request.GET.get("subcatnm")
	sclist=myadmin_models.SubCategory.objects.filter(catnm=catnm)
	plist=myadmin_models.Product.objects.filter(psubcategory=subcatnm)
	return render(request,"showproduct.html",{"sunm":request.session['sunm'],"catnm":catnm,"subcatnm":subcatnm,"sclist":sclist,"plist":plist,"MEDIA_URL":MEDIA_URL})

def order(request):
	pid=request.POST.get("pid")
	pprice=request.POST.get("pprice")
	qty=request.POST.get("qty")
	uid=request.session['sunm']
	amount=int(qty)*int(pprice)
	info=time.asctime()
	p=models.Order(pid=int(pid),uid=uid,qty=int(qty),pprice=pprice,amount=amount,info=info)
	p.save()
	return render(request,"orderconfirm.html",{"sunm":uid})