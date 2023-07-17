from tkinter import *
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from datetime import datetime

# Interface
root = Tk()
root.title("Weather App")

# Geocoding
geolocator = Nominatim(user_agent="geoapiExercises")


def search():
    # cleaning listbox
    listbox.delete(0, END)

    # city latitude and longtitude
    city_name = city_name_entry.get()
    try:
        location_list = geolocator.geocode(city_name, exactly_one=False)
        for location in location_list:
            listbox.insert(END, f"{location.address} ({location.latitude}, {location.longitude})")
    except GeocoderTimedOut:
        listbox.insert(END, "Service is not available. Try again later.")


def get_weather():
    # parse data
    selected_location = listbox.get(listbox.curselection())
    address, lat_long = selected_location.split(" (")
    latitude, longitude = map(float, lat_long[:-1].split(", "))

    # openweather "5 Day / 3 Hour Forecast" API
    api_key = "bc880fa8b02061feba391b34cefd8d16"  # API, you can use this one also can take your own, it's free.
    base_url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()

    # print to textbox
    forecast_time = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
    result_text.insert(INSERT, f"Forecast Time: {forecast_time}\n")
    result_text.insert(INSERT, "Weather:\n")
    result_text.insert(INSERT, f"City: {data['name']}\n")
    result_text.insert(INSERT, f"Temperature: {data['main']['temp']}°C\n")
    result_text.insert(INSERT, f"Feels Like: {data['main']['feels_like']}°C\n")
    result_text.insert(INSERT, f"Minimum Temperature: {data['main']['temp_min']}°C\n")
    result_text.insert(INSERT, f"Maximum Temperature: {data['main']['temp_max']}°C\n")
    result_text.insert(INSERT, f"Atmospheric Pressure: {data['main']['pressure']} hPa\n")
    result_text.insert(INSERT, f"Humidity: {data['main']['humidity']}%\n")
    result_text.insert(INSERT, f"Weather Condition: {data['weather'][0]['description']}\n")
    result_text.insert(INSERT, "-------------------------------------------------------\n")


pad = 10

# City
# Label(root, text="City:").grid(row=0, column=0, sticky=E, padx=pad, pady=pad)
Label(root, text="City:").place(x=240, y=12)
city_name_entry = Entry(root)
city_name_entry.grid(row=0, column=1, sticky=E, padx=pad, pady=pad)

# Buttons
Button(root, text="Search", command=search).grid(row=0, column=2, sticky=W, padx=pad, pady=pad)
Button(root, text="Check Weather", command=get_weather).grid(row=1, column=2, sticky=W+N, padx=pad, pady=pad)

# Results
listbox = Listbox(root, width=60, height=10)
listbox.grid(row=1, column=0, columnspan=2, sticky=E, padx=pad, pady=pad)

# Weather info
result_text = Text(root)
result_text.grid(row=2, column=0, columnspan=3, sticky=W, padx=pad, pady=pad)


root.mainloop()
