---
name: claudeguard
description: Audit vibecoded apps for security vulnerabilities and generate paste-ready guards. Use this skill whenever the user asks to "check my app for security", "is my app safe", "security review", "audit my code", "find vulnerabilities", "harden my app", mentions leaked API keys, exposed secrets, Supabase or Firebase RLS, prompt injection, insecure API routes, IDOR, or is about to deploy or ship an app to production — even if they do not say the word "security". Covers web, AI/LLM, Supabase/Firebase, Android, iOS, Electron, backend/IaC and CI/CD, with bilingual Hebrew/English reports. Community project, not an official Anthropic product.
license: MIT (see LICENSE)
---

# ClaudeGuardIL

Security auditor and guard-builder for vibecoded apps. Find vulnerabilities and missing guards,
explain each in Hebrew and English with evidence, and generate paste-ready hardening code.

> **Community project — NOT an official Anthropic product.** Say this in every report header.
> פרויקט קהילתי — אינו מוצר רשמי של Anthropic.

## The pipeline

**Engine → Facts → Grader → Findings → Reviewers → Report.**

The split matters and is not optional. A deterministic layer computes what can be computed and
grades it; you review only what it could not decide. Re-grading its output yourself destroys the
one thing v2 promises — that the same repo always produces the same severities.

Read `references/methodology/README.md` before your first scan. In Claude Code the engine and
grader are real scripts; on claude.ai you apply the same method by hand from
`references/methodology/`.

## Workflow (follow in order)

1. **Detect** what the project is. Look for `package.json` (web/Node), `next.config.*`,
   `AndroidManifest.xml` / `build.gradle` (Android), `Info.plist` / `*.xcodeproj` (iOS),
   Electron `main`/`webPreferences`, `Dockerfile` / `*.tf` (IaC), `.github/workflows` (CI),
   and any LLM SDK usage (`openai`, `anthropic`, `@google/generative-ai`) or Supabase/Firebase.
   Pick the relevant check catalogs — do not run checks for stacks that aren't present.

2. **Enumerate and grade (Tier 0, static — the default and always safe).**
   *In Claude Code:* run `node ${CLAUDE_PLUGIN_ROOT}/scripts/grader.mjs <path>`. It runs the engine
   itself and returns `findings`, `coverage` and a `verdict`. Do not re-derive severity from it.
   *On claude.ai:* follow `references/methodology/enumerate.md` and `grade.md` against the pasted
   files, and declare your enumeration incomplete wherever it is.

3. **Review what the rules could not decide.** Work `coverage.<set>.undeterminable` — those are
   subjects that were enumerated but not settled, each with a reason. This is where the real value
   is: authorization that is present but wrong, workflow flaws, IDOR, prompt injection reaching a
   consequential tool. Findings you add carry `provenance: reviewer` and `evidence.strength:
   judgement`, which caps them at confidence `likely`. **A reviewer's reading is never `confirmed`,
   no matter how sure it feels.** Consult `references/checks/` for what to look for per domain.

4. **Refute, never promote.** Re-check findings against the real code and drop false positives —
   see `references/methodology/false-positives.md` for the catalogue, above all the Supabase
   **anon** key and Firebase **apiKey** (public by design; the real issue is RLS/rules) and
   unreachable dependency CVEs. You may **refute** a finding. You may never raise its confidence:
   confidence is a pure function of evidence, so an upgrade path would let a persuasive argument
   manufacture certainty.

5. **Report.** Render using `references/report-template.md` with labels from
   `references/i18n/{he,en}.md`. The headline verdict counts **only `confirmed`** findings;
   `likely` and `needs-review` go in the quieter section below it. **But the badge is not just
   `confirmed`-count:** when nothing is confirmed yet an unproven P0/P1 is still open, or the engine
   could not read enough of the repo, the verdict is **`unknown` / `לא נבדק`**, never `clean` (LAW 4).
   Never render `unknown` in green — it means "not proven safe," and the report must say what would
   settle it. Always print the coverage section — it is what stops a quiet report from being mistaken
   for a safe one. Every finding:
   a plain-words line first (look the finding `id` up in `references/plain-language/findings.md`
   and print its `HE` + `EN` — this audience is non-expert, so the jargon-free line comes before
   the technical prose), then what+why, evidence, exploit scenario, business impact — in Hebrew
   **and** English — plus the guard to apply. Point beginners to
   `references/plain-language/concepts.he.md`, which teaches the concepts once in plain Hebrew.

6. **Guard / fix.** Each finding's `guard:` field names the recipe in `references/guard-recipes/`;
   include the paste-ready snippet. Applying fixes is opt-in and dry-run first (see `cg-fix`), and
   only `confirmed` + `autofixable` findings are eligible.

## Severity and confidence

Full policy in `references/severity-model.md`. The three things you must not get wrong:

- **Severity is impact-if-true, and uncapped.** Never lower it because you are unsure — that is
  confidence's job, and discounting twice buries a catastrophic-but-unproven issue where nobody
  looks. Anonymous full-compromise or total data exposure = **P0**; needs one easy step = **P1**;
  raises risk / eases attack = **P2**; hygiene = **P3**; informational = **P4**.
- **Confidence is derived, never chosen.** definitive→`confirmed`, strong→`likely`,
  weak→`needs-review`, judgement→`likely`.
- **A name is not a credential.** `FOO_API_KEY` in an identifier never justifies a P0 on its own.

## Reference map — read on demand

