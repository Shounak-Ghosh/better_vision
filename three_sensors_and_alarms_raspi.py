#Libraries
import RPi.GPIO as GPIO
import time


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER1 = 11
GPIO_ECHO1 = 10
GPIO_RAWECHO1 = 9

GPIO_TRIGGER2 = 25
GPIO_ECHO2 = 8
GPIO_RAWECHO2 = 7

GPIO_TRIGGER3 = 16
GPIO_ECHO3 = 20
GPIO_RAWECHO3 = 21


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_RAWECHO1, GPIO.IN)

GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_RAWECHO2, GPIO.IN)

GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
GPIO.setup(GPIO_RAWECHO3, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER1, True)
    GPIO.output(GPIO_TRIGGER2, True)
    GPIO.output(GPIO_TRIGGER3, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER1, False)
    GPIO.output(GPIO_TRIGGER2, False)
    GPIO.output(GPIO_TRIGGER3, False)
    StartTime1 = time.time()
    StopTime1 = time.time()
    StartTime2 = time.time()
    StopTime2 = time.time()
    StartTime3 = time.time()
    StopTime3 = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO1) == 0:
        StartTime1 = time.time()
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime2 = time.time()
    while GPIO.input(GPIO_ECHO3) == 0:
        StartTime3 = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO1) == 1:
        StopTime1 = time.time()
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime2 = time.time()
    while GPIO.input(GPIO_ECHO3) == 1:
        StopTime3 = time.time()

    # time difference between start and arrival
    TimeElapsed1 = StopTime1 - StartTime1
    TimeElapsed2 = StopTime2 - StartTime2
    TimeElapsed3 = StopTime3 - StartTime3
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance1 = (TimeElapsed1 * 34300) / 2
    distance2 = (TimeElapsed2 * 34300) / 2
    distance3 = (TimeElapsed3 * 34300) / 2
    
    pause1 = StopTime1 + 0.001
    pause2 = StopTime2 + 0.001
    pause3 = StopTime3 + 0.001
    
    while pause1 > time.time():
        pause1 = pause1
    while GPIO.input(GPIO_RAWECHO1) == 0:
        StartTime1 += 0
    while GPIO.input(GPIO_RAWECHO1) == 1:
        StopTime1 = time.time()

    while pause2 > time.time():
        pause2 = pause2
    while GPIO.input(GPIO_RAWECHO2) == 0:
        StartTime2 += 0
    while GPIO.input(GPIO_RAWECHO2) == 1:
        StopTime2 = time.time()
    
    while pause3 > time.time():
        pause3 = pause3
    while GPIO.input(GPIO_RAWECHO3) == 0:
        StartTime2 += 0
    while GPIO.input(GPIO_RAWECHO3) == 1:
        StopTime3 = time.time()
    
    TimeElapsed1 = StopTime1 - StartTime1
    TimeElapsed2 = StopTime2 - StartTime2
    TimeElapsed3 = StopTime3 - StartTime3   

    raw_distance1 = (TimeElapsed1 * 34300) / 2
    raw_distance2 = (TimeElapsed1 * 34300) / 2
    raw_distance3 = (TimeElapsed1 * 34300) / 2    

    val = [distance1, distance2, distance3, raw_distance1, raw_distance2, raw_distance3]
    
    return val
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print("Left Distance = %.1f cm" % int(float(dist[0])) + " Front Distance = %.1f cm" % int(float(dist[1])) + " Right Distance = %.1f cm" % int(float(dist[2])))
            print("Further Left Distance = %.1f cm" % int(float(dist[3])) + " Further Front Distance = %.1f cm" % int(float(dist[4])) + " Further Right Distance = %.1f cm" % int(float(dist[5])))
            time.sleep(1)

            
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()