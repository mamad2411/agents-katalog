---
name: repo-audit
description: "Grade a Git/GitHub repository and hand back a shareable scorecard. Scans the working tree and git history for leaked passwords, API keys, tokens, and private keys (with fixture-vs-real-leak discrimination so demo data does not tank the score), audits repo hygiene (LICENSE, README, .gitignore, .env handling, tests, CI, lockfiles, SECURITY.md), judges maintainability, and computes two headline numbers: a GLOBAL GRADE (0-100 + letter A-F) and a VIBE SCORE (0-100, how much the repo reads as unreviewed AI-generated code). Use when asked to audit / grade / score / review a repo, check a repo for leaked secrets or API keys, rate code quality or 'how vibecoded is this', or produce a repo scorecard. Triggers: 'scan repo', 'audit repo', 'grade my repo', 'check for leaked keys', 'secret scan', 'is this vibecoded', 'repo score', 'code quality score'."
version: 1.0.0
---

# repo-audit - grade a repository, secrets + craft + vibe

Produce one shareable **scorecard** for any repo: a **Global Grade (0-100, A-F)** and a **Vibe Score (0-100)**. The secret scan is table stakes (gitleaks does that); the differentiator is the honest craft read and the Vibe Score. Claude reading the code beats regex for judging craft, so the model does the judging; tools only accelerate the mechanical sweep.

## When to use
- "Scan/audit/grade this repo", "check for leaked API keys/passwords", "is my repo secure".
- "How vibecoded is this?", "rate the code quality", "give my repo a score".
- Before open-sourcing a repo, before a client hands one over, or as a quick due-diligence pass on a dependency.

## Do NOT
- Do not treat every regex hit as a leak. Demo/test/example files exist to hold fake secrets. Discriminate (see §2).
- Do not exfiltrate any real secret you find. Report it truncated (last/first 4 chars), tell the owner to rotate it, never paste it in full into a message or a cloud service.
- Do not run against a repo you are not authorized to read. Public repos and the user's own repos are fine.

## Workflow

1. **Acquire.** If given a URL, `git clone --depth 200 <url>` into a temp dir (depth matters: history holds removed secrets). If given a path, use it. Note default branch + commit count.
2. **Secret sweep** (§2). Working tree + git history. Discriminate real leaks from fixtures.
3. **Hygiene audit** (§3). Presence/quality of the files a maintained repo should have.
4. **Maintainability read** (§4). Tests, CI, structure, dependency hygiene.
5. **Craft / Vibe read** (§5). This is the judgment call. Read a representative sample of source files and score how much the repo reads as unreviewed AI output.
6. **Score** (§6). Compute the four sub-scores, the Global Grade, and the Vibe Score.
7. **Report** (§7). Emit the scorecard.

Optional accelerator: `scripts/repo_grade.py <path-or-url> [--json]` runs the mechanical parts (secret regex sweep, hygiene checks, coarse vibe signals) and prints a draft scorecard. Use it to seed the numbers, then override with your own read. It is a helper, not the source of truth.

## 2. Secret detection + fixture discrimination

Scan every text file (skip `.git`, `node_modules`, `dist`, `build`, `vendor`, lockfiles, binaries) and the git history.

**History:** if `gitleaks` is on PATH, run `gitleaks detect --source . --no-banner --redact`. Else `git log -p | grep -nE '<pattern>'`. A secret committed then deleted is still a leak until rotated.

