---
name: cg-scan
description: Run a static (Tier 0) ClaudeGuardIL security scan of the current project — the engine computes facts, the grader assigns every severity, the domain auditors review only what the rules could not decide. Use when the user types /cg-scan or asks to scan, audit, or security-check the codebase without touching a live server.
argument-hint: "[path] [--domain web|ai-llm|supabase-firebase|android|ios|desktop|backend-iac|ci-cd]"
allowed-tools: [Read, Glob, Grep, Bash]
user-invocable: true
---

# /cg-scan — static security scan (Tier 0)

Run a safe, read-only static audit. No network, no credentials. This is the default entry point.

Arguments: `$ARGUMENTS` — optional path to scan (default: repo root) and an optional `--domain`
filter. `--domain` narrows which auditors you dispatch and which catalogs you read; it does **not**
narrow the grader, which always grades the whole model so coverage still adds up.

## The pipeline

```
Engine → Facts → Grader → Findings → Auditors add reviewer findings → Report
```

| Stage | Who | What it is allowed to do |
|---|---|---|
| Engine | `scripts/project_model.mjs` | Emits **Facts**: routes, tables, env vars, LLM sites, clients, the client/server boundary. Has no opinion about danger. |
| Grader | `scripts/grader.mjs` | **The single authority on severity and confidence.** Turns Facts into Findings and builds the coverage ledger. |
| Auditors | `web-auditor`, `ai-auditor`, `mobile-auditor`, `infra-auditor` | Add findings with `provenance: 'reviewer'` and `evidence: 'judgement'` — capped at confidence `likely`, never `confirmed`. |
| Verifier | `finding-verifier` | **Refutes only** — removes a finding by naming the fact that disproves it. It never edits a confidence, never lowers a severity, never adds findings. |
| Report | you | **Render what the grader produced.** |

**You do not grade.** Not while reading a file, not while writing the report, not "just this once
because it looks worse than P2". Severity being reproducible — the same repo grading the same way
every time — is the entire public claim of this tool. The moment you re-derive it from a check
document, two runs of `/cg-scan` on one repo disagree, and every conversation about a finding turns
into a conversation about the model.

Concretely:

- **Severity and confidence come from `grader.mjs` and nowhere else.** Confidence is a pure
  function of evidence strength (`definitive` → `confirmed`, `strong` → `likely`, `weak` →
  `needs-review`, `judgement` → `likely`). Never hand-set it, never "upgrade" one.
- **Auditors add judgement findings**, which is the work no rule can do — auth that is present and
  does not enforce, ownership filtered on the wrong column, a workflow step that can be skipped.
  They are capped at `likely` because no amount of reading is a proof.
- **You render.** Titles, ordering, coverage, both languages.

The policy itself is written out in the `claudeguard` skill's `references/methodology/grade.md` and
`references/severity-model.md`. Read them to *understand* a grade, never to *produce* one.

## Steps

1. **Build the model (Facts).**

   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/project_model.mjs <path> > cg-model.json
   ```

   Read it yourself: `framework`, `artifacts` (manifests, Dockerfiles, workflows, migrations),
   `boundary`, `graphCoverage`, `limits`. The auditors need parts of it too.

2. **Grade it (Findings + coverage).**

   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs --model cg-model.json > cg-graded.json
   ```

   `--model` reuses step 1. Passing a repo path instead (`grader.mjs <path>`) makes the grader run
   the engine itself — the one-command form when you do not need the model separately.
   `project_model.mjs <path> | grader.mjs` also works if you would rather not write files.
   Put the two JSON files in a scratch directory outside the user's repo and clean them up: a scan
   should not leave a file listing their env var names sitting in a working tree.

   The result has: `verdict`, `counts`, `findings`, `coverage`, `verifyQuery`, `limits`.

   If the user has accepted specific subjects as known-and-intended, pass `--allowlist <file>` (a
   JSON file with a `subjects` array of subject ids). Allowlisted subjects stay in the coverage
   ledger under `allowlisted` rather than vanishing — an accepted risk is still a risk somebody
   accepted, and it has to remain visible.

   **Business-logic intent.** The grader reads `claudeguard.intent.yml` from the scanned repo root
   automatically when it is there, and is silent when it is not — a missing optional config is a
   coverage fact, never a finding. Check `result.businessLogic.status`: `confirmed` means the audit
   ran against the author's stated ownership rules; `assumed` means it ran against a model guessed
   from column names, and every conclusion in that section is worth less. When it is `assumed`, tell
   the user (in step 9) that `/cg-intent` turns the guess into a review — do **not** write the file
   yourself; proposing and confirming are two different acts, and the confirmation is theirs.

