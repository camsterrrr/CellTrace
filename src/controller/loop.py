import logging as log
from time import sleep

from src.controller.gps import gps
from src.controller.network import network
from src.controller.output import write


log.getLogger(__name__)


def loop(gps_monitor: gps, network_monitor: network, timeout: int = 15):
    log.info("Starting monitoring loop")

    while True:
        sleep(timeout)

        lat, lon = gps_monitor.read_gps_vars()
        download, upload = network_monitor.read_network_vars()

        log.debug(f"Latitude, Longitude: {lat, lon}")
        print(f"Latitude, Longitude: {lat, lon}")
        log.debug(f"Download, Upload: {download, upload}")
        print(f"Download, Upload: {download, upload}")

        write(lat, lon, download, upload)

    log.error("Monitoring loop exited unexpectedly.")
    return
