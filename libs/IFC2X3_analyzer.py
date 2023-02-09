import multiprocessing
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.unit
import numpy as np

def ifc2x3_analyzer(fname, settings):
    print("Processing file with IFC2X3 schema...")
    try:
        model = ifcopenshell.open(fname)
        unit_scale = ifcopenshell.util.unit.calculate_unit_scale(model)
        iterator = ifcopenshell.geom.iterator(settings, model, multiprocessing.cpu_count())
        min = None
        max = None
        if iterator.initialize():
            while True:
                shape = iterator.get()
                matrix = np.array(shape.transformation.matrix.data).reshape(3,4)
                # faces = np.unique(np.array(shape.geometry.faces))
                verts = np.array(shape.geometry.verts).reshape(-1,  3)#[faces]
                #verts = verts - matrix[:, 3]
                #verts = np.array([matrix[0:3,0:3].T @ v.T for v in verts])

                if min is not None:
                    verts = np.vstack((verts, min))
                if max is not None:
                    verts = np.vstack((verts, max))
                min = np.min(verts, axis=0)
                max = np.max(verts, axis=0)
                if not iterator.next():
                    break
        l, w, h = tuple((max - min)*unit_scale)
        result = (fname.split('/')[-1], l, w, h)
        print("Done.")
        return result
    except ifcopenshell.SchemaError as e:
        print(e)