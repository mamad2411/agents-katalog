---
name: genie-request
description: Automate AMS workspace access requests with browser automation (auto-approved, no Slack needed)
---

# AMS Workspace Access Request Skill

Automates the AMS (Approval Management System) workspace access request workflow. Fills the form at `https://ams.internal.azuredatabricks.net/approval-entries/create`, submits it, and the request is auto-approved. No Slack approval posting required.

## When to Use This Skill

Use this skill when you need to:
- Request workspace access through AMS
- Skip manual form filling on the AMS portal

**Note**: Use `/genie-case` first if you need to create a Salesforce case. Or just say you don't have one yet during this skill and it will create one for you.

## Prerequisites

- Chrome browser with Chrome DevTools MCP enabled
- Authenticated to AMS (`https://ams.internal.azuredatabricks.net/`) via Okta/SSO

## Instructions

### Step 1: Gather User Inputs

Prompt the user for the required information:

#### Workspace ID

```
Workspace ID (numeric only): [wait for user input]
```

**Validation:**
- Must be numeric only
- If invalid: "Please provide the workspace ID only (numeric value like 2143836972759139)"

#### Cloud Provider (Auto-Detected)

Auto-detect the cloud provider from the workspace ID using the logfood skill. Run a query against `main.centralized_system_tables.account_workspace_mappings` to look up the workspace:

```bash
# Use the logfood-querier or execute_sql to look up cloud provider
# Query: SELECT cloud, workspace_id FROM main.centralized_system_tables.account_workspace_mappings WHERE workspace_id = '<WORKSPACE_ID>'
```

Use the `/fe-internal-tools:logfood-querier` skill or `mcp__plugin_databricks-ai-dev-kit_databricks__execute_sql` to run this query.

**Map the result to AMS values:**
- `cloud` = "aws" -> `CLOUD_PROVIDER` = "AWS"
- `cloud` = "azure" -> `CLOUD_PROVIDER` = "AZURE"
- `cloud` = "gcp" -> `CLOUD_PROVIDER` = "GCP"

Display to user:
```
Cloud Provider: ${CLOUD_PROVIDER} (auto-detected)
```

**Fallback:** If the lookup fails, ask the user:
```
Could not auto-detect cloud provider. Cloud Provider (AWS / AZURE / GCP): [wait for user input]
```

**Validation (fallback only):**
- Must be one of: AWS, AZURE, GCP (case-insensitive, normalize to uppercase)

#### Justification Type

```
Justification type - (1) Salesforce Ticket or (2) JIRA ES Ticket: [wait for user input]
```

#### Ticket / Case Number

Based on justification type:

**If Salesforce Ticket:**
```
Salesforce case number (or "new" to create one): [wait for user input]
```

- If user provides a case number: validate format (e.g., "00849424"), check case is open/active
- If user says "new", "none", "don't have one", or similar: **invoke `/genie-case` to create a Salesforce case first**, then use the returned case number automatically as `TICKET_NUMBER`
- If validation fails: "Case [NUMBER] is already closed/solved. Please use a different case number."

**If JIRA ES Ticket:**
```
JIRA ES ticket number (e.g., ES-123456): [wait for user input]
```

- Validate format starts with "ES-" followed by digits
- If invalid: "Please provide a valid ES ticket number (e.g., ES-123456)"

#### Additional Justification

```
Brief justification for workspace access: [wait for user input]
```

Free text. Required field.

#### Requested TTL

```
Requested TTL: 8 hours (default) - Is this OK? (y/n): [wait for user input]
```

If no:
```
Select TTL: 1 hour / 2 hours / 4 hours / 8 hours / 12 hours / 24 hours: [wait for user input]
```

**Store inputs in variables:**
- `WORKSPACE_ID` - Numeric workspace ID
- `CLOUD_PROVIDER` - AWS, AZURE, or GCP (auto-detected, fallback to user input)
- `JUSTIFICATION_TYPE` - "JIRA Ticket" or "Salesforce Ticket"
- `TICKET_NUMBER` - ES ticket or Salesforce case number
- `ADDITIONAL_JUSTIFICATION` - Free text justification
- `TTL` - Requested TTL (default: "8 hours")
- `USER_EMAIL` - Current user's email (from Step 2)

---

### Step 2: Get Current User Email

Determine the current user's email:

```bash
# Try getting from Salesforce CLI first
USER_EMAIL=$(sf org display --json 2>/dev/null | jq -r '.result.username')

# If that fails, try git config
if [ -z "$USER_EMAIL" ]; then
  USER_EMAIL=$(git config user.email)
fi
```

Display to user:
```
Using email: ${USER_EMAIL}
```

---

### Step 3: Open AMS and Navigate to Create Form

Use Chrome DevTools MCP to open AMS:

```
1. Check if AMS page is already open
2. If not, create new page: https://ams.internal.azuredatabricks.net/approval-entries/create
3. Wait for authentication to complete
4. Take snapshot to verify form is loaded
```

**Commands:**
- `mcp__chrome-devtools__list_pages` - Check existing pages
- `mcp__chrome-devtools__new_page` - Open AMS if needed
- `mcp__chrome-devtools__take_snapshot` - Verify form loaded

