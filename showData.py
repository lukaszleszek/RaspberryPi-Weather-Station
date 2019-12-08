#!/usr/bin/python
import time,sys,json,urllib2,math
import unicornhathd as sense
from datetime import datetime

# colors definition
WHITE_DAY = [27,27,27]
WHITE_NIGHT = [7,7,7]
WHITE_FULL = [255,255,255]
TEMP_DAY = [167,167,50]
TEMP_NIGHT = [127,127,0] 
HUM_NIGHT = [7,35,7]
HUMIDITY_BG_DAY = [6,72,6]
HUMIDITY_BG_NIGHT = [4,12,4]
HUM_DAY = [15,220,10]
RAIN_DAY = [87,87,87]
RAIN_NIGHT = [47,47,47]
RAIN_BG_NIGHT = [27,27,27]
RAIN_BG_DAY = [37,37,37]
LUNA_NIGHT = [7,7,7]
LUNA_DAY = [57,57,57]
BLACK = [0,0,0]
black = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

updateHour = startInd = 0
currentHour = int(time.strftime("%H",time.localtime()))
lineCounter = 1
tempMax = float(0)
tempMin = float(0)
tempData = float(0)
# arrays for forecasts
humForecast = []
precipForecast = []
tempForecast = []
todo=1

def update_color(color,r,g,b,isWhite):
	if  isWhite:
		return color
	color[0]=color[0]+r
	if color[0]>255:
		color[0]=255
        if color[0]<0:
                color[0]=0

	color[1]=color[1]+g
        if color[1]>255:
                color[1]=255
        if color[1]<0:
                color[1]=0

	color[2]=color[2]+b
        if color[2]>255:
                color[2]=255
        if color[2]<0:
                color[2]=0

	return color
def show_one_pixel(value,r,g,b,isWhite,isDarker):
	if isWhite:
		WARM = COLD = ZERO = [r,g,b]		
	else:
		WARM = [255,255,0]
		COLD = [50,248,245]
		ZERO = [255,0,0]
	pixel_counter = 0
	# setting proper color based on  value
	if (value <= 0):
			color = COLD
			value = value * -1
	else:
			color = WARM
	# decreasing value by 1 since display index starts from 0 (not from 1)
	value = value - 1
        # 1
        # 0,0 to 0,15
        for i in range(0,15):
                if pixel_counter==value:
			if ((isDarker) & (i<15)):
				#sense.set_pixel(1,i,color[0],color[1],color[2])
				#sense.set_pixel(0,i,color[0],color[1]+60,color[2])
				sense.set_pixel(1,i,color[0]+35,color[1]+35,color[2]+35)
				sense.set_pixel(2,i,color[0]+5,color[1]+5,color[2]+5)
				sense.set_pixel(3,i,color[0],color[1],color[2])
			else:
                        	sense.set_pixel(0,i,color[0],color[1],color[2])
			sense.show()
                        return
                else:
                        pixel_counter +=1
			color=update_color(color,0,-12,0,isWhite)
        # 2
        # 0,15 to 15,15
        for i in range(0,15):
                if pixel_counter==value:
			if (isDarker):
                                #sense.set_pixel(i,14,color[0],color[1],color[2])
				#sense.set_pixel(i,15,color[0],color[1]+150,color[2])
				sense.set_pixel(i,14,color[0]+35,color[1]+35,color[2]+35)
                                sense.set_pixel(i,13,color[0]+5,color[1]+5,color[2]+5)
                                sense.set_pixel(i,12,color[0],color[1],color[2])
			else:
                        	sense.set_pixel(i,15,color[0],color[1],color[2])
                        sense.show()
			return
                else:
                        pixel_counter +=1
			color=update_color(color,0,-12,0,isWhite)
        # 3
        # 15,15 to 15,0
        for i in range(0,15):
                if pixel_counter==value:
			if (isDarker):
                                #sense.set_pixel(14,15-i,color[0],color[1],color[2])
				 sense.set_pixel(15,15-i,color[0]+2,color[1],color[2])
			else:
                        	sense.set_pixel(15,15-i,color[0],color[1],color[2])
                        sense.show()
			return
                else:
                        pixel_counter +=1
			color=update_color(color,-1,0,45,isWhite)
        # 4
        # 15,0 to 0,0
        for i in range(0,15):
                if pixel_counter==value:
			if (isDarker):
                                #sense.set_pixel(15-i,1,color[0],color[1],color[2])
				 sense.set_pixel(15-i,0,color[0]-60,color[1]-60,color[2]-60)
			else:
                        	sense.set_pixel(15-i,0,color[0],color[1],color[2])
                        sense.show()
			return
                else:
                        pixel_counter +=1
			color=update_color(color,25,25,0,isWhite)
