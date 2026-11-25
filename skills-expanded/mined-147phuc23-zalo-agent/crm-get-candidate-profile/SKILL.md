# CRM Get Candidate Profile
Description: Load a mocked CRM candidate/customer profile by Zalo external user id.

Use this skill early in the conversation to avoid asking for information that is already known.

Input contract:
- `tenantId`: tenant id.
- `channel`: currently `zalo`.
- `externalUserId`: Zalo user id.

Output contract:
- Candidate profile with name, contact details, skills, experience, preferences, and notes when available.
