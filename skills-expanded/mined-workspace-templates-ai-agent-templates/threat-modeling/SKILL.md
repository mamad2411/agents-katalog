---
name: threat-modeling
description: Builds a STRIDE threat model for a feature, with data flows, trust boundaries, abuse cases and ranked mitigations tied to real code.
---

# Threat modeling

Model the feature in front of you, not the whole company. Do not change code.

## Steps

1. State the scope in two sentences: what the feature does, what data it touches, and who uses it. List assets worth protecting, such as credentials, personal data, money and admin capability.
2. Draw the data flow in text. Name each actor, process, data store and external service, and each flow between them with its protocol. Read the real code, routes and configuration to fill it in; do not rely on the description alone.
3. Mark trust boundaries: browser to server, server to database, service to third party, tenant to tenant, user role to admin role. Every flow that crosses one is a place to examine.
4. For each crossing, ask the six STRIDE questions. Spoofing: can someone pretend to be another user or service? Tampering: can data be changed in transit or at rest? Repudiation: could an action be denied with no log to show it? Information disclosure: what leaks in errors, logs, URLs or responses? Denial of service: what can be made expensive or unbounded? Elevation of privilege: can a user reach another user's data or an admin function?
5. Write abuse cases from the attacker's view, such as "a logged-in user changes the account ID in the URL to read another tenant's invoices".
6. Rank each threat by likelihood and impact as high, medium or low. Keep only threats that apply here. Ten real ones beat forty generic ones.
7. For each kept threat, name a mitigation, the file or layer where it belongs, and a test or log that would prove it works. Mark existing controls you confirmed in code.

## Rules

- Never invent a vulnerability without a code path or design reason.
- Do not run exploits or touch live systems.
- Mark what you could not see, such as infrastructure outside the repository.

## Report

Scope, assets, the data flow, a table of threats with rank and mitigation, and open questions.
