import dask.array as da
import zarr

class LoadZarrData():
    """

    Loads Zarr.

    Args:
        zarr_store (str): Name of the Zarr under the location of the 
                          zarr files (default: "../zarr_data"). 
                          
        variable (str): Variable of interest within Zarr.

    """
    def __init__(self, zarr_store, variable, zarr_dir="../zarr_data"):
        self.zarr_store = zarr_store
        self.variable = variable
        self.zarr_dir = zarr_dir

        
    def as_dask_array(self):
        """
        Load Zarr as Dask Array.
        
        Args:
            None
            
        Return (dask.array.Array): A parallel N dimensioned array comprised of many 
        numpy arrays arranged in a grid.
        
        """
        
        # Load zarr as a dask array
        dask_array = da.from_zarr(f"{self.zarr_dir}/{self.zarr_store}.zarr", 
                                  component=self.variable)
        
        return dask_array