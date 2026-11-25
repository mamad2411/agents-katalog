---
name: security-audit-runner
description: Runs Cloudflare's security-audit skill in full audit mode from Claude Code. It builds each agent's prompt file from that skill's text, pulls each agent's JSON reply out of its transcript, and keeps the coverage ledger, findings, agent-call budget and NEEDS-VALIDATION.md. Use it together with `security-audit` when the user asks for a full, end-to-end or report-producing security audit or pen test of a codebase. For a security question or a focused review, use `security-audit` alone.
---

# Security audit runner

[Cloudflare's `security-audit` skill](https://github.com/cloudflare/security-audit-skill) (MIT) supplies the method: phases, prompts, schemas, validators. It is a dependency, installed separately, and its files decide every rule. This skill is the parent-side tooling for its full audit mode in Claude Code. `scripts/audit_runner.py` reads the installed skill at run time, copies its blocks into prompt files verbatim, checks each reply against the contract its prompt gave, and writes the parent-owned run files. It was tested against `security-audit` at commit `c1c8a8c`. If a later version renames a heading, the script stops and names the missing anchor; it never guesses.

Requirements: Python 3.9+, and `node` for the skill's two validators. Below, `R` is `python3 -I <this skill's folder>/scripts/audit_runner.py` and `RUN` is the run's output directory. `R <command> -h` lists each command's options.

## Rules the run depends on

- **Replies stay out of context.** Prompts run to tens of kilobytes, so each agent gets one line: the `agent_prompt` that `R prompt` prints, which tells it to read its prompt file. Launch every agent in the background. Its completion notice names its transcript, `.../tasks/<agentId>.output` (a JSONL symlink). Pass that path to `R extract` and never open it yourself. Read a `result.json` only where a step below says so.
- **A bad reply is discarded, never repaired.** `extract` checks each reply against its role's contract and its schema branch, runs `validate-findings.cjs` on any record, and on any error saves the raw text as `discarded-reply.txt` and marks the call discarded. A code fence or a word of prose around the JSON counts as an error. A real verifier once put a field beside `record` and added a stray brace; both are caught here. The fix is a fresh agent under a new ID, so leave room in the budget for a re-run.
- **Validate early.** `apply-hunter` checks each hunter result as it stands: paths must already be repository-relative, and each candidate must pass its schema branch and `validate-findings.cjs` (a trace with two `sink` entries fails it). A unit whose result or candidate fails goes back to `planned` for a fresh hunter. Every ledger and findings write runs the skill's validator first and saves nothing on failure; without `node` the script refuses to save.
- **Fresh IDs.** Every agent ID is lowercase, used once, and never the ID of an agent that hunted, verified or rewrote the same candidate. The script refuses a reused or dependent ID.
- **Models.** Reconnaissance and hunters run on Sonnet. Critics and verifiers run on Opus. Use `subagent_type: general-purpose` and the `model` that `R prompt` prints. Reconnaissance, critics and record verifiers are the skill's read-only `research` role, and only their prompts keep them from writing.
- **macOS runs are source-only.** macOS cannot enforce the skill's sandbox controls, so `init` refuses `--sandbox` there. Prompts then forbid target code, and only `source` checks count.

## Steps

1. **Confirm full audit mode.** Use it only for the requests `security-audit`'s SKILL.md names. If the request could be guidance, ask that skill's one focused question. Settle the profile (`quick`, `standard` or `deep`), any scope paths and any budget with the user. Read `security-audit`'s SKILL.md now.
2. **Start the run.** `R init [RUN] --target <repo> --profile <p> [--budget N] [--scope path ...] [--prior <earlier run> ...] [--skill-dir <dir>] [--sandbox "<how target code is confined>"]`. The skill defaults to `~/.claude/skills/security-audit`, and `RUN` defaults to `~/security-audit-skill/<repo>/run-<N>`. Pass `--sandbox` only for a sandbox that enforces every control in their SKILL.md. When the budget cannot fund 4 reconnaissance calls, the critics and one verifier, `init` refuses: ask for a larger budget, a narrower scope or another profile.
3. **Reconnaissance.** For each of `1a 1b 1c 1d`: `R prompt recon RUN r-<x> --agent <x>`, then launch it. A focused agent takes `--text-file` with your own prompt. As each finishes, run `R extract RUN r-<x> <transcript>` and read its `result.md`. Write `RUN/architecture.md` from the four results under RECONNAISSANCE.md's cap.
4. **Seed the ledger.** Write a spec (see [Seed spec](#seed-spec)) and run `R seed RUN spec.json`. It derives each `coverage_id`, checks every block reference against the skill files, and fails on any duplicate. For each unchanged prior `confirmed` or still-blocked `needs_validation` record, run `R carry RUN --prior-findings <file> --fingerprint <fp> --unit <coverage_id>` against its planned unit.
5. **Hunt one wave.** `R budget RUN` prints `hunters_affordable`. Take units in HUNTING.md's priority order. For each hunter: `R assign RUN h-<name> <coverage_id> ...`, then `R prompt hunter RUN h-<name>`, then launch. As each finishes: `R extract RUN h-<name> <transcript>`, then `R apply-hunter RUN h-<name>`. `assign` refuses a hunter the budget cannot fund before it touches the ledger, and `R unassign RUN h-<name>` frees units whose prompt was never built. Units the budget cannot reach get `R defer RUN --reason budget_cannot_reserve_critics_and_validation <coverage_id> ...`. Each `uncovered` entry a hunter returns lands in `uncovered.json` and in the critic's prompt. Seed it as a unit for the next wave, or in `quick` as `deferred` with a reason.
6. **Merge shared root causes.** When two fingerprints are one root cause, run `R merge RUN <keep> <drop> --reason "..." [--lead <fp with the strongest trace>]`.
7. **Critic.** `R prompt critic RUN c-<n>` (add `--final-clean` for that pass in `standard` and `deep`), launch it, `R extract`, then read its `result.json` and judge each proposal. `R apply-critic RUN c-<n>` accepts every missing unit unless told otherwise: `--reject N=reason`, `--out-of-scope N=reason`, `--keep-closed <coverage_id>=reason`. Pass `--refs` with source-derived `canonical_refs` for each accepted unit, because refs derived from the critic's labels are weaker. A `quick` run records accepted and reopened units as `deferred` with `quick_profile_final_critic`. In `standard` and `deep`, planned units mean another wave from step 5. A clean post-wave critic is followed by a final-clean critic.
8. **Verify candidates.** For each `unvalidated` candidate, in fingerprint order: `R prompt verifier RUN v-<n> --fingerprint <fp>`, launch, `R extract`, then `R apply-verifier RUN v-<n>`. This rewrites `findings.json`. After a discard, re-run with a fresh ID when the budget allows. Otherwise stop and finish incomplete with `validation_budget_exhausted`. A verifier that returns a new fingerprint changes nothing until you decide. `--different-root-cause` adds its record as a new candidate, and both fingerprints then need a fresh verifier.
9. **Verify final records** (`standard` and `deep`; in `quick` the step 8 verifier already did this). For each `confirmed` and `needs_validation` record: `R prompt record-verifier RUN r-<n> --fingerprint <fp>`, launch, `R extract`, then `R apply-record-verifier RUN r-<n>`. A material replacement waits for another fresh record verifier.
10. **Close, then report.** `R status RUN` shows the counts, the spend and any open work. Run `R finish RUN`, or `R finish RUN --incomplete <reason>`, which removes disputed records and marks each unvalidated candidate on its units. Then run `R validate RUN` (both codes must be 0) and `R needs-validation RUN [--order fp,...]`. Write `REPORT.md` and `FINDINGS-DETAIL.md` yourself from the final records, under VALIDATION-AND-REPORTING.md's Phase 6.

## Cost

Count before step 3 and tell the user. `budget` reserves the critics and validation for you, and its `hunters_affordable` is what `assign` will allow.

| Profile | Agent calls |
| --- | --- |
| `quick` | 4 reconnaissance + one per hunter + 1 critic + 1 verifier per candidate |
| `standard`, `deep` | 4 reconnaissance + hunters per wave + 2 critics per wave + 2 verifiers per candidate |

Add one call for each discarded reply that is re-run.

## Seed spec

A JSON array, one object per unit:

```json
{
  "surface": "GET /items", "boundary": "Item owner check", "subsystem": "API", "attack_class": "Access control",
  "refs": {"surface": "src/routes.js#GET /items", "boundary": "src/authz.js#requireOwner", "subsystem": "src"},
  "starting_paths": ["src/routes.js"],
  "ordinary_block": "ATTACK-CLASSES.md#Access control",
  "companions": {"WEB-PROTOCOL-AND-AUTH.md": ["<class name as written in bold>"]},
  "excluded_blocks": [{"block": "FILE.md#<class>", "reason": "the source fact that excludes it"}],
  "priority": 1, "rationale": "lowest-trust entry surface"
}
```

`companions` expands to that file's `Core discipline`, the named classes, `Universal moves` and `Validation rules`. Use `companion_blocks` instead for an explicit list. `refs.attack_class` defaults to the ordinary block, else the first companion class. A `quick` run fixes the subsystem ref to `profile/quick/all-in-scope-subsystems`, so omit `subsystem` there. `status` may be `out_of_scope`, `not_applicable` or `deferred` with a `reason`, and `prior_status` and `lifecycle` (with `refs.lifecycle`) follow RECONNAISSANCE.md.

## Run files

The skill's own: `run-metadata.json`, `architecture.md`, `coverage-ledger.json`, `findings.json`, `NEEDS-VALIDATION.md`, `REPORT.md`, `FINDINGS-DETAIL.md`. The runner adds `agent-calls.json` (every call, its role, model and status), `candidates.json` (proposals, merges and verifier decisions by fingerprint), `uncovered.json`, `critic-log.json`, and `agents/<id>/` with `prompt.md`, `result.json` or `discarded-reply.txt`, `scratch/` and `artifacts/`.

In a sandboxed run, list each file an agent may keep with `--allow-artifact <scratch path>=<bytes>` when building its prompt. After its sandbox exits, `R promote RUN <id> <scratch path>` copies the file into `artifacts/` with descriptor-relative, no-follow opens and the size checks. A `local` check counts only when its artifact was promoted this way. The script opens the scratch and artifacts roots at promotion time, not before the agent runs. That matches the skill's retained-descriptor rule only while nothing but the parent can write `agents/<id>/`.
