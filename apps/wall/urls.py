from django.conf.urls import url, include
from . import views

app_name = "wall"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^entrance$', views.entrance, name='entrance'),
    url(r'^user/user_update$', views.user_update, name='user_update'),
    url(r'^user_delete$', views.user_delete, name='user_delete'),
    url(r'^wall$', views.wall, name='wall'),
    url(r'^post_message$', views.post_message, name='post_message'),
    url(r'^user/(?P<id>\d*)$', views.user, name='user'),
    url(r'^all_users$', views.all_users, name="all_users"),
]
