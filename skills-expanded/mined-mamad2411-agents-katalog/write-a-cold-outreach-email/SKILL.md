---
name: write-a-cold-outreach-email
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Draft a compliant cold outreach email that is relevant, concise, and ready for review or sending.

## Preconditions

- A lawful prospect source and permission or lawful basis for outreach.
- The prospect's business role, company, and likely problem.
- Approved messaging, unsubscribe language, and sender identity.

## Steps

1. **Confirm outreach eligibility.** Check consent, opt-out status, geography, suppression lists, and account ownership. → *Expect:* the prospect is allowed to receive outreach.
2. **Identify one relevant reason.** Use a business trigger, role responsibility, company initiative, or known pain point. → *Expect:* the email has a specific reason for contacting this person.
3. **Write the subject line.** Keep it short, accurate, and non-deceptive. → *Expect:* the subject matches the body and sender.
4. **Draft the opening.** Name the relevant reason in one sentence without exaggerated familiarity. → *Expect:* the first line could not be sent unchanged to every prospect.
5. **State the value and proof.** Explain one business outcome and include a credible proof point if approved. → *Expect:* the recipient can understand why the message matters.
6. **Ask for one action.** Request a brief reply, meeting, referral to the right owner, or permission to send more detail. → *Expect:* the call to action is simple.
7. **Add compliance elements.** Include sender identity, company, physical mailing address or approved footer, and opt-out language where required. → *Expect:* the email meets policy and legal footer requirements.
8. **Save or send through the CRM.** [BRANCH: Salesforce | HubSpot | generic] use Salesforce email composer or sequence; use HubSpot email or sequence; in another CRM, use the approved outreach tool. → *Expect:* the draft or sent email is logged to the contact.

## Decision points

- If the prospect opted out → do not send and update the suppression status if needed.
- If the message references customer names or metrics → use only approved public or permissioned proof.
- If the recipient is in the EU or UK → confirm GDPR lawful basis and local policy before sending.

## Failure modes & recovery

- **F1 Compliance missing:** detect no opt-out, sender identity, or required footer → add approved compliance text before sending.
- **F2 Generic message:** detect no prospect-specific reason → add a role, company, or trigger-based opening.
- **F3 Wrong owner:** detect an account owner or active opportunity → route the draft to the owner instead of sending.

## Verification

The outreach email has a lawful recipient, accurate subject, relevant opening, clear value, single call to action, required compliance footer, and CRM log.

## Variations

- Executive outreach: use fewer details and a sharper business outcome.
- Referral ask: ask for the right owner instead of a meeting.
- Event follow-up: mention the event source and any permission captured there.

## Safety & privacy

Medium compliance risk. Follow CAN-SPAM, GDPR, opt-out, consent, sender identity, truthful subject line, and company frequency rules; never use scraped private data or misleading personalization.
