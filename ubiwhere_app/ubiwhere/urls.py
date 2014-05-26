########################### import django ########################### 
from django.conf.urls import patterns, url


########################### import centroproduto ###########################
from ubiwhere_app.ubiwhere import views


urlpatterns = patterns('',
    #url(r'^$', views.index, name='index'),
    # ex: /entities/5/
    #url(r'^(?P<entity_id>\d+)/$', views.detail, name='detail'),
    url(r'^ubiwhere_index/$', views.ubiwhere_index, name='ubiwhere_index'),
    #
    url(r'^user_add/$', views.user_add, name='user_add'),
    url(r'^music_add/$', views.music_add, name='music_add'),
    url(r'^user_music_add/$', views.user_music_add, name='user_music_add'),
    url(r'^user_music_view/(?P<user_id>\d+)/$', views.user_music_view, name='user_music_view'),
    ###### api urls
    url(r'^api_user_add/$', views.api_user_add, name='api_user_add'),
    url(r'^api_music_add/$', views.api_music_add, name='api_music_add'),
    url(r'^api_user_music_add/$', views.api_user_music_add, name='api_user_music_add'),
    
    )
