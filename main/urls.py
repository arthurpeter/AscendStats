from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('climbs', views.climbs, name='climbs'),
    path('climb/delete/<int:climb_id>/', views.delete_climb, name='delete_climb'),
    path('climb/edit/<int:climb_id>/', views.edit_climb, name='edit_climb'),
    path('comming_soon', views.comming_soon, name='comming_soon'),
    path('about', views.about, name='about'),
    path('profile', views.profile, name='profile'),
    path('advanced', views.advanced, name='advanced'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('style-distribution-data/', views.style_distribution_data, name='style_distribution_data'),
    path('grade-distribution-data/', views.grade_distribution_data, name='grade_distribution_data'),
    path('success-rate-data/', views.success_rate_data, name='success_rate_data'),
    path('average-grade-data/', views.average_grade_data, name='average_grade_data'),
]