3. **Detect the stack and pick catalogs.** From `model.framework` and `model.artifacts`, plus a
   Glob/Grep pass for anything the engine does not model. That leftover list is short: manifests,
   plists, Dockerfiles, compose files, Terraform, GitHub workflows and Firebase rules are all
   parsed into fact blocks and graded by rules now; what the engine sees but does not grade
   (Electron `webPreferences` internals, Kubernetes manifests) arrives as `undeterminable` rows in
   `coverage.ungradedSurfaces` rather than silently. Read the matching
   catalogs in the `claudeguard` skill's `references/checks/`. Those catalogs describe what a
   vulnerability class **looks like**. They are not a work list and they are not a severity table —
   the grader's `coverage.<set>.undeterminable` rows are the work list.

4. **Optional: real scanners.** Run `node ${CLAUDE_PLUGIN_ROOT}/scripts/detect_tools.mjs` and, for
   any tool it reports as available, use the matching adapter: `run_gitleaks.mjs` (secrets, falls
   back to regex/entropy), `run_semgrep.mjs` (SAST), `run_dep_audit.mjs` (deps). Do **not** install
   anything; you may offer the install command.

   **Snyk**, if `detect_tools.mjs` reports it **installed AND authenticated** (both booleans true).
   Run it *in addition to* `run_dep_audit.mjs`, never instead — dropping npm-audit would silently
   lose the `scan:dependencies` row the day a token expires. Its reachability and dataflow are the
   two things a regex cannot have, so the grader can raise a dependency finding to `likely` on a
   reachable path.

   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/run_snyk.mjs <path> > cg-snyk.json
   ```

   **Consent, stated as a prohibition:** *never pass `--code` on your own initiative.* `snyk code`
   (SAST) **uploads the user's source to Snyk's cloud** — everything else runs locally. Ask exactly
   one plain HE+EN question, safe option first, and pass `--code` only on an explicit yes. `SNYK_TOKEN`
   being present is **not** consent; a prior run is not consent. If `claudeguard.scope.yml` already
   carries `snyk.code_scan_uploads_source: true`, the adapter reads it itself and no flag is needed.

   Feed their output to the grader — do not grade it yourself:

   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs --model cg-model.json \
     --secrets cg-secrets.json --sast cg-sast.json --dependencies cg-deps.json \
     --snyk cg-snyk.json > cg-graded.json
   ```

   The grader owns the severity for scanner findings too, and it is deliberately sceptical: a
   committed **value** for a privileged credential is a `confirmed` P0 (a value match is what LAW 3
   allows to justify one), but an often-public key like a Google Maps key is held to `needs-review`,
   a semgrep result is never better than `likely`, and a dependency CVE is `needs-review` because
   reachability was not checked. Crucially, whether each scanner could run **properly** is recorded
   in `coverage.scanCoverage` — a fallback regex scan that never read git history, or a missing
   semgrep, shows up as an `undeterminable` row, so a shallow scan can never masquerade as a clean
   one.

5. **Dispatch the domain auditors.** Launch them in parallel, each with the grader's JSON. Their job
   is the judgement-level work the rules cannot do, and their work list is the coverage ledger:

   | Auditor | Walks |
   |---|---|
   | `web-auditor` | `coverage.routes.undeterminable`, `coverage.supabaseClients.undeterminable`, `coverage.nextConfigKeys.undeterminable` |
   | `ai-auditor` | `coverage.llmSites.undeterminable` |
   | `infra-auditor` | `coverage.sqlFunctions.undeterminable`, `coverage.tables.undeterminable`, `coverage.dynamicTableRefs` |
   | `mobile-auditor` | `coverage.mobileArtifacts.undeterminable` and `coverage.exportedComponents.undeterminable` — the grader now decides the definitive manifest facts (debuggable, cleartext, exported components, iOS ATS); the auditor takes the rest, such as secrets in resources and logic in the source the manifest points to |

   The `ciWorkflows`, `iacFiles` and `firebaseRules` sets are decided by rules (`pass`/`fail`), so
   they add no undeterminable rows of their own. `coverage.ungradedSurfaces` is the opposite —
   every row in it is `undeterminable` by construction, because it holds what the engine saw and
   no rule grades (see `references/methodology/grade-or-declare.md`). Route each row to the
   matching auditor: Electron and Kubernetes subjects to `infra-auditor`, route-framework gaps to
   `web-auditor`.

   An `undeterminable` row is not a shrug. It is a rule refusing to print a checkmark it cannot
   back: "the handler mentions `getUser`, but nothing proves the result gates anything." That is
   precisely where a human has to look, and it is why the auditors get a list instead of a repo.

   Every auditor must return its coverage block (how many subjects it reviewed, and every subject
   it skipped with a reason). An auditor that reviewed 4 of 27 routes and stays quiet about the
   other 23 has produced a false all-clear.

   **Each reviewer finding must carry the exact `subject` string from the coverage row it came
   from** (e.g. `route:pages/api/orders/[id].ts`, copied verbatim). The subject is the join key
   between the grader's inventory and the reviewer's findings; a finding whose subject the grader
   never enumerated is flagged `unanchored` in the merge step — which is right for a genuine
   hallucination, but is pure self-inflicted noise when it was only a paraphrased path.

