import logging as log

from serial import Serial, SerialException
from pynmea2 import ParseError, parse, types

from src.util.threads import get_thread_warden


log.getLogger(__name__)


class gps:

    def __init__(self, com_port: str = "COM20") -> None:
        # GPS chip serial object.
        self.serial_port: Serial = Serial(com_port, 9600)

        # GPS variables.
        self.lon: int = None
        self.lat: int = None

        return

    def gps_spinlock(self) -> None:
        log.info("Starting GPS spinlock")

        while True:
            try:
                line = (
                    self.serial_port.readline().decode("ascii", errors="ignore").strip()
                )
                # log.debug(line)

                # Only parse lines if they have a start delimeter. Helps avoid
                #   misalignment issues.
                if not line:
                    continue
                if line.startswith("$"):
                    try:
                        # Parse the raw data and convert to NMEA object.
                        nmea_msg = parse(line)
                        # log.debug(nmea_msg)

                        # From Wikipedia: $Talker ID+GGA: Global Positioning System Fixed Data
                        if isinstance(nmea_msg, types.talker.GGA):
                            log.debug(
                                f"Lat: {nmea_msg.latitude}, "
                                f"Lon: {nmea_msg.longitude}, "
                                f"Alt: {nmea_msg.altitude} {nmea_msg.altitude_units}, "
                                f"Fix: {nmea_msg.gps_qual}"
                            )
                            self.write_gps_vars(nmea_msg.latitude, nmea_msg.longitude)

                    except ParseError as p_err:
                        log.error(f"Error while parsing NMEA GPS data: {p_err}")

            except SerialException as s_err:
                log.error(f"Error while reading data from serial port: {s_err}")

        log.error("GPS spinlock thread exited unexpectedly.")

        return

    def read_gps_vars(self) -> int | int:
        # * Enter mutual exclusion zone.
        thread_warden = get_thread_warden()
        thread_warden.acquire_reader_lock()

        lat = self.lat
        lon = self.lon

        # * Exit mutual exclusion zone.
        thread_warden.release_reader_lock()

        return lat, lon

    def write_gps_vars(self, lat: int, lon: int) -> None:
        # * Enter mutual exclusion zone.
        thread_warden = get_thread_warden()
        thread_warden.acquire_writer_lock()

        self.lat = lat
        self.lon = lon

        # * Exit mutual exclusion zone.
        thread_warden.release_writer_lock()

        return
