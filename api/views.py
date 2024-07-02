from django.http import JsonResponse
import requests
from ipware import get_client_ip

my_weather_api_key = 'be0610be66cccb3fce8540aae404e8d7'

def get_ip(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip = request.META.get('REMOTE_ADDR')
    return client_ip

def get_location(request):
    try:
        ip_address = get_ip(request)
        user_location_data = requests.get(f'https://ipinfo.io/{ip_address}/json/').json()
        
        city = user_location_data.get("city")
        
        weather_response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={my_weather_api_key}&units=metric', timeout=20
        )
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        
        return {
            "ip": ip_address,
            "city": city,
        }, temperature
    except requests.RequestException:
        return {
            "ip": ip_address,
            "city": "Unknown city",
        }, "N/A"

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Visitor')
    client_ip = get_ip(request)

    user_location_data, temperature = get_location(request)

    greeting = f"Hello, {visitor_name.capitalize()}!, the temperature is {temperature} degrees Celsius in {user_location_data['city']}"
    response_data = {
        'client_ip': client_ip,
        'location': user_location_data['city'],
        'greeting': greeting
    }

    return JsonResponse(response_data)
