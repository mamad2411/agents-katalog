---
name: runbook-author
description: Write a runbook for on-call so the next person can resolve an alert without paging the author - symptoms, diagnostics, mitigation, escalation. Use when the user asks to write a runbook, document an alert, create an incident playbook, or improve on-call ergonomics.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [runbook, on-call, ops, sre]
---

# Runbook Author

A good runbook answers, at 3 AM, in priority order:
**Is this real? → How bad? → Make it stop. → Tell people. → Investigate.**

A bad runbook tells you what the alert is named.

## When to use

- "Write a runbook for X alert"
- "Document the on-call procedure for Y"
- "Create an incident playbook"
- "Make our alerts actionable"

## Core principle

The reader is **the next on-call**: someone with general competence but **no specific context** about this system. They are tired, possibly woken up, and have one tab open. Write for them.

If a step requires ambient knowledge ("you know how the cache works, right?"), it doesn't belong in a runbook — it belongs *in* the runbook as a link or one-liner.

## Procedure

1. **Anchor to the alert** — what fires, with what threshold, why
2. **Walk the priority order**: confirm → assess severity → mitigate → communicate → diagnose
3. **Make every step executable** — exact commands, exact links
4. **Test it** — have someone else follow it cold
5. **Update after each real incident** where reality diverged from the doc

## Template

```markdown
# Runbook: <alert name>

> **TL;DR:** <one sentence — what's broken when this fires, and what the fastest mitigation is>

**Severity:** SEV-<n> by default (downgrade if symptoms mild)
**Owner team:** @<team>
**Dashboards:** [<dashboard 1>](url) · [<dashboard 2>](url)
**Related:** [<other runbook>](url)

---

## 1. Is this real?

Confirm the alert isn't a fluke before paging anyone.

\`\`\`bash
# Check the current value
<command or query>
# Look at the dashboard
\`\`\`

- If <condition>, it's real. Continue.
- If <condition>, it's a false alarm. <action> and consider tuning the alert.

## 2. How bad?

Quick severity check.

| Signal | SEV-1 | SEV-2 | SEV-3 |
|---|---|---|---|
| <metric> | > X | > Y | > Z |
| <metric> | … | … | … |

Promote/demote the page accordingly. **When in doubt, go higher.** Downgrading costs nothing.

## 3. Stop the bleeding (mitigate)

In order of preference. Try the cheapest first.

### Option A: Flip the feature flag (fastest, ~30 seconds)

\`\`\`bash
# Exact command:
<command>
\`\`\`

Confirms working when: <expected change in metric>

### Option B: Roll back the last deploy (1–3 minutes)

\`\`\`bash
<rollback command>
\`\`\`

Use this if option A doesn't apply or didn't help. Confirms working when: <…>

### Option C: Scale up / restart (3–5 minutes)

\`\`\`bash
<scale command>
\`\`\`

Use this for resource-exhaustion symptoms.

### Option D: <last resort>

<describe>

## 4. Communicate

### If SEV-1 or SEV-2:

\`\`\`
🚨 SEV-<n> declared: <one-line summary>
Incident channel: #incident-<date>
Status page updated: <url>
Updating every 15 min.
\`\`\`

- Update status page: [link to status page template](url)
- Notify in #ops
- If user-facing: get comms lead involved

## 5. Diagnose (after the bleeding stops)

Now investigate cause. Don't do this before mitigation.

### Common causes (top 3 historical)

1. **<cause>** — check via <command>; fix by <…>
2. **<cause>** — check via <command>; fix by <…>
3. **<cause>** — check via <command>; fix by <…>

### Where to look

- **Logs**: <query in your log system>
- **Recent deploys**: <command>
- **Recent config changes**: <command>
- **Dependency health**: <link to vendor status pages>

## 6. Resolve and follow up

- Confirm metrics back to baseline for ≥ 15 minutes
- Update incident channel: `[Resolved] <summary>`
- Update status page
- Open a postmortem doc (link to template)
- File follow-up tickets for prevention

## Escalation

- L1 (on-call): you
- L2: @<senior on-call> after 15 min if not mitigating
- L3: @<service owner> after 30 min OR if data integrity / customer-facing data loss
- External: <vendor support contact> for <dependency>

## Known false positives

- <condition> — usually means <…>; not pageable
- <condition> — see issue #<n>

## Related runbooks

- [<related>](url)
- [<related>](url)

---

**Last verified:** YYYY-MM-DD by @<name> (mark when you ran through it end-to-end)
**Last incident using this runbook:** YYYY-MM-DD ([postmortem](url))
```

