import streamlit as st
import time
import pandas as pd
from pyignite import Client
from pyignite.datatypes import MapObject
import matplotlib.pyplot as plt

# Initialize the Ignite client and connect to the Ignite cluster
ignite_client = Client()
ignite_client.connect('127.0.0.1', 10800)  # Replace with your Ignite server address and port

# Get the cache where data is being stored
cache = ignite_client.get_cache('flight_data_cache')

# Streamlit setup
st.title("Flight Data - Real-time View")
st.write("Displaying real-time flight data (oil temperature, altitude, and engine status)")

# Create a placeholder for the plot
placeholder = st.empty()

# Initialize an empty DataFrame to store data for plotting

# Real-time data collection
while True:
    df = pd.DataFrame(columns=['timestamp', 'oil_temperature', 'altitude_ft', 'engine_running'])
    # Get the current timestamp
    current_time = int(time.time())
    
    # Fetch the last 100 keys in the cache (the most recent data points)
    data_points = []
    
    # Fetch data for the range current_time-100 to current_time
    for offset in range(100):
        key = current_time - offset
        if cache.contains_key(key):
            data_point = cache.get(key)[1]  # The data point is the second item in the tuple
            data_points.append(data_point)
    
    # If there are data points, convert them into a DataFrame
    if data_points:
        new_data = pd.DataFrame(data_points)
        # Sort the data by timestamp in ascending order (to ensure it is ordered correctly)
        new_data = new_data.sort_values(by='timestamp', ascending=True)
        
        # Concatenate the new data with the previous data and keep only the latest 100 entries
        df = pd.concat([df, new_data], ignore_index=True).tail(100)

    # Plot the data
    fig, ax = plt.subplots()

    ax.plot(df['timestamp'], df['oil_temperature'], label='Oil Temperature (°F)', color='tab:red')
    ax.plot(df['timestamp'], df['altitude_ft'], label='Altitude (ft)', color='tab:blue')

    ax.set_xlabel('Timestamp')
    ax.set_ylabel('Values')
    ax.set_title('Flight Data (Oil Temperature & Altitude)')
    ax.legend(loc='upper right')

    # Update the Streamlit plot
    placeholder.pyplot(fig)

    # Sleep for a short period before the next update
    time.sleep(1)

# Close Ignite client connection when done
ignite_client.close()

