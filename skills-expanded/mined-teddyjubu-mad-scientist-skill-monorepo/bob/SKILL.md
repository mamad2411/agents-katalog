---
name: bob
description: bob lets the user skip trace a property address to find owner names, phone numbers (with DNC/TCPA compliance flags), email addresses, alternate mailing addresses, and property details via the BatchData API v3, making it useful when they need to move fast on a deal, qualify a lead, or run outreach without doing manual people-search work one record at a time.
---

## What This Skill Does

This skill bob lets the user skip trace a property address to find owner names, phone numbers (with DNC/TCPA compliance flags), email addresses, alternate mailing addresses, and property details via the BatchData API v3, making it useful when they need to move fast on a deal, qualify a lead, or run outreach without doing manual people-search work one record at a time.

## Trigger
Use whenever Charles asks to skip trace, find contact info, or look up an owner's phone/email for a specific property address.

## API Details
- **Endpoint:** `POST https://api.batchdata.com/api/v3/property/skip-trace`
- **Auth:** Bearer token — API key stored in `~/.hermes/skills/bob/.env` as `BATCHDATA_API_KEY`
- **Content-Type:** `application/json`
- **Accept:** `application/json`
- **Sync vs Async:** Use sync endpoint (`/skip-trace`) for immediate results. Async (`/skip-trace/async`) requires a webhook and is for batch processing.

## Request Format
```json
{
  "requests": [
    {
      "propertyAddress": {
        "street": "<street address>",
        "city": "<city>",
        "state": "<2-letter state abbreviation>",
        "zip": "<5-digit ZIP>"
      }
    }
  ]
}
```

### Valid Address Combinations (pick one)
- `street + city + state + zip`
- `street + zip`
- `street + city + state`

### Known Issues from Testing
- **CF Error 1010 (browser signature banned):** `execute_code` with Python urllib fails with DNS error on `api.batchdata.io` and Cloudflare 1010 on `batchdata.io`. Use `terminal` with `curl` instead — it bypasses the Cloudflare browser check that blocks Python's urllib.
- **Wrong base URL trap:** The docs show `api.batchdata.com` — do NOT use `api.batchdata.io` (DNS fails) or `batchdata.io/api/` (Cloudflare blocks).
- **Charles's account:** Key is stored in `~/.hermes/skills/bob/.env` as `BATCHDATA_API_KEY`.

## Response Structure
```json
{
  "status": { "code": 200, "text": "OK" },
  "result": {
    "data": [{
      "input": { "propertyAddress": {...}, "requestId": "..." },
      "property": {
        "id": "<uuid>",
        "address": { "fullAddress": "...", "county": "...", "zipPlus4": "..." },
        "mailingAddress": { ... },
        "owners": [{ "name": { "first": "", "last": "", "full": "" } }]
      },
      "persons": [{
        "propertyOwner": true,
        "name": { "first": "", "last": "", "middle": "", "full": "", "akas": [...] },
        "addresses": [{ "fullAddress": "", "rank": 1, "propertyMailingAddress": true/false }],
        "phones": [{ "rank": 1, "number": "...", "type": "Mobile|Land Line", "carrier": "...", "dnc": false, "tcpa": false, "reachable": true }],
        "emails": [{ "rank": 1, "email": "...", "tested": true }],
        "litigator": false,
        "deceased": false,
        "dob": "YYYY-MM-DD..."
      }],
      "meta": { "matched": true, "error": false }
    }],
    "meta": {
      "results": { "requestCount": 1, "matchCount": 1, "noMatchCount": 0, "errorCount": 0 },
      "requestId": "<ulid>"
    }
  }
}
```

## How to Run
```bash
eval "$(cat ~/.hermes/skills/bob/.env | xargs)"
curl -s -X POST "https://api.batchdata.com/api/v3/property/skip-trace" \
  -H "Authorization: Bearer $BATCHDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "requests": [{
      "propertyAddress": {
        "street": "944 N Hill Rd",
        "city": "Baltimore",
        "state": "MD",
        "zip": "21218"
      }
    }]
  }' | python3 -c "
import json,sys
d=json.load(sys.stdin)
p=d['result']['data'][0]['persons'][0]
print('OWNER:', p['name']['full'])
print('DOB:', p.get('dob','')[:10])
print()
print('PHONES (DNC-free first):')
for ph in sorted(p['phones'], key=lambda x: x['dnc']):
    dnc='⚠ ON DNC' if ph['dnc'] else '✓'
    print(f\"  {dnc} {ph['number']} ({ph['type']}, {ph['carrier']})\")
print()
print('EMAILS:')
for e in p['emails']:
    print(f\"  {e['email']}\")
"
```

## API Key Setup
Store in `~/.hermes/skills/bob/.env`:
```
BATCHDATA_API_KEY=YOUR_BATCHDATA_API_KEY_HERE
```
(Keys live in `.env` files next to the SKILL.md — never hardcode them in documentation)

## Output for Charles
Always present skip trace results in this format:
- **Owner name + DOB** if available
- **Phones** sorted: DNC-free first, with carrier and type. Flag TCPA-blacklisted
- **Emails** ranked
- **Other known addresses** for the owner
- **"No match"** if `matched: false`

## Pitfalls
- **Wrong base URL:** `api.batchdata.io` fails DNS, `batchdata.io/api/` gets Cloudflare 1010. Correct: `api.batchdata.com/api/v3/`
- **Python urllib blocked:** `execute_code` (urllib) fails with Cloudflare 1010 from this server IP. Always use `terminal` with `curl` — it bypasses the browser signature check.
- **If `matched: false`:** try different address formats ("N" vs "North", "St" vs "Street")
- **Phones with `dnc: true`:** do not call — Charles avoids DNC-listed numbers
- **Multiple owners:** present all persons returned, not just the first one
- **Async endpoint:** only use `/skip-trace/async` if doing batch work with a webhook — for single-property lookups use sync `/skip-trace`
