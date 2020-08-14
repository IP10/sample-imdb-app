# IMDB Sample App

## Introduction

This project built and exposes the dependent rest endpoints to web application of IMDB Sample App.

## Setup Instructions
__Steps__

1.  Install Required Packages for Server  
   
        sudo apt-get install python3  
        
        sudo apt-get install python3-pip python3-dev
        
        sudo pip3 install virtualenv
    

2. Django Environment Setup
    
        virtualenv -p python3 env_name 
        
        source env_name/bin/activate
        
        pip install -r requirements.txt

3. Run Server
    
        python manage.py migrate            # to migrate all the migrations
                
        python manage.py runserver          # to run the server
     
4. Setup Command

        python manage.py setup_backend --help   
        # display the list of option.
        1.setup movies data 
        2.setup django admin user
        3. setup Oauth application
                
        python manage.py setup_backend          # to run all the option
        
        python manage.py setup_backend --only 1 2 # space separated option to run specfic option.
        

*Application Endpoint:* https://sample-imdb.herokuapp.com/api/

*API Document:* https://app.swaggerhub.com/apis-docs/ilamparithi/IMDB_sample_app/1.0.0#/
(or)
https://sample-imdb.herokuapp.com/swagger/api-doc/

*Scalability Writeup:* https://drive.google.com/file/d/1M8m-Z5tgjg8A63r6thxw0yhNKlQjsKXU/view?usp=sharing
