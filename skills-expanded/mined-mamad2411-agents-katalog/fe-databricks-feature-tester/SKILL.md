---
name: fe-databricks-feature-tester
description: Actually test whether Databricks features work by running real tests. Use this to try out features, verify they work in practice, check if something actually works, or validate feature behavior hands-on. Provisions infrastructure, executes test code, and documents results. Use this when you want to RUN a test, not just research whether something is supported.
user-invocable: true
---

# Databricks Feature Tester Skill

This skill performs comprehensive end-to-end testing of Databricks features, feature interactions (e.g., two features working together), or Databricks integration with external systems. It handles the complete workflow from research to infrastructure provisioning to test execution to documentation.

**Announce at start:** "I'm using the fe-databricks-feature-tester skill to test Databricks features."

## Overview

The feature testing workflow has four phases:

1. **Research & Planning** - Understand the feature and identify infrastructure requirements
2. **Parallel Setup** - Research implementation details while spinning up infrastructure
3. **Test Execution** - Run tests with clear success/failure criteria and remediation
4. **Documentation** - Write findings to a Google Doc

## Scope

**Supported Databricks Environments:**
- AWS workspaces (e2-demo, FE-VM, One-Env)
- Serverless and Classic compute

**Supported External Integrations:**
- Snowflake (via `fe-snowflake` skill)
- AWS services (S3, Glue, Kinesis, DynamoDB, MSK, RDS) via `aws-authentication` skill
- Public APIs and services (no auth required)

**Not Yet Supported:**
- Azure or GCP workspaces
- Non-AWS external cloud integrations

---

## Phase 1: Research & Infrastructure Planning

### Step 1.1: Understand the Feature(s) to Test

Parse the user's request to identify:

1. **Primary feature** - The main Databricks feature being tested
2. **Secondary features** - Related features or interactions being tested
3. **External integrations** - Non-Databricks systems involved
4. **Test scenarios** - What specific behaviors to validate

### Step 1.2: Research Using Glean

Use Glean MCP to gather initial context about the feature(s):

```bash
mcp-cli call glean/glean_read_api_call '{"endpoint": "search.query", "params": {"query": "<feature name> requirements configuration", "page_size": 20}}'
```

**Extract from research (examples - identify ALL relevant prerequisites for the specific feature):**
- Feature status (GA, Public Preview, Private Preview)
- Required DBR versions
- Required configurations (Photon, access mode, etc.)
- Feature flags that need enabling
- Cloud-specific limitations (AWS only, etc.)
- SDK version requirements
- Table format requirements (Delta, Iceberg, etc.)
- Unity Catalog requirements
- Compute requirements (serverless-only, classic-only, etc.)
- Networking requirements (VPC, PrivateLink, etc.)
- Any other feature-specific prerequisites discovered during research

### Step 1.3: Determine Infrastructure Requirements

Based on research, categorize the test requirements:

| Requirement | Infrastructure Choice |
|-------------|----------------------|
| Simple feature test, no integrations | e2-demo workspace |
| Feature test with Apps/Lakebase (no AWS integrations) | FE-VM Serverless workspace |
| Classic compute required (no AWS integrations) | FE-VM Classic workspace |
| **AWS resource integration (RDS, DynamoDB, Kinesis, Glue, MSK, etc.)** | **One-Env workspace** |
| Custom VPC/PrivateLink | One-Env workspace |
| Snowflake integration | FE-VM + Snowflake trial |

> **⚠️ CRITICAL: AWS Account Boundary Rule**
>
> When your test requires creating AWS resources (RDS, DynamoDB, Kinesis streams, MSK clusters, S3 buckets, etc.) that Databricks compute needs to access privately:
>
> **You MUST use One-Env workspace, NOT FE-VM.**
>
> **Why?**
> - AWS resources created via `aws-authentication` skill are in the **aws-sandbox account** (332745928618)
> - **One-Env workspaces** are deployed in the **same aws-sandbox account** - they can connect to these resources privately via VPC
> - **FE-VM workspaces** are in a **different AWS account** - they CANNOT privately connect to aws-sandbox resources
>
> **If you use FE-VM with aws-sandbox resources:**
> - The only way to connect would be exposing the resource to the public internet
> - This is a security risk and NOT allowed for databases (RDS, etc.)
> - The test will fail due to network connectivity issues
>
> **Examples requiring One-Env:**
> - Testing Lakeflow Connect with RDS MySQL/PostgreSQL
> - Testing DynamoDB integration
> - Testing Kinesis streaming ingestion
> - Testing MSK (Managed Kafka) connectivity
> - Testing cross-account S3 access patterns
> - Any test that creates AWS resources that Databricks needs to reach

