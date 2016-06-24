from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^login$', views.loginUser, name='login'),
    url(r'^register$', views.registerUser, name='register'),
    url(r'^pokes$', views.displayPokes, name='display-pokes'),
    url(r'^poke$', views.poke, name='poke'),
    url(r'^logout$', views.logout, name='logout')
]