**Expected form elements:**
- Application dropdown (default: "Workspace Access")
- Workspace ID text input
- Environment dropdown (default: "PROD")
- Cloud Provider dropdown
- Regulatory Domain dropdown (disabled, default: "PUBLIC")
- Justification Type dropdown
- Ticket/case text input
- Additional Justification textarea
- Requested TTL dropdown (default: "8 hours")
- "Submit Request" button

---

### Step 4: Fill AMS Form

Use Chrome DevTools to fill each field. Take a snapshot first to get field UIDs.

**Implementation:**

```javascript
// 1. Take snapshot to get UIDs
mcp__chrome-devtools__take_snapshot
```

**4a. Verify defaults (no action needed):**
- Application should show "Workspace Access"
- Environment should show "PROD"
- Regulatory Domain should show "PUBLIC" (disabled)

**4b. Fill Workspace ID:**
```javascript
// Find textbox for "Workspace ID" in snapshot, note its uid
mcp__chrome-devtools__fill(uid=<WORKSPACE_ID_UID>, value=<WORKSPACE_ID>)
```

**4c. Select Cloud Provider (dropdown):**

Dropdowns require a click-snapshot-click pattern:
```javascript
// 1. Find the Cloud Provider dropdown/combobox element in snapshot
// 2. Click it to open the options
mcp__chrome-devtools__click(uid=<CLOUD_PROVIDER_DROPDOWN_UID>)

// 3. Take fresh snapshot to see the dropdown options
mcp__chrome-devtools__take_snapshot

// 4. Find the option matching CLOUD_PROVIDER (e.g., "AWS")
mcp__chrome-devtools__click(uid=<AWS_OPTION_UID>)
```

**4d. Select Justification Type (dropdown):**

Same click-snapshot-click pattern:
```javascript
// 1. Find Justification Type dropdown
mcp__chrome-devtools__click(uid=<JUSTIFICATION_TYPE_DROPDOWN_UID>)

// 2. Fresh snapshot
mcp__chrome-devtools__take_snapshot

// 3. Click matching option ("JIRA Ticket" or Salesforce option)
mcp__chrome-devtools__click(uid=<JUSTIFICATION_OPTION_UID>)

// 4. IMPORTANT: Take another snapshot after selection
//    The form may change fields based on justification type
mcp__chrome-devtools__take_snapshot
```

**4e. Fill Ticket/Case Number:**
```javascript
// After justification type snapshot, find the ticket input field
// For JIRA: look for input near "JIRA Tickets" label
// For Salesforce: look for input near Salesforce case label
mcp__chrome-devtools__fill(uid=<TICKET_INPUT_UID>, value=<TICKET_NUMBER>)
```

**4f. Fill Additional Justification:**
```javascript
// Find the textarea for "Additional Justification"
mcp__chrome-devtools__fill(uid=<JUSTIFICATION_TEXTAREA_UID>, value=<ADDITIONAL_JUSTIFICATION>)
```

**4g. Select Requested TTL (dropdown, only if not default "8 hours"):**

If TTL is not "8 hours":
```javascript
mcp__chrome-devtools__click(uid=<TTL_DROPDOWN_UID>)
mcp__chrome-devtools__take_snapshot
mcp__chrome-devtools__click(uid=<TTL_OPTION_UID>)
```

**4h. Verify all fields:**
```javascript
// Take final snapshot to confirm everything is filled correctly
mcp__chrome-devtools__take_snapshot
```

**Note:** UIDs change between page loads. Always get fresh UIDs from each snapshot.

---

### Step 5: Submit Form

Click the "Submit Request" button. This is a standard `button` element visible in normal snapshots (no verbose snapshot needed).

```javascript
// 1. Find button "Submit Request" in the snapshot from Step 4h
//    It appears as: button "Submit Request"

// 2. Click the button
mcp__chrome-devtools__click(uid=<SUBMIT_BUTTON_UID>)

// 3. Wait for submission
sleep 4

// 4. Check result
mcp__chrome-devtools__take_snapshot
mcp__chrome-devtools__take_screenshot  // Visual verification
```

**Expected results after submission:**

**Case 1: Success (auto-approved)**
- Page shows confirmation/success message
- Access is granted immediately

**Case 2: Error**
- Error message displayed on page
- Form may remain visible for correction

---

### Step 6: Display Results

**For successful submission:**

The result page shows status "APPROVED" with a "Login to Workspace" button and request details. Extract the request ID from the page URL (pattern: `https://ams.internal.azuredatabricks.net/approval-entries/<REQUEST_ID>`).

```
AMS Request Submitted - Auto-Approved!

Request Details:
  Request ID:      ${REQUEST_ID}
  Workspace ID:    ${WORKSPACE_ID}
  Cloud Provider:  ${CLOUD_PROVIDER}
  Environment:     PROD
  Justification:   ${JUSTIFICATION_TYPE} ${TICKET_NUMBER}
  TTL:             ${TTL}
  Access Expires:  [from page: "ACCESS EXPIRES" field]

Status: Auto-approved. Access granted.
Click "Login to Workspace" in your browser to access the workspace.
```

