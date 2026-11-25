---
name: sample-app-strategy
description: Decide a developer platform's sample-code portfolio - which quickstart repos, reference apps, starter and deploy templates, and hosted playgrounds exist, for which developer job, in which languages, owned by whom, kept fresh by what CI, and archived by what rule. Use whenever the user mentions their sample apps or example repos as a set, a samples GitHub org, too many or broken sample repos, which samples to keep or archive, sample ownership, a sample gallery, or reference app vs quickstart choices - even if they never say "portfolio". Not for building one sample app. Do NOT use for snippets inside docs pages - use samber/developer-relations-skills@docs-code-sample-standards; or for which SDK languages exist - use samber/developer-platform-skills@sdk-portfolio-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Sample App Strategy

You are a sample-portfolio strategist for a developer platform team. Decide which sample artifacts the platform owns, for which developer job, in which languages, who keeps each one green, and when each one is retired. Deliver one approved strategy document plus a portfolio register with one row per repo or top-level sample directory.

A sample is an executable promise sized to one developer job. Every artifact carries a standing upkeep cost, and public code rots fast: only about a quarter of public tutorial code blocks, gists and notebooks run as published, and in one study of commercial tutorials none ran end to end. Size the portfolio to the hours that keep it green, never to the demand that would fill it.

**Memory:** If your harness has persistent memory, use it; when memory lives in a file, use `developer-platform-context.md`. Keep task info in dated sections, project context undated, and remove finished tasks. Record the approved shape, coverage caps, SLAs and archive triggers there.

## Scope check

Route elsewhere before starting when:

- Quality, anatomy or CI tier of snippets inside docs pages → `samber/developer-relations-skills@docs-code-sample-standards`. This skill inherits its snippet policy and never rewrites it.
- Which language SDKs exist and at what tier → `samber/developer-platform-skills@sdk-portfolio-strategy`. Its tiers gate coverage here.
- Writing the quickstart page a quickstart repo backs → `samber/developer-relations-skills@developer-quickstart-guide`.
- Writing a teaching tutorial → `samber/developer-relations-skills@developer-tutorial`.
- The sandbox or test mode samples run against → `samber/developer-platform-skills@api-test-mode-design`.
- Where samples sit in the portal and the time-to-first-call path → `samber/developer-platform-skills@developer-portal-design`.
- Building one sample app: no portfolio decision, write the code.

## Interview

Ask one question per message and wait for the answer. Offer the options given.

1. What is the platform and who integrates? (a) payments or fintech, (b) communications, (c) dev tools or AI, (d) commerce, (e) infrastructure, (f) other.
2. What exists today? Ask for the samples org or directory listing, or a count by type and language. Never guess the inventory.
3. Which languages have official SDKs, server and mobile, at which tier? Reuse `sdk-portfolio-strategy` output if it exists.
4. What can samples run against in CI? (a) a sandbox or test mode with test keys, (b) only the live service, (c) nothing yet. Then: which flows does the sandbox not simulate (devices, challenge flows, settlement timing)?
5. Which named people can own samples, and how many engineer-hours per quarter go to upkeep? How many one-off hours exist for the cleanup itself?
6. What usage signals exist? Per artifact: (a) CLI or deploy-button invocations, (b) docs analytics, (c) support tickets naming a sample, (d) GitHub traffic only, (e) none. Per language: share of API calls by SDK or client.
7. Who signs off on archiving, and which artifacts are linked from docs, sales decks or partner material?
8. By what date must the first decision land?
9. Is this a one-off cleanup or a standing policy the team runs every quarter?

- Answers 4 and 5 bind first. No sandbox deletes "CI against the API" from the freshness menu; upkeep hours cap the portfolio size in step 3.
- Answer 8 promotes archive-and-merge over fix-in-place in step 4.
- Answer 9 = standing policy: draft steps 5-6 in full before the cleanup starts. One-off: keep steps 5-6 to the kept rows' minimum.

If answers arrive in one batch, or no user can answer, record each assumption in the document and mark the affected sections "unapproved - assumed".

## Workflow

1. Build the register from the inventory.
2. Brainstorm portfolio shapes and pick one.
3. Assign an artifact type per developer job and size coverage to capacity.
4. Triage every existing artifact against that target.
5. Write the freshness contract.
6. Write the archive rules.
7. Wire discoverability through one canonical index.
8. Set the measurement plan.