### Step 1.4: Workspace Selection Decision Tree

```
FIRST: Does the test create or connect to AWS resources (RDS, DynamoDB, Kinesis, MSK, Glue, etc.)?
│
├── YES → **MUST use One-Env** (same AWS account as aws-sandbox)
│         (databricks-oneenv-workspace-deployment skill)
│         │
│         └── Do you need classic compute (custom VPC)?
│             ├── YES → One-Env Classic
│             └── NO → One-Env Serverless
│
└── NO → Does the test require custom VPC or PrivateLink?
         │
         ├── YES → Use One-Env workspace
         │
         └── NO → Does the test require Apps or Lakebase?
                  │
                  ├── YES → Use FE-VM Serverless (databricks-fe-vm-workspace-deployment skill)
                  │
                  └── NO → Does the test require classic compute?
                           │
                           ├── YES → Use FE-VM Classic (databricks-fe-vm-workspace-deployment skill)
                           │
                           └── NO → Is this a quick/simple test?
                                    ├── YES → Use e2-demo workspace (databricks-authentication skill)
                                    └── NO → Use FE-VM Serverless for isolation
```

**⚠️ DO NOT use FE-VM if you need to access AWS resources created in aws-sandbox!**

FE-VM and aws-sandbox are in **different AWS accounts**. Private networking is not possible between them.

### Step 1.5: Document Initial Plan

Create a test plan with:

1. **Features being tested** - List with descriptions
2. **Success criteria** - What defines a successful test
3. **Failure criteria** - What defines a failed test (distinguishing setup failures from feature failures)
4. **Infrastructure requirements** - Workspace type, external integrations
5. **Prerequisites to validate** - DBR version, configs, flags, etc.

---

## Phase 2: Parallel Research & Infrastructure Setup

Execute these in parallel where possible:

### Step 2.1: Deep Research (if needed)

For complex features or unclear implementation, invoke the product-question-research skill:

```
Task tool with subagent_type='fe-workflows:product-question-researcher' and model='opus'
Prompt: "Research how to implement/test <feature> including prerequisites, configurations, and code examples"
```

**Skip this step if:**
- The feature is well-documented and straightforward
- You already have clear implementation guidance from Phase 1 research
- The user provided detailed instructions

### Step 2.2: Provision Databricks Workspace

Based on the decision tree, invoke the appropriate skill:

**For e2-demo (existing shared workspace):**
```
/databricks-authentication
Select: e2-demo-west profile
```

**For FE-VM workspace:**
```
/databricks-fe-vm-workspace-deployment
```
- Check for existing suitable workspace first
- Deploy serverless or classic as needed

**For One-Env workspace:**
```
/databricks-oneenv-workspace-deployment
```
- Include AWS integration role setup
- Create necessary IAM permissions for integrations

### Step 2.3: Set Up External Integrations

**For Snowflake:**
```
/fe-snowflake
```
- Check for existing valid account
- Create new trial if needed
- Configure CLI connection

**For AWS resources (when using One-Env):**
The One-Env skill handles most AWS setup. For additional resources:
```
/aws-authentication
```
Then use AWS CLI or boto3 to create:
- S3 buckets
- DynamoDB tables
- Kinesis streams
- Glue databases/tables
- MSK clusters

### Step 2.4: Begin Test Code Development

While infrastructure provisions, start writing test code if:
- Implementation approach is clear from research
- No blocking dependencies on infrastructure details

---

## Phase 3: Test Execution Loop

**CRITICAL:** This phase uses the `databricks-feature-test-executor` agent for systematic test execution.

### Step 3.1: Define Success/Failure Criteria

Before running any tests, explicitly define:

**Success Criteria Example:**
- Query returns expected results
- Feature behaves as documented
- Integration data flows correctly
- No errors in logs

**Failure Criteria - Setup Issues (remediate these):**
- Missing permissions/IAM roles
- Wrong DBR version
- Feature flag not enabled
- SDK version mismatch
- Configuration not applied
- Network/connectivity issues

**Failure Criteria - Actual Feature Failure (report these):**
- Feature doesn't work as documented
- Unexpected behavior when properly configured
- Error even with correct setup
- Inconsistent results

### Step 3.2: Validate Prerequisites

**CRITICAL:** Before running tests, validate ALL prerequisites identified during Phase 1 research. The specific prerequisites vary by feature - identify them during research, don't assume a fixed list.

**Common prerequisites (examples - not exhaustive):**

