<!-- agent-notes: { ctx: "refresh cloud landscape research files", deps: [docs/research/aws-landscape.md, docs/research/azure-landscape.md, docs/research/gcp-landscape.md], state: active, last: "cloud-architect@2026-02-12" } -->
Research and update the cloud service landscape for: $ARGUMENTS

This command refreshes the cloud knowledge files that the cloud specialist agents depend on. Run it when you suspect the landscape has changed — new services, pricing changes, deprecated features, or before a major architecture decision.

**Target cloud:** The argument should be one of `AWS`, `Azure`, or `GCP`. If not specified, ask which cloud to update.

## Landscape Files

| Cloud | File |
|-------|------|
| AWS | `docs/research/aws-landscape.md` |
| Azure | `docs/research/azure-landscape.md` |
| GCP | `docs/research/gcp-landscape.md` |

## Process

### 1. Read the Current Landscape

Read the target cloud's landscape file. Note the "Last updated" date to understand how stale it might be.

### 2. Research Current State

Use `WebSearch` to find:

- **New service launches** since the last update date. Search for "[Cloud] new services [year]", "[Cloud] re:Invent / Build / Next announcements".
- **Significant pricing changes.** Search for "[Cloud] pricing changes [year]".
- **Deprecated or sunset services.** Search for "[Cloud] deprecated services".
- **New regions or availability changes.** Search for "[Cloud] new regions".
- **Changed best practices.** Search for "[Cloud] well-architected updates" or "[Cloud] architecture guidance changes".
- **New enterprise features.** Landing zone updates, new policy types, new networking options.

Focus on changes that would affect the cloud specialist agents' recommendations.

### 3. Validate Findings

For each finding:
- Confirm it's GA (Generally Available), not just announced or in preview.
- Check the pricing page for exact current numbers.
- Verify deprecation timelines.

### 4. Update the Landscape File

Update the target cloud's landscape file:

- **Update tables** with new services, changed pricing, or removed services.
- **Update the "Recent Changes and New Services" section** with dated entries.
- **Update the "Known Enterprise Patterns" section** if best practices have changed.
- **Update the "Last updated" header** with today's date.
- **Don't delete the file structure** — keep the same sections so the agents know where to find things.
- **Update agent-notes** per `docs/methodology/agent-notes.md`.

### 5. Review Impact on Agents

After updating, briefly check whether any agent system prompts in `.claude/agents/` (specifically `cloud-architect.md`, `cloud-costguard.md`, `cloud-netdiag.md`) contain hardcoded recommendations that are now wrong. Flag but don't modify agent prompts — those are structural.

### 6. Summary

Report:
- What changed since the last update.
- Any new services the team should consider.
- Any pricing changes that affect existing architecture decisions.
- Any stale information found in agent prompts (if applicable).
- When to run this command again (suggest a cadence based on how much changed).
