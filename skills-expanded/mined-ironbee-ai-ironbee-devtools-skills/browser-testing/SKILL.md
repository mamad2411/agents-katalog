---
name: browser-testing
description: Automated browser testing, interaction automation, and form testing. Use when the user needs to test web pages, automate browser interactions, fill forms, test validation, run multi-step wizards, or test login/signup flows.
allowed-tools: Bash(ironbee-browser-devtools-cli:*)
---

# Browser Testing Skill

Automated browser testing, interaction automation, and form testing using Browser DevTools CLI.

## When to Use

This skill activates when:
- User asks to test a web page or application
- User wants to automate browser interactions
- User needs to verify UI behavior
- User wants to automate form submission
- User needs to test form validation
- User mentions multi-step forms or wizards
- User wants to test login/signup flows

## Capabilities

### Navigation
```bash
ironbee-browser-devtools-cli navigation go-to --url "https://example.com"
ironbee-browser-devtools-cli navigation go-back-or-forward --direction back
ironbee-browser-devtools-cli navigation go-back-or-forward --direction forward
ironbee-browser-devtools-cli navigation reload
```

### Interaction
All accept CSS selector or ref (e1, @e1) from ARIA snapshot.

```bash
ironbee-browser-devtools-cli interaction click --selector "#button"
ironbee-browser-devtools-cli interaction click --selector "e1"   # ref from a11y take-aria-snapshot
ironbee-browser-devtools-cli interaction fill --selector "#input" --value "text"
ironbee-browser-devtools-cli interaction select --selector "#dropdown" --value "option"
ironbee-browser-devtools-cli interaction hover --selector "#element"
ironbee-browser-devtools-cli interaction press-key --key "Enter"
ironbee-browser-devtools-cli interaction scroll --mode bottom
ironbee-browser-devtools-cli interaction drag --source-selector "#drag" --target-selector "#drop"
```

### Content Capture
```bash
ironbee-browser-devtools-cli content take-screenshot --name "screenshot"
ironbee-browser-devtools-cli content get-as-html
ironbee-browser-devtools-cli content get-as-text
ironbee-browser-devtools-cli content save-as-pdf --name "page"
```

### Synchronization
```bash
ironbee-browser-devtools-cli sync wait-for-network-idle
```

### Mocking & Stubbing
```bash
ironbee-browser-devtools-cli stub mock-http-response --pattern "**/api/**" --response '{"status":200}'
ironbee-browser-devtools-cli stub intercept-http-request --pattern "**/api/**" --modifications '{"headers":{}}'
ironbee-browser-devtools-cli stub list
ironbee-browser-devtools-cli stub clear
```

## Basic Testing Workflow

1. **Navigate**: Go to the page under test
2. **Wait**: Ensure page is fully loaded
3. **Snapshot** (optional): `a11y take-aria-snapshot` to get refs (e1, e2) for stable element targeting
4. **Interact**: Click, fill, scroll (use `--selector "e1"` for refs or CSS selector)
5. **Verify**: Check page state, take screenshots
6. **Document**: Report results

## Form Automation Patterns

### Basic Form Fill

```bash
# Fill text input
ironbee-browser-devtools-cli interaction fill \
  --selector "#email" \
  --value "test@example.com"

# Fill password
ironbee-browser-devtools-cli interaction fill \
  --selector "#password" \
  --value "SecurePass123"

# Click submit
ironbee-browser-devtools-cli interaction click \
  --selector "button[type=submit]"
```

### Select Dropdown

```bash
ironbee-browser-devtools-cli interaction select \
  --selector "#country" \
  --value "US"
```

### Checkbox/Radio

```bash
# Check checkbox
ironbee-browser-devtools-cli interaction click \
  --selector "#terms-checkbox"

# Select radio option
ironbee-browser-devtools-cli interaction click \
  --selector "input[name=plan][value=premium]"
```

### Multi-Step Wizard

```bash
SESSION="--session-id wizard-test"

# Step 1: Personal Info
ironbee-browser-devtools-cli $SESSION interaction fill --selector "#name" --value "John Doe"
ironbee-browser-devtools-cli $SESSION interaction fill --selector "#email" --value "john@example.com"
ironbee-browser-devtools-cli $SESSION interaction click --selector "#next-step"

# Wait for step 2
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# Step 2: Address
ironbee-browser-devtools-cli $SESSION interaction fill --selector "#address" --value "123 Main St"
ironbee-browser-devtools-cli $SESSION interaction select --selector "#state" --value "CA"
ironbee-browser-devtools-cli $SESSION interaction click --selector "#next-step"

# Step 3: Confirm
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle
ironbee-browser-devtools-cli $SESSION interaction click --selector "#submit"
```

## Validation Testing

### Test Required Fields

```bash
# Submit empty form
ironbee-browser-devtools-cli interaction click --selector "button[type=submit]"

# Check for error messages
ironbee-browser-devtools-cli content get-as-text --selector ".error-message"
```

### Test Invalid Input

```bash
# Invalid email
ironbee-browser-devtools-cli interaction fill --selector "#email" --value "not-an-email"
ironbee-browser-devtools-cli interaction click --selector "button[type=submit]"

# Check validation error
ironbee-browser-devtools-cli content get-as-html --selector ".email-error"
```

## Session-Based Testing

```bash
SESSION="--session-id my-test"

# Navigate
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://example.com"

# Interact
ironbee-browser-devtools-cli $SESSION interaction click --selector ".login-btn"
ironbee-browser-devtools-cli $SESSION interaction fill --selector "#email" --value "test@example.com"

# Verify
ironbee-browser-devtools-cli $SESSION content take-screenshot --name "after-login"

# Cleanup
ironbee-browser-devtools-cli session delete my-test
```

## Best Practices

1. **Use sessions** for multi-step flows
2. **Wait for network idle** after navigation and actions
3. **Take screenshots** after important actions for verification
4. **Use specific selectors** to avoid wrong elements
5. **Test empty submission** first for validation testing
6. **Clear fields** before filling (use `interaction fill` which clears first)
7. **Handle dynamic fields** with wait strategies
8. **Screenshot after errors** for documentation
9. **Batch steps when useful**: For long flows, `run execute --code "..."` with `callTool()` reduces round-trips (see ironbee-browser-devtools-cli execute reference).
