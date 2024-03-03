from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

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