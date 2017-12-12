# Import all the libraries we need to run
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib2
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

DEBUG = 1
# Setup the pins we are connect to
# RCpin = 24
DHTpin = 23

#Setup our API and delay
myAPI = "XVFX5JKP2L99P7C5"
myDelay = 15 #how many seconds between posting data

GPIO.setmode(GPIO.BCM)
#GPIO.setup(RCpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    print "In read_temp"
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        WT = float(temp_string) / 1000.0
        WTF = WT * 9.0 / 5.0 + 32.0
    #return WT,WTF
    return (str(WT) ,str(WTF))

def getSensorData():
    print "In getSensorData"
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32
   
    # return dict
    return (str(RHW), str(TW), str(TWF))

# main() function
def main():
    
    print 'starting...'

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        try:
            print "Reading Sensor Data"
            RHW, TW, TWF = getSensorData()
	    WT, WTF = read_temp()
	    #print(read_temp())
            #LT = RCtime(RCpin)
            f = urllib2.urlopen(baseURL + "&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s" % (TW, TWF, RHW, WT, WTF)) #WT - water temperature
            print f.read()
            print "TW:"+TW + " " + "TWF:"+TWF+ " " + "RHW:" + RHW + " "  + "WT:" + WT + " " + "WTF:" + WTF + " " 
            f.close()

        except:
            print 'exiting.'
            break

        sleep(int(myDelay))

# call main

if __name__ == '__main__':
    main()
