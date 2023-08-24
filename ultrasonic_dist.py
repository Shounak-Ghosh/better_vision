#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER_R = 18
GPIO_ECHO_R = 24

GPIO_TRIGGER_L = 20
GPIO_ECHO_L = 21

GPIO_TRIGGER_F = 27
GPIO_ECHO_F = 22

#GPIO direction
GPIO.setup(GPIO_TRIGGER_R, GPIO.OUT)
GPIO.setup(GPIO_ECHO_R, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_L, GPIO.OUT)
GPIO.setup(GPIO_ECHO_L, GPIO.IN)

GPIO.setup(GPIO_TRIGGER_F, GPIO.OUT)
GPIO.setup(GPIO_ECHO_F, GPIO.IN)

#measuring distance from right sensor
def distance_R():
        #Set trigger to high
        GPIO.output(GPIO_TRIGGER_R, True)
        #Wait 0.00001 seconds
        time.sleep(0.00001)
        #Set trigger to low
        GPIO.output(GPIO_TRIGGER_R, False)
        
        StartTime_R = time.time()
        StopTime_R = time.time()



        while GPIO.input(GPIO_ECHO_R) == 0:
                #Record Start Time
                StartTime_R = time.time()
        while GPIO.input(GPIO_ECHO_R) == 1:
                #Record Stop Time
                StopTime_R = time.time()
        #Calculate time 
        TimeElapsed_R = StopTime_R - StartTime_R

        #Calculate distance
        distance_R = (TimeElapsed_R * 17150)

        return distance_R

#measuring distance from left sensor
def distance_L():
        GPIO.output(GPIO_TRIGGER_L, True)

        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_L, False)

        StartTime_L = time.time()
        StopTime_L = time.time()



        while GPIO.input(GPIO_ECHO_L) == 0:
                StartTime_L = time.time()
        while GPIO.input(GPIO_ECHO_L) == 1:
                StopTime_L = time.time()
        TimeElapsed_L = StopTime_L - StartTime_L


        distance_L = (TimeElapsed_L * 17150)

        return distance_L
#measuring distance from front sensor
def distance_F():
        GPIO.output(GPIO_TRIGGER_F, True)

        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER_F, False)

        StartTime_F = time.time()
        StopTime_F = time.time()



        while GPIO.input(GPIO_ECHO_F) == 0:
                StartTime_F = time.time()
        while GPIO.input(GPIO_ECHO_F) == 1:
                StopTime_F = time.time()
        TimeElapsed_F = StopTime_F - StartTime_F


        distance_F = (TimeElapsed_F * 17150)

        return distance_F
#function to determine volume of the audio cue
def audio(distance_L, distance_F, distance_R):
    #Libraries
    from pydub import AudioSegment
    from pydub.playback import play
    
    #collecting audio files
    front = AudioSegment.from_file(file = 'front.wav', format = 'wav')
    left = AudioSegment.from_file(file = 'left.wav', format = 'wav')
    right = AudioSegment.from_file(file = 'right.wav', format = 'wav')

    front1 = front * 0
    left1 = left * 0
    right1 = right * 0
    
    #formula to determine volume
    if distance_R <= 80:
        right1 = right + 2 - (distance_R ** 3) * 0.0000234
    if distance_L <= 80:
        left1 = left + 5 - (distance_L ** 3) * 0.0000234
    if distance_F <= 80:
        front1 = front - (distance_F ** 3) * 0.0000234
        
    colat = left1 + front1 + right1
        
    play(colat)
    
if __name__ == '__main__':
        try:
                while True:
                        dist_R = distance_R()
                        dist_L = distance_L()
                        dist_F = distance_F()
                        print('Right Distance = %.1f cm' % dist_R)
                        print('Left Distance = %.1f cm' % dist_L)
                        print('Front Distance = %.1f cm' % dist_F)
                        audio(dist_L, dist_F, dist_R)
                        time.sleep(.25)
        #reset by pressing ctrl + c
        except KeyboardInterrupt:
                print('Measurement stopped by user')
                GPIO.cleanup()





