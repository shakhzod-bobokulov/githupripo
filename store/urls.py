from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("mahsulotlar/", views.product_list, name="product_list"),
    path("mahsulotlar/<slug:slug>/", views.product_detail, name="product_detail"),
    path("savat/", views.cart_detail, name="cart_detail"),
    path("savat/qoshish/<int:product_id>/", views.cart_add, name="cart_add"),
    path("savat/yangilash/<int:product_id>/", views.cart_update, name="cart_update"),
    path("savat/ochirish/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("buyurtma/", views.checkout, name="checkout"),
    path("buyurtma/<int:order_id>/tayyor/", views.order_success, name="order_success"),
    path("aloqa/yuborish/", views.contact_submit, name="contact_submit"),
]