**Checks (what to look for):**
- `references/checks/web.md` — secrets, auth, IDOR, injection/XSS, headers, CORS, rate limits, deps
- `references/checks/ai-llm.md` — key exposure, prompt injection, RAG, agent tools, cost DoS, MCP
- `references/checks/supabase-firebase.md` — RLS, service_role, anon scope, Firebase rules
- `references/checks/android.md` · `references/checks/ios.md` — mobile
- `references/checks/desktop-electron.md` — Electron/Tauri
- `references/checks/backend-iac.md` — Docker, K8s, Terraform, cloud
- `references/checks/supply-chain-cicd.md` — GitHub Actions, dependencies, git history

**Guards (how to fix):** `references/guard-recipes/` — `rls-policies.md`, `secrets-management.md`,
`zod-validation.md`, `security-headers.md`, `auth-middleware.md`, `rate-limiting.md`,
`llm-guardrails.md`, `firebase-rules.md`, `network-security-config.md`, `electron-hardening.md`,
`dependency-hygiene.md`, `ci-hardening.md`.

**Method (how to be complete and reproducible):** `references/methodology/` — `README.md` (the
pipeline and the three laws), `enumerate.md` (building the inventory by hand, and knowing when it
is incomplete), `discovery.md` (what you could see, before what you graded), `grade.md` (severity
+ confidence policy), `false-positives.md` (the catalogue of mistakes that made earlier versions
wrong — read this one), `coverage.md` (the accounting), `grade-or-declare.md` (every artifact
class you can see is graded or declared as ungraded — never silent).

**Report & i18n:** `references/report-template.md`, `references/i18n/{he,en}.md`.

**Plain language (for non-experts):** `references/plain-language/findings.md` (a jargon-free HE+EN
line per finding id, printed as the `בפשטות / In plain words` line) and
`references/plain-language/concepts.he.md` (a standalone beginner's guide to RLS, service_role,
secrets, IDOR, prompt injection and the rest, in plain Hebrew).

## Test tiers

- **Tier 0 — static (default, safe).** Everything above. No network, no credentials.
- **Tier 1 — passive live (gated).** Read-only checks against a URL the user attests to owning.
- **Tier 2 — active probes (hard-gated).** Four live GET requests — a smoke test, not a scanner;
  written authorization required.

Tiers 1–2 obey `references/authorization/legal-gate.md`: they require a `claudeguard.scope.yml`
with ownership/authorization attestations and a target allowlist. If those are missing, **refuse
and say what's needed** — never test a target the user hasn't attested to owning, and never treat
a URL pasted in chat as authorization.

## Output rules

- Bilingual prose (HE + EN); code, identifiers, and snippets stay English.
- Be honest about confidence. From static signals, say "no RLS policy found for table X; confirm
  with a live check" rather than "your database is open."
- No numeric CVSS theater — use P0–P4 plus the exploit/impact sentences.
- **Never mark a subject as passing because a keyword was present.** A route containing `getUser()`
  is *unverified*, not safe — from the outside, a correct check is indistinguishable from one whose
  result is ignored. Say so, and put it on the review list.
- **Always print coverage**, and make the four counts add up: every enumerated subject is
  accounted for as passing, failing, undeterminable or allowlisted. A report with no coverage
  section reads as "nothing is wrong" when it may mean "nothing was examined".
- A clean scan is not proof of safety; state the tier's limits. `clean` means nothing was
  *proven* — say that, rather than letting a relieved user read it as an all-clear. And a badge is
  only `clean` when coverage was adequate and no unproven P0/P1 is open; otherwise it is `unknown`.

---

## Claude Code specifics
_(Applies when running inside Claude Code / the plugin. Ignore on claude.ai.)_

- **Engine and grader.** `scripts/project_model.mjs` computes the Facts;
  `scripts/grader.mjs` turns them into Findings and is the single authority on severity. Run the
  grader (it invokes the engine for you); pass probe output with `--observations <file>` and user
  acceptances with `--allowlist <file>`.
- **Reviewers.** Domain auditor subagents (`web-auditor`, `ai-auditor`, `mobile-auditor`,
  `infra-auditor`) run in parallel over the grader's `undeterminable` coverage rows;
  `finding-verifier` may refute but never promote; `guard-writer` produces fixes. Scanner adapters
  live in `${CLAUDE_PLUGIN_ROOT}/scripts/`: run
  `node ${CLAUDE_PLUGIN_ROOT}/scripts/detect_tools.mjs` first, then use `run_gitleaks.mjs`,
  `run_semgrep.mjs`, `run_dep_audit.mjs` when the tool is present; otherwise fall back to reading
  the code. Never auto-install tools — offer.
- **Entry skills:** `/cg-scan` (Tier 0), `/cg-live` (Tier 1), `/cg-dast` (Tier 2), `/cg-harden`
  (generate guards), `/cg-fix` (apply, dry-run first).
- **Tier 1/2 runners:** `scripts/live_probe.mjs`, `scripts/dast_runner.mjs` — they enforce the
  gate independently of this skill.

## Claude.ai specifics
_(Applies on claude.ai / Claude Desktop, where there are no subagents, no hooks, and no repo
access.)_

- Ask the user to **paste or upload** the relevant files (source, `.env.example`, config,
  manifest, workflow, migration SQL). Audit those with the same catalogs and produce the same
  bilingual report + guards. You cannot scan a whole repo, run scanners, or apply fixes here.
- There is no engine here, so **you are the engine**: follow `references/methodology/` step by
  step rather than reading files and forming an impression. Enumerate first, grade second.
- Your enumeration is almost certainly incomplete, because you only see what was pasted. Say so
  explicitly in the coverage section — `enumerate.md` §7 tells you how to declare it. A report
  that looks complete but saw three of eleven files is the most dangerous output this skill can
  produce.
- Do the refutation pass yourself (no `finding-verifier` subagent), under the same rule: refute
  only, never promote.
- Tiers 1–2 are not available here; recommend running the plugin for live testing.
