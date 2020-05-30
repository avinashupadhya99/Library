from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('getOTP/',views.getOTP,name='getOTP'),
    path('password_reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('dashboard/edit_email/',views.edit_email,name='edit_email'),
    path('dashboard/edit_phone/',views.edit_phone,name='edit_phone'),
    path('dashboard/change_password/',views.change_password,name='change_password'),
    path('forgot/',views.forgot_password,name='forgot_password'),
    path('generateOTP/',views.addreg,name='addreg'),
]
