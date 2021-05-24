# Code originally from Tony Sohn
import argparse
import os
import glob
import numpy as np
import multiprocessing
import functools
import asdf
from jwst.pipeline import Detector1Pipeline
from jwst.pipeline import Image2Pipeline
from jwst.pipeline import Image3Pipeline
 
os.environ['MIRAGE_DATA'] = '/ifs/jwst/wit/mirage_data'
os.environ['PYSYN_CDBS']  = '/grp/hst/cdbs'

# Define input variables if not using argparse
DATA_DIR = "/user/jotaylor/git/jo_niriss_illumflat_notebook/niriss_illumflat_notebook/indir"
DET1FILES = glob.glob(os.path.join(DATA_DIR, "*uncal.fits"))
N_PROCS = None
OUTDIR = "/user/jotaylor/git/jo_niriss_illumflat_notebook/niriss_illumflat_notebook/out"

# Modify Image2 parameter ref file to skip photom and resample
step = Image2Pipeline()
step.export_config('calwebb_image2.asdf')
af = asdf.open("calwebb_image2.asdf")
for i,dct in enumerate(af.tree["steps"]):
    if dct["name"] in ["photom", "resample", "background"]:
        af.tree["steps"][i]["parameters"]["skip"] = True
new_config = os.path.join(OUTDIR, "calwebb_image3.asdf")
af.write_to(new_config)

CONFIG_FILES = {"Detector1Pipeline": None, "Image2Pipeline": new_config} 


# Function to run pipeline with multiprocessing
def _make_pipeline(pipeline, outdir, config_file, raw_file):
    if config_file is None:
        result = pipeline.call(raw_file, save_results=True, output_dir=outdir) 
    else:
        result = pipeline.call(raw_file, save_results=True, output_dir=outdir, 
                           config_file=config_file)


# Run the pipeline in parallel
def parallelize_pipeline(det1files, n_procs=N_PROCS, outdir=OUTDIR, config_files=CONFIG_FILES):
    if n_procs is None:
        n_procs = multiprocessing.cpu_count()
    with multiprocessing.Pool(n_procs) as pool:
        pipeline_function = functools.partial(_make_pipeline, Detector1Pipeline, 
                                outdir, config_files["Detector1Pipeline"])
        pool.map(pipeline_function, det1files)
    im2files = [os.path.join(outdir, os.path.basename(x).replace("uncal.fits", "rate.fits")) for x in det1files]
    with multiprocessing.Pool(n_procs) as pool:
        pipeline_function = functools.partial(_make_pipeline, Image2Pipeline, 
                                outdir, config_files["Image2Pipeline"])
        pool.map(pipeline_function, im2files)

 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--datadir", 
                        help="Directory with uncal files to calibrate")
    parser.add_argument("-o", "--outdir", 
                        help="Calibrated file output directory")
    parser.add_argument("-c", "--cpu", 
                        help="CPU count for multiprocessing")
    args = parser.parse_args()
    files = glob.glob(os.path.join(args.datadir, "*uncal.fits"))
    parallelize_pipeline(files, n_procs = args.cpu, outdir=args.outdir)
