from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.contrib.auth.models import AbstractBaseUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

from .models import *



def index(request):
    # try:
    #     user = User.objects.get(username=request.user)
    # except User.DoesNotExist:
    #     return JsonResponse({"Error": "user was not found"}, status=400)
    
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

@csrf_exempt
def allpost(request):
     if request.method == 'POST':
       # try:
        data = json.loads(request.body)
        # except json.JSONDecodeError:
        #    return JsonResponse({'Error': 'post was not loaded'}, status=400)
       
        if data.get('post') is not None:
           p = Post(body=data.get('post'), username=request.user)
           p.save()
           
     posts = Post.objects.all()
     posts = posts.order_by('-time').all().reverse()
     return JsonResponse([post.serialize() for post in posts], safe=False)
   
    
@csrf_exempt
def likes(request, post_id, username):
     try:
        post = Post.objects.get(id=post_id)
        # to make sure user is loged in
        if (username != 'guest'):
            user = User.objects.get(username=username)

     except Post.DoesNotExist or User.DoesNotExist:
        return JsonResponse({"Error": "Invalid post id or username"}, status=404)
     
     if request.method == 'PUT':
          data = json.loads(request.body)
          if data.get('likes') is not None:
             #add user if he likes remove if he dislikes
             if data.get('likes') == 'liked':
                 # if the user has already liked the post
                 likers = post.likers()
                 if user.id in likers['liked_by']:
                     return JsonResponse({'Error': 'User has already liked this post'})
                 
                 post.likes += 1
                 post.liked_by.add(user.id)
             else:
                 # if likes are already zero cannot be unliked
                 if post.likes == 0:
                     return JsonResponse({'Error': "zero likes can not be unliked"})
        
                 post.likes -= 1
                 try:
                     post.liked_by.remove(user.id)
                 except ValueError:
                     return JsonResponse({'Error': 'fuck'}, status=400)
             
             post.save()
          else:
              return JsonResponse({'error': 'likes was not updated'}, status=400)
          
     elif username != 'guest':
         likers = post.likers()
         like = 'None'
         if user.id in likers['liked_by']:
             like = 'liked'
         else:
             like = 'notliked'
         
         return JsonResponse(like, safe=False)
     
     # sends post likes either way 
     return JsonResponse(post.likes, safe=False)
    

@csrf_exempt
def user(request, username, current_user):
    if request.method == "GET":
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"Error": "User does not exist"}, status=400)
        
        try:
            posts = Post.objects.filter(username=username).all()
        except Post.DoesNotExist:
            return JsonResponse({'Error': 'User was not found'}, status=500)
        
        follow = 'None'
        if current_user != 'guest':
            f = Follow.objects.get(user=current_user)
            followers = f.follower()
            if current_user in followers:
               follow = 'followed'
            else:
               follow = 'notfollowed'
       
        # to count the followers
        followers = Follow.objects.filter(following=user).count()
        
        # to count the followings
        followings = Follow.objects.filter(user=user)
        followings = followings.count()

        #posts = posts.reverse('-time').all()
        posts = posts.order_by('-time').all()
        return JsonResponse({'followings': followings, 'followers': followers, 'follow': follow, 'post': [post.serialize() for post in posts]}, safe=False)
    
   

@csrf_exempt
def following(request, username):
    if request.method == 'PUT':
        try:
            usr = User.objects.get(username=username)
        except User.DoesNotExist or ValueError:
            return JsonResponse({"Error": "User does not exist"}, status=400)
        
        try:
            current_user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return JsonResponse({'Error': 'current_user'}, status=401)
        
        data = json.loads(request.body)
        # adding the removing the follow according to the button click
        if data.get('follow') == 'followed':
            # try:
            #     # check if the user has already followed the current user 
            #     # if not then add the user
            #     f = Follow.objects.get(user=username)
            f = Follow(user=current_user, following=usr)
            f.save()
        else:
            try:
                f = Follow.objects.filter(user=current_user, following=usr).all()
                f.delete()
                f.save()
            except ValueError or Follow.DoesNotExist:
                return JsonResponse({"Error": "Value Error"}, status=401)
        
        
        # so the user function is able process it like a get function
        request.method = 'GET'
        return user(request, username, request.user)
    
    return JsonResponse({'Error': 'wrong input'}, status=400)
