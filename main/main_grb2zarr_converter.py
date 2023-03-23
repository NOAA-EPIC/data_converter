import sys
sys.path.append( '../modules' )
from data_converter import DataConverter
import argparse

"""
********************
*** Description ***
********************

Convert GRIB to Xarray & Zarr.

********************
* User Arguments. *
********************

filename(str): Name of the file of interest (e.g. filename.grb, filename.GrbF##) located under ../raw_data.

filename2save(str): Name to save Zarr as under ../zarr_data.            

grb_key (str): Unique GRIB's Xarray key of interest. In some cases, GRIB files (e.g. .Grbf##) may feature
               multiple values of a unique key per variable. This will require the user to filter
               the GRIB's Xarray by its unique key because Xarray package retricts representing a
               GRIB file that contains more than one hypercube of the same variable.

grb_val (str): Unique GRIB's Xarray value to the GRB key of interest. In some cases, GRIB files (e.g. .Grbf##) may feature
               multiple values of a unique key per variable. This will require the user to filter
               the GRIB's Xarray by its unique key-to-value pair because Xarray package retricts representing a
               GRIB file that contains more than one hypercube of the same variable.                                                                                    
********************************                  
*** BASH COMMAND TO EXECUTE: ***
********************************

python main_grb2zarr_converter.py -f <filename> -z <filename2save> -k <GRIB_KEY_1 GRIB_VALUE_2 ... GRIB_KEY_N_(if_applicable)> -v <GRIB_VALUE_1 GRIB_VALUE_2 ... GRIB_VALUE_N_(if_applicable)>

******************************
*** BASH COMMAND EXAMPLES: ***
******************************

- For .grb,

python main_grb2zarr_converter.py -f global_slmask.t1534.3072.1536.grb -z global_slmask.t1534.3072.1536

python main_grb2zarr_converter.py -f global_snoclim.1.875.grb -z global_snoclim.1.875

python main_grb2zarr_converter.py -f global_soilmgldas.t1534.3072.1536.grb -z global_soilmgldas.t1534.3072.1536

python main_grb2zarr_converter.py -f global_snowfree_albedo.bosu.t1534.3072.1536.rg.grb -z global_snowfree_albedo.bosu.t1534.3072.1536.rg

python main_grb2zarr_converter.py -f global_mxsnoalb.uariz.t126.384.190.rg.grb -z global_mxsnoalb.uariz.t126.384.190.rg

- For .GrbF##,

python main_grb2zarr_converter.py -f GFSPRS.GrbF24 -z GFSPRS.GrbF24 -k typeOfLevel -v highCloudTop
python main_grb2zarr_converter.py -f GFSPRS.GrbF24 -z GFSPRS.GrbF24 -k typeOfLevel -v middleCloudTop
python main_grb2zarr_converter.py -f GFSPRS.GrbF24 -z GFSPRS.GrbF24 -k typeOfLevel -v sigmaLayer
python main_grb2zarr_converter.py -f GFSPRS.GrbF24 -z GFSPRS.GrbF24 -k typeOfLevel -v maxWind

python main_grb2zarr_converter.py -f GFSFLX.GrbF00 -z GFSFLX.GrbF00 -k typeOfLevel -v surface
python main_grb2zarr_converter.py -f GFSFLX.GrbF00 -z GFSFLX.GrbF00 -k typeOfLevel -v convectiveCloudLayer
python main_grb2zarr_converter.py -f GFSFLX.GrbF00 -z GFSFLX.GrbF00 -k typeOfLevel shortName -v depthBelowLandLayer sm

python main_grb2zarr_converter.py -f GFSPRS.GrbF12 -z GFSPRS.GrbF12 -k typeOfLevel -v meanSea
python main_grb2zarr_converter.py -f GFSPRS.GrbF12 -z GFSPRS.GrbF12 -k typeOfLevel -v sigmaLayer
python main_grb2zarr_converter.py -f GFSPRS.GrbF12 -z GFSPRS.GrbF12 -k typeOfLevel -v potentialVorticity
python main_grb2zarr_converter.py -f GFSPRS.GrbF12 -z GFSPRS.GrbF12 -k typeOfLevel -v maxWind

python main_grb2zarr_converter.py -f GFSPRS.GrbF00 -z GFSPRS.GrbF00 -k typeOfLevel shortName -v heightAboveGround v
python main_grb2zarr_converter.py -f GFSPRS.GrbF00 -z GFSPRS.GrbF00 -k typeOfLevel shortName -v hybrid refd
python main_grb2zarr_converter.py -f GFSPRS.GrbF00 -z GFSPRS.GrbF00 -k typeOfLevel -v potentialVorticity
python main_grb2zarr_converter.py -f GFSPRS.GrbF00 -z GFSPRS.GrbF00 -k typeOfLevel -v surface

References:
- https://github.com/ecmwf/cfgrib/issues/2
- https://github.com/ecmwf/cfgrib/issues/263
- https://github.com/ecmwf/cfgrib/issues/285

"""

# User arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-f", "--filename", type=str, help="GRIB file of interest to convert to Zarr (include file's extension).")
argParser.add_argument("-k", "--grb_key", type=str, nargs='+', help="Unique GRIB key of interest.")
argParser.add_argument("-v", "--grb_val", type=str, nargs='+', help="GRIB value corresponding to unique GRIB key of interest.")
argParser.add_argument("-z", "--filename2save", type=str, help="Save as Zarr name.")
args = argParser.parse_args()

# Convert single .GrbF## file of interest & save to default location (../zarr_data).
dc_wrapper = DataConverter(args.filename, None)

if args.grb_key!=None and args.grb_val!=None:
    data_zarr = dc_wrapper.convert_grb2zarr(args.filename2save, dict(zip(args.grb_key, args.grb_val)))
else:
    data_zarr = dc_wrapper.convert_grb2zarr(args.filename2save, dict())

