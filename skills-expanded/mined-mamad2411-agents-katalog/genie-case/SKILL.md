---
name: genie-case
description: Create Salesforce cases for Genie workspace access requests with proper field population
---

# Genie Request Case Creation Skill

Automates Salesforce case creation for Genie workspace access requests. This skill eliminates manual case creation and ensures consistent formatting across all Genie request cases.

## When to Use This Skill

Use this skill when you need to:
- Create a Salesforce case for requesting Genie workspace access
- File a Genie access request with proper case fields
- Document a customer's Genie workspace access request

## Instructions

### Step 1: Verify Salesforce Authentication

Check if authenticated with Salesforce:

```bash
sf org display --json
```

**If not authenticated or if the command fails:**
- Direct the user to run `/salesforce-authentication` skill first
- Exit this skill and wait for authentication to complete

**If authenticated:**
- Display org details: username, org ID, and instance URL
- Proceed to Step 2

---

### Step 2: Discover Required Field Values

Query the example case to discover Type and BusinessHoursId values that should be used for Genie cases.

#### Query Example Case

```bash
# Get Type and BusinessHoursId from the example Genie case
sf data query --query "SELECT Type, BusinessHoursId, Subject, Description FROM Case WHERE Id = '500Vp00000mjIYMIA2'" --json
```

#### Get Default Business Hours (Fallback)

If the example case query fails or BusinessHoursId is null:

```bash
sf data query --query "SELECT Id, Name FROM BusinessHours WHERE IsDefault = true LIMIT 1" --json
```

#### Search for DBC Access Custom Field

```bash
# Query all custom fields from the example case to find DBC Access field
sf data query --query "SELECT FIELDS(CUSTOM) FROM Case WHERE Id = '500Vp00000mjIYMIA2'" --json | jq -r '.result.records[0]' | grep -i "dbc\|access"
```

**Display discovered values to the user:**

```
✓ Case Type: [discovered Type value or "Customer Success" if not found]
✓ Business Hours: [discovered BusinessHoursId or default]
✓ DBC Access Field: [field name if found, or "Not found - will need manual check"]
```

**Store these values in variables for later use:**
- `CASE_TYPE` - From example or default to "Customer Success"
- `BUSINESS_HOURS_ID` - From example or default BusinessHours
- `DBC_ACCESS_FIELD` - Field API name if found (likely `DBC_Access_Granted_By_Customer__c`)

---

### Step 3: Gather User Inputs

Prompt the user for the required information. Use interactive prompts for each field.

#### Customer Name

```
Customer name: [wait for user input]
```

**Validation:**
- Cannot be empty
- If empty, re-prompt: "Customer name is required. Please provide the customer name:"

#### Workspace ID

```
Workspace ID (numeric only, not URL): [wait for user input]
```

**Validation:**
- Must be numeric only (no URLs, no letters)
- Remove any URL prefixes if provided (e.g., "https://..." should be rejected)
- If validation fails: "Please provide the workspace ID only (numeric value like 123456), not a URL"

**Example valid inputs:** `123456`, `7890123`
**Example invalid inputs:** `https://example.com/workspace/123`, `ws-123`, `workspace123`

#### Reasoning

```
Reasoning for Genie access request (can be multiple lines, press Enter twice when done):
[wait for user input]
```

**Validation:**
- Cannot be empty
- If empty, re-prompt: "Reasoning is required for Genie requests. Please explain why access is needed:"

**Store inputs in variables:**
- `CUSTOMER_NAME` - User-provided customer name
- `WORKSPACE_ID` - Validated numeric workspace ID
- `USER_REASONING` - User-provided reasoning text

---

### Step 4: Account Lookup with Fuzzy Matching

Search for the customer account using fuzzy LIKE matching.

```bash
# Fuzzy search for account (handles partial/misspelled names)
sf data query --query "SELECT Id, Name, Type, Owner.Name FROM Account WHERE Name LIKE '%${CUSTOMER_NAME}%' ORDER BY Name LIMIT 10" --json
```

