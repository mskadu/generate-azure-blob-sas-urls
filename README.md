# Azure Generate Blob Storage SAS URL

## Description

This tool generates a Shared Access Signature (SAS) URLs for a given blob file within Azure Blog storage.

This tool has been intentionally designed to work on a single file at time. This makes it amenable for use in scripting for mass usage.

## Usage

```
python generate-blob-sas-url.py <blobname>
```

for example,
```
python generate-blob-sas-url.py filename.dat
```

## Setup

### Pre-requisites:

- Python 3.10+
- This git repository in a dedicated directory 
- The following details from the Azure admin portal
    - Storage Account Name
    - Storage Account Connection String (from Azure account)
    - Storage Account Key (from Azure account)
    - Container name

### Setup 
The following steps are only necessary the first time this tool is set up

1. Open a terminal session and execute the following commands
```sh
cd <git repository directory>
pip install -r requirements.txt
```
2. In a new browser window, navigate to the [Azure Portal](https://portal.azure.com/) and login
3. Navigate to the relevant storage account 
4. Under Security + Networking --> Access Keys, locate and note value for the field _storage account name_.
5. Within the same screen for key 1, locate and note values for the fields _key_ and _connection string_
6. Copy/ rename 'config-template.json' to 'config.json'
7. Edit 'config.json' to add in the values noted above

### Configuration file
The tool requires a file named 'config.json' to be present in the root of the git repository. It's format is as follows

```json
{
"storage_account_name": "<Azure storage account name>",
"storage_account_connection_string": "<Azure storage account connection string>",
"storage_account_key": "<Azure storage account key>",
"container_name": "<Name of the container within the above storage account>" 
}
```

### Running the tool

Assuming you have already executed the setup process..

1. Open a terminal session and run the following command
```sh
cd <git repository directory>
```
2. To generate the SAS URL run the command 
```sh
python generate-blob-sas-url.py my_blob_filename
```
5. If the blob does not exist, an error message will be displayed
6. If the blob exists, the SAS-enabled URL will be displayed on the screen

*TIP:* To run this command for multiple files, create a text file listing the blob names. And execute the following command

```sh
cat blobs.list | xargs -I {} python generate-blob-sas-url.py {}
```
