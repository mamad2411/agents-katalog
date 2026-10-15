---
name: kyn-wiki-lint
description: Health-check the user's wiki/vault for broken links, orphan pages, missing raw provenance, duplication, and contradictions — reports findings and suggests fixes, never applies them without confirmation. Works from any session, regardless of the current working directory.
argument-hint: "(optional) scope the check to a specific page or folder"
disable-model-invocation: true
---

**Vault resolution:** `{vault}` below is the write-target vault: the `path:` of the `default:` vault in `~/.almagest/config.yml`, if that file exists and declares one; otherwise `~/vault`. That single lookup is the only thing Kuyen reads from the shared Almagest config — no registry machinery, no vault-name arguments.

1. **Check structure.** Across every page in `{vault}/wiki/concepts/`, `wiki/entities/`, and `wiki/sources/`: verify every `[[wikilink]]`/relative link resolves, every Source page's `raw:` field points to a real file in `.raw/`, and every page appears in `{vault}/wiki/index.md` (and vice versa — no index entry without a matching file). Done when every page has been checked against all three.

2. **Check for contradictions.** Group pages that share a tag, alias, or cross-link, then compare their claims on the shared subject: CONTRADICTION means incompatible facts; CONSISTENT means the pages merely differ in emphasis, scope, or vintage — discard CONSISTENT, it isn't a finding. Done when every group of related pages has been compared.

3. **Check for duplication.** Look for pages that describe the same underlying thing more than once — same `.raw/` file referenced by two Source pages, near-identical titles/slugs, or an entry listed in more than one section of `index.md`. Use judgment on what counts as "the same thing"; don't chase superficial overlap. If a pair also surfaced in step 2 as a contradiction, it's a duplicate, not a contradiction — report it once, here. Done when every Source's `raw:` target, every title/slug, and every index entry has been checked for duplicates.

4. **Report.** Group findings by category (broken links, missing provenance, orphan/missing-index pages, duplication, contradictions); skip empty categories — no "all good" padding. Pair every mechanical finding (broken link, missing raw file) with a one-line suggested fix; pair every duplication finding with a suggested merge (which page stays canonical — the merged content itself is the user's call); flag contradictions with both excerpts side by side and no suggested action. Never apply any of these without explicit confirmation in a separate turn. If the user confirms a fix later in this same conversation, log it in `wiki/meta/log.md` the same way `kyn-wiki-ingest` does — `log.md` is the vault's complete append-only ledger, and an unlogged fix breaks that silently. Done when every finding from steps 1-3 appears exactly once.