**For errors:**
```
AMS Request Failed

Error: [display error message from page]

Common issues:
- Invalid workspace ID
- Missing required fields (justification, ticket number)
- Network or authentication error

Please fix the issue and try again.
```

---

## Error Handling

| Error Scenario | Detection | Response |
|----------------|-----------|----------|
| Not authenticated to AMS | Redirect to Okta/SSO login | "Please log in to AMS first, then re-run this skill" |
| Chrome not running | MCP connection error | "Please ensure Chrome is running with DevTools enabled" |
| Form not loaded | Missing expected elements | "Could not find AMS form. Please verify page loaded correctly" |
| Invalid workspace ID | Contains non-numeric chars | Re-prompt with validation message |
| Cloud provider lookup fails | Logfood query returns no results | Fall back to asking the user |
| Dropdown option not found | Option missing from snapshot | "Could not find option in dropdown. Try manually selecting it" |
| Submit failed | No result page after click | "Form submission failed. Please try manually" |
| Case already closed | Validation error | Display error, suggest using a different case number |

---

## Field Reference

| Field | Value | Source |
|-------|-------|--------|
| Application | "Workspace Access" | Default (no change) |
| Workspace ID | User input | Step 1 |
| Environment | "PROD" | Default (no change) |
| Cloud Provider | Auto-detected or user input (AWS/AZURE/GCP) | Step 1 |
| Regulatory Domain | "PUBLIC" | Default (disabled) |
| Justification Type | User input (JIRA Ticket / Salesforce) | Step 1 |
| Ticket/Case # | User input or from /genie-case | Step 1 |
| Additional Justification | User input | Step 1 |
| Requested TTL | User input or "8 hours" | Step 1 |

---

## Example Usage

**User invokes skill:**
```
/genie-request
```

**Example with Salesforce ticket:**
1. Workspace ID: "7474660626058020"
2. Cloud Provider: AWS (auto-detected)
3. Justification: Salesforce Ticket
4. Case number: "00875728"
5. Justification text: "Troubleshooting S3 ingestion issue for customer"
6. TTL: 8 hours (default)
7. Opens AMS, fills form, submits
8. Auto-approved!

**Example with JIRA ticket:**
1. Workspace ID: "1567431796348938"
2. Cloud Provider: AZURE (auto-detected)
3. Justification: JIRA Ticket
4. Ticket: "ES-123456"
5. Justification text: "Investigating cluster startup failure"
6. TTL: 4 hours
7. Opens AMS, fills form, submits
8. Auto-approved!

**Example creating a new case on the fly:**
1. Workspace ID: "9876543210"
2. Cloud Provider: GCP (auto-detected)
3. Justification: Salesforce Ticket
4. Case number: "new" --> invokes /genie-case, gets back "00874001"
5. Justification text: "Customer onboarding support"
6. TTL: 8 hours (default)
7. Opens AMS, fills form, submits
8. Auto-approved!

---

## Chrome DevTools MCP Reference

**Available tools:**
- `mcp__chrome-devtools__list_pages` - List open browser pages
- `mcp__chrome-devtools__new_page` - Open new page
- `mcp__chrome-devtools__navigate_page` - Navigate to URL
- `mcp__chrome-devtools__select_page` - Switch to specific page
- `mcp__chrome-devtools__take_snapshot` - Get page element tree (use `verbose=true` for hidden elements)
- `mcp__chrome-devtools__take_screenshot` - Capture visual screenshot
- `mcp__chrome-devtools__fill` - Fill form field
- `mcp__chrome-devtools__click` - Click element

**Snapshot element format:**
```
uid=X_Y ElementType "Label" attribute="value"
```

**Dropdown interaction pattern:**
```
1. Click dropdown element to open it
2. Take fresh snapshot to see option elements
3. Click the desired option
4. (Optional) Take snapshot to verify selection and check for form changes
```

---

## Known Limitations

1. **Requires manual authentication** - User must complete Okta/SSO auth before automation starts
2. **Browser must be running** - Chrome with DevTools MCP must be active
3. **Dropdown interactions may break** if AMS UI changes its component library
4. **No batch request support** - One workspace at a time

---

## Future Enhancements (Out of Scope)

- Support batch requests for multiple workspaces
- Cache frequently used workspace IDs
- Support other Application types beyond "Workspace Access"

---

## Testing Checklist

- [ ] User input validation (workspace ID, ticket format)
- [ ] Cloud provider auto-detection from logfood works
- [ ] Email detection works (Salesforce CLI + git config fallback)
- [ ] /genie-case integration works when user says "new"
- [ ] Browser opens to AMS create form
- [ ] All dropdown selections work (Cloud Provider, Justification Type, TTL)
- [ ] Justification type change updates form correctly
- [ ] Text fields fill correctly (Workspace ID, ticket, justification)
- [ ] Submit button clicks successfully
- [ ] Success message displays all details
- [ ] Error handling for each failure scenario
