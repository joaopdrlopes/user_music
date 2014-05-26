########################### import django ###########################
from django.db import models


class ModelsCommons(models.Model):
    """
    Translation abstract model, saves multilanguage fields
    <2013-02-19 Dinis> creation
    """
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    #def save(self):
    #    if self.pk==None:
    #        self.creation_date = timezone.now()
    #    self.modified_date = timezone.now()
    #    super(ModelsCommons, self).save()

    class Meta:
        abstract = True