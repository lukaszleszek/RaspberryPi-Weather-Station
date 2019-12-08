# RaspberryPi-Weather-Station
Weather station based on Raspberry Pi and Unicorn HAT HD
https://www.youtube.com/watch?v=u-e2rMbgelA

Raspberry Pi3 with unicorn HAT HD (16x16 RGB LED panel - https://shop.pimoroni.com/products/un...) inside Short Crust Plus case (http://shortcrust.net/short-crust-plus/).

Weather data (forecast and current conditions) is fetched from AccuWeather. Air Quality data is fetched from http://aqicn.org/.

Outside square (64 values) displays current temperature, changing color gradient gradually. Red/Blue dot on outside square indicates maximum temperature value for next 12 hours. 3-dot long blue line indicates minimum temperature value for next 12 hours. 

Outside margin (light blue) indicates air quality index (blue=good,yellow=moderate,orange=unhealthy,red=very unhealthy). 

Inside square (12x12) displays forecast data for next 12 hours (green=humidity,blue=probability of rain/snow)

SETUP
1. Install Pimoroni Unicorn HAT HD libraries - https://github.com/pimoroni/unicorn-hat-hd
2. Create Accuweather account and obtain API KEY. Free key is available but limits number of requests to 50 per day
3. Get free Air Quality Index token - https://aqicn.org/api/
4. Place both .py files in /home/pi/Pimoroni/unicornhathd/accuweather/ or modify the script to store temporary files in different location
5. Replace Accuweather keys in getData.py and showData.py
6. Find location KEY of Your city
7. Replace AQI token in showData.py
8. Add scripts to cron to get updates automaticaly, check example_crontab.txt for working example
9. Remember to run getData.py first as it prepares data for forecast (12h in advance)
10. Run showData.py manualy or from cron
