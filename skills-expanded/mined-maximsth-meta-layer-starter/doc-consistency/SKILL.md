---
name: doc-consistency
description: Walk the doc-consistency sweep when a session makes a substantive edit to a draft or active planning/spec doc in markdowns/ (decision changed, shared value updated, section restructured), or on explicit /doc-consistency invocation. Not for typo fixes, status flips, or style/voice issues — those belong to mechanical gates.
---

# /doc-consistency

Substance lives in [`markdowns/protocols/doc-consistency.md`](../../../markdowns/protocols/doc-consistency.md).

Steps:

1. **Discriminate kickoff vs iteration** per [`auto-trigger-discriminator.md`](../../../markdowns/protocols/auto-trigger-discriminator.md). Typo fixes, status flips, and style edits exit silently. Explicit `/doc-consistency` invocation bypasses.
2. **State the semantic delta** of the edit — what claim changed, what premise it may invalidate.
3. **Enumerate the sweep set:** all `status: draft` + `status: active` docs; the edited doc itself, in full (sibling sections + summary surfaces — frontmatter `description`, intro, verdict/summary tables); every declared quoter (`quotes:` frontmatter or `<!-- quotes: ... -->` comment) of any changed value.
4. **Read each enumerated doc and check it for dependent claims** — restated values, descriptions of the changed mechanism, premises the change invalidates.
5. **Classify findings** — contradiction / stale-but-harmless / unaffected. Fix contradictions in the same change-set; report anchored `file:line` per [`rubric-shared-anchors.md`](../../../markdowns/protocols/rubric-shared-anchors.md).
6. **Check the handoff + escalation triggers.** If a value moved doc → runtime, verify the value-authority handoff edit landed. If the same doc pair contradicts repeatedly or the sweep set has grown heavy, walk the protocol's escalation path (consolidate first; gate only if consolidation doesn't apply).
