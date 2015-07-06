# headers
operate http headers  
## set_header
KarlBaseResponse.BaseResponse.set_header(value)  
use this method to set http header  
## add_header
KarlBaseResponse.BaseResponse.add_header(value)  
use this method to add http header  
# cookies
operate cookie
## set_cookie

## get_cookie
## set_security_cookie
## get_security_cookie
## clear_cookie
# templates
## render
# handler
## get
## post
## get_argument
## response
# settings
## ip
## static files' path
## templates' path
## cookie security code
# application
## handlers
configure the handlers use a dictionary settings:  

    import os
    
    settings = {
        "ip": 192.168.1.108,  # your host's ip
        "static": os.path.join(os.path.dirname(__file__), "static/"),  # static files folder
        "template": os.path.join(os.path.dirname(__file__), "template/"),  #
        "cookie_code": "this_is_an_example"
    }
    
move the static files (as *.css *.js *.jpg etc) to the folder named static.  
move the html template files to the folder named template.  

  
## listen