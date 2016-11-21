from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^dashboard$', views.index, name="index"),
        url(r'^wish_items/(?P<id>\d+)$', views.viewWish, name="view"),
        url(r'^wish_items/create$', views.new, name="new"),
        url(r'^create$', views.create, name="create"),
        url(r'^addwish/(?P<id>\d+)$', views.addWish, name="add"),
        url(r'^destroy/(?P<id>\d+)$', views.destroy, name="destroy"),
        url(r'^removewish/(?P<id>\d+)$', views.remove, name="remove"),
]
