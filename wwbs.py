import pyspeedtest
import pyowm
import csv
import datetime


def get_broadband():

    speedlist = [datetime.datetime.now()]

    print("Obtaining ping")
    ping = st.ping()
    print(ping)

    speedlist.append(ping)

    print("Obtaining download")
    download = st.download()
    print(download)

    speedlist.append(download)

    print("Obtaining upload")
    upload = st.upload()
    print(upload)

    speedlist.append(upload)

    print(ping, download, upload)

    return speedlist


def get_weather():
    weatherlist = temperature()
    weatherlist += wind()
    weatherlist.append(w.get_humidity())
    weatherlist.append(w.get_clouds())
    weatherlist += precipitation()
    weatherlist += pressure()
    return weatherlist


def wind():
    wind_arr = []
    wind = w.get_wind()

    wind_speed = wind['speed']
    wind_dir = wind['deg']

    wind_arr.append(wind_speed)
    wind_arr.append(wind_dir)

    return wind_arr


def temperature():
    temp_arr = []
    temp = w.get_temperature('celsius')

    temp_avg = temp['temp']
    temp_max = temp['temp_max']
    temp_min = temp['temp_min']

    temp_arr.append(temp_avg)
    temp_arr.append(temp_max)
    temp_arr.append(temp_min)

    return temp_arr


def pressure():
    prss_arr = []
    prss = w.get_pressure()

    prss_arr.append(prss['press'])
    return prss_arr

def precipitation():
    precp_arr = []
    snow = w.get_snow()
    rain = w.get_rain()

    if snow == "{}":
        snow = 0
    elif rain == "{}":
        rain = 0

    precp_arr.append(rain)
    precp_arr.append(snow)

    return precp_arr


def logger():
    output = get_broadband() + get_weather()  # List concatenation
    writer.writerow(output)


if __name__ == "__main__":

    outfile = open('outfile.csv', "w")
    writer = csv.writer(outfile)

    writer.writerow(
        ["time", "ping", "upld", "dwnld", "temp", "temp_max", "temp_min", "windspd", "winddir", "hmdt", "clouds",
         "rain", "snow", "prss"])

    speedlist = []
    weatherlist = []

    st = pyspeedtest.SpeedTest()

    owm = pyowm.OWM(API_key='867d56c41c4381897f24da1546177a85')
    observation = owm.weather_at_place('Ostrava, Czech Republic')

    w = observation.get_weather()

    logger()

