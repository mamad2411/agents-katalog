# n8n Code Node — JavaScript Expert

Write correct JavaScript for n8n Code nodes. Handles n8n's specific APIs and patterns.

## Basic structure

Every Code node must return an array of items:

```javascript
// Return one item
return [{ json: { result: "done" } }];

// Return multiple items (one per input)
const results = [];
for (const item of $input.all()) {
  results.push({
    json: {
      original: item.json,
      processed: true
    }
  });
}
return results;
```

## Accessing input data

```javascript
// First item
const first = $input.first().json;

// All items
const all = $input.all();

// Map to just the json
const data = $input.all().map(i => i.json);

// Specific item by index
const third = $input.item(2).json;
```

## Common patterns

### Parse CSV rows and normalize fields
```javascript
const results = [];

for (const item of $input.all()) {
  const row = item.json;

  results.push({
    json: {
      company_name: (row.company_name || row.Company || "").trim(),
      contact_name: (row.contact_name || row.Name || row["Full Name"] || "").trim(),
      email: (row.email || row.Email || "").toLowerCase().trim(),
      linkedin_url: row.linkedin_url || row.LinkedIn || "",
      website: row.website || row.Website || "",
      category: (row.category || row.Category || "").toLowerCase(),
      source: row.source || "manual"
    }
  });
}

return results;
```

### Extract domain from email
```javascript
function getDomain(email) {
  if (!email || !email.includes("@")) return null;
  const domain = email.split("@")[1].toLowerCase();
  // Skip personal email domains
  const personal = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"];
  if (personal.includes(domain)) return null;
  return domain;
}

return $input.all().map(item => ({
  json: {
    ...item.json,
    domain: getDomain(item.json.email)
  }
}));
```

### Build enrichment waterfall status
```javascript
const item = $input.first().json;

// Determine which tier found the email
// Adapt provider field names to match your enrichment tools
let enrichment_source = null;
let email_found = false;

if (item.provider1_email) {
  enrichment_source = "provider_1";
  email_found = true;
} else if (item.provider2_email) {
  enrichment_source = "provider_2";
  email_found = true;
} else if (item.provider3_email) {
  enrichment_source = "provider_3";
  email_found = true;
}

return [{
  json: {
    ...item,
    final_email: item.provider1_email || item.provider2_email || item.provider3_email || null,
    enrichment_source,
    email_found
  }
}];
```

### Build dedup check result
```javascript
const contact = $input.first().json;

// Input should have these from previous CRM search nodes
// (adapt field names to match your CRM — HubSpot, Salesforce, Pipedrive, etc.)
// - crm_contact_exists (boolean)
// - crm_company_exists (boolean)
// - crm_active_deal (boolean)
// - crm_recent_deal (boolean)

const skipped = contact.crm_contact_exists ||
                contact.crm_active_deal ||
                contact.crm_recent_deal;

let skip_reason = null;
if (contact.crm_contact_exists) skip_reason = "contact already exists in CRM";
else if (contact.crm_active_deal) skip_reason = "active deal for this company";
else if (contact.crm_recent_deal) skip_reason = "deal closed in last 12 months";

return [{
  json: {
    ...contact,
    should_enroll: !skipped,
    skip_reason
  }
}];
```

### Build batch summary report
```javascript
const items = $input.all().map(i => i.json);

const enriched = items.filter(i => i.email_found).length;
const unresolved = items.filter(i => !i.email_found).length;
const enrolled = items.filter(i => i.should_enroll && i.sequence_enrolled).length;
const skipped_dedup = items.filter(i => !i.should_enroll).length;

const skipped_reasons = items
  .filter(i => i.skip_reason)
  .reduce((acc, i) => {
    acc[i.skip_reason] = (acc[i.skip_reason] || 0) + 1;
    return acc;
  }, {});

const summary = `
Batch Processing Summary
Date: ${new Date().toLocaleDateString()}
Total processed: ${items.length}
Enriched (email found): ${enriched}
Unresolved (no email): ${unresolved}
Enrolled in sequence: ${enrolled}
Skipped (dedup): ${skipped_dedup}

Dedup reasons:
${Object.entries(skipped_reasons).map(([k, v]) => `- ${k}: ${v}`).join("\n")}
`;

return [{ json: { summary, stats: { enriched, unresolved, enrolled, skipped_dedup } } }];
```

### Parse meeting transcript for key points
```javascript
const transcript = $input.first().json;

const sentences = transcript.sentences || [];
const actionItems = transcript.action_items || [];
const summary = transcript.summary || {};

// Extract speaker turns
const turns = [];
let currentSpeaker = null;
let currentText = [];

for (const s of sentences) {
  if (s.speaker_name !== currentSpeaker) {
    if (currentSpeaker) {
      turns.push({ speaker: currentSpeaker, text: currentText.join(" ") });
    }
    currentSpeaker = s.speaker_name;
    currentText = [s.text];
  } else {
    currentText.push(s.text);
  }
}
if (currentSpeaker) turns.push({ speaker: currentSpeaker, text: currentText.join(" ") });

return [{
  json: {
    title: transcript.title,
    date: transcript.date,
    action_items: actionItems,
    overview: summary.overview || "",
    key_turns: turns.slice(0, 20), // first 20 speaker turns
    full_text: sentences.map(s => `${s.speaker_name}: ${s.text}`).join("\n")
  }
}];
```

## Error handling in Code nodes

```javascript
try {
  const result = someOperation();
  return [{ json: { success: true, result } }];
} catch (error) {
  return [{ json: { success: false, error: error.message } }];
}
```

## Useful utilities

```javascript
// Slugify a string for use as an ID or filename
function slugify(str) {
  return str.toLowerCase().replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, "");
}

// Truncate text
function truncate(str, n) {
  return str.length > n ? str.slice(0, n - 3) + "..." : str;
}

// Remove HTML tags
function stripHtml(str) {
  return str.replace(/<[^>]*>/g, "");
}

// Format date for CRMs that need milliseconds since epoch (e.g. HubSpot)
function toEpochMs(dateStr) {
  return new Date(dateStr).getTime();
}

// Format date as locale string
function formatDate(date, locale = "en-US") {
  return new Date(date).toLocaleDateString(locale, { day: "numeric", month: "long", year: "numeric" });
}
```
