from django.shortcuts import render
import os
import requests

# Create your views here.

API_KEY = os.environ.get("API_KEY")

def home(request):
    payload = {
        'message': 'not searched',
        'given_city': ''
    }

    if request.method == "GET":
        city = request.GET.get('city')
        if city:
            payload['given_city'] = city

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

            data = requests.get(url).json()

            # print(data)

            if (data['cod'] == '404' and data['message'] == "city not found"):
                payload = {
                    'message': 'city not found'
                }
            
            else:
                payload = {
                    'city': data['name'],
                    'weather': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'temp_kel': data['main']['temp'], #in kelvin
                    'feels_like_kel': data['main']['feels_like'], #in kelvin
                    'temp_max_kel': data['main']['temp_max'], #in kelvin
                    'temp_min_kel': data['main']['temp_min'], #in kelvin
                    'humidity': data['main']['humidity'], #in percentage
                    'pressure': data['main']['pressure'], #in mb
                    'wind_speed': data['wind']['speed'], #in m/s
                    'visibility': data['visibility'], #in m
                }



                #normal temp in celsius and fahrenheit
                payload['temp_cel'] = round(payload['temp_kel'] - 273.15, 2)
                payload['temp_far'] = round(((payload['temp_kel'] -273.15)*9/5)+32, 2)

                #feels like temp in celsius
                payload['feels_like_cel'] = round(payload['feels_like_kel'] - 273.15, 2)

                #min max temp in celsius
                payload['temp_max_cel'] = round(payload['temp_max_kel'] - 273.15, 2)
                payload['temp_min_cel'] = round(payload['temp_min_kel'] - 273.15, 2)


                #visibility in km
                payload['visibility_km'] = round(payload['visibility']/1000, 1)
    
        else:
            error_message = {'error': 'City parameter is missing'}
            print(error_message)

    return render(request, 'index.html', payload)    