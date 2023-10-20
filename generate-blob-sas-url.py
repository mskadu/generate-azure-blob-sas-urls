from azure.storage.blob import (
    generate_blob_sas,
    BlobSasPermissions,
    BlobClient
)
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import sys, os
import configparser
import json

# config file to use to read the settings from
CONFIG_FILE = 'config.json'

# Function to generate Shared Access Signature (SAS) enabled
# blob URL
# args - 
#   blob_name - name of the blob (assumed to exist)
#   account_key - Storage account key (Azure)
# returns - 
#   SAS-enabled URL to the given blob
# 
def generate_sas(account_name, account_key, container_name, blob_name, expiry_time):
    
    permission = BlobSasPermissions(read=True)
    
    # Generate the SAS token using the generate_blob_sas function
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        expiry=expiry_time,
        permission=permission
    )
    # Construct the SAS URL by appending the SAS token to the blob URL
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"
        
    return sas_url

#  Function to check whether a given blobname exists
#  args:
#       blob_name - name of the blob to check
#       connection_string - Storage Connection String (Azure)
#       container_name - name of the container within the Storage
#  returns:
#       boolean value to indicate whether the blob was found
# 
def blob_exists(connection_string, container_name, blob_name):
    blob = BlobClient.from_connection_string(
        conn_str=connection_string, 
        container_name=container_name, 
        blob_name=blob_name
    )
    return blob.exists()

# function to load the given config file in memory.
# args:
#   config_file_name - name of the config file (can include path)
# errors:
#   File not found - config file could not be found or read
#   JSONDecodeError - the file could be read but the json within was invalid
# returns:
#   file object representing the json config file
#
def read_config(config_file_name):
    try:
        with open(config_file_name, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
         print(f"Error reading config file: {e}")
         return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in the config file ({config_file_name}): {e}")
        return None

# function to read the given key in the configution file
# args:
#   config - file object for the json config file
#   config_key - the key to read from the config file
# errors:
#   will print error message to STDOUT if config_key cannot be found
# returns:
#   - value of the config_key
#   - None if the config_key cannot be found in the config file
#
def fetch_config_key( config, config_key ):
    config_value = config.get(config_key)            
    if config_value is None:
        print(f"Error - {CONFIG_FILE} did not have a key named '{config_key}'")
        exit(1)
    return config_value
    
# Entry point
if __name__ == '__main__':

    # the first argument is mandatory
    args_count = len(sys.argv)
    if args_count == 1:
        print("Error - no arguments passed")
        exit(1) 
    
    # load config file
    config = read_config(CONFIG_FILE)    
    if not config:
        exit(1)
        
    # read configuration
    storage_account_name = fetch_config_key( config, 'storage_account_name')
    connect_str = fetch_config_key(config,'storage_account_connection_string')                   
    account_key = fetch_config_key(config,'storage_account_key')
    container_name = fetch_config_key(config, 'container_name')
    
    # Define the expiry time for the SAS
    expiry_time = datetime.utcnow() + timedelta(days=30)

    blob_name = sys.argv[1]
    # check if blob exists in the specified container within the storage account
    if blob_exists(connect_str, container_name, blob_name):
        # generate and print the SAS
        url = generate_sas(
                    account_name=storage_account_name,
                    account_key=account_key,
                    container_name=container_name,
                    blob_name=blob_name,
                    expiry_time=expiry_time
                )
        print(url)
    else:
        print(f"Error - blob named {blob_name} not found in the container '{container_name}'")
            