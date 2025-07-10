# Fairytales 4 Kids - Project Index

This document provides a comprehensive overview of the project structure and all files in the codebase.

## 📁 Root Directory

### Core Files
- **`README.md`** - Main project documentation and setup instructions
- **`PROJECT_INDEX.md`** - This file - comprehensive project overview
- **`requirements.txt`** - Python dependencies with pinned versions
- **`config.py`** - Centralized configuration management
- **`setup.py`** - Automated setup and validation script
- **`env.template`** - Environment variables template
- **`.gitignore`** - Git ignore patterns for security and cleanliness

### Documentation
- **`SETUP_GITHUB_ACTIONS.md`** - GitHub Actions deployment setup guide

## 📁 Source Directory (`src/`)

### Main Pages
- **`index.html`** - Homepage with forest-themed welcome screen
- **`pages/stories.html`** - Main stories listing page with grid layout

### Story Pages (`pages/stories/`)
Individual fairy tale pages, each with:
- SEO-optimized meta tags
- Responsive design
- Google AdSense integration
- Social media sharing tags

**Available Stories:**
- `cinderella.html`
- `frog-prince.html`
- `goldilocks.html`
- `hansel-and-gretel.html`
- `humpty-dumpty.html`
- `jack-and-the-beanstalk.html`
- `jack-frost.html`
- `little-red-riding-hood.html`
- `mother-goose.html`
- `princess-and-the-pea.html`
- `puss-in-boots.html`
- `rapunzel.html`
- `rose-red.html`
- `sleeping-beauty.html`
- `snow-white.html`
- `the-ugly-duckling.html`
- `three-blind-mice.html`
- `three-little-pigs.html`

### Assets (`assets/`)
- **`images/`** - Story illustrations (AI-generated)
- **`images_backup/`** - Backup images (gitignored)
- **`logo.png`** - Site logo

### Styles (`styles/`)
- **`styles.css`** - Global styles and utilities
- **`home.css`** - Homepage-specific styles
- **`story.css`** - Story page-specific styles

## 📁 Scripts Directory (`scripts/`)

### Content Generation (`page_generator/`)
- **`generate_page.py`** - Generate new fairy tale pages with AI
- **`enhance_page.py`** - Enhance existing story content with AI
- **`upload_to_s3.py`** - Upload files to AWS S3 for deployment

### Utilities
- **`generate_sitemap.py`** - Generate XML sitemap for SEO
- **`watch_pages.py`** - File watcher for development

## 📁 Public Directory (`public/`)
- **`robots.txt`** - Search engine crawling instructions
- **`sitemap.xml`** - Generated sitemap for SEO

## 📁 GitHub Actions (`.github/workflows/`)
- **`deploy.yml`** - Main deployment workflow
- **`test-deploy.yml`** - Test deployment workflow

## 📁 Testing Suite (`testing-suite/`)

### Configuration
- **`package.json`** - Node.js dependencies and scripts
- **`cypress.config.js`** - Cypress test configuration

### Tests (`cypress/`)
- **`e2e/pages/homePage.cy.js`** - Homepage test page object
- **`e2e/pomdemo.cy.js`** - Page Object Model demonstration
- **`e2e/spec.cy.js`** - Main test specifications

### Support (`cypress/support/`)
- **`commands.js`** - Custom Cypress commands
- **`e2e.js`** - End-to-end test configuration

### Fixtures (`cypress/fixtures/`)
- **`example.json`** - Test data

## 🔧 Configuration Management

### Environment Variables
All sensitive configuration is managed through environment variables:

**Required:**
- `OPENAI_API_KEY` - OpenAI API key for content generation
- `AWS_ACCESS_KEY_ID` - AWS access key for S3 deployment
- `AWS_SECRET_ACCESS_KEY` - AWS secret key for S3 deployment
- `S3_BUCKET_NAME` - S3 bucket name for hosting
- `CLOUDFRONT_DISTRIBUTION_ID` - CloudFront distribution ID

**Optional:**
- `GOOGLE_ADSENSE_CLIENT_ID` - Google AdSense client ID
- `WEBSITE_URL` - Website URL for meta tags

### Configuration File (`config.py`)
Centralized configuration management with:
- Environment variable loading
- Default values
- Configuration validation
- Path constants
- API settings

## 🚀 Deployment

### Automated Deployment
GitHub Actions workflow that:
1. Generates updated sitemap
2. Uploads files to S3
3. Invalidates CloudFront cache
4. Sends deployment notifications

### Manual Deployment
Scripts for manual deployment:
- `scripts/generate_sitemap.py`
- `scripts/page_generator/upload_to_s3.py`

## 🧪 Testing

### Test Structure
- **E2E Tests**: End-to-end testing with Cypress
- **Page Object Model**: Organized test structure
- **Fixtures**: Test data management

### Test Commands
```bash
npm run test          # Run all tests
npm run cypress:open  # Open Cypress UI
npm run cypress:run   # Run tests in headless mode
```

## 🔒 Security Features

### Gitignore Patterns
- Environment files (`.env`, `.env.*`)
- Virtual environments (`venv/`, `.venv/`)
- Python cache (`__pycache__/`)
- Node modules (`node_modules/`)
- AWS credentials (`.aws/`)
- Log files (`*.log`)
- Temporary files (`*.tmp`, `*.temp`)
- Backup files (`*.bak`, `*.backup`)

### Secret Management
- All API keys stored in environment variables
- No hardcoded secrets in source code
- GitHub Secrets for CI/CD
- Configuration validation

## 📊 Dependencies

### Python Dependencies
- **openai==1.12.0** - OpenAI API client
- **boto3==1.34.34** - AWS SDK
- **python-dotenv==1.0.0** - Environment variable management
- **requests==2.31.0** - HTTP requests
- **beautifulsoup4==4.12.3** - HTML parsing
- **Pillow==10.2.0** - Image processing
- **httpx==0.26.0** - Async HTTP client
- **watchdog==3.0.0** - File system monitoring

### Development Dependencies
- **pytest==7.4.3** - Testing framework
- **black==23.11.0** - Code formatting
- **flake8==6.1.0** - Linting

### Node.js Dependencies
- **cypress==14.3.3** - End-to-end testing

## 🎯 Key Features

### AI Integration
- **Content Generation**: GPT-4 for story creation
- **Image Generation**: DALL-E 3 for illustrations
- **Content Enhancement**: AI-powered story improvement

### Web Features
- **Responsive Design**: Mobile-first approach
- **SEO Optimization**: Meta tags, sitemap, structured data
- **Performance**: Optimized images and assets
- **Accessibility**: Semantic HTML and ARIA labels

### Development Features
- **Automated Setup**: Setup script with validation
- **Configuration Management**: Centralized config system
- **Testing Suite**: Comprehensive E2E tests
- **CI/CD Pipeline**: Automated deployment

## 📝 Maintenance

### Regular Tasks
1. **Update Dependencies**: Keep packages up to date
2. **Monitor API Usage**: Track OpenAI and AWS usage
3. **Test Deployment**: Verify automated deployment
4. **Backup Content**: Regular content backups
5. **Security Audits**: Review access and permissions

### Monitoring
- GitHub Actions deployment status
- CloudFront invalidation status
- Website performance metrics
- Error logs and monitoring

This index provides a complete overview of the Fairytales 4 Kids project structure and can be used for onboarding new developers or understanding the codebase architecture. 