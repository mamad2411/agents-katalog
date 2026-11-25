---
name: databricks-oneenv-workspace-deployment
description: Create and manage Databricks workspaces in the One-Env account for demos requiring custom AWS integrations
---

# Databricks One-Env Workspace Deployment

## Purpose

Create Databricks workspaces in the **One-Env AWS account** for demos and testing that require custom AWS integrations not possible with the FE Vending Machine (FEVM). This includes scenarios like:

- Custom IAM role configurations
- Cross-account S3 access patterns
- Custom VPC networking (classic workspaces)
- PrivateLink demonstrations
- AWS service integrations (Glue, Athena, etc.)

**When to use this skill vs FEVM:**
- Use **FEVM** (`/databricks-fe-vm-workspace-deployment`) for standard demos, Apps, Lakebase - it's faster and simpler
- Use **this skill** when you need direct AWS infrastructure control or custom integrations

## Important: 2-Week Cleanup Automation

The AWS sandbox account and Databricks One-Env account have **automated cleanup every 2 weeks**. This means:

- Workspaces may be deleted
- AWS resources (IAM roles, S3 buckets, VPCs) may be deleted independently
- Partial state is common (e.g., workspace exists but IAM role is gone)

**This skill is designed to handle this.** It always verifies resource state before use and offers repair options.

## Prerequisites and Authentication

**IMPORTANT**: Before proceeding with any workspace operations, you MUST verify authentication is working. If auth fails, invoke the appropriate skill to authenticate.

### Step 0: Verify and Establish Authentication

#### AWS Sandbox Authentication

```bash
# Check if AWS auth is working
aws sts get-caller-identity --profile aws-sandbox-field-eng_databricks-sandbox-admin
```

**If this fails** (token expired, profile not found, etc.):
→ **Invoke `/aws-authentication` skill** to authenticate with the AWS sandbox account.

The AWS profile needed is: `aws-sandbox-field-eng_databricks-sandbox-admin`

#### Databricks One-Env Account Authentication

```bash
# Check if Databricks account-level auth is working
databricks account workspaces list --profile one-env-admin-aws --output json | head -5
```

**If this fails** (not configured, token expired, etc.):
→ **Invoke `/databricks-authentication` skill** and select the `one-env-admin-aws` profile (Databricks Account level auth for One-Env AWS account).

The Databricks profile needed is: `one-env-admin-aws`
- Account ID: `0d26daa6-5e44-4c97-a497-ef015f91254a`
- Host: `https://accounts.cloud.databricks.com`

### Authentication Flow Summary

```
1. Check AWS auth → if fails → /aws-authentication
2. Check Databricks account auth → if fails → /databricks-authentication (one-env-admin-aws)
3. Only proceed with workspace operations after BOTH authentications succeed
```

## Registry Location

All created resources are tracked in: `~/.vibe/oneenv/`

```
~/.vibe/oneenv/
├── registry.json              # Master registry of all resources
└── workspaces/
    └── {workspace-name}.json  # Individual workspace configs with dependencies
```

## Naming Conventions

Use these deterministic naming patterns to enable repair/recreation:

| Resource Type | Pattern | Example |
|--------------|---------|---------|
| Workspace | `oneenv-{user}-{purpose}-{region-short}` | `oneenv-bkvarda-s3demo-use1` |
| IAM Cross-Account Role | `oneenv-{workspace}-cross-account` | `oneenv-bkvarda-s3demo-use1-cross-account` |
| IAM UC Access Role | `oneenv-{workspace}-uc-access` | `oneenv-bkvarda-s3demo-use1-uc-access` |
| S3 UC Root Bucket | `oneenv-{workspace}-uc-root` | `oneenv-bkvarda-s3demo-use1-uc-root` |
| Storage Credential | `oneenv-{workspace}-cred` | `oneenv-bkvarda-s3demo-use1-cred` |
| Metastore (shared) | `oneenv-shared-{region}` | `oneenv-shared-us-east-1` |

**Region short codes:** us-east-1 = use1, us-east-2 = use2, us-west-2 = usw2, eu-central-1 = euc1

---

## Workflow: Creating a New Workspace

