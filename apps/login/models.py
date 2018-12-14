from django.db import models
import datetime
import re
import bcrypt
import datetime

class Validator(models.Manager):
    def basic_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["title"] = "First Name should be at least 2 characters,letters only"
        if len(postData['last_name']) < 2:
            errors["network"] = "Last Name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']='Invalid email adress'
        hello=User.objects.filter(email=(postData['email']))
        if  hello:
            errors['duplicate']='email alredy exist...please create a new one'
        if not  PASSWORD_REGEX.match(postData['password']):
            errors['password']='Password must be greater than 8 characters!Password must contain at least one lowercase letter, one uppercase letter, and one digit'
        if len(postData['password'] )!= len(postData['conf_pass']):
            errors['conf_pass']="Confirm the password!"
        if (postData['birthday']) != "":
            if datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.datetime.now():
                errors['erelease_date']= "Are you kidding me? put your real birthday please)"
            today=datetime.datetime.today()
            yearGap=datetime.timedelta(days=4745)
            user=datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
            if today - yearGap <= user:
                errors['young']='you need to be 13 or older to register in this website'
        if (postData['birthday'])== "":
            errors['birthday']="Please enter your birthday"
        return errors
        
    def login_validator(self,postData):
        errors={}
        user = User.objects.filter(email=(postData['email']))	
        if len(user) == 0:
            errors['email']='There is no such email'
        elif bcrypt.checkpw((postData['password']).encode(),user[0].password.encode()):
            print('hello')
        else:
            errors['password']="Invalid password"
        return errors
        
        
class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateTimeField()
    email = models.CharField(max_length=255)
    password=models.CharField(max_length =255)
    objects = Validator()

class Message(models.Model):
    user = models.ForeignKey(User,related_name='messages')
    message=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user =models.ForeignKey(User,related_name='comments')
    message= models.ForeignKey(Message,related_name='comments')



