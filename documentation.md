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
    KarlBaseResponse.BaseResponse.set_cookie(key, value)
use this method to set cookie
## get_cookie
    KarlBaseResponse.BaseResponse.get_cookie(key)
use this method to get cookie
## set_security_cookie
    KarlBaseResponse.BaseResponse.set_security_cookie(key, value)
use this method to set security cookie
## get_security_cookie
    KarlBaseResponse.BaseResponse.get_security_cookie(key)
use this method to get security cookie
## clear_cookie
    KarlBaseResponse.BaseResponse.clear_cookie(key)
use this method to clear cookie
# templates
pass object, list, dict and string.
## render
    KarlBaseResponse.BaseResponse.render(template, dict)
pass a dict the template, the value of the dict can be dict, list, string or object.
# handler
## get_argument
    KarlBaseResponse.BaseResponse.get_argument(key, default)
get the key's value.
## response
response to web browser
# settings
configure the handlers use a dictionary settings:  

    import os
    
    settings = {
        "ip": 192.168.1.108,  # your host's ip
        "static": os.path.join(os.path.dirname(__file__), "static/"),  # static files folder
        "template": os.path.join(os.path.dirname(__file__), "template/"),  # html template
        "cookie_code": "this_is_an_example"
    }
    
move the static files (as *.css *.js *.jpg etc) to the folder named static.  
move the html template files to the folder named template.
# application
create web application  

    KarlBaseApplication.BaseApplication

## handlers
  
    handlers = {
        "/hello": HelloHandler
    }
  
## listen
    
    application = MyApplication()
    application.listen(8888)

create an application and listen 8888 port.
