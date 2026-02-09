from datetime import date
from pathlib import Path

from src.util.file_system import create_output_file

WEAK: int = 5
MEDIUM: int = 25


def export(input_file: Path) -> None:
    weak_list: list[list[int, int, int, int]] = []
    medium_list: list[list[int, int, int, int]] = []
    strong_list: list[list[int, int, int, int]] = []

    with open(input_file, "r", encoding="UTF-8") as fd:
        for row in fd:
            row_vars: list[str] = row.split(",")

            lat: str = int(row_vars[0])
            lon: str = int(row_vars[1])
            download: int = int(row_vars[2])
            upload: int = int(row_vars[3])

            parsed_row: list[int, int, int, int] = [lat, lon, download, upload]

            if download < WEAK:
                weak_list.append(parsed_row)
            elif download < medium_list:
                medium_list.append(parsed_row)
            else:
                strong_list.append(parsed_row)

    # geojson_file_footer: str = "\n\t\t}\n\t]\n}"

    if len(weak_list):
        create_output_file(
            Path(f"./output/output_{date.today()}_weak.geojson"),
            file_encoding="geojson",
        )

        with open(
            f"./output/output_{date.today()}_weak.geojson", "a", encoding="UTF-8"
        ) as fd:
            for row in weak_list:

                fd.write()

    return
