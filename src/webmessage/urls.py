from django.urls import path
from . import views

app_name = 'webmessage'

urlpatterns = [

    # /hoomepage/
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    # /registration/
    path('register/', views.register, name='register'),
    # /login/
    path('login_user/', views.login_user, name='login_user'),
    # /logout/
    path('logout_user/', views.logout_user, name='logout_user'),
    path('compose/', views.compose, name='compose'),
    path('outbox/', views.outbox, name='outbox'),
    path('detail/<int:message_id>/', views.detail, name='detail'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
]
