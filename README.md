# karloop
an python web framework like webpy and tornado

# install
download the package or check out the project  
the cd to the project folder  
run these commands:  

    sudo python setup.py install  

# demo
## hello world

    # coding=utf-8
    from karloop.KarlBaseApplication import BaseApplication  
    from karloop.KarlBaseHandler import BaseHandler  
  
  
    class HelloHandler(BaseHandler):  
        def get(self):  
           return self.response("hello world")  
          
    
    handlers = {
        "/hello": HelloHandler
    }


    class HelloApplication(BaseApplication):
        def __init__(self):
            super(HelloApplication, self).__init__(handlers=handlers)
            
    
    if __name__ == "__main__":
        application = HelloApplication()
        application.listen(port=8888)
        application.run()
        
### run hello world
    python index.py
then open the web browser and go to "127.0.0.1:8888/hello", you will see the hello world.


# Notice
This framework has been used on the linux version of <a href="http://www.cubebackup.com"> CubeBackup for Google Apps</a>, which is a local backup solution for Google Apps data.   
There are probably some bugs about stream video on windows operating system
If you find bugs or know how to fix them,  please send a message to karlvorndoenitz@gmail.com,special thanks.   
