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
5. Replace Accuweather keys in getData.py (forecast) and showData.py (current conditions)
    url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/REPLACE_WITH_LOCATION?apikey=REPLACE_WITH_32BYTE_KEY&details=true&metric=true"
    url = "http://dataservice.accuweather.com/currentconditions/v1/REPLACE_WITH_LOCATION?apikey=REPLACE_WITH_32BYTE_KEY&details=true"
    
6. Find location KEY of Your city and replace it in showData.py
    url = "http://dataservice.accuweather.com/currentconditions/v1/REPLACE_WITH_LOCATION?apikey=REPLACE_WITH_32BYTE_KEY&details=true"
7. Replace AQI token in showData.py
    url = "http://api.waqi.info/feed/@3392/?token=REPLACE_WITH_TOKEN"
8. Add scripts to cron to get updates automaticaly,
    # m h  dom mon dow   command
    # get sensor data every 30 minutes form 6:00 AM to 23:30 PM and store the output
    0,30 6-23 * * * python /home/pi/Pimoroni/unicornhathd/accuweather/showData.py >> /home/pi/Pimoroni/unicornhathd/accuweather/Data.dat
    # clear hat every midnight
    10 0 * * * python /home/pi/Pimoroni/unicornhathd/accuweather/clear.py
    # get forecast data every 3 hours at minute 59
    59 5,8,11,14,17,19,20,21,22 * * * python /home/pi/Pimoroni/unicornhathd/accuweather/getData.py >> /home/pi/Pimoroni/unicornhathd/accuweather/Data.dat

9. Remember to run getData.py first as it prepares data for forecast (12h in advance)
10. Run showData.py manualy or from cron
