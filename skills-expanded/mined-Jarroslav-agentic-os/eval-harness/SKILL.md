---
name: eval-harness
description: Scaffold a two-layer eval framework — deterministic contract checks plus optional LLM-judge behavioral cases — for every Claude Code skill (and agent file) in a repository. Invoke when the user asks to add evals, regression guards, or skill tests, to wire eval automation into hooks/CI, or to extend an existing evals.json setup. Not for: writing ordinary unit tests or merely running an eval suite that already exists.
---

# Eval Harness

Bootstrap repo-wide evaluation for skill and agent instruction files. Two layers, one spec file per target.

| Layer | Mechanism | Failure class caught | Cost profile |
|---|---|---|---|
| Contract | Code-only checks, zero LLM calls | Structural rot: missing files, edited-away instructions, oversized bodies, broken helper scripts | Cheap — safe to run on every commit |
| Judge | Candidate model executes the skill against a case prompt; judge model grades output vs assertions | Behavioral drift: skill still loads but no longer behaves as designed | Model calls — on demand or scheduled |

> Both layers exist because they detect different failure classes. Route structure to code checks and behavior to the judge: never regex-grade prose, never burn a model call to confirm a file exists.

Both layers read the same spec, `eval/evals.json`, colocated inside each target's directory. A spec with contracts and no behavioral cases is valid. Each judge case runs N repetitions, so flakiness surfaces as a pass rate instead of a binary verdict.

> **`eval/` here is not `evals/` in the agentic-os marketplace repo**, and the
> near-collision is deliberate to name rather than rename. This skill writes
> `<target>/eval/evals.json` into *your* repo. The marketplace repo's own CI
> (`tests/lib/check-skill-contract.py`) separately requires `<skill>/evals/evals.json`
> for the skills it *ships*. Different scope, different owner, no conflict —
> except when you point this skill at the marketplace repo itself, where you
> will end up with both. In that one case keep the plugin's `evals/` as the
> shipped contract and treat the generated `eval/` as local scaffolding.

Blast radius: **R2** — this skill writes harness code, spec files, and config into the repo. Judge runs place outbound model calls; automation wiring is opt-in and confirmed first. It never creates real credential files and never gates merges on paid model runs.

## Inputs

Collect during the interview phase. Ask only what the repo has not already answered; confirm inferences rather than re-asking.

| Input | How to obtain |
|---|---|
| Harness language | TypeScript (Node 18+), Python (3.10+), or both. Always ask explicitly — repo signals (package.json vs pyproject.toml) shape the recommendation, never the decision. Scaffold one language unless the user requests both. |
| Provider backend | One of the three below. Only the choice is needed at setup; credentials load from `.env` at run time. |
| Candidate + judge model ids | Always user-supplied — the same model carries different ids per provider or gateway catalog. If the user is unsure, point them at their provider's model-list endpoint. Candidate and judge are configured independently. |
| Skills root | Templates default discovery to `.claude/`; repoint the root env var/constant if skills live elsewhere. |
| Automation opt-in | Hooks/CI only on explicit yes, or when CI already exists to extend. |

### Provider backends

| Backend | Model id shape | Notes |
|---|---|---|
| Anthropic via Portkey gateway | Fully-qualified `@provider-slug/model` | A bare model name returns a 400 about a missing provider header |
| OpenAI-compatible chat endpoint | Bare served-model name | Covers local servers: vLLM, Ollama, LM Studio |
| Native Anthropic SDK | Plain vendor model id | |

> Grading is reasoning-heavy work: put the judge on a standard or premium tier. The candidate can run on an economy tier when the goal is cheap smoke coverage.

Full env vars, endpoints, and SDK details: `references/judge-providers.md`.

## Operating steps

Work in five phases. Do not skip ahead.

1. **Interview.** Resolve the inputs above using the decision rules stated with each.
2. **Repo exploration.** Discover targets: any directory containing a SKILL.md, searched under common roots, excluding `node_modules`, dot-directories, and generated output dirs. Markdown agent definitions under agents-style directories are targets too and are treated identically. Read every target you will write a spec for — in full.
   > Grounding rule: every contract string and every behavioral assertion must derive from an instruction file you actually read. A placeholder scaffold aimed at an imagined skill is forbidden. If you cannot perform discovery, stop and state the exact commands the maintainer should run instead.
