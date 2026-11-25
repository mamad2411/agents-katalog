---
name: payload
description: Use when working with Payload CMS projects (payload.config.ts, collections, fields, hooks, access control, Payload API). Use when debugging validation errors, security issues, relationship queries, transactions, or hook behavior.
---

# Payload CMS Application Development

Payload is a Next.js native CMS with TypeScript-first architecture, providing admin panel, database management, REST/GraphQL APIs, authentication, and file storage.

## Quick Reference

| Task                     | Solution                                  | Details                                                                                                                          |
| ------------------------ | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Auto-generate slugs      | `slugField()`                             | [FIELDS.md#slug-field-helper](references/FIELDS.md#slug-field-helper)                                                             |
| Restrict content by user | Access control with query                 | [ACCESS-CONTROL.md#row-level-security-with-complex-queries](references/ACCESS-CONTROL.md#row-level-security-with-complex-queries) |
| Local API user ops       | `user` + `overrideAccess: false`          | [QUERIES.md#access-control-in-local-api](references/QUERIES.md#access-control-in-local-api)                                       |
| Draft/publish workflow   | `versions: { drafts: true }`              | [COLLECTIONS.md#versioning--drafts](references/COLLECTIONS.md#versioning--drafts)                                                 |
| Computed fields          | `virtual: true` with afterRead            | [FIELDS.md#virtual-fields](references/FIELDS.md#virtual-fields)                                                                   |
| Conditional fields       | `admin.condition`                         | [FIELDS.md#conditional-fields](references/FIELDS.md#conditional-fields)                                                           |
| Custom field validation  | `validate` function                       | [FIELDS.md#validation](references/FIELDS.md#validation)                                                                           |
| Filter relationship list | `filterOptions` on field                  | [FIELDS.md#relationship](references/FIELDS.md#relationship)                                                                       |
| Select specific fields   | `select` parameter                        | [QUERIES.md#field-selection](references/QUERIES.md#field-selection)                                                               |
| Auto-set author/dates    | beforeChange hook                         | [HOOKS.md#collection-hooks](references/HOOKS.md#collection-hooks)                                                                 |
| Prevent hook loops       | `req.context` check                       | [HOOKS.md#context](references/HOOKS.md#context)                                                                                   |
| Cascading deletes        | beforeDelete hook                         | [HOOKS.md#collection-hooks](references/HOOKS.md#collection-hooks)                                                                 |
| Geospatial queries       | `point` field with `near`/`within`        | [FIELDS.md#point-geolocation](references/FIELDS.md#point-geolocation)                                                             |
| Reverse relationships    | `join` field type                         | [FIELDS.md#join-fields](references/FIELDS.md#join-fields)                                                                         |
| Next.js revalidation     | Context control in afterChange            | [HOOKS.md#nextjs-revalidation-with-context-control](references/HOOKS.md#nextjs-revalidation-with-context-control)                 |
| Query by relationship    | Nested property syntax                    | [QUERIES.md#nested-properties](references/QUERIES.md#nested-properties)                                                           |
| Complex queries          | AND/OR logic                              | [QUERIES.md#andor-logic](references/QUERIES.md#andor-logic)                                                                       |
| Transactions             | Pass `req` to operations                  | [ADAPTERS.md#threading-req-through-operations](references/ADAPTERS.md#threading-req-through-operations)                           |
| Background jobs          | Jobs queue with tasks                     | [ADVANCED.md#jobs-queue](references/ADVANCED.md#jobs-queue)                                                                       |
| Custom API routes        | Collection custom endpoints               | [ADVANCED.md#custom-endpoints](references/ADVANCED.md#custom-endpoints)                                                           |
| Cloud storage            | Storage adapter plugins                   | [ADAPTERS.md#storage-adapters](references/ADAPTERS.md#storage-adapters)                                                           |
| Multi-language           | `localization` config + `localized: true` | [ADVANCED.md#localization](references/ADVANCED.md#localization)                                                                   |
| Create plugin            | `(options) => (config) => Config`         | [PLUGIN-DEVELOPMENT.md#plugin-architecture](references/PLUGIN-DEVELOPMENT.md#plugin-architecture)                                 |
| Plugin package setup     | Package structure with SWC                | [PLUGIN-DEVELOPMENT.md#plugin-package-structure](references/PLUGIN-DEVELOPMENT.md#plugin-package-structure)                       |
| Add fields to collection | Map collections, spread fields            | [PLUGIN-DEVELOPMENT.md#adding-fields-to-collections](references/PLUGIN-DEVELOPMENT.md#adding-fields-to-collections)               |
| Plugin hooks             | Preserve existing hooks in array          | [PLUGIN-DEVELOPMENT.md#adding-hooks](references/PLUGIN-DEVELOPMENT.md#adding-hooks)                                               |
| Check field type         | Type guard functions                      | [FIELD-TYPE-GUARDS.md](references/FIELD-TYPE-GUARDS.md)                                                                           |

## Quick Start

```bash
npx create-payload-app@latest my-app
cd my-app
pnpm dev
```

### Minimal Config

```ts
import { buildConfig } from 'payload'
import { mongooseAdapter } from '@payloadcms/db-mongodb'
import { lexicalEditor } from '@payloadcms/richtext-lexical'
import path from 'path'
import { fileURLToPath } from 'url'

const filename = fileURLToPath(import.meta.url)
const dirname = path.dirname(filename)

export default buildConfig({
  admin: {
    user: 'users',
    importMap: {
      baseDir: path.resolve(dirname),
    },
  },
  collections: [Users, Media],
  editor: lexicalEditor(),
  secret: process.env.PAYLOAD_SECRET,
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  db: mongooseAdapter({
    url: process.env.DATABASE_URL,
  }),
})
```

## Essential Patterns

For essential patterns (Basic Collection, Common Fields, Hook Examples, Access Control, Queries), see [PATTERNS.md](references/PATTERNS.md).

## Security Pitfalls

For critical security pitfalls (Local API bypass, Transaction failures, Hook loops), see [SECURITY-AND-GOTCHAS.md](references/SECURITY-AND-GOTCHAS.md).

## Project Structure

```txt
src/
├── app/
│   ├── (frontend)/
│   │   └── page.tsx
│   └── (payload)/
│       └── admin/[[...segments]]/page.tsx
├── collections/
│   ├── Posts.ts
│   ├── Media.ts
│   └── Users.ts
├── globals/
│   └── Header.ts
├── components/
│   └── CustomField.tsx
├── hooks/
│   └── slugify.ts
└── payload.config.ts
```

## Type Generation

```ts
// payload.config.ts
export default buildConfig({
  typescript: {
    outputFile: path.resolve(dirname, 'payload-types.ts'),
  },
  // ...
})

// Usage
import type { Post, User } from '@/payload-types'
```

## Best Practices & Gotchas

For common gotchas, security best practices, performance tips, and data integrity rules, see [SECURITY-AND-GOTCHAS.md](references/SECURITY-AND-GOTCHAS.md).

## Reference Documentation

- **[FIELDS.md](references/FIELDS.md)** - All field types, validation, admin options
- **[FIELD-TYPE-GUARDS.md](references/FIELD-TYPE-GUARDS.md)** - Type guards for runtime field type checking and narrowing
- **[COLLECTIONS.md](references/COLLECTIONS.md)** - Collection configs, auth, upload, drafts, live preview
- **[HOOKS.md](references/HOOKS.md)** - Collection hooks, field hooks, context patterns
- **[ACCESS-CONTROL.md](references/ACCESS-CONTROL.md)** - Collection, field, global access control, RBAC, multi-tenant
- **[ACCESS-CONTROL-ADVANCED.md](references/ACCESS-CONTROL-ADVANCED.md)** - Context-aware, time-based, subscription-based access, factory functions, templates
- **[QUERIES.md](references/QUERIES.md)** - Query operators, Local/REST/GraphQL APIs
- **[ENDPOINTS.md](references/ENDPOINTS.md)** - Custom API endpoints: authentication, helpers, request/response patterns
- **[ADAPTERS.md](references/ADAPTERS.md)** - Database, storage, email adapters, transactions
- **[ADVANCED.md](references/ADVANCED.md)** - Authentication, jobs, endpoints, components, plugins, localization
- **[PLUGIN-DEVELOPMENT.md](references/PLUGIN-DEVELOPMENT.md)** - Plugin architecture, monorepo structure, patterns, best practices

## Resources

- llms-full.txt: <https://payloadcms.com/llms-full.txt>
- Docs: <https://payloadcms.com/docs>
- GitHub: <https://github.com/payloadcms/payload>
- Examples: <https://github.com/payloadcms/payload/tree/main/examples>
- Templates: <https://github.com/payloadcms/payload/tree/main/templates>
