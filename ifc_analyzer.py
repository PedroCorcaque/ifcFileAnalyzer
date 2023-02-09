import ifcopenshell
import ifcopenshell.geom
from os import listdir
from os.path import isfile, isdir, join
from tqdm import tqdm

from libs import ifc2x3_analyzer, ifc4_analyzer

FILE_TYPES = ["ifc", "IFC"]

ifc2x3_file = "/home/pedro/Dev/aeroscan_ws/data/ifc/Staircase.ifc"
ifc4_file = "/home/pedro/Dev/aeroscan_ws/data/ifc/mapping_IFC4_Convenience_store.ifc"

if __name__ == "__main__":
    directories = []

    filenames = []
    while len(directories) > 0:
        current_dir = directories.pop(0)
        files = [join(current_dir, f) for f in listdir(current_dir) if f[-3:] in FILE_TYPES and isfile(join(current_dir, f))]
        dirs = [join(current_dir, d) for d in listdir(current_dir) if isdir(join(current_dir, d))]
        
        filenames += files
        directories += dirs

    settings = ifcopenshell.geom.settings()
    for file in tqdm(filenames):
        if ifcopenshell.open(file).schema == "IFC2X3":
            ifc2x3_analyzer(file, settings)
        elif ifcopenshell.open(file).schema == "IFC4":
            ifc4_analyzer(file, settings)
        else:
            raise Exception("Schema not found.")