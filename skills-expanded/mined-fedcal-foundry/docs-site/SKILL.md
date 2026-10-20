---
name: docs-site
description: Bootstrap or audit a documentation site for an open source project — Diátaxis structure, navigation, search, versioning, translation, ownership and the CI pipeline that fails when docs rot. Use when a project has scattered markdown, a wiki nobody trusts, or a docs site with no owner and no build gates. Produces a plan.v1 with machine-checkable gates, or a review.v1 when auditing. Not for writing page prose and not for generating API reference.
user-invocable: true
argument-hint: "[--audit | --bootstrap] [--path docs/]"
model: sonnet
effort: medium
metadata:
  foundry.vertical: research
  foundry.io: "repository -> plan.v1 | review.v1"
license: Apache-2.0
---

# Bootstrap or audit a documentation site

Two modes, one checklist. `--audit` measures an existing site and emits `review.v1`.
`--bootstrap` designs a new one and emits `plan.v1`. Both use the same twelve checks, because
the definition of a working docs site does not depend on whether it exists yet.

**Firewall:** the full inventory, the navigation tree and the finding list go to
`.foundry/blackboard/<wave>/docs-architect.json`. The reply is **≤ 300 tokens**: artifact path,
the three highest-severity gaps, and blockers.

## When not to use this

- The task is writing or fixing one page → `technical-writer`.
- The task is producing reference documentation from code → `api-reference`.
- The task is a README → `write-readme`; a README is a different artifact with different rules.
- The project has fewer than ~10 documentation pages and one maintainer. A good README plus a
  generated reference beats a site nobody maintains. Say so and stop — recommending
  infrastructure that will be abandoned is a disservice.

## Step 0 — Inventory before opinion

```bash
find docs site content -type f \( -name '*.md' -o -name '*.mdx' -o -name '*.rst' -o -name '*.adoc' \) 2>/dev/null | sort
git log -1 --format='%cs' -- docs/            # how stale is the whole tree
git log --format='%cs' --name-only -- docs/ | head -100   # which pages move at all
wc -l $(find docs -name '*.md' 2>/dev/null) | sort -n | tail -20
```

Then per page record: path, title, quadrant (inferred), last commit date, last author, whether
it appears in navigation, and whether anything links to it. Two derived lists matter most:

- **Orphans** — pages in the tree but not in navigation and not linked. They are still indexed
  by search engines and still wrong.
- **Fossils** — pages untouched for longer than their subject's release cadence.

## The twelve checks

Each check has a measurement, a pass condition and a `finding.v1` severity when it fails.

### 1. Audience coverage — `high`
Every audience named by `docs-architect` has at least one entry point and one page. Measure:
audiences × entry points matrix, no empty row. Pages serving no audience are listed for
deletion, not improvement.

### 2. Quadrant purity — `medium`
Every page belongs to exactly one Diátaxis quadrant (tutorial / how-to / reference /
explanation). Measure: count pages whose headings mix imperative steps with conceptual prose.
Pass: zero mixed pages, or each mixed page has a split proposal. An empty quadrant is a
finding in its own right — a project with no explanation pages answers the same "why" issue
forever.

### 3. Navigation depth and routing — `medium`
Depth ≤ 3 levels. Every section has a landing page whose only job is routing: who it is for,
the three commonest tasks, where to go otherwise. Measure: max nesting in the nav config;
count of sections without a landing page.

### 4. Reference is generated — `critical`
No reference content is hand-maintained. Measure:

```bash
grep -rlE '^\|\s*(`?--?[a-z-]+`?|`[A-Z_]{3,}`)\s*\|' docs/ | sort
```

Hand-written flag tables, option lists, environment-variable tables and endpoint tables are
drift waiting to happen. Pass: every such table is produced by a generator into a gitignored
directory, and CI fails when regenerated output differs from what is committed. Hand this to
`api-reference`.

### 5. Build strictness — `high`
The site builds from a clean clone with **one** documented command, with warnings promoted to
errors, and without network access. Measure: run it in a fresh clone; record the command and
the exit code. Pass: exit 0, no warnings, no network.

### 6. Link integrity — `high`
Internal links all resolve. External links are checked, and failures are allow-listed
individually by URL with a reason — never suppressed wholesale. Measure: link checker exit
code in CI. Pass: 0 broken internal links.

### 7. Executable examples — `high`
Every fenced block a reader is expected to run is executed in CI, with its real output. Measure:
count of runnable blocks vs. count executed. Pass: 100%. Blocks that cannot be executed are
explicitly marked non-runnable so the ratio stays honest.

### 8. Prose gates — `medium`
A prose linter enforces terminology from the project glossary and the banned-word list
(`simply`, `just`, `easily`, `obviously`, `blazing fast`, `click here`, …). Measure: linter
exit code. Pass: 0 violations, with the config committed at `vale.ini` / `.vale/` or the
equivalent.

### 9. Accessibility — `high`
Rendered pages are checked against WCAG 2.2 AA. The criteria a docs site fails most often, and
that the gate must cover by number: SC 1.1.1 (non-text content), SC 1.3.1 (info and
relationships), SC 1.4.3 (contrast), SC 1.4.10 (reflow at 320 CSS px), SC 2.4.4 (link purpose),
SC 2.4.7 (focus visible), SC 2.4.11 (focus not obscured), SC 3.1.1 (page language). Measure:
automated check on a representative page sample plus a keyboard-only pass on navigation and
search. Pass: zero automated failures; keyboard reaches every interactive control.

