import pyspeedtest
import pyowm
import csv
import datetime


def get_broadband():

    speeddict = {'time': datetime.datetime.now()}

    # TODO: Add exception handling for when the is no internet

    print("Obtaining ping")
    ping = st.ping()
    print(ping)

    speeddict['ping'] = ping

    print("Obtaining download")
    download = st.download()
    print(download)

    speeddict['download'] = download

    print("Obtaining upload")
    upload = st.upload()
    print(upload)

    speeddict['upload'] = upload

    return speeddict


def get_weather():
    weatherdict = {'humidity': w.get_humidity()}
    weatherdict.update(w.get_temperature(unit='celsius'))
    weatherdict.update(w.get_wind())
    weatherdict['clouds'] = w.get_clouds()
    weatherdict['rain'] = w.get_rain()
    weatherdict['snow']  = w.get_snow()
    weatherdict.update(w.get_pressure())

    return weatherdict

def logger():
    output = {}
    output.update(get_broadband())
    output.update(get_weather())# Dict concatenation
    writer.writerow(output)


if __name__ == "__main__":

    print("Opening outfile.csv as 'w'")
    try:
        outfile = open('outfile.csv', "w")
        fieldnames = ("time", "ping", "download", "upload", "humidity", "temp", "temp_kf", "temp_max", "temp_min", "deg", "speed", "clouds",
         "rain", "snow", "press", "sea_level")
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
    except Exception as e:
        print("Problem opening the file.")

    speeddict = []
    weatherdict = []

    st = pyspeedtest.SpeedTest()

    print("Connecting to OWM with API key and setting location to Ostrava")
    try:
        owm = pyowm.OWM(API_key='867d56c41c4381897f24da1546177a85')
        observation = owm.weather_at_place('Ostrava, Czech Republic')
    except Exception as e:
        print("Problem connection to OWM")

    w = observation.get_weather()

    while True:
        logger()
        print("Logger printed")
        #time.sleep(10*60)  # OWM doesn't update more often

