# Azure Generate Blob Storage SAS URL

## Description

This tool generates a Shared Access Signature (SAS) URL for a given blob file within Azure Blob Storage.

It is designed to work on a single file at a time, making it ideal for scripting and batch processing.

## Usage

```sh
python generate-blob-sas-url.py <blobname>
```

Example:

```sh
python generate-blob-sas-url.py filename.dat
```

## Setup

### Prerequisites

- Python 3.10+
- A dedicated directory for this Git repository
- The following details from the Azure portal:
  - Storage Account Name
  - Storage Account Connection String
  - Storage Account Key
  - Container Name to look into

### Initial Setup

The following steps are required only for the first-time setup:

#### Configuration File

The tool requires a `config.json` file in the root of the Git repository, formatted as follows:

```json
{
  "storage_account_name": "<Azure storage account name>",
  "storage_account_connection_string": "<Azure storage account connection string>",
  "storage_account_key": "<Azure storage account key>",
  "container_name": "<Name of the container>"
}
```
For convenience, a file named `config-template.json` is present and can be copied for use.

1. Log in to the [Azure Portal](https://portal.azure.com/).
2. Navigate to the relevant storage account.
3. Under **Security + Networking > Access Keys**, locate and note the **Storage Account Name**.
4. On the same screen under **Key 1**, note the **Key** and **Connection String**.
5. Copy or rename `config-template.json` to `config.json`.
6. Edit `config.json` to include the values noted above.

#### Setting up a local environment
Open a terminal and execute the following commands
   ```sh
   cd <git repository directory>
   python3 -m venv .venv
   source ./.venv/bin/activate 
   pip install -r requirements.txt
   ```
#### Setting up a Docker container environment

**Note**: Before you begin - if you are behind a corporate firewall, you will need to ensure that the proxy is set up 
correctly to allow connections. Also ensure that you CA certificates chain is present as individual CRT files in a 
folder named `.certs` in the root folder of the repository

Open a terminal and execute the following commands
```sh
cd <git repository directory>
docker build -t azure-blob-sas-generator .
```

## Running the tool
**Important**: Ensure that your config.json file is correctly set up before running the container.

### Locally
Once setup is complete:

1. Open a terminal and navigate to the repository directory:
   ```sh
   cd <git repository directory>
   ```
2. Run the following command to generate a SAS URL:
   ```sh
   python generate-blob-sas-url.py my_blob_filename.dat
   ```
3. If the blob does not exist, an error message will be displayed.
4. If the blob exists, the SAS-enabled URL will be displayed.

**Tip:** To generate SAS URLs for multiple files, create a text file (`blobs.list`) with blob names and run:

```sh
cat blobs.list | xargs -I {} python generate-blob-sas-url.py {}
```

## With Docker
To run this tool within a Docker container:

1. . Open a terminal and navigate to the repository directory:
   ```sh
   cd <git repository directory>
   ```
2. Run the following command to generate a SAS URL:
   ```sh
   # docker run --rm -v $(pwd)/config.json:/app/config.json azure-blob-sas-generator <blobname>
   # For example
   docker run --rm -v $(pwd)/config.json:/app/config.json azure-blob-sas-generator python generate-blob-sas-url.py my_blob_filename.dat
   ```
3. If the blob does not exist, an error message will be displayed.
4. If the blob exists, the SAS-enabled URL will be displayed.