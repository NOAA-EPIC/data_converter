import sys
sys.path.append( '../modules' )
from download_data import DownloadData
import argparse

"""
********************
*** Description ***
********************

Download object from S3 cloud storage.

********************
* User Arguments. *
********************

bucket (str): Cloud bucket's Amazon Resource Name (ARN). 
              Options: 'noaa-ufs-regtests-pds', 'noaa-ufs-land-da-pds',
              'noaa-ufs-srw-pds'

key (str): Key of the object in cloud.

save_as_fn (str): Name to save object as file.
                   
********************************                  
*** BASH COMMAND TO EXECUTE: ***
********************************

python main_s3_download.py -b <bucket_arn> -k <key> -z <save_as_fn> 

******************************
*** BASH COMMAND EXAMPLES: ***
******************************

- For .nc, 

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/sfcf000.nc -z atm_sfcf000.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/sfcf024.nc -z sfcf024.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/rap_sfcdiff/sfcf000.nc -z rap_sfcf000.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/rap_sfcdiff/sfcf009.nc -z sfcf009.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k input-data-20221101/FV3_hafs_input_data/INPUT_hafs_regional_1nest_atm/C96_oro_data.tile7.halo4.nc -z C96_oro_data.tile7.halo4.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k BM_IC-20220207/2012010100/gfs_p7/C384_L127/INPUT/gfs_data.tile6.nc -z gfs_data.tile6.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k BM_IC-20220207/2012010100/gfs_p7/C384_L127/INPUT/gfs_data.tile1.nc -z gfs_data.tile1.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k BM_IC-20220207/2012010100/gfs_p7/C384_L127/INPUT/gfs_ctrl.nc -z gfs_ctrl.nc

- For .nc4, 

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/gocart.inst_aod.20210323_0600z.nc4 -z gocart.inst_aod.20210323_0600z.nc4

- For .nc (Matching Variable & Dim for Multi-Dimensional NCs),

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/RESTART/20210323.060000.fv_core.res.tile4.nc -z 20210323.060000.fv_core.res.tile4.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/RESTART/20210323.060000.phy_data.tile6.nc -z 20210323.060000.phy_data.tile6.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/control_CubedSphereGrid/sfcf024.tile6.nc -z sfcf024.tile6.nc

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/cpld_control_c96_noaero_p8/atmf024.tile4.nc -z atmf024.tile4.nc

- For .grb,

python main_s3_download.py -b noaa-ufs-regtests-pds -k input-data-20221101/FV3_regional_input_data/global_slmask.t1534.3072.1536.grb -z global_slmask.t1534.3072.1536.grb

python main_s3_download.py -b noaa-ufs-regtests-pds -k input-data-20221101/FV3_regional_input_data/global_snoclim.1.875.grb -z global_snoclim.1.875.grb

python main_s3_download.py -b noaa-ufs-regtests-pds -k input-data-20221101/FV3_regional_input_data/global_soilmgldas.t1534.3072.1536.grb -z global_soilmgldas.t1534.3072.1536.grb

python main_s3_download.py -b noaa-ufs-regtests-pds -k input-data-20221101/FV3_input_data768/global_snowfree_albedo.bosu.t1534.3072.1536.rg.grb -z global_snowfree_albedo.bosu.t1534.3072.1536.rg.grb

python main_s3_download.py -b noaa-ufs-regtests-pds -k input-data-20221101/FV3_input_data_L149/global_mxsnoalb.uariz.t126.384.190.rg.grb -z global_mxsnoalb.uariz.t126.384.190.rg.grb


- For .GrbF##,

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/GFSPRS.GrbF00 -z GFSPRS.GrbF00

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/atmaero_control_p8_rad/GFSPRS.GrbF24 -z GFSPRS.GrbF24

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/rap_sfcdiff/GFSFLX.GrbF00 -z GFSFLX.GrbF00

python main_s3_download.py -b noaa-ufs-regtests-pds -k develop-20230222/INTEL/rap_sfcdiff/GFSPRS.GrbF12 -z GFSPRS.GrbF12

"""

# User arguments.
argParser = argparse.ArgumentParser()
argParser.add_argument("-b", "--bucket", type=str, help="Bucket's Amazon Resource Name (ARN). Options: 'noaa-ufs-regtests-pds', 'noaa-ufs-land-da-pds', 'noaa-ufs-srw-pds', etc.")
argParser.add_argument("-k", "--key", type=str, help="Key of the object in cloud to download.")
argParser.add_argument("-z", "--save_as_fn", type=str, help="Save as filename of downloaded cloud object.")
args = argParser.parse_args()

# Download & save to default location of the raw files. Default: "../raw_data"
dl_wrapper = DownloadData(args.bucket, args.key, args.save_as_fn, csp_storage='s3')
