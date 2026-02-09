# Cell Trace 📶🗼

This tool allows you to continuously monitor and store cellular network throughput metrics and pin it to geographic locations. After collecting the data, you can export it to GeoJSON and import it to Google Earth or GIS applications. This is useful for anyone wishing to map cellular connectivty to geographic locations to identify deadspots, such as high throughput in Salinas and low throughput on Highway 1 in Big Sur.

The geographic location is captured from a GPS chip. GPS NMEA (National Marine Electronics Association) is the standard ASCII-based communication protocol used by GNSS receivers to transmit data to other devices and communicate global positioning. 


## How to use 

### Capture metrics 

To run this program with default parameters, issue the following command. This will run network and GPS evaluations until a keyboard interrupt is issued.

```python
python -m src.main
```

Here are the options defined within the help menu. 

```powershell
python -m src.main -h                  
    usage: main.py [-h] [-c COM] [-l {none,debug,info,warning,error}] [-t TIMEOUT]

    options:
    -h, --help            show this help message and exit
    -c, --com COM         Set the COM serial port to read GPS data from.
    -l, --log {none,debug,info,warning,error}
                            Set the logging level of the application. Default is "INFO" level logging.
    -t, --timeout TIMEOUT
                            The interval between network and GPS data sampling.
```


## Python package dependencies

To run this program, install the following Python packages.

```python
python -m pip install pynmea2 serial speedtest-cli
```


## Contributors

Programmer: Cameron Oakley (Oakley.CameronJ@gmail.com)

Organization: Monterey County Sheriff's Office