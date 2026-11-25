---
name: kb-article
description: Drafts knowledge base articles from resolved tickets, common questions, or known-issue patterns — turns one-off resolutions into reusable self-service content. Make sure to use this skill whenever the user says document this for the KB, write a knowledge base article, this should be a help center post, the same question keeps coming up so let's write an article, document this resolution, publish a workaround article, or describes wanting to convert a support resolution into reusable customer-facing content. Optimized for searchability, scannability, and self-service success. Do NOT use for: drafting a response to one specific customer (use customer-support:draft-response), internal documentation/runbooks (use runbook), marketing blog content (use marketing:draft-content), or product release notes (handle directly). Defining characteristic: "customer-facing self-service content, evergreen, optimized for search and scan."
---

# KB Article

Drafts customer-facing knowledge base articles from support resolutions and recurring questions.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Output is customer-facing self-service content | Replying to one customer specifically → `customer-support:draft-response` |
| Content will be evergreen / reused | Internal procedure documentation → `runbook` |
| Optimized for search and scan | Marketing blog content → `marketing:draft-content` |
| Help center / docs / KB destination | Product release notes → handle directly |

## When to actually write a KB article

Not every resolved ticket deserves an article. The criteria:

1. **Frequency:** Same question has come in 3+ times (or projected to)
2. **Self-service viable:** A reader could resolve this themselves without escalating back
3. **Stable answer:** The fix isn't going to change in the next 30 days
4. **Searchable phrasing exists:** People will search for terms that match the article
5. **Reduces ticket volume:** A successful KB article deflects future tickets

If 3+ of these are true, write the article. If <3, just resolve the ticket and move on.

## KB article anatomy

Every article produced includes ALL of these sections:

```markdown
# [Title — phrased as user's question or task]

> **Quick answer:** [One sentence — what they need to know if they only read this]

## When this happens
[Specific scenario in user language. Symptoms, error messages, conditions. Helps them confirm they're in the right article.]

## Why this happens (optional, if it helps trust)
[Brief root cause — only if helpful. Some articles benefit from "this is how the system works" context. Others don't need it.]

## How to fix it

### Option 1: [Most common fix]
1. [Step one]
2. [Step two]
3. [Step three — verify it worked: "you should now see..."]

### Option 2: [Alternative if Option 1 doesn't work]
[Conditional: "If after Option 1 you still see X, try this..."]
1. ...

## Verify the fix worked
[Specific check — "navigate to X, you should see Y"]

## If this didn't work
[Path to escalation — "contact support with [these details]"]

## Related articles
- [Article 1 link]
- [Article 2 link]

---

**Last updated:** YYYY-MM-DD
**Applies to:** [versions / tiers / regions]
**Article ID:** KB-NNNN
```

## Title patterns that work

KB articles get found via search. Titles must match what users type:

### Pattern: How to [task]
- "How to enable MFA for my account"
- "How to export my data"
- "How to add a team member"

### Pattern: Why is [thing happening]
- "Why is my report empty?"
- "Why am I getting [error code]?"
- "Why did my integration stop working?"

### Pattern: Fix / Resolve [problem]
- "Fix: 'Authentication failed' error on login"
- "Resolve sync delays in [feature]"

### Pattern: [Feature] not working / showing [behavior]
- "Reports not updating in real time"
- "Dashboard showing yesterday's data"

Avoid:
- "Information about [feature]" (nobody searches "information about")
- "Article on [topic]" (nobody searches that)
- Internal jargon in the title (users don't know it)
- All-caps "ERROR" (looks like spam)

## Searchability optimization

### Use the user's words, not yours
If users call it "the dashboard" but internally you call it "the workspace canvas," title with "dashboard." Translate internal jargon to user vocabulary.

### Include error messages verbatim
If the article addresses an error, include the EXACT error text the user will see. Searches frequently start with copy-pasted error strings.

### Synonyms in body
Mention alternative terms once: "Multi-Factor Authentication (MFA, 2FA, two-factor authentication)" — captures all three search variants.

### Question reformulation
Include the question 2-3 ways: in title, in the "When this happens" section, naturally in body. Search engines weight question-form matches.

### Short URL slug
URL: `/kb/mfa-setup` not `/kb/article-id-9847362-multi-factor-authentication-setup-instructions`

## Scannability optimization

Customers don't read KB articles linearly. They scan for the section that applies. Therefore:

- **Bold the action verbs** in numbered steps ("**Click** Settings", "**Enter** your email")
- **Use H2/H3 hierarchy** clearly so the table of contents auto-generates
- **Code blocks for commands** — visually distinct from narrative
- **Screenshots strategically** — only when they materially help (annotated to point at the right thing)
- **Numbered steps for procedures, bullets for options/properties**
- **Callout boxes** for warnings ("⚠ This action can't be undone") and tips ("💡 You can also...")

## Tone

KB tone defaults:

- **Direct, not chatty** — customers in support context want efficiency
- **Active voice** — "Click Save" not "The Save button should be clicked"
- **Imperative for steps** — "Enter your email" not "You should enter your email"
- **Empathetic when issue is frustrating** — one acknowledgment line in articles for confusing UI: "This is in a non-obvious location — we're working on improving discoverability"
- **No hype, no marketing copy** — KB is for help, not selling

## Cybersecurity KB patterns

For security product KB articles, additional patterns:

### "How to [security action]" articles
- Two-step verification setup
- API key rotation
- Session management
- Granular permission configuration

### "Why is [security alert] firing" articles
Help reduce alert fatigue by explaining what triggers each alert type and when to act vs. tune.

### Compliance evidence articles
- "How to download your SOC 2 evidence package"
- "Where to find audit logs for [framework] compliance"
- "Generating your access review report"

### Customer-facing security responsibility articles
- "What we secure and what you secure (shared responsibility model)"
- "Sub-processor list and how to subscribe to changes"
- "Security incident response — what we'll tell you and when"

### Sensitive content guidelines for security KB
- Never publish active vulnerability details before patch
- Never publish customer-specific security incident details
- Always link to security.txt or vulnerability disclosure for reporting
- Always include "if you suspect a breach" emergency contact

## Article lifecycle

Every published article has a maintenance lifecycle:

- **At publish:** Note publish date, applicable versions
- **Quarterly review:** Verify steps still work in current product
- **On product change:** Update or deprecate articles affected by feature changes
- **On metric review:** Articles with low success rate (high "this didn't help" feedback) get rewritten
- **Deprecation:** Outdated articles get a deprecation banner pointing to current article

## Anti-patterns

- **Wall of text** — KB articles must be scannable; structure required
- **Ten options before the most common one** — lead with the fix that works for 80% of cases
- **No verification step** — customers must know whether the fix worked
- **No escalation path** — when the fix doesn't work, customers need a next step
- **Internal jargon** — customer doesn't know your codename for the feature
- **Stale screenshots** — UI changed, article's screenshot didn't, customer is confused
- **Every article is "how to"** — also write "why" and "what" and "when" articles
- **Duplicate articles** — search returns 3 nearly-identical articles, customer doesn't know which to trust
- **Articles that just describe instead of resolve** — the goal is task completion, not encyclopedia entries

## Output

Produces:
1. The KB article in the structure above, ready to publish
2. Suggested URL slug
3. Suggested category / placement in the KB structure
4. Internal "decommission criteria" — what would make this article need an update
5. Tags for findability (5-10 relevant tags)
6. Suggested cross-links to related KB articles
7. If the article addresses a common issue, recommendation to also instrument an in-product help link to it
