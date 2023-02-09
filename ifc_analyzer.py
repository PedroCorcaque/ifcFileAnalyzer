import ifcopenshell

from libs import ifc4_analyzer, ifc2x3_analyzer

import inspect

RIGHT_FILENAME = "/home/pedro/Dev/aeroscan_ws/data/ifc/Staircase.ifc"
WRONG_FILENAME = "/home/pedro/Dev/aeroscan_ws/data/ifc/mapping_IFC4_Convenience_store.ifc"
LIST_OF_ALL_FILES = [RIGHT_FILENAME, WRONG_FILENAME]

if __name__ == "__main__":

    settings = ifcopenshell.geom.settings()
    for file in LIST_OF_ALL_FILES:
        if ifcopenshell.open(file).schema == "IFC2X3":
            ifc2x3_analyzer(file, settings)
        elif ifcopenshell.open(file).schema == "IFC4":
            ifc4_analyzer(file, settings)
        else:
            raise Exception("Schema is not found.")
