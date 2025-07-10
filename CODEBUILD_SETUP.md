# AWS CodeBuild Self-Hosted GitHub Actions Runner Setup

This guide explains how to set up AWS CodeBuild as a self-hosted GitHub Actions runner for your Fairytales project using the new "Runner project" feature.

## Prerequisites

1. AWS Account with appropriate permissions
2. GitHub repository with admin access
3. GitHub Personal Access Token (PAT) with `repo` and `admin:org` scopes

## Step 1: Create GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with the following scopes:
   - `repo` (Full control of private repositories)
   - `admin:org` (Full control of organizations and teams)
3. Copy the token and save it securely

## Step 2: Create AWS CodeBuild Runner Project

### 2.1 Create IAM Role for CodeBuild

1. Go to AWS IAM Console
2. Create a new role with the following policies:
   - `AWSCodeBuildDeveloperAccess`
   - Custom policy for additional permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::your-artifacts-bucket/*"
        }
    ]
}
```

### 2.2 Create CodeBuild Runner Project

1. Go to AWS CodeBuild Console
2. Click "Create build project"
3. Configure the project:

**Project configuration:**
- Project name: `fairytales-github-actions-runner`
- Project type: **Runner project** (this is the key difference!)
- Description: `Self-hosted GitHub Actions runner for Fairytales project`

**Runner:**
- Runner provider: `GitHub`
- Credential: Connect your GitHub account (OAuth recommended)
- Runner location: `Repository`
- Repository URL: `https://github.com/your-username/Fairytales`

**Environment:**
- Environment image: `Managed image`
- Operating system: `Ubuntu`
- Runtime: `Standard`
- Image: `aws/codebuild/standard:7.0`
- Privileged: `Enabled` (required for Docker operations)
- Service role: Select the IAM role created in step 2.1

**Additional configuration:**
- Manual creation: `Enabled` (allows manual triggering)
- Webhook event filters: Configure as needed

## Step 3: Configure Webhook

### 3.1 Create Webhook in CodeBuild

1. In your CodeBuild project, go to the "Build triggers" tab
2. Click "Create webhook"
3. Configure the webhook:

**Webhook configuration:**
- Webhook name: `github-actions-webhook`
- Source provider: `GitHub`
- Repository: Select your repository
- Source version: `main`

**Event types:**
- `WORKFLOW_JOB` - This is the key event for GitHub Actions runners
- `PUSH` - Trigger on code pushes (optional)
- `PULL_REQUEST_CREATED` - Trigger on PR creation (optional)
- `PULL_REQUEST_UPDATED` - Trigger on PR updates (optional)

**Webhook filters:**
- Event: `WORKFLOW_JOB`
- Base reference: `refs/heads/main`
- File path: `Fairytales/**` (to trigger only when files in Fairytales directory change)

### 3.2 Configure GitHub Webhook

1. Go to your GitHub repository settings
2. Navigate to Webhooks → Add webhook
3. Configure the webhook with the values CodeBuild provided:

**Payload URL:** (Use the URL from CodeBuild)
**Content type:** `application/json`
**Secret:** (Use the secret from CodeBuild)

**Events:**
- Select **"Let me select individual events"**
- Check the following events:
  - ✅ **Workflow jobs** (this is the key one for GitHub Actions runners)
  - ✅ **Pushes** (optional, for general repository updates)
  - ✅ **Pull requests** (optional, if you want to test on PRs)

## Step 4: Update GitHub Secrets

In your GitHub repository, add the following secrets:

1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:

| Name | Value |
|------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `S3_BUCKET_NAME` | Your S3 bucket name |
| `CLOUDFRONT_DISTRIBUTION_ID` | Your CloudFront distribution ID |

## Step 5: Test the Setup

1. **Make a small change** to any file in your `Fairytales/` directory
2. **Commit and push** the changes to the `main` branch
3. **Check the webhook delivery** in GitHub:
   - Go to Settings → Webhooks
   - Click on your webhook
   - Scroll down to "Recent Deliveries"
   - You should see a recent delivery with a green checkmark

4. **Check CodeBuild console** to see if a build was triggered
5. **Check GitHub Actions** to see if your workflow runs on the CodeBuild runner

## Key Differences from Traditional Setup

### What's Different:
1. **No buildspec.yml required**: CodeBuild automatically handles the runner setup
2. **Simpler configuration**: Just select "Runner project" type
3. **Automatic runner management**: CodeBuild handles runner lifecycle automatically
4. **Built-in webhook support**: Easier webhook configuration
5. **Workflow job events**: Uses `workflow_job` events instead of `workflow_run`

### Workflow Changes:
Your workflow now uses the format:
```yaml
runs-on: codebuild-fairytales-github-actions-runner-${{ github.run_id }}-${{ github.run_attempt }}
```

This ensures each job gets a unique runner instance.

## Logs and Monitoring

- **CodeBuild logs**: Available in CloudWatch Logs
- **GitHub Actions logs**: Available in the Actions tab of your repository
- **Webhook delivery logs**: Available in GitHub repository settings
- **Runner logs**: Available in CodeBuild build logs

## Security Considerations

1. **GitHub Connection:** Use OAuth for better security
2. **IAM Roles:** Follow the principle of least privilege
3. **Webhook Security:** CodeBuild handles webhook authentication automatically
4. **Secrets Management:** Use AWS Secrets Manager for sensitive data in production

## Cost Optimization

1. **Build Timeout:** Set appropriate timeout values to avoid unnecessary costs
2. **Instance Types:** Choose cost-effective instance types for your workload
3. **Log Retention:** Configure CloudWatch log retention to manage storage costs
4. **Idle Timeout:** Configure build timeout to prevent long-running builds

## Next Steps

After successful setup:

1. Monitor the first few builds to ensure everything works correctly
2. Consider setting up build notifications (SNS, Slack, etc.)
3. Implement build caching strategies to improve performance
4. Set up monitoring and alerting for build failures

## Benefits of Runner Project Approach

1. **Simplified Setup:** No need for custom buildspec.yml
2. **Automatic Management:** CodeBuild handles runner lifecycle
3. **Better Integration:** Native GitHub Actions integration
4. **Easier Maintenance:** Less custom code to maintain
5. **Built-in Security:** Automatic credential management 