# SAP-034: React Database Integration - Claude-Specific Awareness

**SAP ID**: SAP-034
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-10

---

## 📖 Quick Reference

**New to SAP-034?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Quick setup with production-ready configuration
- 📚 **Time Savings** - 6% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020, SAP-023, SAP-033, SAP-035, SAP-036, SAP-041

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-034.
s.

---

## Claude Code Database Workflows

### Workflow 1: Helping User Choose ORM

```markdown
User: "Add a database to my Next.js app"

Claude (Phase 1: Requirements Gathering):
1. Ask clarifying questions:
   - "Do you need a database admin UI? (Prisma Studio)"
   - "Is performance critical? (real-time, analytics)"
   - "Is your team comfortable with SQL?"
   - "Are you deploying to edge runtime?"

Claude (Phase 2: ORM Recommendation):
2. Based on answers, recommend ORM:
   - Need UI → Prisma (includes Prisma Studio)
   - Performance critical → Drizzle (40% faster, 73% smaller)
   - Team new to SQL → Prisma (abstracts SQL complexity)
   - Edge runtime → Drizzle (optimized for edge)
   - Unsure → Prisma (easier learning curve)

3. Explain trade-offs:
   - Prisma: Better DX, Prisma Studio, easier migrations, larger bundle (300KB)
   - Drizzle: Better performance, SQL transparency, smaller bundle (80KB), steeper learning curve

Result: User makes informed ORM choice
```

---

### Workflow 2: Setting Up Prisma (7 phases)

```markdown
User: "Set up Prisma for my Next.js app"

Claude (Phase 1: Install Dependencies):
1. Bash: npm install -D prisma
2. Bash: npm install @prisma/client
3. Bash: npx prisma init

Claude (Phase 2: Configure Environment):
4. Read .env.local (if exists)
5. Edit .env.local
   # Add: DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

Claude (Phase 3: Define Schema):
6. Write prisma/schema.prisma
   # Content: datasource, generator, models

Claude (Phase 4: Create Database Singleton):
7. Write lib/db.ts
   # Content: Singleton PrismaClient pattern (prevents pool exhaustion)

Claude (Phase 5: Run Migration):
8. Bash: npx prisma migrate dev --name init
9. Bash: npx prisma generate

Claude (Phase 6: Test Query):
10. Write app/test/page.tsx
    # Content: Server Component with prisma.model.findMany()

11. Bash: npm run dev
12. Navigate to http://localhost:3000/test
13. Verify data renders

Claude (Phase 7: Clean Up):
14. Remove test page (if temporary)
15. Confirm: "Prisma successfully configured!"

Result: Prisma fully configured and tested
```

---

### Workflow 3: Setting Up Drizzle (7 phases)

```markdown
User: "Set up Drizzle for my Next.js app"

Claude (Phase 1: Install Dependencies):
1. Bash: npm install drizzle-orm postgres
2. Bash: npm install -D drizzle-kit

Claude (Phase 2: Configure Environment):
3. Read .env.local (if exists)
4. Edit .env.local
   # Add: DATABASE_URL="postgresql://user:password@localhost:5432/mydb"

Claude (Phase 3: Define Schema):
5. Write lib/schema.ts
   # Content: Export tables using pgTable()

6. Write drizzle.config.ts
   # Content: Connection string, schema path, output directory

Claude (Phase 4: Create Database Client):
7. Write lib/db.ts
   # Content: Drizzle client with connection pooling

Claude (Phase 5: Run Migration):
8. Bash: npx drizzle-kit generate
9. Bash: npx drizzle-kit migrate

Claude (Phase 6: Test Query):
10. Write app/test/page.tsx
    # Content: Server Component with db.select().from(table)

11. Bash: npm run dev
12. Navigate to http://localhost:3000/test
13. Verify data renders

Claude (Phase 7: Clean Up):
14. Remove test page (if temporary)
15. Confirm: "Drizzle successfully configured!"

Result: Drizzle fully configured and tested
```

---

### Workflow 4: Creating Type-Safe Server Action

```markdown
User: "Create a Server Action to insert a post"

Claude (Phase 1: Define Zod Schema):
1. Read existing form validation schemas (if using SAP-041)
2. Write lib/validations/post.ts
   # Content: Zod schema for post creation

Claude (Phase 2: Create Server Action - Prisma):
3. Write app/actions/posts.ts
   # Content:
   # - "use server" directive
   # - Import prisma from lib/db
   # - Validate FormData with Zod
   # - prisma.post.create()
   # - revalidatePath("/posts")

Claude (Phase 2: Create Server Action - Drizzle):
3. Write app/actions/posts.ts
   # Content:
   # - "use server" directive
   # - Import db, posts from lib/db, lib/schema
   # - Validate FormData with Zod
   # - db.insert(posts).values().returning()
   # - revalidatePath("/posts")

Claude (Phase 3: Test Server Action):
4. Write simple form component that calls Server Action
5. Bash: npm run dev
6. Test form submission
7. Verify database insert (Prisma Studio or SQL query)

Result: Type-safe Server Action working with database
```

---

## Claude-Specific Tips

### Tip 1: Always Ask About Database First

