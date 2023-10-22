from azure.storage.blob import generate_blob_sas, BlobSasPermissions, BlobClient
from datetime import datetime, timedelta
import sys
import json

# config file to use to read the settings from
CONFIG_FILE = "config.json"


def generate_sas(account_name, account_key, container_name, blob_name, expiry_time):
    """_Generate Shared Access Signature (SAS) enabled blob URL_

    Args:
        account_name (_str_): _Azure Blob storage account (assumed to exist)_
        account_key (_str_): _Blob storage account key_
        container_name (_str_): _Blob container name_
        blob_name (_str_): _blob name_
        expiry_time (_datetime_): _Expiry date time of the SAS_

    Returns:
        _str_: _A fully qualified SAS-enabled URL for the given blob_
    """
    permission = BlobSasPermissions(read=True)

    # Generate the SAS token using the generate_blob_sas function
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=account_key,
        container_name=container_name,
        blob_name=blob_name,
        expiry=expiry_time,
        permission=permission,
    )
    # Construct the SAS URL by appending the SAS token to the blob URL
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

    return sas_url


def blob_exists(connection_string, container_name, blob_name):
    """Check whether the given blobname exists in the specified container

    Args:
        connection_string (_str_): _Azure storage account connection string_
        container_name (_str_): _name of the container within the storage account_
        blob_name (_str_): _blob name_

    Returns:
        _boolean_: _indicating whether blob exists within the specified container and storage account_
    """
    blob = BlobClient.from_connection_string(
        conn_str=connection_string, container_name=container_name, blob_name=blob_name
    )
    return blob.exists()


def read_config(config_file_name):
    """_Load given config file into memory_

    Args:
        config_file_name (_str_): _config filename_

    Returns:
        _dict_: _Python object representing the config file_
    """
    try:
        with open(config_file_name, "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error reading config file: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in the config file ({config_file_name}): {e}")
        return None


def fetch_config_key(config, config_key):
    """_Read given key from the config file. Exit with error message if not found_

    Args:
        config (_dict_): _Python dict object representing the config file_
        config_key (_str_): _key name to retrieve from the config_

    Returns:
        _str_: _config value for the specified key_
    """
    config_value = config.get(config_key)
    if config_value is None:
        print(f"Error - {CONFIG_FILE} did not have a key named '{config_key}'")
        exit(1)
    return config_value


# Entry point
if __name__ == "__main__":
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
    storage_account_name = fetch_config_key(config, "storage_account_name")
    connect_str = fetch_config_key(config, "storage_account_connection_string")
    account_key = fetch_config_key(config, "storage_account_key")
    container_name = fetch_config_key(config, "container_name")

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
            expiry_time=expiry_time,
        )
        print(url)
    else:
        print(
            f"Error - blob named {blob_name} not found in the container '{container_name}'"
        )
