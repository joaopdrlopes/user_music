########################### import python and others ################### 
from lib.common_models import ModelsCommons

########################### import django ###########################
from django.db import models


class UbiwhereUser(ModelsCommons):
    """
    Stores actor information
    """
    
    name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=75, blank=True)
    
    #return values to dropdownlist for template
    def __unicode__(self):
        return '%s' % self.name
    
    
    class Meta:
        app_label = 'centroprodutoapp'
        

class UbiwhereMusic(ModelsCommons):
    """
    Stores actor information
    """
    
    artist = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=100, blank=True)
    album = models.CharField(max_length=100, blank=True)
    
    #return values to dropdownlist for template
    def __unicode__(self):
        return '%s' % self.title
    
    class Meta:
        app_label = 'centroprodutoapp'
        

class UbiwhereUserMusic(ModelsCommons):
    """
    Stores actor information
    """
    
    user = models.ForeignKey(UbiwhereUser, related_name='user_ubiwhere_users')
    music = models.ForeignKey(UbiwhereMusic, related_name='music_ubiwhere_musics')
    
    class Meta:
        app_label = 'centroprodutoapp'
