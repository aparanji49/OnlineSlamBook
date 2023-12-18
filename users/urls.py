from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # users views
    path('signup', views.signup, name='signup'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('loginpage/', views.user_login_page, name='user_login_page'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('list', views.list_users, name='list_users'),
    path('profile/<str:username>/update', views.update_profile, name='update_profile'),
    # path('make_user_admin', views.make_user_admin, name='make_user_admin'),

]
