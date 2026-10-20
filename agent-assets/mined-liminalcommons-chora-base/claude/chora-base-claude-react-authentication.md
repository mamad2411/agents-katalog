# React Authentication (SAP-033) - Claude-Specific Awareness

**SAP ID**: SAP-033
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-033?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Quick setup with production-ready configuration
- 📚 **Time Savings** - 75% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020 (Foundation)

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-033.
s.

---

## Claude Code Authentication Workflows

### Workflow 1: Choosing Authentication Provider

```markdown
User: "Add authentication to my Next.js app"

Claude (Phase 1: Requirements Gathering):
1. Ask clarifying questions:
   - "Do you need self-hosted auth (full control) or managed service (faster)?"
   - "What's your budget? (Free tier or paid service)"
   - "Do you already use a database provider?"
   - "Need enterprise features (SSO, SAML)?"

Claude (Phase 2: Provider Recommendation):
2. Based on answers, recommend provider:
   - Self-hosted + Free → NextAuth v5
   - Fast setup + Budget → Clerk
   - Supabase database → Supabase Auth
   - Enterprise SSO → Auth0

3. Explain trade-offs:
   - NextAuth: Free, self-hosted, 30 min setup, full control
   - Clerk: $25/mo after free tier, 7 min setup, pre-built UI
   - Supabase: Free 50k MAU, 20 min setup, native RLS
   - Auth0: Enterprise pricing, 30 min setup, advanced features

Result: User makes informed provider choice
```

---

### Workflow 2: Setting Up NextAuth v5

```markdown
User: "Set up NextAuth v5 for my Next.js app"

Claude (Phase 1: Install Dependencies):
1. Bash: npm install next-auth@beta
2. Bash: npm install @auth/prisma-adapter  # If using Prisma

Claude (Phase 2: Create Auth Configuration):
3. Write app/api/auth/[...nextauth]/route.ts
   # Content: NextAuth handler with providers, session strategy

4. Write auth.ts (root)
   # Content: NextAuth configuration, callbacks, pages

Claude (Phase 3: Add Environment Variables):
5. Edit .env.local
   # Add: NEXTAUTH_URL, NEXTAUTH_SECRET, provider credentials

Claude (Phase 4: Protect Routes):
6. Write middleware.ts (root)
   # Content: Protected routes configuration

7. Edit app/dashboard/page.tsx
   # Add: Session check, redirect if unauthenticated

Claude (Phase 5: Test):
8. Bash: npm run dev
9. Navigate to http://localhost:3000/api/auth/signin
10. Verify sign-in flow works

Result: NextAuth v5 fully configured and tested
```

---

### Workflow 3: Setting Up Clerk (Fastest)

```markdown
User: "Set up Clerk authentication"

Claude (Phase 1: Create Clerk Account):
1. Instruct user:
   "Go to https://clerk.com → Sign Up → Create Application"
   "Copy NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY"

Claude (Phase 2: Install and Configure):
2. Bash: npm install @clerk/nextjs
3. Edit .env.local
   # Add: NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY, CLERK_SECRET_KEY

4. Edit app/layout.tsx
   # Wrap with <ClerkProvider>

5. Write middleware.ts
   # Content: Clerk middleware with protected routes

Claude (Phase 3: Add UI Components):
6. Edit app/sign-in/[[...sign-in]]/page.tsx
   # Content: <SignIn /> component

7. Edit app/sign-up/[[...sign-up]]/page.tsx
   # Content: <SignUp /> component

8. Edit app/dashboard/page.tsx
   # Add: User session access with useUser()

Claude (Phase 4: Test):
9. Bash: npm run dev
10. Navigate to /sign-in
11. Verify sign-in flow with pre-built UI

Result: Clerk authentication in 7 minutes (fastest setup)
```

---

## Claude-Specific Tips

### Tip 1: Always Ask About Provider Requirements First

