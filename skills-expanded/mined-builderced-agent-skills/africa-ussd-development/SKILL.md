---
name: africa-ussd-development
description: Build USSD applications for African markets — menu design, session management, multi-operator integration, and user experience patterns for feature phones.
version: "1.0.0"
last-updated: "2026-04-22"
model_tested: "claude-sonnet-4-6"
category: africa
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [africa]
priority: medium
dependencies:
  mcp: []
  skills: [africa-mobile-money]
  apis: []
  data: []
update_sources:
  - url: "https://africastalking.com/ussd"
    check_frequency: "yearly"
    last_checked: "2026-04-22"
license: MIT
---

# Africa USSD Development

> **DISCLAIMER**: USSD regulations vary by country and operator. Verify with local telecom authorities.

## When to Use

- Building apps for feature phone users (no internet required)
- Creating mobile money menus or services
- Designing interactive text-based interfaces
- Integrating with African telecom operators

## USSD Fundamentals

USSD (Unstructured Supplementary Service Data) = real-time text session between phone and server. No internet needed. Works on ANY phone (feature phone or smartphone).

### Key Constraints
| Constraint | Limit |
|-----------|-------|
| Message length | 182 characters max per screen |
| Session timeout | 120-180 seconds (operator-dependent) |
| Input | Numeric only (0-9, *, #) |
| Navigation | No back button (must design "0 for back") |
| Connectivity | Real-time (not store-and-forward like SMS) |

## Menu Design Patterns

### Basic Menu
```
Welcome to MyService
1. Check balance
2. Send money
3. Buy airtime
4. My account
0. Exit
```

### Pagination (Long Lists)
```
Select product (1/3):
1. Rice 5kg - 2500 CFA
2. Sugar 1kg - 800 CFA
3. Oil 1L - 1200 CFA
98. Next page
0. Back
```

### Confirmation Pattern
```
Send 5000 CFA to Amadou (77X XX XX)?
1. Confirm
2. Cancel
```

### Input Collection
```
Enter amount (CFA):
```
Then validate: numeric, min/max, divisible by denomination.

## Session Architecture

```
Phone → *123# → Operator → Your Server (HTTP POST)
                                ↓
                         Process + respond
                                ↓
                    Response text (182 chars max)
                                ↓
                         Phone displays
```

### Server Response Format
Most operators expect:
- `CON` prefix = continue session (expect more input)
- `END` prefix = close session

```
CON Welcome\n1. Balance\n2. Transfer
```
```
END Your balance is 15,000 CFA. Thank you.
```

## Multi-Operator Integration

| Provider | Coverage | API |
|----------|----------|-----|
| Africa's Talking | 20+ countries | REST, webhooks |
| Twilio | Limited Africa | REST |
| Infobip | 15+ countries | REST |
| Direct operator | Per country | SMPP/HTTP varies |

### Africa's Talking (Recommended for Multi-Country)
```
POST callback URL receives:
- sessionId: unique per session
- phoneNumber: caller MSISDN
- text: accumulated input (separated by *)
- serviceCode: your USSD shortcode
```

## UX Best Practices

1. **Max 3 levels deep** — users lose context after 3 menus
2. **Always offer exit** — "0. Exit" on every screen
3. **Confirm destructive actions** — money transfers, cancellations
4. **Short messages** — 182 chars including options
5. **Numeric shortcuts** — power users dial full path: `*123*1*2#`
6. **Language selection first** — if multilingual market
7. **Error messages clear** — "Invalid choice. Try again:" not "Error 422"
8. **Session state on server** — phone has no state

## Testing

- Test with actual phones (emulators miss operator quirks)
- Test session timeout handling
- Test on slow networks (USSD can lag 3-5s per round trip)
- Test with different operators in target market

## What This Skill Does NOT Do

- Does not provide USSD shortcodes (apply through operator)
- Does not handle SMS (different protocol)
- Does not manage telecom operator relationships
- Does not cover IVR (voice-based menus)