def show_temperature_circle(temp_c,timer,isWhite):
	if isWhite:
		# define colors for Air Quality
		aqiDay1 = [27,27,27]
		aqiDay2 = [50,50,0]
		aqiDay3 = [60,30,0]
		aqiDay4 = [80,20,0]
		aqiDay5 = [177,27,27]
		aqiDay6 = [255,0,0]
		aqiCOLORday = aqiDay1

		aqiNight1 = [7,7,7]
		aqiNight2 = [30,30,0]
		aqiNight3 = [40,10,0]
		aqiNight4 = [70,5,0]
		aqiNight5 = [155,7,7]
		aqiNight6 = [255,0,0]
		aqiCOLORnight = aqiNight1

		# check polution status
		try:
			url = "http://api.waqi.info/feed/@3392/?token=REPLACE_WITH_TOKEN"
			result = urllib2.urlopen(url).read()
			json_data = json.loads(result)
			aqi = json_data['data']['aqi']
			#aqi = 25
			#print "RESULT : %s" % (result)
			print "AQI index : %s " % (aqi)
			if aqi<51: # AQI = GOOD, no changes, as color stays the same
				aqiCOLORday =  aqiDay1
				aqiCOLORnight = aqiNight1
			if ((aqi>50) & (aqi<101)): #AQI = MODERATE
                                aqiCOLORday =  aqiDay2
                                aqiCOLORnight = aqiNight2
			if ((aqi>100) & (aqi<151)): #AQI = UNHEALTHY for  SENSITIVE GROUPS
                                aqiCOLORday =  aqiDay3
                                aqiCOLORnight = aqiNight3
			if ((aqi>150) & (aqi<201)): #AQI = UNHEALTHY
                                aqiCOLORday =  aqiDay4
                                aqiCOLORnight = aqiNight4
			if ((aqi>200) & (aqi<301)): #AQI = VERY UNHEALTHY
                                aqiCOLORday =  aqiDay5
                                aqiCOLORnight = aqiNight5
			if aqi>300: #AQI = HAZARDOUS
                                aqiCOLORday =  aqiDay6
                                aqiCOLORnight = aqiNight6
		except:
			print "Error getting AQI index"
			aqi = 0
		if IsDayTime:
			WARM = COLD = ZERO = aqiCOLORday
		else:
			WARM = COLD = ZERO = aqiCOLORnight
	else:
		WARM = [255,255,0]
		COLD = [50,248,245]
		ZERO = [255,0,0]

	pixel_counter = 0
	UPDATE_SCREEN = False
	temp_c = float(temp_c)
	#print "Current temperature = %s " % (temp_c)
	# setting proper color based on temp_c value
	if (temp_c < -0.5):
			UPDATE_SCREEN = True
			pixel_counter = round(temp_c * -1,0)
			color = COLD
			#print "It will be COLD"
	if ((temp_c <= 0.5) & (temp_c >= -0.5)):
			UPDATE_SCREEN = True
			pixel_counter = 1
			color  = ZERO
			#print "It will be around ZERO"
	if (temp_c > 0.5):
			UPDATE_SCREEN = True
			pixel_counter = round(temp_c)
			color = WARM
			#print "It will be WARM"
	
	
	# below is never true
	#if pixel_counter<=0:
	#	sense.set_pixel(0,0,color)
	#	return
	
	# 1
	# 0,0 to 0,15
	for i in range(0,15):
		if pixel_counter>0:
			sense.set_pixel(0,i,color[0],color[1],color[2])
			pixel_counter -= 1
		else:
			return
		color=update_color(color,0,-12,0,isWhite)
		time.sleep(timer)
		sense.show()
	# 2
	# 0,15 to 15,15
	for i in range(0,15):
		if pixel_counter>0:
			sense.set_pixel(i,15,color[0],color[1],color[2])
			pixel_counter -= 1
		else:
			return
		color=update_color(color,0,-12,0,isWhite)
		time.sleep(timer)
		sense.show()
	# 3
	# 15,15 to 15,0
	for i in range(0,15):
		if pixel_counter>0:
			sense.set_pixel(15,15-i,color[0],color[1],color[2])
			pixel_counter -= 1
		else:
			return
		color=update_color(color,-1,0,45,isWhite)
		time.sleep(timer)
		sense.show()
	# 4
	# 15,0 to 0,0
	for i in range(0,15):
		if pixel_counter>0:
			sense.set_pixel(15-i,0,color[0],color[1],color[2])
			pixel_counter -= 1
		else:
			return
		color=update_color(color,25,25,0,isWhite)
		time.sleep(timer)
		sense.show()
