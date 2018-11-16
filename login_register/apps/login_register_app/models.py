# By Andy Nguyen
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # Validation Rules for First Name
        if len(postData['first_name']) < 1:
            errors["first_name"] = "First name is required"
        elif len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        elif not postData['first_name'].isalpha():
            errors["first_name"] = "First Name can only have letters"
        
        # Validation Rules for Last Name
        if len(postData['last_name']) < 1:
            errors["last_name"] = "Last name is required"
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        elif not postData['last_name'].isalpha():
            errors["last_name"] = "Last name can only have letters"

        # Validation Rules for Email
        if len(postData['email']) < 1:
            errors["email"] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address"
        if User.objects.filter(email = postData['email']):
            errors["email"] = "Sorry, email is already in use"
        
        # Validation Rules for Password
        if len(postData['password']) < 1:
            errors["password"] = "Password is required"
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        
        # Validation Rules for Confirm Password
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Password and Password Confirmation did not match"

        return errors
    
    def login_validator(self, postData):
        errors = {}
        # Validation Rules for Login Email
        if len(postData['email']) < 1:
            errors["email"] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address"
        elif not User.objects.filter(email = postData['email']):
            errors["email"] = "This account does not exist. Please register."
            
        # Validation Rules for Login Password
        if len(postData['password']) < 1:
            errors["password"] = "Password is required"
        else:
            user = User.objects.get(email=postData['email'])
            print(user)
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors["password"] = "Password is not correct"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"<User: {self.id} {self.first_name} {self.last_name} {self.email}>"
    
    objects = UserManager()
    