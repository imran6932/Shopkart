from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import CustomerLogin, ChangePassword, PasswordReset, SetPassword
urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),

    path('query/', views.search_bar, name='search'),

    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('buy/', views.buy, name='buy'),

    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('cart/', views.show_cart, name='showcart'),

    path('pluscart/', views.plus_cart, name='pluscart'),

    path('minuscart/', views.minus_cart, name='minuscart'),

    path('removecart/', views.remove_cart, name='removecart'),

    path('add_profile/', views.Customer_profile.as_view(), name='add_profile'),

    path('orders/', views.orders, name='orders'),

    path('profile/', views.profile_page, name='profile'),

    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=ChangePassword, success_url='/passwordchangedone/'), name='changepassword'),

    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=PasswordReset), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=SetPassword), name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('mobile/', views.mobile, name='mobile'),

    path('book/', views.book, name='book'),

    path('book/<slug:data>', views.book, name='bookdata'),

    path('address/', views.address, name='address'),

    path('delete/<int:id>/', views.delete_customer_add, name='delete'),

    path('update/<int:id>/', views.update_customer_add, name='update'),

    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    path('laptop/', views.laptop, name='laptop'),

    path('laptop/<slug:data>', views.laptop, name='laptopdata'),

    path('topwear/', views.topwear, name='topwear'),

    path('topwear/<slug:data>', views.topwear, name='topweardata'),

    path('bottomwear/', views.bottomwear, name='bottomwear'),

    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=CustomerLogin), name= 'login'), 
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('registration/', views.CustomerReg.as_view(), name='customerregistration'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