| Prerequisite | Validation Method |
|--------------|-------------------|
| DBR Version | Check cluster/warehouse runtime version |
| Photon | Verify Photon is enabled on compute |
| Access Mode | Check cluster access mode (shared, single-user, etc.) |
| Feature Flag | Query workspace conf or contact PM |
| Serverless | Verify serverless compute is available |
| SDK Version | Check installed library versions |
| Cloud | Confirm workspace cloud (AWS/Azure/GCP) |
| Unity Catalog | Verify UC is enabled and configured |
| Permissions | Check user/SP has required grants |
| Table Properties | Check CDF, UniForm, liquid clustering, etc. |
| Workspace Settings | Check relevant workspace configurations |
| Network Config | Verify connectivity, VPC settings, etc. |

**Feature-specific prerequisites** should be discovered during research and added to this validation. Every feature has different requirements - the research phase should identify what matters for YOUR specific test.

**Document each validation result.**

### Step 3.3: Deploy Test Resources

Use the appropriate method for deploying test code/resources:

**For notebooks:**
```bash
databricks workspace import /path/to/notebook.py /Workspace/Users/<user>/feature-tests/ --profile <profile>
```

**For jobs:**
```bash
databricks jobs create --json @job_config.json --profile <profile>
```

**For SQL:**
```bash
databricks sql query execute --query "<sql>" --warehouse-id <id> --profile <profile>
```

**For bundles (complex deployments):**
```bash
databricks bundle deploy --profile <profile>
```

### Step 3.4: Execute Tests

Invoke the test executor agent:

```
Task tool with subagent_type='fe-workflows:databricks-feature-test-executor' and model='opus'
Prompt: |
  Execute the following feature test:

  **Feature:** <feature name>
  **Workspace:** <workspace URL>
  **Profile:** <databricks profile>

  **Success Criteria:**
  <list success criteria>

  **Prerequisites Validated:**
  <list prerequisite validation results>

  **Test Code/Commands:**
  <test commands or code to run>

  **How to Distinguish Setup vs Feature Failure:**
  <guidance on distinguishing>
```

### Step 3.5: Iterate on Failures

**If test fails due to setup issues:**
1. Identify the specific setup problem
2. Remediate (fix config, enable flag, install library, etc.)
3. Re-validate prerequisites
4. Re-run test
5. Repeat until confident setup is correct

**If test fails after setup is validated:**
1. Document the failure
2. Attempt alternative configurations if applicable
3. Determine if this is a bug, limitation, or expected behavior
4. Record confidence level in results

### Step 3.6: Record Results

For each test scenario, record:
- **Result:** PASS / FAIL / INCONCLUSIVE
- **Configuration:** Exact setup used
- **Evidence:** Logs, screenshots, query results
- **Confidence:** How confident are we in this result (1-10)
- **Notes:** Any observations or caveats

---

## Phase 4: Documentation

### Step 4.1: Compile Findings

Gather all test results into a structured format:

```markdown
# Feature Test Report: <Feature Name>

## Summary
- **Test Date:** YYYY-MM-DD
- **Tested By:** <user>
- **Overall Result:** PASS / FAIL / PARTIAL

## Features Tested
1. <Feature 1> - <brief description>
2. <Feature 2> - <brief description>

## Environment
- **Workspace:** <URL>
- **Workspace Type:** e2-demo / FE-VM Serverless / FE-VM Classic / One-Env
- **Region:** <region>
- **DBR Version:** <version>
- **Compute Type:** Serverless / Classic
- **Key Configurations:**
  - Photon: Yes/No
  - Access Mode: <mode>
  - Feature Flags: <list>

## External Integrations
- <Integration 1>: <details>

## Test Results

### Test 1: <Scenario Name>
- **Result:** PASS / FAIL
- **Configuration:** <specific config for this test>
- **Evidence:** <logs, output, screenshots>
- **Notes:** <observations>

### Test 2: <Scenario Name>
...

## Prerequisites Validation
| Prerequisite | Required | Actual | Status |
|--------------|----------|--------|--------|
| DBR Version | >=15.0 | 15.4 | ✅ |
| Photon | Yes | Yes | ✅ |
| ...

## Confidence Assessment
- **Confidence Level:** X/10
- **Why this rating:** <explanation>
- **What would increase confidence:** <suggestions>

## Known Limitations Discovered
- <limitation 1>
- <limitation 2>

## Recommendations
- <recommendation 1>
- <recommendation 2>
```

### Step 4.2: Create Google Doc

Use the google-docs skill to create a formatted report:

```
/google-docs create
Title: "Feature Test Report: <Feature Name> - YYYY-MM-DD"
Content: <compiled markdown from Step 4.1>
```

