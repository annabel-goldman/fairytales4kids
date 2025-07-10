# Fairytales 4 Kids

This site was created as an experiment in using AI in my development workflow. As a child, I remember asking my parents to read me stories in situations where we didn't have a book readily available, so I thought a site like this could help other families in similar moments. I also just genuinely love fairytales and building things, so this was a one-off passion project that brought together my interests in technology, storytelling, and creativity.

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