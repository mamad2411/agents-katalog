---
name: web-qa
description: "Test web applications on authenticated pages: navigate flows, check for errors, verify behavior, cross-browser compare, and report findings."
---

# Web QA / Exploratory Testing

Test web applications on authenticated pages using the user's real browser
session. Navigate through flows, check for errors, verify behavior, and
report findings.

## When to Use

- Testing authenticated pages that automated testing tools cannot access
  (staging environments, internal tools, admin panels)
- Exploratory QA sessions on pages behind login
- Verifying deployments or configuration changes on live sites
- Cross-browser testing (compare Chrome vs Safari behavior)

## Workflow

### 1. Verify Connection

Call `list_browsers` to check connected browsers. For cross-browser testing,
ensure both browsers are connected and note their `browserInstanceId` values.

### 2. Read the Page

Call `read_current_page` with `includeContent: true` and an appropriate
`maxContentChunks` value (start with 5, increase for complex pages).

### 3. Systematic Exploration

Walk through the page elements in a structured order:

#### Navigation Audit

- Click each navigation link → verify the destination page loads correctly
- Check for broken links (click leads to 404 or error)
- Verify the active/current state reflects the current page

#### Form Validation Testing

- Submit forms with empty required fields → verify validation messages appear
- Enter invalid data (letters in number fields, short passwords, bad email
  format) → verify appropriate error messages
- Check that error messages are clear and accessible

#### Interactive Element Testing

- Click buttons (actions array) → verify expected behavior occurs
- Toggle checkboxes and radio buttons → verify state changes
- Test select dropdowns → verify options load and selection works
- Test contenteditable areas → verify text input and formatting

#### Accessibility Check

- Verify all images have alt text (visible in content)
- Check heading hierarchy (content should show proper structure)
- Ensure forms have associated labels (check `controls[].label`)
- Verify color contrast is readable (visual review)

#### Cross-Browser Comparison (Multiple Browsers)

When both Chrome and Safari are connected:

1. Read the page on browser A → capture structure and content
2. Read the same page on browser B (using different `browserInstanceId`)
3. Compare: layout, missing elements, broken functionality, visual differences

### 4. Report Findings

Structure the QA report with clear categories:

```markdown
# QA Report: [Page URL]

Date: [timestamp]
Browser: [Chrome/Safari/both]

## Navigation

- ✅ Home link works
- ❌ About link → 404 page
- ✅ Contact link works

## Forms

- ✅ Login form validates empty fields
- ❌ Email field accepts "test@" (should reject invalid email)
- ✅ Password field shows masking

## Accessibility

- ⚠️ Logo image missing alt text
- ✅ Form labels present for all inputs
- ❌ Color contrast insufficient on secondary buttons

## Cross-Browser

- ❌ Safari: dropdown options not rendering correctly
- ✅ Chrome: all interactive elements functional
```

## Pitfalls

### Page State Mutation

QA testing changes page state. After filling forms, clicking buttons, or
submitting data, the page may redirect or change. Always re-read the page
after interactions to get fresh element IDs.

### Destructive Actions

Avoid testing destructive actions (delete, remove, reset) without the user's
explicit permission. These actions are **irreversible** on real data. Ask
before clicking any "Delete", "Remove", or "Reset" action.

### Session Expiry

Long QA sessions may encounter session timeouts. If the page suddenly shows
a login screen, ask the user to re-authenticate before continuing.

### Dynamic Content

SPAs may update content without page reloads. The page context read at
time T may be stale at time T+1 for dynamic elements. Re-read before
asserting element state.

### Rate Limiting and Anti-Bot

Rapid clicks and form submissions through Brijio may trigger
rate-limiting or anti-bot protections on the target site. Add brief pauses
between rapid interactions.

### Short-Lived IDs

Element IDs expire on navigation and DOM changes. After any click that
triggers a page update, re-read before referencing new element IDs.

## Example: Login Page QA

```
1. list_browsers → Confirm browser connected
2. read_current_page → Get login page context
3. Test empty submit:
   - click_element(kind: "action", id: "a3")  // "Sign In" button
   - read_current_page → Verify validation errors appear
4. Test invalid email:
   - fill_input(formId: "f1", controlId: "c1", text: "not-an-email")
   - click_element(kind: "action", id: "a3")  // Submit
   - read_current_page → Verify "Invalid email" error
5. Test password masking:
   - Verify password field exists with type="password" (cannot fill via BB)
6. Test valid flow:
   - fill_input(formId: "f1", controlId: "c1", text: "user@example.com")
   - Ask user to enter password manually
   - Ask user to click Submit
7. read_current_page → Verify successful redirect to dashboard
8. Generate QA report
```
