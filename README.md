# Fairytales 4 Kids

Note: This site was created as an experiment in using AI in my development workflow, and using AI for automated content generation. 

As a child, I remember asking my parents to read me stories in situations where we didn't have a book readily available, and I remember that usually my dad would find one online. so I thought a site like this could help other families in similar moments. I also just genuinely love fairytales and building things, so this was a fun one-off project.

> **Note:**
> If you only want to use the HTML files locally (for example, to read stories or host the site on your own computer), you do **not** need to set up any API keys, AWS credentials, or follow the CodeBuild/deployment instructions. Just open the files in your browser or use a simple static server.

## AI Story Generation


### Generate New Stories

Create entirely new fairy tale stories with AI-generated content and illustrations:

```bash
cd scripts/page_generator
python generate_page.py
```

This script will:
- Generate a complete fairy tale story using GPT-4
- Create a custom illustration using DALL-E 3
- Build a complete HTML page with proper styling
- Add the story to your site's navigation

### Enhance Existing Stories

Improve existing stories with more detailed content, formatting, or new illustrations. (Honestly, I think this script could use better promting. As is, running this script often results in stories with overly complex language for kids):

```bash
cd scripts/page_generator
python enhance_page.py
```



```

### Deploy to AWS

Upload your site to AWS S3 for web hosting:

```bash
cd scripts/page_generator
python upload_to_s3.py
```

### Generate Sitemap

Create an XML sitemap for search engine optimization:

```bash
cd scripts
python generate_sitemap.py
```


## Prerequisites

- Python 3.11+ (for content generation)
- AWS Account with S3 bucket and CloudFront distribution (for deployment)
- OpenAI API key (for content generation)

> **Note:** For local viewing only, you don't need any of these prerequisites!

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/annabel-goldman/fairytales4kids.git
cd Fairytales

# Run automated setup
python setup.py
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
S3_BUCKET_NAME=your_s3_bucket_name
CLOUDFRONT_DISTRIBUTION_ID=your_cloudfront_distribution_id

# Optional Configuration
GOOGLE_ADSENSE_CLIENT_ID=ca-pub-3709806584351963
WEBSITE_URL=https://fairytales4kids.com
```

### 3. Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt

```

## Running the Project Locally

### Option 1: Direct File Opening
The simplest way to view the site:

```bash
# Navigate to the source directory
cd src

# Open the homepage in your browser
open index.html  # macOS
# or
start index.html  # Windows
# or
xdg-open index.html  # Linux
```

### Option 2: Local Web Server (Recommended)
For better functionality, use a local server:

```bash
# Using Python (recommended)
cd src
python -m http.server 8000
# Then visit http://localhost:8000

# Using Node.js (if you have it installed)
cd src
npx serve .
# Then visit the URL shown in terminal
```

## Automated Deployment Setup

> **Note:**
> The deployment setup is optional. The site works perfectly for local viewing without any AWS setup.

### 1. Configure GitHub Secrets
For automatic deployment to AWS, add these secrets to your GitHub repository:

1. Go to GitHub → Your Repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `AWS_ACCESS_KEY_ID` - Your AWS access key
   - `AWS_SECRET_ACCESS_KEY` - Your AWS secret key
   - `S3_BUCKET_NAME` - Your S3 bucket name
   - `CLOUDFRONT_DISTRIBUTION_ID` - Your CloudFront distribution ID

### 2. AWS Setup Requirements
- S3 bucket configured for static website hosting
- CloudFront distribution pointing to your S3 bucket
- IAM user with permissions for S3 and CloudFront

### 3. Automatic Deployment
Once configured, the site automatically deploys when you:
1. Push changes to the `main` branch
2. The GitHub Actions workflow runs on GitHub-hosted runners
3. Files are uploaded to S3 and CloudFront cache is invalidated