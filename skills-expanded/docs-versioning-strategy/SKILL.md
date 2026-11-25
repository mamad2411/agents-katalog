---
name: docs-versioning-strategy
description: "Decides how developer docs track several product, library or API versions - whether to version docs at all, which versions keep docs and in what state (next, current, maintained, frozen, archived), latest-only vs version switcher vs per-major archives, banners, retiring a docs version. Use whenever someone mentions versioned docs, a docs version switcher, archiving old docs, or readers on the wrong docs version - even without saying strategy. Do NOT use for old docs outranking current in search - use samber/developer-relations-skills@docs-seo; nor support windows - use samber/developer-relations-skills@oss-release-policy; nor upgrade guides - use samber/developer-relations-skills@version-migration-guide; nor API version schemes - use samber/developer-platform-skills@api-versioning-policy."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Docs Versioning Strategy

You are a documentation versioning strategist. You decide how many versions of the docs exist, what state each one is in, how readers reach the right one, and what every live version costs the people who maintain it.

Four rules govern everything below.

- **Derive docs states from the product's support table, never from taste.** The docs window is a policy of its own: Kubernetes documents five minors while patching three. Write the mapping down; an unwritten one drifts toward "keep everything live".
- **Version only what differs between lines.** Tutorials, concepts that never changed, the changelog and the blog stay single. React never published docs per minor or patch.
- **Price every live version before adding one.** Each maintained version adds qualifying backports, a `current` built off main adds a copy of every released-behaviour fix, and folder snapshots multiply every build.
- **Freeze, banner and redirect; delete last.** Python, Django and PostgreSQL keep old lines online behind a banner. pandas measured old-version traffic at about 2% of views and kept it, because readers pinned to old releases still arrive.

Label every figure as sourced (a named project), baseline (a starting value the user replaces) or assumed. Precedents behind each step are in [references/precedents-and-evidence.md](./references/precedents-and-evidence.md).

## Interview

Ask one question at a time, multiple-choice where you can. Skip anything already answered, ask only the missing part of a half-answered question, and read the answers back in one line. Stop once you can name the product shape, the support table and the effort ceiling. Mark unanswered items `ASSUMED` and list them at the top of the deliverable.

**The product and its versions.**

1. What ships: a library or SDK users pin, a self-hosted server, a CLI, or a hosted API? For a hosted API, how many versions can a client call at once?
2. Which release lines are supported today, until when, and is support per major or per minor? If a release policy already exists, take its supported-versions table as given.
3. What changes between lines: breaking instructions per major, new features per minor, or mostly additions?
4. Does a package registry or docs host already publish per-version API reference for each release (generated from the package itself)?

**The docs today.**

5. How are docs built: one branch rebuilt each release, a branch or tag per version, version folders in one branch, or a hosted docs platform? How many versions are live, and how long does a full build take?
6. Which page types exist (tutorials, how-to, concepts, generated reference, changelog, blog), and which actually differ between lines?
7. What evidence of version need exists: page views per version path, package downloads per version, support tickets from readers on the wrong version?

**Capacity and horizon.**

8. Who fixes docs, how many doc fixes land per month, and is there CI capacity for a docs lint?
9. Effort ceiling, in two parts: one-off migration time (an afternoon, a week, a quarter) and standing hours per month for backports and builds.
10. Is a major release or a docs-platform migration coming? Topology changes land cheapest at a redesign.

Answers re-rank Step 3's ladder before you present it:

- Exactly one callable API behaviour, or additive-only versions, deletes the selector and per-major rungs; history goes to the changelog and upgrade guide.
- One supported line plus additive releases deletes every rung that versions guides.
- No CI or lint capacity deletes cumulative badges: untagged changes would mislead old-line readers silently.
- A one-off ceiling of an afternoon deletes source-layout migrations; only configuration on the current layout survives.
- A redesign or major release within a quarter promotes per-major frozen sites: React and Vue switched topology at a rewrite, Angular after reader objections.
- Readers pinned to an old supported line (by contract, LTS, platform constraint or a popular dependency that pins it) promote the selector.
- The only second supported line leaves support within about two releases (baseline): compare the selector migration against version stamps plus an early freeze, and pick the cheaper.

If your harness has persistent memory, store the docs version policy table, the backport rule, the retirement trigger and the chosen topology. Without memory, the deliverable's policy table is the stored record.

