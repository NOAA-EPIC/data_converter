
<h1 align="center">
Data Converter to Zarr
</h1>

[Prerequisites](#Prerequisites) • [Quick Start](#Quick-Start) • [Environment Setup](#Environment-Setup) • [Status](#Status) • [What's Included](#What's-Included) • [Documentation](#Documentation) • [References](#Reference(s))
</h5>

# About

__Purpose:__

The purpose of this program is to convert NetCDF to Zarr data. The program will support the developers working on UFS-based applications.

# Table of Contents
* [Prerequisites](#Prerequisites)
* [Dataset](#Dataset)
* [Quick Start](#Quick-Start)
* [Environment Setup](#Environment-Setup)
* [Status](#Status)
* [What's Included](#What's-Included)
* [Documentation](#Documentation)
* [References](#Reference(s))

# Prerequisites
* Python 3.9
* Setting up conda environment w/in RDHPCS.
    * Refer to [Environment Setup](#Environment-Setup)

# Quick Start
1) Install miniconda per the "Environment Setup" section.
2) Create a conda environment based on the YAML file provided within this repository via executing the following command:

    * conda env create -f environment.yml
    
3) Activate the conda environment via executing the following command:

    * conda activate data_converter
    
4) Save the data in need of conversion under **/raw_data**. If an object needs to be download from Amazon Web Services (AWS) S3 storage, then execute the following command within your terminal:

   * python main_s3_download.py -b <bucket_arn> -k <key> -z <save_as_fn> 
   
      * <bucket_arn>: Cloud bucket's Amazon Resource Name (ARN). Options: 'noaa-ufs-regtests-pds', 'noaa-ufs-land-da-pds', 'noaa-ufs-srw-pds' 
      * <key>: Key of the object in cloud.
      * save_as_fn (str): Name to save downloaded file as on local disk.

Note: The object will be located under **/raw_data.**

5) Execute the following command to convert the netCDF data file to zarr.

   * python main_nc2zarr_converter.py -f <filename> -z <filename2save> -d <modifymultivars_if_applicable>

7) 

# Environment Setup:

* Install miniconda on your machine. Note: Miniconda is a smaller version of Anaconda that only includes conda along with a small set of necessary and useful packages. With Miniconda, you can install only what you need, without all the extra packages that Anaconda comes packaged with:
Download latest Miniconda (e.g. 3.9 version):

    * wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh

* Check integrity downloaded file with SHA-256:

    * sha256sum Miniconda3-py39_4.9.2-Linux-x86_64.sh

Reference SHA256 hash in following link: https://docs.conda.io/en/latest/miniconda.html

* Install Miniconda in Linux:

    * bash Miniconda3-py39_4.9.2-Linux-x86_64.sh

* Next, Miniconda installer will prompt where do you want to install Miniconda. Press ENTER to accept the default install location i.e. your $HOME directory. If you don't want to install in the default location, press CTRL+C to cancel the installation or mention an alternate installation directory. If you've chosen the default location, the installer will display “PREFIX=/var/home//miniconda3” and continue the installation.

* For installation to take into effect, run the following command:

source ~/.bashrc

* Next, you will see the prefix (base) in front of your terminal/shell prompt. Indicating the conda's base environment is activated.

* Once you have conda installed on your machine, perform the following to create a conda environment:

    * To create a new environment (if a YAML file is not provided)

        * conda create -n [Name of your conda environment you wish to create]

(OR)

    * To ensure you are running Python 3.9:

        * conda create -n myenv Python=3.9

(OR)

* To create a new environment from an existing YAML file (if a YAML file is provided):

    * conda env create -f environment.yml

*Note: A .yml file is a text file that contains a list of dependencies, which channels a list for installing dependencies for the given conda environment. For the code to utilize the dependencies, you will need to be in the directory where the environment.yml file lives.

### Activate the new environment via:

conda activate [Name of your conda environment you wish to activate]

* Verify that the new environment was installed correctly via:

    * conda info --env

*Note:

* From this point on, must activate conda environment prior to .py script(s) or jupyter notebooks execution using the following command: conda activate
    * To deactivate a conda environment:
        * conda deactivate

## Open & Run Application on Jupyter Notebook (Optional)

* Open OnDemand has a built-in file explorer and file transfer application available directly from its dashboard via:

    * Login to https://orion-ood.hpc.msstate.edu/

* In the Open OnDemand Interface, select Interactive Apps > Jupyter Notbook

### Additonal Information

To create a .yml file, execute the following commands:

* Activate the environment to export:

    * conda activate myenv

* Export your active environment to a new file:

    * conda env export > [ENVIRONMENT FILENAME].yml

# Status
[![Version badge](https://img.shields.io/badge/Python-3.9-blue.svg)](https://shields.io/)
[![Build badge](https://img.shields.io/badge/Build--gray.svg)](https://shields.io/)

# What's Included
Within the download, you will find the following directories and files:
* Demo:
    * 
* Scripts:
    * Modules:
        * .py
            * 
        *  .py
            *
        *  .py
            *   
    * Main:
        * .py
            * Main executable script for 
        * .py
            *  Main executable script for 

* List of Dependencies: 
    * data_converter.yml

# Documentation

# Version:
* Draft as of 
