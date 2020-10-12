from django.shortcuts import render, redirect
import django_semantic_ui, socket, googlemaps, requests, pytz
from datetime import datetime, timedelta
from .models import Trip
from pytz import timezone
from .api_keys import keys


# Create your views here.
def index(request):
    key_key = keys['key']
    request.session['api_key'] = keys['key']
    # print("Session Lat: {}\nSession Lng: {}".format(request.session['latitude'], request.session['longitude']))
    # print("Address: {}".format(request.session['address']))
    # print(request.session['geo_lat_lng'])
    print("Formatted Session Start: {}\nFormatted End: {}".format(request.session['formatted_starting_address'],request.session['formatted_ending_address']))
    print("Start Start: {}\nSession End: {}".format(request.session['starting_address'],request.session['ending_address']))
    context = {
        "key_key": key_key,
    }
    return render(request, 'google_maps_directions/index.html', context)


def enter(request):
    key_key = keys['key']
    context = {
        "key_key": key_key,
    }
    return render(request, 'google_maps_directions/enter.html', context)

def enter_trip(request):
    key_key = keys['key']
    now = datetime.now()
    # timezone = pytz.timezone("America/Los_Angeles")
    # d_aware = timezone.localize(now)
    gmaps = googlemaps.Client(key=key_key)
    if request.method == "POST":
        # gmaps = googlemaps.Client(key="AIzaSyA8ISZ4TkGCSGsurBj0jUPqztlTkfOwAog")
        starting_address = request.POST['starting_address']
        ending_address = request.POST['ending_address']
        print("Starting Address: {}\nEnding Address: {}".format(starting_address, ending_address))
        request.session['starting_address'] = starting_address
        request.session['ending_address'] = ending_address
        formatted_starting_address = ""
        for i in request.session['starting_address']:
            if i == " " or i == " ":
                formatted_starting_address += '%20'
            else:
                formatted_starting_address += i
        print("Formatted Starting Address: {}".format(formatted_starting_address))
        request.session['formatted_starting_address'] = formatted_starting_address
        formatted_ending_address = ""
        for i in request.session['ending_address']:
            if i == " " or i == " ":
                formatted_ending_address += '%20'
            else:
                formatted_ending_address += i
        print("Formatted Ending Address: {}".format(formatted_ending_address))
        request.session['formatted_ending_address'] = formatted_ending_address
        geo_starting_address = gmaps.geocode(starting_address)
        geo_ending_address = gmaps.geocode(ending_address)
        geo_start_lat = geo_starting_address[0]['geometry']['location']['lat']
        geo_start_lng = geo_starting_address[0]['geometry']['location']['lng']
        geo_end_lat = geo_ending_address[0]['geometry']['location']['lat']
        geo_end_lng = geo_ending_address[0]['geometry']['location']['lng']
        print("Geocoded Starting Address Latitude: {}\nGeocoded Starting Address Longitude: {}".format(geo_start_lat, geo_start_lng))
        print("Geocoded Ending Address Latitude: {}\nGeocoded Endting Address Longitude: {}".format(geo_end_lat, geo_end_lng))
        starting_lat_lng = str(geo_start_lat) + "," + str(geo_start_lng)
        ending_lat_lng = str(geo_end_lat) + "," + str(geo_end_lng)
        request.session['starting'] = starting_lat_lng
        request.session['ending'] = ending_lat_lng
        #Directions Result
        directions_result = gmaps.directions(starting_address,
        ending_address,
        mode="driving",
        departure_time=now)
        print("Directions Result: {}".format(directions_result))
        request.session['directions_result'] = directions_result
        session_directions_result = request.session['directions_result']
        print(request.session['directions_result'])
        Trip.objects.create_trip(request.POST)
        trips = Trip.objects.all()
        print("This is all of the trips that have been taken: {}".format(trips))
        print("First Results: \n{}".format(request.session['directions_result'][0]))
        print("Current Time: {}".format(now))
        # print("D Aware: {}".format(d_aware))
        for directions in directions_result:
            duration_string = directions["legs"][0]['duration']['text']
            print("Duration String: {}".format(duration_string))
            duration_seconds_value = directions["legs"][0]['duration']['value']
            duration_hours = int(duration_seconds_value / 3600)
            duration_minutes = int((duration_seconds_value % 3600) / 60)
            print("Duration Hours: {}\nDuration Minutes: {}".format(duration_hours, duration_minutes))
            arrival_time = now + timedelta(hours=duration_hours, minutes=duration_minutes)
            print("Arrival Time: {}".format(arrival_time))
            arrival_time_string = str(arrival_time)
            arrival_hour = arrival_time_string[11:13]
            arrival_minutes = arrival_time_string[14:16]
            print("Arrival Hour: {}".format(arrival_hour))
            print("Arrival Minutes: {}".format(arrival_minutes))
        # print("D Aware: {}".format(d_aware))
        # print("Now: {}".format(now))
        print("API Key: {}".format(key_key))
        context = {
            'directions_result': directions_result,
            'formatted_starting_address': formatted_starting_address,
            'formatted_ending_address': formatted_ending_address,
            'starting_address': starting_address,
            'ending_address': ending_address,
            'session_formatted_starting_address': request.session['formatted_starting_address'],
            'session_formatted_ending_address': request.session['formatted_ending_address'],
            'geo_starting_address': geo_starting_address,
            'geo_ending_address': geo_ending_address,
            'gmaps': gmaps,
            'now': now,
            'session_directions_result': session_directions_result,
            'trips': trips,
        }
    else:
        print("Error!")
    return redirect('/', context)