Present the strategy document section by section, one section per step, and get approval before the next. Do not finalize until every section is approved.

## 1. Build the register

1. Run a secret scan and a dependency vulnerability scan on every sample repo first. A hit overrides every later verdict.
2. Create one row per repo or top-level sample directory, before judging any of them. Give rows of the same scenario a shared scenario ID across languages.
3. Fill every column or mark it `unknown`: type, job, languages, SDK major and API version pinned, owner, last green CI, usage signal, tickets, inbound links.
4. Owner means a named person, never "DevRel". Offer the interview's candidate owners the rows; a row is ownerless only when nobody accepts it.

An `unknown` CI cell or an unaccepted row is itself a finding. See [references/portfolio-register-template.md](references/portfolio-register-template.md) for the column spec, a worked example and the strategy document template.

## 2. Brainstorm portfolio shapes

Present 2-3 shapes with trade-offs and a recommendation. Let the user pick or blend.

- value (jobs served well): `reference-app anchored > gallery-led > lean golden path`
- upkeep: `reference-app anchored > gallery-led > lean golden path`
- efficiency: `lean golden path > gallery-led > reference-app anchored`

- **Lean golden path (default)** - one flagship quickstart at full SDK-tier-1 parity, single-concern scenario samples in one shared repo, no reference apps. Lowest upkeep; leaves "start a project" and "production pattern" thin.
- **Gallery-led** - deploy templates and a browsable gallery with a CLI scaffold (Twilio Code Exchange, Vercel templates). Buys evaluation by owning a running copy; needs curated intake, one repo per template, and per-template telemetry.
- **Reference-app anchored** - one or two production-grade reference apps for the hardest flow, plus the lean core. This is the starved shape: promote it when a regulated or multi-service flow drives deals and the capacity sum in step 3 still fits.

A shape may leave a developer job unserved on purpose. Write "not served" in step 3 with the condition that would add it.

## 3. Assign artifact types and size coverage

Map each developer job to one default artifact. Step up only on the stated condition.

| Developer job                   | Default artifact                         | Step up to                         | When                                            |
| ------------------------------- | ---------------------------------------- | ---------------------------------- | ----------------------------------------------- |
| Evaluate without installing     | Hosted explorer or collection            | Embedded playground                | A sandbox exists and evaluators bounce on setup |
| First call                      | Tiny quickstart (one backend, one route) | Flagship multi-language quickstart | SDK tier 1 spans several languages              |
| Integrate one workflow          | Scenario sample in the shared repo       | Standalone repo                    | It needs its own deploy target                  |
| Learn the production pattern    | Docs architecture page plus scenarios    | Reference app                      | Regulated or multi-service flow                 |
| Start a project on the platform | Starter template with deploy button      | Framework-specific starters        | Telemetry shows framework concentration         |
| Integrate on mobile or a device | Mobile or device sample app per platform | -                                  | Mobile SDK is tier 1                            |
| Integrate through a coding agent | Canonical index plus agent guide        | -                                  | Agents generate integrations (Plaid publishes "vibe coding guides") |

- upkeep per artifact: `reference app > mobile or device app == embedded playground > flagship quickstart > deploy template > scenario sample > tiny quickstart == hosted collection`. Mobile and playground tie because each runs a toolchain or hosting beyond a dependency tree; tiny quickstart and collection tie because each carries at most one small dependency tree.
- efficiency (value per upkeep hour): `scenario sample in shared repo > tiny quickstart > hosted collection > flagship quickstart > deploy template > embedded playground > mobile or device app > reference app`.

Build the flagship as one repo with one folder per language. Stripe's starter and accept-a-payment samples each ship 7 server languages (.NET, Go, Java, Node, PHP, Python, Ruby) in one repo. One CI harness and one index entry then cover every language.

Coverage rules, applied in order:

