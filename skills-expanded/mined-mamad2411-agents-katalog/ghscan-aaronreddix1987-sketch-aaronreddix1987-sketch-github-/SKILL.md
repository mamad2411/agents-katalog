# Skill: TTI Revenue Watch

## Trigger
Hourly (or on demand).

## Instructions
1. Query the connected Stripe account for charges created in the last 2 hours with status succeeded.
2. For each new charge, match the product metadata to the catalog in thank-you.html and email the buyer the matching Drive download link.
3. If the charge is for the AI Front Desk setup ($497), start the onboarding checklist and text Aaron at 747-301-8586.
4. Check Gmail for replies to outreach; tag any warm lead and draft a follow-up.
5. If Stripe returns a permission or 403 error, stop and email Aaron the reconnect link from the most recent "ACTION NEEDED" email.
6. Never invent sales, clients, testimonials, or approvals. Report only events Stripe or Gmail actually show.
7. Log every action to the TTI Execution Ledger in Google Drive.

## Stop conditions
- Stripe write/read permission missing.
- No verified buyer email on the charge.
- Any regulated, medical, legal, or dispute request — escalate to Aaron.
