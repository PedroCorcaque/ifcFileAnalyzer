import ifcopenshell
import ifcopenshell.geom
import multiprocessing
import ifcopenshell.util.unit
import numpy as np

def get_rotation_matrix(axis, ref_direction=None):
    z_axis = np.array(axis.DirectionRatios)
    z_axis = z_axis / np.linalg.norm(z_axis)
    x_axis = np.array(ref_direction.DirectionRatios) if ref_direction is not None else np.array([1.0, 0.0, 0.0])
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)
    return np.array([x_axis, y_axis, z_axis]).T

def ifc4_analyzer(fname, settings):
    print("Processing file with IFC4 schema...")
    try:
        file = ifcopenshell.open(fname)
        unit_scale = ifcopenshell.util.unit.calculate_unit_scale(file)

        min_x, min_y, min_z = float("inf"), float("inf"), float("inf")
        max_x, max_y, max_z = float("-inf"), float("-inf"), float("-inf")

        products = file.by_type("IfcProduct")

        for product in products:
            matrix = np.identity(4)

            object_placement = product.ObjectPlacement
            if object_placement.is_a("IfcLocalPlacement"):
                relative_placement = object_placement.RelativePlacement
                if relative_placement.is_a("IfcAxis2Placement3D"):
                    location = relative_placement.Location
                    axis = relative_placement.Axis
                    ref_direction = relative_placement.RefDirection

                    matrix[0:3, 3] = location.Coordinates
                    matrix[0:3, 0:3] = get_rotation_matrix(axis, ref_direction)           
                else:
                    print("IfcAxis2Placement3D not found.")
            else:
                print("IfcLocalPlacement not found.")  
        print("Done.")
    except Exception as e:
        print(e)
        print(ifcopenshell.get_log())

    