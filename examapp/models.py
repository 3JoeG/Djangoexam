from django.db import models
import re
from datetime import date


class UserManager(models.Manager):
    def registrationValidator(self, inputdata):
        errors={}
        f_regex= re.compile(r'^[a-zA-Z]+$')
        l_regex= re.compile(r'^[a-zA-Z]+$')
        email_regex= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(inputdata['first'])==0:
            errors['fnone']='first name required'
        elif len(inputdata['first'])<2:
            errors['flen']='First name must be at least 2 characters'
        elif not f_regex.match(inputdata['first']):
            errors['fchar']='First name must only be letters'

        if len(inputdata['last'])==0:
            errors['lnone']='Last name required'
        elif len(inputdata['last'])<2:
            errors['llen']='Last name must be at least 2 characters'
        elif not l_regex.match(inputdata['last']):
            errors['lchar']='Last name must only be letters'

        if len(inputdata['email'])==0:
            errors['enone']='Email required'
        elif not email_regex.match(inputdata['email']):               
            errors['epat'] = "Invalid email address!"
        elif len(Users.objects.filter(email=inputdata['email']))>0:
            errors['dup']= "Email already exists! Please Login."

        if len(inputdata['pw'])==0:
            errors['pass']='Password required'
        elif len(inputdata['pw'])<8:
            errors['passlen']='Password must be 8 characters long'
        elif inputdata['pw']!=inputdata['con']:
            errors['match']='Passwords must match'
        return errors

    def loginvalidator(self, inputdata):
        errors={}  
        matchingemail=Users.objects.filter(email = inputdata['em'])  
        if len(matchingemail)==0:
            errors['emin']="Email doesn't exist please register"
        elif matchingemail[0].pword != inputdata['pw']:
            errors['pwmat']="Passwords don't match"
        return errors

    def tripvalidator(self, inputdata):
        errors={}
        if len(inputdata['place'])==0:
            errors['nowhere']='Place Required'
        elif len(inputdata['place'])<3:
            errors['few']='Place needs to be at least 3 Char'
        if inputdata['to']<inputdata['from']:
            errors['timetravel']='To date needs to be after From date'
        if not inputdata['from']:
            errors['fdate']='Need a From date'    
        if not inputdata['to']:
            errors['tdate']='Need a To date'    
        if inputdata['from']<date.today():
            errors['past']='Invalid Date'
        return errors

# Create your models here.
class Users(models.Model):
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.EmailField()
    pword=models.CharField(max_length=50)
    created=models.DateTimeField(auto_now_add=True)
    update= models.DateTimeField(auto_now=True)
    objects= UserManager()


class Travels(models.Model):
    place=models.CharField(max_length=255)
    desc=models.TextField()
    people=models.ManyToManyField(Users,related_name='going')
    travel_from=models.DateField()
    travel_to=models.DateField()
    created_by=models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    update= models.DateTimeField(auto_now=True)
    objects= UserManager()

