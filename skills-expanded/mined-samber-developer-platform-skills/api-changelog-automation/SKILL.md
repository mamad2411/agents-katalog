---
name: api-changelog-automation
description: "Designs the provider-side pipeline that turns contract diffs of an API you publish (OpenAPI, GraphQL SDL, protobuf, AsyncAPI) into a breaking-change CI gate and a traced, per-version API changelog feed, classified by your own policy. Use whenever the user mentions oasdiff, openapi-diff, graphql-inspector diff, buf breaking, API schema checks, failing a PR on breaking changes to a published API contract, or an auto-generated API changelog. Do NOT use for release-note prose (samber/developer-relations-skills@changelog-writing), consumer-side upgrades (samber/developer-relations-skills@version-migration-guide), deprecation policy (samber/developer-platform-skills@api-versioning-policy) or callers of deprecated endpoints (samber/developer-platform-skills@integration-health-monitoring)."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# API Changelog Automation

You are building the machinery that notices every change to a published API contract, decides whether it breaks callers by your own written rules, stops the unapproved breaks, and writes a record integrators and their tools can read. The deliverable is a pipeline design: severity map, baselines, CI gate, declared-change channel, approval record, entry schema and feed, each wired to a file in the repo.

The recurring failure is trusting the diff tool twice: once for what counts as breaking (its defaults are not your policy) and once for what changed at all (it only sees declared structure). A green check then publishes a changelog that omits the change that broke a partner.

Boundaries:

- The breaking-change definition, notice windows and sunset rules come from `samber/developer-platform-skills@api-versioning-policy`. This skill encodes that policy into tool configuration; it never invents one.
- Polishing entries into readable release notes belongs to `samber/developer-relations-skills@changelog-writing`; the before/after upgrade guide to `samber/developer-relations-skills@version-migration-guide`. This skill hands them traced, structured entries.
- Who still calls a deprecated operation, and reaching them, belongs to `samber/developer-platform-skills@integration-health-monitoring`.

**Memory (advised):** When memory lives in a file, consider using `developer-platform-context.md`; if a different memory system is in use, rely on that instead. Store the severity-map location, baselines, approver group and feed URL there so later runs extend the pipeline instead of redesigning it.

## Interview

Ask these before designing anything. Batch them; this is an engineering setup, not a strategy debate.

1. **Surfaces and formats:** REST (OpenAPI 3.x or Swagger 2.0), GraphQL SDL, protobuf, AsyncAPI events, webhooks? One spec or several?
2. **Spec source:** hand-written contract-first, or generated from code annotations? Is it validated against the running service (contract tests, traffic validation)?
3. **Policy:** is there a written breaking-change definition? Paste it, or say none exists.
4. **Versioning and release unit:** URI major, header or date versions, semver in `info.version`, or continuous deploy with no versions? What does "a release" mean for the changelog?
5. **Audiences in the spec:** do internal, beta or partner-only operations live in the same file as public ones? How are they marked?
6. **Usage data:** can you count calls per operation (or per GraphQL field) per client over the last 30-90 days?
7. **Where the record goes:** changelog page, RSS/Atom, JSON feed, email digest, in-dashboard banner? Who reads it: humans, monitoring pipelines, coding agents?
8. **Deadline and effort:** when must the first gate run, is this one migration or a standing pipeline, and how many engineer-days plus which reviewers can you commit?

Question 3 gates the workflow. With no written definition, every severity choice is the tool author's opinion; route the policy to `api-versioning-policy` and, if the user must ship a gate first, mark every severity-map row **provisional** pending policy sign-off.

## Choose the rungs first

Pick which rungs to build before the workflow; steps 6-7 run only when the chosen rung includes them. Rank by value per unit of effort, and say the order out loud:

- efficiency: `PR gate > release diff + declared channel > approval record > feed > usage-aware classification > version-derived changelog`
- effort: `version-derived > usage-aware > feed > release diff + declared channel > approval record > PR gate`
- value: `version-derived > release diff + declared channel > PR gate > approval record > usage-aware > feed`

| Rung | You do | You get | Effort |
| --- | --- | --- | --- |
| PR gate | Diff vs merge base, fail on `err`, severity map | Accidental breaks stopped before merge | An hour or two, mostly reviewing the severity map |
| Release diff + declared channel | Diff vs last release, PR question, fragments | A complete record of what shipped, incl. behavior changes | Half a day plus a habit |
| Approval record | Acknowledgement rows with fingerprint, approver, link | Audit trail; entry text for every accepted break | A few hours, then per-break minutes |
| Feed | JSON + Atom with stable ids, per version | Monitoring pipelines and agents consume changes | About a day |
| Usage-aware classification | Operation-level telemetry feeding the gate | Fewer false alarms; safe removal of deprecated elements | A day or two, needs telemetry |
| Version-derived changelog | Each breaking change as a version-change record in code | Entries written at the change, impossible to omit | Weeks; only with per-version transformation |

