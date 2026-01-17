import requests
import pandas as pd
from datetime import datetime, timedelta
import os


def process_earthquake_data():
    today_date = datetime.now()

    date_15_days_ago = today_date - timedelta(days=15)
    start_time = date_15_days_ago.strftime("%Y-%m-%d")
    end_time = today_date.strftime("%Y-%m-%d")

    # Define the API endpoint
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_time}&endtime={end_time}"




    # Send a GET request to the API endpoint
    response = requests.get(url)

    print(response.json())
    print(response.status_code)

# check if the request waas sucessful
    if response.status_code == 200:
        #parse the response content as JSON
        data =response.json()


        #Extract earthquake features
        features = data['features']

        # Create a list of dictionaries containing relevant data
        earthquakes = []

        date = today_date.strftime("%Y_%m_%d")
        filename = rf"C:\Users\iyanu\Downloads\LEARNING DATA ANALYTICS\Data Pipelines Course\earthquake_{date}.csv"

        for feature in features :
            properties = feature['properties']
            geometry = feature['geometry']
            earthquake ={
                'time': properties ['time'],
                'place': properties ['place'],
                'magnitude':properties ['mag'],
                'longitude': geometry ['coordinates'][0],
                'latitude': geometry ['coordinates'][1],
                'depth':geometry ['coordinates'][2],
                'file_name':filename
            }

            earthquakes.append(earthquake)
        print(earthquakes)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(earthquakes)

        #use today's date variable to create a file name

        #check if the files exsists
        #check if the files exsists
        if os.path.exists(filename):
            # if it exists, remove it
            os.remove(filename)
            print(f"File{filename} removed.")


        #now create a new file

        df.to_csv(filename, index=False)
        print(f"File {filename} created and written to.")
    else:
        print(f"Failed to retrive data: {response.status_code}")
      


def main():
    process_earthquake_data()


if __name__ == "__main__":
    main()