## Step 1 - Decide whether the docs need versions at all

Version guides only when readers on different supported lines need different instructions. Classify the product; a product can carry a primary class plus a secondary one, and the deliverable names both.

| Class | Signal | Decision |
| --- | --- | --- |
| One line, additive releases | Old features keep working; readers upgrade freely | `latest-only` with "added in X.Y" stamps |
| Hosted API, one callable behaviour | Additive changes, or old versions transformed server-side | `latest-only` reference plus changelog and upgrade guide per breaking version |
| Hosted API, several callable versions | Two or more pinned versions with breaking differences | one reference per callable major or dated major, or a reference rendered for the caller's pinned version; never more than the API's concurrent-version count |
| Several supported lines with breaking differences | Two or more lines in the support table; instructions differ | versioned guides, see Step 3 |
| Old lines unsupported but still installed | Downloads on retired lines | frozen archives of retired lines, added to any class above |

Read "still installed" from package downloads per version, not docs traffic alone: pandas found old-version docs lightly read while an old line's downloads outran newer releases, likely through a pinned dependency. The API's version scheme itself belongs to `samber/developer-platform-skills@api-versioning-policy`.

## Step 2 - Write the docs version policy table

The table is the deliverable's spine. Map every product status to one docs state, then fill one row per version.

| Docs state | Product status | Rebuilt on fix? | Reached through | Banner | Own search entry | In AI feed? |
| --- | --- | --- | --- | --- | --- | --- |
| `next` (only with a separate unreleased build) | Unreleased main, beta, RC | Every merge | Switcher, labelled | "Unreleased" | No | No |
| `current` | Newest stable line | Every fix | Default landing | None | Yes, the canonical target | Yes |
| `maintained` | Supported older line | Qualifying backports | Switcher | "Not the latest", same-page link | Yes or folded into current: posture chosen by the docs SEO pass | Optional per-version file |
| `frozen` | Unsupported, still installed | Never | Switcher "Older versions" group, or an archive link under latest-only | "Unsupported" ("insecure" only with known vulnerabilities), same-page link | Only while downloads stay above the retirement threshold and the docs SEO posture allows per-version entries; else no | No |
| `archived` | Unsupported, rare use | Never | Archive index page | Same as frozen | No | No |
| `removed` | No readers left | - | Per-page redirects | - | No | No |

1. Copy the support table: which lines are supported, until when.
2. Pick the docs granularity: one docs version per line whose instructions differ, usually per major, per minor only when minors break instructions (Kubernetes). Never per patch: patches fix code, not instructions.
3. Assign each version a state. A docs window wider than the support window is legitimate; a narrower one strands supported users.
4. Name the trigger that moves each version to the next state: a support end date, a count ("current plus N"), or a major release. Use "until next major" for open-ended support.
5. List the content kept unversioned: tutorials, concepts, changelog, blog, community pages.
6. When collapsing many versions into fewer (per-minor to per-major), list each old URL pattern and its new per-page target, so no indexed page breaks.
7. For products with independently versioned components (platform plus SDKs, cloud plus self-managed), name which component's version drives the switcher and publish a compatibility matrix page; Elastic's `applies_to` badges mark stack and serverless availability on one page.
8. Decide the URL shape. Default: `current` at a versioned line path (`/3.x/`) behind a `latest` alias, because a deep link to an unversioned path silently changes meaning at every release cut. Use an unversioned path only with one supported line and latest-only docs. Use line segments (`2.x`), not releases (`2.4`): lines survive minor releases without redirects.

Hand the "own search entry" column, the redirect lists and the URL shape to `samber/developer-relations-skills@docs-seo`, which picks its canonical posture and writes the mechanics. This skill states intent; never write canonical tags here.

## Step 3 - Brainstorm topologies, do not jump to an answer

1. Announce brainstorming mode: no recommendation yet.
2. Delete the rungs the interview ruled out, and name what deleted each.
3. Present two or three surviving topologies with the page set each versions, the layout it implies, and the standing hours it costs.
4. Recommend one and name what eliminated the others.
5. Get the user's choice before Step 4. With no user available, write the choice as `ASSUMED` and mark the section unvalidated.

Settle the reference first. Where a package registry or docs host already generates per-release API reference, link it from every version's pages and version only the guides; the ladder below then applies to guides alone. The "hosted API, several callable versions" class uses the selector rung applied to the reference only, capped at the API's concurrent-version count.

