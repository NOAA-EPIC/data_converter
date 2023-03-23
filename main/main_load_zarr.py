import sys
sys.path.append( '../modules' )
from load_zarr_data import LoadZarrData
import argparse
import time

"""
********************
*** Description ***
********************

Loads Zarr as Dask Array.

********************
* User Arguments. *
********************

zarr_store (str): Name of the Zarr under the location of the 
                  zarr files (default: "../zarr_data"). 

variable (str): Variable of interest within Zarr.
                   
********************************                  
*** BASH COMMAND TO EXECUTE: ***
********************************

python main_load_zarr.py -z <zarr_store> -v <variable> 

"""

# User arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-z",  "--zarr_store", type=str, help="Zarr name (exclude .zarr extension).")
argParser.add_argument("-v", "--variable", type=str, help="Zarr's variable of interest.")
args = argParser.parse_args()

# Loads Zarr as Dask Array.
start_t = time.time()
load_wrapper = LoadZarrData(args.zarr_store, args.variable)
dask_array = load_wrapper.as_dask_array()
print(dask_array)

# Calculalate processing time.
delta_t = (time.time()-start_t)/60
print(f"\nProcessing time: {delta_t} min.")