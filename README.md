# Fairytales 4 Kids

This site was created as an experiment in using AI in my development workflow. As a child, I remember asking my parents to read me stories in situations where we didn't have a book readily available, so I thought a site like this could help other families in similar moments. I also just genuinely love fairytales and building things, so this was a one-off passion project that brought together my interests in technology, storytelling, and creativity.

> **Note:**
> If you only want to use the HTML files locally (for example, to read stories or host the site on your own computer), you do **not** need to set up any API keys, AWS credentials, or follow the CodeBuild/deployment instructions. Just open the files in your browser or use a simple static server.

## Features

- AI-Generated Content: Uses OpenAI GPT-4 to create and enhance fairy tale stories
- AI-Generated Images: Uses DALL-E 3 to create custom illustrations for each story
- Modern Web Design: Responsive design with beautiful animations and typography
- SEO Optimized: Proper meta tags, sitemap, and structured content
- Automated Deployment: GitHub Actions for automatic deployment to AWS S3 and CloudFront
- Comprehensive Testing: Cypress-based end-to-end testing with CI/CD integration
- Security: Proper secret management and environment variables

## Prerequisites

- Python 3.11+
- Node.js 16+ (for testing suite)
- AWS Account with S3 bucket and CloudFront distribution
- OpenAI API key

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

# Testing suite dependencies
cd testing-suite
npm install
cd ..
```

## Project Structure

```
Fairytales/
├── src/                   # Source files
│   ├── assets/            # Images and static assets
│   │   ├── images/        # Story illustrations (AI-generated)
│   │   └── logo.png       # Site logo
│   ├── pages/             # HTML pages
│   │   ├── stories.html   # Main stories listing page
│   │   └── stories/       # Individual story pages (18 stories)
│   └── styles/            # CSS stylesheets
│       ├── styles.css     # Global styles
│       ├── home.css       # Homepage styles
│       └── story.css      # Story page styles
├── scripts/               # Python utility scripts
│   ├── page_generator/    # Content generation scripts
│   │   ├── generate_page.py
│   │   ├── enhance_page.py
│   │   └── upload_to_s3.py
│   ├── generate_sitemap.py
│   └── watch_pages.py
├── public/                # Public assets
│   ├── robots.txt         # Search engine instructions
│   └── sitemap.xml        # Generated sitemap
├── testing-suite/         # Cypress testing suite
│   ├── cypress/           # Test files
│   ├── package.json       # Node.js dependencies
│   └── cypress.config.js  # Cypress configuration
├── .github/workflows/     # GitHub Actions workflows
│   └── test-and-deploy.yml # Single workflow for testing and deployment
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
└── .env                  # Environment variables (not tracked)
```

## Available Stories

The project includes 18 classic fairy tales:
- Cinderella
- Snow White
- Sleeping Beauty
- Rapunzel
- Little Red Riding Hood
- Jack and the Beanstalk
- Three Little Pigs
- Goldilocks
- Hansel and Gretel
- Frog Prince
- Princess and the Pea
- Puss in Boots
- Rose Red
- Humpty Dumpty
- Jack Frost
- Mother Goose
- The Ugly Duckling
- Three Blind Mice

## Usage

### Generate New Story

```bash
cd scripts/page_generator
python generate_page.py
```

### Enhance Existing Story

```bash
cd scripts/page_generator
python enhance_page.py
```

## AWS CodeBuild GitHub Actions Runner Setup

> **Note:**
> You only need to follow this section if you want to automate deployment and hosting using AWS CodeBuild and GitHub Actions. If you do not plan to host or deploy the site using AWS, you can skip this section entirely.

### 1. Create GitHub Personal Access Token
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` and `admin:org` scopes
3. Save the token securely

### 2. Create IAM Role for CodeBuild
1. Go to AWS IAM Console
2. Create a new role with `AWSCodeBuildDeveloperAccess` and S3 permissions

### 3. Create CodeBuild Runner Project
1. Go to AWS CodeBuild Console
2. Click "Create build project"
3. Set Project name: `fairytales-github-actions-runner`
4. Project type: **Runner project**
5. Runner provider: `GitHub`
6. Connect your GitHub account using the token
7. Runner location: `Repository`
8. Repository URL: `https://github.com/your-username/fairytales4kids`
9. Webhook event filter:
   - Event type: `WORKFLOW_JOB_QUEUED`
   - Filter: `workflow name` = `Test and Deploy` (or your workflow name)
10. Environment:
    - Provisioning Model: `On-demand`
    - Image: `aws/codebuild/standard:7.0`
    - Privileged: `Enabled`
11. Service role: Select the IAM role from step 2

### 4. Add GitHub Secrets
1. Go to GitHub → Settings → Secrets and variables → Actions
2. Add:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `S3_BUCKET_NAME`
   - `CLOUDFRONT_DISTRIBUTION_ID`

### 5. Configure GitHub Webhook
1. Go to GitHub → Settings → Webhooks
2. Click the CodeBuild webhook
3. Select "Let me select individual events"
4. Check **Workflow jobs** (uncheck others)
5. Save

### 6. Test
1. Make a small change and push to `main`
2. Check CodeBuild console for a triggered build
3. Check GitHub Actions for runner activity