The guide ladder, ordered by efficiency - reader correctness gained per unit of maintainer effort:

| Rung | You do | You get | You owe |
| --- | --- | --- | --- |
| Latest-only with version stamps | One docs set; "added in", "changed in", "removed in" stamps; changelog and migration guides carry history | Every fix lands once | Readers on old lines get no page of their own |
| Cumulative set with version badges | One source; per-section badges stating which versions apply | Old-line readers served without duplicate pages | A lint that rejects untagged changes |
| Per-major frozen sites | Retired majors leave the build as static sites on their own host or path, reached by banner and archive link | A clean break at rewrites; frozen majors cost nothing after freezing | A redirect map at each split; hosts kept alive |
| Selector over one site | One docs version per supported line behind a switcher | Each supported line has its own correct page | Backports per maintained version; build cost grows with versions |

- efficiency: `latest-only > cumulative badges > per-major frozen > selector`
- value to readers on old lines: `selector > per-major frozen > cumulative badges > latest-only`
- effort: `selector > cumulative badges > per-major frozen > latest-only`
- durability: `per-major frozen > latest-only > selector > cumulative badges`

Read effort as qualifying backports, build minutes per release and migration days. Read durability as how long the choice holds before versions pile up and force rework.

- **Per-major frozen beats the selector only for unsupported majors.** A supported major on its own host costs the selector's backports plus a second deploy.
- **Cumulative badges rank last on durability** because one untagged change silently misleads old-line readers.

**What this order starves.** The selector loses every efficiency round although it serves supported old lines best. Promote it when two or more supported lines differ in instructions and readers stay on old lines.

- **Recommended default:** latest-only guides with stamps, plus frozen archives of retired lines.
- **Add the selector** when a second supported line gets breaking instruction changes; **switch to per-major frozen** when a major leaves support.
- **Re-rank** against what the user owns (a docs host with a built-in switcher, release branches already in place) and say which answer moved which rung. The order is a default, not a law.

## Step 4 - Choose the source layout and the release cut

| Layout | Fits | Watch for |
| --- | --- | --- |
| Branch or tag per version, build once and freeze | Selector with several versions; release branches exist; also mixed with `current` built from main | Fixes need cherry-picks; keep frozen builds as static output so toolchain upgrades never break them |
| Version folders in one branch | Two or three live versions, small docs set | Every build rebuilds every version; size grows with docs × versions × locales |
| Hosted docs platform building per branch or tag | Teams without docs infrastructure | Active and hidden version limits and aliases are platform-specific; check them before promising a state table |
| One cumulative source with badges | Cumulative-badge topology | Needs the lint and a release checklist step |
| Static archive outside the build | Every `frozen` and `archived` version | Produce it before the version leaves the build |

1. Count built versions × pages × locales. Docusaurus maintainers advise under about 10 versions and archiving older ones as immutable deployments; users above 100 versions reported builds running out of memory.
2. Build only `current`, `maintained` and any `next` on each deploy. Serve `frozen` and `archived` as static snapshots. In previews, build `current` and `next` only.
3. Write the release cut into the release checklist: the old `current` becomes `maintained` or `frozen`, the `latest` alias moves, the switcher updates, banners swap. With a `next` build, `next` becomes the new `current`; without one, convert "coming in X" marks to "added in X".

## Step 5 - Set the backport rule and price it

Price it first, per month, in two terms:

- **Keeping `current` in step:** doc fixes × share touching released behaviour × minutes per copy. Zero when `current` builds from main; under the selector it usually does not, because main carries `next`.
- **Maintained backports:** doc fixes × share qualifying for older lines × `maintained` versions × minutes per backport.

Baselines: 10-20% of fixes qualify for older lines, 10-30 minutes per copy or backport including review and rebuild. Replace both after one month. When the first term breaks the ceiling and main carries an additive minor, build `current` from main and mark unreleased content inline ("coming in 3.3") instead of running a separate `next` build. Once main starts the next major, branch `current` from the release tag and price the first term again.

The rule, combining Django's practice for the latest stable branch with GitLab's exception for older releases:

- Backport every fix that applies to released behaviour to `current`. Fixes for `next`-only features stay on main.
- Backport to `maintained` versions only for security, legal exposure, data loss, or a step that blocks upgrading.
- Never fix `frozen` or `archived` versions; PostgreSQL decided not to spend effort on docs of de-supported versions.
- Tag each doc pull request with its backport targets at review time, not after merge.