### Step 4.3: Report to User

Provide the user with:
1. Google Doc URL
2. Brief summary of results
3. Key findings and recommendations
4. Confidence level explanation

---

## Quick Reference: Skills Used

| Task | Skill |
|------|-------|
| Research implementation | `product-question-research` |
| FE-VM workspace | `databricks-fe-vm-workspace-deployment` |
| One-Env workspace | `databricks-oneenv-workspace-deployment` |
| e2-demo auth | `databricks-authentication` |
| Snowflake setup | `fe-snowflake` |
| AWS auth | `aws-authentication` |
| Create report | `google-docs` |
| Run queries | `databricks-query` |
| Deploy resources | `databricks-resource-deployment` |

---

## Example Invocations

### Example 1: Simple Feature Test
```
User: Test if materialized views support incremental refresh on Delta tables
→ Use e2-demo workspace
→ Create test Delta table with CDF enabled
→ Create materialized view
→ Validate incremental refresh works
→ Document findings
```

### Example 2: Feature Interaction Test
```
User: Test if Lakeflow Connect streams can write to Delta tables with UniForm enabled
→ Research both features and their interaction
→ Use FE-VM workspace (Lakeflow Connect requires it)
→ Set up streaming table with UniForm
→ Validate Iceberg reads work
→ Document results
```

### Example 3: External Integration Test
```
User: Test if Databricks can read from Snowflake Iceberg tables
→ Use FE-VM workspace + Snowflake trial
→ Set up Snowflake trial account
→ Create Iceberg table in Snowflake
→ Configure Databricks to read via Iceberg catalog
→ Validate data access
→ Document integration steps and results
```

### Example 4: AWS Integration Test (DynamoDB)
```
User: Test DynamoDB integration with Databricks using boto3
→ Use One-Env workspace (needs AWS IAM integration)
→ Create DynamoDB table via integration_resources.py
→ Test read/write from Databricks notebook
→ Clean up resources
→ Document results
```

### Example 5: AWS RDS Integration Test (Lakeflow Connect)
```
User: Test Lakeflow Connect MySQL connector with RDS
→ **MUST use One-Env workspace** (NOT FE-VM!)
  - RDS will be created in aws-sandbox account
  - One-Env is in same aws-sandbox account (can connect privately)
  - FE-VM is in different account (cannot connect without public internet exposure)
→ Use databricks-oneenv-workspace-deployment skill
→ Create RDS MySQL instance via integration_resources.py
→ Configure security group to allow Databricks IP ranges
→ Set up Lakeflow Connect MySQL source
→ Test CDC streaming
→ Document results
```

---

## Troubleshooting

### Cannot Connect to AWS Resources (RDS, DynamoDB, etc.)

If you're getting network/connectivity errors when trying to connect to AWS resources:

**Root Cause:** You likely used FE-VM workspace but the AWS resources are in the aws-sandbox account.

**Solution:**
1. AWS resources created via `aws-authentication` skill go into aws-sandbox account (332745928618)
2. FE-VM workspaces are in a **different** AWS account - they cannot privately reach aws-sandbox
3. You **must** use One-Env workspace for AWS resource integrations

**Fix:**
1. Delete the AWS resources if already created
2. Deploy a One-Env workspace using `/databricks-oneenv-workspace-deployment`
3. Recreate the AWS resources
4. Ensure security groups allow Databricks IP ranges (One-Env integration role handles this)

### Feature Flag Not Enabled
If a feature requires a flag that isn't enabled:
1. Document the flag name
2. Check if it can be enabled via workspace conf
3. If not, note that PM contact is required
4. Mark test as INCONCLUSIVE with clear explanation

### Wrong DBR Version
If tests fail due to DBR version:
1. Try different DBR versions (latest LTS, latest, etc.)
2. Document which versions work/don't work
3. Note minimum required version in report

### External Integration Authentication Failures
1. Verify credentials are correct and not expired
2. Check IAM role permissions
3. Verify network connectivity (VPC peering, security groups)
4. Document the authentication method used

### Inconsistent Results
If results are inconsistent:
1. Run test multiple times
2. Check for race conditions or timing issues
3. Look for resource contention
4. Document all variations observed

---

## Resources

- `fe-workflows/agents/databricks-feature-test-executor.md` - Test execution agent
- `fe-databricks-tools/skills/databricks-oneenv-workspace-deployment/resources/` - One-Env helpers
- `fe-databricks-tools/skills/databricks-fe-vm-workspace-deployment/resources/` - FE-VM helpers
