Download latest version of FlightGear [here](https://www.flightgear.org/download/).

Start FlightGear [in a terminal in linux]:

```bash
./FlightGear-2020.3.19-x86_64.AppImage --developer=true --telnet=socket,bi,60,localhost,5500,tcp
```

Establish connection between FlightGear and Apache Ignite:

```bash
python connect_and_store.py
```

View dashboard with parameter values:

```bash
streamlit run app.py
```
