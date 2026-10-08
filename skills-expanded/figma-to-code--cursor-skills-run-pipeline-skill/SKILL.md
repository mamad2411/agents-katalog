---
name: run-pipeline
description: Run the figma-to-component-gen pipeline for a UI component description. Use when the user wants to generate a component, test the pipeline, try an example input, or debug pipeline output.
---

# Run Pipeline

## Prerequisites

```bash
# .env must exist with valid keys
cp .env.example .env
# Set ANTHROPIC_API_KEY  (required)
# Set FIGMA_ACCESS_TOKEN (required — pipeline fails without it)
```

## CLI — generate a component

`--figma-url` is **required** and must include a `node-id` query parameter.

```bash
# Inline description + Figma URL
npm run dev generate "Your component description here" \
  --figma-url "https://www.figma.com/design/<key>/Name?node-id=1-2" \
  --pretty --files-dir ./output/MyComponent

# Description from file
npm run dev generate \
  --input description.txt \
  --figma-url "https://www.figma.com/design/<key>/Name?node-id=1-2" \
  --pretty --files-dir ./output/MyComponent

# Override JSON output path (default: <files-dir>/pipeline-output.json)
npm run dev generate "description" \
  --figma-url "…" \
  --output result.json \
  --pretty --files-dir ./output/MyComponent
```

## HTTP API

```bash
# Start server
npm run api:dev

# Call it — both fields are required
curl -X POST http://localhost:3000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Your component description here",
    "figma_url": "https://www.figma.com/design/<key>/Name?node-id=1-2"
  }'
```

## Three ready-to-use example inputs

**PaymentCard:**
```
Payment card component. Shows card number (masked: **** **** **** 1234), expiry date, cardholder name, card brand icon (Visa/Mastercard/Amex). Used in merchant dashboard to display saved payment methods. User can select a card or delete it.
```

**TransactionTable:**
```
Transaction table with columns: date, amount, status, merchant name, payment method. Supports sorting by any column and pagination (25/50/100 per page). Status values: pending, completed, failed, refunded. Each status has a colored badge. Row click opens transaction details.
```

**KYC Wizard:**
```
KYC verification wizard. 3 steps: personal info, document upload, selfie. Step indicator at the top. Back/Next navigation. Document upload supports drag-and-drop and file picker (PDF, JPG, PNG, max 10MB). Final step shows verification status: pending review, approved, rejected.
```

## Reading the output

When `--files-dir` is set, the CLI writes 4 files:

```
ComponentName.tsx            React component with all states
ComponentName.module.css     CSS Modules using design tokens
ComponentName.types.ts       TypeScript interfaces
pipeline-output.json         Full pipeline result (all 5 stage outputs)
```

The JSON result has 5 top-level sections: `component`, `extraction`, `gap_analysis`,
`generated_code`, `validation`. Check `validation.hallucinations_caught` — if non-empty,
the pipeline already ran re-generation automatically.

## Debugging

- **Figma stage fails "No node-id"**: the Figma URL must contain `?node-id=…` — right-click the frame in Figma → Copy link
- **Figma stage fails "FIGMA_ACCESS_TOKEN not set"**: add `FIGMA_ACCESS_TOKEN=…` to `.env`
- **401 error**: `ANTHROPIC_API_KEY` is wrong or missing in `.env`
- **Zod parse error**: the agent returned malformed JSON — increase `ANTHROPIC_MAX_TOKENS`
- **Hallucinations caught > 0 after 2 re-gens**: inspect `validation.issues_found` and consider editing the component description to be more specific
