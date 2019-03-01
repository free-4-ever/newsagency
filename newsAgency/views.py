from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from .models import Author, Story
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models.functions import Now

# Create your views here.
@csrf_exempt
def HandleLoginRequest (request):
   if request.method != 'POST':
      http_bad_request = HttpResponseBadRequest()
      http_bad_request['Content-Type'] = 'text/plain'
   else:
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username = username, password = password)

      if user is not None:
         if user.is_active:
            if user.is_authenticated:
               request.session['user'] = username
               http_response = HttpResponse('Login successful')
               http_response.status_code = 200
               http_response['Content-Type'] = 'text/plain'
               return http_response
         else:
            return HttpResponse('Disabled account!')
      else:
         http_response = HttpResponse('Username or password incorrect!')
         http_response.status_code = 400
         http_response['Content-Type'] = 'text/plain'
         return http_response

@csrf_exempt
def HandleLogoutRequest(request):
   if request.session['user']:
      logout(request)
      http_response = HttpResponse('Logout successful')
      http_response.status_code = 200
      http_response['Content-Type'] = 'text/plain'
      return http_response
   else:
      http_response = HttpResponse('No session detected!')
      http_response.status_code = 400
      http_response['Content-Type'] = 'text/plain'
      return http_response

@csrf_exempt
def HandleNewPostRequest(request):
   if request.session['user']:
      user = User.objects.get(username=request.session['user'])
      author = Author.objects.get(user=user)
      headline = request.POST['headline']
      category = request.POST['category']
      region = request.POST['region']
      details = request.POST['details']

      story = Story(author=author, headline=headline, category=category, region=region,
                     details=details, pub_date=Now())
      story.save()
      http_response = HttpResponse('Story created!')
      http_response.status_code = 201
      http_response['Content-Type'] = 'text/plain'
      return http_response
   else:
      http_response = HttpResponse('Not Authenticated!')
      http_response.status_code = 503
      http_response['Content-Type'] = 'text/plain'
      return http_response

@csrf_exempt
def HandleNewsRequest(request):
   if request.method == 'GET':
      # return 'rrrrs'
      #    category = request.GET['story_cat']
      stories = Story.objects.filter(category=request.GET['story_cat'], region=request.GET['story_region'],
                                    pub_date=request.GET['story_date'])
      if (stories.count()):
         # http_response = HttpResponse()
         # http_response.status_code = 200
         # http_response['Content-Type'] = 'application/json'
         return JsonResponse(stories)
      else:
         http_response = HttpResponse('Your query returned no results!')
         http_response.status_code = 404
         http_response['Content-Type'] = 'text/plain'
         return http_response
   else:
      http_response = HttpResponse('Not Authenticated!')
      http_response.status_code = 503
      http_response['Content-Type'] = 'text/plain'
      return http_response

@csrf_exempt
def HandleDeleteRequest(request):
   if request.session['user']:
      story = Story.objects.get(id=request.POST['story_key'])
      story.delete()
      http_response = HttpResponse('Story deleted!')
      http_response.status_code = 201
      http_response['Content-Type'] = 'text/plain'
      return http_response
   else:
      http_response = HttpResponse('Not Authenticated!')
      http_response.status_code = 503
      http_response['Content-Type'] = 'text/plain'
      return http_response