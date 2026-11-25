# CRM Add Candidate Profile Note
Description: Append a durable note to a mocked CRM candidate profile.

Use this skill when the candidate says something useful for recruiters but it should not overwrite structured profile fields, such as preferences, constraints, context, or follow-up details.

Input contract:
- `tenantId`: tenant id.
- `channel`: currently `zalo`.
- `externalUserId`: Zalo user id.
- `note`: note text to append.
- `source`: optional source label.

Output contract:
- `profile`: updated candidate profile.
- `created`: whether a missing profile was created.
- `note`: appended note metadata.

This skill is for durable CRM notes. Use Save History for auditable conversation records.
