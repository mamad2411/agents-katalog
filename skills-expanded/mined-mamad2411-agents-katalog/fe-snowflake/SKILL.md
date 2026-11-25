---
name: fe-snowflake
description: Set up and manage Snowflake trial accounts for Field Engineering demos and testing
---

# Snowflake Trial Account Setup Skill

This skill automates the setup of Snowflake trial accounts for Field Engineering demos and testing. It handles the complete workflow from creating a burner Gmail account to configuring the Snowflake CLI.

**Announce at start:** "I'm using the fe-snowflake skill to set up a Snowflake trial account."

## Prerequisites

- Chrome DevTools MCP server running (for web automation)
- Homebrew installed (for Snowflake CLI)

## Quick Reference

| File | Purpose |
|------|---------|
| `~/.vibe/snowflake/environment` | Stored credentials and account info |
| `~/Library/Application Support/snowflake/config.toml` | Snowflake CLI configuration |
| `resources/DATABRICKS_INTEGRATION.md` | Databricks Iceberg table access from Snowflake |

## Step 1: Check for Existing Valid Account

**ALWAYS check for an existing account first before creating a new one.**

```bash
# Check if environment file exists
if [ -f ~/.vibe/snowflake/environment ]; then
  source ~/.vibe/snowflake/environment
  echo "Found existing Snowflake account: $SNOWFLAKE_ACCOUNT"
  echo "User: $SNOWFLAKE_USER"
  echo "Expiration: $SNOWFLAKE_EXPIRATION_DATE"
fi
```

### Validate Account Status

```bash
# Test if the account is still valid
snow connection test 2>&1
```

**If connection test succeeds:** Use the existing account. Skip to "Using the Account" section.

**If connection fails or account expired:** Proceed with creating a new trial account.

### Check Expiration Date

```bash
source ~/.vibe/snowflake/environment
TODAY=$(date +%Y-%m-%d)
if [[ "$TODAY" > "$SNOWFLAKE_EXPIRATION_DATE" ]]; then
  echo "Account expired. Need to create new trial."
else
  echo "Account still valid until $SNOWFLAKE_EXPIRATION_DATE"
fi
```

### Check Credits

If connected, check remaining credits:

```bash
snow sql -q "SELECT SYSTEM\$GET_ACCOUNT_CREDIT_BALANCE()" 2>&1
```

**If credits exhausted (returns 0 or error):** Create a new trial account.

---

## Step 2: Open Browser for Burner Gmail and Snowflake Signup

Snowflake trial accounts require an email address. We use a burner Gmail account to receive the activation email.

### Open Browser Tabs

Use Chrome DevTools MCP to open two tabs - one for Gmail and one for Snowflake signup:

```bash
# Check for open browser pages
mcp-cli call chrome-devtools/list_pages '{}'

# Open Gmail in the first tab
mcp-cli call chrome-devtools/new_page '{"url": "https://gmail.com"}'

# Open Snowflake trial signup in a second tab
mcp-cli call chrome-devtools/new_page '{"url": "https://signup.snowflake.com/"}'
```

### Instructions for User

Tell the user:

