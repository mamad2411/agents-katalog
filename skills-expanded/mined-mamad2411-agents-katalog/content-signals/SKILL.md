---
name: content-signals
description: >-
  Content Signals Policy: write and read Content-Signal lines in robots.txt that state whether content
  may be used for search, ai-input and ai-train, following Cloudflare's CC0 Content Signals Policy of
  24 September 2025 as published at contentsignals.org. Use when a site or CDN declares how crawled
  content may be used after access (search index, retrieval-augmented generation and grounding, model
  training or fine-tuning), per user-agent group or per path, with the human-readable policy comment
  block, or when a crawler, AI agent or training pipeline must parse those yes and no values, treat
  missing signals as no preference, and combine them with Allow and Disallow. Covers the three
  signals, the four generator presets, path-scoped signals, how RFC 9309 parsers must tolerate the
  line, and its limits (a preference, not enforcement). Triggers: Content-Signal, content signals,
  contentsignals.org, ai-train=no, ai-input, search=yes, robots.txt AI training opt-out, managed
  robots.txt.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Content Signals

The Content Signals Policy is a robots.txt addition, published by Cloudflare under CC0, that lets a site state how its content may be used after it has been accessed: for search, as AI input, or for AI training. With this skill the agent writes Content-Signal lines and the policy text for a site, or parses and applies them in a crawler or agent.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). "Policy" refers to the Cloudflare announcement and policy text of 24 September 2025; "site" refers to contentsignals.org. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Content Signals is a published vendor policy, not an IETF or W3C standard. The same three definitions are reused by RSL 1.0's usage vocabulary.

## Inputs (fill in, or ask before starting)

- Role: publisher (site or CDN that writes robots.txt), consumer (crawler or AI pipeline that reads it), or both.
- Intent: `yes`, `no` or no statement for each of `search`, `ai-input` and `ai-train`.
- Scope: all crawlers (`User-Agent: *`), named crawlers, and any paths that need different signals.
- Target version: Content Signals Policy 2025 (default). No legacy line or preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check contentsignals.org for new signals or syntax, check whether the policy has moved to a standards body, and update the pins.

## Invariants

1. **Three signals.** `search` (building a search index and returning links and short excerpts, excluding AI-generated search summaries), `ai-input` (inputting content into AI models, such as RAG, grounding or real-time use for generative AI answers) and `ai-train` (training or fine-tuning AI models) (Policy; site).
2. **Values are `yes` or `no`,** comma-delimited after `Content-Signal:` (Policy).
3. **`yes` means the content may be collected for that use; `no` means it may not; a missing signal neither grants nor restricts permission** via content signals (Policy, clauses a to c).
4. **A missing signal does not mean the operator has no preference;** it only means robots.txt does not express one (Policy).
5. **Signals sit in a `User-Agent` group** next to `Allow` and `Disallow`, and may carry a path before the values to scope them (site, Targeting Specific User-Agents, Protect Specific Pages).
6. **The policy text is a comment block** that crawlers ignore; it defines the signals and states that restrictions are express reservations of rights under Article 4 of Directive (EU) 2019/790 (Policy).
7. **Preferences, not countermeasures.** Signals do not stop crawling; Cloudflare advises combining them with WAF rules and bot management, and notes that courts may not treat robots.txt as binding (Policy; site).
8. **Signals govern use after access; `Allow` and `Disallow` govern access.** A disallowed path is not fetched whatever its signals (Policy; RFC 9309 § 2.2.2).

## Workflow

1. **Pick the version.** Use the 2025 policy.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded.
2. **Map the intent** (publisher). Decide each signal, or deliberately leave it out; pick one of the four presets if it fits.
   -> [`references/syntax.md`](references/syntax.md)
   ✓ Every signal the site cares about is explicit, and omissions are deliberate.
3. **Write robots.txt** (publisher). Add the policy comment block, then `Content-Signal` lines in the right groups, with paths where needed, keeping `Allow`/`Disallow` consistent.
   -> [`references/syntax.md`](references/syntax.md)
   ✓ For each sample crawler and path, the selected group yields the intended access and signals.
4. **Parse and apply** (consumer). Select the group by product token, find the signal line for the path, read `yes`/`no` per signal, treat missing as unstated, and never let the line disturb RFC 9309 parsing.
   -> [`references/syntax.md`](references/syntax.md)
   ✓ Each use of fetched content maps to `yes`, `no` or unstated, with the robots.txt version recorded.
5. **Combine with other signals.** Reconcile with aipref `Content-Usage`, RSL licenses and TDMRep where present, and record which one decided.
   -> [`references/syntax.md`](references/syntax.md)
   ✓ Conflicts are resolved by a written rule, not by accident.

## Verify before done

- [ ] Only `search`, `ai-input` and `ai-train` keys appear, each with `yes` or `no` (Policy).
- [ ] Each `Content-Signal` line is inside the `User-Agent` group it should affect (site).
- [ ] The human-readable policy comment block is present when signals are used (Policy).
- [ ] Paths that must not be fetched use `Disallow`, not `ai-train=no` (Policy; RFC 9309).
- [ ] A consumer treats a missing signal as unstated and an unknown key or value as unstated, never as `yes`.
- [ ] Documentation calls signals preferences, not enforcement (Policy).

## Reference index

- **`references/versions.md`**: the single policy line, its relationship to aipref and RSL, and what to watch. Load for step 1.
- **`references/syntax.md`**: the signal definitions, line syntax, presets, path-scoped and group-scoped examples, parsing rules and combining with other signals. Load for steps 2 to 5.

## Related skills

- `robots-txt` for RFC 9309 groups, matching and AI crawler tokens: `npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt`.
- `aipref` for the IETF `Content-Usage` header and robots.txt rule: `npx skills add ScaleDockHQ/scaledock-skills --skill aipref`.
- `rsl` for licensing terms that reuse these three definitions: `npx skills add ScaleDockHQ/scaledock-skills --skill rsl`.
- `tdmrep` for the W3C text and data mining reservation: `npx skills add ScaleDockHQ/scaledock-skills --skill tdmrep`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Giving users choice with Cloudflare's new Content Signals Policy](https://blog.cloudflare.com/content-signals-policy/): Cloudflare announcement and policy text, CC0, 24 September 2025, checked 2026-10-09.
- [Content Signals (contentsignals.org)](https://contentsignals.org/): Cloudflare policy site and generator, unversioned page, checked 2026-10-09.
- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309): RFC (Proposed Standard), RFC 9309, checked 2026-10-09.
