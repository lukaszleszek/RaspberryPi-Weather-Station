import json,time,urllib2
from datetime import datetime
url = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/REPLACE_WITH_LOCATION?apikey=REPLACE_WITH_32BYTE_KEY&details=true&metric=true"
result = urllib2.urlopen(url).read()
json_data = json.loads(result)
#with open("data.json") as json_file:
#	json_data = json.load(json_file)
# Open file to store forecast data
lineHour = ""
lineTemp = ""
lineHum = ""
linePrecip = ""
lineWind = ""
tempMax = 99
tempMin = 99
tempData = 99
file = open("/home/pi/Pimoroni/unicornhathd/accuweather/forecast.txt","w")
for i in range(0,12):
	lineTime = datetime.fromtimestamp(int(json_data[i]['EpochDateTime'])).strftime('%H')
	lineHour += lineTime+"|"
	lineTemp += str(json_data[i]['Temperature']['Value'])+"|"
        lineHum += str(json_data[i]['RelativeHumidity'])+"|"
        linePrecip += str(json_data[i]['PrecipitationProbability'])+"|" 
	lineWind += str(json_data[i]['Wind']["Speed"]["Value"])+"|"
	# note highest temperature
	tempCurrent = json_data[i]['Temperature']['Value']
	if (i == 0):
		tempMin = tempMax = tempCurrent
	if (tempCurrent < tempMin):
		tempMin = tempCurrent
	if (tempCurrent > tempMax):
		tempMax = tempCurrent 
if ((tempMin < 0) & (tempMax < 0)):
	tempData = tempMax
	tempMax = tempMin
	tempMin = tempData
# write to file
file.write(";Hour of forecast\n")
file.write(lineHour+"\n")
file.write(";Temperature forecast\n")
file.write(lineTemp+"\n")
file.write(";Maximum and minimum temperature for next 12h\n")
file.write(str(int(tempMax))+"|"+str(int(tempMin))+"\n")
file.write(";Humidity forecast\n")
file.write(lineHum+"\n")
file.write(";Precipitation forecast\n")
file.write(linePrecip+"\n")
file.write(";Wind forecast\n")
file.write(lineWind+"\n")

file.close()

#print "lineHour = %s" % (lineHour)
#print "lineTemp = %s" % (lineTemp)
#print "lineHum = %s" % (lineHum)
#print "linePrecip = %s" % (linePrecip)
#print "lineWind = %s" % (lineWind)
print "Forecast (12h) at hour : %s" % time.strftime("%H",time.localtime())
print "tempMin = %s tempMax = %s" % (tempMin,tempMax)
