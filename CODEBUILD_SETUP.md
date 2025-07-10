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

### 2.3 Configure Webhook Event Filters (During Project Creation)

**Important:** For Runner projects, webhook configuration is done during the initial project creation, not in the Build triggers tab.

1. **Expand the "Webhook event filter groups" section** in the project configuration
2. **Click "Add filter group"**
3. **Configure the filter group:**

**Event type:**
- Select `WORKFLOW_JOB_QUEUED` (this is the key event for GitHub Actions runners)

**Add filters:**
Click "Add filter" and configure the following filters:

**Filter 1: Repository Name**
- **Condition**: `START_BUILD`
- **Type**: `repository name`
- **Pattern**: `your-username/fairytales4kids`

**Filter 2: Organization Name**
- **Condition**: `START_BUILD`
- **Type**: `organization name`
- **Pattern**: `your-username`

**Filter 3: Workflow Name (optional)**
- **Condition**: `START_BUILD`
- **Type**: `workflow name`
- **Pattern**: `Test and Deploy`

**Filter 4: Actor Account ID (optional, for security)**
- **Condition**: `START_BUILD`
- **Type**: `actor account id`
- **Pattern**: Your GitHub user ID

## Step 3: Update GitHub Secrets

In your GitHub repository, add the following secrets:

1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:

| Name | Value |
|------|-------|
| `AWS_ACCESS_KEY_ID` | Your AWS access key |
| `AWS_SECRET_ACCESS_KEY` | Your AWS secret key |
| `S3_BUCKET_NAME` | Your S3 bucket name |
| `CLOUDFRONT_DISTRIBUTION_ID` | Your CloudFront distribution ID |

## Step 4: Test the Setup

1. **Make a small change** to any file in your `Fairytales/` directory
2. **Commit and push** the changes to the `main` branch
3. **Check CodeBuild console** to see if a build was triggered
4. **Check GitHub Actions** to see if your workflow runs on the CodeBuild runner

## Key Differences from Traditional Setup

### What's Different:
1. **No buildspec.yml required**: CodeBuild automatically handles the runner setup
2. **Simpler configuration**: Just select "Runner project" type
3. **Automatic runner management**: CodeBuild handles runner lifecycle automatically
4. **Built-in webhook support**: Webhook configuration is done during project creation
5. **Workflow job events**: Uses `WORKFLOW_JOB_QUEUED` events for GitHub Actions integration

### Workflow Changes:
Your workflow now uses the format:
```yaml
runs-on: codebuild-fairytales-github-actions-runner-${{ github.run_id }}-${{ github.run_attempt }}
```

This ensures each job gets a unique runner instance.

## Webhook Filter Configuration Details

### Available Filter Types:
- **Repository name**: Ensures builds only trigger for your specific repository
- **Organization name**: Adds an extra layer of security
- **Workflow name**: Ensures builds only trigger for your specific workflow
- **Actor account ID**: Restricts who can trigger builds (optional but recommended for security)

### Filter Conditions:
- **START_BUILD**: Triggers a build when the filter conditions are met
- **DO_NOT_START_BUILD**: Prevents a build from starting when the filter conditions are met

### Event Types:
- **WORKFLOW_JOB_QUEUED**: The main event for GitHub Actions runners
- **PUSH**: Trigger on code pushes (optional)
- **PULL_REQUEST_CREATED**: Trigger on PR creation (optional)
- **PULL_REQUEST_UPDATED**: Trigger on PR updates (optional)

## Logs and Monitoring

- **CodeBuild logs**: Available in CloudWatch Logs
- **GitHub Actions logs**: Available in the Actions tab of your repository
- **Runner logs**: Available in CodeBuild build logs

## Security Considerations

1. **GitHub Connection:** Use OAuth for better security
2. **IAM Roles:** Follow the principle of least privilege
3. **Webhook Security:** CodeBuild handles webhook authentication automatically
4. **Secrets Management:** Use AWS Secrets Manager for sensitive data in production
5. **Filter Configuration:** Use specific filters to restrict which events trigger builds

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
6. **Integrated Webhook Configuration:** Webhook setup is part of the initial project configuration 