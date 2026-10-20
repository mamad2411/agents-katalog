---
description: Run Code Quality and Architectural Hygiene Check
globs: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.py", "**/*.go", "src/**/*"]
---
# Code Quality: Architectural Hygiene

<audit_rules>
- You MUST verify that files are organized logically (e.g., separating components, utils, APIs, tests).
- You MUST enforce naming consistency across the codebase (e.g., enforce kebab-case for files, PascalCase for components). Do NOT allow mixed casing in the same directory.
- You MUST detect and flag layer boundary violations (e.g., database queries leaking into route handlers or UI components).
- You MUST flag DRY (Don't Repeat Yourself) violations. Identify identical blocks of code (>10 lines), duplicate imports, or magic values repeated >3 times.
</audit_rules>

<example_good>
```typescript
// src/services/user.service.ts
import { db } from '@/lib/db';

export async function getUser(id: string) {
  return db.user.findUnique({ where: { id } });
}

// src/app/api/users/[id]/route.ts
import { getUser } from '@/services/user.service';

export async function GET(req: Request, { params }: { params: { id: string } }) {
  const user = await getUser(params.id);
  return NextResponse.json(user);
}
```
</example_good>

<example_bad>
```typescript
// src/app/api/users/[id]/route.ts
// BAD: Database layer leaking into route handler
import { db } from '@/lib/db';

export async function GET(req: Request, { params }: { params: { id: string } }) {
  const user = await db.user.findUnique({ where: { id: params.id } });
  return NextResponse.json(user);
}
```
</example_bad>

