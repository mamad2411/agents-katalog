# CRM Update Candidate Profile
Description: Create or update durable CRM candidate profile fields from Zalo chat.

Use this skill when the candidate shares stable profile facts such as name, contact details, location, experience, current title, skills, preferred roles, salary expectation, or availability.

Input contract:
- `tenantId`: tenant id.
- `channel`: currently `zalo`.
- `externalUserId`: Zalo user id.
- `patch`: partial profile fields to update.

Patchable fields:
- `displayName`
- `phone`
- `email`
- `location`
- `yearsOfExperience`
- `currentTitle`
- `skills`
- `preferredRoles`
- `salaryExpectationVnd`
- `availability`

Output contract:
- `profile`: updated candidate profile.
- `created`: whether a missing profile was created.

This skill is for durable CRM facts. Use Gather Requirement for temporary job-search criteria.
