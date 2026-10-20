---
name: error-message-ux-writing
description: >
  Write and review user-facing error messages that are actionable, free of
  secrets, and paired with stable machine codes. Use when error copy, 错误文案,
  API error payloads, toast/alert text, form validation messages, or UX review
  of vague/leaky/untranslatable errors. Complements code-quality-standards;
  does not replace logging-message-style.
---

# Error Message UX Writing

## Scope And Authorization

- **In scope:** Product UI/API error strings for systems you own.
- **Out of scope:** Social-engineering copy designed to trick users; leaking other tenants’ data in messages.
- Never put secrets, stack traces, or internal hostnames in user-facing text.
- Support i18n—prefer message ids over hardcoded English-only in multi-locale apps.
- Pair with `logging-message-style` for operator logs and `code-quality-standards`.

## When To Use

- Designing API error envelopes (`code`, `message`, `details`).
- Replacing “Something went wrong” with actionable guidance.
- Fixing messages that enable user enumeration or info disclosure.
- Form validation and payment/checkout failure copy.
- Preparing strings for translation.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Structured logging for ops | `logging-message-style` |
| i18n framework setup | `i18n-l10n-guidelines` |
| Auth enumeration controls depth | auth/ATO skills |
| Implementation quality baseline | `code-quality-standards` |
| Accessibility of error presentation | `accessibility-a11y-checklist` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| User text | What happened + what to do next |
| Machine code | Stable `ERR_*` / numeric for clients |
| Safety | No secrets, tokens, SQL, paths |
| Tone | Blame-free, concise, consistent |
| i18n | ICU/message catalogs; avoid string concat of sentences |
| HTTP | Status conveys class; body conveys detail |

## Workflow

### 1. Confirm scope and success criteria

1. Surfaces: API, web, mobile, email.
2. Success: sample flows show actionable errors; security review finds no leaks; codes documented.

### 2. Inventory current messages

```bash
rg -n "throw new|HttpError|toast\\.|setError\\(|\"error\":" --glob '!node_modules' | head
rg -n "Something went wrong|Internal Server Error|stack" -i
```

1. Collect top support tickets caused by unclear errors.
2. Note where exceptions are `.toString()`’d into responses.

### 3. Define error contract

```json
{
  "error": {
    "code": "PAYMENT_CARD_DECLINED",
    "message": "Your card was declined. Try another card or contact your bank.",
    "request_id": "req_abc123",
    "details": [{ "field": "card", "issue": "declined" }]
  }
}
```

1. `code` stable for clients; `message` may be localized.
2. `request_id` always present for support—never replace the human message.
3. Field errors use structured `details`, not prose-only.

### 4. Write with the checklist

| Check | Pass example | Fail example |
| --- | --- | --- |
| Specific | “Email is not a valid address.” | “Invalid input.” |
| Actionable | “Session expired. Sign in again.” | “Forbidden.” |
| Safe | “Unable to reset password.” | “User exists: true” |
| No stack | — | `NullPointerException at...` |
| Non-enum (when required) | Same text for bad login | “Unknown user” vs “Bad password” |

### 5. Map status codes thoughtfully

| HTTP | Use |
| --- | --- |
| 400 | Validation / malformed |
| 401 | Unauthenticated |
| 403 | Authenticated but not allowed |
| 404 | Missing resource (or mask if enum risk) |
| 409 | Conflict / concurrency |
| 429 | Rate limit with Retry-After |
| 500 | Unexpected; generic user text + log detail |

### 6. Verify with evidence

1. Snapshot tests for error JSON shapes.
2. Manual UX review of top 20 failures.
3. Security pass: grep responses for `Exception`, `at com.`, file paths, SQL.
4. Translation spot-check for truncated or concatenated strings.

### 7. Hand off

1. Error code catalog in docs for client teams.
2. Support macro mapping code → help article.
3. Log full detail server-side with same `request_id`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Copy | “Payment failed—check card details or try another method.” | “Error 5001” only |
| Secrets | Redacted | API key in message |
| Enum | Uniform login error | “Email not registered” |
| i18n | Message id + params | English sentence + glued names |
| Support | request_id in UI | No correlation id |

## Output Checklist

- [ ] Error envelope standard documented
- [ ] Top user-facing paths use actionable copy
- [ ] Stable codes listed
- [ ] No secret/stack leakage verified
- [ ] Enumeration policy applied where needed
- [ ] i18n path considered
- [ ] request_id in user-visible errors
- [ ] Residual risk noted

## Rules

- User messages ≠ log messages—split them.
- Prefer helpful and safe over clever.
- Never expose internal topology.
- Keep codes stable once published.
- Logging style → `logging-message-style`.
