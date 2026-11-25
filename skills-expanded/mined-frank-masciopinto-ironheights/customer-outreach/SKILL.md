---
name: customer-outreach
description: Compose professional customer emails from the templates shipped in this skill. Use when drafting welcome emails, follow-ups or security notices.
---

# Customer Outreach

## Workflow

1. Identify the type of email the user needs
2. Pick the closest template from `references/templates/` (all shipped with this skill), or write from scratch if none fits
3. Fill placeholders with user details
4. Show the full draft to the user and send only after they approve it

## Templates

| Template | Use When |
|----------|----------|
| `references/templates/welcome.md` | New customer onboarding |
| `references/templates/security_alert.md` | Password changes, policy updates |

## Guidelines

- Templates are a starting point; adapt them to the user's request
- Security notices never ask customers to click a login link, reply with credentials or install anything; they point to the company's normal account page