**Pattern**:
```markdown
Claude (before implementation):
"I recommend we choose an authentication provider first. Quick questions:
1. Do you need self-hosted (full control) or managed (faster setup)?
2. What's your budget? (Free tier or paid)
3. Using Supabase/Firebase database?
4. Need enterprise features (SSO, SAML)?"
```

**Why**: Provider choice impacts entire architecture (can't easily switch later)

---

### Tip 2: Use Environment Variables Template

**Pattern**:
```markdown
Claude (when setting up auth):
1. Read .env.example (if exists)
2. Edit .env.local with provider-specific variables
3. Add to .env.example for documentation
4. Remind user: "Add these to production environment variables"
```

**Why**: Prevents hardcoded secrets, ensures production compatibility

---

### Tip 3: Protect Routes with Middleware

**Pattern**:
```markdown
Claude (after auth setup):
1. Write middleware.ts with protected route patterns:
   export const config = {
     matcher: ['/dashboard/:path*', '/api/:path*']
   }
2. Test protected routes: try accessing without login
3. Verify redirect to sign-in page
```

**Why**: Middleware protects all routes with single configuration

---

### Tip 4: Test Before Declaring Complete

**Pattern**:
```markdown
Claude (after setup):
1. Bash: npm run dev
2. Instruct user: "Test these flows:
   - Sign up new account
   - Sign in existing account
   - Access protected route (/dashboard)
   - Sign out
   - Try accessing protected route (should redirect)"
3. Fix any issues found during testing
```

**Why**: Auth failures in production are critical bugs

---

## Common Pitfalls for Claude

### Pitfall 1: Not Asking About Provider First

**Problem**: Claude implements NextAuth when user wanted Clerk (or vice versa)

**Fix**:
```markdown
Claude (at session start):
ALWAYS ask about provider requirements BEFORE writing code
Present decision tree
Get explicit confirmation of provider choice
```

---

### Pitfall 2: Forgetting Environment Variables

**Problem**: Auth setup complete but missing .env.local configuration

**Fix**:
```markdown
Claude (after writing auth code):
ALWAYS edit .env.local with required variables
ALWAYS remind user to add to production environment
ALWAYS check .env.example exists for documentation
```

---

### Pitfall 3: Not Protecting Routes

**Problem**: Auth implemented but all routes publicly accessible

**Fix**:
```markdown
Claude (after auth setup):
ALWAYS create middleware.ts with protected routes
ALWAYS test protection (try accessing without login)
ALWAYS verify redirect behavior
```

---

## Support & Resources

**SAP-033 Documentation**:
- [README.md](README.md) - Complete authentication guide (8-min read)
- [awareness-guide.md](awareness-guide.md) - Generic agent patterns (15-min read)
- [Protocol Spec](protocol-spec.md) - Technical specification (20-min read)
- [Adoption Blueprint](adoption-blueprint.md) - Step-by-step setups for all 4 providers (30-min read)

**Provider Documentation**:
- [NextAuth v5 Docs](https://authjs.dev/) - Official NextAuth documentation
- [Clerk Docs](https://clerk.com/docs) - Official Clerk documentation
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth) - Official Supabase Auth documentation
- [Auth0 Docs](https://auth0.com/docs) - Official Auth0 documentation

**Related SAPs**:
- [SAP-020 (React Foundation)](../react-foundation/) - Next.js 15 baseline
- [SAP-034 (Database Integration)](../react-database-integration/) - Prisma/Drizzle for user storage
- [SAP-041 (Form Validation)](../react-form-validation/) - React Hook Form for sign-up forms

---

## Version History

- **1.0.0** (2025-11-09): Initial CLAUDE.md for SAP-033
  - Claude Code authentication workflows
  - Tool usage patterns (Write, Edit, Bash)
  - Provider selection and setup patterns
  - Common pitfalls and tips
  - 4 complete provider setups

---

**Next Steps**:
1. Read [README.md](README.md) for complete authentication guide
2. Choose provider based on requirements (use decision tree)
3. Follow provider-specific setup in adoption-blueprint.md
4. Test all authentication flows before deployment
5. Add environment variables to production
