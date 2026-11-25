---
name: "Error Message Optimizer"
version: "1.0.0"
description: "Optimizes error messages for clarity, actionability, and user experience. Transforms technical errors into user-friendly messages."
author: "workspace"
activated: false
---

# Error Message Optimizer

Optimizes error messages for clarity, actionability, and user experience. Transforms technical errors into user-friendly messages.

## Decision Framework

### When to Apply
Use when: Form validation, API error handling, user-facing error states, onboarding flows

### When NOT to Apply
Don't use when: Internal logging only, developer-only tools

## Anti-Patterns

### 1. Technical Errors to Users
```javascript
// BAD
"Error: ECONNREFUSED 127.0.0.1:5432"

// GOOD
"We couldn't connect to our servers. Please try again in a few moments."
```

### 2. Blame Language
```javascript
// BAD: Blames user
"You entered an invalid email address"

// GOOD: Neutral
"Please enter a valid email address (e.g., name@example.com)"
```

### 3. No Recovery Path
```javascript
// BAD: Dead end
"Error occurred"

// GOOD: Actionable
"Your session expired. <a href='/login'>Sign in again</a> to continue."
```


## Trigger Phrases

- "Improve error messages"
- "User-friendly errors"
- "Form validation messages"
- "Error UX"

## Patterns

### Error Message Map
```javascript
const errorMessages = {
  'auth/invalid-email': {
    user: 'Please enter a valid email address.',
    action: 'highlight-field',
    recovery: 'Check for typos in your email.'
  },
  'auth/user-not-found': {
    user: 'No account found with this email.',
    action: 'show-signup-link',
    recovery: 'Would you like to create an account?'
  },
  'network/timeout': {
    user: 'The request took too long. Please try again.',
    action: 'show-retry-button',
    recovery: 'Check your internet connection.'
  }
};
```

## Integration
- Works with: form-pattern-engine, accessibility-pattern-library, notification-system-builder

