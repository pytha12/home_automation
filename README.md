# django-rest-framework home automation API
Home automation application

Purpose: 
  - Setup Houses, Rooms 
  - Get information about a given house and rooms, 
  - Turn off and on lights, and change the state of the furnace.
  - Save energy whenever furnace status changes (Furnaces automatically set max or min furnace temperature to the 
    maximum or minimum room temperature required by the rooms there by cutting down on energy waste). 
    
 Setup:
   - python 3.7+
   - install and activate virtualenv
   - install pip
   - pip install Django==2.1.4
   - pip install djangorestframework==3.9.0
   - django-admin startproject your_project_name
     cd your_project_name
   - Edit your_project_name\settings.py
   
      INSTALLED_APPS = (
             ...
         'rest_framework',
         'hauto.apps.HautoConfig',
      )
      
      REST_FRAMEWORK = {
         'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
         'PAGE_SIZE': 10
      }



