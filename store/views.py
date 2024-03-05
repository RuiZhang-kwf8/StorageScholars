from django.shortcuts import render, redirect 
import json
from django.http import JsonResponse, HttpRequest, StreamingHttpResponse, HttpResponse

from datetime import datetime
import asyncio

from typing import AsyncGenerator
from . import models
import random

# Create your views here.
from django.shortcuts import redirect
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from .models import Marker
from django.core.mail import send_mail

import json
from allauth.socialaccount.models import SocialAccount

def get_user_email(request, username):
    try:
        # Get the user's social account associated with Google
        social_account = SocialAccount.objects.filter(user__username=username, provider='google').first()

        if social_account:
            # Access the user's email address
            email = social_account.extra_data.get('email')
            return JsonResponse({'email': email})
        else:
            return JsonResponse({'error': 'User does not have a Google social account'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)









def send_email(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body)
        
        recipient = data.get('recipient')
        chat_link = data.get('chatLink')

        # Validate recipient and chat_link
        if not recipient or not chat_link:
            return JsonResponse({'status': 'error', 'message': 'Recipient or chat link missing'}, status=400)

        try:
            # Send the email
            send_mail(
                'New Chat Request',
                f'You have received a new chat request. Click the following link to start the chat: {chat_link}',
                'ruizhangslc2017@example.com',  # Replace with your sender email address
                [recipient],
                fail_silently=False,
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def chat_box(request, chat_box1):
    # we will get the chatbox name from the url
    return render(request, "chatbox.html", {"box1": chat_box1})

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


    
def get_markers(request):
    # Query your database to get the markers
    markers = Marker.objects.all()  # Assuming you have a Marker model

    # Serialize the marker data
    serialized_markers = []
    for marker in markers:
        serialized_markers.append({
            'address': marker.address,
            'mapID': marker.mapID,
            'user': marker.user,
            # Add more fields as needed
        })

    # Return the serialized markers as a JSON response
    return JsonResponse(serialized_markers, safe=False)




def create_message(request: HttpRequest) -> HttpResponse:
    content = request.POST.get("content")
    username = request.session.get("username")

    if not username:
        return HttpResponse(status=403)
    author, _ = models.Author.objects.get_or_create(name=username)

    if content:
        models.Message.objects.create(author=author, content=content)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=200)



async def stream_chat_messages(request, username):
    """
    Streams chat messages to the client as we create messages.
    """
    async def event_stream():
        """
        We use this function to send a continuous stream of data 
        to the connected clients.
        """
        async for message in get_existing_messages(username):
            yield message

        last_id = await get_last_message_id(username)

        # Continuously check for new messages
        while True:
            new_messages = models.Message.objects.filter(
                id__gt=last_id, author__name=username
            ).order_by('created_at').values(
                'id', 'author__name', 'content'
            )
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message['id']
            await asyncio.sleep(0.1)  # Adjust sleep time as needed to reduce db queries.

    async def get_existing_messages(username) -> AsyncGenerator:
        messages = models.Message.objects.filter(author__name=username).order_by('created_at').values(
            'id', 'author__name', 'content'
        )
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"

    async def get_last_message_id(username) -> int:
        last_message = await models.Message.objects.filter(author__name=username).last()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
