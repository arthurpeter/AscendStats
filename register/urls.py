from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import CustomConfirmEmailView

urlpatterns = [
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('email_confirmation_sent/', TemplateView.as_view(template_name='register/email_confirmation_sent.html'), name='email_confirmation_sent'),
    path('email-confirm/<key>/', CustomConfirmEmailView.as_view(), name='account_confirm_email'),
]
