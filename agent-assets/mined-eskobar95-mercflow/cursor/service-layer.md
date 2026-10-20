---
description: Service layer and backend module patterns for MercFlow. Apply when writing service methods, API routes, or Medusa module code.
globs: ["packages/*/src/modules/**/*", "packages/*/src/api/**/*", "packages/*/src/integrations/**/*"]
alwaysApply: false
---

# Service Layer Rules

MercFlow backend modules follow a strict pattern: **DML model → service factory → API route → Zod validation**. Never skip a layer or combine them.

---

## Module file structure

Every Medusa module must follow this layout:

```
src/modules/<module-name>/
├── models/
│   ├── <entity>.ts          ← DML model definition only — no logic
│   └── index.ts             ← re-export all models
├── migrations/
│   └── Migration<timestamp>_<description>.ts
├── service.ts               ← service factory — ALL business logic lives here
├── types.ts                 ← TypeScript types for service inputs/outputs
├── http-schemas.ts          ← Zod schemas for API validation
├── index.ts                 ← module export (MedusaModule.define)
└── locale-maps.ts           ← (if module supports i18n)

src/api/
└── admin/
    └── <resource>/
        └── [id]/
            └── route.ts     ← thin route handler — calls service, returns response
```

**Rule:** Models have no methods. Services have all logic. Routes have no logic — they validate input (Zod), call service, return response.

---

## Service rules

### Small, focused methods

Each service method does exactly one thing. Name it after what it does.

```ts
// ❌ Too large — does multiple things
async upsertProductContent(productId: string, data: any) {
  // validates, fetches, creates or updates, sends event...
}

// ✅ Focused — each method is independently callable and testable
async getProductContent(productId: string): Promise<ProductContent | null>
async createProductContent(data: CreateProductContentInput): Promise<ProductContent>
async updateProductContent(id: string, data: UpdateProductContentInput): Promise<ProductContent>
async deleteProductContent(id: string): Promise<void>
```

### Use service factory — never raw MikroORM

```ts
// ❌ Wrong — raw repository access
const repo = this.manager_.getRepository(ProductContent)
const content = await repo.findOne({ where: { product_id: productId } })

// ✅ Correct — service factory generated methods
const [content] = await this.listProductContents({ product_id: productId }, { take: 1 })
```

Service factory provides these generated methods automatically:
- `listX(filters, config)` — list with filters
- `retrieveX(id, config)` — single by ID, throws if not found
- `createX(data)` — create one
- `updateX(id, data)` — update one
- `deleteX(id)` — soft delete
- `softDeleteX(id)` — explicit soft delete

### Input types — always explicit

```ts
// types.ts
export type CreateProductContentInput = {
  product_id: string
  description_rich?: Record<string, unknown> | null
  seo_title?: string | null
  seo_description?: string | null
}

export type UpdateProductContentInput = Partial<Omit<CreateProductContentInput, "product_id">>
```

Never accept `any` or raw `Record<string, unknown>` as a service input — always define the type.

### Validation belongs in the service, not the route

```ts
// ✅ Service validates business rules
async updateProductContent(id: string, data: UpdateProductContentInput) {
  if (data.seo_description && data.seo_description.length > 160) {
    throw new MedusaError(MedusaError.Types.INVALID_DATA, "seo_description exceeds 160 characters")
  }
  return this.updateProductContents([{ id, ...data }])
}
```

Routes validate *shape* (Zod). Services validate *business rules* (MedusaError).

---

## API route rules

### Route files are thin — 3 responsibilities only

1. Parse and validate request body/params with Zod
2. Call one service method
3. Return the response in MercFlow shape

```ts
// ✅ Correct route handler
export const POST = async (req: MedusaRequest, res: MedusaResponse) => {
  const body = UpdateProductContentSchema.parse(await req.json())
  const service = req.scope.resolve<ContentModuleService>(CONTENT_MODULE)
  const content = await service.upsertProductContent(req.params.id, body)
  res.json({ data: content })
}
```

```ts
// ❌ Wrong — business logic in route
export const POST = async (req, res) => {
  const body = await req.json()
  if (!body.product_id) return res.status(400).json({ error: "missing product_id" })
  const existing = await db.query("SELECT * FROM product_content WHERE...")
  // ... 40 more lines of business logic
}
```

### Response shapes — always consistent

```ts
// Single resource
res.json({ data: content })

// List
res.json({ data: contents, count, limit, offset })

// Error (use MedusaError — framework handles the HTTP status)
throw new MedusaError(MedusaError.Types.NOT_FOUND, "Product content not found")
```

### Zod validation — always before field access

```ts
// http-schemas.ts
export const UpdateProductContentSchema = z.object({
  description_rich: z.record(z.unknown()).nullable().optional(),
  seo_title: z.string().max(255).nullable().optional(),
  seo_description: z.string().max(160).nullable().optional(),
})

// route.ts
const body = UpdateProductContentSchema.parse(await req.json())
// Only now access body.seo_title — it is guaranteed to be valid
```

---

## Modularisation rules

### File size limits

| File type | Soft limit | Hard limit | Action when exceeded |
|---|---|---|---|
| Service file | 200 lines | 300 lines | Split into focused sub-services |
| Route file | 50 lines | 80 lines | Extract helpers to utils file |
| Component | 150 lines | 250 lines | Extract sub-components |
| Hook | 80 lines | 120 lines | Split into focused hooks |

### When to split a service

Split when a service handles more than one domain concept:

```
❌ content-service.ts (handles products, categories, pages, blog posts — 400 lines)

✅ product-content-service.ts  (product content only)
✅ category-content-service.ts (category content only)
```

Each service is registered separately in the module's `index.ts`.

---

## Scope discipline

The implementation agent works within one vertical slice. It must not:

- Modify files outside the packages listed in the task's "Layers in scope"
- Refactor unrelated code "while it's there"
- Change API contracts of existing endpoints (except if the task explicitly requires it)
- Add dependencies to packages that are not in scope

If a needed change is outside scope: add a code comment `// TODO: [task-title] - [brief description]` and continue. Do not implement it. Report it in the Notion task comment after pushing.
