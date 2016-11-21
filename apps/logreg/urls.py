from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name="logreg_index"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
#r means raw text input; actual regex in single quotes;
#carrot ^ means start of string
]
