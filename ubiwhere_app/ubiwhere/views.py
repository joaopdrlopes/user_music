########################### import python and others ################### 
import json
from lib.http_response_api import HttpResponseAPI

########################### import Django ################### 
#messages
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
#import http404 Response
from django.http import Http404
from django.db import transaction
from django.utils import simplejson
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

########################### import  ###########################
#import forms validators
from ubiwhere_app.ubiwhere.forms import CreateUserForm, CreateMusicForm, CreateUserMusicForm

from ubiwhere_app.models import UbiwhereUser, UbiwhereMusic, UbiwhereUserMusic


def user_add(request):
    
    """
    View to create user
   
    """
    # get all users for listing
    user_objs = UbiwhereUser.objects.all().order_by('name')
    
   
    if request.method == 'POST': # If the form has been submitted...
           
        user_form = CreateUserForm(request.POST) # A form bound to the POST data
        
        if user_form.is_valid(): # All validation rules pass         
            user_form.save()
            messages.success(request, _('Request sent with success.'))
        else:
            messages.error(request, _('An error occurred, please try again.'))
    
    else:        
        user_form = CreateUserForm() # An unbound form
        
        
        
    template_data = {
        'user_form': user_form,
        'user_objs':user_objs,
        }
    return render_to_response('ubiwhere/user_add.html', template_data,  RequestContext(request))



def music_add(request):
    
    """
    View to create music
   
    """
    
    # get all musics
    musics_obj = UbiwhereMusic.objects.all().order_by('artist')
    
    if request.method == 'POST': # If the form has been submitted...
            
        music_form = CreateMusicForm(request.POST) # A form bound to the POST data
        #import pdb; pdb.set_trace()
        if music_form.is_valid(): # All validation rules pass         
            music_form.save()

            messages.success(request, _('Request sent with success.'))
            
        else:
            messages.error(request, _('An error occurred, please try again.'))
    
    else:        
        music_form = CreateMusicForm() # An unbound form
        
    template_data = {
        'music_form': music_form,
        'musics_obj':musics_obj,
        }
    return render_to_response('ubiwhere/music_add.html', template_data,  RequestContext(request))


def user_music_add(request):
    
    """
    View to create user music
   
    """
       
    if request.method == 'POST': # If the form has been submitted...
            
        user_music_form = CreateUserMusicForm(request.POST) # A form bound to the POST data
        #import pdb; pdb.set_trace()
        if user_music_form.is_valid(): # All validation rules pass         
            user_music_form.save()

            messages.success(request, _('Request sent with success.'))
           
        else:
            messages.error(request, _('An error occurred, please try again.'))
    
    else:        
        user_music_form = CreateUserMusicForm() # An unbound form
        
    template_data = {
        'user_music_form': user_music_form
        }
    return render_to_response('ubiwhere/user_music_add.html', template_data,  RequestContext(request))


def user_music_view(request, user_id):
    
    """
    View to see user music
   
    """
    
    # check if id exist
    if user_id:
        # get user music object
        try:
            user_music_objs = UbiwhereUserMusic.objects.select_related().filter(user_id=user_id)
        except UbiwhereUserMusic.DoesNotExist:
            raise Http404

    else:
        user_music_objs=[]
           
    template_data = {
        'user_music_objs': user_music_objs
        }
    return render_to_response('ubiwhere/user_music_view.html', template_data,  RequestContext(request))


# index for application
def ubiwhere_index(request):
    
    """
    View to create index
   
    """
    
              
    template_data = {  }
    return render_to_response('ubiwhere/ubiwhere_index.html', template_data,  RequestContext(request))


########################### REQUEST API ###################
@csrf_exempt
def api_user_add(request):
    """
    Request Api to create user
    """    
        
    #initialize response variable
    response_data = {}
    
    if request.method == 'POST':
        
        # try to read the post data from the request
        try:
            post_data=json.loads(request.body)
        except:
            return HttpResponseAPI(status=400, error='Invalid syntax.')
        
        # check if all required fields are present
        if not ('name' in post_data and post_data['name']!='' and 'email' in post_data and post_data['email']!=''):
            return HttpResponseAPI(status=400, error='Fill all fields correctly.')
        else:
            name=post_data['name']
            email=post_data['email']
            
        # validate email
        try:
            validate_email( email )
        except ValidationError:
            return HttpResponseAPI(status=400, error='Email is incorrect.')
        
        # check if email already exist in DB
        try:
            UbiwhereUser.objects.get(email=email)
        except UbiwhereUser.DoesNotExist:
            pass
        else:
            return HttpResponseAPI(status=400, error='This Email is already exist.')
        
            
        # star transaction to save fields
        with transaction.commit_manually():
            
            # save fields
            UbiwhereUser.objects.create(name=name, email=email)
            
            
            response_data['success']='Create User'
                
            transaction.commit()            
            return HttpResponseAPI(simplejson.dumps(response_data), mimetype="application/json")
    else:
        # wrong request method!!!
        return HttpResponseAPI(status=405, error='Wrong request method. It is not Post.')
    
