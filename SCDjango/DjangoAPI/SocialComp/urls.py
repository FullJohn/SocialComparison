from django.conf.urls import url

from SocialComp import views

urlpatterns = [
    # Database connection for storing posts
    url(r'^post/$', views.postAPI),
    url(r'^post/([0-9]+)$', views.postAPI),
    
    # Database connection for storing query paramaters
    url(r'^query/$', views.queryAPI),
    url(r'^query/([0-9]+)$', views.queryAPI),

    url(r'run/$', views.runQuery),
    url(r'^run/$([0-9]+)$', views.runQuery),
]