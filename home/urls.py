from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('myAccount', views.myAccount),
    path('orderHistory', views.orderHistory), 
    path('favorites', views.favorites),
    path('checkout', views.checkout),
    path('updateInfo', views.updateInfo),
    path('taco', views.taco),
    path('logout',views.logout),
    path('success',views.success),
    path('favoriteTaco/<int:taco_id>',views.favoriteTaco),
    path('unfavorite/<int:taco_id>',views.unfavorite),
    path('reOrder', views.reOrder)
]