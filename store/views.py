from django.shortcuts import render
import json
from django.http import JsonResponse

# Create your views here.
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import Marker

def chat_box(request, chat_box_name):
    # we will get the chatbox name from the url
    return render(request, "chatbox.html", {"chat_box_name": chat_box_name})

def report(request):
    # Assuming the user is authenticated
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'listing.html', {'username': username})
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'index.html')
    
def housing(request):
    # Assuming the user is authenticated
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'findhousing.html', {'username': username})
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'index.html')
    
def modelmarker(request):
        # Parse the JSON data sent from the frontend
        
        data = json.loads(request.body.decode('utf-8'))
        
        # Access the individual parameters
        address = data.get('address')
        mapID = data.get('mapID')
        user = data.get('user')

        # Now you can do whatever you need to do with the data
        # For example, you can save it to the database
        # You may need to adjust this part based on your model structure
        # For demonstration purposes, let's assume you have a Marker model
        # with 'address' and 'stuff' fields
        marker = Marker.objects.create(address=address, mapID=mapID, user= user)
        marker.save()

        # Respond with a success message
        return render(request, 'listing.html', {'username': user})