**High-signal patterns** (most-specific first): AWS `AKIA/ASIA…`, GCP `"type":"service_account"`, Google `AIza…`, GitHub `ghp_/github_pat_/gho_`, Stripe `sk_live_`, Slack `xox[baprs]-`, SendGrid `SG.…`, Anthropic `sk-ant-…`, OpenAI `sk-…T3BlbkFJ…` / `sk-proj-…`, HuggingFace `hf_`, GitLab `glpat-`, Postman `PMAK-`, Doppler `dp.pt.`, Vault `hvs.`, Terraform `…​.atlasv1.…`, DigitalOcean `dop_v1_`, npm `npm_`, PyPI `pypi-AgENdGV…`, `-----BEGIN … PRIVATE KEY-----`, JWT `eyJ….eyJ….…`, basic-auth-in-URL `https://user:pass@host`, and the generic `(?i)(api_key|secret|token|password)['"\s:=]+['"]([A-Za-z0-9/+=_-]{16,})['"]`. The full 80-pattern catalog lives in the companion `offensive-osint` skill §17 / `scripts/secret_scan.py` - reuse it when you need breadth.

**Real leak vs fixture - the call that makes this skill trustworthy.** Downgrade a hit to `fixture` (does not hurt the score) when ANY of:
- Path signals test data: `example`, `sample`, `fixture`, `demo`, `mock`, `test`, `spec`, `README`, `CHANGELOG`, `docs/`, `*.md`.
- Value looks placeholder: `your-api-key`, `<token>`, `changeme`, `xxxx`, `sk-live-0123456789…` (sequential), `example`, `...`.
- File is a CI test that FEEDS a fake secret to assert redaction (e.g. an anonymizer's "0-leak" test).
- It is a UI placeholder (`placeholder='{"type":"service_account", ...}'`).

Only a hit that survives all of these is a **real leak candidate**. Flag it CRITICAL/HIGH, tell the owner to rotate, and (if it matches a validator in `offensive-osint` §23) note it can be liveness-checked read-only. Everything else: report as "N fixtures (expected)".

## 3. Hygiene checklist (each = pass/fail)

`README` · `LICENSE` · `.gitignore` present · `.gitignore` lists `.env` · no real `.env` tracked (`git ls-files`) · `.env.example` present · a tests dir/files · CI config (`.github/workflows`, `.gitlab-ci.yml`, …) · a lockfile / pinned deps · `.dockerignore` when a Dockerfile exists · `SECURITY.md`. Hygiene score = passed / total × 100.

## 4. Maintainability read

Start 100, subtract: no tests −30; no CI −20; no lockfile/pinned deps −15; no README −15. Then sanity-check by eye: giant files (>800 lines), one-file-does-everything, no module boundaries, dependency sprawl (deps declared but unused), dead code. Adjust ±10 on judgment.

## 5. Vibe Score (0-100) - the differentiator

**Question:** how much does this repo read as *AI-generated code that a human shipped without really reviewing it*? 0 = handcrafted / clearly reviewed. 100 = pure unreviewed slop. This is a craft signal, not a "was an LLM involved" signal (good engineers use LLMs; the tell is the *lack of review*, not the generation).

Read a representative sample (entry points, the biggest files, a few random modules). Score by accumulating penalties, cap 100:

| Signal (unreviewed-AI tell) | Weight | What it looks like |
|---|---|---|
| **Chatbot phrasing left in code/comments** | very high | `# As an AI…`, `Certainly! Here's the function…`, `# In a real-world scenario you would…`, `# This is a basic example` |
| **Narration comments on trivial code** | high | `# increment i by 1`, `// loop through the items`, `# import the necessary libraries`, docstrings that just restate the signature |
| **Emoji inside source code** (not README) | high | `# 🚀 initialize the app`, `logger.info("✅ done")` |
| **Swallowed errors** | high | `except: pass`, `except Exception: pass`, empty `catch {}` - the classic "make the red go away" |
| **Stubs / unfinished** | med | `raise NotImplementedError`, `throw new Error("not implemented")`, dense `TODO/FIXME` |
| **Debug left in** | med | stray `print(` / `console.log(` in library code |
| **Copy-paste duplication** | med | same 6+ line block repeated; near-identical functions differing by a literal |
| **Mega-files / no boundaries** | med | 800+ line files, everything in one module, no separation of concerns |
| **Lots of code, ~no tests** | med | >400 LOC and test-to-code ratio < 5% |
| **README slop** | low | wall of `- ` bullets, 8+ emojis, `## ✨ Features` / `## 🚀 Getting Started` generated boilerplate with no real content |
| **Generic commit history** | low | `update`, `fix`, `changes`, `wip`, `asdf` dominate; OR uniform `feat: implement the X` with zero human texture |
| **Inconsistent conventions** | low | camelCase and snake_case mixed in one language; tabs/spaces mixed; naming drift |
| **Real leaked secret present** | signal | a hardcoded live key is itself a review-failure tell |

Weight by prevalence, not single instances. One `print` is nothing; `print`-debugging scattered across the codebase is a tell. **Craftsmanship sub-score = 100 − Vibe Score.**

Counter-signals that LOWER the Vibe Score (evidence of real review): meaningful tests that assert behavior, encryption/security done correctly (fails-closed, constant-time compares), tidy commit messages that explain *why*, thoughtful error handling, small focused modules, a real CHANGELOG. Reward these.

## 6. Scoring

- **Security 40%** - 100 minus severity-weighted real leaks (critical −45, high −25, medium −10, low −4) minus history findings (−8 each, cap −40). Fixtures do not subtract.
- **Hygiene 20%** - §3 pass rate.
- **Maintainability 20%** - §4.
- **Craftsmanship 20%** - 100 − Vibe Score.
- **GLOBAL = 0.40·Security + 0.20·Hygiene + 0.20·Maintainability + 0.20·Craftsmanship.**
- Letter: A ≥90, B ≥80, C ≥70, D ≥60, E ≥50, else F.
- A real CRITICAL leak caps the Global Grade at **D** regardless of the rest (a live key in the tree is disqualifying).

## 7. Output - the scorecard

Lead with the two headline numbers, then the breakdown, then the fix list. Keep it shareable (people will screenshot it).

```
┌─ REPO SCORECARD ─ <owner/repo> ─────────────┐
│  GLOBAL GRADE   72/100   (C)                 │
│  VIBE SCORE     31/100   (mostly handcrafted)│
├──────────────────────────────────────────────┤
│  Security        90/100   0 real leaks, 6 fixtures
│  Hygiene         82/100
│  Maintainability 70/100   tests: yes · CI: yes
│  Craftsmanship   69/100
└──────────────────────────────────────────────┘
```

Then:
- **Secrets** - real leak candidates (rule · file:line · truncated value · "ROTATE NOW"), and a one-line "N fixtures ignored (demo/test data)".
- **What's good** - 2-4 concrete strengths (reward real review).
- **What to fix** - ranked: Critical (leaks) → High → Medium → Low, each with a one-line action.
- **Vibe verdict** - one honest sentence on the craft, citing the actual signals seen.
- **How to level up this repo** - REQUIRED closing section. A ranked, quick-wins-first improvement path, each item as: `action → expected score delta (+N to <sub-score>), effort (S/M/L)`. Order by score-gain-per-effort, not by category. Anchor every item to something actually seen in the scan (a missing tests dir, a duplicated module, an unpinned dep), never generic advice. End with the single highest-leverage move ("if you do one thing: …"). This is what turns a scorecard into something the owner acts on.

Vibe Score bands for the label: 0-20 "handcrafted", 21-40 "mostly handcrafted", 41-60 "mixed / partly unreviewed", 61-80 "heavily vibecoded", 81-100 "raw AI slop".

## Notes on positioning (why this is shareable)
Secret scanning is a solved, boring category. The Vibe Score is the hook: it names the 2025+ anxiety (people shipping AI code they did not review) and it is inherently comparative and screenshot-able. Keep it honest - the value is that a low Vibe Score means something because the skill also rewards genuine craft. Overclaiming ("100% detects AI code") kills it; "reads the repo the way a senior reviewer would, and scores the review-failure tells" is the true and defensible pitch.
