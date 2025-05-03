import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import mimetypes

# Load environment variables
load_dotenv()

def should_upload_file(file_path):
    """Determine if a file should be uploaded based on exclusion rules"""
    # List of directories to exclude
    excluded_dirs = {'venv', '__pycache__', '.git', '.env', 'scripts', 'page_generator'}
    # List of file patterns to exclude
    excluded_files = {'.DS_Store', '.gitignore', '.env', 'requirements.txt'}
    
    # Check if path contains any excluded directory
    path_parts = file_path.split(os.sep)
    if any(part in excluded_dirs for part in path_parts):
        return False
    
    # Check if file is in excluded files
    if os.path.basename(file_path) in excluded_files:
        return False
    
    # Special case: allow sitemap.xml in the root directory
    if os.path.basename(file_path) == 'sitemap.xml' and len(path_parts) == 1:
        return True
    
    return True

def upload_file_to_s3(s3_client, file_path, bucket_name, s3_key):
    """Upload a single file to S3 with proper content type"""
    try:
        # Get the content type based on file extension
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        # Upload the file
        s3_client.upload_file(
            file_path,
            bucket_name,
            s3_key,
            ExtraArgs={'ContentType': content_type}
        )
        print(f"Successfully uploaded {file_path} to {s3_key}")
        return True
    except ClientError as e:
        print(f"Error uploading {file_path}: {e}")
        return False

def upload_directory_to_s3(s3_client, directory_path, bucket_name, s3_prefix=''):
    """Upload all files in a directory to S3"""
    total_files = 0
    uploaded_files = 0
    
    # Ensure we're working with absolute paths
    directory_path = os.path.abspath(directory_path)
    
    for root, dirs, files in os.walk(directory_path):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in {'venv', '__pycache__', '.git', 'scripts', 'page_generator'}]
        
        for file in files:
            # Get the full local path
            local_path = os.path.join(root, file)
            
            # Skip if file should not be uploaded
            if not should_upload_file(local_path):
                continue
            
            total_files += 1
            
            # Calculate the S3 key (path in S3)
            # Get the relative path from the src directory
            relative_path = os.path.relpath(local_path, directory_path)
            s3_key = relative_path.replace('\\', '/')
            
            # Upload the file
            if upload_file_to_s3(s3_client, local_path, bucket_name, s3_key):
                uploaded_files += 1
    
    print(f"\nUpload Summary:")
    print(f"Total files processed: {total_files}")
    print(f"Successfully uploaded: {uploaded_files}")
    if total_files != uploaded_files:
        print(f"Failed uploads: {total_files - uploaded_files}")

def main():
    # Get AWS credentials from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('S3_BUCKET_NAME')
    
    if not all([aws_access_key_id, aws_secret_access_key, bucket_name]):
        print("Error: AWS credentials or bucket name not found in environment variables")
        return
    
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Get the absolute path to the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # Upload the sitemap.xml from the root directory
    sitemap_path = os.path.join(project_root, 'sitemap.xml')
    if os.path.exists(sitemap_path):
        if upload_file_to_s3(s3_client, sitemap_path, bucket_name, 'sitemap.xml'):
            print("Successfully uploaded sitemap.xml")
    
    # Upload the src directory
    src_directory = os.path.join(project_root, 'src')
    if not os.path.exists(src_directory):
        print(f"Error: Source directory not found at {src_directory}")
        return
    
    print(f"Uploading files from: {src_directory}")
    print(f"Starting upload to S3 bucket: {bucket_name}")
    upload_directory_to_s3(s3_client, src_directory, bucket_name)
    print("Upload completed!")

if __name__ == "__main__":
    main() 