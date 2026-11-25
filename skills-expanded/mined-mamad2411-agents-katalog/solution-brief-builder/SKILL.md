---
name: solution-brief-builder
description: Generates a print-ready Databricks-branded HTML/PDF solution brief for a customer demo app. Use when asked for a "solution brief", "leave-behind", "customer one-pager", or "print-ready PDF" for a Databricks app demo. Produces a self-contained letter-size HTML file with embedded screenshots and converts to PDF via Chrome headless. NOT for slide decks or presentations — use for printed/PDF customer leave-behinds only.
user-invocable: true
argument-hint: <app-name or description>
---

# Solution Brief Builder

Generates a polished, print-ready HTML one-pager in Databricks brand style — same format as the **Clinical Operations Intelligence** brief (canonical example in `references/clinops-example.md`).

## Reference Materials

- **HTML structure + CSS variables**: [references/template.md](references/template.md)
- **ClinOps session example notes**: [references/clinops-example.md](references/clinops-example.md)

---

## Phase 1 — Gather Information

Before generating anything, collect the following. Check what the user already provided and **only ask for what is missing**. Group all questions into a single prompt rather than asking one at a time.

### Required Fields (must have before generating)

| Field | Prompt if missing | Example |
|---|---|---|
| `APP_NAME` | "What is the display name of the app?" | Enrollment Velocity Optimizer |
| `APP_TAGLINE` | "Give me a one-line tagline/elevator pitch for this app (≤15 words)." | Predict site stall risk before it happens — and intervene earlier. |
| `TARGET_PERSONA` | "Who is the primary buyer or end-user persona (title + context)?" | VP of Clinical Operations, CRO |
| `CHALLENGES` | "What are the top 2–3 business challenges this app solves?" | Late-stage enrollment stalls; no early warning system; site blame game |
| `VALUE_OUTCOMES` | "What are the top 2–3 measurable outcomes or benefits?" | 30% faster stall detection; AI explains every prediction; one workflow for 3 personas |
| `KEY_CAPABILITIES` | "List 3–5 key capabilities (short phrases)." | Stall risk score per site, SHAP driver attribution, persona-aware collaboration, intervention tracking |
| `DATABRICKS_FEATURES` | "Which Databricks platform features does this app highlight?" | LightGBM via MLflow, SHAP explainability, Lakebase persistence, SQL Warehouse, Databricks Apps |

### Optional Fields (use defaults if omitted)

| Field | Default | Notes |
|---|---|---|
| `APP_URL` | *(omit)* | Include as footer link if provided; also used for auto-screenshot |
| `SCREENSHOT_PATH` | *(omit)* | If provided manually, embed as base64 in the HTML; otherwise auto-capture via Phase 1b |
| `CUSTOMER_ACCOUNT` | *(omit)* | If provided, make the brief account-specific (add logo placeholder) |
| `INDUSTRY_VERTICAL` | Life Sciences / Clinical Trials | Change if app is for a different vertical |
| `OUTPUT_FILENAME` | `<kebab-app-name>-solution-brief.html` | Saved to `~/Desktop/` |
| `ARCHITECTURE_NOTES` | *(derive from features)* | Any extra context for the architecture diagram |

---

## Phase 1b — Auto-Screenshot (run when APP_URL is known)

If `APP_URL` is available and `SCREENSHOT_PATH` was not manually provided, automatically capture a screenshot of the live app using the Chrome DevTools MCP **before** generating the HTML. Do not ask the user to provide a screenshot first.

### Steps

**1. Open the app in Chrome:**
```
mcp__chrome-devtools__new_page
  url: <APP_URL>
```

**2. Resize to a clean desktop viewport:**
```
mcp__chrome-devtools__resize_page
  width: 1440
  height: 900
```

