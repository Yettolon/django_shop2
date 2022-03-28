from ast import Pass
from django.urls import path

from .views import cart_add, index , user_is_activate,shop_view,shop_detail,cart_detail, cart_clear, cart_remove,shop_cat,shop_type, buy_redirect
from .views import MyLoginView,RegiserUserView,LogoutView, PasswordResetViewUser,PasswordRe,PasswordResetConfirmViews,AboutView

app_name = 'kind'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('accounts/reset/<uidb64>/<token>/',PasswordResetConfirmViews.as_view(), name='password_reset_confirm'),
    path('accounts/reset_password_sent',PasswordRe.as_view(), name='password_reset_done'),
    path('accounts/reset_password/', PasswordResetViewUser.as_view(), name='reset_password'),
    path('accounts/register/<str:sign>/', user_is_activate, name='register_activate'),
    path('accounts/register/', RegiserUserView.as_view(), name='register'),
    path('accounts/login/', MyLoginView.as_view(), name='login'),
    path('accounts/logout/',LogoutView.as_view(),name='logout'),
    path('buy/',buy_redirect, name='buy_redirect'),
    path('cart/add/<int:product_id>/',cart_add,name='cart_add'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('cart/cart-remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('cart/', cart_detail, name='cart_detail'),
    path('shop/detail/<slug>',shop_detail, name="shop_detail"),
    path('shop/categegory/<int:pk>/<int:id>/',shop_type,name='shop_type'),
    path('shop/categegory/<int:pk>/', shop_cat, name='shop_cat'),
    path('shop/', shop_view, name='shop_list'),
    path('',index,name='index'),
]

