from datetime import date
from pathlib import Path

from src.util.file_system import create_output_directory, create_output_file


ENCODINGS = {"csv": 1}


def to_csv(lat: int, lon: int, download: int, upload: int) -> str:
    return f"'{lat}','{lon}','{download}','{upload}'\n"


def write(
    lat: int, lon: int, download: int, upload: int, file_encoding: str = "csv"
) -> None:
    output_directory: Path = Path(f"./output/")
    output_file: Path = Path(f"./output/output_{date.today()}.csv")

    create_output_directory(output_directory)
    create_output_file(output_file, file_encoding)

    output_str: str = ""
    if file_encoding.lower() == "csv":
        output_str = to_csv(lat, lon, download, upload)

    with open(output_file, "a", encoding="UTF-8") as fd:
        fd.write(output_str)

    return
