import ifcopenshell
import ifcopenshell.geom
import multiprocessing
import ifcopenshell.util.unit
import numpy as np
from tqdm import tqdm

def ifc4_analyzer(fname, settings):
    print("Processing file with IFC4 schema...")
    try:
        file = ifcopenshell.open(fname)
        unit_scale = ifcopenshell.util.unit.calculate_unit_scale(file)

        min, max = None, None

        products = file.by_type("IfcProduct")
        for product in tqdm(products):
            try:
                shape = ifcopenshell.geom.create_shape(settings, product)
                verts = np.array(shape.geometry.verts).reshape(-1,  3)

                if min is not None:
                    verts = np.vstack((verts, min))
                if max is not None:
                    verts = np.vstack((verts, max))
                min = np.min(verts, axis=0)
                max = np.max(verts, axis=0)
            except Exception as e:
                raise Exception("Representation is null in some products.")            
        
        l, w, h = tuple((max - min)*unit_scale)
        return (fname.split('/')[-1], l, w, h)
    except Exception as e:
        print(e)
        print(ifcopenshell.get_log())
    