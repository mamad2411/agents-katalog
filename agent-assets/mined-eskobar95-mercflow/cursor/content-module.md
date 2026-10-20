---
description: Rules for working inside packages/content-module. Apply when creating or editing the Medusa content module, migrations, or API routes.
globs: ["packages/content-module/**/*", "apps/backend/src/modules/content/**/*"]
alwaysApply: false
---

# Content Module Rules

## What is the Content Module?

`packages/content-module` is a Medusa v2 custom module that adds native content fields to `Product` and `ProductCategory` entities. It follows Medusa v2's official module architecture exactly — DML for data models, service factory for data management, MikroORM for migrations.

This module is the single source of truth for all content-related field definitions, migrations, services, and API extensions.

---

## Medusa v2 Module Architecture

Medusa v2 uses its own **Data Model Language (DML)** — not raw MikroORM entities. Always use DML (`model.define`) to define data models. Never write raw MikroORM entity classes for data models.

The module follows this structure:

```
src/modules/content/
├── models/
│   ├── product-content.ts       ← DML model definition
│   └── category-content.ts      ← DML model definition
├── migrations/
│   └── Migration<YYYYMMDDHHmm>_<description>.ts
├── service.ts                   ← Extends MedusaService (service factory)
├── index.ts                     ← Module export via Module()
└── README.md
```

**There is no separate repository layer for standard operations.** The service factory generates all basic CRUD methods automatically. A custom repository is only used for complex queries that the service factory cannot handle.

---

## Data Models — DML Syntax

All data models use Medusa's DML. Never use raw MikroORM decorators (`@Entity`, `@Property`, etc.) for data model definitions.

```ts
// ✅ Correct — Medusa v2 DML
import { model } from "@medusajs/framework/utils"

export const ProductContent = model.define("product_content", {
  id: model.id().primaryKey(),
  product_id: model.text(),
  description_rich: model.json().nullable(),
  seo_title: model.text().nullable(),
  seo_description: model.text().nullable(),   // max 160 chars enforced in service
  seo_og_image_id: model.text().nullable(),
  media_gallery: model.array().nullable(),    // ordered array of media IDs
})

// ❌ Wrong — do not use raw MikroORM decorators
@Entity()
export class ProductContent {
  @PrimaryKey()
  id: string
  // ...
}
```

**Note:** `created_at`, `updated_at`, and `deleted_at` are added automatically by Medusa's DML. Never define them manually.

### ProductContent fields

| Field | DML type | Notes |
|---|---|---|
| `id` | `model.id().primaryKey()` | Auto-generated |
| `product_id` | `model.text()` | FK reference to Product |
| `description_rich` | `model.json().nullable()` | TipTap JSON output |
| `seo_title` | `model.text().nullable()` | |
| `seo_description` | `model.text().nullable()` | Max 160 chars, enforced in service |
| `seo_og_image_id` | `model.text().nullable()` | Media file ID |
| `media_gallery` | `model.array().nullable()` | Ordered array of media IDs |

### CategoryContent fields

| Field | DML type | Notes |
|---|---|---|
| `id` | `model.id().primaryKey()` | Auto-generated |
| `category_id` | `model.text()` | FK reference to ProductCategory |
| `description_rich` | `model.json().nullable()` | TipTap JSON output |
| `seo_title` | `model.text().nullable()` | |
| `seo_description` | `model.text().nullable()` | Max 160 chars, enforced in service |
| `seo_og_image_id` | `model.text().nullable()` | Media file ID |
| `banner_image_id` | `model.text().nullable()` | Hero/banner image ID |

**Do not add fields to these models without first updating this rule file.**

---

## Service — Service Factory Pattern

The module service extends `MedusaService` from `@medusajs/framework/utils`. This generates all standard CRUD methods automatically.

```ts
// src/modules/content/service.ts
import { MedusaService } from "@medusajs/framework/utils"
import { MedusaError } from "@medusajs/utils"
import { ProductContent } from "./models/product-content"
import { CategoryContent } from "./models/category-content"

class ContentModuleService extends MedusaService({
  ProductContent,
  CategoryContent,
}) {
  // Generated automatically by service factory:
  // createProductContents, retrieveProductContent, listProductContents,
  // updateProductContents, deleteProductContents, softDeleteProductContents
  // createCategoryContents, retrieveCategoryContent, etc.

  // Add custom methods only for logic the factory cannot handle:
  async upsertProductContent(productId: string, data: UpdateProductContentDTO) {
    if (data.seo_description && data.seo_description.length > 160) {
      throw new MedusaError(
        MedusaError.Types.INVALID_DATA,
        "seo_description must not exceed 160 characters"
      )
    }
    // upsert logic here
  }
}

export default ContentModuleService
```

**Rules:**
- Always extend `MedusaService` — never build a service from scratch
- Custom methods go in the service class, not in a separate repository
- Only use a data model repository for complex query operations that the factory cannot handle
- Business logic (validation, transformation) always lives in the service, never in route handlers

