import logging as log
from time import sleep

from src.controller.gps import gps
from src.controller.network import network


log.getLogger(__name__)


def loop(gps_monitor: gps, network_monitor: network, timeout: int = 15):
    while True:
        log.info("Starting monitoring loop")
        sleep(timeout)

        log.debug(f"Latitude, Longitude: {gps_monitor.read_gps_vars()}")
        print(f"Latitude, Longitude: {gps_monitor.read_gps_vars()}")
        log.debug(f"Download, Upload: {network_monitor.read_network_vars()}")
        print(f"Download, Upload: {network_monitor.read_network_vars()}")

    log.error("Monitoring loop exited unexpectedly.")
    return
