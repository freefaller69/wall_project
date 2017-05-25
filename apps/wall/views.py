# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Message, Comment
import re
EMAILREG = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your views here.
def index(request):
    return render(request, "wall/index.html")

def wall(request):
    context = {
        "user_messages": Message.objects.all().order_by('id').reverse(),
        "user_comments": Comment.objects.all().order_by('id'),
    }
    return render(request, "wall/wall.html", context)

def post_message(request):
    if request.method == 'POST':
        if request.POST["wall_posts"] == "message_submit":
            response = Message.objects.new_message_input(request.POST, request.session['user']['id'])
        if request.POST["wall_posts"] == "comment_submit":
            response = Comment.objects.new_comment_input(request.POST, request.session['user']['id'])
    return redirect('wall:wall')

def user(request, id):
    context = {
        "user": User.objects.get(id=id),
    }
    return render(request, "wall/user.html", context)

def all_users(request):
    context = {
        "all": User.objects.all(),
    }
    return render(request, "wall/allusers.html", context)

def entrance(request):
    if request.method == "POST":
        if request.POST["gate"] == "register":
            response = User.objects.check_create(request.POST)
        elif request.POST["gate"] == "login":
            response = User.objects.check_login(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
            return redirect('wall:index')
        else:
            request.session['user'] = {
            "id": response[1].id,
            "first_name": response[1].first_name,
            "last_name": response[1].last_name,
            }
            return redirect('wall:all_users')
    return redirect('wall:index')

def user_update(request):
    user_id = str(request.session['user']['id'])
    if request.method == "POST":
        if request.POST["update_option"] == "profile":
            response = User.objects.check_update(request.POST, request.session['user']['id'])
        if request.POST["update_option"] == "password":
            response = User.objects.check_password(request.POST, request.session['user']['id'])
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
        return redirect('/user/'+user_id)
    return redirect('/user/'+user_id)

def user_delete(request):
    user_id = request.session['user']['id']
    User.objects.filter(id=user_id).delete()
    return redirect('wall:logout')

def logout(request):
    request.session.clear()
    return redirect('wall:index')
