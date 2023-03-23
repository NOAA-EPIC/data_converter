import os
import time
import boto3

class DownloadData():
    """

    Downloads object from S3 cloud storage.

    """
    def __init__(self, bucket_arn, obj_key, save_as_fn, raw_data_dir="../raw_data", csp_storage='s3'):
        """
        Args:
            bucket_arn (str): Cloud bucket's Amazon Resource Name (ARN). 
                              Options: 'noaa-ufs-regtests-pds', 'noaa-ufs-land-da-pds',
                              'noaa-ufs-srw-pds'
            
            obj_key (str): Key of the object in cloud storage.
            
            save_as_fn (str): Name to save downloaded file as on local disk.
            
            raw_data_dir (str): Directory to save downloaded file. 
                                Default: "../raw_data"
                                
            csp_storage (str): Cloud service providers storage name. 
                               Default is 's3'
        
        """
        self.bucket_arn = bucket_arn
        self.obj_key = obj_key
        self.save_as_fn = save_as_fn
        self.csp_storage = csp_storage
        self.boto_client = boto3.client(self.csp_storage)
        self.raw_data_dir = raw_data_dir
        
        # Create directory for storing raw files
        try:
            os.makedirs(self.raw_data_dir)
        except FileExistsError:
            pass
        
        # Download file from cloud storage
        start_t = time.time()
        try:
            self.boto_client.download_file(Bucket=self.bucket_arn, 
                                           Key=self.obj_key, 
                                           Filename=f"{self.raw_data_dir}/{self.save_as_fn}")
            
            # Calculate processing time.
            print(f"\nThe following cloud object has been downloaded to {self.raw_data_dir} as {self.save_as_fn}:\n{self.obj_key}")
            delta_t = (time.time()-start_t)/60
            print(f"\nProcessing time: {delta_t} min.\n")

        # If object's key doest not exist within the ARN of interest, then a notification will be sent
        except Exception as e: 
            print(f"\nThe following cloud key does not exist in {bucket_arn} bucket:\n{self.obj_key}\n")
            