---

## Module Export

Every module must export a definition via `Module()` from `@medusajs/framework/utils`:

```ts
// src/modules/content/index.ts
import { Module } from "@medusajs/framework/utils"
import ContentModuleService from "./service"

export const CONTENT_MODULE = "content"

export default Module(CONTENT_MODULE, {
  service: ContentModuleService,
})
```

The module is then registered in `apps/backend/medusa-config.ts`:

```ts
modules: [
  {
    resolve: "./src/modules/content",
  },
]
```

---

## Migrations

### How Medusa v2 generates migrations

**Never write migration SQL manually from scratch.** Use the Medusa CLI to generate migrations from the DML model definitions:

```bash
# Generate migration for the content module
npx medusa db:generate content

# Run all pending migrations
npx medusa db:migrate

# Revert the last migration
npx medusa db:revert
```

The CLI generates a migration file in `src/modules/content/migrations/` based on the current DML model definitions. The import path for the Migration base class is:

```ts
// Medusa v2.11.0+
import { Migration } from "@medusajs/framework/mikro-orm/migrations"
```

### When to regenerate

Run `db:generate` every time you change a DML model (add a field, change a type, add a relation). Each change produces a new migration file — never edit an existing one.

### Migration file naming

Medusa names migration files by timestamp prefix, ensuring they run in creation order:

```
Migration<YYYYMMDDHHmm>_<description>.ts

Examples:
Migration202504241200_create_product_content.ts
Migration202504241530_add_banner_image_to_category_content.ts
```

### Migration decision log

Add a decision log comment to every migration file immediately after the import:

```ts
import { Migration } from "@medusajs/framework/mikro-orm/migrations"

/**
 * MIGRATION DECISION LOG
 * Reason: Create product_content table — PRD section 3.3
 * Changes:
 *   - New table: product_content
 *   - Fields: id, product_id, description_rich (jsonb), seo_title,
 *             seo_description, seo_og_image_id, media_gallery (array)
 *   - Timestamps: created_at, updated_at, deleted_at (auto)
 * Reversible: Yes — down() drops the table
 * Generated via: npx medusa db:generate content
 */
export class Migration202504241200 extends Migration {
  async up(): Promise<void> {
    // CLI-generated SQL — do not modify
  }

  async down(): Promise<void> {
    // CLI-generated SQL — do not modify
  }
}
```

### Never modify an existing migration

Once a migration is committed, it is immutable. Create a new migration to alter the schema. Never edit the SQL inside an existing migration file.

---

## API Routes

Content fields are exposed via custom Medusa admin API routes. Route files follow Medusa v2's file-based routing under `src/api/admin/`.

```ts
// src/api/admin/products/[id]/content/route.ts
import { MedusaRequest, MedusaResponse } from "@medusajs/framework"
import { z } from "zod"
import { CONTENT_MODULE } from "../../../../modules/content"
import ContentModuleService from "../../../../modules/content/service"

const UpdateProductContentSchema = z.object({
  description_rich: z.record(z.unknown()).optional(),
  seo_title: z.string().max(255).optional(),
  seo_description: z.string().max(160).optional(),
  seo_og_image_id: z.string().nullable().optional(),
  media_gallery: z.array(z.string()).optional(),
})

export const GET = async (req: MedusaRequest, res: MedusaResponse) => {
  const contentService: ContentModuleService = req.scope.resolve(CONTENT_MODULE)
  const content = await contentService.listProductContents({
    product_id: req.params.id,
  })
  res.json({ content: content[0] ?? null })
}

export const POST = async (req: MedusaRequest, res: MedusaResponse) => {
  const validated = UpdateProductContentSchema.parse(req.body)
  const contentService: ContentModuleService = req.scope.resolve(CONTENT_MODULE)
  const content = await contentService.upsertProductContent(req.params.id, validated)
  res.json({ content })
}
```

**Route paths — do not change without updating this file:**

```
GET    /admin/products/:id/content
POST   /admin/products/:id/content
GET    /admin/product-categories/:id/content
POST   /admin/product-categories/:id/content
```

**Always use Zod for request validation.** Never access `req.body` fields without validating them first. Note: Medusa v2.14.0+ uses Zod v4 — use the v4 API.

---

## i18n

Locale-aware content fields store translations as a map keyed by locale code, stored as `jsonb`:

```ts
// Stored in the database
description_rich: {
  "en": { type: "doc", content: [...] },
  "da": { type: "doc", content: [...] }
}

seo_title: {
  "en": "English SEO title",
  "da": "Dansk SEO titel"
}
```

The active locale is passed as a query parameter. The service reads and writes only the specified locale:

```
GET  /admin/products/:id/content?locale=da
POST /admin/products/:id/content?locale=da
```

If no locale is specified, the API defaults to `"en"`.