3. **Scaffolding.** Copy the harness templates for the chosen language(s) from `assets/typescript` and/or `assets/python`, following the file lists and edits in `references/typescript.md` / `references/python.md`. Write one `eval/evals.json` per target. Repoint the discovery root if needed. Augment existing setups — never overwrite; an `evals.json` that already holds real cases must never be clobbered. Default layout is per-target spec dir plus a shared harness at repo root, but if the repo already has an eval convention, match it — consistency wins.
4. **Verification.** Install dependencies (Python: prefer a venv — system interpreters are often externally managed; add an empty package init file so the runner works both as loose pytest modules and as a package). Run the contract layer to green. Attempt the judge layer only if credentials are present. Then baseline-audit the assertions (below).
5. **Automation (opt-in).** Wire hooks/CI per the hard rule below, from the copy-paste material in `references/ci.md` and the hook script in `assets/ci`.

## Writing the spec

Schema in full, with a worked example: `references/eval-spec.md`. An example spec JSON ships under `assets/`.

### Contract fields

| Field | Validates |
|---|---|
| Required file paths | Files the skill cannot function without still exist |
| Literal substrings | Load-bearing instruction text is still present verbatim |
| Regex patterns | Instructions whose wording legitimately varies |
| Size ceilings | Body under 500 lines; frontmatter description under 1000 chars |
| Script checks | Each bundled helper compiles; optional smoke run with argv, allowed exit codes, expected output substrings |

> Pin only what genuinely must hold. A contract that fails on harmless rewording trains maintainers to ignore failures.

### Behavioral case fields

Per case: a realistic prompt with inputs inlined; human-readable expected-output prose (documentation only — not graded); optional per-case file inlining; named assertions, each phrased as one objectively judgeable behavior. Spec level: a skill name matching the target's frontmatter, plus optional context files inlined into every case.

Assertion quality bar:

- A good assertion fails when the skill is absent or broken.
- Target the rules, formats, gates, and fallbacks this skill specifically enforces — not generic model competence.
- 2–4 strong cases beat many weak ones.
- Single-turn constraint: the judge sees only final text and cannot observe tool use. For skills that write files, credit clearly stated intent.

### Baseline audit

Rerun every case with the skill body removed; any assertion a bare model still passes is non-discriminating — flag it for rewrite. For doc-heavy skills, a stricter variant also strips inlined reference docs. The audit roughly doubles call volume: treat it as an authoring step, never CI.

## Env hygiene

- Commit only an example env file with placeholder values.
- Never write a real secret to disk — even one pasted into chat; advise rotating it instead.
- Ensure the real env file and generated report directories are git-ignored.

## Automation rules

Hard rule — state it explicitly every time you wire automation: **hooks and required CI checks run the contract layer only.** The judge layer may appear in CI solely as a separate non-required job, manual or scheduled, reading credentials from the platform's secret store.

- Local hook: pre-commit by default, pre-push for slow suites; keep the standard bypass flag working; install via a repointed hooks path.
- CI: GitHub Actions or GitLab CI on pull/merge requests. Match existing workflow conventions and confirm with the user before adding CI files.

## References map

| Open | When |
|---|---|
| `references/eval-spec.md` | Writing or reviewing any `evals.json` — full schema plus worked example |
| `references/judge-providers.md` | Configuring a backend — env vars, endpoints, SDKs, model-id formats |
| `references/typescript.md` | Scaffolding TS — code-validation runner, two Vitest suites, judge runner module; npm scripts `test` (vitest) and `eval:llm` |
| `references/python.md` | Scaffolding Python — equivalent file set; run modes: pytest over modules and module-mode judge runner |
| `references/ci.md` | Wiring hooks or CI — copy-paste material |
| `assets/typescript`, `assets/python` | Harness template sources |
| `assets/ci` | Pre-commit hook script |

## Handoff

Close with a summary: per-target spec counts, contract and judge pass results, assertions flagged weak by the baseline audit, and the exact rerun commands.

## Non-goals

Single responsibility: scaffold and verify the eval framework — nothing else. Out of scope: authoring unrelated unit tests, merely executing an eval suite that already exists, creating real credential files or handling live secrets, gating merges on paid LLM runs, and grading multi-turn tool execution.
