# Twenty — Get candidate profile

Description: Fetch CRM-backed candidate fields from Twenty `Person` records using the custom `externalUserId` field.

When to use:

- Start of conversation or before updating requirements when profile facts might exist in Twenty.

Notes:

- Requires recruiting schema applied (`pnpm --filter @platform/worker twenty:schema`) and optional seed data.
