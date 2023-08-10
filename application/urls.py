from django.urls import path
from . import views
from . import authview
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetCompleteView
from .forms import PasswordResetCustomView,PasswordResetConfirmCustomView


urlpatterns = [
    # home page url
    path('',views.home, name="home"),
    path("feedback",views.feedback,name="feedback"),
    # authentication urls
    path('register',authview.register,name = "register"),
    path('login',authview.login,name = "login"),
    path('logout',authview.logout,name = "logout"),
    path('change-password',authview.changepass,name = "changepass"),
    path('activate/<uidb64>/<token>',authview.activate,name = "activate"),
    path('reset-password',PasswordResetView.as_view(template_name="reset_password.html",form_class=PasswordResetCustomView),name="reset-password"),
    path('password_reset_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name='password-reset-confirm.html',form_class=PasswordResetConfirmCustomView),name="password_reset_confirm"),
    path('password-reset-done',PasswordResetDoneView.as_view(template_name='password-reset-done.html'),name='password_reset_done'),
    path('password_reset_complete',PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'),name="password_reset_complete"),
    # product detail url
    path('product/<str:product_slug>',views.product_details, name="product-details"),
    # cart url
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    # order url
    path("checkout",views.checkout,name="checkout"),
    path('order',views.order,name="order")
]