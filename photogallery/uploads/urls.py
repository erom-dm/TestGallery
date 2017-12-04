from django.conf.urls import url
from . import views

app_name = 'uploads'

urlpatterns = [
    url(r'^create/', views.create, name='create'),
    url(r'^post_detail/(?P<upload_id>[0-9]+)/$', views.postdetail, name='post_detail'),
    url(r'^edit_post/(?P<upload_id>[0-9]+)/$', views.editpost, name='edit_post'),
    url(r'^create_via_dl/', views.download, name='create_via_dl'),
    url(r'^delete_post/(?P<upload_id>[0-9]+)/$', views.delete_post, name='delete_post'),
    url(r'^user/(?P<fk>[0-9]+)/$', views.user_uploads, name='user_uploads'),
]