def show_line(data,index,timer,color,colorZero):
	#Sprint data
	# show 0 with different color
	isZero = False
	isMax = False
	value = 0
	maxValue = int(round(max(data)))
	minValue = int(round(min(data)))
	margin  = margin2draw = (maxValue - minValue)
	# setting window to 10 pixel if it is too large
	if margin>=9:
		margin = (margin-9)/2
		margin2draw = 9
	else:
		margin=0
	#print "minValue : %s maxValue : %s margin : %s margin2draw : %s" % (minValue,maxValue,margin,margin2draw)
	leftMargin = minValue + margin
	rightMargin = leftMargin + 9
	#print "leftMargin : %s rightMargin : %s" % (leftMargin,rightMargin)
	for j in range(0,12-index):
		data[j]=round(data[j])
		if (data[j]==0):
			isZero = True
		else:
			isZero = False
        	# first bar no 2 (2-13)
                # range from 13-4 (10 values==100%, 1pt == 10%)
		# calculate value inside window
		if ((data[j]>=leftMargin) & (data[j]<=rightMargin)):
			isMax = False
			if data[j]>0:
				value =  data[j] - leftMargin
			else:
				value =  (leftMargin*(-1))- (data[j]*(-1))
		# calculate value outside window
		if (data[j]<leftMargin):
			isMax = True
                	value = 0 
		if (data[j]>rightMargin):
			isMax = True
			value = 9
		value = round(value)
		#value= 10 - value
		# outside window
		#print "Value : %s" % value
		if isMax:
			if isZero:
				sense.set_pixel(4+margin2draw-value,2+j,colorZero[0],colorZero[1],colorZero[2])
			else:
				sense.set_pixel(4+margin2draw-value,2+j,color[0]+40,color[1]-50,color[2])
		# inside window
		else:
			if isZero:
				sense.set_pixel(4+margin2draw-value,2+j,colorZero[0],colorZero[1],colorZero[2])
			else:
				sense.set_pixel(4+margin2draw-value,2+j,color[0],color[1],color[2])
		#print "Temp : %s at index : %s with value : %s" % (data[j],j,value)
                time.sleep(timer)
                sense.show()


def show_graph(data,index,timer,color,colorMax):
	for j in range(0,12-index):
		# first bar no 2 (2-13)
		# range from 13-4 (10 values==100%, 1pt == 10%)
		for i in range(0,10):
			if (i==(data[j]-1)):
				# 0 = null, 1 = 13,2 = 12, 10 = 4
				# max dot
				sense.set_pixel(13-i,2+j,colorMax[0],colorMax[1],colorMax[2])
                        	time.sleep(timer)
                        	sense.show()
			else:
				# light dot
				if ((data[j]>0) & (i<data[j]-1)):
					sense.set_pixel(13-i,2+j,color[0],color[1],color[2])
					time.sleep(timer)
					sense.show()


#count days to full moon
def showLunarPhase(color):
        temp = 0
	phase = 0
	beforeFullMoon = True
        x = datetime.now()
        year = x.year
        month = x.month
        day = x.day
        #print "Year : %s Month : %s Day : %s" % (year,month,day)
        # algorithm by John Conway
        r = year % 100
        r %= 19
        if (r>9):
                r -= 19
        r = ((r * 11) % 30) + month + day
        if (month<3):
                r += 2
        if (year<2000):
                temp = 4
        else:
                temp = 8.3
        r -= temp
        r = round(r+0.5)%30
        if (r<0):
                phase = r +30
        else:
                phase = r

	#print "Lunar phase : %d" % phase
	# drawing lunar phase graph
	if phase>15:
		beforeFullMoon = False
		phase = 30 - phase
	
	phase = int(phase)
	#pre full moon alert for Magda, only 2-4 days before full moon
	if ( (phase>10) & (phase<14) & beforeFullMoon):
		# fill scale with red first
		for i in range(1,15):
			sense.set_pixel(i,0,220,60,30)
		sense.show()
		#sense.set_pixel(15,0,220,60,30)  # bottom left
		#sense.set_pixel(14,0,220,60,30)  # up
		#sense.set_pixel(15,1,220,60,30)  # right
		
	# then fill actual moon phase indicator 	
	for i in range (1,phase+1):
		#first part from 0 (new moon) to 15 (full moon)
		sense.set_pixel(i,0,color[0],color[1],color[2]) # top right
		color = update_color(color,8,8,8,False)
		time.sleep(0.1)
		sense.show()




sense.clear()
sense.rotation(270)
# set accuweathercurrent conditions  request url
url = "http://dataservice.accuweather.com/currentconditions/v1/REPLACE_WITH_LOCATION?apikey=REPLACE_WITH_32BYTE_KEY&details=true"
result = urllib2.urlopen(url).read()
json_data = json.loads(result)
# current temp
temp = json_data[0]['Temperature']['Metric']['Value']
IsDayTime = json_data[0]['IsDayTime']
#IsDayTime = True
#temp=-20