> I've opened two browser tabs for you:
> 1. **Gmail** - for creating a burner account
> 2. **Snowflake Trial Signup** - for registering the trial
>
> Please complete these steps:
>
> 1. **Create a burner Gmail account** in the Gmail tab
>    - Click "Create account" → "For my personal use"
>    - Use any name (can be fake)
>    - Create an email like `snowflake-trial-<random>@gmail.com`
>    - Complete the signup process
>
> 2. **Once done, sign up for a Snowflake trial** in the Snowflake tab
>    - Use the burner Gmail address you just created
>    - Fill in the required fields (I'll help with this next)
>
> 3. **Check your burner Gmail for the activation email**
>    - Look for an email titled **"Activate your Snowflake account"**
>    - It may take a few moments to arrive
>    - **Check the Spam folder** if you don't see it in your inbox
>
> 4. **Paste the activation link**
>    - Right-click on the **"Click to Activate"** button in the email
>    - Select **"Copy Link Address"**
>    - Paste the link here
>
> Let me know the burner Gmail address you created, then we'll proceed with the signup.

### Wait for User Confirmation

The user should provide:
1. The burner Gmail address they created
2. Later: The activation link from the email

---

## Step 3: Generate Fake Identity for Signup

**IMPORTANT:** To protect user privacy, always generate fake names for Snowflake trial signups. Never use the user's real name.

### Generate Fake Name

Use Python to generate a realistic-sounding fake name:

```python
import random
import string

# Common first names for generating fake identities
FIRST_NAMES = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Quinn", "Avery",
    "Cameron", "Dakota", "Drew", "Emerson", "Finley", "Harper", "Jamie", "Kendall",
    "Logan", "Madison", "Parker", "Reese", "Sage", "Skyler", "Sydney", "Blake"
]

# Generate a random fabricated last name (8-12 random letters)
def generate_fake_last_name():
    length = random.randint(8, 12)
    # First letter uppercase, rest lowercase
    return random.choice(string.ascii_uppercase) + ''.join(random.choices(string.ascii_lowercase, k=length-1))

first_name = random.choice(FIRST_NAMES)
last_name = generate_fake_last_name()

print(f"Generated identity for signup:")
print(f"  First name: {first_name}")
print(f"  Last name: {last_name}")
print(f"  Full name: {first_name} {last_name}")
```

**Store these values** - you'll need them for:
- The signup form (Step 4)
- The credentials file (Step 6)

---

## Step 4: Sign Up for Snowflake Trial

### Navigate to Snowflake Trial Signup

Use Chrome DevTools MCP to open the signup page:

```bash
# Check for open browser page
mcp-cli call chrome-devtools/list_pages '{}'

# Navigate to Snowflake trial signup
mcp-cli call chrome-devtools/navigate_page '{"type": "url", "url": "https://signup.snowflake.com/"}'
```

### Fill Out the Signup Form

Take a snapshot to see the form fields:

```bash
mcp-cli call chrome-devtools/take_snapshot '{}'
```

Fill out the required fields using the **generated fake name** from Step 3:

```bash
# Fill first name (use the GENERATED fake first name, NOT the user's real name)
mcp-cli call chrome-devtools/fill '{"uid": "<FIRST_NAME_UID>", "value": "<GENERATED_FIRST_NAME>"}'

# Fill last name (use the GENERATED fake last name, NOT the user's real name)
mcp-cli call chrome-devtools/fill '{"uid": "<LAST_NAME_UID>", "value": "<GENERATED_LAST_NAME>"}'

# Fill email (use the burner Gmail address)
mcp-cli call chrome-devtools/fill '{"uid": "<EMAIL_UID>", "value": "<BURNER_GMAIL_ADDRESS>"}'

# Fill company (use a made-up company name, NOT Databricks)
mcp-cli call chrome-devtools/fill '{"uid": "<COMPANY_UID>", "value": "Pinnacle Data Solutions"}'

# Select country (usually a dropdown)
mcp-cli call chrome-devtools/fill '{"uid": "<COUNTRY_UID>", "value": "United States"}'
```

**Remember:** Use the fake names generated in Step 3. Never use the user's real name.

### Select Cloud Provider and Region

Snowflake offers trials on AWS, Azure, or GCP. Select based on demo requirements:

```bash
# Click appropriate cloud provider button
mcp-cli call chrome-devtools/click '{"uid": "<AWS_BUTTON_UID>"}'  # or Azure/GCP

# Select region
mcp-cli call chrome-devtools/click '{"uid": "<REGION_UID>"}'
```

### Accept Terms and Submit

```bash
# Check terms checkbox if required
mcp-cli call chrome-devtools/click '{"uid": "<TERMS_CHECKBOX_UID>"}'

# Submit the form
mcp-cli call chrome-devtools/click '{"uid": "<SUBMIT_BUTTON_UID>"}'
```

### Wait for Confirmation Page

After submission, Snowflake shows a confirmation page. Take a snapshot to verify:

```bash
sleep 3
mcp-cli call chrome-devtools/take_snapshot '{}'
```

---

## Step 5: Get Activation Link from User

### Prompt User for Activation Link

Ask the user:

> Please check your burner Gmail account for the activation email from Snowflake:
>
> 1. Look for an email titled **"Activate your Snowflake account"** from `no-reply@snowflake.net`
> 2. It may take a few moments to arrive - refresh your inbox
> 3. **Check your Spam folder** if you don't see it
> 4. Once you find it, right-click on the **"Click to Activate"** button
> 5. Select **"Copy Link Address"**
> 6. Paste the activation link here

### Wait for User to Provide Activation Link

The user should provide a URL in the format:
```
https://<account-id>.snowflakecomputing.com/console/login?activationToken=<token>
```

**Validate the URL:**
- Must contain `.snowflakecomputing.com`
- Must contain `activationToken=`

If the user says they can't find the email:
- Ask them to wait 2-3 minutes and refresh
- Remind them to check Spam/Junk folder
- Verify they used the correct email during signup

---

## Step 6: Activate Account via Chrome DevTools

### Navigate to Activation URL

```bash
mcp-cli call chrome-devtools/navigate_page '{"type": "url", "url": "<ACTIVATION_URL>"}'
```

### Wait for Page Load and Take Snapshot

```bash
sleep 2
mcp-cli call chrome-devtools/take_snapshot '{"verbose": true}'
```

### Generate Username and Password

Generate secure credentials:

```python
import secrets
import string

# Username: letters and numbers only (Snowflake requirement)
# Use format: <initials><year> or similar
username = "bkvarda2026"

# Password: 14-256 chars, at least 1 uppercase, 1 lowercase, 1 number
# NO special characters (Snowflake trial requirement)
password_chars = [
    secrets.choice(string.ascii_uppercase),
    secrets.choice(string.ascii_lowercase),
    secrets.choice(string.digits),
]
remaining = string.ascii_letters + string.digits
password_chars.extend(secrets.choice(remaining) for _ in range(17))
import random
random.shuffle(password_chars)
password = ''.join(password_chars)

print(f"Username: {username}")
print(f"Password: {password}")
```

### Fill the Activation Form

```bash
# Take snapshot to get current UIDs
mcp-cli call chrome-devtools/take_snapshot '{}'

# Fill username
mcp-cli call chrome-devtools/fill '{"uid": "<USERNAME_UID>", "value": "<GENERATED_USERNAME>"}'

# Fill password (UIDs change after each fill, take new snapshot)
mcp-cli call chrome-devtools/take_snapshot '{}'
mcp-cli call chrome-devtools/fill '{"uid": "<PASSWORD_UID>", "value": "<GENERATED_PASSWORD>"}'

# Fill confirm password
mcp-cli call chrome-devtools/take_snapshot '{}'
mcp-cli call chrome-devtools/fill '{"uid": "<CONFIRM_PASSWORD_UID>", "value": "<GENERATED_PASSWORD>"}'
```

### Submit the Form

```bash
# Take snapshot to get button UID (it should now be enabled)
mcp-cli call chrome-devtools/take_snapshot '{}'

# Click "Get started" button
mcp-cli call chrome-devtools/click '{"uid": "<GET_STARTED_BUTTON_UID>"}'
```

### Verify Activation Success

```bash
sleep 3
mcp-cli call chrome-devtools/take_snapshot '{}'
```

**Success indicators:**
- URL changes to `https://app.snowflake.com/<org>/<account>/#/homepage`
- Page shows "Home" heading and Snowflake dashboard
- Trial credits and days remaining are displayed

---

## Step 7: Store Credentials

### Create the Configuration Directory

```bash
mkdir -p ~/.vibe/snowflake
```

### Write the Environment File

```bash
cat > ~/.vibe/snowflake/environment << 'EOF'
# Snowflake Account Credentials
# Created: <YYYY-MM-DD>
# Account activated via fe-snowflake skill

# Account Information
SNOWFLAKE_ACCOUNT=<account-identifier>
SNOWFLAKE_ACCOUNT_URL=https://app.snowflake.com/<org>/<account>
SNOWFLAKE_CONSOLE_URL=https://<account-identifier>.snowflakecomputing.com

# User Credentials
SNOWFLAKE_USER=<username>
SNOWFLAKE_PASSWORD=<password>

# Account Owner (use the GENERATED fake name from Step 3, NOT real name)
SNOWFLAKE_ACCOUNT_OWNER_NAME="<GENERATED_FIRST_NAME> <GENERATED_LAST_NAME>"
SNOWFLAKE_ACCOUNT_OWNER_EMAIL=<burner-gmail>@gmail.com

# Trial Information
SNOWFLAKE_TRIAL_CREDITS=400
SNOWFLAKE_TRIAL_DAYS=30
SNOWFLAKE_CREATED_DATE=<YYYY-MM-DD>
SNOWFLAKE_EXPIRATION_DATE=<YYYY-MM-DD + 30 days>

# Burner Gmail (for receiving emails)
SNOWFLAKE_BURNER_EMAIL=<burner-gmail>@gmail.com

# Connection String (for programmatic access)
# snowsql -a <account-identifier> -u <username>
# snow sql -q "SELECT CURRENT_USER()"
EOF
```

### Secure the File

```bash
chmod 600 ~/.vibe/snowflake/environment
```

---

## Step 8: Install Snowflake CLI

### Check if Already Installed

```bash
snow --version 2>&1
```

### Install via Homebrew (if not installed)

```bash
brew tap snowflakedb/snowflake-cli
brew update
brew install snowflake-cli
```

### Verify Installation

```bash
snow --version
```

---

## Step 9: Configure Snowflake CLI

### Add Connection

```bash
source ~/.vibe/snowflake/environment

snow connection add \
  --connection-name "default" \
  --account "$SNOWFLAKE_ACCOUNT" \
  --user "$SNOWFLAKE_USER" \
  --password "$SNOWFLAKE_PASSWORD" \
  --default \
  --no-interactive
```

### Test Connection

```bash
snow connection test
```

**Expected output:**
```
+-----------------------------------------------------------+
| key             | value                                   |
|-----------------+-----------------------------------------|
| Connection name | default                                 |
| Status          | OK                                      |
| Host            | <account>.snowflakecomputing.com        |
| Account         | <account>                               |
| User            | <username>                              |
| Role            | ACCOUNTADMIN                            |
| Warehouse       | COMPUTE_WH                              |
+-----------------------------------------------------------+
```

---

## Using the Account

### Running SQL Queries

```bash
# Simple query
snow sql -q "SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_ROLE()"

# Query with output format
snow sql -q "SHOW DATABASES" --format JSON

# Multi-line query
snow sql -q "
SELECT
    TABLE_CATALOG,
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
LIMIT 10
"
```

### Creating a Warehouse

```bash
# Create a small warehouse for testing
snow sql -q "
CREATE WAREHOUSE IF NOT EXISTS DEMO_WH
WITH
    WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
"

# Use the warehouse
snow sql -q "USE WAREHOUSE DEMO_WH"

# List warehouses
snow sql -q "SHOW WAREHOUSES"
```

### Creating a Database and Schema

```bash
# Create database
snow sql -q "CREATE DATABASE IF NOT EXISTS DEMO_DB"

# Create schema
snow sql -q "CREATE SCHEMA IF NOT EXISTS DEMO_DB.DEMO_SCHEMA"

# Set context
snow sql -q "USE DATABASE DEMO_DB"
snow sql -q "USE SCHEMA DEMO_SCHEMA"
```

### Creating and Querying Tables

```bash
# Create a sample table
snow sql -q "
CREATE TABLE IF NOT EXISTS DEMO_DB.DEMO_SCHEMA.SAMPLE_DATA (
    ID INTEGER,
    NAME VARCHAR(100),
    CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
"

# Insert data
snow sql -q "
INSERT INTO DEMO_DB.DEMO_SCHEMA.SAMPLE_DATA (ID, NAME)
VALUES (1, 'Test Record 1'), (2, 'Test Record 2')
"

# Query data
snow sql -q "SELECT * FROM DEMO_DB.DEMO_SCHEMA.SAMPLE_DATA"
```

### Checking Account Usage

```bash
# Check credit usage
snow sql -q "
SELECT *
FROM SNOWFLAKE.ORGANIZATION_USAGE.USAGE_IN_CURRENCY_DAILY
ORDER BY USAGE_DATE DESC
LIMIT 10
"

# Check warehouse usage
snow sql -q "
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
ORDER BY START_TIME DESC
LIMIT 10
"
```

---

## Troubleshooting

### Connection Test Fails

```bash
# Check if credentials are correct
source ~/.vibe/snowflake/environment
echo "Account: $SNOWFLAKE_ACCOUNT"
echo "User: $SNOWFLAKE_USER"

# Try manual connection test
snow connection test --connection default
```

### Account Expired

If the trial has expired:
1. Check expiration date in `~/.vibe/snowflake/environment`
2. If expired, start the process from Step 2 (create new burner Gmail)
3. Use a new burner Gmail address to get a fresh trial

### Credits Exhausted

Snowflake trials come with $400 in credits. If exhausted:
1. Create a new trial with a new burner Gmail account
2. Consider using smaller warehouses (XSMALL) for demos
3. Enable AUTO_SUSPEND on warehouses to conserve credits

### Chrome DevTools Not Available

Ensure the Chrome DevTools MCP server is running:
```bash
mcp-cli servers
mcp-cli tools chrome-devtools
```

---

## Summary Checklist

- [ ] Check for existing valid account in `~/.vibe/snowflake/environment`
- [ ] If no valid account: Open browser tabs for Gmail and Snowflake signup
- [ ] Guide user to create burner Gmail account
- [ ] Sign up for Snowflake trial at https://signup.snowflake.com/ with burner Gmail
- [ ] User retrieves activation link from burner Gmail (check Spam folder)
- [ ] Activate account via Chrome DevTools (generate username/password)
- [ ] Store credentials in `~/.vibe/snowflake/environment`
- [ ] Install Snowflake CLI via Homebrew
- [ ] Configure CLI connection with `snow connection add`
- [ ] Test connection with `snow connection test`
- [ ] Create demo warehouse and database as needed

---

## Advanced Integrations

### Databricks Iceberg Table Access

For demos showing Snowflake querying Databricks Unity Catalog tables via the Iceberg REST Catalog, see:

**[resources/DATABRICKS_INTEGRATION.md](resources/DATABRICKS_INTEGRATION.md)**

This guide covers:
- Creating an FE-VM Databricks workspace
- Creating managed Iceberg tables and Delta tables with UniForm
- Configuring vended credentials for Snowflake access
- Creating catalog integrations and linked databases
- Querying Databricks tables from Snowflake

**Prerequisites for Databricks Integration:**
- Valid Snowflake account (complete this skill first)
- `databricks-fe-vm-workspace-deployment` skill for getting a workspace
- `databricks-authentication` skill for CLI authentication
