# Fairytales 4 Kids

A beautiful collection of classic fairy tales for children, featuring AI-generated content and modern web design.

## 🚀 Features

- **AI-Generated Content**: Uses OpenAI GPT-4 to create and enhance fairy tale stories
- **AI-Generated Images**: Uses DALL-E 3 to create custom illustrations for each story
- **Modern Web Design**: Responsive design with beautiful animations and typography
- **SEO Optimized**: Proper meta tags, sitemap, and structured content
- **Automated Deployment**: GitHub Actions for automatic deployment to AWS S3 and CloudFront
- **Testing Suite**: Cypress-based end-to-end testing

## 📋 Prerequisites

- Python 3.11+
- Node.js 16+ (for testing suite)
- AWS Account with S3 bucket and CloudFront distribution
- OpenAI API key

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/annabel-goldman/fairytales4kids.git
cd Fairytales
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

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

### 5. Setup Testing Suite

```bash
cd testing-suite
npm install
```

## 🎯 Usage

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

### Upload to S3

```bash
cd scripts/page_generator
python upload_to_s3.py
```

### Run Tests

```bash
cd testing-suite
npm run test
```

## 📁 Project Structure

```
Fairytales/
├── src/                    # Source files
│   ├── assets/            # Images and static assets
│   ├── pages/             # HTML pages
│   │   └── stories/       # Individual story pages
│   └── styles/            # CSS stylesheets
├── scripts/               # Python utility scripts
│   ├── page_generator/    # Content generation scripts
│   ├── generate_sitemap.py
│   └── watch_pages.py
├── public/                # Public assets
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables (not tracked)

testing-suite/
├── cypress/               # Cypress test files
├── package.json           # Node.js dependencies
└── cypress.config.js      # Cypress configuration
```

## 🔒 Security

### Environment Variables

All sensitive information is managed through environment variables:

- **API Keys**: OpenAI API key for content generation
- **AWS Credentials**: Access keys for S3 deployment
- **Configuration**: Website URLs and other configurable values

### Gitignore

The following files are excluded from version control:

- `.env` files
- Virtual environments (`venv/`, `.venv/`)
- Python cache files (`__pycache__/`)
- Node modules (`node_modules/`)
- AWS credentials
- Log files and temporary files

## 🚀 Deployment

### Automated Deployment

The project uses GitHub Actions for automated deployment:

1. Push code to `main` or `master` branch
2. GitHub Actions automatically:
   - Generates updated sitemap
   - Uploads files to S3
   - Invalidates CloudFront cache
   - Sends deployment notifications

### Manual Deployment

```bash
# Generate sitemap
cd scripts
python generate_sitemap.py

# Upload to S3
cd page_generator
python upload_to_s3.py
```

## 🧪 Testing

### Running Tests

```bash
cd testing-suite
npm run test          # Run all tests
npm run cypress:open  # Open Cypress UI
```

### Test Structure

- **E2E Tests**: End-to-end testing of website functionality
- **Page Object Model**: Organized test structure
- **Fixtures**: Test data management

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🤝 Support

For questions or support, please open an issue on GitHub.

## 🔄 Updates

- **Content Generation**: AI-powered story creation and enhancement
- **Image Generation**: Custom illustrations for each story
- **Deployment**: Automated CI/CD pipeline
- **Security**: Proper secret management and environment variables 