"""
dictionary to send fields to insert test 

{"name":"Joao Lopes" , "email":"joao.lopes@centroproduto.com"}   
"""



@csrf_exempt
def api_music_add(request):
    """
    Request Api to create music
    """    
        
    #initialize response variable
    response_data = {}
    
    if request.method == 'POST':
        
        # try to read the post data from the request
        try:
            post_data=json.loads(request.body)
        except:
            return HttpResponseAPI(status=400, error='Invalid syntax.')
        
        # check if all required fields are present
        if not ('artist' in post_data and post_data['artist']!='' and 'album' in post_data and post_data['album']!='' and 'title' in post_data and post_data['title']!=''):
            #import pdb; pdb.set_trace()
            return HttpResponseAPI(status=400, error='Fill all fields correctly.')
        else:
            artist=post_data['artist']
            album=post_data['album']
            title=post_data['title']
            
       
        # check if title already exist for the album and the artist
        try:
            UbiwhereMusic.objects.get(artist=artist, album=album, title=title)
        except UbiwhereMusic.DoesNotExist:
            pass
        else:
            return HttpResponseAPI(status=400, error='This title is already exist for this album and this artist.')
        
            
        # star transaction to save fields
        with transaction.commit_manually():
            
            # save fields
            UbiwhereMusic.objects.create(artist=artist, album=album, title=title)
            
            
            response_data['success']='Create Music'
                
            transaction.commit()            
            return HttpResponseAPI(simplejson.dumps(response_data), mimetype="application/json")
    else:
        # wrong request method!!!
        return HttpResponseAPI(status=405, error='Wrong request method. It is not Post.')
    
"""
dictionary to send fields to insert test 

{"artist":"quim barreiros" , "album":"best quim", "title":"carro da vizinha"}   
"""



@csrf_exempt
def api_user_music_add(request):
    """
    Request Api to create user music
    """    
        
    #initialize response variable
    response_data = {}
    
    if request.method == 'POST':
        
        # try to read the post data from the request
        try:
            post_data=json.loads(request.body)
        except:
            return HttpResponseAPI(status=400, error='Invalid syntax.')
        
        # check if all required fields are present
        if not ('user' in post_data and post_data['user']!='' and 'music' in post_data and post_data['music']!=''):
            #import pdb; pdb.set_trace()
            return HttpResponseAPI(status=400, error='Fill all fields correctly.')
        else:
            user=post_data['user']
            music=post_data['music']
        
        # check if user is an integer    
        try:
            int(user)
        except ValueError:
            return HttpResponseAPI(status=400, error='This user is not integer!')
        
        # check if music is an integer   
        try:
            int(music)
        except ValueError:
            return HttpResponseAPI(status=400, error='This music is not integer!')
        
        # check if association of user and music already exist
        try:
            UbiwhereUserMusic.objects.get(user=user, music=music)
        except UbiwhereUserMusic.DoesNotExist:
            pass
        else:
            return HttpResponseAPI(status=400, error='This association already exist!')
        
        
        # star transaction to save fields
        with transaction.commit_manually():
            
           
            # check if user exist and get object
            try:
                user_obj = UbiwhereUser.objects.get(id=user)
            except UbiwhereUser.DoesNotExist:
                return HttpResponseAPI(status=400, error='This user does not exist.')
                       
            # check if music exist and get object
            try:
                music_obj = UbiwhereMusic.objects.get(id=music)
            except UbiwhereMusic.DoesNotExist:
                return HttpResponseAPI(status=400, error='This music does not exist.')
                       
                   
            # save fields 
            UbiwhereUserMusic.objects.create(user=user_obj, music=music_obj)
            
            
            response_data['success']='Create User Music'
                
            transaction.commit()            
            return HttpResponseAPI(simplejson.dumps(response_data), mimetype="application/json")
    else:
        # wrong request method!!!
        return HttpResponseAPI(status=405, error='Wrong request method. It is not Post.')
    
"""
dictionary to send fields to insert test 

{"user":"1" , "music":"2"}   
"""
