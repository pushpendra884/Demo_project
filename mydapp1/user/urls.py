from django.urls import path

from . import views

urlpatterns = [
    path('',views.userhome),
    path('funds/',views.funds),
    path('payment/',views.payment),
    path('success/',views.success),
    path('cancel/',views.cancel),
    path('paymentdetails/', views.paymentdetails),
    path('cpuser/', views.cpuser),
    path('epuser/', views.epuser),
    path('showcategory/', views.showcategory),
    path('showsubcategory/', views.showsubcategory),
    path('showproduct/', views.showproduct),
    path('order/', views.order)
]

