from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = {}
        try:
            if len(postData['first_name']) < 3 or str.isalpha(postData['first_name']) == False:
                errors['first_name'] = "First name must contain at least 3 characters, letters only"

            if len(postData['last_name']) < 3 or str.isalpha(postData['last_name']) == False:
                errors['last_name'] = "Last name must contain at least 3 characters, letters only"

            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Invalid email address"
            elif EMAIL_REGEX.match(postData['email']):
                existing_emails = User.objects.values_list('email', flat=True)
                # flat = going to just give the value you want not key
                if postData['email'] in existing_emails:
                    errors['email'] = "Email already in use"
            
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters"

            if postData['password'] != postData['confirm']:
                errors['password'] = "Passwords do not match"
        except:
            errors['general'] = 'Something unexpected occured. Please try again'
            # general means nothing
        return errors 
    
    def validate_login(self, postData):
        errors = {}
        try:
            if postData['log_email'] == '':
                errors['log_email'] = "Must input valid email"
            existing_emails = User.objects.values_list('email', flat=True)
            print(existing_emails)
            # flat = going to just give the value you want not key
            if not postData['log_email'] in existing_emails:
                errors['log_email'] = "User does not exist"
            else:
                if postData['log_password'] == '':
                    errors['log_password'] = "Must input valid password"
                existing_user = User.objects.filter(email = postData['log_email'])
                if not bcrypt.checkpw(postData['log_password'].encode(), existing_user[0].password.encode()):
                    errors['log_email'] = "Email and/or password do not match"
        except:
            errors['log_email'] = 'Something unexpected occured. Please try again'
            # general means nothing
        return errors 


class PartyManager(models.Manager):
    def validate_party(self,postData):
        errors = {}
        try:
            if len(postData['title']) < 3:
                errors['title'] = "A title must have at least 3 characters"

            if len(postData['description']) < 3 :
                errors['description'] = "A description must have at least 3 characters"

            if len(postData['address']) < 3 :
                errors['address'] = "An address must have at least 3 characters"

            if len(postData['city']) < 3 :
                errors['city'] = "A city must have at least 3 characters"

            if len(postData['state']) > 2 or len(postData['state']) < 2:
                errors['state'] = "An state must have 2 characters"

            if len(postData['zip_code']) < 5 or len(postData['zip_code']) > 5:
                errors['zip_code'] = "A zip code must have 5 numbers"

            if datetime.datetime.strptime(postData['date'], '%Y-%m-%d') < datetime.datetime.today():
                errors['date'] = 'Party date must be in the future'
        except:
            errors['general'] = 'Something unexpected occured. Please try again'
        return errors
        
    def validate_route(self, id):
        errors = {}
        try:
            Party.objects.get(id = int(id))
        except:
            errors['general'] = 'Something unexpected occured. Please try again'
            # general means nothing
        return errors

class MessageManager(models.Manager):
    def message_validator(self, postData):
        errors = {}
        try:
            if postData['message'] == '':
                errors['message_error'] = 'You need to write a message'
        except:
            errors['message_error'] = 'You need to write a message'
        return errors

class CommentManager(models.Manager):
    def comment_validator(self, postData):
        errors = {}
        try:
            if postData['comment'] == '':
                errors['comment'] = 'You need to write a comment'
        except:
            errors["general"] = "Invalid Route. Please try again"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # party_made
    # party_joined
    # messages_made
    # comments_made
    objects = UserManager()

class Party(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    address = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zip_code = models.IntegerField()
    date = models.DateField(null=True)
    creator = models.ForeignKey(User, related_name="party_made")
    participant = models.ManyToManyField(User, related_name="party_joined")
    # connects to the User
    # related_name relects class you are in
    # party_message
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PartyManager()


class Messages(models.Model):
    user = models.ForeignKey(User, related_name="messages_made")
    party = models.ForeignKey(Party, related_name="party_message", null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()
    # comment_to_message
        

class Comments(models.Model):
    commenttomessage = models.ForeignKey(Messages, related_name="comment_to_message")
    commentmaker = models.ForeignKey(User, related_name="comments_made")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()