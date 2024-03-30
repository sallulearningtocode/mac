from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="ShopHome"),
    path('aboutus', views.about,name="AboutUs"),
    path('contactus', views.contactus,name="ContactUs"),
    path('products/<int:myid>', views.productview,name="ProductView"),
    path('tracker', views.tracker,name="Tracker"),
    path('search/', views.search,name="Search"),
    path('cart', views.cart,name="Cart"),
    path('checkout', views.checkout,name="Checkout"),
    path('addProduct', views.addProduct,name="addProduct"),
    path("handlerequest/",views.handlerequest,name="HandleRequest")

]
