---
name: veo-setup
description: Configure Google Cloud project and authentication for Veo video generation. Creates or configures GCP project, enables APIs, sets up service account, and configures environment variables.
---

This skill configures Google Cloud Platform for Veo video generation. Handles project creation, API enablement, service account setup, and environment variable configuration.

## Prerequisites Check

Before starting, verify gcloud CLI is installed:

```bash
gcloud --version
```

If not installed, direct user to: https://cloud.google.com/sdk/docs/install

## Setup Flow

### Step 1: Determine Project Strategy

Ask the user:
1. **Use existing project** - They have a GCP project ready
2. **Create new project** - Need to create one from scratch

### Step 2: Project Configuration

#### Option A: Existing Project

```bash
# List available projects
gcloud projects list

# Set the project
gcloud config set project PROJECT_ID
```

Verify billing is enabled:
```bash
gcloud billing accounts list
gcloud billing projects describe PROJECT_ID
```

If billing not enabled, instruct user to enable at:
https://console.cloud.google.com/billing/linkedaccount?project=PROJECT_ID

#### Option B: New Project

```bash
# Create project (project IDs must be globally unique)
gcloud projects create PROJECT_ID --name="PROJECT_NAME"

# Set as active project
gcloud config set project PROJECT_ID
```

Link billing account:
```bash
# List billing accounts
gcloud billing accounts list

# Link billing (required for Vertex AI)
gcloud billing projects link PROJECT_ID --billing-account=BILLING_ACCOUNT_ID
```

### Step 3: Enable Required APIs

```bash
# Enable Vertex AI API (required)
gcloud services enable aiplatform.googleapis.com

# Verify enablement
gcloud services list --enabled --filter="name:aiplatform"
```

### Step 4: Create Service Account

```bash
# Create service account for Veo
gcloud iam service-accounts create veo-generator \
  --display-name="Veo Video Generator" \
  --description="Service account for Veo AI video generation via Vertex AI"

# Verify creation
gcloud iam service-accounts list --filter="email:veo-generator"
```

### Step 5: Grant IAM Permissions

```bash
# Get the full service account email
SA_EMAIL="veo-generator@PROJECT_ID.iam.gserviceaccount.com"

# Grant Vertex AI User role (required for video generation)
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"

# Verify role assignment
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:$SA_EMAIL" \
  --format="table(bindings.role)"
```

### Step 6: Create Service Account Key

```bash
# Create key file in user's home directory
gcloud iam service-accounts keys create ~/veo-service-account.json \
  --iam-account=veo-generator@PROJECT_ID.iam.gserviceaccount.com

# Verify key was created
ls -la ~/veo-service-account.json
```

**Security note**: This key file grants access to your GCP project. Keep it secure and never commit to version control.

### Step 7: Configure Environment Variables

Detect user's shell and update appropriate config file.

**For zsh (default on macOS):**
```bash
# Check if variables already exist
grep -q "GOOGLE_CLOUD_PROJECT" ~/.zshrc && echo "Already configured" || echo "Not configured"

# Add environment variables
cat >> ~/.zshrc << 'EOF'

# Veo - Google Cloud Configuration
export GOOGLE_CLOUD_PROJECT="PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/veo-service-account.json"
EOF

# Reload shell configuration
source ~/.zshrc
```

**For bash:**
```bash
cat >> ~/.bashrc << 'EOF'

# Veo - Google Cloud Configuration
export GOOGLE_CLOUD_PROJECT="PROJECT_ID"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/veo-service-account.json"
EOF

source ~/.bashrc
```

### Step 8: Authenticate Application Default Credentials

```bash
# Set up application default credentials
gcloud auth application-default login
```

This opens a browser for OAuth authentication.

### Step 9: Verify Complete Setup

Run all verification checks:

```bash
echo "=== Verification ==="

# Check environment variables
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Location: $GOOGLE_CLOUD_LOCATION"
echo "Credentials: $GOOGLE_APPLICATION_CREDENTIALS"

# Verify credentials file exists
if [ -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
  echo "✓ Credentials file exists"
else
  echo "✗ Credentials file NOT FOUND"
fi

# Test authentication
if gcloud auth application-default print-access-token > /dev/null 2>&1; then
  echo "✓ Authentication working"
else
  echo "✗ Authentication FAILED"
fi

# Verify API is enabled
if gcloud services list --enabled --filter="name:aiplatform" --format="value(name)" | grep -q aiplatform; then
  echo "✓ Vertex AI API enabled"
else
  echo "✗ Vertex AI API NOT enabled"
fi

# Verify service account exists
if gcloud iam service-accounts list --filter="email:veo-generator" --format="value(email)" | grep -q veo-generator; then
  echo "✓ Service account exists"
else
  echo "✗ Service account NOT FOUND"
fi

echo "=== Setup Complete ==="
```

## Quick Setup (All Steps)

For users who want to run everything at once with a new project:

```bash
# Variables - user must set these
PROJECT_ID="veo-video-gen"  # Must be globally unique
PROJECT_NAME="Veo Video Generation"
BILLING_ACCOUNT=""  # Get from: gcloud billing accounts list

# Execute setup
gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"
gcloud config set project $PROJECT_ID
gcloud billing projects link $PROJECT_ID --billing-account=$BILLING_ACCOUNT
gcloud services enable aiplatform.googleapis.com
gcloud iam service-accounts create veo-generator --display-name="Veo Video Generator"
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:veo-generator@$PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/aiplatform.user"
gcloud iam service-accounts keys create ~/veo-service-account.json \
  --iam-account=veo-generator@$PROJECT_ID.iam.gserviceaccount.com

# Add to shell config
echo "" >> ~/.zshrc
echo "# Veo - Google Cloud Configuration" >> ~/.zshrc
echo "export GOOGLE_CLOUD_PROJECT=\"$PROJECT_ID\"" >> ~/.zshrc
echo "export GOOGLE_CLOUD_LOCATION=\"us-central1\"" >> ~/.zshrc
echo "export GOOGLE_APPLICATION_CREDENTIALS=\"\$HOME/veo-service-account.json\"" >> ~/.zshrc

source ~/.zshrc
gcloud auth application-default login
```

## Troubleshooting

### "Project ID already exists"
Project IDs are globally unique. Try adding a random suffix:
```bash
PROJECT_ID="veo-video-gen-$(date +%s)"
```

### "Billing account not found"
List available billing accounts:
```bash
gcloud billing accounts list
```
If none listed, create one at: https://console.cloud.google.com/billing

### "Permission denied creating service account"
Ensure you have Owner or Editor role on the project:
```bash
gcloud projects get-iam-policy PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:user:YOUR_EMAIL"
```

### "API not accessible"
Wait a few minutes after enabling API. If still failing:
```bash
gcloud services disable aiplatform.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

## Cleanup (If Needed)

To remove the setup:

```bash
# Delete service account key
rm ~/veo-service-account.json

# Delete service account
gcloud iam service-accounts delete veo-generator@PROJECT_ID.iam.gserviceaccount.com

# Remove from shell config (manual edit required)
# Edit ~/.zshrc or ~/.bashrc and remove the Veo configuration block

# Optionally delete project entirely
gcloud projects delete PROJECT_ID
```

## Output

After successful setup, confirm to user:

1. **Project ID**: The configured GCP project
2. **Service Account**: veo-generator@PROJECT_ID.iam.gserviceaccount.com
3. **Credentials File**: ~/veo-service-account.json
4. **Environment Variables**: Set in shell config
5. **Ready to use**: The `veo` skill for video generation
