import os
import smtplib
import time
from datetime import datetime

import requests

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("PASSWORD")
REAL_EMAIL = os.environ.get("REAL_EMAIL")
MY_LAT = 52.26194  # Your latitude
MY_LONG = 4.50352  # Your longitude


def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LONG - 5 <= iss_longitude <= MY_LONG + 5 and MY_LAT - 5 <= iss_latitude <= MY_LAT + 5:
        print(iss_longitude, iss_latitude)
        return True
    else:
        print(iss_longitude, iss_latitude)
        return False



def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("http://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        print(time_now, sunrise, sunset)
        return True
    else:
        print(time_now, sunrise, sunset)
        return False


while True:
    time.sleep(10)
    print("LooP")

    if iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=REAL_EMAIL,
            msg="Subject: Look up!\n\nTe ISS is above you in the sky."
        )
    print(iss_overhead())
    print(is_night())
