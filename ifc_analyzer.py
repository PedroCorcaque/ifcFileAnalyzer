import multiprocessing
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.unit
import numpy as np
import argparse
from os import listdir
from os.path import isfile, isdir, join
import csv
from tqdm import tqdm

FILE_TYPES = ['ifc', 'IFC']

parser = argparse.ArgumentParser(
                    prog = 'IfcAnalyzer',
                    description = 'Code to analyze IFC files',
                    epilog = 'Text at the bottom of help')

parser.add_argument('foldername')
# parser.add_argument('-c', '--count')
# parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()

if __name__ == '__main__':
    foldername = args.foldername

    directories = [foldername]
    filenames = []
    while len(directories) > 0:
        current_dir = directories.pop(0)
        files = [join(current_dir, f) for f in listdir(current_dir) if f[-3:] in FILE_TYPES and isfile(join(current_dir, f))]
        dirs = [join(current_dir, d) for d in listdir(current_dir) if isdir(join(current_dir, d))]
        
        filenames += files
        directories += dirs

    results = []
    files_error = []
    settings = ifcopenshell.geom.settings()
    for fname in tqdm(filenames):
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
            result = (fname.split('/')[-1], l, w, h, l*w, l*w*h)
            results.append(result)
        except ifcopenshell.SchemaError as e:
            files_error.append(fname)
    
    outname = join(foldername, 'result.csv')

    with open(outname, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print('Files Error:', files_error)
