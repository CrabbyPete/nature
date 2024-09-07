#!/usr/bin/python
# Naturebytes Wildlife Cam Kit | V1.01
# Based on the excellent official Raspberry Pi tutorials and a little extra from Naturebytes
import csv
import time
import pathlib
import logging
import RPi.GPIO as GPIO

from subprocess import call
from datetime import datetime


# Logging all of the camera's activity to the "naturebytes_camera_log" file. If you want to watch what your camera
# is doing step by step you can open a Terminal window and type "cd /Naturebytes/Scripts" and then type
# "tail -f naturebytes_camera_log" - leave this Terminal window open and you can view the logs live

logging.basicConfig(format='%(asctime)s %(message)s',level=logging.DEBUG)
logging.info('Naturebytes Wildlife Cam Kit started up successfully')

# Assigning a variable to the pins that we have connected the PIR to
SENSOR_PIN = 13

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def what_os():
    path = pathlib.Path("/etc/os-release")
    with open(path) as stream:
        reader = csv.reader(stream, delimiter="=")
        os_release = dict(reader)
    return os_release


def main():

    prevState = False
    currState = False

    # Starting a loop
    if '12' in what_os()['VERSION_ID']
        cam_command = 'rpi-still'
    else:
        cam_command = 'libcamera-still'

    while True:
        time.sleep(0.1)
        prevState = currState

        # Map the state of the camera to our input pins (jumper cables connected to your PIR)

        currState = GPIO.input(SENSOR_PIN)
        if not currState == prevState:
            # About to check if our new state is HIGH or LOW

            newState = "HIGH" if currState else "LOW"
            #  newBattState = "HIGH" if currBattState else "LOW"
            print (f"GPIO {SENSOR_PIN} pin:{newState}")
            # print "Battery level detected via pin %s is %s" % (lowbattPin, newBattState)

            if currState:  # Our state has changed, so that must be a trigger from the PIR

                i = datetime.now() # Get the time now
                get_date = i.strftime('%Y-%m-%d') # Get and format the date
                get_time = i.strftime('%H-%M-%S') # Get and format the time
                # batt_state = newBattState
                # Checking the current status of the battery

                # Recording that a PIR trigger was detected and logging the battery level at this time
                logging.info('PIR trigger detected')
                # logging.info('Battery level is %(get_batt_level)s', { 'get_batt_level': batt_state })

                # Assigning a variable so we can create a photo JPG file that contains the date and time as its name
                photo = get_date + '_' +  get_time + '.jpg'

                # Using the raspistill library to take a photo and show that a photo has been taken in a small preview box on the desktop
                cmd = f'{cam_command} --output {photo}'
                print (f"cmd:{cmd}")

                # Log that we have just taking a photo"
                logging.info('About to take a photo')
                call ([cmd], shell=True)

                # Log that a photo was taken successfully and state the file name so we know which one"
                logging.info('Photo taken successfully %(show_photo_name)s', { 'show_photo_name': photo })
                photo_location =  './' + photo

                # Log that we are about to attempt to write the overlay text"
                logging.info('About to write the overlay text')

                overlay = "/usr/bin/convert "+ photo_location + " "

                # Use ImageMagick to write text and meta data onto the photo.
                # overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " + get_date + '" '" + get_time '" -gravity southeast -annotate +6+6 'Camera 1 " "'" + photo_location
                overlay += " -gravity north -background black -extent +0+40 +repage -box black -fill white -pointsize 24 -gravity southwest -annotate +6+6 'Naturebytes Wildlife Cam Kit | Date & Time: " + get_date + " " + get_time + "' -gravity southeast -annotate +6+6 'Camera 1' " + photo_location

                # Log that we the text was added successfully"
                logging.info('Added the overlay text successfully')
                call ([overlay], shell=True)

                # Add a small Naturebytes logo to the top left of the photo. Note - you could change this to your own logo if you wanted.
                logging.info('Adding the Naturebytes logo')
                overlay = '/usr/bin/convert '+ photo_location + ' ./naturebytes_logo_80.png -geometry +1+1 -composite ' + photo_location
                call ([overlay], shell=True)

                # Log that the logo was added succesfully"
                logging.info('Logo added successfully')
            else:
                # print "Waiting for a new PIR trigger to continue"
                logging.info('Waiting for a new PIR trigger to continue')

if __name__ == "__main__":
    main()

