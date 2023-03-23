import os
import time
import xarray as xr
from netCDF4 import Dataset

class DataConverter():
    """
    
    Converts netCDF & GRIB to Xarray & Zarr.
    
    """
    def __init__(self, filename, refactor_variables=None, raw_data_dir="../raw_data", zarr_data_dir="../zarr_data"):
        """
        Args:
            filename(str): Name of the file of interest located under ../raw_data. 
                           Include file extension (e.g. .nc, .nc4).
            
            refactor_variables (list): List of multidimensional variables for which will require refactoring in their 
                                       naming convention. In some cases, a multidimensional data will require refactoring
                                       specific multidimensional variables when using the Xarray package. This is due to Xarray's
                                       restirction on duplicated variable names shared between coordinates & dimension variables. 
                                       Xarray will not allow for these duplicated variable names as it conflicts to its
                                       restriction. As a result, some netCDF files will require variable names
                                       to be refactored. If a file does not feature duplication in variables, then set argument
                                       to None. Default: None
                                   
            raw_data_dir (str): Location of the raw (unprocessed) files. Default: "../raw_data"
            
            zarr_data_dir (str): Location of the zarr files. Default: "../zarr_data"
                                   
        """
        self.filename = filename
        self.refactor_variables = refactor_variables
        self.raw_data_dir = raw_data_dir
        self.zarr_data_dir = zarr_data_dir
        
        # Create directory for storing zarr
        try:
            os.makedirs(self.zarr_data_dir)
        except FileExistsError:
            pass
        
    def convert_nc2xarray(self, coord_suffix="coord", dim_suffix="node", print_feats=False):
        """
        Converts netCDF to Xarray.
        
        Args:
            coord_suffix (str): Suffix name for the refactored coordinate variable(s).
                                Default: "coord"
                                
            dim_suffix (str):  Suffix name for the refactored dimension variable(s).
                               Default: "node"
                               
            print_feats (bool): Print raw (unprocessed) data's details to prompted screen.

        Return (object): NetCDF file's Xarray object. The object is a dataset resembling an in-memory representation of the
        netCDF file. It consists of the data's variables, coordinates, & attributes to form a self-describing dataset.
        
        References: 
        - https://docs.xarray.dev/en/stable/user-guide/io.html
        - https://github.com/pydata/xarray/issues/4456
        
        """
        start_t = time.time()
        data_xr = None
        try:
            # For index refactoring cases, preprocessing is required
            if self.refactor_variables:
                
                # load raw (unprocessed) data as Xarray Dataset via Xarray package
                # & drop duplicated variable names in need of refactoring.
                data_xr = xr.open_dataset(f'{self.raw_data_dir}/{self.filename}', drop_variables=self.refactor_variables, decode_times=False)

                # load raw (unprocessed) data as nc Dataset via netCDF4 package
                nc = Dataset(f'{self.raw_data_dir}/{self.filename}')

                # Extract the "problematic" coordinate variables in need of refactoring.
                coords = {name:nc[name] for name in self.refactor_variables}

                # Load the "problematic" coordinate variables & create function to
                # extract the "problematic" coordinate variables' attributes from "Dataset"
                get_attrs = lambda name: {attr:coords[name].getncattr(attr) for attr in coords[name].ncattrs()}

                # Create function to convert from nc Dataset() to Xarray DataArray w/ the 
                # coordinate & dimension variables refactored.
                nc2xr = lambda name: xr.DataArray(coords[name], attrs=get_attrs(name), name=f'{name}_{coord_suffix}', dims=(name, dim_suffix))

                # Merge coordinate & dimension variables-refactored Xarray objects
                coords = xr.merge([nc2xr(name) for name in coords.keys()])

                # Re-assign the refactored coordinate & dimension variables to the
                # raw data's Xarray Dataset
                data_xr = data_xr.assign_coords(coords)  
                
            # For non-index refactoring cases
            if not self.refactor_variables:

                # Convert netCDF to Xarray
                data_xr = xr.load_dataset(f'{self.raw_data_dir}/{self.filename}')
            
            # Calculate processing time
            print("\nData Converted to Xarray ... Completed.")
            delta_t = (time.time()-start_t)/60
            print(f"Xarray Conversion Processing Time: {delta_t} min.")
            
            # Print raw (unprocessed) data's information. 
            if print_feats:
                self.print_attributes(data_xr)
        
            
        # If the netCDF file requires data refactoring & the user does not declare
        # the variables in need of refactoring, then a notification will be sent
        except Exception as e:
            error_mssg = f"\n* XARRAY NOTIFICATION:\n{e}\n\n* Note: Variables with the same name as its dimensions are disallowed by Xarray because they conflict with the coordinates used to label dimensions.\n*TO RESOLVE: Re-execute script with the following flag appended: -d <DISALLOWED_VAR_1 DISALLOWED_VAR_2 ... DISALLOWED_VAR_N>\n"
            print(error_mssg)
            
        return data_xr

    def convert_nc2zarr(self, filename):
        """
        Convert netCDF to Zarr. 
                
        Args:
            filename (str): Name to save Zarr as under the location
                           of the zarr files (default: "../zarr_data").
        
        Return: If Xarray is not empty, then Zarr will be saved under the location
        of the Zarr files (default: "../zarr_data") -- otherwise, Zarr will not be saved 
        because it is empty due to an empty Xarray.
        
        """
        
        # Convert netCDF to Xarray
        data_xr = self.convert_nc2xarray()

        # Convert Xarray to Zarr
        start_t = time.time()
        if data_xr!=None:
            try:
                data_zarr = data_xr.to_zarr(store=f'{self.zarr_data_dir}/{filename}.zarr')     
                print("\nData Converted to Zarr ... Completed.")
                
                # Calculate processing time.
                delta_t2 = (time.time()-start_t)/60
                print(f"Zarr Conversion Processing Time: {delta_t2} min.\n")
                
                return data_zarr
            
            # If a user saves Zarr with the name of an existing Zarr, then a notification will be sent.
            # Note: This prevents an exisiting Zarr from being overwritten.
            except Exception as e: 
                print(f"\nData Not Converted to Zarr. REASON: The following Zarr currently exist: {self.zarr_data_dir}/{filename}.zarr.\n*TO RESOLVE: Either remove existing {filename}.zarr within {self.zarr_data_dir} (OR) save newly converted Zarr under a different name. For example, execute command in the following format:\npython main_nc2zarr_converter -f <FILENAME_WITH_EXTENSION> -z <NEW_FILENAME_FOR_ZARR_WHICH_DOES_NOT_EXIST> -d <DISALLOWED_VAR_1 DISALLOWED_VAR_2 ... DISALLOWED_VAR_N (OR) None>\n")
                
        # If Xarray is empty, then conversion to Zarr will not occur & a notification will be sent
        else:
            print('\nConversion to Zarr will not occur because Xarray is empty.\n')
            
        return
    
    def convert_grb2xarray(self, grb_dict={}, print_feats=False):
        """
        Converts GRIB to Xarray.
        
        Args:
            grib_dict (dict): Dictionary to filter GRIB's Xarray by its key.
                              In some cases, GRIB files (e.g. .GrbF##) may feature multiple values 
                              of a unique key per variable. This will require the 
                              user to filter the GRIB's Xarray by its unique key because
                              Xarray package retricts representing a GRIB file that contains more 
                              than one hypercube of the same variable.
            
            print_feats (bool): Print data's information to prompted screen.


        Return (object): GRIB file's Xarray object. The object is a dataset resembling an in-memory representation of the
        netCDF file. It consists of the data's variables, coordinates, & attributes to form a self-describing dataset.
        
        References: 
        - https://github.com/ecmwf/cfgrib/issues/2
        
        """
        start_t = time.time()
        data_xr = None   
        try:

            # Convert GRIB to Xarray           
            data_xr = xr.load_dataset(f'{self.raw_data_dir}/{self.filename}',
                                      engine='cfgrib',
                                      backend_kwargs={'filter_by_keys': grb_dict}) 
            
            # Print filtered GRIB's data features
            if print_feats:
                self.print_attributes(data_xr)

            # Ensure GRIB's Xarray contains variables
            if len(data_xr.keys())!=0:
                print("\nData Converted to Xarray ... Completed.")
                
                # Calculate processing time.
                delta_t = (time.time()-start_t)/60
                print(f"Xarray Conversion Processing Time: {delta_t} min.")
        
            else:
                print("\nData Not Converted to Xarray because the data's unique key(s) has to be specified by the user.")
    
        except Exception as e:
            error_mssg = f"\n* XARRAY NOTIFICATION:\n {e}.\n\nThe GRIB file features a unique key with multiple values. For the conversion to Xarray, the user must request for a unique key-value pair of the GRIB file.\n*TO RESOLVE: Re-execute script with the following  -k & -v flags appended: -k <GRIB_KEY_1 GRIB_VALUE_2 ... GRIB_KEY_N> -v <GRIB_VALUE_1 GRIB_VALUE_2 ... GRIB_VALUE_N>\n"
            print(error_mssg)
            
        return data_xr
        
    def convert_grb2zarr(self, filename, grb_dict={}):
        """
        Convert GRIB (.Grb### or .grb) to Zarr.
                
            filename (str): Name to save Zarr as under the location
                           of the zarr files (default: "../zarr_data").
        
        Return: If Xarray is not empty, then Zarr will be saved under the location
        of the Zarr files (default: "../zarr_data") -- otherwise, Zarr will not be saved 
        because it is empty due to an empty Xarray.
        
        """        

        # Convert GRIB (.Grb### or .grb) to Xarray
        data_xr = self.convert_grb2xarray(grb_dict)
        
        # Convert Xarray to Zarr
        start_t = time.time()
        kv_txt = []
        if data_xr!=None:
            try:
                # For GRIB files not featuring a unique key with multiple values cases
                if grb_dict=={}:
                    data_zarr = data_xr.to_zarr(store=f'{self.zarr_data_dir}/{filename}.zarr')#, mode='w')
                else:
                    # For GRIB file featuring a unique key with multiple values cases
                    for k,v in grb_dict.items():
                        kv_txt.append(f'{k}{v}')
                        combine_kv = '_'.join(kv_txt)
                        
                    # Save Zarr's name with appending unique keys & values
                    data_zarr = data_xr.to_zarr(store=f'{self.zarr_data_dir}/{filename}_{combine_kv}.zarr')#, mode='w')
                
                # Calculate processing time
                delta_t2 = (time.time()-start_t)/60
                print("\nData Converted to Zarr ... Completed.")
                print(f"Zarr Conversion Processing Time: {delta_t2} min.\n")
                
                return data_zarr
            
            # If a user saves Zarr with the name of an existing Zarr, then a notification will be sent.
            # Note: This prevents an exisiting Zarr from being overwritten.
            except Exception as e: 
                print(f"\nData Not Converted to Zarr. REASON: The following Zarr currently exist: {self.zarr_data_dir}/{filename}.zarr.\n*TO RESOLVE: Either remove existing {filename}.zarr within {self.zarr_data_dir} (OR) save newly converted Zarr under a different name. For example, execute command in the following format:\npython main_nc2zarr_converter -f <FILENAME_WITH_EXTENSION> -z <NEW_FILENAME_FOR_ZARR_WHICH_DOES_NOT_EXIST> -k <GRIB_KEY_1 GRIB_VALUE_2 ... GRIB_KEY_N> -v <GRIB_VALUE_1 GRIB_VALUE_2 ... GRIB_VALUE_N>\n")
        
        # If Xarray is empty, then conversion to Zarr will not occur & a notification will be sent
        else:
            print('\nConversion to Zarr will not occur because Xarray is empty.\n')

        return
    
    def print_attributes(self, data_xr):
        """
        Prints data's attributes.
        
        Args:
            data_xr (DataArray): Xarray 
        
        Return: None
        
        """
        
        # Extract coordinate variable(s)
        print("\n== Coordinate Variable(s) & Their Corresponding Dimension Variable(s) ==\n")
        for c in data_xr.coords.values():
            print(f'- {c.name}  {c.dims}') 

        # Extract dimension variable(s)
        print("\n== Dimension Variable(s) to Their Correwsponding Length ==\n\n", data_xr.dims)

        # Extract data variable names & their dimension from the raw file
        print("\n== Data Variable(s) & Their Corresponding Dimension Variable(s) ==\n")
        for v in data_xr.data_vars.values():
            print(f'- {v.name}  {v.dims}') 
            
        return