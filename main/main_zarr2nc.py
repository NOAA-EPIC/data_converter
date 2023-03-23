import sys
sys.path.append( '../modules' )
from zarr2nc import Zarr2NC
import argparse
import time

"""
********************
*** Description ***
********************

Convert Zarr to netCDF.

********************
* User Arguments. *
********************

zarr_store (str): Name of the Zarr store.

combine_by (str): Method to combine all data within Zarr. 
                  Some options: "nested" or "by_coords"

zarr_data_dir (str):  Directory path of the Zarr. Default: "../zarr_data"

nc_data_dir (str): Directory path for the newly converted netCDF file. Default: "../nc_data"
                   
********************************                  
*** BASH COMMAND TO EXECUTE: ***
********************************

python main_zarr2nc.py -z <zarr_store> -c <combine_by> 

"""

# User arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-z", "--zarr_store",  type=str, help="Zarr name (exclude .zarr extension).")
argParser.add_argument("-c", "--combine_by",  type=str, help="Way to combine the Zarr. Options: 'nested' or 'by_coords' to combine all data within Zarr.")
args = argParser.parse_args()

# Convert Zarr to netCDF & save to default location of the netCDF files. Default: "../nc_data"
start_t = time.time()
zarr2nc_wrapper = Zarr2NC()
zarr2nc_wrapper.convert_zarr2nc(args.zarr_store, args.combine_by)


# Calculalate processing time.
delta_t = (time.time()-start_t)/60
print(f"\nProcessing time: {delta_t} min.\n")