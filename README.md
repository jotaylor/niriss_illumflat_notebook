# NIRISS Illumination Flat Analysis Workflow

## Installation
Install all required packages using the requirements file in this repository.  You can install into an existing conda environment or a new environment.

```
pip install -r requirements.txt
```

## Optional calibration

If starting from `uncal` files, run the standalone script to calibrate files in parallel.

 ```
 nice python calibrate_data.py -d <uncal_path> -o <outdir> -c <num_cpus> 
 ```

where `uncal_path` is the path to input files, `outdir` is the output file path, and `num_cpus` is the number of CPUs to use in multiprocessing. If `num_cpus` is not specified, the maximum available number will be used.

## Delta Flat Creation

Run the Jupyter notebook `niriss_illumflat_notebook_part1.ipynb. If testing copy and use the files:

`/ifs/jwst/wit/niriss/tsohn/mirage_simulations/NIS-011/jw01086001001_01101_00021_nis_cal.fits`
`/ifs/jwst/wit/niriss/tsohn/mirage_simulations/NIS-011/jw01086001001_01101_00045_nis_cal.fits`

Copy these two files to the same directory as the notebook.

The final output will be a delta flat file of FITS format, with a 2048x2048 image in the 1st data extension.
