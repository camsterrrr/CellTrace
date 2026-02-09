import logging as log
from os.path import exists
from os import mkdir
from pathlib import Path


log.getLogger(__name__)


##########################################################################
######################   CORE FILE SYSTEM LOGIC   ########################
##########################################################################


def create_output_directory(output_dir: Path = Path("./output/")) -> None:
    if not exists(output_dir):
        mkdir(output_dir)

    return


def create_output_file(output_file: Path, file_encoding: str = "csv") -> None:
    if not exists(output_file):
        with open(output_file, "w", encoding="UTF-8") as fd:
            if file_encoding.lower() == "csv":
                fd.write("'latitude','longitude','download','upload'\n")

            elif file_encoding.lower() == "geojson":
                fd.write('{\n\t"type": "FeatureCollection",\n\t"features": [\n')

    return


def input_file_exists(input_file: Path) -> bool:
    return exists(input_file)
