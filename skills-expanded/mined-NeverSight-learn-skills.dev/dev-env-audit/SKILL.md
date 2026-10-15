---
name: dev-env-audit
description: "Read-only audit of machine-level developer toolchains on macOS (zsh; degraded bash support). Inventories installed SDKs and installation channels for Python, Node, Java/JVM, Go, Rust, Ruby, Swift/Objective-C, PHP, Lua, Zig, Julia, Dart/Flutter, Erlang/Elixir, C/C++, and Git; detects conflicting version managers, stale shell setup, PATH differences across terminal/GUI/script scenarios (including path_helper), and incomplete or broken external-SSD cache relocation. Produces a health report and per-language migration plan based on authoritative/native managers while respecting sound existing setups. Use for whole-machine or single-language audits, SDK inventory, wrong/old command resolution, manager cleanup, PATH/shell conflicts, or cache-relocation checks. Never installs, uninstalls, edits config, or downloads; it only probes and gives reviewable commands for the user to run."
---

<!-- Ver 2026-07-19 16:00, by Claude Sonnet 5 -->

# dev-env-audit — Development Environment Audit

Read-only audit of the local development environment, producing a diagnostic report and migration suggestions against per-language best-practice baselines.
**This skill is entirely read-only**: scanning scripts and all commands you execute must not modify any files, must not install/uninstall anything, and must not download anything over the network. The report provides commands for the user to execute themselves.

## Design Philosophy (Overall Guidelines)

The following principles are the foundation for all judgments and recommendations in this skill. In case of any conflict during execution, this section takes precedence.
**When producing the report, the first section must begin with a 3–5 line summary of these principles** (at minimum including items 1, 3, and 5), and note: all diagnoses and suggestions are based on this philosophy; if the user disagrees (e.g., prefers to manage all languages with mise), the migration suggestions that follow will have limited reference value—align on the philosophy before discussing the plan.

1. **Only probe, analyze, and suggest; never execute.** The core function is a thorough understanding of the system's actual state plus reasonable recommendations; installation/uninstallation/config editing/networking are all off-limits. Change commands appear only in the report, to be executed by the user after confirmation.
2. **Separation of facts and interpretation.** The scan states only facts, never judges, nor hides any fact because it is “benign”; judgment rules are centralized in the references; the report interprets on top of complete facts.
3. **Use each language’s authoritative tool in its domain** (uv / fnm / rustup / rbenv / juliaup…), or one tool for a tightly coupled ecosystem (SDKMAN for JVM, asdf for OTP+Elixir). **Oppose the “one tool to rule all languages” approach**—do not endorse, do not recommend mise-like solutions.
4. **Official over third-party.** Where the language’s native mechanism can handle it (GOTOOLCHAIN, multi-Xcode with xcode-select), do not introduce extra tools; third-party tools must have clear irreplaceable value.
5. **Respect reasonable existing choices.** Equivalent tools (mise↔asdf, zigup↔zvm) that are working fine should not be swapped; the system default “unmanaged” is a legitimate state; cache relocation is optional, not an obligation—**the most dangerous state is half-relocated drift**.
6. **Effective values over configuration appearances.** Judgments are based on the actual location reported by the tool itself (environment variables can deceive), and cover three shell scenarios (interactive terminal / GUI App / script).
7. **Principled guidance, not fine-grained version control.** Focus on whether the toolchain structure is healthy, not on minor version number differences.
8. **No fabrication.** Commands in the report must originate from references; every command in references must pass the anti-hallucination checklist in `_template.md`.
9. **Support scope explicit: macOS; full support for zsh, degraded support for bash, no support for fish and other shells.** It is better to honestly state non‑coverage than to cover incorrectly.

## When NOT to use

- The user requests **direct execution** of migration/installation/uninstallation — this is outside the skill’s boundary. Produce the complete report first, then tell the user: the change commands in the report need to be reviewed one by one and executed by themselves (or after explicit authorization, a separate task can be handled).
- Project-level dependency problems (a repo’s node_modules / venv is broken) — this skill manages the machine‑level toolchain, not individual projects.