## Writing principles

### Be specific

```markdown
❌ "Check the database"
✅ "Run: `psql -h prod-db.internal -c 'SELECT count(*) FROM orders WHERE status=\"pending\" AND created_at > now() - interval \"1 hour\"'`. If > 1000, the worker is stuck."
```

### Lead with the verb

Every step should start with what to *do*, not what to *know*.

```markdown
❌ "There's a queue here that buffers messages…"
✅ "Drain the queue: `<command>`. Watch the depth fall in [dashboard](url)."
```

### Show expected output

```markdown
✅ "Run: `kubectl get pods -n payments`
   Expected: 3 pods, all `Running`.
   If any are `CrashLoopBackOff`, see [pod crash runbook](url)."
```

### Anchor with a screenshot or query

A query that exhibits the symptom is worth a paragraph of description. Embed it.

### Time-box each step

"Try X for 5 minutes; if it doesn't help, escalate" beats "Try X" with no exit criterion.

### Link, don't quote

Other runbooks, docs, dashboards: link. Don't paste — the copy will drift.

## Common runbook gaps

When auditing existing runbooks:

- [ ] No "is this real" step — readers act on noise
- [ ] No severity guidance — readers under-page or over-page
- [ ] Mitigation buried below diagnosis — readers debug while the site is down
- [ ] No exact commands — readers have to figure them out at 3 AM
- [ ] No expected output — readers don't know if a command worked
- [ ] No escalation path — readers stay heroic too long
- [ ] No "last verified" date — readers don't know if it's stale
- [ ] Dashboards linked but inaccessible to on-call (perms!)

## Output format

When writing a runbook from scratch, follow the template.

When auditing existing runbooks:

```markdown
## Runbook audit: <alert / runbook name>

**Last verified:** <date>
**Walkthrough by:** @<name>, <date>

### Strengths
- ✅ <what works>

### Gaps
- 🔴 <blocks on-call from resolving>
- 🟠 <slows resolution significantly>
- 🟡 <polish>

### Specific edits
1. <where, what>
2. …

### Recommendation
APPROVE / NEEDS REWORK
```

## Anti-patterns

- ❌ Runbook that's mostly "context" before the first command
- ❌ "Page <person>" as the mitigation — that's not a runbook, that's a contact card
- ❌ Linking to source code instead of explaining behavior
- ❌ Generic "check logs" without saying *which* logs and *what for*
- ❌ Steps that require access the on-call doesn't have
- ❌ Pasted commands with `<placeholder>` markers, no example value
- ❌ "Restart everything" as the mitigation — too coarse, masks real issues
- ❌ Never tested by anyone but the author
- ❌ Out of date by 6 months
- ❌ Long prose where a numbered list would do

## Tips

- **Game-day exercises**: take a runbook off the shelf and pretend the alert just fired. Time the resolution. Update what broke.
- **New on-call shadows** existing on-call for a week and updates runbooks with everything that wasn't documented.
- **Track which runbooks got used** in each incident — the unused ones might be wrong; the used ones get the most attention.
- **One alert = one runbook**, linked from the alert metadata. No hunting.
- **Aim for one screen**: if it scrolls forever, mitigation got buried.
- **The runbook is a product**: treat changes to it like PRs, with review.

## References

- [Google SRE — Being On-Call](https://sre.google/sre-book/being-on-call/)
- [PagerDuty Runbook Documentation](https://www.pagerduty.com/resources/learn/what-is-a-runbook/)
- [Increment magazine — On-call issue](https://increment.com/on-call/) — practical perspectives
