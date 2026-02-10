from datetime import date, datetime
import logging as log
from pathlib import Path

from src.util.file_system import create_output_file, input_file_exists


log.getLogger(__name__)


WEAK: int = 5_000_000  # 5 Mbps
MEDIUM: int = 25_000_000  # 25 Mbps


def convert_rows(list_to_write: list[float, float, float, float], output_file: Path):
    with open(output_file, "a", encoding="UTF-8") as fd:
        # Write the file header.
        # fd.write("{\n" + '\t"type": "FeatureCollection",\n' + '\t"features": [\n')

        # Convert the CSV data to GeoJSON.
        num_rows: int = len(list_to_write)
        for i, row in enumerate(list_to_write):
            lat: float = row[0]
            lon: float = row[1]
            download: float = row[2]
            upload: float = row[3]

            geojson_row: str = (
                "\t\t{\n"
                + '\t\t\t"type": "Feature",\n'
                + '\t\t\t"properties": {\n'
                + f'\t\t\t\t"download": {download},\n'
                + f'\t\t\t\t"upload": {upload}\n'
                + "\t\t\t},\n"
                + '\t\t\t"geometry": {\n'
                + '\t\t\t\t"type": "Point",\n'
                + f'\t\t\t\t"coordinates": [{lon}, {lat}]\n'
                + "\t\t\t}\n"
            )

            # JSON Formatting weirdness.
            if (i + 1) < num_rows:
                geojson_row += "\t\t},\n"
            else:
                geojson_row += "\t\t}\n"

            fd.write(geojson_row)
            log.debug(geojson_row)

        # Write the file footer.
        fd.write("\t]\n" + "}")


def export(input_file: Path) -> None:
    if not input_file_exists(input_file):
        print("Input file doesn't exist!")
        log.info("Input file doesn't exist!")

        return

    weak_list: list[list[float, float, float, float]] = []
    medium_list: list[list[float, float, float, float]] = []
    strong_list: list[list[float, float, float, float]] = []

    # Iterate through CSV data and determine which rows are weak, medium,
    #   and strong.
    with open(input_file, "r", encoding="UTF-8") as fd:
        next(fd)
        for row in fd:
            row = row.replace("\n", "")
            row = row.replace("'", "")
            print(row)
            row_vars: list[str] = row.split(",")

            lat: float = float(row_vars[0])
            lon: float = float(row_vars[1])
            download: float = float(row_vars[2]) if row_vars[2] != "None" else 0
            upload: float = float(row_vars[3]) if row_vars[3] != "None" else 0

            parsed_row: list[float, float, float, float] = [lat, lon, download, upload]

            if download < WEAK:
                weak_list.append(parsed_row)
            elif download < MEDIUM:
                medium_list.append(parsed_row)
            else:
                strong_list.append(parsed_row)

    # Convert the rows of each list ot GeoJSON.
    if len(weak_list) > 0:
        output_file: Path = Path(
            f"./output/output_{date.today()}-{datetime.now().strftime("%H.%M.%S")}_weak.geojson"
        )
        create_output_file(
            output_file,
            file_encoding="geojson",
        )
        convert_rows(weak_list, output_file)

    if len(medium_list) > 0:
        output_file: Path = Path(
            f"./output/output_{date.today()}-{datetime.now().strftime("%H.%M.%S")}_medium.geojson"
        )
        create_output_file(
            output_file,
            file_encoding="geojson",
        )
        convert_rows(medium_list, output_file)

    if len(strong_list) > 0:
        output_file: Path = Path(
            f"./output/output_{date.today()}-{datetime.now().strftime("%H.%M.%S")}_strong.geojson"
        )
        create_output_file(
            output_file,
            file_encoding="geojson",
        )
        convert_rows(strong_list, output_file)

    return
