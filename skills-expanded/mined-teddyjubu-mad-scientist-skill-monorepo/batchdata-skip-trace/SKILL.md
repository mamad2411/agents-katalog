---

name: batchdata-skip-trace
description: batchdata-skip-trace lets the user upload or work from a property or owner list and quickly find likely contact details tied to those records, such as phone numbers, email addresses, mailing addresses, and related ownership signals, so they can move faster on outreach, lead qualification, and list cleanup without doing manual people-search work one record at a time.

---
Skip trace single or multiple property addresses to retrieve comprehensive owner and property data.

## What This Skill Does

This skill batchdata-skip-trace lets the user upload or work from a property or owner list and quickly find likely contact details tied to those records, such as phone numbers, email addresses, mailing addresses, and related ownership signals, so they can move faster on outreach, lead qualification, and list cleanup without doing manual people-search work one record at a time.

## API Configuration

- **Base URL:** `https://api.batchdata.com/api/v1/property/skip-trace`
- **Auth:** Bearer token — API key stored in `~/.secrets/batchdata.env` as `BATCHDATA_API_KEY`
- **Method:** POST
- **Content-Type:** application/json

## Request Format

```json
{
  "requests": [
    {
      "propertyAddress": {
        "street": "109 S Gilmor St",
        "city": "Baltimore",
        "state": "MD",
        "zip": "21223"
      }
    }
  ]
}
```

**Important:** The address must be wrapped in a `propertyAddress` object. A plain `address` string often returns validation errors.

## Usage

### Single Address
```bash
cd /data/.openclaw/workspace/agents/bob/skills/batchdata-skip-trace/scripts
python3 batchdata_lookup.py "109 S Gilmor St, Baltimore, MD 21223"
```

### Multiple Addresses (CSV)
```bash
cd /data/.openclaw/workspace/agents/bob/skills/batchdata-skip-trace/scripts
python3 batchdata_lookup.py addresses.csv
```

CSV format — first column must be `address` (full address string), or optionally `street,city,state,zip` columns:
```csv
address
123 Main St, Washington, DC 20001
456 Oak Ave, Bethesda, MD 20814
```

### Output
Results saved to `skip_trace_results_YYYYMMDD_HHMMSS.csv` in the scripts directory.

## Response Data Structure

The API returns results in `results.persons` array. Key fields:

| Field | Path | Description |
|-------|------|-------------|
| Owner Name | `name.full` | Full name of skip-traced person |
| Mailing Street | `mailingAddress.street` | Mailing street address |
| Mailing City | `mailingAddress.city` | Mailing city |
| Mailing State | `mailingAddress.state` | Mailing state |
| Mailing Zip | `mailingAddress.zip` | Mailing ZIP |
| Phones | `phoneNumbers[].number` | Phone number(s) |
| Phone Type | `phoneNumbers[].type` | e.g. "Mobile", "Home" |
| Phone Reachable | `phoneNumbers[].reachable` | Boolean |
| Emails | `emails[]` | Email address(es) |
| Property Street | `propertyAddress.street` | Property street address |
| Property City | `propertyAddress.city` | Property city |
| Property State | `propertyAddress.state` | Property state |
| Property Zip | `propertyAddress.zip` | Property ZIP |
| Match Status | `meta.matched` | true/false |
| Match Error | `meta.error` | true/false |
| Error Message | `meta.errorMessage` | Error detail if any |
| Owner (from property record) | `property.owner.name.full` | Owner name on deed |
| Owner Mailing | `property.owner.mailingAddress.*` | Owner's mailing address from property record |

**Note:** Skip-trace responses do NOT include `valuation`, `openLien`, `quickLists`, or `listing` fields. Those require a separate Property Search call (`/api/v1/property/search`) which is billed separately.

## Workflow

1. Load addresses (single string or CSV file)
2. Parse each address into street/city/state/zip components
3. Call `POST /api/v1/property/skip-trace` with `{"requests":[{"propertyAddress":{...}}]}`
4. Parse `results.persons[]` from response
5. Take the first person where `meta.matched` is true and `meta.error` is false
6. Extract owner name, phones, emails, mailing address, property address
7. Output to timestamped CSV
8. Report: how many addresses looked up, how many had matches

## Notes

- Batch limit: ~100 addresses per batch is safe; for large CSVs process in chunks of 50
- `phones` and `emails` fields may be null depending on data availability
- If no match found, the address will still appear in output with blank owner fields
- Rate limit: add `time.sleep(0.25)` between requests to avoid throttling
- **403 Insufficient balance:** If the account has no skip-trace credits, the API returns 403. Fund the BatchData skip-trace product to continue.