#### Handle Results Based on Match Count

**0 matches found:**
```
❌ No account found matching "${CUSTOMER_NAME}"

Suggestions:
- Check the exact account name in Salesforce
- Try searching with fewer words (e.g., "Acme" instead of "Acme Corporation")
- Verify spelling

Would you like to:
1. Try a different search term
2. Exit and look up the account manually
```

If user chooses option 1, go back to Step 3 (Customer Name input).
If user chooses option 2 or says no, exit the skill gracefully.

**1 match found:**
```
✓ Found account: ${ACCOUNT_NAME} (ID: ${ACCOUNT_ID})
  Type: ${ACCOUNT_TYPE}
  Owner: ${OWNER_NAME}
```

Auto-select this account and proceed to Step 5.
Store `ACCOUNT_ID` and `ACCOUNT_NAME` variables.

**Multiple matches found (2-10):**

Display numbered list:
```
Found ${COUNT} matching accounts:

  1. ${ACCOUNT_1_NAME} (${ACCOUNT_1_TYPE}) - Owner: ${OWNER_1_NAME}
  2. ${ACCOUNT_2_NAME} (${ACCOUNT_2_TYPE}) - Owner: ${OWNER_2_NAME}
  3. ...

Select account (1-${COUNT}): [wait for user input]
```

**Validation:**
- Must be a number between 1 and the count of results
- If invalid: "Please select a number between 1 and ${COUNT}:"

Store selected `ACCOUNT_ID` and `ACCOUNT_NAME` variables.

---

### Step 5: Create Genie Request Case

Construct and execute the case creation command with all discovered and user-provided values.

#### Build Case Description

Format the description field to include only the reasoning (workspace ID goes in its own field):

```
Description: ${USER_REASONING}
```

#### Execute Case Creation

```bash
# Create the Genie request case with all fields
sf data create record --sobject Case --values "\
  Subject='Genie Request for ${ACCOUNT_NAME}' \
  Description='${USER_REASONING}' \
  Priority=Normal \
  Origin=Email \
  Type='${CASE_TYPE}' \
  Status=New \
  AccountId=${ACCOUNT_ID} \
  BusinessHoursId=${BUSINESS_HOURS_ID} \
  Workspace_URL_ID__c='${WORKSPACE_ID}'${DBC_ACCESS_FIELD_LINE}" --json
```

**Note on DBC Access field:**
- If `DBC_ACCESS_FIELD` was found in Step 2, append: ` \\\n  ${DBC_ACCESS_FIELD}=true`
- If not found, omit it (user will check manually later)
- Store the line in `DBC_ACCESS_FIELD_LINE` variable

#### Parse Creation Result

Extract the Case ID from the JSON response:

```bash
# Example response parsing
CASE_ID=$(echo "${RESULT}" | jq -r '.result.id')
```

#### Query Created Case Details

```bash
# Get the CaseNumber and verify all fields
sf data query --query "SELECT Id, CaseNumber, Subject, Description, Status, Priority, Origin, Type, Account.Name, Workspace_URL_ID__c FROM Case WHERE Id = '${CASE_ID}'" --json
```

**If case creation fails:**
```
❌ Case creation failed

Error: [display full error message]

Troubleshooting:
- Verify all field API names are correct
- Check that BusinessHoursId is valid
- Ensure you have create permissions on Case object

Would you like to try again or exit? [wait for input]
```

---

### Step 6: Display Success Results

Format and display the success message with case details and next steps.

```
✅ Genie Request Case Created Successfully!

Case Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Case Number: ${CASE_NUMBER}
Case URL: https://databricks.lightning.force.com/lightning/r/Case/${CASE_ID}/view

Customer: ${ACCOUNT_NAME}
Workspace ID: ${WORKSPACE_ID}
Subject: Genie Request for ${ACCOUNT_NAME}
Status: New
Priority: Normal
Origin: Email
Type: ${CASE_TYPE}

Reasoning:
${USER_REASONING}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If DBC Access field was not found:**
```
⚠️  Note: DBC Access field could not be auto-checked.
   Please manually verify this checkbox in Salesforce at:
   https://databricks.lightning.force.com/lightning/r/Case/${CASE_ID}/view
```

**Next Steps:**
```
Next Steps:
1. Review the case in Salesforce (click URL above)
2. Create the actual Genie request in the Genie system
3. Reference Case Number: ${CASE_NUMBER} in your Genie request
4. Update the case with any additional information or links
```

---

## Field Reference

| Field | API Name | Value | Source |
|-------|----------|-------|--------|
| Subject | `Subject` | `Genie Request for ${ACCOUNT_NAME}` | Generated |
| Description | `Description` | `${USER_REASONING}` | User input |
| Workspace URL/ID | `Workspace_URL_ID__c` | `${WORKSPACE_ID}` | User input |
| Priority | `Priority` | `Normal` | Fixed |
| Origin | `Origin` | `Email` | Fixed (required) |
| Type | `Type` | Discovered from example or "Customer Success" | Step 2 |
| Status | `Status` | `New` | Default |
| Account | `AccountId` | Selected account ID | Step 4 |
| Business Hours | `BusinessHoursId` | Discovered from example or default | Step 2 |
| DBC Access | `DBCAccessGrantedByCustomer__c` | `true` | Step 2 (if found) |

---

## Error Handling

| Error Scenario | Detection | Response |
|----------------|-----------|----------|
| Not authenticated | `sf org display` fails | Direct to `/salesforce-authentication` |
| Example case not found | Query returns 0 rows | Use default BusinessHours, continue |
| Account not found | Query returns 0 rows | Offer to try different search or exit |
| Multiple accounts | Query returns >1 row | Display list, prompt selection |
| Invalid workspace ID | Contains non-numeric chars | Re-prompt with validation message |
| Empty reasoning | User input is blank/empty | Re-prompt with requirement message |
| Missing BusinessHoursId | All queries return null | Fail with clear error message |
| Case creation fails | API error response | Display full error, offer retry |

---

## Example Usage

**User invokes skill:**
```
/genie-case
```

**Skill workflow:**
1. Checks authentication ✓
2. Discovers field values (Type: "Customer Success", BusinessHours: 01m...) ✓
3. Prompts for inputs:
   - Customer name: "Acme Corp"
   - Workspace ID: "123456"
   - Reasoning: "Customer needs access to review Genie dashboard for Q1 metrics"
4. Finds account: "Acme Corporation" (001...) ✓
5. Creates case with all fields ✓
6. Displays success with Case Number: 00001234 and URL ✓

**Total time: ~2 minutes**

---

## Tips

- **Workspace ID validation is strict** - Only numeric IDs are accepted to prevent URL confusion
- **Account search is fuzzy** - Try shorter search terms for better results
- **DBC Access field is optional** - If not auto-checked, manually verify in Salesforce
- **Case URL is immediately clickable** - Open in browser to review/edit case details
- **Reference the Case Number** - Include it when creating the actual Genie request

---

## Known Limitations

1. **DBC Access field may not be found** - Custom field names vary by org; manual check may be needed
2. **Example case may be deleted** - If case 500Vp00000mjIYMIA2 is removed, discovery uses defaults
3. **Not fully automated** - Still requires manual Genie request creation after case is filed
4. **Fuzzy matching limitations** - Very short names (1-2 chars) may return too many results

---

## Future Enhancements (Out of Scope)

- Cache discovered field values in config file for faster subsequent runs
- Support command-line arguments: `--customer "Acme" --workspace-id "123" --reason "..."`
- Integrate with Genie request system API (if available)
- Support batch case creation from CSV file
- Add case status tracking and notifications
- Auto-populate DBC Access field with better custom field discovery
