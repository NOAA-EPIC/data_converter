import os
import xarray as xr
from netCDF4 import Dataset
import warnings
warnings.filterwarnings("ignore")

class Zarr2NC():
    """
    
    Convert Zarr to netCDF. 
    
    """
    def __init__(self, zarr_data_dir="../zarr_data", nc_data_dir="../nc_data"):
        """
        Args:
            zarr_data_dir (str):  Directory path of the Zarr.

            nc_data_dir (str): Directory path for the newly converted netCDF file.
            
        """
        
        # Create directory for storing newly converted netCDF files.
        self.nc_data_dir = nc_data_dir
        self.zarr_data_dir = zarr_data_dir
        try:
            os.makedirs(self.nc_data_dir)
        except FileExistsError:
            pass

    def convert_zarr2nc(self, zarr_store, combine_by="by_coords"):
        """
        Convert Zarr to netCDF.
        
        Args:
            zarr_store (str): Name of the zarr (exclude extension).
            
            combine_by (str): Method for combining data within Zarr.
                              Options: "nested" or "by_coords"

        Return: None

        References:
        - https://xarray.pydata.org/en/v0.14.0/generated/xarray.open_mfdataset.html
        
        """
        
        try:
            
            # Load Zarr as Xarray Dataset.
            xr_dataset = xr.open_mfdataset(f'{self.zarr_data_dir}/{zarr_store}.zarr',
                                           combine=combine_by)

            # Convert Xarray Dataset to netCDF.
            xr_dataset.to_netcdf(f"{self.nc_data_dir}/{zarr_store}.nc")
            print(f"\nThe newly converted netCDF has been saved under {self.nc_data_dir}/{zarr_store}.nc") 
            
        except Exception:
            pass

        return
    

        