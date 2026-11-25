---
name: cleo-prescription-reader
description: Read and extract information from prescription label images. Triggered by "read this prescription", "what does this label say?", "Cleo, read this Rx", or any request to interpret a prescription label photo. Extracts NDC, drug name, directions, prescriber, pharmacy, and other details, then optionally runs an FDB lookup on the NDC.
---

# Cleo Prescription Reader

## When to Use

- User shares a photo of a prescription label, pill bottle, or pharmacy printout
- User asks to "read", "interpret", or "extract" info from a prescription image

## Architecture

Two-pass cross-model verification for high-confidence extraction:

- **Pass 1 — GPT-4o** (temperature 0.0): Extracts all visible label fields as structured JSON
- **Pass 2 — Claude Sonnet 4** (temperature 0.3): Re-reads the image with the proposed extraction and scores each field's accuracy (0–100), flags discrepancies
- **Storage:** Images uploaded to S3 (`sph-cleo-rx/<site-id>/`), results saved as JSON with a slot for human corrections

### Why Two Models?

Different architectures, different training, different failure modes. When both agree → high confidence. When they disagree → flag for human review.

## Scripts

All scripts are in `skills/cleo-prescription-reader/scripts/`.

### Full Pipeline

```bash
node skills/cleo-prescription-reader/scripts/rx_read.js <image-path> [--site-id <id>] [--no-ndc] [--output-dir <dir>]
```

Runs the complete flow: S3 upload → GPT-4o extraction → Claude Sonnet verification → NDC lookup → save results.

- `--site-id` — folder in S3 bucket (default: `default`). Examples: `aegis-qa`, `aegis-cala`
- `--no-ndc` — skip the FDB NDC lookup step
- `--output-dir` — where to save result JSON (default: `data/rx-results/`)

### Individual Passes

```bash
# Pass 1 only: GPT-4o extraction
node skills/cleo-prescription-reader/scripts/rx_extract.js <image-path> [--site-id <id>]

# Pass 2 only: Claude Sonnet verification
node skills/cleo-prescription-reader/scripts/rx_verify.js <image-path> <extraction-json-file>
```

## Steps (Interactive Use)

### 1. Save the Image

If the user sends an image in chat, save it to a temp file first.

### 2. Run the Pipeline

```bash
node skills/cleo-prescription-reader/scripts/rx_read.js /tmp/rx-image.jpg --site-id default
```

### 3. Format the Response

Present results in two sections:

#### Section 1: Prescription Label

```
📋 **Prescription Label**

**Patient**
- **Name:** {first_name} {middle_name} {last_name}

**Medication**
- **NDC:** {ndc, formatted 5-4-2 with dashes}
- **Drug:** {drug name and strength}
- **Directions:** {sig / directions for use}
- **Quantity:** {quantity dispensed}
- **Days Supply:** {days supply}
- **Refills:** {refills remaining}
- **RX #:** {prescription number}
- **Date Filled:** {fill date}
- **Expiration:** {expiration date if visible}
- **Manufacturer:** {manufacturer if visible}
- **Pill Description:** {color, shape, imprint if visible}

**Prescriber**
- **Name:** {doctor name and credentials}
- **NPI:** {prescriber NPI}
- **DEA:** {DEA number}

**Pharmacy**
- **Name:** {pharmacy name}
- **Address:** {pharmacy address}
- **Phone:** {pharmacy phone}
- **NPI:** {pharmacy NPI}
```

##### Formatting Rules

1. **NDC is always the first bullet under Medication** — primary identifier for downstream lookups
2. Format NDC with dashes: `XXXXX-XXXX-XX` (5-4-2)
3. NPI is 10 digits, DEA is 2 letters + 7 digits
4. Omit fields that aren't visible on the label (don't show blanks)
5. Preserve exact wording of directions/sig as printed
6. Include any warnings or auxiliary labels if visible

#### Section 2: Confidence Scores

```
🔍 **Verification (Claude Sonnet 4)**

- **Overall Score:** {overall_score}/100
- **NDC:** {score}/100 {flag if any}
- **Drug:** {score}/100
- **Directions:** {score}/100 {flag if any}
...
```

Only show fields with flags or scores below 90. If all scores are 90+, just show the overall score.

#### Section 3: FDB NDC Lookup

Format using the standard **cleo-ndc-lookup** template. Skip if no NDC was found or `--no-ndc` was used.

### 4. Multiple Prescriptions

If the image contains multiple labels, extract each one separately with its own sections, separated by a divider (`---`).

## S3 Storage

- **Bucket:** `sph-cleo-rx`
- **Structure:** `sph-cleo-rx/<site-id>/<timestamp>-<hash>.<ext>`
- **Site IDs:** Use the service's site-id. Default: `default`. Examples: `aegis-qa`, `aegis-cala`

## Result Schema

```json
{
  "id": "rx-<timestamp>-<hash>",
  "site_id": "default",
  "timestamp": "ISO-8601",
  "image": {
    "local_path": "/tmp/rx-image.jpg",
    "s3_uri": "s3://sph-cleo-rx/default/...",
    "s3_key": "default/..."
  },
  "pass1_extraction": {
    "model": "gpt-4o",
    "temperature": 0.0,
    "extraction": { ... }
  },
  "pass2_verification": {
    "model": "claude-sonnet-4-20250514",
    "temperature": 0.3,
    "verification": { ... }
  },
  "ndc_lookup": { ... },
  "human_correction": null
}
```

The `human_correction` field is a slot for storing manual corrections, enabling a feedback loop to improve prompts over time.

## Notes

- Prescription images may be blurry or partially obscured — extract what you can and note anything illegible
- If no NDC is visible, note that and suggest the user check the bottle for an 11-digit code (often near the barcode)
- Never provide medical advice — stick to reading what's on the label and FDB reference data
- Low verification scores (<50) almost always indicate a real problem
- High scores (>90) are generally reliable but the model can occasionally be overconfident
