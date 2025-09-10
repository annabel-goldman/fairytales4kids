#!/usr/bin/env python3
"""
Setup script for Fairytales 4 Kids project.
This script helps users configure their environment and validate setup.
"""

import os
import sys
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if .env file exists and guide user to create it."""
    env_file = Path('.env')
    template_file = Path('env.template')
    
    if env_file.exists():
        print("✅ .env file found")
        return True
    
    if template_file.exists():
        print("📝 Creating .env file from template...")
        shutil.copy(template_file, env_file)
        print("✅ .env file created from template")
        print("⚠️  Please edit .env file with your actual API keys and credentials")
        return False
    
    print("❌ No .env file found and no template available")
    print("   Please create a .env file with the following variables:")
    print("   - OPENAI_API_KEY")
    print("   - AWS_ACCESS_KEY_ID")
    print("   - AWS_SECRET_ACCESS_KEY")
    print("   - S3_BUCKET_NAME")
    print("   - CLOUDFRONT_DISTRIBUTION_ID")
    return False

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import openai
        import boto3
        import requests
        import bs4  # beautifulsoup4 is imported as bs4
        print("✅ All required Python packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_directories():
    """Check if required directories exist."""
    required_dirs = [
        'src',
        'src/assets',
        'src/assets/images',
        'src/pages',
        'src/pages/stories',
        'src/styles',
        'scripts',
        'scripts/page_generator'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("✅ All required directories exist")
    return True

def validate_config():
    """Validate configuration if .env file exists."""
    try:
        from config import validate_config as validate
        validate()
        print("✅ Configuration validation passed")
        return True
    except ImportError:
        print("⚠️  Cannot import config module")
        return False
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Fairytales 4 Kids Setup")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            all_passed = False
    
    # Only validate config if .env file exists
    if Path('.env').exists():
        print(f"\n🔍 Validating Configuration...")
        if not validate_config():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 Setup complete! You're ready to use Fairytales 4 Kids")
        print("\nNext steps:")
        print("1. Activate your virtual environment: source venv/bin/activate")
        print("2. Generate a story: cd scripts/page_generator && python generate_page.py")
    else:
        print("⚠️  Setup incomplete. Please address the issues above.")
        print("\nFor help, see the README.md file")

if __name__ == "__main__":
    main() 