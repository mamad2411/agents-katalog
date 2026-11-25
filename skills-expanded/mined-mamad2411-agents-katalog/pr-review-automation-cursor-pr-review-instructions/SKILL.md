# Daily PR Review Instructions

## Overview
This document provides step-by-step instructions for performing comprehensive PR reviews using Azure MCP tools, GitHub integration, and CircleCI MCP to identify potential production issues before merging.

## Prerequisites
- Access to Azure MCP tools
- GitHub Copilot MCP integration
- CircleCI MCP integration
- Azure CLI access to production resources
- Understanding of Displayr infrastructure
- CircleCI project access and permissions

## Daily PR Review Process

### Step 1: Get Pending Reviews
```bash
# Use GitHub MCP to list all pending reviews
mcp_github-copilot-mcp_list_notifications
```

### Step 2: Categorize PRs
**Infrastructure/Deployment PRs (displayr-deploy):**
- Check for domain/endpoint changes
- Verify certificate migrations
- Validate deployment system changes
- Review Azure resource modifications
- Check CircleCI pipeline configurations

**Dependabot PRs (all services):**
- Verify version compatibility
- Check for breaking changes
- Validate patch/minor version updates
- Check CircleCI build status and test results

**Service-specific PRs:**
- Review code changes
- Check for configuration changes
- Validate dependency updates
- Verify CircleCI pipeline health

### Step 3: CircleCI Pipeline Verification

#### For All PRs:
1. **Check Pipeline Status:**
   ```bash
   mcp_circleci_get_latest_pipeline_status --params '{"projectSlug": "gh/Displayr/[REPO]", "branch": "[BRANCH_NAME]"}'
   ```

2. **Get Test Results:**
   ```bash
   mcp_circleci_get_job_test_results --params '{"projectSlug": "gh/Displayr/[REPO]", "branch": "[BRANCH_NAME]", "filterByTestsResult": "failure"}'
   ```

3. **Check for Flaky Tests:**
   ```bash
   mcp_circleci_find_flaky_tests --params '{"projectSlug": "gh/Displayr/[REPO]"}'
   ```

4. **Validate CircleCI Configuration:**
   ```bash
   mcp_circleci_config_helper --params '{"configFile": "[CIRCLECI_CONFIG_CONTENT]"}'
   ```

#### For Infrastructure Changes:
1. **Check Deployment Pipeline Health:**
   ```bash
   mcp_circleci_get_latest_pipeline_status --params '{"projectSlug": "gh/Displayr/displayr-deploy", "branch": "[BRANCH_NAME]"}'
   ```

2. **Verify Infrastructure Tests:**
   ```bash
   mcp_circleci_get_job_test_results --params '{"projectSlug": "gh/Displayr/displayr-deploy", "branch": "[BRANCH_NAME]"}'
   ```

### Step 4: Azure Resource Verification

#### For Infrastructure Changes:
1. **Azure Front Door + DNS reality check:**
   - Front Door domain state alone isn’t decisive; confirm whether any public DNS records actually resolve to those domains before inferring impact.
   - Prefer a single verification outcome: “domains are unused” backed by DNS + routing evidence.
   ```bash
   # Inspect AFD config (context only)
   mcp_azure_extension_az afd profile list --output table
   mcp_azure_extension_az afd custom-domain list --profile-name dip-prod-shared-fd-profile --resource-group dip-prod-shared-rg --output table

   # Check endpoints and routes
   mcp_azure_extension_az afd endpoint list --profile-name dip-prod-shared-fd-profile --resource-group dip-prod-shared-rg --output table
   mcp_azure_extension_az afd route list --profile-name dip-prod-shared-fd-profile --resource-group dip-prod-shared-rg --endpoint-name [ENDPOINT] --output table
   ```

2. **Confirm no active DNS resolution (required for removal):**
   - Verify there are no A, AAAA, or CNAME records pointing to the Front Door domains slated for removal.
   - If no DNS records resolve, Front Door state may be irrelevant for production impact.
   ```bash
   # Example lookups (replace with actual domains)
   run_terminal_cmd "dig +short example.domain.com"
   run_terminal_cmd "dig +short CNAME example.domain.com"
   ```

3. **Check Resource Groups:**
   ```bash
   mcp_azure_extension_az group list --output table
   mcp_azure_extension_az resource list --resource-group [RG_NAME] --output table
   ```

#### For Deployment System Changes:
1. **Verify Current Deployment Resources:**
   ```bash
   mcp_azure_extension_az resource list --resource-group displayr-deploy-rg --output table
   ```

2. **Check Service Principals and Permissions:**
   ```bash
   mcp_azure_extension_az role assignment list --scope [RESOURCE_ID] --output table
   ```

### Step 5: PR Analysis

#### Get PR Details:
```bash
mcp_github-copilot-mcp_get_pull_request --owner Displayr --repo [REPO] --pullNumber [NUMBER]
```

#### Get PR Diffs:
```bash
mcp_github-copilot-mcp_get_pull_request_diff --owner Displayr --repo [REPO] --pullNumber [NUMBER]
```

### Step 6: Risk Assessment

#### High Risk Indicators:
- **Domain/Endpoint Removal:** Check if domains are actively used
- **Certificate Changes:** Verify migration compatibility
- **Deployment System Changes:** Confirm new system readiness
- **Major Version Updates:** Check for breaking changes
- **Permission Changes:** Verify access requirements
- **CircleCI Pipeline Failures:** Check for failing builds or tests
- **Flaky Tests:** Identify unstable test patterns