## Execution Flow (Four Phases)

All scripts are run with `zsh` (not bash—the scripts use zsh syntax). Script paths are relative to this skill’s directory.

### Phase 1 — Scope Detection (1 invocation)

```bash
zsh scripts/scan.sh
```

The output is a plain inventory: presence, paths, and one‑line version for each language / version manager / package manager, plus duplicate brew installations and PATH duplicates. **The inventory makes no judgments**; judgment rules reside in each language’s reference.

After reading the inventory, determine the scope:
- **First, look at the `login shell` section**. All PATH/init analysis in this skill assumes zsh; if it is not zsh, degrade accordingly and declare explicitly at the beginning of the report:
  - **bash**: tool existence, version, and cache‑relocation conclusions remain valid; the grep targets in references §2 already include `~/.bash_profile ~/.bashrc`, so init residue analysis is largely usable; however, probe‑path’s three scenarios are zsh‑oriented, so PATH scenario conclusions should note “measured by zsh rules; bash’s loading rules (login reads `.bash_profile`, non‑login reads `.bashrc`) differ—the user should map accordingly”.
  - **fish and others**: keep only existence/version/cache‑relocation conclusions; PATH and shell config analysis are stated as “not covered (this skill only supports zsh/bash configuration systems)”, and do not force any assumptions.
- Languages that exist → proceed to Phase 2 deep dive; if not present, skip (do not load its reference).
- Pay attention to entries like `(dir found, command not on PATH)` — a directory exists but the command is not on PATH, usually meaning “was installed but initialization code has been removed or still remains”, which is a key signal for Phase 2 investigation.
- Remember the full set of files listed in the `shell config source chain` section. If the user uses a centralized dotfiles framework (where `~/.zshrc`/`~/.zprofile`/`~/.zshenv` are only a few lines of `source` statements and the real init/PATH logic is elsewhere), the literal greps for `~/.zshrc ~/.zprofile ~/.zshenv` in each reference §2 will likely miss—this does not mean the logic is absent. Add all files from the source chain to the grep targets; only when they all come up empty can you conclude “indeed absent”.

### Phase 2 — Per‑Language Deep Dive (only for existing languages)

For each language hit in Phase 1:

1. Read `references/<lang>.md` (python / node / java / go / rust / ruby / git / swift / php / lua / zig / julia / dart / erlang-elixir / cpp).
2. Execute the commands listed in its **§2 Deep‑Dive Probing** one by one. All commands are read‑only and can be run in parallel across multiple Bash invocations. **They must be actually executed; do not fabricate output from memory.**
3. Classify the findings as OK / WARN / FAIL according to its **§3 Judgment Rules**.
4. When anomalies are found, autonomous follow‑up investigation is allowed (e.g., if a pyenv directory is found, grep shell config for init residue; if two `uv` are found, run `which -a uv` to check all). The follow‑up must also be read‑only.

When the user asks about only a single language: Phase 1 and Phase 3 still need to be run in full (conflicts often hide in languages the user did not ask about). In Phase 2, only deep‑dive the requested language. However, if the Phase 1 inventory shows obvious anomalies in other languages (e.g., dual managers for the same language), mention them briefly at the end of the report.

### Phase 3 — Cross‑Cutting Checks (2 invocations)

```bash
zsh scripts/probe-path.sh        # PATH detection across three scenarios (macOS path_helper pitfalls)
zsh scripts/probe-cache.sh       # Cache relocation environment‑variable inventory check
```