- **Default:** PR gate plus release diff and declared channel. Add the approval record once the first accepted break lands.
- **What the order starves:** the version-derived changelog loses every efficiency round. Promote it when the platform already runs date-based, per-account versioning with response transformers (Stripe's pattern); there it costs a documentation field on records you already write.
- **Re-rank against the interview:** a fixed date (Q8) ships the PR gate alone first; a standing mandate promotes the approval record and feed; no usage data (Q6) deletes usage-aware classification rather than parking it last; machine consumers (Q7) promote the feed above the approval record.

## Workflow

1. Check the preconditions.
2. Build the severity map from the policy.
3. Pick one baseline per job.
4. Wire the PR gate.
5. Open the declared-change channel.
6. Record every accepted break (approval-record rung).
7. Generate entries and the feed per API version (release-diff and feed rungs).
8. Verify traceability, then publish and hand off.

## 1. Check the preconditions

- **No machine-readable spec:** stop. The changelog cannot be automated from prose. Route the source-of-truth rollout to `samber/developer-platform-skills@api-reference-quality`.
- **Spec not validated against the service:** the diff describes a document, not the API. Add contract tests or traffic validation before trusting any green result, and list it as the first gap in the design.
- **Generated spec:** pin the generator version, validate the output, and make it deterministic: stable `operationId`s, `$ref` (not inline) schemas, `$ref`'d `oneOf` branches, stable enum order. Semantic diff tools ignore key order; phantom changes come from positional and inline-versus-`$ref` churn, and they train reviewers to ignore the gate.
- **Baselines need a spec at a release:** a generated spec exists only at build time, so commit the spec of every release (or attach it to the release tag). The first release has no baseline: publish its entries by hand and start diffing from it.

## 2. Build the severity map from the policy

Take each line of the written breaking-change definition and find the check that enforces it. Tools disagree on the same change, so never adopt a default unread:

- Adding a response enum value: GitHub's published policy calls it additive; OpenAPITools `openapi-diff` and oasdiff flag it by default.
- Changing auth: GitHub calls any change to authentication or authorization requirements breaking. oasdiff reports added scopes and removed anonymous access as ERR, but removed scopes and an added alternative (OR) requirement as INFO. Gateway-only auth rules are invisible to every diff.
- Removing a deprecated element: oasdiff and `graphql-inspector` (`suppressRemovalOfDeprecatedField`) can pass it while callers still use it.

Keep two files next to the spec:

- `severity-map.md`, for humans: one row per check id - the policy line it enforces, the chosen level, the reason, and `provisional` while the policy is unsigned.
- The tool's level file, generated from it. oasdiff's `--severity-levels` file accepts only `<check-id> <level>` per line: no comments, no extra columns.

Then:

- Version-bump checks (oasdiff `api-major-version-not-bumped` and siblings) default to INFO and never fail a build. With semver `info.version`, raise them to `err`. With date, header or URI-path versions, oasdiff skips them; the per-version baselines in step 3 do the job.
- Mark lifecycle in the spec so removals are judged correctly: `deprecated`, a sunset date (`x-sunset`), stability (`x-stability-level`).
- Open enums: where the policy says a response enum may grow, declare `x-extensible-enum` on that field. Pin the enum check to `info` only when the policy declares every response enum open; the annotation also tells SDK generators to accept unknown values.
- Pinning a level disables a tool's own downgrades for that check; pin only what the policy contradicts.
- Pin the diff tool version. Upgrades change classification with no spec change; review the rule diff on each bump.

Per-paradigm flags, a CI workflow, the drift recipe, and how to give non-oasdiff findings stable fingerprints: read [references/tool-configuration.md](references/tool-configuration.md).

## 3. Pick one baseline per job

Each comparison answers a different question. Using one baseline for all three is the most common design error.

| Job | Compare the candidate against | Misses if you use another baseline |
| --- | --- | --- |
| PR gate | the merge base on the default branch | Release baseline blames this PR for changes merged earlier |
| Published changelog | the spec of the last **released** version (tag, GA spec, deployed release) | Default-branch baseline splits one release across many tiny diffs and loses the multi-PR total |
| Drift alarm | the spec the production service actually serves, or live traffic validated against it | Both others compare documents with documents |

For date- or header-versioned APIs, diff per version: version N's spec against version N's previous release, and the new version against its predecessor. A break that ships only in a new version must appear in that version's entries and nowhere else.

When one codebase serves every version through transformers or version gates, produce one spec per supported version at build time: run the generator once per version (version header, build flag or transformer-aware export) and commit each as `specs/<version>.yaml`. The release baseline for version N is `specs/N.yaml` at the previous release tag. A diff in a version that was supposed to be frozen is itself a defect.

## 4. Wire the PR gate

- Fail on `err`. Show `warn` in the PR summary as "potentially breaking", never silently drop it.
- Filter by audience before failing: oasdiff's `--stability-level` (default `beta`) excludes draft and alpha operations; exclude internal ones by extension name (`--filter-extension x-internal`) or path (`--unmatch-path`). An operation that gains the internal marker disappears from the filtered diff as a removal: callers lose it, so it stays breaking.
- Require a named approver for any accepted `err`: put the spec, `severity-map.md` and the acknowledgement file under one code-owners rule with required review. The `approver` field records who reviewed; it enforces nothing, and without the rule an author approves their own break in the same PR.
- Post the findings on the PR (comment or annotations) with check id and fingerprint, so approvals survive new commits within the PR.
- For GraphQL and other surfaces with usage data, add usage-aware classification (operation checks, `considerUsage`) only after the static gate works. Usage windows miss quiet clients: monthly jobs, mobile apps, SDKs with no recent traffic. Set the window to the longest client cycle you know of, not the tool default.

## 5. Open the declared-change channel

A structural diff cannot see behavior. Give authors a second channel and merge it into the same changelog:

- PR template question: "Does this change behavior, defaults, validation, error codes or bodies, auth, rate limits, pagination or ordering without a spec change?"
- A yes requires a change fragment (one JSON file per change, committed with the code) carrying the same fields as a diff-derived entry.
- Declared breaking changes go through the same approval as diff-detected ones.
- Date- or header-versioned API: list every version whose callers see the change. More than the newest version means pinned callers are affected; the versioning policy's exception path decides whether that may ship.

The full blind-spot list and the fragment format: read [references/blind-spots-and-declared-changes.md](references/blind-spots-and-declared-changes.md).

## 6. Record every accepted break

An ignore file without a record is where breaking changes disappear. Every acknowledgement row carries:

- the fingerprints or declared-change id it covers, plus the check id, operation, path and the tool's exact text for that change,
- approver, date, ticket,
- reason class: intended break shipping under a new version, spec correction to match the live service, security exception, or `historic` (audited, origin unknown),
- the notice or migration link callers will see,
- for spec corrections, the date the service started behaving this way.

Fingerprints move when the baseline moves (PR merge base versus release tag). The release run re-matches a PR-time approval only on check, operation, path and exact text, and only when a single finding has that location; any other match stays unapproved and needs explicit sign-off.

Spec corrections still produce a changelog entry: callers were told something false and deserve to learn the truth. Review the acknowledgement file each release; a row whose change no longer appears is deleted, never left to match a future change.

Generate the tool's ignore file from the acknowledgement rows in the PR job, before the gate (`python3 scripts/build-entries.py --acks acks.json --ignore-out oasdiff-err-ignore.txt`); never edit it by hand. Commit an empty acknowledgement list and ignore file at setup.

**An existing hand-edited ignore file** is audited before the new gate goes live, line by line:

1. Rerun the diff without the ignore file against the current release baseline. Lines that match nothing are deleted.
2. Each line that still matches gets an acknowledgement row: reason class (`historic` when nobody knows why it was added), ticket if one exists, approver `unknown - audited <date>` if nobody signed it.
3. Each audited line that hides a break callers never saw announced gets a changelog entry in the next release, as a spec correction or a late notice.

Freeze new hand-added lines from the day the audit starts, or the audit never ends.

## 7. Generate entries and the feed per API version

- Build entries only from structured output: the release-baseline diff as JSON (`oasdiff changelog -f json`, or another tool's output mapped to the same fields), fragments, acknowledgement rows. Run once per spec: fingerprints carry no file name. Keep the tool's wording beside any human summary, and attach the author's narrative from the PR or fragment.
- Exclude version-bump findings: they are rules about the release, not contract changes.
- One entry per contract change, grouped by API version, then by resource or product area, breaking first. A change the tool reports for one shared schema is one entry listing every affected operation and every fingerprint it covers; identical wording on unrelated operations stays separate entries.
- Each entry carries a version-scoped id, a classification (`breaking`, `potentially-breaking`, `non-breaking`), its source (`diff:<check-id>` or `declared:<fragment-id>`), the fingerprints it covers, the affected operations, the action required, and the sunset date when one applies.
- Exclude documentation-only edits and operations not visible to the feed's audience.
- Publish two artifacts: a machine-readable feed (JSON and Atom/RSS), and a human page per version. Keep the "action required" text in the feed, not only on the page.

```
python3 scripts/build-entries.py --changelog changelog.json --api-version 2026-07-01 \
  --date 2026-07-01 --fragments changes/ --acks acks.json --out entries.json \
  --ignore-out oasdiff-err-ignore.txt
```

It writes skeleton entries with `summary` and `action_required` left for a human, groups shared-schema findings, rejects fragments with a non-canonical classification or kind, and prints a notice for each break no acknowledgement covers. Entry schema, feed shapes and good/bad examples: read [references/entry-and-feed-format.md](references/entry-and-feed-format.md).

## 8. Verify traceability, then publish and hand off

```
python3 scripts/check-entry-trace.py --diff changelog.json --entries entries.json \
  --fragments changes/ --api-version 2026-07-01 --acks acks.json
```

It fails when an entry traces to no finding or fragment, changes the classification of what it covers, carries another version, or lacks an action; when a breaking or potentially breaking finding or fragment has no entry; and when a breaking entry's approval is missing or does not cover all its sources. Both scripts need Python 3.8+ and the standard library only; exit 0 means pass, 1 findings to fix, 2 unusable input.

- An LLM may shorten or reword an entry. It may not add a path, field, status code, date or consequence absent from the entry's source; rerun the trace check after any rewrite.
- Hand the traced entries to `changelog-writing` for prose, and each breaking entry to `version-migration-guide` when callers need before/after code.

## Rationalizations to reject

| Rationalization | Why it is wrong |
| --- | --- |
| "The diff is green, so nothing breaking shipped." | The diff saw declared structure only. Check the declared-change channel and the drift alarm. |
| "The tool's defaults are industry standard." | Tools disagree with each other and with published provider policies on enums, auth and deprecated removals. |
| "Add it to the ignore file and move on." | An unrecorded ignore hides the break from the changelog and matches future changes. Record it (step 6). |
| "It was deprecated, so removing it is safe." | Deprecation is a label. The versioning policy's sunset and usage rules decide removal; encode them with `x-sunset` and usage-aware checks. |

## Failure modes

- **Gate turned off by noise.** Phantom changes from a non-deterministic generated spec teach the team to set `fail-on none`. Fix the generator output, never the threshold.
- **Spec drift rewarded.** Engineers stop updating the spec to keep CI green. The drift alarm catches this; without it, the gate measures fiction.
- **Changelog per deploy for a versioned API.** Callers pinned to version N read changes that only exist in N+1.

## Measurement

- **Escaped breaks:** breaking changes reported by integrators or support that have no changelog entry. Target zero; each one is a blind-spot row or a severity-map row to add.
- **Trace coverage:** share of published entries the trace check links to a source. Pass bar: 100% before publishing.
- **Acknowledgement hygiene:** rows without approver, ticket or link; rows older than one release with no matching change. Pass bar: zero.
- **Override rate:** accepted `err` findings per release. A rising rate means the severity map drifted from the policy or the policy from reality.

## Invocation examples

- "Set up oasdiff in our GitHub Actions so breaking changes to openapi.yaml fail the PR, and generate the API changelog for each release."
- "Our GraphQL schema checks keep flagging enum additions as breaking. How should we configure graphql-inspector against our policy?"
- "We publish date-based API versions. Design a pipeline that produces a per-version changelog feed partners can subscribe to."

## References

- `samber/developer-platform-skills@public-grpc-api-design` - proto package versioning and buf governance for the protobuf surface this pipeline diffs.
- `samber/developer-platform-skills@public-graphql-api-design` - additive-friendly schema design that keeps the GraphQL gate quiet.
- `samber/developer-platform-skills@webhook-platform-design` - event payload versioning whose AsyncAPI diffs this pipeline classifies.
- `samber/developer-platform-skills@api-beta-program` - beta surfaces excluded from the gate by stability level until GA.
- `samber/developer-platform-skills@sdk-package-publishing` - SDK release notes for generator-caused breaks, kept apart from API-caused entries.
