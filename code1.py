#Code by Aman Gusain

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
ledpin = 12				# PWM pin 12 connected to LED
trigger_pin = 8
echo_pin = 7


distance = 0 #Distance of ultrasonic
startTime = 0
endTime = 0
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
pww = GPIO.PWM(ledpin, 1000)        #frequency of PWM is set to 1000
pww.start(0)                        #initial value of PWM is 0

try:
    while True:
        #sending a pulse
        GPIO.output(trigger_pin, 0)
        time.sleep(0.000002)    #2 microsecond delay
        GPIO.output(trigger_pin, 1)
        time.sleep(0.00001)     #1 microsecond delay
        GPIO.output(trigger_pin, 0)

        # measuring time duration
        while GPIO.input(echo_pin) == 0:
            pass
        startTime = time.time()
        while not GPIO.input(echo_pin) == 0:
            endTime = time.time()
        
        timeDuration = endTime - startTime
        distance=(timeDuration*17150)       #calculating distance
        print("Distance: " + str(distance))

        #pwm LED power manage. Changes acc to distance
        if distance <= 20 and distance > 0:
            pww.ChangeDutyCycle((20 - distance) * 5)   
        else:
            pww.ChangeDutyCycle(0)
        #pwm end
        time.sleep(0.4)
except KeyboardInterrupt:
    print("Keyboard Interrrupt, Programme stopped!")        #keyboard interrupt to stop the program
    pww.stop()
    GPIO.cleanup()


