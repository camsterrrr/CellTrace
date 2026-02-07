from argparse import ArgumentParser, Namespace
from asyncio import run
import logging as log
from threading import Thread

from src.controller.gps import gps
from src.controller.loop import loop
from src.controller.network import network


LOG_LEVELS = {
    "none": log.NOTSET,
    "debug": log.DEBUG,
    "info": log.INFO,
    "warning": log.WARNING,
    "error": log.ERROR,
}


def configure_argparse() -> Namespace:
    """
    Function that instantiates the ArgumentParser object that interprets
        user-specified parameters.

    Returns:
        Namespace: The parameters the user specified.
    """
    parser = ArgumentParser()

    parser.add_argument(
        "-c",
        "--com",
        default="COM20",
        help="Set the COM serial port to read GPS data from.",
        type=str,
    )

    parser.add_argument(
        "-l",
        "--log",
        choices=list(LOG_LEVELS.keys()),
        default="info",
        help='Set the logging level of the application. Default is "INFO" level logging.',
        type=str,
    )

    parser.add_argument(
        "-t",
        "--timeout",
        default=15,
        help="The interval between network and GPS data sampling.",
        type=int,
    )

    return parser.parse_args()


def configure_logging(user_specified_level: str = "info"):
    """
    Function that configures logging for the entire project.

    Args:
        log_level (int, optional): User-specified log level. Defaults to
            2, which represents INFO mode.
    """
    log_level = LOG_LEVELS.get(user_specified_level.lower(), log.INFO)

    log.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="mobile_monitor.log",
        format="%(levelname)s,%(asctime)s,%(message)s",
        level=log_level,
    )

    return


##########################################################################
############################   ENTRY POINT   #############################
##########################################################################

if __name__ == "__main__":
    try:
        # Parse user specified parameters
        user_args = configure_argparse()

        # Configure project logging.
        configure_logging(user_args.log)

        log.info(
            "\n==================================================="
            + "\n\t\t\tStarting Mobile Monitor!\t\t\t"
            + "\n==================================================="
        )

        # Start the main thread.
        gps_monitor = gps(user_args.com)
        network_monitor = network()

        # * Thread(target=gps_monitor.gps_spinlock(), daemon=True).start()
        # * This transfers control to function, not running in background.

        Thread(target=gps_monitor.gps_spinlock, daemon=True).start()
        Thread(target=network_monitor.download_spinlock, daemon=True).start()
        Thread(target=network_monitor.upload_spinlock, daemon=True).start()
        loop(gps_monitor, network_monitor, user_args.timeout)

    except Exception as err:
        log.error(
            "A unexpected error occurred while trying to start the main thread: %s",
            err,
        )
