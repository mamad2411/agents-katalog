---
name: "tech-blogging-patterns"
description: "Writing patterns for technical posts: the developer reading pattern, before and after examples, the specificity standard, headline patterns, the code example quality bar, numbered takeaways, and anti-patterns such as the wall of theory. Use when drafting or editing a technical post."
---

# Tech Blogging Patterns

## The Developer Reading Pattern

Developers do not read technical posts linearly. They scan in this order:
1. Headline (is this relevant to me?)
2. Code blocks (is this real code I can use?)
3. Headers (what does this cover?)
4. First paragraph (what's the point?)
5. Key takeaways / conclusion (is it worth reading fully?)

Design for scanning first, reading second. Put real code within the first 25% of the post.

## The Before/After Pattern

The contrast between a painful approach and an elegant one creates the "aha" moment that makes posts shareable:

```markdown
# Before: the painful way
async function fetchUser(id) {
  try {
    const res = await fetch(`/api/users/${id}`);
    if (!res.ok) throw new Error(`HTTP error: ${res.status}`);
    const data = await res.json();
    return data;
  } catch (err) {
    console.error('Failed to fetch user:', err);
    throw err;
  }
}

# After: using a typed fetch wrapper
const user = await api.users.get(id);  // throws typed errors, no boilerplate
```

Show the before state first -- readers need to recognize their own pain before the solution feels valuable.

## The Specificity Standard

Every claim of improvement needs a measurement:

```
# Bad: vague, untrustworthy
The new approach is significantly faster.

# Good: specific, trustworthy
The new approach reduces p99 response time from 380ms to 65ms
(measured over 24 hours of production traffic, 99th percentile).
```

The specificity elements:
- What metric (p99 latency, throughput, error rate, bundle size)
- What value before and after
- How measured (load test, production, synthetic)
- Conditions (RPS, test duration, environment)

## Headline Patterns for Developer Posts

Searchable headlines follow predictable patterns:

```
"How to [do specific thing] with [specific technology]"
→ "How to Build a Rate Limiter in Go with Redis"

"How We [achieved outcome]: [key insight or approach]"
→ "How We Cut Our Build Time by 70%: Moving from Webpack to esbuild"

"[Technology A] vs. [Technology B]: [specific angle]"
→ "Prisma vs. Drizzle: A Performance Comparison for High-Traffic APIs"

"[N] [specific things] about [topic]"
→ "5 PostgreSQL Features That Replace Complex Application Code"

"Why We [replaced/chose/abandoned] [technology]"
→ "Why We Moved from MongoDB to PostgreSQL (and What We Learned)"
```

What makes a headline work:
- Specific technology names (searchable)
- Concrete outcome or angle (specific enough to filter audience)
- No superlatives ("amazing", "game-changing", "revolutionary")
- Under 70 characters for social preview truncation

## Code Example Quality Bar

Every code block in a post must pass this checklist:
- [ ] Imports are present (never assume)
- [ ] Would actually run (not pseudocode labeled as code)
- [ ] Shows what the output looks like (comment with result)
- [ ] Uses realistic variable names (not `foo`, `bar`, `thing`)
- [ ] Language hint is specified (```typescript, ```bash, ```json)

```markdown
# Bad code example
const result = query(users, filters);
// returns filtered users

# Good code example
import { db } from './db';

const activeUsers = await db
  .select({ id: users.id, name: users.name })
  .from(users)
  .where(eq(users.active, true))
  .limit(10);

console.log(activeUsers);
// [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]
```

## The Numbered Takeaways Pattern

The most shared and bookmarked part of any technical post is the numbered takeaway list. Readers who did not read the whole post will read this. Make each one standalone:

```markdown
# Bad takeaways: too vague
- Use caching
- Monitor your metrics
- Test in production

# Good takeaways: specific and actionable
1. Redis pipeline batching reduces round trips from N to 1 for N operations.
   Use it any time you are executing multiple independent Redis commands.

2. p99 latency is a more honest metric than averages for user-facing performance.
   A 300ms average can hide a 2000ms p99 that affects 1% of users.

3. Profile before optimizing. Our first optimization attempt targeted the wrong bottleneck
   and had no measurable impact.
```

## Anti-Patterns

### The Wall of Theory
Starting with 3 paragraphs of background before any code. Developers will not wait. Code first, explain after.

### The Unnested Prerequisites Lie
Saying "requires basic JavaScript knowledge" when the post uses generators, WeakMaps, and Proxy objects. State the real prerequisites:
```
# Bad
Prerequisites: JavaScript basics

# Good
Prerequisites:
- ES2017 async/await
- Familiarity with HTTP request/response cycle
- Node.js 18+ installed
```

### The One-Sided Comparison
Comparing Tool A to Tool B where the author clearly prefers A and strawmans B. Readers detect this immediately and discount the entire post. Give each tool its best case.

### The Undated Post
Technical content without a date is a trap. Readers cannot know if the APIs are current or if the performance benchmarks still apply. Always include the post date and update date.

### The Marketing Paragraph
```
# Bad
Our team is proud to announce the revolutionary solution that transforms
the developer experience...

# Good
We built [feature] because [specific customer problem].
Here is how it works.
```

## References
- [Technical Blogging by Antonio Cangiano](https://pragprog.com/titles/actb2/)
- [Write the Docs - Community](https://www.writethedocs.org/)
- [Google Technical Writing Courses](https://developers.google.com/tech-writing)
- [Dev.to editor guide](https://dev.to/p/editor_guide)
- [The Documentation System (Diataxis)](https://diataxis.fr/)
