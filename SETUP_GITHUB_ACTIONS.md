# GitHub Actions Deployment Setup

This guide will help you set up automatic deployment to S3 and CloudFront cache invalidation when you push code to GitHub.

## What This Does

When you push code to the `main` or `master` branch, GitHub Actions will:
1. Generate an updated sitemap
2. Upload all files to your S3 bucket
3. Invalidate CloudFront cache to serve new content
4. Notify you of deployment status

## Prerequisites

- GitHub repository with your code
- AWS account with S3 bucket and CloudFront distribution
- AWS credentials with appropriate permissions

## Setup Steps

### 1. Get Your AWS Information

Run these commands to get your CloudFront distribution ID:

```bash
# List your CloudFront distributions
aws cloudfront list-distributions --query 'DistributionList.Items[?Aliases.Items[?contains(@, `fairytales4kids.com`)]].[Id,DomainName,Aliases.Items]' --output table

# Or get all distributions and find yours
aws cloudfront list-distributions --output table
```

### 2. Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key | `wJalrXUtnFEMI...` |
| `S3_BUCKET_NAME` | Your S3 bucket name | `my-fairytales-bucket` |
| `CLOUDFRONT_DISTRIBUTION_ID` | Your CloudFront distribution ID | `E1234567890ABCD` |

### 3. AWS IAM Permissions

Your AWS user needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-BUCKET-NAME",
                "arn:aws:s3:::YOUR-BUCKET-NAME/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudfront:CreateInvalidation",
                "cloudfront:GetInvalidation",
                "cloudfront:ListInvalidations"
            ],
            "Resource": "arn:aws:cloudfront::YOUR-ACCOUNT-ID:distribution/YOUR-DISTRIBUTION-ID"
        }
    ]
}
```

### 4. Test the Workflow

1. Push your code to the main branch
2. Go to Actions tab in GitHub
3. Watch the deployment workflow run
4. Check your website for updates

## Troubleshooting

### Common Issues:

1. **Permission Denied**: Check AWS credentials and IAM permissions
2. **Bucket Not Found**: Verify S3_BUCKET_NAME secret
3. **Distribution Not Found**: Verify CLOUDFRONT_DISTRIBUTION_ID secret
4. **Python Dependencies**: Make sure requirements.txt is up to date

### Manual Trigger

You can manually trigger the workflow:
1. Go to Actions tab
2. Select "Deploy to S3 and Invalidate CloudFront"
3. Click "Run workflow"

## Monitoring

- Check GitHub Actions tab for deployment status
- Monitor CloudFront invalidation status in AWS Console
- Verify website updates at https://fairytales4kids.com

## Workflow Customization

The workflow file is at `.github/workflows/deploy.yml`. You can customize:
- Trigger branches
- Python version
- AWS region
- Deployment steps
- Notifications

## Tips

- Keep your AWS credentials secure
- Monitor CloudFront invalidation costs
- Consider using AWS OIDC for better security
- Set up notifications for failed deployments 