import ifcopenshell
import ifcopenshell.geom

from libs import ifc2x3_analyzer, ifc4_analyzer

ifc2x3_file = "/home/pedro/Dev/aeroscan_ws/data/ifc/Staircase.ifc"
ifc4_file = "/home/pedro/Dev/aeroscan_ws/data/ifc/mapping_IFC4_Convenience_store.ifc"
ALL_FILES = [ifc2x3_file, ifc4_file]

if __name__ == "__main__":

    settings = ifcopenshell.geom.settings()
    for file in ALL_FILES:
        if ifcopenshell.open(file).schema == "IFC2X3":
            ifc2x3_analyzer(file, settings)
        elif ifcopenshell.open(file).schema == "IFC4":
            ifc4_analyzer(file, settings)
        else:
            raise Exception("Schema not found.")