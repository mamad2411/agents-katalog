---
name: aipref
description: >-
  IETF aipref AI usage preferences: publish and read Content-Usage statements (train-ai, ai-use, search)
  in the HTTP Content-Usage header and the robots.txt Content-Usage rule, following
  draft-ietf-aipref-vocab-08 and draft-ietf-aipref-attach-05 (working group drafts, build posture),
  with upgrades from older labels (tdm, ai, genai, inference, all, bots, train-genai, ai-output) and the
  attach-00 group-level rule. Use when a site, CDN or publisher states whether content may be used for
  AI training, as generative AI input or for search, or when a crawler, AI agent, training pipeline or
  search engine must parse, combine and apply those preferences: Structured Fields Dictionary syntax
  (y and n tokens), unknown outcomes, most-restrictive combining, the search override, path-scoped
  robots.txt rules, caching and limits (not enforcement). Triggers: aipref, AI preferences,
  Content-Usage, AI opt-out, robots.txt AI training, RFC 9309 update, draft-ietf-aipref-vocab,
  draft-ietf-aipref-attach.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# AI Preferences (aipref)

The IETF AI Preferences (aipref) working group defines a vocabulary for stating how content may be used by automated processing systems (`draft-ietf-aipref-vocab`), and how to attach those statements to content served over HTTP with a `Content-Usage` header field and a `Content-Usage` rule in robots.txt (`draft-ietf-aipref-attach`, which updates RFC 9309). With this skill the agent publishes preferences for a site, or parses, combines and applies them in a crawler or AI agent.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. "vocab §" refers to `draft-ietf-aipref-vocab-08` and "attach §" to `draft-ietf-aipref-attach-05`. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Draft posture: **build** for both families. Neither draft is an RFC, and both mark large parts as without working group consensus (vocab "Note to Readers", § 3, § 4). Implement the pinned revisions exactly, and re-check the datatracker before relying on a label.

## Inputs (fill in, or ask before starting)

- Role: publisher (origin, CDN or host that declares preferences), consumer (crawler, AI agent, training or search pipeline that reads them), or both.
- Attachment: the `Content-Usage` header field, the robots.txt `Content-Usage` rule, or both (attach § 1.2).
- Consumer identity: the robots.txt product token the crawler matches groups with (RFC 9309 § 2.2.1).
- Unknown policy (consumer): what the consumer does when a category comes out unknown. The drafts take no position (vocab § 5); record it as the consumer's own policy.
- Target version: two families, each with one current line.
  - Vocabulary: draft-ietf-aipref-vocab-08 (default, posture build: implement it). draft-ietf-aipref-vocab-05 to -07, draft-ietf-aipref-vocab-03 to -04, draft-ietf-aipref-vocab-02 and draft-ietf-aipref-vocab-00 to -01 are legacy: read and upgrade from them, never author them.
  - Attachment: draft-ietf-aipref-attach-05 (default, posture build). draft-ietf-aipref-attach-00 is legacy.
  - No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revisions in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check both datatracker pages for a newer revision, an RFC or a replacement, check the working group page for newly adopted documents, check the IANA field registry for `Content-Usage`, and update the pins.

## Invariants

1. **Three categories, three outcomes.** The vocabulary defines AI Training (`train-ai`), AI Use (`ai-use`) and Search (`search`) (vocab § 4, § 6.1). Each category resolves to allowed, disallowed or unknown; with no statement, everything is unknown (vocab § 3, § 5).
2. **The syntax is a Structured Fields Dictionary** of lowercase keys and the Tokens `y` (allow) or `n` (disallow) (vocab § 6, § 6.2; RFC 9651 § 3.2). Labels are case sensitive (vocab § 6.1).
3. **Anything else is unknown, not an error.** A missing key, a non-Token value (including a bare key, which is Boolean true) or a Token other than `y` or `n` gives unknown (vocab § 6.5). Unknown labels and unknown parameters MUST be ignored (vocab § 6.4). A Dictionary that fails to parse, for example one with an uppercase key, makes every preference unknown (vocab § 6.5.1).
4. **The last duplicate key wins** (vocab § 6.5.1; RFC 9651 § 4.2.2), and only its parameters apply (vocab § 6.5.2).
5. **Combine by most restrictive.** Across statements from different methods or parties, absent another resolution: any disallow gives disallow, else any allow gives allow, else unknown (vocab § 5.1). This also resolves robots.txt rules with identical paths and conflicting preferences (attach § 3.1).
6. **Search overrides the other categories** for a use that meets its conditions: links to the original location, excerpts only to judge relevance, no generated summaries (vocab § 4.3).
7. **`Content-Usage` describes the message content, not the resource.** It is representation metadata and has no special effect on caching (attach § 2).
8. **robots.txt preferences follow crawl permission.** `Content-Usage` rules use the Allow and Disallow longest-match, by bytes of the encoded path, within the group selected for the crawler; disallowed paths carry no preferences, and rule order carries no meaning (attach § 3, § 3.1; RFC 9309 § 2.2.1, § 2.2.2).
9. **Preferences come from the robots.txt current at fetch time** and do not apply retroactively; a cached robots.txt may hide updates for up to 24 hours (attach § 3.1, § 3.3; RFC 9309 § 2.4).
10. **Preferences are not enforcement.** They are not a security mechanism (vocab § 8), the drafts do not say whether or when to follow them (vocab § 3.2), contracts can override them (vocab § 5.2), and their source is unknown unless the method identifies it (vocab § 3.1).
11. **Parse as adversarial input,** following RFC 9651 § 6 and RFC 9110 § 17; robots.txt stays within the 500 KiB parsing limit (attach § 4; RFC 9309 § 2.5).