6. **Merge and validate the reviewer findings.** Collect the auditors' findings into one array and
   run them back through the grader, which is the ONLY thing that lets them into the report:

   ```bash
   node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs --model cg-model.json --reviewer cg-reviewer.json > cg-final.json
   ```

   The grader enforces the same laws on agent output that it enforces on its own rules: provenance
   is forced to `reviewer`, evidence is capped at `judgement` (so confidence is `likely` and a
   reviewer finding can **never** be `confirmed`), a name-only P0 is rejected, and a malformed
   finding is dropped with a reason. The result carries `reviewer` (accepted/rejected/unanchored
   counts), `rejected` (each drop with its reason), and `reviewerNotes` (each correction). Read
   those: a wall of `unanchored` notes means the auditors are paraphrasing subjects instead of
   copying them, and a `rejected` entry is an auditor that broke the schema. The headline verdict is
   guaranteed identical before and after this merge — that is the property that makes it safe to let
   an LLM contribute to the report at all.

7. **Verify.** Run `finding-verifier` (or do the pass yourself) against the merged list from step 6
   — rule findings and reviewer findings together. It returns **refutations only**: a finding is removed by
   naming a specific fact at a specific location that makes it false. "Seems intentional" is not a
   refutation. A finding it cannot refute survives *unchanged* — not "verified", not promoted,
   because confidence is a function of evidence and re-deriving it here would mean the same repo
   grades differently depending on how hard someone squinted.

   Refuting a `confirmed` finding is a different event: `confirmed` came from `definitive` evidence,
   so a genuine refutation means the *rule* is defective and mis-grades every repo it runs on. Those
   come back flagged `engine_defect` and must be reported, not quietly dropped.

   The catalogue of known false positives is
   `${CLAUDE_PLUGIN_ROOT}/skills/claudeguard/references/methodology/false-positives.md` — each entry
   is a mistake this tool actually made and names the fact that refutes it.

8. **Report.** Render with the `claudeguard` skill's `references/report-template.md`, bilingual
   Hebrew + English prose, code and identifiers in English only.

   - **Open every finding with a plain-words line, before the technical prose.** The audience is
     non-expert, so the first thing they read must be jargon-free. Look the finding's `id` up in
     `references/plain-language/findings.md` and print its `HE` + `EN` text as the
     `בפשטות / In plain words` line. No entry for an id → write a one-sentence plain paraphrase
     yourself; never skip it. Point beginners to `references/plain-language/concepts.he.md` in the
     footer — it teaches the concepts (RLS, service_role, secrets) once, in plain Hebrew.
   - **Headline verdict = `verdict` from the grader, unchanged.** It counts **only** findings whose
     confidence is `confirmed` (`confirmedP0`, `confirmedP1`, `level`). Print the rule next to it so
     the number is not mistaken for a total.
   - **Below it, quieter:** the `likely` and `needs-review` findings, with each one's `assumption`
     — the single thing that would have to be true for it to be a false positive. Severity is
     uncapped there on purpose: an unproven P0 is still printed as a P0 and sorted to the top of
     that section, it just does not turn the badge red. Discounting it twice — softening the P0
     *and* marking it unconfirmed — would bury it where nobody looks.
   - **Label provenance** on every finding: a rule proved it, or a reviewer thinks so. The two
     deserve different responses from the user.
   - **Render discovery coverage first, then analysis coverage — they are two different axes.**
     Discovery (`result.discovery`) is what the engine could *see*: files parsed vs skipped (with
     reasons), routes modeled vs only partially (`withUnknownMethods`), unresolved imports, and
     `schema.rlsVerifiable`. Analysis coverage (`result.coverage`) is how it *graded* what it saw —
     the pass / fail / undeterminable / allowlisted counts, which add up by construction. A report
     that shows only analysis coverage can look complete while the engine silently skipped half the
     repo, so discovery goes first. If `discovery.reconciles` is false, or `schema.rlsVerifiable` is
     false, say so loudly. See `references/methodology/discovery.md`.
   - If `verifyQuery` is non-null, hand it to the user verbatim — it answers the RLS question the
     repo could not, in about ten seconds against their own database.
   - Print `limits` from the model. A heuristic pass that hides its own blind spots is worse than
     one that names them.

9. **Offer next steps:** `/cg-harden` to generate the fixes, `/cg-fix` to apply the eligible ones
   (dry-run first), or `/cg-live` to observe a running target the user owns.

Every finding shows its `evidence.at[]` (`file:line`) so the user can check the work in their own
editor. If nothing was found, say so honestly and give the coverage numbers: a clean static scan is
not proof of safety, it is proof that nothing was proved.
