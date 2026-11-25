---
name: onboarding
description: "Complete new account onboarding flows: multi-step registration, email verification, profile setup, and preference configuration on authenticated pages."
---

# New Account Onboarding

Guide users through multi-step account creation and onboarding flows on web
applications. Handles signup forms, email verification, profile completion, and
preference setup — the full journey from landing on a signup page to a fully
configured account.

## When to Use

- Setting up new accounts on web platforms
- Testing signup and onboarding flows
- Completing profile information after registration
- Configuring preferences on a new account
- Any multi-step registration wizard flow

## Workflow

### 1. Check Connection

```
list_browsers → Confirm browser connected
```

### 2. Navigate to Signup

If not already on the signup page, use the [navigation](skill://brijio/navigation) skill to get there. Look for links like:

- "Sign up", "Create account", "Register", "Get started"
- Avoid "Sign in" / "Log in" — these are for existing accounts

### 3. Fill Registration Form

```
1. read_current_page → Get signup form
2. fill_input → Name, email, username fields
3. set_checked → Agreement checkboxes, newsletter opt-ins
4. ⚠️ Skip password fields — they return browser_error
5. Ask user for password or let them fill it manually
```

### 4. Handle Email Verification

After submitting the registration form:

1. The page will show a "Check your email" or "Verify your account" message
2. Ask the user to open the verification email
3. **Option A:** The user clicks the link in their email, which opens in the
   same browser → `read_current_page` to see the verified account
4. **Option B:** The page has a code input → ask the user for the code, then
   `fill_input` the verification code field

### 5. Complete Profile

Most platforms show a profile completion wizard after verification:

```
1. read_current_page → Get profile form
2. fill_input → Bio, location, website fields
3. select_options → Industry, role, experience dropdowns
4. set_checked → Notification preferences, interest tags
5. click_element(kind: "action") → "Continue" / "Next"
6. read_current_page → Next profile step
```

Handle each step of the wizard, re-reading the page after each navigation.

### 6. Configure Preferences

After the basic profile, there may be preference screens:

- Topic/content interests (checkboxes)
- Notification settings (checkboxes, dropdowns)
- Privacy settings (radio buttons)
- Integration/connect accounts (links)

Fill these based on the user's instructions. If the user hasn't specified
preferences, present the options and ask.

### 7. Skip Optional Steps

Onboarding flows often include optional steps ("Connect your calendar",
"Invite teammates", "Upload a photo"). These usually have "Skip" or "Do later"
actions. If the user doesn't want to complete optional steps:

```
click_element(kind: "action", id: "a_skip") → Skip optional step
```

### 8. Verify Onboarding Complete

After all onboarding steps, `read_current_page` should show the main dashboard
or home page. Confirm with the user that onboarding is complete.

## Common Onboarding Patterns

### Google-Style Account Creation

```
Step 1: Name + Username
Step 2: Password (user fills manually)
Step 3: Phone verification (user handles)
Step 4: Terms agreement
→ Dashboard
```

### SaaS App Onboarding

```
Step 1: Work email
Step 2: Company name + team size
Step 3: Invite teammates (optional — skip)
Step 4: Choose plan
Step 5: Configure preferences
→ Dashboard
```

### Social Platform Signup

```
Step 1: Name + email + password (user fills password)
Step 2: Email verification
Step 3: Profile photo + bio
Step 4: Follow suggestions / interests
Step 5: Notification preferences
→ Feed / Home
```

## Pitfalls

### Password Fields

Registration forms always include password fields (often two: password +
confirm password). Brijio returns `browser_error` for these. **Skip
them** and let the user fill them manually. This is a security feature, not a
bug.

### CAPTCHA

Some signup flows include CAPTCHA challenges. Brijio cannot solve these.
Ask the user to complete the CAPTCHA manually, then continue with the rest of
the form.

### Email Verification Codes

Verification codes expire (typically 5-15 minutes). If the user hasn't checked
their email yet, don't fill the code field until they provide the code. If the
code expires, look for a "Resend" action to get a new one.

### Progressive Onboarding

Some platforms don't show all onboarding steps at once. After completing one
step, the next may appear on a subsequent visit. Check if the page shows
"Complete your profile" or similar prompts.

### Auto-Generated Passwords

Some platforms generate a temporary password and send it via email. If the
signup form includes a "Show password" or "Copy password" action, the user
should handle this — don't attempt to read or fill generated passwords.

### Mandatory vs Optional Fields

Onboarding forms mix required and optional fields. Required fields will have
validation that prevents proceeding without them. Optional fields can be skipped.
When in doubt, present the fields to the user and ask which to fill.
