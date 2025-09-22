import os
import boto3
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

S3_ENDPOINT = os.environ.get('S3_ENDPOINT', 'http://minio:9000')
S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY', 'minioadmin')
S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY', 'minioadmin')
S3_BUCKET = os.environ.get('S3_BUCKET', 'test-bucket')

s3 = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
    region_name='us-east-1',
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    logger.info(f"Received upload request for file: {file.filename}")
    try:
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
        logger.info(f"Successfully uploaded file: {file.filename}")
        return jsonify({'message': 'File uploaded', 'filename': file.filename})
    except Exception as e:
        logger.error(f"Failed to upload file {file.filename}: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    logger.info(f"Received download request for file: {filename}")
    try:
        s3.download_file(S3_BUCKET, filename, filename)
        logger.info(f"Successfully downloaded file: {filename}")
        return jsonify({'message': 'File downloaded', 'filename': filename})
    except Exception as e:
        logger.error(f"Failed to download file {filename}: {e}")
        return jsonify({'error': str(e)}), 404

@app.route('/buckets', methods=['GET'])
def list_buckets():
    logger.info("Received request to list all buckets")
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response.get('Buckets', [])]
        logger.info(f"Buckets found: {buckets}")
        return jsonify({'buckets': buckets})
    except Exception as e:
        logger.error(f"Failed to list buckets: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/objects', methods=['GET'])
def list_objects():
    logger.info(f"Received request to list all objects in bucket: {S3_BUCKET}")
    try:
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        objects = [obj['Key'] for obj in response.get('Contents', [])] if 'Contents' in response else []
        logger.info(f"Objects found in bucket '{S3_BUCKET}': {objects}")
        return jsonify({'objects': objects})
    except Exception as e:
        logger.error(f"Failed to list objects in bucket '{S3_BUCKET}': {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure bucket exists
    try:
        s3.create_bucket(Bucket=S3_BUCKET)
        logger.info(f"Bucket '{S3_BUCKET}' created or already exists.")
    except Exception as e:
        logger.info(f"Bucket '{S3_BUCKET}' already exists or error: {e}")
    app.run(host='0.0.0.0', port=5000)
