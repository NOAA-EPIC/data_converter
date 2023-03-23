import sys
sys.path.append( '../modules' )
from data_converter import DataConverter
import argparse

"""
********************
*** Description ***
********************

Convert netCDF to Xarray & Zarr.

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

python main_nc2zarr_converter.py -f <filename> -z <filename2save> -d <refactor_variables_if_applicable>

******************************
*** BASH COMMAND EXAMPLES: ***
******************************

- For .nc, 

python main_nc2zarr_converter.py -f sfcf024.nc -z sfcf024

python main_nc2zarr_converter.py -f atm_sfcf000.nc -z atm_sfcf000

python main_nc2zarr_converter.py -f rap_sfcf000.nc -z rap_sfcf000

python main_nc2zarr_converter.py -f sfcf009.nc -z sfcf009

python main_nc2zarr_converter.py -f C96_oro_data.tile7.halo4.nc -z C96_oro_data.tile7.halo4

python main_nc2zarr_converter.py -f gfs_data.tile6.nc -z gfs_data.tile6

python main_nc2zarr_converter.py -f gfs_data.tile1.nc -z gfs_data.tile1

python main_nc2zarr_converter.py -f gfs_ctrl.nc -z gfs_ctrl

- For .nc4, 

python main_nc2zarr_converter.py -f gocart.inst_aod.20210323_0600z.nc4 -z gocart.inst_aod.20210323_0600z

- For .nc (Matching Variable & Dim for Multi-Dimensional NCs),

python main_nc2zarr_converter.py -f 20210323.060000.fv_core.res.tile4.nc -z 20210323.060000.fv_core.res.tile4

python main_nc2zarr_converter.py -f 20210323.060000.phy_data.tile6.nc -z 20210323.060000.phy_data.tile6

python main_nc2zarr_converter.py -f sfcf024.tile6.nc -z sfcf024.tile6 -d grid_xt grid_yt

python main_nc2zarr_converter.py -f atmf024.tile4.nc -z atmf024.tile4 -d grid_xt grid_yt

"""

# User arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--filename", type=str, help="netCDF file to convert to Zarr. Include file extension (e.g. .nc, .nc4).")
argParser.add_argument("-z", "--filename2save", type=str, help="Save as Zarr name.")
argParser.add_argument("-d", "--refactorvars", type=str, nargs='+', help="Multi-dimension variables in need of refactoring due to its duplication in variable. Reason: Xarray will not allow for duplicated variables and will result in conflicts to its restriction. For example, -d Disallowed Variable 1 Disallowed Variable 2 ... Disallowed Variable N")
args = argParser.parse_args()

# Convert single netCDF file of interest & save to default location of the zarr files. Default: "../zarr_data"
dc_wrapper = DataConverter(args.filename, args.refactorvars)
data_zarr = dc_wrapper.convert_nc2zarr(args.filename2save)
