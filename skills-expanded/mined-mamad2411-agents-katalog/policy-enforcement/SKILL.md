# Policy-as-Code Generation & Enforcement Skill

## Overview
This skill guides the agent through generating OPA Rego policies from natural-language 
policy intents, testing them against Terraform plans, identifying violations, and 
auto-remediating by proposing code fixes.

## Workflow

### Step 1: Parse Policy Intent
- Receive a natural-language policy requirement (e.g., "All storage accounts must be encrypted at rest")
- Break it down into:
  - **Resource type**: What resource does this apply to? (e.g., `azurerm_storage_account`)
  - **Condition**: What must be true? (e.g., `encryption enabled`)
  - **Scope**: Where does this apply? (e.g., all environments, only production)
  - **Severity**: How critical is this? (e.g., `high`, `medium`, `low`)

### Step 2: Generate OPA Rego Policy
- Use the resource type and condition to produce a valid Rego policy
- Follow OPA conventions:
  - Package name: `policy.<category>.<resource_type>`
  - Rule name: `deny[msg]` for violations, `warn[msg]` for warnings
  - Include descriptive violation messages with resource identifiers
  - Add metadata comments: author, date, description, severity
- Reference `rego-examples/` for syntax patterns
- Validate generated Rego using `opa check` if available

### Step 3: Test Against Terraform Plans
- Use `opa_tester` tool to evaluate the policy against Terraform plan JSON files
- If no plan files provided, search the target repository for `*.tfplan.json` or generate from Terraform configs
- Parse test results to identify violations (resources that fail the policy)

### Step 4: Identify Violations
- For each violation, extract:
  - Resource name and type
  - File path and line number (if available)  
  - What's wrong (missing attribute, wrong value)
  - What the fix should be

### Step 5: Auto-Remediate (Optional)
- For each violation, generate a code fix:
  - Open the Terraform file containing the non-compliant resource
  - Add or modify the required attributes
  - Ensure the fix doesn't break other configurations
- Create a new branch and commit the fixes
- Open a pull request with:
  - Title: "fix: enforce <policy_name> compliance"
  - Body: list of violations found and fixes applied
  - Reference to the policy file

### Step 6: Commit Policy
- Save the new Rego policy to the policy repository (e.g., `policies/<category>/<policy_name>.rego`)
- Include a corresponding test file (`policies/<category>/<policy_name>_test.rego`)
- Create a PR for the new policy itself if not auto-merging

---

## OPA Rego Conventions

### Package Naming
```rego
package policy.storage.encryption
```

### Deny Rules (Violations)
```rego
deny[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "azurerm_storage_account"
    not resource.values.enable_https_traffic_only
    msg := sprintf("Storage account '%s' must enforce HTTPS-only traffic", [resource.name])
}
```

### Warn Rules (Advisory)
```rego
warn[msg] {
    resource := input.planned_values.root_module.resources[_]
    resource.type == "azurerm_storage_account"
    not resource.values.tags["environment"]
    msg := sprintf("Storage account '%s' is missing 'environment' tag", [resource.name])
}
```

### Metadata Comments
```rego
# METADATA
# title: Require encryption at rest for storage accounts
# description: All Azure storage accounts must have encryption at rest enabled
# severity: high
# author: compliance-agent
# date: 2026-01-01
# framework: PCI-DSS
# controls: ["3.5", "4.1"]
```

### Test Files
```rego
package policy.storage.encryption_test

import data.policy.storage.encryption

test_deny_unencrypted_storage {
    result := encryption.deny with input as {"planned_values": {"root_module": {"resources": [
        {"type": "azurerm_storage_account", "name": "bad_storage", "values": {}}
    ]}}}
    count(result) > 0
}

test_allow_encrypted_storage {
    result := encryption.deny with input as {"planned_values": {"root_module": {"resources": [
        {"type": "azurerm_storage_account", "name": "good_storage", "values": {"enable_https_traffic_only": true}}
    ]}}}
    count(result) == 0
}
```

---

## Common Policy Patterns

### Encryption Policies
- storage encryption at rest
- TLS minimum version enforcement
- HTTPS-only traffic
- database TDE (Transparent Data Encryption)
- disk encryption

### Network Policies
- no public IPs on internal resources
- NSG rules restricting inbound access  
- require private endpoints for PaaS services
- VNet integration required

### Access Control Policies
- RBAC role restrictions (no Owner role on subscriptions)
- managed identity required (no password-based auth)
- key expiration policies
- no shared access keys

### Tagging Policies
- required tags (environment, owner, cost-center)
- tag value validation (environment must be dev/staging/prod)

### Logging Policies
- diagnostic settings required
- audit logging enabled
- log retention minimum days

---

## Error Handling
- If Rego generation fails `opa check`, review the error, fix syntax, and retry
- If violations found but auto-fix is uncertain, output the violation list with recommended manual fixes
- If Terraform plan is unavailable, generate policy only and skip testing step
- Always validate generated Rego against at least one positive and one negative test case

## Output Format
Present results as:
1. **Policy file**: the generated `.rego` file content
2. **Test file**: the generated `_test.rego` file content  
3. **Violations found**: list of non-compliant resources (if tested)
4. **Fixes applied**: list of code changes made (if auto-remediated)
5. **PR link**: link to the created pull request (if committed)
