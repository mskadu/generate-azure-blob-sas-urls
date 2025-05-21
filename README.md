# Azure Generate Blob Storage SAS URL

## Description

This tool generates a Shared Access Signature (SAS) URL for a given blob file within Azure Blob Storage.

It is designed to work on a single file at a time, making it ideal for scripting and batch processing.

## Overview
This script, `generate-blob-sas-url.py`, provides a command-line interface to generate a Shared Access Signature (SAS) URL for a specified blob in Azure Blob Storage. It reads Azure Storage account details from a `config.json` file, checks if the target blob exists, and then generates a SAS URL with read-only permissions, valid for 30 days. The script is designed for ease of use in generating SAS URLs for individual files and can be integrated into scripting workflows. It also includes support for custom SSL certificates via the `truststore` library, which is particularly useful in corporate environments with specific CA requirements, especially when using the provided Dockerfile.

## How it Works

The `generate-blob-sas-url.py` script performs the following steps to generate a SAS URL:

1.  **Argument Parsing:** It first parses command-line arguments to get the mandatory blob filename and the optional path to the `config.json` file.
2.  **Configuration Loading:** The script reads the Azure Storage account details (account name, connection string, account key, and container name) from the `config.json` file.
3.  **`truststore` Initialization:** Early in its execution, the script calls `truststore.inject_into_ssl()`. This allows the Python SSL context to use custom CA certificates, which is particularly important for users in corporate environments with SSL inspection or custom CAs. For Docker deployments, these custom CAs can be provided via the `.certs` directory during the image build.
4.  **Blob Existence Check:** Using the `storage_account_connection_string` and `container_name`, it utilizes the `azure-storage-blob` library to verify if the specified blob actually exists within the given container. If not, it exits with an error.
5.  **SAS Token Generation:** If the blob exists, the script generates a SAS token. This token is created with:
    *   Read-only permissions (`BlobSasPermissions(read=True)`).
    *   An expiry time set to 30 days from the current time.
    *   The `storage_account_name`, `storage_account_key`, `container_name`, and `blob_name`.
6.  **SAS URL Construction:** Finally, it constructs the full SAS-enabled URL for the blob by appending the generated SAS token to the standard blob URL format (`https://<account_name>.blob.core.windows.net/<container_name>/<blob_name>`).
7.  **Output:** The script prints the generated SAS URL to the standard output.

This process allows for a secure and straightforward way to grant temporary, read-only access to specific blobs.

## Setup

### Prerequisites

- Python 3.10+
- `pip` (Python package installer) to install dependencies from `requirements.txt`.
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

**Why these values are needed:**
*   `storage_account_name`: Used by the script to construct the full URL endpoint for the blob and required by the Azure SDK.
*   `storage_account_connection_string`: Used by the `azure-storage-blob` library to authenticate and connect to your Azure Storage account, primarily for checking if the specified blob exists.
*   `storage_account_key`: Used by the `azure-storage-blob` library to generate the Shared Access Signature (SAS) token.
*   `container_name`: Specifies the container within your Azure Storage account where the script will look for the blob.

For convenience, a file named `config-template.json` is present and can be copied for use.