#### Medium Risk Indicators:
- **Minor Version Updates:** Review changelog for breaking changes
- **Configuration Changes:** Validate impact on services
- **Health Check Changes:** Test endpoint compatibility
- **CircleCI Configuration Changes:** Validate pipeline modifications
- **Test Coverage Changes:** Assess impact on quality gates

#### Low Risk Indicators:
- **Patch Version Updates:** Standard maintenance
- **Code Refactoring:** No functional changes
- **Documentation Updates:** No operational impact
- **CircleCI Pipeline Success:** All tests passing
- **Minor Configuration Updates:** Non-breaking changes

### Step 7: Comment Strategy

#### For Safe PRs (neutral, succinct):
- Add an approval comment with a brief verification summary and the key reason it’s safe (e.g., non-functional refactor, patch-level update, all tests passing).
- Include 1–2 lines of objective evidence (e.g., CI status, scope of diff).
- Mark as “Approved – safe to merge”.
- Add "Comment added by Cursor AI" attribution.

#### For PRs Requiring Verification (single ask):
- Use a neutral tone; avoid alarmist language.
- Provide a one-line concern and 1–2 lines of evidence you already checked.
- Include a single verification ask: list only the minimal facts required to decide (3–5 bullets max).
- Recommend: “Hold merge pending verification.”

### Step 8: Documentation

#### Update TODO List:
```bash
todo_write --merge true --todos [{"id": "pr_review_complete", "content": "Daily PR review completed", "status": "completed"}]
```

#### Record Findings:
- Document any critical issues found
- Note PRs that require follow-up
- Track verification requests made

## Critical Checkpoints

### Before Approving Any PR:
1. ✅ Verify no active production resources are being removed
2. ✅ Confirm all dependencies are properly migrated
3. ✅ Validate rollback plans exist
4. ✅ Check for breaking changes in dependencies
5. ✅ Ensure new systems are tested and ready
6. ✅ Verify CircleCI pipelines are passing
7. ✅ Check for any failing tests or flaky test patterns
8. ✅ Validate CircleCI configuration changes

### Red Flags (Hold Approval)
- 🚨 Removing active domains without verification
- 🚨 Breaking deployment systems without replacement
- 🚨 Major version updates without testing
- 🚨 Permission changes without validation
- 🚨 Certificate changes without compatibility check
- 🚨 CircleCI pipeline failures or broken builds
- 🚨 Significant increase in flaky tests
- 🚨 CircleCI configuration changes without validation

## Generic Verification Framework

Use this structure across all issue types (infrastructure, dependencies, services, CI):

1) Concern (1 line):
   - Example: “Potential impact to live traffic if endpoint X is removed.”

2) Evidence checked (1–2 lines):
   - What you already verified (e.g., CI status, code paths touched, config diffs).

3) Verification ask (single set of checks, 3–5 bullets max):
   - Define the minimal facts needed to decide. Examples:
     - Dependencies: Confirm no breaking API usage; link to changelog; confirm tests cover critical paths.
     - Infrastructure: Confirm unused resources (no references/traffic); confirm replacement exists and is validated.
     - Service changes: Confirm backward compatibility; confirm config/feature flag rollout plan; confirm health checks pass.
     - Permissions: Confirm principle-of-least-privilege; confirm scope matches intended resources.

4) Decision rule (1 line):
   - Example: “If all checks pass, proceed; otherwise, hold merge and address gaps.”

## Tools Reference

### Azure MCP Commands:
- `mcp_azure_extension_az` - Azure CLI operations
- `mcp_azure_*` - Specific Azure service operations

### GitHub MCP Commands:
- `mcp_github-copilot-mcp_get_pull_request` - Get PR details
- `mcp_github-copilot-mcp_get_pull_request_diff` - Get PR changes
- `mcp_github-copilot-mcp_add_issue_comment` - Add review comments
- `mcp_github-copilot-mcp_list_notifications` - List pending reviews

### CircleCI MCP Commands:
- `mcp_circleci_get_latest_pipeline_status` - Check pipeline status
- `mcp_circleci_get_job_test_results` - Get test results and failures
- `mcp_circleci_find_flaky_tests` - Identify flaky test patterns
- `mcp_circleci_config_helper` - Validate CircleCI configuration
- `mcp_circleci_list_followed_projects` - List available projects
- `mcp_circleci_run_pipeline` - Trigger new pipeline runs
- `mcp_circleci_rerun_workflow` - Rerun failed workflows

### Utility Commands:
- `todo_write` - Track review progress
- `web_search` - Research breaking changes
- `run_terminal_cmd` - Execute system commands

## Emergency Procedures

### If Critical Issue Found:
1. **Immediately add blocking comment**
2. **Notify team via Slack/Teams**
3. **Document issue in incident log**
4. **Create follow-up task for resolution**

### If Production Issue Suspected:
1. **Block PR merge immediately**
2. **Escalate to infrastructure team**
3. **Prepare rollback procedures**
4. **Schedule emergency review meeting**

## Quality Assurance

### Review Checklist:
- [ ] All active resources verified
- [ ] Dependencies checked
- [ ] Breaking changes identified
- [ ] Rollback plans confirmed
- [ ] CircleCI pipelines verified
- [ ] Test results reviewed
- [ ] Flaky tests identified
- [ ] Comments added with clear recommendations
- [ ] TODO list updated
- [ ] Documentation completed

### Weekly Review:
- Analyze patterns in PR issues
- Update review procedures
- Refine risk assessment criteria
- Improve automation where possible
