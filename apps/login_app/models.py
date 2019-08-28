from __future__ import unicode_literals
from django.db import models
from datetime import date, datetime
import re


# pip install validate_email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# password rules
rulesp =[lambda s: any(x.isupper() for x in s), # must have at least one uppercase
        lambda s: any(x.islower() for x in s),  # must have at least one lowercase
        lambda s: any(x.isdigit() for x in s),  # must have at least one digit
        lambda s: len(s) >= 8  and len(s) <= 50,  # must be at least 7 characters
        ]

# first, last name rules    
rulesn =[lambda s: any(x.isalpha() for x in s), # must be letters      
        lambda s: len(s) > 2  and len(s) < 20,  # must be at least 2 characters
        ]
passstring = "password must have at least one uppercase \nat least one lowercase\n \
    at least one digit\nat least 7 characters and no more than 50 characters long."

class ShowManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first_name should be at least 2 characters"
        if not all(rule(postData['first_name']) for rule in rulesn):
            errors["first_name"] = "First Name should be at least 8 characters long and should include only letters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last_name should be at least 2 characters"
        if not all(rule(postData['last_name']) for rule in rulesn):
            errors["last_name"] = "Last Name should be at least 8 characters long and should include only letters."
        if len(postData['password']) < 7:
            errors["password"] = "network should be at least 3 characters"
        
        # if len(postData['email']) < 7:
        #     errors["email"] = "network should be at least 3 characters"

        if not EMAIL_REGEX.match(postData['email']): 
            errors["email"]  = "Invalid email format." 

        if not all(rule(postData['password']) for rule in rulesp):
            errors["password"] = passstring
        if  postData['password'] != postData['password2']:
            errors["password"] = "Password do not match"  
        return errors
    
    
    
class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    # description = models.TextField(null=True)
    # release_date=models.DateTimeField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects =ShowManager()
