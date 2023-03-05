import pprint
import requests

from matplotlib import pyplot as plt
from datetime import datetime
from dotenv import dotenv_values

config = dotenv_values(".env")

DEG_F ='f'
DEG_C = 'c'

def to_fahrenheit(K):
    return round((float(K) - 273.15)* 1.8000+ 32.00)


def to_celcius(K):
    return round(float(K) - 273.15)

def formatter(dates):
    def get_dates(x):
        try:
            return dates[int(x)]
        except:
            return ""
    def fmt(x):
        dt = datetime.fromisoformat(get_dates(x))
        if dt.hour == 0 or x == 0 or x == len(dates) - 1:
            return dt.strftime("%b %d %#I %p")
        else:
            return dt.strftime("%#I %p")
    return lambda x,pos: fmt(x)       


def get_regional_weather(region, units = DEG_F):
    API_KEY = config["API_KEY"]
    print(API_KEY)
    API_URL= f"https://api.openweathermap.org/data/2.5/forecast?appid={API_KEY}&q={region}"
    req= requests.get(API_URL)
    print(req)
    response=req.json()

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(response)

    forecast_list = response["list"]

    dates =[]
    temps =[]

    temp_formatter = to_fahrenheit if units is DEG_F else to_celcius

    for forecast in forecast_list:
        date = forecast["dt_txt"]
        temp = temp_formatter(forecast["main"]["feels_like"])
        dates.append(date)
        temps.append(temp)

    return dates, temps, units

def plot_data(region, dates, temps, units):
    plt.title(f"The 5 day forecast for {region}")
    plt.plot(dates, temps)

    plt.xlabel("Dates")

    unit="Fahrenheit" if units is DEG_F else "Celcius"
    plt.ylabel(f"Temperatures in {units}")

    ax = plt.gca()
    ax.xaxis.set_major_formatter(formatter(dates))
    
    plt.tick_params(axis = "x", labelrotation =90)
    plt.show()

def main():
    print(config)
    region = input("Weather Forecast\n\nFor what reagion do you want weather?  ")
    data=None
    if len(region) == 0 or region.upper()=="NONE":
        exit()
    try:
        data = get_regional_weather(region)
    except (ValueError) as e:
        print(str(e))
        exit()
    except:
        print("Sorry I could not find that region")
        exit()
    else:
        print("Generating weather plot...")
        plot_data(region, *data)


if __name__ == "__main__":
    main()