## Workflow

1. **Pick the versions.** Use draft-ietf-aipref-vocab-08 and draft-ietf-aipref-attach-05. If an existing statement uses labels such as `bots`, `all`, `tdm` or `train-genai`, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ Both target revisions are recorded, and no legacy label is planned for output.
2. **Map the intent to categories** (publisher). Decide `y`, `n` or nothing for `train-ai`, `ai-use` and `search`, knowing what each excludes: non-generative training, user-provided input, summaries (vocab § 4.1 to § 4.3).
   -> [`references/vocabulary.md`](references/vocabulary.md)
   ✓ Every category the declaring party cares about has an explicit value; the rest are deliberately left unknown.
3. **Serialize the statement.** Write a Dictionary such as `train-ai=n, search=y`, with no uppercase, no bare keys and no duplicates (vocab § 6, § 6.5.1).
   -> [`references/vocabulary.md`](references/vocabulary.md)
   ✓ The string parses as an RFC 9651 Dictionary and yields the intended values.
4. **Attach it** (publisher). Send `Content-Usage` on responses, and/or add path-scoped `Content-Usage` rules to the right robots.txt groups (attach § 2, § 3).
   -> [`references/attachment.md`](references/attachment.md)
   ✓ For each sample URL and crawler token, the crawl decision and the preference match the plan (attach § 3.4 table method).
5. **Collect statements** (consumer). Select the robots.txt group for your product token, find the longest-matching `Content-Usage` rule for crawlable paths, and parse every `Content-Usage` header on the response (attach § 3.1, § 3.2; RFC 9651 § 4.2).
   -> [`references/processing.md`](references/processing.md)
   ✓ Each fetched asset has the statements found, with the robots.txt version used.
6. **Resolve and apply** (consumer). Turn each statement into per-category outcomes, combine them most-restrictively, apply the search override for qualifying uses, then apply the unknown policy (vocab § 4.3, § 5, § 5.1).
   -> [`references/processing.md`](references/processing.md)
   ✓ Each use of an asset maps to one category and one recorded outcome.
7. **Review limits and security.** Check parsing limits, untrusted input, caching delays, and that nothing presents preferences as access control (vocab § 8; attach § 4).
   -> [`references/processing.md`](references/processing.md)
   ✓ Access that must be blocked uses robots.txt Disallow or real access control, not `Content-Usage`.
8. **Upgrade** (only when asked). Follow the checklist for the source revision: rename or drop labels, rewrite group-level attach-00 rules as path-scoped rules, and re-check meaning.
   -> [`references/versions.md`](references/versions.md)
   ✓ The new statement parses under vocab-08, and every intent the old one expressed is either kept or listed as not expressible.

## Verify before done

- [ ] Every published value is a Dictionary of lowercase `train-ai`, `ai-use` or `search` keys with `y` or `n` Tokens (vocab § 6.1, § 6.2).
- [ ] No published statement uses a legacy label (`tdm`, `ai`, `genai`, `inference`, `all`, `bots`, `train-genai`, `ai-output`) (see versions).
- [ ] robots.txt `Content-Usage` paths start with `/`, percent-encode SP and HTAB, and sit in the group the target crawler selects (attach § 3.1, § 3.2; RFC 9309 § 2.2.1).
- [ ] The consumer treats parse failures, unknown labels and non-`y`/`n` values as unknown, never as allow (vocab § 6.4, § 6.5).
- [ ] Conflicts resolve most-restrictively, including header versus robots.txt (vocab § 5.1).
- [ ] The consumer's default for unknown is written down as its own policy (vocab § 5).
- [ ] Documentation calls preferences preferences, not access control or enforcement (vocab § 3.2, § 8).