### Step 1: Gather Requirements

Ask the user for:

1. **Workspace type**: Serverless (recommended) or Classic?
2. **Region**: us-east-1 (default), us-east-2, us-west-2, eu-central-1?
3. **Purpose**: Brief description for naming (e.g., "s3demo", "glue-integration")
4. **IP ACLs**: Standard FE list (default) or disabled for public access?
5. **Workspace name**: Auto-generate based on purpose, or user-specified?

### Step 2: Verify Prerequisites

```bash
# Get current user for naming
USER_SHORT=$(aws sts get-caller-identity --profile aws-sandbox-field-eng_databricks-sandbox-admin --query 'Arn' --output text | sed 's/.*\///' | cut -d'@' -f1 | tr '.' '-')

# Verify Databricks account access
databricks account workspaces list --profile one-env-admin-aws --output json | head -5
```

### Step 3: Check for Existing Metastore

Metastores are shared to avoid quota limits. Check for existing ones:

```bash
# List all metastores in the account
databricks account metastores list --profile one-env-admin-aws --output json
```

**Decision logic:**
1. If a metastore exists in the target region → use it (prefer newest if multiple)
2. If no metastore in region → attempt to create one
3. If creation fails (quota) → find any existing metastore in region (even if we didn't create it)

### Step 4: Create AWS Infrastructure

#### 4a. Create S3 Bucket for Unity Catalog

```bash
BUCKET_NAME="oneenv-${WORKSPACE_NAME}-uc-root"
REGION="us-east-1"

# Create bucket
aws s3api create-bucket \
  --bucket "${BUCKET_NAME}" \
  --region "${REGION}" \
  $([ "${REGION}" != "us-east-1" ] && echo "--create-bucket-configuration LocationConstraint=${REGION}") \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Block public access (security best practice)
aws s3api put-public-access-block \
  --bucket "${BUCKET_NAME}" \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Enable versioning (recommended for UC)
aws s3api put-bucket-versioning \
  --bucket "${BUCKET_NAME}" \
  --versioning-configuration Status=Enabled \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin
```

#### 4b. Create IAM Role for Unity Catalog Access

Use the template at `resources/templates/uc_access_trust_policy.json` and `resources/templates/uc_access_permissions_policy.json`.

```bash
ROLE_NAME="oneenv-${WORKSPACE_NAME}-uc-access"
BUCKET_NAME="oneenv-${WORKSPACE_NAME}-uc-root"
AWS_ACCOUNT_ID="332745928618"
DATABRICKS_ACCOUNT_ID="0d26daa6-5e44-4c97-a497-ef015f91254a"

# Create trust policy (allows Databricks to assume role)
cat > /tmp/trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::414351767826:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "DATABRICKS_ACCOUNT_ID_PLACEHOLDER"
        }
      }
    }
  ]
}
EOF
sed -i '' "s/DATABRICKS_ACCOUNT_ID_PLACEHOLDER/${DATABRICKS_ACCOUNT_ID}/" /tmp/trust-policy.json

# Create the role
aws iam create-role \
  --role-name "${ROLE_NAME}" \
  --assume-role-policy-document file:///tmp/trust-policy.json \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Create permissions policy
cat > /tmp/permissions-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::${BUCKET_NAME}",
        "arn:aws:s3:::${BUCKET_NAME}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "sts:AssumeRole"
      ],
      "Resource": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${ROLE_NAME}"
    }
  ]
}
EOF

# Attach the policy
aws iam put-role-policy \
  --role-name "${ROLE_NAME}" \
  --policy-name "${ROLE_NAME}-policy" \
  --policy-document file:///tmp/permissions-policy.json \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin
```

#### 4c. For Classic Workspaces Only: Create VPC

Classic workspaces require a customer-managed VPC. Use the template at `resources/templates/vpc_config.json`.

```bash
# Create VPC
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block "10.0.0.0/16" \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=oneenv-${WORKSPACE_NAME}-vpc}]" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin \
  --query 'Vpc.VpcId' --output text)

# Enable DNS hostnames (required for Databricks)
aws ec2 modify-vpc-attribute --vpc-id "${VPC_ID}" --enable-dns-hostnames \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Create subnets (2 for HA), NAT gateway, security groups...
# See resources/classic_vpc_setup.sh for full script
```

### Step 5: Create Databricks Workspace

#### 5a. For Serverless Workspace

```bash
WORKSPACE_NAME="oneenv-bkvarda-s3demo-use1"
REGION="us-east-1"

# Create workspace
databricks account workspaces create \
  --workspace-name "${WORKSPACE_NAME}" \
  --aws-region "${REGION}" \
  --pricing-tier "ENTERPRISE" \
  --profile one-env-admin-aws

# Wait for workspace to be provisioned (can take 5-15 minutes)
databricks account workspaces get --workspace-id <ID> --profile one-env-admin-aws
```

#### 5b. For Classic Workspace

```bash
# Requires network configuration created in Step 4c
databricks account workspaces create \
  --workspace-name "${WORKSPACE_NAME}" \
  --aws-region "${REGION}" \
  --pricing-tier "ENTERPRISE" \
  --network-id "<network-config-id>" \
  --profile one-env-admin-aws
```

### Step 6: Assign Metastore to Workspace

```bash
WORKSPACE_ID="<from step 5>"
METASTORE_ID="<from step 3>"

databricks account metastore-assignments create \
  --workspace-id "${WORKSPACE_ID}" \
  --metastore-id "${METASTORE_ID}" \
  --default-catalog-name "main" \
  --profile one-env-admin-aws
```

### Step 7: Create Storage Credential (if new metastore)

If we created a new metastore, we need to create a storage credential:

```bash
# First, authenticate to the new workspace
WORKSPACE_URL="https://${WORKSPACE_NAME}.cloud.databricks.com"
databricks auth login --host "${WORKSPACE_URL}" --profile "oneenv-${WORKSPACE_NAME}"

# Create storage credential
databricks storage-credentials create \
  --name "oneenv-${WORKSPACE_NAME}-cred" \
  --aws-iam-role-arn "arn:aws:iam::332745928618:role/oneenv-${WORKSPACE_NAME}-uc-access" \
  --profile "oneenv-${WORKSPACE_NAME}"
```

### Step 8: Configure IP ACLs

Apply standard FE IP ACLs (matching FEVM workspaces):

```bash
# Get FE standard IPs from an existing FEVM workspace for reference
# Or use the predefined list in resources/templates/ip_acl_list.json

databricks ip-access-lists create \
  --label "FE-Standard-IPs" \
  --list-type "ALLOW" \
  --ip-addresses '["list", "of", "approved", "ips"]' \
  --profile "oneenv-${WORKSPACE_NAME}"

# Enable IP access lists
databricks workspace-conf set-status \
  --json '{"enableIpAccessLists": "true"}' \
  --profile "oneenv-${WORKSPACE_NAME}"
```

**To disable IP ACLs** (for demos requiring public access):

```bash
databricks workspace-conf set-status \
  --json '{"enableIpAccessLists": "false"}' \
  --profile "oneenv-${WORKSPACE_NAME}"
```

### Step 9: Update Registry

After successful creation, update the registry using the Python helper:

```bash
uv run resources/registry_manager.py add-workspace \
  --name "${WORKSPACE_NAME}" \
  --workspace-id "${WORKSPACE_ID}" \
  --url "${WORKSPACE_URL}" \
  --region "${REGION}" \
  --type "serverless" \
  --metastore-id "${METASTORE_ID}" \
  --iam-role-arn "arn:aws:iam::332745928618:role/oneenv-${WORKSPACE_NAME}-uc-access" \
  --s3-bucket "oneenv-${WORKSPACE_NAME}-uc-root"
```

### Step 10: Report to User

Provide the user with:
- Workspace URL
- CLI profile name: `oneenv-{workspace-name}`
- Authentication command: `databricks auth login --host <url> --profile oneenv-<name>`
- Created resources summary
- Reminder about 2-week cleanup

---

## Post-Deployment: Unity Catalog and Integration Setup

After creating the workspace, set up Unity Catalog resources and the integration role for AWS service access.

### Step 11: Create UC Storage Credential and External Location

Every workspace should have a dedicated storage credential and external location for data storage.

```bash
WORKSPACE_PROFILE="oneenv-${WORKSPACE_NAME}"
UC_BUCKET="oneenv-${WORKSPACE_NAME}-uc-data"
INTEGRATION_ROLE_ARN="arn:aws:iam::332745928618:role/oneenv-${WORKSPACE_NAME}-integration"

# First, authenticate to the workspace
databricks auth login --host "https://${WORKSPACE_NAME}.cloud.databricks.com" --profile "${WORKSPACE_PROFILE}"

# Create the UC data bucket
aws s3api create-bucket \
  --bucket "${UC_BUCKET}" \
  --region "${REGION}" \
  $([ "${REGION}" != "us-east-1" ] && echo "--create-bucket-configuration LocationConstraint=${REGION}") \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

aws s3api put-public-access-block \
  --bucket "${UC_BUCKET}" \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Create the storage credential (uses the integration role created in Step 12)
databricks storage-credentials create \
  --name "oneenv-${WORKSPACE_NAME}-storage-cred" \
  --aws-iam-role "{ \"role_arn\": \"${INTEGRATION_ROLE_ARN}\" }" \
  --profile "${WORKSPACE_PROFILE}"

# Create external location pointing to the UC data bucket
databricks external-locations create \
  --name "oneenv-${WORKSPACE_NAME}-external" \
  --url "s3://${UC_BUCKET}/" \
  --credential-name "oneenv-${WORKSPACE_NAME}-storage-cred" \
  --profile "${WORKSPACE_PROFILE}"
```

### Step 12: Create Integration IAM Role

Create a multi-purpose IAM role that can be used as both:
- **Instance profile** for Databricks cluster instances
- **Cloud service credential** for accessing AWS services

This role has permissions for: S3, Glue, Kinesis, MSK, DynamoDB, RDS, Secrets Manager.

```bash
INTEGRATION_ROLE_NAME="oneenv-${WORKSPACE_NAME}-integration"
UC_BUCKET="oneenv-${WORKSPACE_NAME}-uc-data"
CATALOG_BUCKET="oneenv-${WORKSPACE_NAME}-catalog"
DBFS_BUCKET="oneenv-${WORKSPACE_NAME}-dbfs-root"  # If classic workspace
AWS_ACCOUNT_ID="332745928618"
DATABRICKS_ACCOUNT_ID="0d26daa6-5e44-4c97-a497-ef015f91254a"

# Create trust policy (allows Databricks, EC2, and self-assume)
# Note: Self-assume is required for Unity Catalog storage credentials
cat > /tmp/integration-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DatabricksAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::414351767826:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "${DATABRICKS_ACCOUNT_ID}"
        }
      }
    },
    {
      "Sid": "EC2AssumeRoleForInstanceProfile",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "SelfAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${INTEGRATION_ROLE_NAME}"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name "${INTEGRATION_ROLE_NAME}" \
  --assume-role-policy-document file:///tmp/integration-trust-policy.json \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Create comprehensive permissions policy
# See resources/templates/integration_role_permissions_policy.json for full template
cat > /tmp/integration-permissions.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3FullAccess",
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": [
        "arn:aws:s3:::oneenv-${WORKSPACE_NAME}-*",
        "arn:aws:s3:::oneenv-${WORKSPACE_NAME}-*/*"
      ]
    },
    {
      "Sid": "GlueFullAccess",
      "Effect": "Allow",
      "Action": ["glue:*"],
      "Resource": [
        "arn:aws:glue:${REGION}:${AWS_ACCOUNT_ID}:catalog",
        "arn:aws:glue:${REGION}:${AWS_ACCOUNT_ID}:database/*",
        "arn:aws:glue:${REGION}:${AWS_ACCOUNT_ID}:table/*/*"
      ]
    },
    {
      "Sid": "KinesisAccess",
      "Effect": "Allow",
      "Action": ["kinesis:*"],
      "Resource": "arn:aws:kinesis:${REGION}:${AWS_ACCOUNT_ID}:stream/oneenv-${WORKSPACE_NAME}-*"
    },
    {
      "Sid": "KinesisListStreams",
      "Effect": "Allow",
      "Action": ["kinesis:ListStreams"],
      "Resource": "*"
    },
    {
      "Sid": "DynamoDBAccess",
      "Effect": "Allow",
      "Action": ["dynamodb:*"],
      "Resource": [
        "arn:aws:dynamodb:${REGION}:${AWS_ACCOUNT_ID}:table/oneenv-${WORKSPACE_NAME}-*",
        "arn:aws:dynamodb:${REGION}:${AWS_ACCOUNT_ID}:table/oneenv-${WORKSPACE_NAME}-*/index/*",
        "arn:aws:dynamodb:${REGION}:${AWS_ACCOUNT_ID}:table/oneenv-${WORKSPACE_NAME}-*/stream/*"
      ]
    },
    {
      "Sid": "DynamoDBListTables",
      "Effect": "Allow",
      "Action": ["dynamodb:ListTables"],
      "Resource": "*"
    },
    {
      "Sid": "MSKAccess",
      "Effect": "Allow",
      "Action": ["kafka:*", "kafka-cluster:*"],
      "Resource": [
        "arn:aws:kafka:${REGION}:${AWS_ACCOUNT_ID}:cluster/oneenv-${WORKSPACE_NAME}-*/*",
        "arn:aws:kafka:${REGION}:${AWS_ACCOUNT_ID}:topic/oneenv-${WORKSPACE_NAME}-*/*",
        "arn:aws:kafka:${REGION}:${AWS_ACCOUNT_ID}:group/oneenv-${WORKSPACE_NAME}-*/*"
      ]
    },
    {
      "Sid": "RDSAccess",
      "Effect": "Allow",
      "Action": ["rds:Describe*", "rds-db:connect"],
      "Resource": [
        "arn:aws:rds:${REGION}:${AWS_ACCOUNT_ID}:db:oneenv-${WORKSPACE_NAME}-*",
        "arn:aws:rds-db:${REGION}:${AWS_ACCOUNT_ID}:dbuser:*/*"
      ]
    },
    {
      "Sid": "SecretsManagerAccess",
      "Effect": "Allow",
      "Action": ["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
      "Resource": "arn:aws:secretsmanager:${REGION}:${AWS_ACCOUNT_ID}:secret:oneenv-${WORKSPACE_NAME}-*"
    },
    {
      "Sid": "SelfAssume",
      "Effect": "Allow",
      "Action": ["sts:AssumeRole"],
      "Resource": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/${INTEGRATION_ROLE_NAME}"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name "${INTEGRATION_ROLE_NAME}" \
  --policy-name "${INTEGRATION_ROLE_NAME}-policy" \
  --policy-document file:///tmp/integration-permissions.json \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Create instance profile and attach role
aws iam create-instance-profile \
  --instance-profile-name "${INTEGRATION_ROLE_NAME}" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

aws iam add-role-to-instance-profile \
  --instance-profile-name "${INTEGRATION_ROLE_NAME}" \
  --role-name "${INTEGRATION_ROLE_NAME}" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin
```

### Step 13: Create Catalog with Default Storage Location

Create a Unity Catalog catalog with a dedicated S3 bucket as its default storage location.

**Note:** A catalog with a storage root requires an external location to exist first.

```bash
CATALOG_NAME="oneenv_${WORKSPACE_NAME//-/_}_catalog"  # Replace hyphens with underscores for SQL compatibility
CATALOG_BUCKET="oneenv-${WORKSPACE_NAME}-catalog"
STORAGE_CRED_NAME="oneenv-${WORKSPACE_NAME}-storage-cred"

# Create catalog bucket
aws s3api create-bucket \
  --bucket "${CATALOG_BUCKET}" \
  --region "${REGION}" \
  $([ "${REGION}" != "us-east-1" ] && echo "--create-bucket-configuration LocationConstraint=${REGION}") \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

aws s3api put-public-access-block \
  --bucket "${CATALOG_BUCKET}" \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Create external location for catalog bucket (REQUIRED before creating catalog with storage-root)
databricks external-locations create \
  --name "oneenv-${WORKSPACE_NAME}-catalog-location" \
  --url "s3://${CATALOG_BUCKET}/" \
  --credential-name "${STORAGE_CRED_NAME}" \
  --profile "${WORKSPACE_PROFILE}"

# Create the catalog with storage location
databricks catalogs create \
  --name "${CATALOG_NAME}" \
  --storage-root "s3://${CATALOG_BUCKET}/" \
  --profile "${WORKSPACE_PROFILE}"

# Create a default schema
databricks schemas create \
  --catalog-name "${CATALOG_NAME}" \
  --name "default" \
  --profile "${WORKSPACE_PROFILE}"

# Grant permissions to workspace users
databricks grants update catalog "${CATALOG_NAME}" \
  --json '{"changes": [{"principal": "account users", "add": ["USE_CATALOG", "USE_SCHEMA", "SELECT", "MODIFY", "CREATE_TABLE", "CREATE_SCHEMA"]}]}' \
  --profile "${WORKSPACE_PROFILE}"
```

### Step 14: Register Instance Profile in Databricks

Register the instance profile so clusters can use it.

```bash
INTEGRATION_ROLE_NAME="oneenv-${WORKSPACE_NAME}-integration"
INSTANCE_PROFILE_ARN="arn:aws:iam::332745928618:instance-profile/${INTEGRATION_ROLE_NAME}"

# Register instance profile (for classic compute)
# Note: --skip-validation is used because the workspace cross-account role may not have iam:PassRole
# This is acceptable for test/demo environments
databricks instance-profiles add \
  --instance-profile-arn "${INSTANCE_PROFILE_ARN}" \
  --skip-validation \
  --profile "${WORKSPACE_PROFILE}"
```

---

## AWS Integration Testing

Create small, cost-effective AWS resources for integration testing with Databricks.

### Creating Test Resources

Use the `integration_resources.py` helper to create test resources:

```bash
cd /path/to/skill/resources

# Create a DynamoDB table (on-demand billing, minimal cost)
uv run integration_resources.py create-dynamodb \
  --workspace "${WORKSPACE_NAME}" \
  --table-name "test-table" \
  --region "${REGION}"

# Create a Kinesis stream (1 shard, minimal cost)
uv run integration_resources.py create-kinesis \
  --workspace "${WORKSPACE_NAME}" \
  --stream-name "test-stream" \
  --region "${REGION}"

# Create an RDS PostgreSQL instance (db.t3.micro, minimal cost)
# Note: RDS takes 5-10 minutes to provision
uv run integration_resources.py create-rds \
  --workspace "${WORKSPACE_NAME}" \
  --db-name "testdb" \
  --region "${REGION}" \
  --security-group "${SECURITY_GROUP_ID}"  # Optional: use workspace VPC security group

# Create MSK Serverless cluster (requires VPC subnets)
# Note: MSK takes 10-15 minutes to provision
uv run integration_resources.py create-msk \
  --workspace "${WORKSPACE_NAME}" \
  --cluster-name "test-kafka" \
  --region "${REGION}" \
  --subnet-ids "${PRIVATE_SUBNET_1},${PRIVATE_SUBNET_2}" \
  --security-group "${SECURITY_GROUP_ID}"
```

### Listing Test Resources

```bash
uv run integration_resources.py list \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}"
```

### Testing with Databricks

Example notebook code to test the integrations:

```python
# Test DynamoDB
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table(f'oneenv-{workspace_name}-test-table')

# Write
table.put_item(Item={'pk': 'test', 'sk': '1', 'data': 'hello'})

# Read
response = table.get_item(Key={'pk': 'test', 'sk': '1'})
print(response['Item'])
```

```python
# Test Kinesis with Spark Structured Streaming
df = (spark.readStream
  .format("kinesis")
  .option("streamName", f"oneenv-{workspace_name}-test-stream")
  .option("region", "us-west-2")
  .option("initialPosition", "TRIM_HORIZON")
  .load())

display(df)
```

```python
# Test RDS PostgreSQL with JDBC
jdbc_url = f"jdbc:postgresql://{rds_endpoint}:5432/postgres"
df = (spark.read
  .format("jdbc")
  .option("url", jdbc_url)
  .option("user", "admin")
  .option("password", password)  # Get from Secrets Manager
  .option("query", "SELECT 1")
  .load())
```

### Cleaning Up Test Resources

```bash
# Dry run - see what would be deleted
uv run integration_resources.py cleanup \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}"

# Actually delete all test resources
uv run integration_resources.py cleanup \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}" \
  --confirm

# Delete only specific resource type
uv run integration_resources.py cleanup \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}" \
  --resource-type dynamodb \
  --confirm
```

---

## Workflow: Verify & Repair Existing Workspace

When reusing an existing workspace, always verify its health first.

### Step 1: Load Registry

```bash
uv run resources/registry_manager.py get-workspace --name "${WORKSPACE_NAME}"
```

### Step 2: Run Health Checks

```bash
uv run resources/health_checker.py check-all --workspace "${WORKSPACE_NAME}"
```

This checks:
1. **Workspace**: Does it exist? Is it running?
2. **Metastore Assignment**: Is a metastore assigned?
3. **Storage Credential**: Does it exist? Is the IAM role valid?
4. **IAM Role**: Does the role exist? Is the trust policy correct?
5. **S3 Bucket**: Does the bucket exist? Is it accessible?
6. **VPC (classic only)**: Does the VPC exist? Are subnets intact?

### Step 3: Report Findings

Present findings to user in a clear table:

```
Resource Health Check for: oneenv-bkvarda-s3demo-use1
═══════════════════════════════════════════════════════
Resource                 Status      Notes
───────────────────────────────────────────────────────
Workspace                HEALTHY     Running, accessible
Metastore Assignment     HEALTHY     oneenv-shared-us-east-1
Storage Credential       BROKEN      IAM role not found
IAM UC Access Role       MISSING     Was deleted by cleanup
S3 UC Root Bucket        MISSING     Was deleted by cleanup
───────────────────────────────────────────────────────

Issues Found: 3
```

### Step 4: Ask User for Decision

Present options:
1. **Repair**: Recreate missing resources, update references
2. **Start Fresh**: Delete workspace and all resources, create new
3. **Cancel**: Do nothing

### Step 5a: Repair Flow

Repair in dependency order (bottom-up):

1. Create S3 bucket (if missing)
2. Create IAM role (if missing) - policy references bucket
3. Update storage credential (if broken) - references IAM role ARN
4. Metastore assignment usually survives if metastore exists

```bash
# Example repair sequence
uv run resources/health_checker.py repair --workspace "${WORKSPACE_NAME}" --confirm
```

### Step 5b: Start Fresh Flow

1. Delete workspace (if exists)
2. Delete workspace-specific IAM roles
3. Delete workspace-specific S3 buckets
4. Remove from registry
5. Run full creation workflow

```bash
uv run resources/registry_manager.py cleanup --workspace "${WORKSPACE_NAME}" --confirm
```

---

## Workflow: Full Cleanup

Use the `full_cleanup.py` script to delete a workspace and ALL associated resources. This script:
- Discovers resources by both registry data AND naming convention scanning
- Deletes in the correct dependency order
- Handles both tracked and untracked resources

### Deletion Order

Resources are deleted in reverse dependency order:

1. **Integration test resources** (DynamoDB, Kinesis, RDS, MSK, Secrets)
2. **Databricks workspace resources** (catalogs, external locations, storage credentials)
3. **AWS IAM** (instance profiles, then roles with their policies)
4. **AWS S3 buckets** (emptied then deleted)
5. **Databricks workspace**
6. **Databricks account resources** (storage config, credentials config, network config)
7. **AWS VPC resources** (NAT gateways, internet gateways, subnets, security groups, VPC)
8. **Registry cleanup** (workspace file removed)

### Usage

```bash
cd /path/to/skill/resources

# First, do a dry run to see what will be deleted
uv run full_cleanup.py \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}" \
  --dry-run

# Review the output, then actually delete
uv run full_cleanup.py \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}" \
  --confirm

# To keep the workspace but delete supporting resources (UC resources, IAM, etc.)
uv run full_cleanup.py \
  --workspace "${WORKSPACE_NAME}" \
  --region "${REGION}" \
  --skip-workspace \
  --confirm
```

### Example Output

```
🔍 Discovering resources for workspace: oneenv-bkvarda-demo-usw2
  Scanning S3 buckets...
    Found bucket: oneenv-bkvarda-demo-usw2-catalog
    Found bucket: oneenv-bkvarda-demo-usw2-uc-data
    Found bucket: oneenv-bkvarda-demo-usw2-uc-root
  Scanning IAM roles...
    Found role: oneenv-bkvarda-demo-usw2-integration
    Found role: oneenv-bkvarda-demo-usw2-uc-access
  ...

============================================================
RESOURCE SUMMARY
============================================================

📦 Integration Test Resources:
  • DynamoDB: oneenv-bkvarda-demo-usw2-test-table
  • Kinesis: oneenv-bkvarda-demo-usw2-test-stream

🔷 Databricks Workspace Resources:
  • Catalog: oneenv_bkvarda_demo_usw2_catalog
  • External Location: oneenv-bkvarda-demo-usw2-external
  • Storage Credential: oneenv-bkvarda-demo-usw2-storage-cred

🔐 AWS IAM:
  • Instance Profile: oneenv-bkvarda-demo-usw2-integration
  • Role: oneenv-bkvarda-demo-usw2-integration
  • Role: oneenv-bkvarda-demo-usw2-uc-access

🪣 AWS S3 Buckets:
  • oneenv-bkvarda-demo-usw2-catalog
  • oneenv-bkvarda-demo-usw2-uc-data
  • oneenv-bkvarda-demo-usw2-uc-root

🌐 AWS VPC Resources:
  • VPC: vpc-0123456789abcdef
  • Subnet: subnet-abc123
  • NAT Gateway: nat-xyz789
  ...

============================================================
```

### Important Notes

- **Shared metastore is NOT deleted** - Metastores are shared across workspaces
- **Dry run first** - Always run with `--dry-run` before `--confirm`
- **VPC deletion takes time** - NAT gateways require ~60 seconds to delete
- **Some deletions may fail** - The script continues on errors and reports them

---

## Reference: Account and Profile Information

| Resource | Value |
|----------|-------|
| AWS Sandbox Account ID | `332745928618` |
| AWS Profile | `aws-sandbox-field-eng_databricks-sandbox-admin` |
| Databricks Account ID | `0d26daa6-5e44-4c97-a497-ef015f91254a` |
| Databricks Account Profile | `one-env-admin-aws` |
| Databricks Control Plane AWS Account | `414351767826` |
| Account Console URL | `https://accounts.cloud.databricks.com` |

---

## Troubleshooting

### Metastore Quota Error

If you see "quota exceeded" when creating a metastore:

```bash
# List existing metastores to find one to reuse
databricks account metastores list --profile one-env-admin-aws --output json

# Use the newest one in your target region
```

### IAM Role Already Exists

If recreating a role that wasn't fully cleaned up:

```bash
# Delete existing role and its policies first
aws iam delete-role-policy --role-name "${ROLE_NAME}" --policy-name "${ROLE_NAME}-policy" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin
aws iam delete-role --role-name "${ROLE_NAME}" \
  --profile aws-sandbox-field-eng_databricks-sandbox-admin

# Then create fresh
```

### Workspace Stuck in Provisioning

Workspaces sometimes get stuck. Check status:

```bash
databricks account workspaces get --workspace-id <ID> --profile one-env-admin-aws
```

If stuck for >30 minutes, try deleting and recreating.

### Classic Workspace VPC Issues

If VPC was deleted but workspace exists, the workspace is likely non-functional. **Recommended: Start fresh** - delete the workspace and create a new one with a new VPC.

---

## Security Best Practices

1. **S3 Buckets**: Always block public access
2. **IAM Roles**: Use external ID in trust policy, least-privilege permissions
3. **IP ACLs**: Enable by default, only disable when explicitly needed for demo
4. **Credentials**: Never hardcode - use CLI profiles and SSO
5. **Cleanup**: Remove resources when done to minimize attack surface
