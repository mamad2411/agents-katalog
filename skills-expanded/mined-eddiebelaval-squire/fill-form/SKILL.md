---
name: Fill Form
slug: fill-form
description: **Trigger:** `/fill-form [URL] [optional: form data file]`
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "fill-form"
  - "fill form"
tags:
  - operations
  - tool-factory-retrofitted
---

# Form Filling Skill


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

**Trigger:** `/fill-form [URL] [optional: form data file]`

## Purpose
Automate web form filling with built-in retry logic and verification, addressing common friction points from browser automation.

## Workflow

### 1. Pre-Flight Check
- Verify URL is accessible (retry with alternate patterns if 404)
- Take initial screenshot for reference
- Identify form fields using accessibility tree snapshot

### 2. Field Filling Protocol
For each form field:

**Text Inputs:**
- Clear existing value first
- Type with realistic delays (50-100ms between keystrokes)
- Verify value after input

**Dropdowns/Selects (CRITICAL - High friction area):**
- Click to open dropdown
- Wait 300ms for options to render
- Select the option
- Wait 300ms for UI to settle
- **VERIFY:** Check selected value matches expected
- If mismatch: Retry selection up to 2 more times
- If still failing: Screenshot and report, continue with other fields

**Checkboxes/Radio:**
- Verify current state before clicking
- Click to toggle
- Verify new state matches expected

**Date Pickers:**
- Try native input first (type date string)
- If custom picker: Click to open, navigate to date, select
- Verify selected date

### 3. Navigation Handling
- Use `waitUntil: 'networkidle'` for all navigations
- If page not found (404):
  1. Try removing trailing slash
  2. Try adding /app or /portal prefix
  3. Try www subdomain
  4. Screenshot and report if all fail

### 4. Form Submission
- Screenshot form BEFORE submission
- Click submit button
- Wait for network idle
- Check for:
  - Success indicators (confirmation message, redirect)
  - Error messages (validation failures)
  - Unchanged state (submission may have failed silently)
- Screenshot AFTER submission

### 5. Error Recovery
- On transient errors: Auto-retry once after 2 second wait
- On validation errors: Report specific field failures
- On timeout: Extend wait, retry submission
- Log all failures to `~/form-automation-logs/{date}.json`

## Usage Examples

```
/fill-form https://example.com/application
```
Interactive mode - Claude will ask for field values as needed.

```
/fill-form https://example.com/application ./form-data.json
```
Batch mode - Uses provided JSON file for field values.

## Form Data JSON Format
```json
{
  "fields": {
    "firstName": "Eddie",
    "lastName": "Belaval",
    "email": "eddie@example.com",
    "state": "CA",
    "agreeToTerms": true
  },
  "submit_button": "#submit-btn",
  "success_indicator": ".confirmation-message"
}
```

## Output
- Screenshots: Before and after submission
- Log file: Detailed step-by-step with timings
- Summary: Fields filled, retries needed, final status

## Signals
- "Form filling: Starting [URL]..."
- "Field [name]: Filled successfully" / "Field [name]: Required retry"
- "Dropdown verification: PASSED/FAILED for [field]"
- "Form submission: SUCCESS/FAILED - [details]"
