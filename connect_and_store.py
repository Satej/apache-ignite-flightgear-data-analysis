import time
from flightgear_python.fg_if import TelnetConnection
from pyignite import Client
from pyignite.datatypes import CollectionObject, MapObject, ObjectArrayObject

# Initialize the Ignite client and connect to the Ignite cluster
ignite_client = Client()
ignite_client.connect('127.0.0.1', 10800)  # Replace with your Ignite server address and port

# Create or get a cache for storing the data points
cache = ignite_client.get_or_create_cache('flight_data_cache')

# Start FlightGear with the appropriate telnet configuration: `--telnet=socket,bi,60,localhost,5500,tcp`
telnet_conn = TelnetConnection('localhost', 5500)
telnet_conn.connect()  # Establish connection with FlightGear
type_id = MapObject.LINKED_HASH_MAP

while True:
    # Get properties for oil temperature, engine state, and altitude
    oil_temperature_str = telnet_conn.get_prop('/engines/engine/oil-temperature-degf')
    engine_running = telnet_conn.get_prop('/engines/engine/running')
    altitude_ft_str = telnet_conn.get_prop('/position/altitude-ft')

    # Directly convert properties to float, without checks (empty values will result in 0.0)
    oil_temperature = float(oil_temperature_str) if oil_temperature_str else 0.0
    altitude_ft = float(altitude_ft_str) if altitude_ft_str else 0.0
    timestamp = time.time()

    # Prepare the data as a dictionary (or tuple) to store in Ignite
    data_point = {
        'timestamp': timestamp,
        'oil_temperature': oil_temperature,
        'altitude_ft': altitude_ft,
        'engine_running': engine_running
    }
    
    cache.put(int(timestamp), (type_id, data_point))

    print(f"Oil Temperature: {oil_temperature:.1f} °F")
    print(f"Altitude: {altitude_ft:.1f} ft")
    print(f"Engine Running: {engine_running}")


    # Sleep before the next data collection
    time.sleep(1)

# Close Ignite client connection when done
ignite_client.close()