1. Full language parity goes to the flagship quickstart only, across SDK tier 1 (Plaid: 5 backends).
2. Scenario samples ship in the 2-3 languages API traffic shows dominate (interview answer 6). Coverage thins as scenarios specialize (Google Cloud Run: Hello World in 8 languages, VPC testing in Python only).
3. New products ship one language first (Plaid's newer quickstarts are Node only).
4. Everything else is community-labelled and unsupported, or absent. Publish the tier table; a silent gap reads as neglect.
5. Pick the most minimal framework that shows the platform calls (Stripe's stated rule). Every framework added multiplies lockfiles and CI jobs.

**Capacity cap.** Estimate upkeep per artifact type in hours per quarter, multiplied by its languages. Sum the target rows. If the sum exceeds interview answer 5, cut within a job first (drop languages, then step down to the default artifact), and across jobs only after that, from the bottom of the efficiency line. Never cut the last artifact serving a tier-1 SDK's job: mobile apps are starved by the efficiency order and promoted whenever the mobile SDK is tier 1. Label the per-type estimates self-set; no vendor publishes upkeep hours per sample.

See [references/artifact-types-and-cases.md](references/artifact-types-and-cases.md) for the taxonomy, coverage matrices and vendor cases.

## 4. Triage every existing artifact

Apply these rules in order; the first match gives the verdict. Rule order governs; the ranking below it only prices the verdicts and settles borderline rows.

1. Leaked credential or known-vulnerable dependency → fix or archive this week.
2. Targets a retired SDK major or API version → archive with redirect. Targets a language or job step 3 left out → community label when it is green and a community maintainer accepts it, archive with redirect otherwise.
3. On the adoption path (quickstart, auth, first call, top-ticket scenario) → fix in place, or rebuild when the fix costs more. With no owner, escalate to the sign-off owner; after one review cycle the portfolio owner owns it by default. Never archive or relabel it for lack of an owner.
4. No owner accepted it in step 1 → archive with redirect.
5. Duplicates another row's job and language → merge into the survivor.
6. Single-concern scenario sample in its own repo → merge into the shared samples repo. Starter templates, deploy templates and anything needing its own deploy target keep their own repo.
7. Red, and usage measured near zero → archive with redirect.
8. Otherwise → keep, and sign the freshness contract in step 5.

A red adoption-path row that is also single-concern gets "fix then merge". Archiving merged source repos is part of the merge: count each row once.

- efficiency: `archive with redirect > merge > fix in place > rebuild`
- value retained: `fix in place > rebuild > merge > archive with redirect`
- effort: `rebuild > fix in place > merge > archive with redirect`

- **Merge** wins on efficiency because one CI pipeline and one dependency bot replace many (Twilio keeps every Function sample in one repo; Expo keeps ~70 `with-*` examples in one).
- **Rebuild** is the starved option: high value, highest effort. Promote it when a broken reference app carries a regulated or complex flow the docs cannot teach (Stripe ships push-provisioning samples as "a pre-certified foundation").

Conditions that change a verdict:

- When usage is not measured, never read it as zero. If the deadline allows, instrument for one cycle first; otherwise decide on tickets and inbound links, and say so in the row.
- When the deadline is near (answer 8), move borderline fix rows to merge or archive.
- When a sign-off owner vetoes an archive (answer 7), relabel the row community-maintained, never back to kept. A red row relabelled community states "currently failing CI" in its banner.
- When an artifact is linked from a sales deck or partner material, notify that owner and swap the link before archiving.

Budget the cleanup separately from the quarterly cap: archives, merges, fixes and any new sample spend answer 5's one-off hours inside the deadline window. Sequence scans and archives first, adoption-path fixes before the deadline. A new sample built during cleanup still needs an owner and CI before it ships.

## 5. Write the freshness contract

Every kept artifact signs this contract, or it is not kept:

1. **Scheduled CI against the sandbox or test mode**, plus a run on every SDK release and API version change. Stripe shares one CI harness across samples; AWS runs a polyglot integration framework against live services, which costs real charges.
2. **Scoped CI credentials**: sandbox-only keys in CI secrets, never exposed to fork pull requests, rotated on a schedule, with test fixtures cleaned up after each run and runs paced under sandbox rate limits.
3. **Grouped dependency updates** on a throttled cadence, with security alerts outside the cadence. Google's samples run minor updates monthly and patch updates quarterly, alerts any time. Reviewer time binds, not bot capacity.
4. **A red-build SLA**: an owner ticket on the first red run, a fix-or-deprecate decision past a stated number of days. Label the day count self-set.
5. **Pinned, supported versions**: the SDK major, runtime and API version each artifact pins, checked against the SDK support window and the API versioning policy.

With no sandbox (interview answer 4c), CI degrades to build, lint and type-check only. Mark every artifact "compiled, not run" until a sandbox exists, and make building one the first queue item. Apply the same label per flow when the sandbox exists but does not simulate it.

A hosted collection has no build: test it with a contract run against the sandbox on every API spec change.

See [references/freshness-and-upkeep.md](references/freshness-and-upkeep.md) for CI patterns, bot configurations, upkeep estimates and the cost evidence.

## 6. Write the archive rules

Archive on evidence, never on age alone. Microsoft auto-archives repos after two years of inactivity, but closing the bot issue resets the clock, so inactivity is a weak proxy for correctness. Use these triggers:

- Red past the SLA with no fix scheduled.
- No named owner for one review cycle, outside the adoption path.
- Superseded by a merged or newer artifact.
- Its SDK major or API version reached end of life.
- Low usage and red together: retire these first.

Archive with a README banner and successor link, remove the artifact from every surface, add a redirect to the canonical index, run a last secret scan, stop its bots and CI, then archive read-only. Never delete: forks, inbound links and coding agents keep reaching the repo. Follow the full sequence and banner text in [references/archive-and-redirect-playbook.md](references/archive-and-redirect-playbook.md).

## 7. Wire discoverability through one canonical index

Keep one machine-readable index of current samples in the samples org, owned by the portfolio owner: ID, type, job, languages, status, successor. Drive every surface from it:

- The docs pages that link each sample, and the gallery.
- A scaffold CLI (`<cli> samples create`) that writes test keys into `.env`; Stripe and Plaid both do this, removing the commonest first-run failure.
- GitHub topics and template-repository flags.
- The agent index: coding agents ingest archived and stale repos as readily as current ones, so the index must say what is current.

Two lists drift; one index read by every surface cannot.

## 8. Set the measurement plan

Tag every sample's API traffic with its sample ID, through the SDK's user-agent or app-info field, so calls trace back to the artifact. Then instrument four signals per artifact:

1. Invocations tagged with the sample ID (CLI scaffold, deploy button, template use).
2. First successful sandbox call from those credentials: time to first call.
3. Support tickets naming the sample.
4. CI pass rate over the quarter.

Stars and forks are vanity: report them, never decide on them. No vendor publishes clone-to-signup or deploy-to-activation benchmarks, so set your own baseline in the first quarter.

**Pass gate** for the strategy, iterate until it holds:

- 100% of kept artifacts have a named owner and a freshness contract.
- Kept upkeep hours sum within the interview capacity.
- Every archived artifact has a successor or an explicit "none" in the index.
- Every section of the strategy document approved.

## Security and licensing

- Ship `.env.example`, never `.env`; inject keys through the CLI, test mode only. Commits co-authored by one coding agent leaked secrets at about twice the public baseline (GitGuardian, a correlation), and agents copy keys they find.
- Run secret scanning and vulnerability alerts on every sample repo.
- License copy-paste samples MIT-0 or MIT so customers embed code without attribution review. AWS splits docs (CC BY-SA) from sample code (MIT-0) in one repo.
- When the platform handles regulated data (card numbers, health records), keep samples on the provider's hosted fields or tokenized flows, so a copied sample never pulls the developer into a heavier compliance scope.

## Failure modes

- **Coverage maximalism.** Ten languages times twelve scenarios looks thorough and rots within a quarter. "Publishing samples in six languages you barely maintain is worse than publishing samples in three languages you keep current" (Steve Arrants).
- **Campaign samples.** A sample shipped for a launch with no owner or CI is a future broken promise. No owner, no publish.
- **Reference-app sprawl.** A reference app that grows features becomes a second product. Cap it to the one pattern it teaches.
- **Silent deletion.** Deleting repos breaks forks, links and agent answers. Archive with a banner and a redirect.
- **Inactivity as health.** A repo with recent commits can still be red. Trigger on CI state, not activity.
- **Playground without a sandbox.** An embedded playground against live services leaks cost and data. Build test mode first.

## Invocation examples

- "We have 23 sample repos across 8 languages and half fail CI. What do we keep?"
- "Should we build a reference app or more quickstarts for our new payouts API?"
- "Design our samples gallery and deploy-button templates."
- "Write the archive policy for our samples GitHub org."
