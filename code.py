import os
import time
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import displayio
import busio
import sharpdisplay
import framebufferio
import gc
import terminalio
from adafruit_display_text import label
import microcontroller
import rtc
#Connect to SSID
wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'), os.getenv('CIRCUITPY_WIFI_PASSWORD'))
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
gc.collect()
#---------------------------------------------------------------------------------------------------
#Initialize Display
displayio.release_displays()
spi_bus = busio.SPI(board.GP14, MOSI=board.GP15)
framebuffer = sharpdisplay.SharpMemoryFramebuffer(spi_bus, board.GP13, 400, 240)
display = framebufferio.FramebufferDisplay(framebuffer, auto_refresh = True)
#---------------------------------------------------------------------------------------------------
#Used to convert Kelvin to Farenheit
def k_to_f(k):
    return (k - 273.15) * 9/5 + 32
#Used to convert meters/second into miles.hour
def ms_to_mph(ms):
    return ms * 2.23694
#Used to convert millimeters to inches
def mm_to_in(mm):
    return mm * 0.0393701
#Used to find the hour and minute from posix time
def posix_to_hrsmins(posix):
    currtime = time.localtime(posix)
    return "{:02}:{:02}".format(currtime[3] + 5, currtime[4])
#Used to add a leading zero to the minutes value, turns 6 into 06, 7 into 07, etc.
def add_lead_zero(num):
    if 0 <= num <= 9:
        return f"0{num}"
    else:
        return num
#---------------------------------------------------------------------------------------------------
#Set correct current time using WorldTimeAPI
time_response = requests.get("http://worldtimeapi.org/api/timezone/America/Los_Angeles")
time_data = time_response.json()
time_response.close()
rtc.RTC().datetime = time.localtime(time_data['unixtime'])
#---------------------------------------------------------------------------------------------------
#Fetch weather data from OpenWeatherMap
weather_response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Seattle&appid=19ccdc9363d94d7eeca102ec82c34007")
data = weather_response.json()
weather_response.close()
rain_last_hour = 'None'
if 'rain' in data:
    rain_last_hour = mm_to_in(data['rain']['1h']) + 'in'
font = terminalio.FONT
color = 0xFFFFFF
# Create the text label
city = data['name']
weather_text_area = label.Label(font, text=f"""
WEATHER RIGHT NOW IN {city}
----------------------------------
Temperature: {k_to_f(data['main']['temp'])}F
Feels Like: {k_to_f(data['main']['feels_like'])}F
Description: {data['weather'][0]['description']}
Wind: {ms_to_mph(data['wind']['speed'])}mph
Rain Last Hour: {rain_last_hour}
Humidity: {data['main']['humidity']}%
Sunset Today: {posix_to_hrsmins(data['sys']['sunset'])}
---------------------------------
""", color=color)
# Set the text location
weather_text_area.x = 10
weather_text_area.y = 10
# Show the weather
display.root_group = weather_text_area
#--------------------------------------------------------------------------------
#Get quote from quotableAPI
gc.collect()
quote_response = requests.get("http://api.quotable.io/quotes/random?maxLength=80")
quote_data = quote_response.json()
quote_response.close()
quote_text = quote_data[0]['content'] + '\n-' + quote_data[0]['author']
display.root_group.append(label.Label(font, text = quote_text, color = color, x = 0, y = 160))
#--------------------------------------------------------------------------------
#Reset every 15 minutes to update the weather and quote, update the time every minute
start_time = time.monotonic()
real_time = time.localtime()
time_label = label.Label(font, text = f"{real_time[3] + 5}:{add_lead_zero(real_time[4])}", 
                         color = color, x = 190, y = 80, scale = 6)
display.root_group.append(time_label)
while True:
    if time.monotonic() - start_time >= 900:
        microcontroller.reset()
    real_time = time.localtime()
    time_label.text = f"{real_time[3] + 5}:{add_lead_zero(real_time[4])}"
    time.sleep(60)