**3. Wait for the app to finish loading** — use meaningful UI text that appears once the app is interactive (e.g., the app's heading, a button label, or a data table value). Timeout 20 seconds:
```
mcp__chrome-devtools__wait_for
  text: ["<app_heading_or_known_ui_text>"]
  timeout: 20000
```
If the exact text is unknown, wait for common landmarks: `["Loading", "Dashboard", "Filter", "Search"]` — use whichever is appropriate for the app. If wait times out, proceed anyway.

**4. Save the screenshot directly to a temp file:**
```
mcp__chrome-devtools__take_screenshot
  filePath: /tmp/<kebab-app-name>-screenshot.png
```
`filePath` saves the file directly — no manual base64 step needed from the response.

**5. Base64-encode for HTML embedding:**
```bash
base64 < /tmp/<kebab-app-name>-screenshot.png
```
Capture the output as `SCREENSHOT_B64`.

**6. Set `SCREENSHOT_PATH`** = `/tmp/<kebab-app-name>-screenshot.png` so Phase 2 embeds it rather than using the placeholder.

### Auth Wall Handling
Databricks Apps redirect to Okta for authentication. If the page lands on a login screen:
- **Do not attempt to fill credentials.** Chrome DevTools MCP shares the user's browser session, so Okta passkey/biometric auth typically resolves automatically within a few seconds.
- Call `take_screenshot` immediately after the redirect — by the time the tool executes, the session cookie often satisfies the auth and the app loads.
- If the app still hasn't loaded, call `wait_for` with known app UI text (e.g., the app title) with a 15–20s timeout to let auth complete.

### Fallback
If the page fails to load (network error, persistent auth wall after 20s), log a note and fall back to the placeholder div — do not block brief generation.

---

## Phase 2 — Generate the HTML

Use [references/template.md](references/template.md) as the structural blueprint. The output is a **single self-contained HTML file** (no external CSS/JS dependencies) with these sections:

### One-Pager Structure (single page, letter size)

The default brief for a single app is **one page** (the per-app one-pager). If the user wants a multi-page document (cover + multiple apps + architecture), expand to the multi-page format described in [references/clinops-example.md](references/clinops-example.md).

**Single-page layout:**

```
┌─────────────────────────────────────────┐
│ HEADER: Databricks logo + doc label     │  ← 0.16in margin-bottom
├─────────────────────────────────────────┤
│ HERO: App name + tagline                │  ← red eyebrow, dark h1, muted tagline
├──────────────────┬──────────────────────┤
│  LEFT COLUMN     │  RIGHT COLUMN        │
│  (~45%)          │  (~55%)              │
│                  │                      │
│  THE CHALLENGE   │  [SCREENSHOT]        │
│  • bullet 1      │  (full width of col) │
│  • bullet 2      │                      │
│  • bullet 3      │  AI CALLOUT BOX      │
│                  │  ──────────────────  │
│  KEY CAPABILITIES│  "Key insight or     │
│  ─────────────── │   stat highlighted"  │
│  • feature 1     │                      │
│  • feature 2     │                      │
│  • feature 3     │                      │
│  • feature 4     │                      │
│                  │                      │
│  DATABRICKS      │                      │
│  PLATFORM USED   │                      │
│  [chip] [chip]   │                      │
│  [chip] [chip]   │                      │
├─────────────────────────────────────────┤
│ VALUE OUTCOMES (3-col cards at bottom)  │
├─────────────────────────────────────────┤
│ FOOTER: © Databricks + app URL          │
└─────────────────────────────────────────┘
```

### CSS Design Tokens (never deviate from these)

```css
--red:   #FF3621;   /* Databricks red — used for eyebrow labels, accents */
--green: #00A972;   /* AI/value callouts */
--dark:  #1B3139;   /* Dark navy — headings, cover backgrounds */
--pale:  #E6F7F1;   /* Light green tint — AI callout backgrounds */
--body:  #2D3748;   /* Body text */
--muted: #6B7280;   /* Captions, metadata */
--rule:  #E5E7EB;   /* Dividers */
```

Font: `DM Sans` via Google Fonts import (always include the `@import` at top of `<style>`).

Page size: `width: 8.5in; min-height: 11in;` with `margin: 0.3in auto;` and `padding: 0.38in 0.58in;`.

### Embedding a Screenshot

If `SCREENSHOT_PATH` is provided:
1. Read the file and convert to base64: `base64 < <path>`
2. Embed as `<img src="data:image/png;base64,<base64>" ...>`
3. Style with `border-radius: 8px; box-shadow: 0 4px 18px rgba(0,0,0,0.14); width: 100%;`

If no screenshot is provided, use a **placeholder div** styled as:
```html
<div style="background:#F3F4F6; border-radius:8px; height:200px; display:flex;
            align-items:center; justify-content:center; color:#9CA3AF;
            font-size:11pt; border:2px dashed #D1D5DB;">
  [App Screenshot]
</div>
```

### AI Callout Box Pattern

Used to highlight a key AI/ML stat or insight:
```html
<div style="background:var(--pale); border-left:3px solid var(--green);
            border-radius:6px; padding:12px 14px; margin-top:14px;">
  <div style="font-size:7.5pt; font-weight:700; text-transform:uppercase;
              letter-spacing:0.1em; color:var(--green); margin-bottom:5px;">
    AI-Powered Insight
  </div>
  <div style="font-size:9pt; color:var(--dark); line-height:1.55;">
    <!-- stat or key finding here -->
  </div>
</div>
```

### Platform Feature Chips

```html
<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">
  <span style="background:#F3F4F6; border-radius:20px; padding:3px 10px;
               font-size:7.5pt; color:var(--body);">MLflow</span>
  <!-- repeat per feature -->
</div>
```

### Value Outcome Cards (bottom strip, 3 columns)

```html
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:18px;">
  <div style="background:#F9FAFB; border-radius:8px; padding:14px 16px; border-top:3px solid var(--red);">
    <div style="font-size:14pt; font-weight:700; color:var(--dark);">{{METRIC}}</div>
    <div style="font-size:8pt; color:var(--muted); margin-top:4px;">{{DESCRIPTION}}</div>
  </div>
</div>
```

---

## Phase 3 — Save and Convert to PDF

1. Save the HTML to `~/Desktop/<OUTPUT_FILENAME>` (or user-specified path)
2. **Immediately convert to PDF using Chrome headless** — do not ask the user to print manually. Detect Chrome using the first match:

```bash
# Detect Chrome (macOS or Linux)
CHROME=$(command -v google-chrome || command -v chromium || command -v chromium-browser \
  || echo "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

"$CHROME" \
  --headless=new \
  --disable-gpu \
  --print-to-pdf="$HOME/Desktop/{{OUTPUT_FILENAME_PDF}}" \
  --print-to-pdf-no-header \
  --no-margins \
  "file://$HOME/Desktop/{{OUTPUT_FILENAME}}"
```

Replace `{{OUTPUT_FILENAME_PDF}}` with the same name but `.pdf` extension.

3. Confirm both outputs: "Saved `~/Desktop/<name>.html` and `~/Desktop/<name>.pdf`."
4. If Phase 1b ran successfully, confirm the screenshot was auto-captured and embedded. If it fell back to the placeholder, offer to retry: "The app screenshot could not be captured automatically (possible auth wall). Do you want me to try again or provide a path to a local screenshot?"

---

## Quality Checklist

Before outputting, verify:
- [ ] No raw technical table names (e.g., `gold_model_predictions`) visible in body text — use business language
- [ ] No model metrics (MAE, F1) unless rephrased as business outcomes ("78% stall prediction accuracy")
- [ ] No customer names (J&J, Pfizer, etc.) unless user explicitly says this is account-specific
- [ ] All CSS uses the defined `--red / --green / --dark` color tokens
- [ ] Font is DM Sans (Google Fonts import present)
- [ ] File is self-contained (no external JS/CSS links except Google Fonts)
- [ ] Print-ready: `@media print` block with `page-break-after: always` and `print-color-adjust: exact`
