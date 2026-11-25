---
name: client-build
description: Use this skill to build a complete client skill set from an intake form. Triggers on phrases like "build skills for", "new client build", "set up skills for", or when given a JSON or structured intake form. Reads templates from /templates/, substitutes all placeholder variables, validates completeness, and outputs to /clients/[business-name]/skills/. Do NOT use without a complete intake form.
---

# Client Build

Turns a completed intake form into a ready-to-deliver skill set for a new client. Reads the 5 template files from `/templates/`, substitutes all `{{PLACEHOLDER}}` variables with the client's actual business data, validates that no placeholders remain, and writes the output to `/clients/[business-name]/skills/`.

## What you need to provide

Provide the intake form data in any of these formats:
- Structured plain text (field: value, one per line)
- JSON object with the field names below
- A path to an intake form file

### Required fields (15)

| Field | Placeholder | Example |
|-------|------------|---------|
| Business name | `{{BUSINESS_NAME}}` | Arctic Air HVAC |
| Owner name | `{{OWNER_NAME}}` | Mike Torres |
| City | `{{CITY}}` | Phoenix |
| Service area | `{{SERVICE_AREA}}` | Phoenix metro and East Valley |
| Primary services | `{{PRIMARY_SERVICES}}` | AC repair, heating, commercial HVAC |
| Labour rate | `{{LABOUR_RATE}}` | $95/hr |
| Call-out fee | `{{CALL_OUT_FEE}}` | $75 |
| Payment terms | `{{PAYMENT_TERMS}}` | 50% upfront, balance on completion |
| Licence number | `{{LICENCE_NUMBER}}` | AZ-ROC-123456 |
| Warranty terms | `{{WARRANTY_TERMS}}` | 12 months on all labour |
| Emergency call-outs | `{{EMERGENCY_CALLOUTS}}` | yes |
| Tone preference | `{{TONE_PREFERENCE}}` | friendly |
| Google review link | `{{GOOGLE_REVIEW_LINK}}` | https://g.page/r/arctic-air/review |
| Phone | `{{PHONE}}` | 602-555-0123 |
| Email | `{{EMAIL}}` | mike@arcticairhvac.com |

### Optional fields (2)

| Field | Placeholder | Default if blank |
|-------|------------|-----------------|
| Technician names | `{{TECHNICIAN_NAMES}}` | "the team" |
| Booking link | `{{BOOKING_LINK}}` | Use phone number: "Call or text {{PHONE}}" |

## Build process

Follow these steps exactly:

### Step 1 — Parse the intake form
Extract all 15 required fields + 2 optional fields from the provided data. If any required field is missing, list the missing fields and HALT — do not proceed with a partial build.

### Step 2 — Map tone preference
Convert `{{TONE_PREFERENCE}}` to `{{TONE_INSTRUCTION}}`:
- If tone is "professional" → use "professional and authoritative"
- If tone is "friendly" → use "warm, friendly, and conversational"
- If tone is anything else → ask for clarification before proceeding

### Step 3 — Create the output directory
Slugify the business name for the folder:
- Lowercase everything
- Replace spaces with hyphens
- Remove special characters (apostrophes, ampersands, etc.)
- Example: "Arctic Air HVAC" → `arctic-air-hvac`
- Example: "Mike's Plumbing & Electrical" → `mikes-plumbing-electrical`

Create: `/clients/[slug]/skills/`

### Step 4 — Read and substitute templates
For each of the 5 template files in `/templates/`:
1. Read the template SKILL.md
2. Replace every `{{PLACEHOLDER}}` with the corresponding intake form value
3. Replace `{{TONE_INSTRUCTION}}` with the mapped tone value from Step 2
4. Handle optional fields:
   - If `{{TECHNICIAN_NAMES}}` is blank → substitute "the team"
   - If `{{BOOKING_LINK}}` is blank → substitute "Call or text {{PHONE}}" (using the actual phone number)
5. Write the result to `/clients/[slug]/skills/[skill-name]/SKILL.md`

The 5 skills to process:
- `templates/job-complete-followup/SKILL.md` → `clients/[slug]/skills/job-complete-followup/SKILL.md`
- `templates/estimate-writer/SKILL.md` → `clients/[slug]/skills/estimate-writer/SKILL.md`
- `templates/review-responder/SKILL.md` → `clients/[slug]/skills/review-responder/SKILL.md`
- `templates/missed-call-handler/SKILL.md` → `clients/[slug]/skills/missed-call-handler/SKILL.md`
- `templates/seasonal-campaign/SKILL.md` → `clients/[slug]/skills/seasonal-campaign/SKILL.md`

### Step 5 — Validate
After writing all 5 files, check every output file:
- **Zero `{{` occurrences** in any file. If any remain, list the file, line number, and placeholder — then HALT.
- **All 5 files exist** and are non-empty.
- **Each file's YAML `name:` field** matches its folder name.

If validation fails, report exactly what's wrong. Do not proceed to the summary.

### Step 6 — Confirm
Print a build summary:

```
✓ Client build complete: [Business Name]
  Output: /clients/[slug]/skills/

  Files created:
  - job-complete-followup/SKILL.md ([X] bytes)
  - estimate-writer/SKILL.md ([X] bytes)
  - review-responder/SKILL.md ([X] bytes)
  - missed-call-handler/SKILL.md ([X] bytes)
  - seasonal-campaign/SKILL.md ([X] bytes)

  Next step: Run /reference-card [business name] to generate the client's delivery document.
```

## Example invocation

```
/client-build

Business name: Arctic Air HVAC
Owner name: Mike Torres
City: Phoenix
Service area: Phoenix metro and East Valley
Primary services: AC repair, heating, commercial HVAC
Labour rate: $95/hr
Call-out fee: $75
Payment terms: 50% upfront, balance on completion
Licence number: AZ-ROC-123456
Warranty terms: 12 months on all labour
Emergency call-outs: yes
Tone preference: friendly
Google review link: https://g.page/r/arctic-air/review
Phone: 602-555-0123
Email: mike@arcticairhvac.com
Technician names: Jake, Carlos, Ben
Booking link: https://arcticairhvac.com/book
```

## Notes

- The `/clients/` folder is gitignored — client builds never leave this machine unless explicitly exported
- After a successful build, run `/reference-card` to generate the client's delivery document
- To deliver to the client: zip the `/clients/[business-name]/` folder and send with upload instructions for claude.ai
- Client uploads the ZIP at: claude.ai → Settings → Capabilities → Upload skill
