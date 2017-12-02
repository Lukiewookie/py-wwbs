#!/usr/bin/python3

import csv
import datetime
import socket
import sys
import time
from configparser import ConfigParser

import pyowm
import pyspeedtest


def get_broadband():
    speeddict = {'time': datetime.datetime.now()}

    print("Obtaining ping")
    ping = st.ping()

    speeddict['ping'] = ping

    print("Obtaining download")
    download = st.download()

    speeddict['download'] = download

    print("Obtaining upload")
    upload = st.upload()

    speeddict['upload'] = upload

    return speeddict


def get_weather():
    weatherdict = {'humidity': w.get_humidity()}

    weatherdict.update(w.get_temperature(unit='celsius'))
    weatherdict.update(w.get_wind())

    weatherdict['clouds'] = w.get_clouds()
    weatherdict['rain'] = w.get_rain()
    weatherdict['snow'] = w.get_snow()

    weatherdict.update(w.get_pressure())

    return weatherdict


def logger():
    output = {}

    output.update(get_broadband())
    output.update(get_weather())

    writer.writerow(output)


if __name__ == "__main__":

    parser = ConfigParser()
    parser.read('config.ini')

    remote_server = "www.google.com"

    try:
        host = socket.gethostbyname(remote_server)
        s = socket.create_connection((host, 80), 2)
        pass
    except socket.gaierror:
        print("Can't connect to internet, exiting...")
        sys.exit()

    print("Opening %s as 'w'" % parser.get('Functions', 'csv_file'))
    try:
        outfile = open(parser.get('Functions', 'csv_file'), "w")
        fieldnames = (
            "time", "ping", "download", "upload", "humidity",
            "temp", "temp_kf", "temp_max", "temp_min", "deg",
            "speed", "clouds", "rain", "snow", "press", "sea_level")
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    except RuntimeError as e:
        print("Problem opening the file.")
        print("error:", str(e))

    st = pyspeedtest.SpeedTest()

    print("Attempting connection to OWM...")
    try:
        owm = pyowm.OWM(API_key=parser.get('API','API_key'))
        observation = owm.weather_at_place(parser.get('Functions', 'location'))
        print("Location set to %s" % parser.get('Functions', 'location'))
    except RuntimeError as e:
        print("Problem connection to OWM")
        print("error:", str(e))

    w = observation.get_weather()

    while True:
        logger()
        print("Logger printed")
        print("Sleeping for %s seconds"  % parser.get('Functions', 'update_timer'))
        time.sleep(int(parser.get('Functions', 'update_timer')))  # OWM doesn't update more often