### 10. Search — `medium`
Search exists, is keyboard-reachable, and its **zero-result query log** is collected. Measure:
is the log being written anywhere? Pass: yes, and it is reviewed on a stated cadence. That log
is the only unbiased list of documentation gaps a project will ever get, and almost nobody
collects it.

### 11. Versioning — `high`
One model, chosen deliberately: latest-only, latest-plus-previous-major, or full matrix.
Required regardless of model: a version selector, a banner on non-current versions, canonical
link tags pointing at current, a migration guide per major, and a redirect map for moved URLs.
Docs ship from the same commit as the code. Measure: presence of each; count of inbound URLs
without a redirect. Pass: all present, redirect map covers every moved path.

### 12. Ownership and freshness — `critical`
`CODEOWNERS` covers 100% of the docs path. Every page carries `last_reviewed: YYYY-MM-DD` and a
cadence. A scheduled job reports pages past cadence. A CI rule requires a docs change (or an
explicit labelled exemption with a reason) when a watched source path changes.

```bash
# uncovered pages: present in the tree, absent from CODEOWNERS patterns
comm -23 <(find docs -name '*.md' | sort) <(git check-attr --stdin -a < /dev/null; echo)
grep -c 'docs/' CODEOWNERS .github/CODEOWNERS 2>/dev/null
grep -Lr 'last_reviewed:' docs/ --include='*.md' | head -50
```

Pass: uncovered set empty, `last_reviewed` present on 100% of pages, stale report scheduled.

Cadences by risk: security/auth 3 months; install/quickstart every minor release; how-to
6 months; explanation 12 months; reference never (it is regenerated).

## Contribution flow

Measure the path from "I found a mistake" on a rendered page to "the fix is proposed", in
clicks. Required: an edit link on every page pointing at the source file; a docs build command
in `CONTRIBUTING.md`; issue templates that separate *docs wrong* from *docs missing*; a preview
deployment URL on every pull request; a stated review SLA.

Pass: ≤ 4 clicks, preview URL present on pull requests. Every extra step loses contributors,
and a docs site that is hard to fix is a docs site that stays wrong.

## Translation, only if someone owns it

Decide before launching a locale, not after:

- Which subset is translated — typically landing, install, quickstart and top task guides.
  Reference is generated and normally stays in one language.
- One source locale; translations may lag but must show a banner and link to the source page.
- Missing translation falls back to the source locale, never 404.
- Machine translation is labelled as such, or not published.
- `lang` attribute per page (WCAG 2.2 SC 3.1.1), `hreflang` alternates, locale in the URL path
  rather than a cookie, and a build that fails on an untranslated key rather than emitting it.

**If no named person is accountable for a locale, do not launch it.** A stale translation is
worse than none, because it is trusted.

## Output

- `--audit` → `review.v1` to `.foundry/blackboard/<wave>/docs-architect.json`, with
  `dimension: documentation-system`, one `finding.v1` per failed check, each with a
  `failureScenario` describing a real reader hitting the gap, and `verdict` = `block` if any
  `critical` check fails.
- `--bootstrap` → `plan.v1` with waves ordered by dependency: ownership and CI gates first,
  structure second, content last. Every `gate` is a command with an expected exit code, never a
  human judgement. `outOfScope[]` names what the docs will not cover.

Validate with `mcp__plugin_foundry-core_foundry__contract_validate` before returning.

Wave ordering is deliberate: putting content first produces a large set of pages with no owner
and no gate, which is the state most projects are already in.

## Exit criteria

- [ ] Inventory complete, with orphan and fossil lists.
- [ ] All twelve checks measured, each with its command and result.
- [ ] Every failed check emits a `finding.v1` with a severity and a concrete failure scenario.
- [ ] Reference-is-generated check run with the grep above; every hand-maintained table listed.
- [ ] Build reproduced from a clean clone; the exact command recorded.
- [ ] Accessibility gate names the WCAG 2.2 success criteria by number.
- [ ] `CODEOWNERS` coverage measured as a percentage, with the uncovered list.
- [ ] Contribution path measured in clicks.
- [ ] Versioning model named, with the redirect map status.
- [ ] Artifact validates; reply ≤ 300 tokens.

## Interop and degradation

- Structure decisions that are expensive to reverse (generator, versioning model, search
  backend) are routed to `tech-scout` for an `adr.v1`, not decided on preference here.
- Page prose: `technical-writer`. Reference generation: `api-reference`.
- Glossary terms come from `fact.v1` type `glossary`; do not invent vocabulary.
- If `superpowers` is installed, invoke `superpowers:writing-plans` to turn the wave list into
  scheduled work; otherwise emit `plan.v1` directly and note that planning was unassisted.
- If the `foundry` MCP server is unavailable, keep the audit in `.foundry/scratch/<session>/`
  and report the blocker; do not hand-write blackboard files.
- If no link checker, prose linter or accessibility tool is installed, do not install one
  silently. Record the check as `unmeasured`, and make installing it a wave-1 task with the
  exact command.

## Deliberately not covered

- Page content, examples and titles.
- Visual design, theming and branding beyond the named WCAG criteria.
- Marketing site, blog and release-announcement copy.
- Developer-portal product features: authenticated API consoles, key management, usage dashboards.
- SEO strategy. Canonical tags, `hreflang` and stable URLs are specified because they are
  correctness; ranking work is out of scope.
- The translation itself.

## References

- `references/site-checklist.md` — the twelve checks as a copyable checklist with commands and
  pass conditions.
- `references/ci-pipeline.md` — the eight CI stages, their failure conditions, and the
  generator-agnostic wiring.
