from django.urls import path
from . import views
from .views import register_view, login_view, logout_view, profile_view

urlpatterns = [
    path('', views.Homepage, name='Homepage'),
    path('register/', register_view, name='Register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/',views.Dashboard , name="Dashboard"),
    path('json' ,views.Dashboard , name = "dashboard"),
    path('IPL/', views.IPL , name = "IPL"),
    path('Rankings/', views.Rankings, name = "Rankings"),
    path("News/", views.News, name="News"),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    path('dashboard/<int:match_id>/' ,views.scorecard , name='scorecard'),
    path('<str:team_name>/', views.team_details, name='team_details'),
    path(r'^player/(?P<player_name>[\w\s\'\-]+)/$', views.player_details, name='player_details'),
    path('IPL/<str:team_name>',views.IPLteam_details , name = 'IPLteam_details'),
    

    # Dashboard routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('contest/<int:contest_id>/', views.contest_detail, name='contest_detail'),
    path('profile/',views.profile_view , name='profile'),
]
