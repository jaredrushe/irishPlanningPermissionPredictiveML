import requests
import pandas as pd
import time

#N.B. This script has an extremely long execution time on my dataset of around 15 hours
#Imported Photon API
PHOTON_URL = "https://photon.komoot.io/api/"

#Read in processed Planning Data saved locally from Drive
#To reproduce code, replace with your own file path
df = pd.read_csv("planningAppsCleaned.csv")

#Added columns for latitude and longitude values as well as a boolean for whether the address could be converted
df["lat"] = None
df["lon"] = None
df["geocode_success"] = False

#Defined function to convert addresses to GPS coordinates
def geocode_address(address, delay=0.1):
    try:
        #Sent request to PHOTON API to convert address 
        r = requests.get(PHOTON_URL, params={"q": address, "limit": 1}, timeout=10)
        
        #Added waittime to prevent overloading server
        time.sleep(delay)

        #Read response as json
        data = r.json()

        #If conversion was successful, return latitude, longitude and boolean
        if "features" in data and len(data["features"]) > 0:
            lon, lat = data["features"][0]["geometry"]["coordinates"]
            return lat, lon, True
        #Else return None and False values
        else:
            return None, None, False

    #Printed error message if problem occurs
    except Exception as e:
        print(f"Error for '{address}': {e}")
        return None, None, False


#Iterate through dataframe calling each address as parameter for function
for idx, row in df.iterrows():
    address = row["full_address"]

    lat, lon, ok = geocode_address(address)

    #Save values into dataframe
    df.at[idx, "lat"] = lat
    df.at[idx, "lon"] = lon
    df.at[idx, "geocode_success"] = ok

    #Print status updates for each address
    print(f"[{idx+1}/{len(df)}] {address}  →  {lat}, {lon}")

#Saved geocoded dataframe to csv
df.to_csv("planningAppsGeocoded.csv", index=False)