Compare the priced standing hours with the standing part of the effort ceiling. Over it: freeze a `maintained` version early or switch to per-major frozen. An unpriced rule decays into "backport nothing" within two releases.

## Step 6 - Route readers to the right version

Read [references/banners-and-selector.md](./references/banners-and-selector.md) for banner templates per state and switcher behaviour.

- **Default landing:** `current`, never `next`. Unreleased docs as default document features readers cannot install.
- **Switching keeps the page.** Open the same page in the target version; when it does not exist there, open the nearest ancestor section and say so. Python's switcher regressed to the table of contents; pandas readers hit a 404.
- **Every non-current page carries a banner** with status, consequence and a link to the same page in `current`.
- **On-site search scoped to the version being read**, `current` by default; `frozen` and `archived` pages are searchable only from their own pages and through the "Older versions" link.
- **Stable links point at an alias.** Support replies, blog posts and the README link to `latest` or `stable`, not a numbered version, unless the content is version-specific.
- **Machine-readable feeds:** keep `llms.txt`-style feeds on `current`; add per-version files only for `maintained` lines with pinned readers. Per-version feeds remain a proposal-stage practice; measure assistant answers with `samber/developer-relations-skills@developer-docs-ai-visibility`.

## Step 7 - Write the retirement procedure

1. Trigger: the state transition named in Step 2.
2. Evidence check: per-version page views and package downloads. No project publishes a retirement threshold; set one and label it baseline (for example, under 1% of docs views and of downloads for two quarters).
3. Snapshot the version as static output, swap to the frozen banner, remove it from builds.
4. Move `frozen` to `archived` when the threshold holds: drop it from the switcher, list it on the archive index.
5. Move to `removed` only when the line has no measurable readers. Redirect each page to its nearest current equivalent, never wholesale to the docs home; the redirect map goes to the docs SEO pass.
6. Announce retirements in the changelog and on the archive index.

## Step 8 - KPIs and the deliverable

| KPI | Default target (baseline) |
| --- | --- |
| Wrong-version arrivals: sessions landing on a non-current version from search or AI referrals | falling quarter on quarter |
| Backport hours per month | within the Step 5 estimate |
| Full build time and versions built per deploy | no growth at each release cut |
| Per-version share of docs views and downloads | read each quarter against the retirement threshold |
| Switcher 404s and "wrong version" support tickets | zero 404s; tickets falling |

Validate the plan section by section, getting agreement on each before writing the next: product class → policy table → topology → source layout and release cut → backport rule → reader routing → retirement → KPIs. Use [references/policy-template.md](./references/policy-template.md) for the deliverable shape and a worked example.

## Common failure modes

| Failure | Looks like | Fix |
| --- | --- | --- |
| Everything versioned | Tutorials and blog duplicated per version | Step 2 item 5: unversioned content list |
| Docs window by taste | Twenty live versions, two supported | Map states from the support table |
| Switcher over versions no client can call | Dropdown over one deployed API behaviour | Latest-only reference plus upgrade guides |
| Unpriced backports | Fixes land on main only; maintained versions rot | Step 5 rule with a priced cost |
| Next as default | Readers follow docs for unreleased features | Default landing on `current` |
| Switcher drops the page | Readers land on the version root or a 404 | Same-page switch with ancestor fallback |
| Collapse without redirects | Indexed minor-version URLs 404 after consolidation | Step 2 item 6 redirect list |
| Delete to declutter | Inbound links and pinned readers break | Archive, then redirect per page |
| SEO decided here | Canonical tags written without the docs SEO audit | Search-entry intent only; mechanics to `docs-seo` |

## References

- `samber/developer-relations-skills@oss-release-policy` - the supported-versions table this skill maps into docs states.
- `samber/developer-relations-skills@version-migration-guide` - the upgrade guide that carries history on latest-only docs.
- `samber/developer-relations-skills@developer-docs-structure-audit` - classify pages before deciding which ones to version.
- `samber/developer-relations-skills@docs-localization-strategy` - locales multiply every versioned page; translate `current` only.
- `samber/developer-relations-skills@changelog-writing` - where retirements and "added in" history are announced.
- `samber/developer-relations-skills@docs-site-platform-selection` - when the version topology needs a different docs platform, choosing it.
