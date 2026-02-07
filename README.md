# Mobile Monitor

This tool allows you to continuously run network throughput evaluations and pin it to a specific geographic location. After exporting the data, you can import it to Google Earth or GIS applications.

Geographic location is captured from GPS data. GPS NMEA (National Marine Electronics Association) is the standard ASCII-based communication protocol used by GNSS receivers to transmit data to other devices and communicate global positioning. 

## How to use

```python
python -m src.main
```


## Python package dependencies

```python
python -m pip install pynmea2 serial speedtest-cli
```


## Contributors

Programmer: Cameron Oakley (Oakley.CameronJ@gmail.com)
Organization: Monterey County Sheriff's Office