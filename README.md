# Morning Assistant
## Proposal
A small project to display the weather, time, and a nice quote on a small screen using a Raspberry Pi Pico W, a small something to put by my bed 
to look at when I wake up. 

## Components
 - [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)
 - [Adafruit 400x240 Sharp Memory Display](https://www.adafruit.com/product/4694)

## How it Works
This project makes heavy use of the Wifi part of the Raspberry Pi Pico W. All components of the project, the weather data, the quote, and the current time
are all fetched from the internet. OpenWeatherAPI is used to source the weather data, quoteable API is used to get quotes, and WorldTime API is used to 
get the time. The data from these three APIs is then parsed and formatted to be displayed on the screen.


https://github.com/IanK02/Morning-Assistant/assets/102310492/59d708ba-08dd-45bf-a695-9c3633cefe27


## Next Steps
Likely none. Since it's only sitting on my nightstand I don't mind having it stuck to a breadboard. Furthermore I'm near the limits of the capability of 
the RAM of the Raspberry Pi Pico W so it is unlikely it would be incapable of adding much else to the display.