- `probe-path.sh` resolves key commands under three zsh scenarios: non‑login non‑interactive, login non‑interactive, and login interactive. If the three differ, that’s WARN. “Login non‑interactive” (common for GUI Apps and launchd) is the most frequently missed tier. For per‑language deep dives, you can append a specific check: `zsh scripts/probe-path.sh <cmd>` (as used in git.md / ruby.md §2). Note that `zsh -l -c` is an **approximate model** for GUI App/launchd environments (the true launchd environment needs `launchctl getenv PATH` for precision), but it is sufficient to catch the vast majority of issues. If the report involves launchd‑precise diagnosis, note this approximation.
- `probe-cache.sh` checks each item against the relocation inventory: for items where “environment variables lie” (like uv/pnpm/go/maven), judgment uses **the effective value reported by the tool itself** (capable of catching relocations done via `go env -w`/`pnpm config set`); for others, judgment uses the environment variables inherited by the current process. At the end it also performs a **three‑scenario consistency check** on relocation variables (a variable written only in `~/.zshrc` is invisible to GUI Apps/launchd = implicit drift). **Drift determination is grouped by tool** (uv/node/jvm/go/rust/asdf/poetry/php/ruby/dart/julia/cpp/bun/deno/lua each form a group): only when within the same group some variables are relocated and others are not does it count as drift and WARN; different groups being at different stages of relocation (e.g., uv is fully relocated, Maven not yet) is a normal state and not considered drift—relocation is optional, and there is no obligation to “do all or nothing”. If it reports FAIL (path pointing to an unmounted volume), **do not halt halfway to ask the user**—skip the cache check, finish the remaining flow, and note in the report: “Detected that the external path is not mounted; this check is skipped for this run. After mounting the disk, you may rerun `zsh scripts/probe-cache.sh` to re‑audit.”
- Both scripts primarily read from **the environment inherited by the current process** (the first line of output declares the snapshot scope); cross‑scenario differences are covered by probe‑path.sh (PATH) and the last section of probe‑cache.sh (relocation variables) respectively.

### Phase 4 — Comprehensive Report

Phase 4 automatically produces **three deliverables**, without ever pausing to ask the user (if the HTML template is not specified, choose one at random; the report language defaults to English; any uncertainty is written into the report, never interrupting execution):

1. **JSON structured summary** → written to `/tmp/dev-env-audit-summary.json` (internal data for the agent, consumed by the HTML renderer)
2. **Markdown main report** → output directly to the conversation window (human‑readable, with full details), **and at the same time** saved to `~/Desktop/dev-env-audit/dev-env-audit-report-<timestamp>.md`
3. **Single‑page HTML report card** → `zsh scripts/render-card.sh /tmp/dev-env-audit-summary.json ~/Desktop/dev-env-audit/dev-env-audit-report-<timestamp>.html [terminal|paper|brutalist]`, **generated every time by default**, not optional

`<timestamp>` is the same value for this run (e.g., `date +%Y%m%d-%H%M%S`). The Markdown and HTML files must land in the same directory with the same stem—the HTML card’s “open Markdown report” link is a relative path that depends on this convention. If the directory does not exist, `mkdir -p ~/Desktop/dev-env-audit`; this does not violate the “read‑only” philosophy—read‑only means not altering existing files/config of the system being audited; producing the report deliverables is the core output of this skill, and creating directories and new files is allowed from the start (just as writing JSON to `/tmp` is allowed).

#### 4.0 Report Language (Default English)

By default, reports are written in **English**—headings, findings, suggestions, and all `title`/`detail` fields in the JSON are in English. This is the default output language of this skill, independent of the language you use in conversation with the user. Only switch to Chinese (same structure, translated text) if the user explicitly asks for “a Chinese report”. The fixed labels in the three HTML templates (“Top Actions” “Stability” “Languages”, etc.) are **only available in English** and do not switch with the report language—they are the shell; the actual content comes from the JSON.

#### 4.1 Markdown Report Structure

The report **must** start with a **first‑glance trio** (score + immediate actions + one‑minute overview), allowing junior‑level users to grasp the full picture in three seconds; **then** proceed to the seven detail sections.

**First‑Glance Trio** (mandatory, compact, not expanded, default English, example):

```markdown
# Dev Environment Health Check

> **Overall: $SCORE / 100 $EMOJI $TIER_LABEL** (Excellent / Good / Needs Attention / At Risk / Critical)
> 🟢 OK: $OK  ·  🟡 WARN: $WARN  ·  🔴 FAIL: $FAIL

## Top 3 Actions
1. 🔴 $ACTION_1
2. 🟡 $ACTION_2
3. 🟡 $ACTION_3

## One-Minute Overview

| Language | Current | Recommended | Status |
|---|---|---|---|
| ... | | | |

---
(the original 7 detail sections follow below)
```

**Seven Detail Sections** (keeping the original structure with the minor adjustments described here; write them in English by default):

0. **Philosophy Declaration** — 3–5 line summary of design philosophy (at minimum including items 1/3/5: suggest not execute, per‑language authoritative tools, respect existing reasonable choices), and note: all diagnoses and suggestions are based on this philosophy; those who disagree may find this report less useful.
1. **Overall Conclusion** — start with score + tier; still mark PASS/WARN/FAIL, but the score is the “shareable asset”; the 3 most important findings (merged by common root cause).
2. **Per‑Language Status Table** — simplified to four columns: `Language | Current (incl. install channel) | Recommended | Status`. The original “Action Needed” and “Risk” columns are moved to section 5, to avoid an overly wide first‑glance table.
3. **Conflict Inventory** — each item written as “Symptom → Root cause → Impact”.
4. **Cache Relocation Status** — three categories: Relocated / Not Relocated / Drift. **Drift is the most dangerous state**, highlight it emphatically.
5. **Per‑Language Migration Plan** — only list languages that need action; follow reference §4 five‑step method; **carry over the “Action Needed” and “Risk” columns moved from section 2**. Commands must come from the references; no fabrication. Every destructive command is individually labeled with its risk, citing reference §5.
6. **Recommended Execution Order** — cross‑language dependencies: install new before removing old (install fnm before removing brew node); CARGO_HOME must be decided before installing uv; SDKMAN_DIR / RUSTUP_HOME / ASDF_DATA_DIR must be set before installation.
7. **✅ Positive Findings** — list items that are “correctly configured”. This is both a teaching moment for junior users (“what did I do right”) and makes the report more shareable by not appearing only full of problems. **At least 1 item**, encouraged 3–5. Examples (in English):
   - ✅ Python on uv, PATH is unique, no pyenv/conda leftovers
   - ✅ Rust on rustup, single rustc/cargo install
   - ✅ Cache uniformly relocated to `/Volumes/SSD/dev-cache/`, no drift

The report ends with clearly separated columns, never interleaved:

- **Read‑only verification commands you can rerun directly**
- **Change commands that require your review and manual execution**

Writing discipline:
- Merge multiple WARNs with the same root cause into one item.
- The reader is “your future self three months later who forgot how you configured things”—every suggestion should explain the why, not just give commands.
- Machine‑specific values (like the exact external disk path) are shown as‑is, with no assumption that all machines are the same; however, any value resembling credentials/keys is always masked (see “Security Discipline”), outside the “show as‑is” scope here.
- **The first‑glance trio must be “3‑second readable”**: each immediate action item no longer than one line; the TL;DR table only shows present languages; status uses emoji + colored text (not bare text).
- **Any point requiring user decision/confirmation is written into the report (e.g., as a “To Confirm” subsection or inline note), never pause execution to ask.**

#### 4.2 Scoring Rules (How the First‑Glance Score Is Calculated)

```
Score = 100
  - each FAIL             -15
  - each WARN             -5
  - each INFO             -0
  - cache drift detected  -10 (drift is the most dangerous state — design philosophy #5)
  - PATH inconsistent across 3 scenarios  -8 (probe-path.sh reports WARN)
  - Apple git with no brew takeover       -3 (version freeze is a latent risk even without conflict)
floor: 0
```

Tiers:

| Score | Tier | Emoji | Meaning |
|---|---|---|---|
| 90-100 | Excellent | 🟢 | share it as‑is |
| 75-89 | Good | 🟢 | fine day to day, worth clearing the WARNs |
| 60-74 | Needs Attention | 🟡 | a few clear gaps |
| 40-59 | At Risk | 🟠 | occasional breakage likely |
| 0-39 | Critical | 🔴 | fix before doing anything else |

Three dimension scores (displayed as three compact horizontal progress bars in the HTML card; may be omitted from the Markdown report):

- **Stability** = 100 - 20 × number of FAILs (floor 0)
- **Consistency** = 100 - 15 × number of PATH inconsistencies - 15 × number of cache drifts (floor 0)
- **Modernity** = 100 - 8 × number of non‑authoritative managers (floor 0)

#### 4.3 JSON Summary

Written to `/tmp/dev-env-audit-summary.json`. Schema details in `scripts/render-card.schema.md`. **Required fields**:

- `score` / `tier` / `tier_label` / `tier_emoji` / `counts.{ok,warn,fail}`
- `scores.{stability,consistency,modernity}`
- `languages[]` (per item: `name`, `current`, `recommended`, `status` ∈ `ok`/`warn`/`fail`/`info`)
- `top_actions[]` (per item: `severity`, `title`, `detail`; **maximum 3, sorted by severity**)
- `positive_findings[]` (per item: `title`, `detail`; **at least 1**, otherwise the report looks entirely negative)
- `host.{os,shell}`, `timestamp` (ISO 8601)
- `report_md` (**required**, the filename of the Markdown report saved to disk in this Phase 4 run, relative path—see next section, the HTML card uses it to generate the “open full report” link)

Natural language fields like `title`/`detail` default to English per §4.0.

#### 4.4 HTML Single‑Page Report Card (Default Artifact, Three Skins to Choose From)

No dependency on Python: `scripts/render-card.sh` is pure `zsh` + `sed` + `awk`, mechanically inserting the JSON into one of three static templates (`render-card.terminal.html` / `render-card.paper.html` / `render-card.brutalist.html`) by substituting their sole placeholder; the templates’ HTML/CSS/JS are never regenerated, and the model never needs to write them.

```bash
zsh scripts/render-card.sh /tmp/dev-env-audit-summary.json \
  ~/Desktop/dev-env-audit/dev-env-audit-report-<timestamp>.html \
  [terminal|paper|brutalist]
```

- **How the template is chosen**: if the user names one of the three styles when initiating the audit (e.g., “use the brutalist template”), pass that name as the third argument; **if not named, do not pass anything—the script will pick one randomly using `$RANDOM`**. Do not ask the user to choose a style.
- The three templates share the exact same information architecture, differing only in visual style:
  - `terminal` — dark terminal window style, monospace font
  - `paper` — light editorial/certificate style, serif numerals, circular stamp‑like tier badge
  - `brutalist` — neo‑brutalist style, thick black borders, hard shadows, high‑saturation color blocks
- Features (common to all three templates):
  - Single‑file HTML, CSS/JS/data all inline, no external dependencies, no network requests
  - Double‑click to open, screenshot‑ready, printable
  - Status is always expressed with CSS dots/color blocks, never colored emoji (to avoid cross‑system font rendering inconsistencies)
  - Large letter grade at the top (A/B/C/D/F, derived by embedded JS from `tier`, no extra field needed from the agent)
  - If the JSON provides `report_md`, the card shows a prominent “Full details in the Markdown report →” link
  - All template text is **in English only**, not switching with report language (see §4.0)
  - Responsive, and essentially all content fits in one screen capture

**Phase 4 Completion Checklist**:
- [ ] `/tmp/dev-env-audit-summary.json` exists and contains all required fields from §4.3 (including `report_md`)
- [ ] The Markdown report has been output to the conversation window (first‑glance trio + seven detail sections + ending two columns) and also saved to `~/Desktop/dev-env-audit/`
- [ ] `zsh scripts/render-card.sh` has been run and the HTML card has been generated in the same directory, with the same stem as the Markdown file
- [ ] No questions were asked to the user during the process regarding template choice, report language, etc.

## Security Discipline (Default Behavior That Overrides Temporary User Requests)

- Deep‑dive and follow‑up use only read‑only commands: `command -v` / `which -a` / `ls` / `cat` / `grep` / each tool’s `--version` / `list` / `config get`, and each tool’s own env query subcommands (e.g., `go env`, `npm config get`—which only echo a few named variables managed by that tool, not the full system environment).
- **Forbidden**: `env` / `printenv` / `export -p` / bare `set` or any other command that dumps the entire process environment—probing only targets named variables (e.g., `echo $GOPATH`, `go env GOCACHE`); bulk environment dumps are never performed.
- When `cat`/`grep` is used on shell configuration files (`~/.zshrc`, `~/.zprofile`, etc.), if a matched line appears to assign a credential (variable name containing KEY/TOKEN/SECRET/PASSWORD, or a value resembling a key/token), only report “the line exists, variable name is …”, and replace the value with `***`—never write plaintext suspected keys into any output, including intermediate reasoning or the final report.
- Do not execute any install / uninstall / `rm` / `mv` / redirect‑write / `curl` / `wget` / shell‑config edits.
- If the user says “just fix it for me” mid‑process: first complete and output the report, then clearly state that executing changes is outside the skill’s boundary and the user needs to review each specific command, confirming and executing them manually, or grant explicit authorization in a separate task.
- **Never interrupt execution to ask the user any preference‑based questions (style/language etc.)**: once the audit is initiated, Phase 1–4 runs to completion without pausing for questions like “do you want to mount the disk to re‑verify”, “which HTML template”, or “what language for the report”. When not explicitly specified, decisions follow the defaults stated in each section (random template, default English, skip if external disk not mounted). Any point needing user confirmation or review is written into the report; never halt to ask.

## Reference Overview

| File | When to Read |
|---|---|
| `references/python.md` | Phase 1 finds any of python3 / uv / pyenv / conda |
| `references/node.md` | Finds any of node / fnm / nvm / volta / pnpm |
| `references/java.md` | Finds any of java / sdkman / jenv / gradle / maven |
| `references/go.md` | Finds any of go / gvm / asdf-golang |
| `references/rust.md` | Finds any of rustc / cargo / rustup |
| `references/ruby.md` | Finds a non-system ruby, rbenv, or rvm (if only the macOS system ruby is present with no manager, skip it and label it "system default, unmanaged") |
| `references/git.md` | Always read (everyone has git, and the Apple frozen version is a widespread problem) |
| `references/csharp.md` | Removed: .NET/C# is rare on macOS and was dropped from scope. |
| `references/swift.md` | Finds swift (installing Xcode usually means it is present, but that does not mean the user writes Swift; deep-dive only when the user asks or Phase 1 shows obvious anomalies) |
| `references/php.md` | Finds php or composer |
| `references/lua.md` | Finds lua or luarocks |
| `references/zig.md` | Finds zig or zigup |
| `references/julia.md` | Finds julia or juliaup |
| `references/dart.md` | Finds dart, flutter, or fvm |
| `references/erlang-elixir.md` | Finds erl, elixir, or mix |
| `references/cpp.md` | Finds gcc, clang, cmake, or vcpkg—but note that clang is present on nearly all Macs because Xcode CLT provides it; deep-dive only when the user explicitly writes C/C++, or Phase 1 reveals multiple gcc versions or vcpkg; do not run it on every machine |
| `references/_template.md` | must read before adding or modifying any reference (contains anti‑hallucination checklist); not read during an audit |

Bun / Deno do not have references: they do not conflict with Node, are installed on demand, and the existence information from scan.sh is sufficient; only report WARN if “both brew and the official script have installed a copy”.

mise does not have a reference and is not part of the baseline: this skill’s philosophy is **use each language’s authoritative tool** (uv / fnm / rustup…) or one tool per ecosystem (SDKMAN for JVM); it does not endorse the “one tool to unify all languages” route and never actively recommends mise. Rules when mise is discovered:
1. If mise and a language‑specific manager are **managing the same language simultaneously** → handle per that language reference’s “dual manager” rule (pick one, usually keep the dedicated tool).
2. If the user is already using mise (or asdf) for full‑stack uniformity and it works fine → **respect the status quo**, do not recommend swapping mise↔asdf type tools—the gain is lower than the cost of churn.
3. Node is an explicit exception: the baseline recommends fnm (see node.md) regardless of existing mise/asdf.
