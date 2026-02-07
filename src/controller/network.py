import logging as log
from time import sleep

from speedtest import Speedtest, SpeedtestException

from src.util.threads import get_thread_warden


log.getLogger(__name__)


class network:

    def __init__(self) -> None:
        self.st: Speedtest = Speedtest()

        self.download: int = None
        self.upload: int = None

        return

    def download_spinlock(self) -> None:
        log.info("Starting download spinlock")

        while True:
            try:
                download: int = self.st.download()
                self.write_download_var(download)
                log.debug(f"Download: {download}")

            except SpeedtestException as s_err:
                log.error(f"Error while evaluating the download speed: {s_err}")

        log.error("Download spinlock thread exited unexpectedly.")

        return

    def upload_spinlock(self) -> None:
        log.info("Starting upload spinlock")

        while True:
            try:
                upload: int = self.st.upload()
                self.write_upload_var(upload)
                log.debug(f"Upload: {upload}")

            except SpeedtestException as s_err:
                log.error(f"Error while evaluating the upload speed: {s_err}")

        log.error("Upload spinlock thread exited unexpectedly.")

        return

    def read_network_vars(self) -> int | int:
        # * Enter mutual exclusion zone.
        thread_warden = get_thread_warden()
        thread_warden.acquire_reader_lock()

        download = self.download
        upload = self.upload

        # * Exit mutual exclusion zone.
        thread_warden.release_reader_lock()

        return download, upload

    def write_download_var(self, download: int) -> None:
        # * Enter mutual exclusion zone.
        thread_warden = get_thread_warden()
        thread_warden.acquire_writer_lock()

        self.download = download

        # * Exit mutual exclusion zone.
        thread_warden.release_writer_lock()

        return

    def write_upload_var(self, upload: int) -> None:
        # * Enter mutual exclusion zone.
        thread_warden = get_thread_warden()
        thread_warden.acquire_writer_lock()

        self.upload = upload

        # * Exit mutual exclusion zone.
        thread_warden.release_writer_lock()

        return
