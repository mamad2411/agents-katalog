---
name: ecosystem-research
description: Research community usage patterns, real-world gotchas, and client compatibility for a specific known library, tool, or protocol feature. Use when a technical-researcher orchestrator needs community-sourced evidence about a named library or feature — bug reports, workarounds, compatibility gaps, and patterns from issue trackers and discussions. Distinct from the broad ecosystem-researcher agent — this skill targets a KNOWN entity and mines what real users have actually experienced, not what exists in a domain.
---

# Ecosystem Research

## Scope

Research target received from orchestrator:

$ARGUMENTS

Confirm the library/protocol/feature and the specific behavior or compatibility concern
before proceeding. If either is absent or ambiguous, state the gap and stop.

## Step 1 — GitHub Issues and Discussions

Search the primary repository's issue tracker and discussion board for real-world reports.

Search terms to apply (adapt to the library name and feature):

- `"doesn't work with"`, `"not supported"`, `"not compatible"`
- `"workaround for"`, `"gotcha"`, `"unexpected behavior"`
- `"error"` + feature name
- Changelog entries referencing the feature (look for `fix:`, `breaking:` prefixes)

For each finding: record the issue or discussion URL, a one-sentence summary of the report, and whether it was resolved.

## Step 2 — Client / Host Compatibility

Identify which clients, hosts, or consumers support this feature.

Look for:

- Explicit support statements in official docs (cite URL + access date)
- Issue reports naming specific clients as broken, partial, or missing
- Test matrices or compatibility tables in the repository

Record per-client status as one of: `supported`, `partial`, `unsupported`, `unknown`. Every status requires an evidence source — do not infer.

## Step 3 — Community Patterns

Identify what approaches the community has converged on.

Look for:

- Repeated workarounds appearing across multiple issues or threads
- Alternative implementations recommended by maintainers or frequent contributors
- Patterns that replaced a broken original approach (check changelogs for deprecation notices)

Cite each pattern with at least one source URL. Do not describe a pattern as "common" without at least two independent sources.

## Step 4 — Real-World Gotchas

Identify what surprised users — content that is NOT in official docs but IS in issue threads, discussions, blog posts, or changelogs.

Signals to look for:

- Maintainer corrections to user assumptions in issue comments
- Changelog entries for unexpected behavioral changes (not just new features)
- Documentation PRs that added a warning section — the warning was added because someone was burned

Every gotcha requires a source. Gotchas derived from training data are not acceptable — they must come from a retrievable URL.

## Step 5 — Alternatives

Identify community-preferred alternatives to broken or missing features.

Look for:

- Issues closed as "use X instead"
- Discussion threads converging on a replacement approach
- README sections recommending alternatives

For each alternative: state what problem it solves, why the original approach was insufficient, and cite the source.

## Output Format

Return a structured report in exactly this format:

```
## Ecosystem Research — {technology/feature} — {date}

### Community Usage Patterns
[patterns with source URLs — one bullet per pattern, each with at least one URL]

### Client / Host Compatibility
[per-client status: supported / partial / unsupported / unknown — with evidence source for each entry]

### Real-World Gotchas (sourced)
[each item with source — issue URL, discussion link, blog post URL, or changelog entry]

### Alternatives
[community-preferred alternatives to broken or missing features — with evidence]

### Gaps
[explicit list of what was searched for but not found — include search terms used and locations searched]
```

Every section must appear even if empty. For empty sections, write "None found after searching [locations]."

## Constraints

- Every claim requires a source: issue URL, discussion URL, docs URL with access date, or changelog entry. Claims without sources are findings gaps, not findings.
- Do NOT rely on training data for version-specific facts, bug reports, or compatibility claims. Training data reflects a past snapshot; issue trackers are current.
- Do NOT write to any backlog item. Return all content to the caller.
- Do NOT broaden scope to domain discovery. If the caller asks about a specific library, research that library — do not survey alternatives unless Step 5 applies.
- Rate limit transparency: if a search endpoint returns fewer results than expected, or blocks entirely, note it in the Gaps section and report what was searched before the limit was reached.
