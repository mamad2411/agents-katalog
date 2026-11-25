---
name: fill-form
description: >
  Fill out web forms with human-like anti-detection typing. Applications, registration,
  checkout, surveys, contact forms. Use when: "fill out form", "complete application",
  "register on", "submit form", "fill in details", "checkout", "sign up on".
disable-model-invocation: true
allowed-tools:
  - mcp__sh__browser_stealth
  - mcp__sh__browser_open
  - mcp__sh__browser_navigate
  - mcp__sh__browser_dom
  - mcp__sh__browser_fill_form
  - mcp__sh__browser_click
  - mcp__sh__browser_wait
  - mcp__sh__browser_js
  - mcp__sh__browser_page_info
  - mcp__sh__key
  - mcp__sh__type_text
  - mcp__sh__select_with_fallback
  - mcp__sh__click_with_fallback
  - mcp__sh__type_with_fallback
  - mcp__sh__read_with_fallback
  - mcp__sh__screenshot_file
  - mcp__sh__playbook_preflight
  - mcp__sh__observer_start
  - mcp__sh__observer_status
  - mcp__sh__observer_stop
  - mcp__sh__memory_recall
  - mcp__sh__memory_save
  - mcp__sh__memory_query_patterns
---

# Form Filling with Anti-Detection

You are filling out a web form using ScreenHand's browser automation with human-like behavior.

## Intelligence Wrapper

Every tool call returns automatic hints from the server. Watch for:
- **`[HINT]`** — selector suggestions, known working patterns from past sessions
- **`[WARNING]`** — this tool has failed before on this domain, here's the fix
- **`[STRATEGY]`** — suggested next step based on past successful form-fill sequences

Always read and act on these hints.

## Setup

1. `browser_stealth()` — ALWAYS call first. Patches automation detection markers.
2. `playbook_preflight(url)` — check for CAPTCHA, bot detection systems.
3. `memory_recall(task="fill form {domain}")` — check past strategies.
4. `memory_query_patterns(scope="{domain}")` — check verified selectors for this site.
5. `observer_start(bundleId="com.google.Chrome")` — detect popups, cookie banners, CAPTCHA dialogs during filling.

## Step 1: Discover Form Fields

```
browser_dom(selector="input, select, textarea, [contenteditable='true']")
```

This returns all form fields with their:
- `type` (text, email, password, tel, number, date, checkbox, radio, file)
- `name` and `id` attributes
- `placeholder` and `aria-label` for context
- `required` attribute

Map each field to the data the user wants to fill.

## Step 2: Fill Fields (Human-Like)

**Text fields** — use `browser_fill_form` (character-by-character with randomized delays):
```
browser_fill_form(selector="input[name='email']", text="user@example.com")
```

If `browser_fill_form` fails, fall back to `type_with_fallback(label="Email", text="user@example.com")` which tries AX → CDP automatically.

**Order**: Fill fields top-to-bottom, tab between them naturally.

**For each field**:
1. Click the field: `browser_click(selector="...")` or `click_with_fallback(text="Email")`
2. Clear existing content: `browser_js(expression="document.querySelector('...').value = ''")`
3. Fill: `browser_fill_form(selector, text)`

## Step 3: Special Field Types

**Dropdowns (`<select>`):**
```
select_with_fallback(label="Country", value="United States")
```

**Checkboxes/Radio buttons:**
```
browser_click(selector="input[name='agree']")
```
Or click the label: `click_with_fallback(text="I agree")`

**Date pickers:**
- Try `browser_js` to set value directly: `el.value = '2024-03-15'; el.dispatchEvent(new Event('change'))`
- If custom picker: click to open, navigate months, click date

**File uploads:**
1. `browser_dom(selector="input[type='file']")`
2. `browser_js(expression="document.querySelector('input[type=file]').click()")`
3. File dialog opens — use `type_text` to enter the file path + `key("enter")` to confirm

**Rich text editors (contenteditable):**
```
browser_click(selector="[contenteditable='true']")
browser_fill_form(selector="[contenteditable='true']", text="Content here")
```

## Step 4: CAPTCHA & Popup Check

Check `observer_status()` — the observer detects cookie banners, permission dialogs, and CAPTCHA overlays automatically.

Also check manually:
```
browser_dom(selector="iframe[src*='captcha'], iframe[src*='recaptcha'], [class*='captcha']")
```

If CAPTCHA found:
- Take `screenshot_file`
- Tell the user: "A CAPTCHA is present. Please solve it manually, then tell me to continue."
- Wait for user confirmation before submitting

## Step 5: Submit

1. Find submit button: `browser_dom(selector="button[type='submit'], input[type='submit']")`
2. Click with `click_with_fallback(text="Submit")` — tries AX → CDP → OCR
3. Wait for response: `browser_wait(condition="!document.querySelector('button[type=submit][disabled]')")`
4. Take `screenshot_file` for confirmation

## Step 6: Verify Success

Check for:
- Success message: `read_with_fallback(text="Thank you")` or `browser_dom(selector="[class*='success'], [role='alert']")`
- URL change: `browser_page_info` — did we navigate to a confirmation page?
- Error messages: `browser_dom(selector="[class*='error'], [aria-invalid='true'], .field-error")`

If errors found: read them, correct the fields, resubmit.

## Multi-Page Forms

For forms that span multiple pages:
1. Fill current page
2. Click "Next" / "Continue" via `click_with_fallback(text="Next")`
3. `browser_wait` for new fields to load
4. Repeat until final submission

## Cleanup

- `observer_stop()` — stop popup detection
- `memory_save(task="fill form on {domain}: {form_type}")` — persist the strategy

$ARGUMENTS
