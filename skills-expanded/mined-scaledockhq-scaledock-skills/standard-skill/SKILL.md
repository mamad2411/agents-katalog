---
name: my-spec
description: Start with the spec's searchable name and what the skill does (for example "RFC 9457 Problem Details for HTTP API errors"), because the install picker shows only the first 57 characters. Then name every supported version line and the preview, and say when an agent should use it, with the trigger phrases, identifiers and RFC numbers people search for.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# My spec

One or two sentences on what the specification is, who publishes it, and what the agent produces with this skill.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: {{ROLE}} (for example server or client, producer or consumer, issuer or verifier).
- Target version: My Spec 1.1 (default). My Spec 1.0 is legacy: read it and upgrade from it, never author it. My Spec 2.0 is a preview (posture: track): never emit it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the publishing body's index for a newer revision or version line, and update the pins.

## Invariants

The requirements every implementation must meet, each citing the spec section it comes from.

1. **First requirement** (§ 3.1). Why it matters.
2. **Second requirement** (§ 4). Why it matters.

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy or preview line.
2. **First step.** What to do.
   -> [`references/topic.md`](references/topic.md) (create it in `references/`)
   ✓ What is true when this step is done.
3. **Upgrade** (only when asked). Follow the upgrade section for each step from the source version to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded artifact validates against the target version and behaves the same.

## Verify before done

- [ ] A check that can be confirmed against the spec text, a published schema or an official example.
- [ ] Nothing from a preview line is emitted unless its posture is build.

## Reference index

- **`references/versions.md`**: every version line with its status, which one to use, what changed, upgrade steps and the preview. Load for steps 1 and 3.
- **`references/topic.md`**: what it covers and when to load it.

## Related skills

Install related spec skills by name, for example `npx skills add ScaleDockHQ/scaledock-skills --skill other-spec`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Spec title](https://example.org/spec): status, revision, checked YYYY-MM-DD.
