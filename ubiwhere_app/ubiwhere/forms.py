########################### import django ########################### 
from django import forms
from django.db import transaction
from django.utils.translation import ugettext as _
########################### import models ########################### 
from ubiwhere_app.models import UbiwhereUser, UbiwhereMusic, UbiwhereUserMusic

class CreateUserForm(forms.ModelForm):
    """
    Create users
    """
    
        
    email = forms.EmailField()
    
    
    def __init__(self, *args, **kwargs):
        """
        Creates custom fields
        
        """

        super(CreateUserForm, self).__init__(*args, **kwargs)
    
    
    def clean_email(self):
        
        # get email
        email = self.cleaned_data["email"]
        
        # check if email aready exist
        try:
            UbiwhereUser.objects.get(email=email)
        except UbiwhereUser.DoesNotExist:
            return email
        raise forms.ValidationError("Este email ja existe !") 
    
    
    def clean_name(self):
        # check if name already exist
        
        # get name
        name = self.cleaned_data["name"]
        
        try:
            UbiwhereUser.objects.get(name=name)
        except UbiwhereUser.DoesNotExist:
            return name
        raise forms.ValidationError("Este nome ja existe !") 
        
    def clean(self):
        """
        Validates data
        """
        cleaned_data = super(CreateUserForm, self).clean()
        
        return cleaned_data
    
    @transaction.commit_on_success            
    def save(self, *args, **kwargs):
        """
        Saves data

        """
        user = super(CreateUserForm, self).save(*args, **kwargs)
        
                                    
        return user
    
    class Meta:
        model = UbiwhereUser
        fields = ['name', 'email']
        


class CreateMusicForm(forms.ModelForm):
    """
    Create musics
    """
    
       
    def __init__(self, *args, **kwargs):
        """
        Creates custom fields
        
        """

        super(CreateMusicForm, self).__init__(*args, **kwargs)
           
         
    
   
    def clean(self):
        """
        Validates data
        """
        cleaned_data = super(CreateMusicForm, self).clean()
        
        # get artist
        artist = self.cleaned_data["artist"]
        
        # get album
        album = self.cleaned_data["album"]
        
        # get title
        title = self.cleaned_data["title"]
        
        try:
            UbiwhereMusic.objects.get(artist=artist, album=album, title=title)
        except UbiwhereMusic.DoesNotExist:
            return cleaned_data
        else:
            raise forms.ValidationError("Ja existe o titulo para o album e artista!") 
        
        return cleaned_data
    
    @transaction.commit_on_success            
    def save(self, *args, **kwargs):
        """
        Saves data

        """
        user = super(CreateMusicForm, self).save(*args, **kwargs)
        
                                    
        return user
    
    class Meta:
        model = UbiwhereMusic
        fields = ['artist', 'title', 'album']




class CreateUserMusicForm(forms.ModelForm):
    """
    Create user musics
    """
    
    
    def __init__(self, *args, **kwargs):
        """
        Creates custom fields
        
        """

        super(CreateUserMusicForm, self).__init__(*args, **kwargs)
           
        # get list of user
        self._available_user_list = UbiwhereUser.objects.all()
        
                
        self.fields['user']  = forms.ModelChoiceField(label=_('User'),queryset=self._available_user_list, empty_label=_('Choose one'), required=True)
       
        
        # get list of musics
        self._available_music_list = UbiwhereMusic.objects.all()
        
        self.fields['music']  = forms.ModelChoiceField(label=_('Music'),queryset=self._available_music_list, empty_label=_('Choose one'), required=True)
        
    
   
       
    
    def clean(self):
        """
        Validates data
        """
        cleaned_data = super(CreateUserMusicForm, self).clean()
        
        # get user
        user = self.cleaned_data["user"]
        
        # get music
        music = self.cleaned_data["music"]
        
        try:
            UbiwhereUserMusic.objects.get(user_id=user, music_id=music)
        except UbiwhereUserMusic.DoesNotExist:
            return cleaned_data
        else:
            raise forms.ValidationError("Ja existe a associacao dessa musica ao user !") 
        
        
        return cleaned_data
    
    
    @transaction.commit_on_success            
    def save(self, *args, **kwargs):
        """
        Saves data

        """
        user = super(CreateUserMusicForm, self).save(*args, **kwargs)
        
                                    
        return user
    
    class Meta:
        model = UbiwhereUserMusic
        fields = ['user', 'music']
        
