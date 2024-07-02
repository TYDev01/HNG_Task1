from django.http import JsonResponse
import requests


my_weather_api_key = 'be0610be66cccb3fce8540aae404e8d7'



def get_ip(request):
    get_client_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if get_client_ip:
        ip = get_client_ip.split(',')[0]
    else:
        # ip = request.META.get('REMOTE_ADDR')
        ip = request.META.get('REMOTE_ADDR')
    return ip

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
