from django.urls import path

from . import views

urlpatterns = [
    path('',views.adminhome),
    path('manageusers/',views.manageusers),
    path('manageuserstatus/',views.manageuserstatus),
    path('addcategory/',views.addcategory),
    path('addsubcategory/',views.addsubcategory),
    path('addproduct/', views.addproduct),
    path('scAJAX/',views.scAJAX),
    path('paymentdetails/', views.paymentdetails),
    path('cpmyadmin/', views.cpmyadmin),
    path('epmyadmin/', views.epmyadmin)
]
