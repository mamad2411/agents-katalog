---
name: customerconnect
description: "Integrate and synchronize customer data from multiple sources with automated validation and real-time normalization. Use when the user needs unified customer profiles, data quality assurance, or multi-source CRM synchronization across WordPress, Salesforce, HubSpot, and Stripe."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["CUSTOMERCONNECT_API_KEY","CUSTOMERCONNECT_WORKSPACE_ID"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🔗"}}
---

## Overview

**CustomerConnect** is a production-grade customer data integration skill that solves the critical problem of fragmented customer information across multiple business systems. Instead of manually syncing data between WordPress, Shopify, Salesforce, HubSpot, Google Sheets, Stripe, and custom databases, CustomerConnect automates the entire pipeline with intelligent validation and real-time synchronization.

### Why This Matters

Businesses lose an average of 40% productivity when customer data is scattered across disconnected systems. Sales teams can't see purchase history, support teams duplicate customer records, and marketing sends campaigns to outdated email addresses. CustomerConnect eliminates this chaos by:

- **Unifying customer profiles** across all your data sources
- **Validating data quality** in real-time (email format, phone numbers, address standardization)
- **Preventing duplicates** through intelligent matching algorithms
- **Syncing bidirectionally** so changes in one system propagate everywhere
- **Maintaining audit trails** for compliance (GDPR, CCPA, SOC 2)

### Supported Integrations

✅ **CRM Platforms:** Salesforce, HubSpot, Pipedrive, Zoho CRM  
✅ **E-commerce:** Shopify, WooCommerce, BigCommerce, Magento  
✅ **Websites:** WordPress, Webflow, custom APIs  
✅ **Payment Processors:** Stripe, Square, PayPal  
✅ **Spreadsheets:** Google Sheets, Excel Online, Airtable  
✅ **Databases:** PostgreSQL, MySQL, MongoDB, SQL Server  
✅ **Communication:** Slack, Discord (webhook notifications)  

---

## Quick Start

Try these prompts immediately to see CustomerConnect in action:

### Example 1: Sync Shopify Customers to HubSpot
```
Sync all customers from Shopify store "mystore.myshopify.com" 
to HubSpot CRM, matching by email address. 
Normalize phone numbers to E.164 format and 
flag any customers with missing addresses for review.
```

### Example 2: Deduplicate and Validate Customer Database
```
Import customer CSV from Google Drive "Sales Database - Q4 2024".
Identify and merge duplicate records (same email or phone number).
Validate all email addresses, phone numbers, and postal codes.
Export cleaned data to new Google Sheet with audit log of changes.
```

### Example 3: Real-Time Sync Between Multiple Systems
```
Set up continuous sync between WordPress (source) and Salesforce (target).
When new customers register on WordPress, automatically create contacts in Salesforce.
Sync updates every 15 minutes. Email admin@company.com if sync fails.
Include customer tags from WordPress as Salesforce lead sources.
```

### Example 4: Data Quality Report
```
Analyze all customer records in HubSpot.
Generate report showing:
- Records with missing required fields (email, phone, company)
- Invalid email addresses or phone numbers
- Duplicate entries by name similarity
- Last update dates to identify stale records
Export as PDF with actionable recommendations.
```

---

## Capabilities

### 1. **Multi-Source Data Integration**
Connects to 25+ data sources simultaneously. CustomerConnect automatically handles authentication (OAuth 2.0, API keys, database credentials) and maintains secure credential storage.

**Usage Example:**
```
Connect these data sources:
- Shopify: shopify_api_key=xxx, shopify_password=yyy
- HubSpot: hubspot_api_key=zzz
- Google Sheets: "Customer Master List" sheet
Fetch all customer records updated in last 7 days.
```

### 2. **Intelligent Data Validation**
Built-in validation rules for common data types:
- **Email:** RFC 5322 compliance + disposable domain detection
- **Phone Numbers:** E.164 format, country code detection, carrier validation
- **Addresses:** USPS/Royal Mail standardization, geocoding
- **Names:** Duplicate detection, name parsing (first/last/middle)
- **Dates:** Timezone handling, age calculation, format standardization
- **Custom Rules:** Create regex patterns or SQL queries for domain-specific validation

**Usage Example:**
```
Validate customer records with custom rules:
- Email must not be from free domains (gmail.com, yahoo.com)
- Phone must be 10+ digits
- Company size must be numeric
- Annual revenue must be > $0
Flag records failing validation for manual review.
```

### 3. **Real-Time Synchronization**
Bidirectional sync with configurable frequency (real-time, hourly, daily, weekly). Conflict resolution strategies handle when the same record updates in multiple systems simultaneously.

**Sync Modes:**
- **One-way sync:** Source → Target only
- **Bidirectional:** Changes flow both directions
- **Scheduled:** Run at specific times
- **Event-triggered:** Sync when webhook fires (new order, contact created, etc.)

**Usage Example:**
```
Enable bidirectional sync between Salesforce and HubSpot.
Sync frequency: Real-time
Conflict resolution: Last-write-wins
Track all changes in audit log.
Notify slack #sales-ops if sync fails.
```

### 4. **Duplicate Detection & Merging**
Uses probabilistic matching (fuzzy logic) combined with exact matching to identify duplicates. Merge strategy preserves the most complete and recent data.

**Matching Strategies:**
- Exact email match (100% confidence)
- Phone number match (95% confidence)
- Name + address similarity (80% confidence)
- Custom matching rules (domain-specific)

**Usage Example:**
```
Find duplicate customers in HubSpot using:
- Exact email match
- Phone number match (ignore formatting)
- Similar names + same company
Merge duplicates, keeping most recent contact info.
Create merge report showing which records were combined.
```

### 5. **Data Normalization & Enrichment**
Automatically standardizes data formats and enriches records with additional information.

**Normalization:**
- Phone numbers → E.164 format (+1-555-123-4567)
- Addresses → USPS/Royal Mail standard format
- Names → Proper case (John Smith, not JOHN SMITH or john smith)
- Dates → ISO 8601 format (2024-01-15T09:30:00Z)
- Currency → Standardized to specified currency with conversion rates

**Enrichment (Optional):**
- Company name → Industry, employee count, annual revenue (via Clearbit, Hunter.io)
- Email → Name, company, job title (via email verification services)
- Phone → Carrier, line type (mobile/landline)
- Address → Timezone, coordinates, county

**Usage Example:**
```
Normalize and enrich all customers in Salesforce:
- Standardize phone numbers to E.164 format
- Geocode addresses and add timezone
- Enrich with company industry and size via Clearbit
- Add email verification status
Update Salesforce with enriched data.
```

### 6. **Audit & Compliance Logging**
Every data change is logged with timestamp, user, source, and previous value. Supports GDPR right-to-be-forgotten, CCPA data export requests, and audit reports.

**Logged Events:**
- Record created/updated/deleted
- Field-level changes with before/after values
- Data access (who viewed what, when)
- Sync operations (success/failure, record count)
- Validation results and data quality scores

**Usage Example:**
```
Generate GDPR data export for customer john@example.com.
Include all records, audit logs, and consent status.
Export as JSON + PDF report.
```

---

## Configuration

### Environment Variables (Required)

```bash
# CustomerConnect API credentials
export CUSTOMERCONNECT_API_KEY="cck_live_abc123def456"
export CUSTOMERCONNECT_WORKSPACE_ID="ws_12345"

# Source system credentials (choose what you need)
export SHOPIFY_API_KEY="your_shopify_api_key"
export SHOPIFY_PASSWORD="your_shopify_password"
export HUBSPOT_API_KEY="pat-na1-xxxxx"
export SALESFORCE_CLIENT_ID="your_salesforce_client_id"
export SALESFORCE_CLIENT_SECRET="your_salesforce_secret"
export STRIPE_API_KEY="sk_live_xxxxx"
export GOOGLE_SHEETS_API_KEY="your_google_api_key"
export WORDPRESS_REST_API_KEY="your_wordpress_key"

# Optional: Enrichment services
export CLEARBIT_API_KEY="sk_live_xxxxx"
export HUNTER_API_KEY="your_hunter_api_key"

# Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export ADMIN_EMAIL="ops@company.com"
```

### Setup Instructions

1. **Get API Credentials**
   - Visit [CustomerConnect Dashboard](https://app.customerconnect.io)
   - Create workspace and generate API key
   - Authenticate each data source (OAuth flow or API key)

2. **Install CLI (Optional)**
   ```bash
   npm install -g @customerconnect/cli
   customerconnect login --api-key $CUSTOMERCONNECT_API_KEY
   ```

3. **Configure Sync Rules**
   ```bash
   customerconnect sync:create \
     --source shopify \
     --target hubspot \
     --frequency hourly \
     --match-by email
   ```

4. **Test Connection**
   ```bash
   customerconnect test:connection shopify
   customerconnect test:connection hubspot
   ```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `match_strategy` | string | `email` | How to identify duplicate records: `email`, `phone`, `name`, `custom` |
| `conflict_resolution` | string | `last-write-wins` | When same record updates in multiple systems: `last-write-wins`, `source-priority`, `manual` |
| `sync_frequency` | string | `hourly` | How often to sync: `realtime`, `hourly`, `daily`, `weekly` |
| `validate_emails` | boolean | `true` | Check email validity and disposable domain detection |
| `validate_phones` | boolean | `true` | Validate phone numbers and convert to E.164 |
| `enrich_data` | boolean | `false` | Add company/industry data (requires paid enrichment service) |
| `audit_logging` | boolean | `true` | Log all data changes for compliance |
| `error_notification` | string | `slack` | Where to send error alerts: `slack`, `email`, `webhook` |
| `batch_size` | number | `1000` | Records per sync batch (higher = faster, more memory) |

---

## Example Outputs

### Output 1: Sync Summary Report
```json
{
  "sync_id": "sync_abc123def456",
  "timestamp": "2024-01-15T14:32:00Z",
  "source": "shopify",
  "target": "hubspot",
  "status": "success",
  "records_processed": 2847,
  "records_created": 312,
  "records_updated": 1205,
  "records_skipped": 1330,
  "validation_errors": 45,
  "duplicates_merged": 18,
  "duration_seconds": 127,
  "error_details": [
    {
      "record_id": "cust_12345",
      "field": "email",
      "error": "Invalid email format: john@example",
      "action": "Skipped record"
    }
  ],
  "next_sync": "2024-01-15T15:32:00Z"
}
```

### Output 2: Data Quality Report
```
═══════════════════════════════════════════════════════════
CUSTOMERCONNECT DATA QUALITY REPORT
Generated: 2024-01-15 | System: HubSpot CRM
═══════════════════════════════════════════════════════════

SUMMARY
Total Records: 15,432
Data Quality Score: 87.3% (↑2.1% from last week)
Records Needing Attention: 1,997

MISSING FIELDS
├─ Email Address: 342 records (2.2%)
├─ Phone Number: 1,205 records (7.8%)
├─ Company Name: 847 records (5.5%)
└─ Job Title: 2,103 records (13.6%)

INVALID DATA
├─ Malformed Emails: 45 records
├─ Invalid Phone Numbers: 123 records
├─ Incomplete Addresses: 687 records
└─ Future Birth Dates: 12 records

DUPLICATES DETECTED
├─ Exact Email Match: 34 pairs
├─ Phone Number Match: 67 pairs
├─ Similar Names (>90%): 156 pairs
└─ Estimated Duplicates: ~200 records

STALE DATA (Not updated >90 days)
├─ Total: 3,421 records (22.2%)
├─ Last Contact >1 Year Ago: 1,205 records
└─ No Activity: 2,216 records

RECOMMENDATIONS
1. Merge 34 email duplicates (estimated 1.2 hours manual work)
2. Validate/correct 45 malformed email addresses
3. Reach out to 3,421 stale contacts or archive
4. Implement email verification on web forms
5. Add job title to onboarding process

═══════════════════════════════════════════════════════════
```

### Output 3: Audit Log Export
```csv
timestamp,user_email,action,record_id,field,old_value,new_value,system,status
2024-01-15T14:22:15Z,sync@customerconnect.io,UPDATE,cust_abc123,email,old@example.com,new@example.com,hubspot,success
2024-01-15T14:22:16Z,sync@customerconnect.io,UPDATE,cust_abc123,phone,,+1-555-123-4567,hubspot,success
2024-01-15T14:22:17Z,sync@customerconnect.io,MERGE,cust_def456,duplicate_of,null,cust_abc123,hubspot,success
2024-01-15T14:22:18Z,john@company.com,VIEW,cust_abc123,null,null,null,hubspot,success
2024-01-15T14:22:45Z,sync@customerconnect.io,VALIDATE,cust_ghi789,email,invalid@,null,hubspot,error
```

---

## Tips & Best Practices

### 1. **Start with Email as Primary Key**
Email addresses are the most reliable unique identifier across systems. Use email as your primary matching field before adding phone numbers or names.

```
✅ DO: Match by email first, then phone, then name
❌ DON'T: Match by name alone (too many false positives)
```

### 2. **Implement Data Validation Early**
Set up validation rules BEFORE syncing data. Garbage data propagates quickly across systems.

```
Recommended validation rules:
- Email: RFC 5322 + no disposable domains
- Phone: E.164 format, valid country code
- Company: Not empty, not "test" or "n/a"
- Revenue: Numeric, > $0
```

### 3. **Use Audit Logs for Troubleshooting**
When data looks wrong, check the audit log first. You'll see exactly when it changed, who changed it, and what the previous value was.

```bash
# View recent changes to a specific customer
customerconnect logs:view --record-id cust_abc123 --last 30days
```

### 4. **Schedule Syncs During Off-Hours**
Large syncs can impact system performance. Run them at night or weekends when usage is low.

```
Recommended schedule:
- Real-time sync: Critical integrations only (< 100 records/minute)
- Hourly: