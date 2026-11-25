---
name: rl-protect-audit
description: "Deep supply chain security audit of an existing project. Runs the full rl-appsec pipeline: assessor → triager → investigator → remediator, with phase gates between each stage. TRIGGER when: the user asks to audit, assess, or review a project directory's installed dependencies for supply chain risk. SKIP when: the user is installing, adding, or updating a package — use rl-protect-scan for that. SKIP when: the user asks about a single package or an existing report — use rl-protect-scan or rl-protect-interpret for that."
---

This skill audits the supply chain security of an **existing project directory** — it assesses what is already installed, not what is about to be added. For pre-install package gating, use `rl-protect-scan` instead.

Run the full pipeline on the project directory the user specified. Follow the steps below in order. Never run two agents simultaneously — sequential execution prevents concurrent writes to the shared remediation plan.

## Step 1 — Locate plan.py

```
Glob: **/rl-appsec-agent/scripts/plan.py
```

**`{plan.py}` is a placeholder throughout — substitute the absolute path returned by Glob.**

All pipeline artifacts live under `{project_dir}/.rl-protect/` (in categorized subfolders: `plan/`, `reports/`, `cache/`, `tmp/`). The remediation plan is always written to `{project_dir}/.rl-protect/plan/remediation-plan.db`. Use this as `{plan_path}` in all phase-gate checks below.

---

## Step 2 — Run the assessor

Spawn `rl-appsec-assessor`. Pass the project directory and any context the user provided.

The assessor auto-discovers scan targets with `find-manifests.py` and **prefers lock files** over
source manifests (scanning a lock at `release,transitive` — `release` alone under-scans even a lock,
but on a lock the transitive walk is cheap+exact) — you don't need to point it at a specific manifest.

Wait for the assessor to complete before proceeding.

---

## Step 3 — Phase gate: check for untriaged CVEs

```bash
python {plan.py} findings --plan {plan_path} --untriaged
```

- Empty array → skip to Step 5.
- Non-empty → proceed to Step 4.

---

## Step 4 — Run the triager

Spawn `rl-appsec-triager`. Pass the plan path and project directory.

Wait for the triager to complete before proceeding.

---

## Step 5 — Phase gate: check for uninvestigated malware

```bash
python {plan.py} findings --plan {plan_path} --uninvestigated
```

Filter the result for entries where `type` is `"threats"` or `"malware"`.

- None → skip to Step 7.
- Any found → proceed to Step 6.

---

## Step 6 — Run the investigator

Spawn `rl-appsec-investigator`. Pass the plan path and project directory.

Wait for the investigator to complete before proceeding.

---

## Step 7 — Explore alternate versions

Run the alternate-version explorer so the report can show, per package, which versions resolve its
findings and how far each package is behind latest. It runs here — after triage (and investigation)
so dismissed findings are gone, and before remediation.

```bash
python {explore_versions} --plan {plan_path} --actionable
```

`--actionable` scopes the (expensive) version_options exploration to **triage survivors** — the
packages that still have an OPEN/exploitable CVE an upgrade could resolve — so it never scans upgrade
versions for the packages triage already cleared as not-reachable/accepted/resolved (usually the large
majority). `op_risk` (how far behind latest) is still computed for **every** package, so the staleness
view is unaffected. This is what prepares the remediator: the packages it will act on are exactly the
ones now carrying scan-validated `version_options`.

`{explore_versions}` is from `python {plan.py} locate` (key `explore_versions`). It scans temp
manifests with version expressions (no registry APIs), diffs via `diff-behavior.py`, and writes
`version_options`/`op_risk` into the plan. It is deterministic and cached, so re-running is cheap.
Network access to the package registry (through rl-protect's resolver) is required; if the scans
cannot reach it, note that version exploration was skipped and continue. Running this before
remediation also lets the **remediator pick its upgrade target from `version_options`** (the smallest
version that resolves the findings, scan-validated) rather than re-deriving it.

---

## Step 7b — Triage candidate-version deltas (only if any exist)

The explorer applied the installed version's decisions to every alternate-version candidate so they are judged by the same rules (a not-imported package's candidates are fully cleared package-wide; same-CVE findings inherit our verdict). The **only** thing it can't transfer is a **genuinely-new CVE** a candidate introduces that the installed version never had — those stay unevaluated and are listed in each candidate card's `needs_triage`. Left alone, such a candidate shows a raw scanner verdict the user can't compare against.

Check whether any deltas remain:

```bash
python {plan.py} version-options --plan {plan_path}
```

If **every** candidate's `card.needs_triage` is empty, skip this step — the common case. If any is non-empty, spawn `rl-appsec-triager` **in candidate-delta mode** (its Step 8): instruct it to triage the candidate-version deltas in `needs_triage`, recording each verdict with `plan.py triage-version`. This is reachability-only — no rl-protect re-scan, no manifest change — so every version ends up evaluated equally and the user can judge an upgrade before taking it.

---

## Step 8 — Remediation gate

Only spawn `rl-appsec-remediator` if the user explicitly requested fixes. If the request is ambiguous, ask before proceeding — the remediator edits manifest and lock files.

If remediation was requested, spawn `rl-appsec-remediator` with the plan path and wait for it to complete.

---

## Step 9 — Report

Summarize: which stages ran, which were skipped and why, and the overall verdict from the final plan state.

```bash
python {plan.py} findings --plan {plan_path}
```

---

## Step 10 — Offer the interactive report (optional)

The audit produced findings the user may want to triage, suppress, or accept by clicking rather than by typing. The `rl-protect-run-report` skill opens the HTML report and wires its action buttons back to this session.

- If the user **already asked** for an interactive/clickable report (or to "open the report"), invoke `rl-protect-run-report` for `{project_dir}` now.
- Otherwise, **offer it in one line** and invoke it only if they say yes — e.g. *"Want me to open the interactive report so you can triage/suppress/accept findings by clicking? (starts a local bridge + a watch loop)"*.

Do not invoke it unprompted: it auto-opens a browser and starts a polling loop that spends some idle tokens, so it needs the user's go-ahead. If there were no findings at all, skip this step.
