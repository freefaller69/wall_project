# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re
EMAILREG = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z)(?=.*[\W_]).{8,}$')
# Create your models here.
class UserDataManager(models.Manager):
    def check_create(self, data):
        errors = []
        if len(data['firstName']) < 2:
            errors.append(['firstName', "First Name must be at least two characters in length."])
        if len(data['lastName']) < 2:
            errors.append(['lastName', "Last Name must be at least two characters in length."])
        if not re.match(EMAILREG, data['email']):
            errors.append(['email', "Email must be a valid address."])
        if not re.match(PASSWORD_REGEX, data['password']):
            errors.append(['password', "Password must be at least 8 characters in length and  include 1 uppercase letter, 1 lowercase letter, and 1 number."])
        if (data['password'] != data['pwdConfirm']):
            errors.append(['pwdConfirm', "Password confirmation does not match.  Please reenter."])
        if errors:
            return [False, errors]
        else:
            mail_check = User.objects.filter(email=data['email'])
            if mail_check:
                errors.append(['mail_check', "Unable to register, please use alternate information."])
                return [False, errors]
            newUser = User(first_name=data['firstName'], last_name=data['lastName'], email=data['email'])
            hashed_pass = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            newUser.pw_hash = hashed_pass
            newUser.save()
            return [True, newUser]

    def check_update(self, data, id):
        errors = []
        user_id = User.objects.get(id=id)
        if data['firstName'] != "":
            User.objects.filter(id=id).update(first_name=data['firstName'])
        if data['lastName'] != "":
            User.objects.filter(id=id).update(last_name=data['lastName'])
        if data['email'] != "":
            if not re.match(EMAILREG, data['email']):
                errors.append(['email', "Email must be a valid address."])
            mail_check = User.objects.filter(email=data['email'])
            if mail_check:
                errors.append(['mail_check', "Invalid email, please use alternate information."])
                return [False, errors]
            if errors:
                return [False, errors]
            User.objects.filter(id=id).update(email=data['email'])
        return [True]

    def check_password(self, data, id):
        errors = []
        user_id = User.objects.get(id=id)
        if data['password'] != "":
            if not re.match(PASSWORD_REGEX, data['password']):
                errors.append(['password', "Password must be at least 8 characters in length and  include 1 uppercase letter, 1 lowercase letter, and 1 number."])
            if (data['password'] != data['pwdConfirm']):
                errors.append(['pwdConfirm', "Password confirmation does not match.  Please reenter."])
            if errors:
                return [False, errors]
            hashed_pass = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            pw_hash = hashed_pass
            print "x"*100
            print pw_hash
            print "x"*100
            User.objects.filter(id=id).update(pw_hash=pw_hash)
        return [True]

    def check_login(self, data):
        errors= []
        current_user = User.objects.filter(email=data['email'])
        if not current_user:
            errors.append(['account', "Invalid username/password combination."])
        elif not bcrypt.checkpw(data['password'].encode(), current_user[0].pw_hash.encode()):
            errors.append(['account', "Invalid username/password combination."])
        if errors:
            return [False, errors]
        else:
            return [True, current_user[0]]

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserDataManager()

    def __str__(self):
        return 'ID: %s | Name: %s %s | Email: %s | Created: %s | Updated: %s' % (self.id, self.first_name, self.last_name, self.email, self.created_at, self.updated_at)

class MessageDataManager(models.Manager):
    def new_message_input(self, data, id):
        errors= []
        user_id = User.objects.get(id=id)
        if len(data['message_input']) < 2:
            errors.append(['message', "Messages have a minimum length of two characters."])
        if errors:
            return [False, errors]
        else:
            newMessage = Message(message=data['message_input'], user_id=user_id)
            newMessage.save()
            return [True]

class Message(models.Model):
    message = models.TextField(max_length=1000)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MessageDataManager()

    def __str__(self):
        return 'ID: %s | Message: %s | User_ID: %s | CreatedAt: %s' % (self.id, self.message, self.user_id, self.created_at)

class CommentDataManager(models.Manager):
    def new_comment_input(self, data, id):
        errors= []
        user_id = User.objects.get(id=id)
        message_id = Message.objects.get(id=data['message_id'])
        if len(data['comment_input']) < 2:
            errors.append(['comment', "Comments have a minimum length of two characters."])
        if errors:
            return [False, errors]
        else:
            newComment = Comment(comment=data['comment_input'], user_id=user_id, message_id=message_id)
            newComment.save()
            return [True]

class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentDataManager()

    def __str__(self):
        return self.comment
        return 'ID: %s | Comment: %s | User_ID: %s | Message_ID: %s | CreatedAt: %s' % (self.id, self.comment, self.user_id, self.message_id, self.created_at)
