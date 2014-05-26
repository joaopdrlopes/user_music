########################### import django ###########################
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


#URLS FOR UBIWHERE_APP
urlpatterns += i18n_patterns('',
    
    url(r'^ubiwhere/', include('centroprodutoapp.ubiwhere.urls', namespace='ubiwhere')),
)


