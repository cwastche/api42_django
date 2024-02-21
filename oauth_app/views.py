from django.shortcuts import render

from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
import requests

def authorize(request):
    auth_url = f"https://api.intra.42.fr/oauth/authorize?client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}&response_type=code"

    return redirect(auth_url)

def dashboard(request):
    code = request.GET.get('code')
    if code:
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'code': code,
            'redirect_uri': settings.REDIRECT_URI
        }
        
        # Make the POST request
        response = requests.post('https://api.intra.42.fr/oauth/token', data=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Here you can process the access token, refresh token, etc.
            token_info = response.json()
            return HttpResponse(f"Access Token: {token_info.get('access_token')}")
        else:
            return HttpResponse("Failed to retrieve access token", status=response.status_code)
    else:
        return HttpResponse("No code provided or error occurred")
