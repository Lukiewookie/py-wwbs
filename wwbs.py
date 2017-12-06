#!/usr/bin/python3

import csv
import datetime
import os.path
import smtplib
import socket
import sys
from configparser import ConfigParser
from datetime import time
from email import encoders

import pyowm
import pyspeedtest
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


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


def email_sender(msg_from, msg_to, password, heading, body):



    message = MIMEMultipart()

    message['From'] = msg_from
    message['To'] = msg_to
    message['Subject'] = heading

    message.attach(MIMEText(body, 'plain'))

    attachment = open(parser.get('Functions', 'csv_file'), "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % str(parser.get('Functions', 'csv_file')))

    message.attach(part)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(msg_from, password)
    text = message.as_string()
    server.sendmail(msg_from, msg_to, text)
    server.quit()


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

    fieldnames = (
        "time", "ping", "download", "upload", "humidity",
        "temp", "temp_kf", "temp_max", "temp_min", "deg",
        "speed", "clouds", "rain", "snow", "press", "sea_level")

    try:
        if os.path.isfile('outfile.csv'):
            print("Opening %s as 'a'" % parser.get('Functions', 'csv_file'))
            outfile = open(parser.get('Functions', 'csv_file'), "a")
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        else:
            print("Opening %s as 'w'" % parser.get('Functions', 'csv_file'))
            outfile = open(parser.get('Functions', 'csv_file'), "w")
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            print("Adding headings to file...")
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

        if datetime.time().now() == time(21,00):
            email_sender(parser.get('Email', 'address_from'),
                         parser.get('Email', 'address_from'),
                         parser.get('Email', 'password'),
                         'Summery of py-wwbs for today',
                         'The file is attached below. Have a good day me :)')
