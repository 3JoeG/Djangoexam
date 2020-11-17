from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('register', views.register),
    path('travels', views.travels),
    path('addtrip', views.addtrip),
    path('logout',views.logout),
    path('add',views.add),
    path('join/<int:tripid>',views.join),
    path('view/<int:tripid>',views.view),
    path('cancel/<int:tripid>', views.cancel),
    path('delete/<int:tripid>',views.delete)

]