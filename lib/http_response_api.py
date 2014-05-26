########################### import django ###########################
from django.http import HttpResponse
from django.utils import simplejson
import warnings



class HttpResponseAPI(HttpResponse):
    """
    Extends the response object to allow communication with frontend requests
    <2013-12-19 Joao/Jose> creation
    """
    
    def __init__(self, *args, **kwargs):
        """
        <2013-12-19 Joao/Jose> creation
        """
	CORS_ORIGIN_WHITELIST = ('localhost:8000')
        
        if 'mimetype' in kwargs:
            warnings.warn("Using mimetype keyword argument is deprecated, use"
                          " content_type instead", PendingDeprecationWarning)
            kwargs['content_type'] = kwargs['mimetype']
        
        # make the default mimetype in the api responses be application/json
        if not 'content_type' in kwargs: 
            kwargs['content_type']="application/json"
        # check if an error message should be returned and initialize the response object accordingly
        if 'error' in kwargs:
            # save the error message and remove it from the keyword arguments since the common httpresponse does not support such an argument
            try:
                error = simplejson.dumps(kwargs.pop('error'))
            except:
                super(HttpResponseAPI, self).__init__(*args, **kwargs)
            else:                
                super(HttpResponseAPI, self).__init__(error, *args, **kwargs)
        else:        
            # initialize the response normally         
            super(HttpResponseAPI, self).__init__(*args, **kwargs)
        
        # ensure the fe can always view this response 
        fe_path = 'http://' + CORS_ORIGIN_WHITELIST[0]
        self["Access-Control-Allow-Origin"] = fe_path
        self["Access-Control-Allow-Credentials"] = 'true'
        
        
        
        
        
