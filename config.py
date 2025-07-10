"""
Configuration file for Fairytales 4 Kids project.
All configurable values should be set here or via environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and Credentials
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
CLOUDFRONT_DISTRIBUTION_ID = os.getenv('CLOUDFRONT_DISTRIBUTION_ID')

# Google AdSense Configuration
GOOGLE_ADSENSE_CLIENT_ID = os.getenv('GOOGLE_ADSENSE_CLIENT_ID', 'ca-pub-3709806584351963')

# Website Configuration
WEBSITE_URL = os.getenv('WEBSITE_URL', 'https://fairytales4kids.com')
WEBSITE_TITLE = 'Fairytales 4 Kids'
WEBSITE_DESCRIPTION = 'Classic fairy tales for children - perfect for bedtime reading'

# File Paths
SRC_DIR = 'src'
ASSETS_DIR = os.path.join(SRC_DIR, 'assets')
IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
PAGES_DIR = os.path.join(SRC_DIR, 'pages')
STORIES_DIR = os.path.join(PAGES_DIR, 'stories')
STYLES_DIR = os.path.join(SRC_DIR, 'styles')

# Content Generation Settings
DEFAULT_IMAGE_SIZE = "1024x1024"
DEFAULT_IMAGE_QUALITY = "standard"
DEFAULT_MODEL = "gpt-4"
DALL_E_MODEL = "dall-e-3"

# Validation
def validate_config():
    """Validate that all required configuration is present."""
    required_vars = {
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
        'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY,
        'S3_BUCKET_NAME': S3_BUCKET_NAME,
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True 