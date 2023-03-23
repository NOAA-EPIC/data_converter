import sys
sys.path.append( '../modules' )
from data_converter import DataConverter
import argparse

"""
********************
*** Description ***
********************

Load single netCDF as Xarray.

********************
* User Arguments. *
********************

filename(str): Name of the file of interest location of the raw (unprocessed) files (default: "../raw_data")
               Include file extension (e.g. .nc, .nc4).
               
filename2save(str): Name to save Zarr as under ../zarr_data.
            
refactor_variables (list): List of multidimensional variables for which will require refactoring in their 
                           naming convention. In some cases, a multidimensional data will require refactoring
                           specific multidimensional variables when using the Xarray package. This is due to Xarray's
                           restirction on duplicated variable names shared between coordinates & dimension variables. 
                           Xarray will not allow for these duplicated variable names as it conflicts to its
                           restriction. As a result, some netCDF files will require variable names
                           to be refactored. If a file does not feature duplication in variables, then set argument
                           to None. Default: None.
                   
********************************                  
*** BASH COMMAND TO EXECUTE: ***
********************************

python load_nc_data.py -f <filename> -d <refactor_variables_if_applicable>

"""

# User arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--filename", type=str, help="netCDF file of interest to convert to Xarray (include file's extension).")
argParser.add_argument("-d", "--refactorvars", type=str, nargs='+', help="Multidimensional variables in need of refactoring due to its duplication in variable. Reason: Xarray will not allow for duplicated variables & result in conflict to its restriction. For example, -d Disallowed Variable 1 Disallowed Variable 2 ... Disallowed Variable N.")
args = argParser.parse_args()

# Load single netCDF as Xarray.
dc_wrapper = DataConverter(args.filename, args.refactorvars)
data_xr = dc_wrapper.convert_nc2xarray()
