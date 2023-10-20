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

- Python (developed on 3.10.xx)
- Poetry (developed on 1.6.1)
- This git repository in a dedicated directory 
- The following detail from the Azure admin portal
    - Storage Account Name
    - Storage Account Connection String (from Azure account)
    - Storage Account Key (from Azure account)
    - Container name

### Setup 
The following steps are only necessary the first time this tool is set up

1. Open a terminal session
2. cd `<git repository directory>`
3. Execute the command `poetry virtualenvs.in-project true`
4. Execute the command `poetry install`
5. If there are no errors displayed, execute the command `poetry shell`
6. In a new browser window, navigate to the [Azure Portal](https://portal.azure.com/) and login
7. Navigate to the relevant storage account 
8. Under Security + Networking --> Access Keys, locate and note value for the field _storage account name_.
9. Within the same screen for key 1, locate and note values for the fields _key_ and _connection string_
10. Copy/ rename 'config-template.json' to 'config.json'
11. Edit 'config.json' to add in the values noted above

### Configuration file
The tool requires a file named 'config.json' to be present in the root of the git repository. It's format is as follows

```
{
"storage_account_name": "<Azure storage account name>",
"storage_account_connection_string": "<Azure storage account connection string>",
"storage_account_key": "<Azure storage account key>",
"container_name": "<Name of the container within the above storage account>" 
}
```

### Running the tool

Note - Skip to step 4 to follow on from the setup process

1. Open a terminal session
2. cd `<git repository directory>`
3. Execute the command `poetry shell`
4. To generate the SAS URL run the command `python generate-blob-sas-url.py my_blob_filename`
5. If the blob does not exist, an error message will be displayed
6. If the blob exists, the SAS-enabled URL will be displayed on the screen

*TIP:* To run this command for multiple files, create a text file listing the blob names. And execute the following command

```
cat blobs.list | xargs -I {} python generate-blob-sas-url.py {}
```