# get max temperature from forecast data
with open("/home/pi/Pimoroni/unicornhathd/accuweather/forecast.txt","r") as file:
	forecastData = file.readlines()
for line in forecastData:
	words = line.split("|")
	if line[0]==";": # comment line
		todo
		#print "Line : %s" % (words)
	else:
		if (lineCounter==1): #hour
			updateHour = int(words[0])
			# startInd points to current forecast hour
			startInd = currentHour - updateHour
			if startInd < 0:
				startInd=0
			#startInd=0
			#print "startInd : %s" % startInd
		if (lineCounter==2): #temperature
                        # looking for temperature forecast
                        #print "Checking temperature"
                        j = 0
                        for i in range (startInd,12):
				tempForecast.append(float(words[i]))
                                #print "Value : %s" % tempForecast[j]
                                j+=1

			# looking up minTemp and maxTemp
			for i in range (startInd,12):
				tempData = float(words[i])
				if (i == startInd):
                			tempMin = tempMax = float(words[i])
        			if (tempData < tempMin):
                			tempMin = float(words[i])
        			if (tempData > tempMax):
                			tempMax = float(words[i])
			#revert values if both are negative, since temp circle represent negatie in diff color
			if ((tempMin < 0) & (tempMax < 0)):
        			        tempData = tempMax
				        tempMax = tempMin
        				tempMin = tempData
			localTime = time.asctime( time.localtime(time.time()) )
			print "%s - Forecast for hour : %s tempMin : %s tempMax : %s temp : %s" % (localTime,currentHour,tempMin,tempMax,temp)
		if (lineCounter==3): #max temp (obsolete)
			todo
			#maxTemp = int(words[0])
			#minTemp = int(words[1])
			#print "maxTemp : %s minTemp : %s" % (maxTemp,minTemp)
		if (lineCounter==4): #humidity
			# looking for humidity forecast
			#print "Checking humidity"
			j = 0
			for i in range (startInd,12):
				humForecast.append(int(math.ceil((int(words[i])/10))))
				#print "Value : %s" % humForecast[j]
				j+=1
		if (lineCounter==5): #precipitation
			#print "Checking precip"
			j = 0
                        for i in range (startInd,12):
				# divide by 10 to get value in range (0,10)
				precipForecast.append(int(math.ceil((int(words[i])/10))))
                                #print "Value : %s" % humForecast[j]
                                j+=1
		if (lineCounter==6): #wind
			todo
		lineCounter +=1
file.close()


# setting brightness according to day or night
if IsDayTime:
	sense.brightness(1)
	print "Day"
	WHITE = RAIN_BG_DAY
	RAIN = RAIN_DAY
	HUMIDITY = HUM_DAY
	HUMIDITY_BG = HUMIDITY_BG_DAY
	TEMP = TEMP_DAY
	LUNA = LUNA_DAY

else:
	sense.brightness(0.4)
	print "Night"
	WHITE = RAIN_BG_NIGHT
	RAIN = RAIN_NIGHT
	HUMIDITY = HUM_NIGHT
	HUMIDITY_BG = HUMIDITY_BG_NIGHT
	TEMP = TEMP_NIGHT
	LUNA = LUNA_NIGHT
# correcting minTemp if lover than actual (only if both are positive)
if ((temp < tempMin) & (tempMin > 0) & (tempMax > 0)):
	tempMin = temp
# correcting minTemp if higher than actual (only if both are negative)
if ((temp > tempMin) & (tempMin < 0) & (tempMax < 0)):
	tempMin = temp
# correcting minTemp if it points the corner, not to overwrite current temp line
if (int(round(tempMin))==16):
	tempMin = 15
# show max temp circel
show_temperature_circle(64,0.01,True)

# show current temp cicrle
show_temperature_circle(round(temp),0.03,False)
# show min & max values for next 12h
show_one_pixel(int(round(tempMax)),255,255,255,False,False)
show_one_pixel(int(round(tempMin)),20,20,20,True,True)

show_graph(humForecast,12-len(humForecast),0.01,HUMIDITY_BG,HUMIDITY)
show_graph(precipForecast,12-len(precipForecast),0.01,WHITE,RAIN)
time.sleep(2)
show_graph(black,0,0,BLACK,BLACK)
show_graph(precipForecast,12-len(precipForecast),0.01,WHITE,RAIN)
show_line(tempForecast,12-len(tempForecast),0.1,TEMP,WHITE_FULL)

#show lunar phase
showLunarPhase(LUNA)

#sense.clear()
#sense.set_pixel(0,0,255,255,255)
#sense.set_pixel(0,15,255,0,0)
#sense.set_pixel(15,0,0,255,0)
#sense.set_pixel(15,15,0,0,255)
#sense.show()
