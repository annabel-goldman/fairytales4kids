# AWS CodeBuild Self-Hosted GitHub Actions Runner Setup

This guide explains how to set up AWS CodeBuild as a self-hosted GitHub Actions runner for your Fairytales project using the new "Runner project" feature.

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
- Project type: **Runner project** 

**Runner:**
- Runner provider: `GitHub`
- Credential: Connect your GitHub account using the Personal Access Token created in Step 1
- Runner location: `Repository`
- Repository URL: `https://github.com/your-username/Fairytales`

**Webhook Event Filters (under Runner section):**
1. **Expand the "Webhook event filter groups" subsection**
2. **Click "Add filter group"**
3. **Configure the filter group:**

**Event type:**
- Select `WORKFLOW_JOB_QUEUED` (this is the key event for GitHub Actions runners)

**Add filters:**
Click "Add filter" and configure the following filters:

**Filter 1: Workflow Name (recommended)**
- **Condition**: `START_BUILD`
- **Type**: `workflow name`
- **Pattern**: `Test and Deploy`

**Filter 2: Actor Account ID (optional, for security)**
- **Condition**: `START_BUILD`
- **Type**: `actor account id`
- **Pattern**: Your GitHub user ID

**How to find your GitHub user ID:**
1. **Curl**: Use `curl https://api.github.com/users/your-username` and look for the `"id"` field
2. **Your user ID** will be a numeric value (like `12345678`), not your username.

**Note:** You can skip this filter if you prefer to keep it simple. The Workflow Name filter alone is sufficient for most use cases.

**Note:** For `WORKFLOW_JOB_QUEUED` events, only `workflow name` and `actor account id` filters are supported. Organization name and repository name filters are not available for this event type.

**Environment:**
- Provisioning Model: `On-demand`
- Environment image: `Managed image`
- Compute: `EC2`
- Running Mode: `Container`
- Operating system: `Ubuntu`
- Runtime: `Standard`
- Image: `aws/codebuild/standard:7.0`
- Image version: `Always use the latest image for this runtime version`

**Additional Environment configuration:**
- Privileged: `Enabled` (required for Docker operations)


**Service Role Permissions**
- Service role: Select the IAM role created in step 2.1

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

### Available Filter Types for WORKFLOW_JOB_QUEUED Events:
- **Workflow name**: Ensures builds only trigger for your specific workflow (recommended)
- **Actor account ID**: Restricts who can trigger builds (optional but recommended for security)

### Available Filter Types for PUSH Events:
- **Actor account ID**: Restricts who can trigger builds
- **Organization name**: Adds an extra layer of security
- **Repository name**: Ensures builds only trigger for your specific repository (only for organization/global webhooks)

### Available Filter Types for PULL_REQUEST Events:
- **Actor account ID**: Restricts who can trigger builds
- **Organization name**: Adds an extra layer of security
- **Repository name**: Ensures builds only trigger for your specific repository (only for organization/global webhooks)

### Filter Type Options Summary:
- **Actor account ID**: Available for all event types
- **Workflow name**: Only available for WORKFLOW_JOB_QUEUED events
- **Organization name**: Available for PUSH and PULL_REQUEST events
- **Repository name**: Available for PUSH and PULL_REQUEST events (only for organization/global webhooks)

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