**Pattern**:
```markdown
Claude (before implementation):
"I recommend we set up the database first. Quick questions:
1. Do you already have a PostgreSQL database? (local, Supabase, Vercel, Neon)
2. Do you need a database admin UI? (Prisma Studio)
3. Is performance critical for your app? (real-time, analytics)
4. Is your team comfortable with SQL?"
```

**Why**: Database choice impacts entire architecture (can't easily switch ORMs later)

---

### Tip 2: Use Database Singleton Pattern

**Pattern**:
```markdown
Claude (when creating lib/db.ts):
1. ALWAYS use singleton pattern for Prisma/Drizzle client
2. Cache instance in globalThis to prevent pool exhaustion
3. Remind user: "This pattern prevents connection issues in Next.js development"
```

**Example (Prisma)**:
```typescript
const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined }
export const prisma = globalForPrisma.prisma ?? new PrismaClient()
if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma
```

**Why**: Next.js hot reload creates multiple client instances without singleton

---

### Tip 3: Always Generate Types After Schema Changes

**Pattern**:
```markdown
Claude (after editing schema):
1. For Prisma:
   - Bash: npx prisma migrate dev --name <descriptive_name>
   - Bash: npx prisma generate
2. For Drizzle:
   - Bash: npx drizzle-kit generate
   - Types auto-infer from lib/schema.ts
3. Remind user: "TypeScript types are now updated!"
```

**Why**: Schema changes don't auto-propagate to TypeScript without regeneration

---

### Tip 4: Test Queries Before Declaring Complete

**Pattern**:
```markdown
Claude (after setup):
1. Create temporary test page (app/test/page.tsx)
2. Write simple Server Component with database query
3. Bash: npm run dev
4. Instruct user: "Navigate to /test to verify database works"
5. If successful, remove test page
6. If failed, debug connection/schema issues
```

**Why**: Database failures in production are critical bugs

---

## Common Pitfalls for Claude

### Pitfall 1: Not Asking About ORM Choice First

**Problem**: Claude implements Prisma when user wanted Drizzle (or vice versa)

**Fix**:
```markdown
Claude (at session start):
ALWAYS ask about ORM preference BEFORE writing code
Present decision criteria (performance, DX, SQL comfort)
Get explicit confirmation of ORM choice
```

---

### Pitfall 2: Forgetting Environment Variables

**Problem**: Database setup complete but missing DATABASE_URL in .env.local

**Fix**:
```markdown
Claude (after database setup):
ALWAYS edit .env.local with DATABASE_URL
ALWAYS remind user to add to production environment
ALWAYS check .env.example exists for documentation
```

---

### Pitfall 3: Not Using Singleton Pattern

**Problem**: Multiple PrismaClient instances created, causing connection pool exhaustion

**Fix**:
```markdown
Claude (when creating lib/db.ts):
ALWAYS use singleton pattern (cache in globalThis)
ALWAYS explain why this pattern is critical
NEVER create PrismaClient/drizzle client without singleton
```

---

### Pitfall 4: Skipping Migration After Schema Changes

**Problem**: Schema updated but migration not run, causing runtime errors

**Fix**:
```markdown
Claude (after editing prisma/schema.prisma or lib/schema.ts):
ALWAYS run migration commands immediately
ALWAYS regenerate types (Prisma only)
ALWAYS verify types updated in IDE
```

---

## Support & Resources

**SAP-034 Documentation**:
- [README.md](README.md) - Complete database integration guide (12-min read)
- [awareness-guide.md](awareness-guide.md) - Generic agent patterns (20-min read)
- [Protocol Spec](protocol-spec.md) - Technical specification (35-min read)
- [Adoption Blueprint](adoption-blueprint.md) - Step-by-step setups for Prisma and Drizzle (25-min read)

**ORM Documentation**:
- [Prisma Docs](https://www.prisma.io/docs) - Official Prisma documentation
- [Drizzle Docs](https://orm.drizzle.team) - Official Drizzle documentation
- [Prisma + Next.js Guide](https://www.prisma.io/docs/guides/database/nextjs) - Prisma Next.js integration
- [Drizzle + Next.js Example](https://orm.drizzle.team/docs/get-started-postgresql#nextjs) - Drizzle Next.js setup

**Related SAPs**:
- [SAP-020 (React Foundation)](../react-foundation/) - Next.js 15 baseline
- [SAP-033 (React Authentication)](../react-authentication/) - User auth for Row-Level Security
- [SAP-041 (React Form Validation)](../react-form-validation/) - Zod schemas for type-safe forms

---

## Version History

- **1.0.0** (2025-11-10): Initial CLAUDE.md for SAP-034
  - Claude Code database workflows
  - Tool usage patterns (Write, Edit, Bash)
  - ORM selection and setup patterns
  - Common pitfalls and tips
  - 4 complete ORM setup workflows

---

**Next Steps**:
1. Read [README.md](README.md) for complete database integration guide
2. Choose ORM based on requirements (use decision tree)
3. Follow ORM-specific setup in adoption-blueprint.md
4. Test database queries before deployment
5. Add DATABASE_URL to production environment