1. Log in to the [Azure Portal](https://portal.azure.com/).
2. Navigate to the relevant storage account.
3. Under **Security + Networking > Access Keys**, locate and note the **Storage Account Name**.
4. On the same screen under **Key 1**, note the **Key** and **Connection String**.
5. Copy or rename `config-template.json` to `config.json`.
6. Edit `config.json` to include the values noted above.

### Dependencies
This project uses specific Python libraries, listed in `requirements.txt`. These are installed automatically when setting up the local or Docker environment.
*   `azure-storage-blob`: The official Microsoft Azure Storage SDK for Python. It's used to interact with Azure Blob Storage for operations like checking if a blob exists and generating the SAS token.
*   `truststore`: A library to inject custom certificate authorities (CAs) into Python's SSL context. This is particularly useful for users in corporate environments that might use custom SSL certificates or proxies.

#### Setting up a local environment
Open a terminal and execute the following commands
   ```sh
   cd <git repository directory>
   python3 -m venv .venv
   source ./.venv/bin/activate 
   pip install -r requirements.txt
   ```
#### Building the Docker Image

Open a terminal and execute the following commands
```sh
cd <git repository directory>
docker build -t azure-blob-sas-generator .
```

#### Corporate Firewalls and Custom Certificates
If you are operating behind a corporate firewall or in an environment that uses custom SSL/TLS certificates, you may need to take extra steps for the Docker container to connect to Azure services and for Python's SSL verification to work correctly.

**Custom CA Certificates for Docker:**
The `Dockerfile` is configured to look for a directory named `.certs` in the root of this repository.
1.  Create a directory named `.certs` in the root of this repository (if it doesn't exist).
2.  Place your organization's CA certificate chain files into this `.certs` directory. Each certificate should be in its own file, typically with a `.crt` extension (e.g., `intermediate.crt`, `root.crt`).
3.  When you build the Docker image (`docker build ...`), these certificates will be copied into the image and added to the system's trusted certificate store.

**Python `truststore` Integration:**
The Python script `generate-blob-sas-url.py` uses the `truststore` library. This library is initialized at the beginning of the script (`truststore.inject_into_ssl()`) and helps Python's SSL context recognize these custom CA certificates that have been added to the Docker image's trust store. This allows for successful HTTPS connections to Azure services even when custom CAs are in use.

**Proxy Configuration:**
If you are behind a proxy, ensure your Docker environment is configured to use this proxy. This might involve setting `http_proxy` and `https_proxy` environment variables when building the image or running the container, or configuring Docker's global proxy settings. Consult your Docker documentation or IT department for specific instructions on proxy configuration.

## Usage

```sh
python generate-blob-sas-url.py <blob_filename>
```

Example:

```sh
python generate-blob-sas-url.py filename.dat
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
4. If the blob exists, the SAS URL will be displayed.

**Tip:** To generate SAS URLs for multiple files, create a text file (`blobs.list`) with blob names and run:

```sh
cat blobs.list | xargs -I {} python generate-blob-sas-url.py {}
```

## With Docker
To run this tool within a Docker container:

1. Open a terminal and navigate to the repository directory (the one containing your `config.json` file).
   ```sh
   cd <git repository directory>
   ```
2. Run the following command to generate a SAS URL:
   ```sh
   docker run --rm -v "$(pwd)/config.json:/app/config.json" azure-blob-sas-generator <blob_filename>
   ```
   **Command Explanation:**
   *   `--rm`: This flag automatically removes the container when it exits, keeping your system clean.
   *   `-v "$(pwd)/config.json:/app/config.json"`: This mounts your `config.json` (expected to be in your current directory, `$(pwd)`) into the container at `/app/config.json`, where the script expects it. Ensure `config.json` is present and correctly populated in your current working directory before running.
   *   `azure-blob-sas-generator`: This is the name of the Docker image you built earlier.
   *   `<blob_filename>`: Replace this with the actual name of the blob you want to generate a SAS URL for.

3. If the blob does not exist, an error message will be displayed.
4. If the blob exists, the SAS URL will be displayed.

## Error Handling and Troubleshooting

This section covers common issues you might encounter and how to resolve them.

*   **Error: `config.json` not found or `Error reading config file: [Errno 2] No such file or directory: 'config.json'`**
    *   **Cause:** The `config.json` file is missing from the root directory of the repository (for local execution) or not correctly mounted into the Docker container.
    *   **Solution (Local):** Ensure you have copied `config-template.json` to `config.json` and populated it with your Azure credentials. Make sure it's in the same directory as the `generate-blob-sas-url.py` script.
    *   **Solution (Docker):** When using `docker run`, ensure the volume mount `-v "$(pwd)/config.json:/app/config.json"` is correct and that `config.json` exists in your current host directory (`$(pwd)`).

*   **Error: `Error decoding JSON in the config file (config.json): ...`**
    *   **Cause:** The `config.json` file has a syntax error (e.g., missing comma, incorrect quoting).
    *   **Solution:** Carefully review `config.json` to ensure it's valid JSON. You can use an online JSON validator to check its syntax.

*   **Error: `Error - config.json did not have a key named '...'`**
    *   **Cause:** A required key (e.g., `storage_account_name`, `storage_account_key`) is missing from your `config.json`.
    *   **Solution:** Ensure all required keys as specified in the "Configuration File" section are present in your `config.json` and have valid values.

*   **Error: `Error - blob named <blob_name> not found in the container '<container_name>'`**
    *   **Cause:** The specified blob name does not exist in the Azure Blob Storage container you've configured, or the container name itself is incorrect in `config.json`.
    *   **Solution:** Double-check the blob name for typos. Verify that the blob exists in the correct container in the Azure portal. Confirm that the `container_name` in `config.json` is correct.

*   **Network Connectivity Issues (e.g., timeouts, connection refused):**
    *   **Cause:** Problems with your internet connection, firewall restrictions, or proxy misconfiguration. Azure services might also occasionally experience outages.
    *   **Solution:**
        *   Check your internet connection.
        *   If behind a corporate firewall, ensure it allows outbound connections to Azure Blob Storage endpoints (`*.blob.core.windows.net`).
        *   If using a proxy, ensure your local environment or Docker setup is correctly configured for it (see notes on proxy configuration in the Docker section).
        *   Check the Azure status page for any ongoing service disruptions.

*   **SSL/TLS Certificate Errors (e.g., `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain`):**
    *   **Cause:** This often occurs in corporate environments where network traffic is inspected via a proxy that uses custom SSL certificates not recognized by default by Python or the Docker container's OS.
    *   **Solution:**
        *   **Local Script:** The `truststore` library, used by `generate-blob-sas-url.py`, attempts to use the operating system's trust store. If your corporate CAs are installed there, it might work. If not, you may need to configure `truststore` further or set environment variables like `SSL_CERT_FILE`.
        *   **Docker:** This is the primary scenario the `.certs` directory and `truststore` integration are designed to solve. Ensure you have placed your corporate CA certificates in the `.certs` directory *before building the Docker image*, as detailed in the "Corporate Firewalls and Custom Certificates" section. The script inside the container will then use `truststore` to leverage these CAs.
        *   If issues persist, verify the certificates in `.certs` are correct and in the proper format (PEM, usually `.crt` files).

*   **Docker Error: `docker: Error response from daemon: ... manifest for azure-blob-sas-generator not found: manifest unknown: manifest unknown.`**
    *   **Cause:** You are trying to run the `azure-blob-sas-generator` image, but it was not built successfully or is not available locally.
    *   **Solution:** Ensure you have run the `docker build -t azure-blob-sas-generator .` command successfully from the repository root.