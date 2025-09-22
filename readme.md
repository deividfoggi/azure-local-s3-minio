# Project Overview

This project demonstrates how to use a local S3-compatible storage solution with Docker Compose. It provides sample configuration and instructions for deploying and interacting with S3 storage locally, which is useful for development, testing, or migration scenarios.

## Features

- Deploys a local S3-compatible service (e.g., MinIO) using Docker Compose.
- Includes example `docker-compose.yaml` for deployment.
- Provides instructions for accessing and testing S3 storage from your local machine.

# Demo Instructions

## Prerequisites

- Docker and Docker Compose installed
- (Optional) `curl` for HTTP requests to S3-compatible endpoints

## Steps

1. **Deploy S3-Compatible Storage**
    - Start MinIO using Docker Compose:
      ```sh
      docker-compose up -d
      ```
    - The example `docker-compose.yaml` should define the MinIO service and expose port 9000.

2. **Access the S3 Service**
    - Access the MinIO web UI at [http://localhost:9000](http://localhost:9000).

3. **Create Buckets and Upload Files**
    - Use the MinIO web UI to create buckets.
    - To upload a file using `curl`, first create a bucket via the web UI, then run:
      ```sh
      curl -X PUT "http://localhost:9000/demo-bucket/sample.txt" \
        --upload-file ./sample.txt \
        -H "Host: localhost:9000" \
        -u minioadmin:minioadmin
      ```
    - Replace `demo-bucket` and `sample.txt` with your bucket name and file as needed.

4. **Test Integration**
    - Use your application or scripts to interact with the S3 endpoint using the provided credentials and endpoint URL.

## Cleanup

To remove the demo resources:
```sh
docker-compose down
```

---

**Note:** Update credentials and endpoints in your `docker-compose.yaml` and scripts as needed for your environment.