## Reference index

- **`references/versions.md`**: both families, every revision line with its labels, what changed, and upgrade checklists from each legacy line. Load for steps 1 and 8.
- **`references/vocabulary.md`**: the data model, the three categories and their exclusions, the search override, extensions, the Dictionary syntax and parsing edge cases. Load for steps 2 and 3.
- **`references/attachment.md`**: the `Content-Usage` header field, the robots.txt rule ABNF, parsing and path matching, worked examples and publisher mistakes. Load for step 4.
- **`references/processing.md`**: the consumer algorithm end to end, combining, unknown handling, caching, limits, security and known cross-reference errors in the drafts. Load for steps 5 to 7.

## Related skills

- `robots-txt` for RFC 9309 groups, Allow and Disallow matching and fetching: `npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt`.
- `web-bot-auth` for crawlers that prove their identity with signed requests, which aipref does not cover: `npx skills add ScaleDockHQ/scaledock-skills --skill web-bot-auth`.
- `http-semantics` for representation metadata, field combining and caching: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.
- `content-signals` for Cloudflare's `Content-Signal` robots.txt line (search, ai-input, ai-train), a separate vocabulary for similar preferences: `npx skills add ScaleDockHQ/scaledock-skills --skill content-signals`.
- `rsl` for RSL licenses that attach AI usage and payment terms through the robots.txt `License` directive: `npx skills add ScaleDockHQ/scaledock-skills --skill rsl`.
- `tdmrep` for W3C TDM Reservation Protocol text and data mining opt-outs: `npx skills add ScaleDockHQ/scaledock-skills --skill tdmrep`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [draft-ietf-aipref-vocab-08: A Vocabulary For Expressing AI Usage Preferences](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-08.txt): WG draft, intended Proposed Standard, -08 (14 September 2026), checked 2026-10-05.
- [draft-ietf-aipref-vocab datatracker page](https://datatracker.ietf.org/doc/draft-ietf-aipref-vocab/): WG Document, active, latest revision -08, checked 2026-10-05.
- [draft-ietf-aipref-attach-05: Associating AI Usage Preferences with Content in HTTP](https://www.ietf.org/archive/id/draft-ietf-aipref-attach-05.txt): WG draft, intended Proposed Standard, updates RFC 9309 if approved, -05 (19 August 2026), checked 2026-10-05.
- [draft-ietf-aipref-attach datatracker page](https://datatracker.ietf.org/doc/draft-ietf-aipref-attach/): WG Document, active, latest revision -05, checked 2026-10-05.
- [AI Preferences (aipref) working group charter](https://datatracker.ietf.org/wg/aipref/about/): Active, charter-ietf-aipref-01, checked 2026-10-05.
- Legacy vocabulary revisions, for upgrades: [-07](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-07.txt) (19 August 2026), [-05](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-05.txt) (1 December 2025), [-04](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-04.txt) (28 October 2025), [-03](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-03.txt) (5 September 2025), [-02](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-02.txt) (21 July 2025), [-01](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-01.txt) (19 June 2025) and [-00](https://www.ietf.org/archive/id/draft-ietf-aipref-vocab-00.txt) (1 May 2025): WG drafts, superseded, checked 2026-10-05.
- Legacy attachment revisions, for upgrades: [-04](https://www.ietf.org/archive/id/draft-ietf-aipref-attach-04.txt) (28 October 2025) and [-00](https://www.ietf.org/archive/id/draft-ietf-aipref-attach-00.txt) (16 June 2025): WG drafts, superseded, checked 2026-10-05.
- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309): RFC (Proposed Standard), RFC 9309, checked 2026-10-05.
- [RFC 9651: Structured Field Values for HTTP](https://www.rfc-editor.org/rfc/rfc9651): RFC (Proposed Standard), RFC 9651, checked 2026-10-05.
- [IANA HTTP Field Name registry](https://www.iana.org/assignments/http-fields): IANA registry, last updated 2026-08-28, no `Content-Usage` entry yet, checked 2026-10-05.
