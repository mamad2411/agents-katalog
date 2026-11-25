---
name: redteam-self-audit
description: Run an authorized, black-box-first security self-audit on a locally running app. Use this skill whenever the user asks for a security review, penetration test, red-team exercise, vulnerability hunt, "hack my app", "attack my project", "find the holes before attackers do", "is this safe to ship", or a pre-deploy security audit. It attacks the running target like a motivated intruder, proves findings with evidence, audits the code for what traffic cannot reveal, reports CVSS-scored findings with a release verdict, then drives approved fixes through retest rounds until the Retest Gate passes. Local and private targets only; an explicit Rules of Engagement is mandatory.
---

# Redteam Self-Audit

Hack yourself before the bad guys do.

This skill runs a real security assessment against a local copy of the project, not a checklist review. It attacks first, proves what is exploitable, then reads the code to find what traffic cannot reveal, and drives fixes until a retest finds the gaps closed.

## Use when

- The user asks for a security review, pen test, red-team exercise, vulnerability hunt, or pre-deploy audit.
- The user says "hack my app", "attack this project", "find the holes", "is this safe to ship", or "audit this before release".
- A repository can be built and run locally, or a local URL is already running.
- The user can attest ownership and authorize testing.

## Do not use

- Public, third-party, production, or customer-facing targets. Refuse and explain the local-only rule.
- Malware, persistence, C2, ransomware behavior, DoS, or data exfiltration.
- "Just run a scanner and list issues" requests. Scanner output is a lead, not a Finding. Explain the difference and offer the protocol.
- No repository and no running target: offer a static-only review, label it as such, and cap the verdict at CONDITIONAL.

## Hard rules

1. **No ROE, no attack.** Write `.redteam/ROE.md` from `templates/ROE.md`, including the authorization attestation, target allowlist, identity list, Proof Cap, window, and expiry. If the user cannot attest ownership, stop.
2. **Local targets only.** Resolve every target to loopback or a private network created for this run. Refuse public IPs and domains, production systems, third-party APIs, real cloud metadata, and anything not spawned here. If the target redirects or calls out, stop that test and record it.
3. **Never destructive.** No DoS or load floods, no dropping or corrupting data, no persistence, no C2, no reverse shells to external hosts, no exfiltration beyond the Proof Cap, no real user accounts, no credential stuffing against anything outside the local target.
4. **Proof Cap.** Prove impact with the minimum. One record, the first bytes of one file, one seeded account's object, one admin action on a seeded admin. Stop immediately after proof.
5. **Black-box isolation.** The Black-Box Attacker gets `BRIEF.md` only: URLs, allowed hosts, credentials, seeded object IDs, rate limit. No repository reads, no source, no audit notes, no stack traces. Enforce with a separate session, subagent, or network-only container where the harness allows. If the harness cannot enforce it, label every report **Gray-Box**.
6. **Confirmed means evidenced.** A Confirmed Finding has a reproduction request/response or browser trace. Tool output is a lead, never a Finding.
7. **Never claim completeness.** Do not write "secure", "no vulnerabilities", or "all clear". Report the Coverage Matrix, residual risk, and the exact commit/build tested. "Clean" means "no confirmed findings within stated coverage".
8. **No unapproved fixes.** The user approves fixes per Finding. The Implementer is separate from the Attacker. Banned fixes: disabling a control, client-side-only validation, blanket exception swallowing, WAF or regex band-aids over an injection sink, deleting the feature.
9. **Stop on danger.** Target unhealthy, unexpected egress, real PII or live secrets, destructive risk, scope drift, or production data: stop and report.
10. **Protect evidence.** Redact tokens, cookies, credentials, and PII from reports. Keep raw evidence under `.redteam/evidence/` with mode `0600` and gitignored.
11. **Three Rounds by default.** Exit only through the Retest Gate, an explicit user stop, or documented risk acceptance.
12. **Stay portable.** Detect capability tier first: A (shell + Docker), B (shell, host-run server), C (no shell, static review). Optional tools are never assumed.
13. **Resources are references, not targets.** Read OWASP, Exploit-DB, HackTricks, and similar sources; never send traffic to them. Treat exploit code as untrusted: read it, verify version applicability, adapt it, never blind-run it.

## Roles and handoff

| Role | Access | Responsibility |
|---|---|---|
| Operator | Repository | Build, run, and seed the target; capture commit/build; write `BRIEF.md`. |
| Black-Box Attacker | Network only | Attack the running target; produce evidence; never read the repo. |
| White-Box Auditor | Repository | Read source after the attack phase; emit Candidate Findings. |
| Implementer | Repository | Apply approved fixes, add regression tests, commit one fix per Finding. |

Roles communicate through files, not memory, so they can run in separate sessions or on different models:

- `.redteam/ROE.md` — authorization and limits.
- `.redteam/BRIEF.md` — the only thing the Attacker receives.
- `.redteam/STATE.md` — round, commit, build hash, open findings, score, verdict.
- `.redteam/findings.json` — machine-readable findings.
- `.redteam/evidence/` — raw and redacted evidence.

The Attacker must not receive the repository path, source snippets, framework names, or audit notes. If the harness forces the same context, declare the run Gray-Box in the report.

## Capability tiers

Detect and record the tier at the start:

- **Tier A** — shell and Docker. Use an isolated container and a network-only attacker context when possible.
- **Tier B** — shell, host-run server. Run the target on loopback; isolate the Attacker in a separate session or subagent.
- **Tier C** — no shell. Static review only. No dynamic claims. Release Verdict is capped at CONDITIONAL.

If an optional tool is missing, substitute a `curl` or Python equivalent. Never skip a test class solely because a tool is absent; record the substitution.

## Round protocol

Each Round runs Phases 0–8. Phase 0 is completed once per engagement; Phases 1–8 repeat each Round.

0. **Authorize.** Write the ROE, confirm ownership, resolve targets, set the window and Proof Cap. Refuse without attestation.
1. **Bring up.** Operator builds, runs, and seeds the target on loopback. Capture `COMMIT` and `BUILD_HASH`. Create Test Identities (anonymous, user A, user B, admin where applicable) and seed owned objects. Write `BRIEF.md`.
2. **Attack.** Black-Box Attacker works from the BRIEF only. Recon, run the attack matrix, exploit, chain, capture evidence. Do not stop at the first hit.
3. **Audit.** White-Box Auditor reads the source and maps it to the matrix. Emit Candidate Findings for logic flaws, races, tenant leakage, crypto misuse, and unsafe parser paths the traffic could not show.
4. **Prove.** Send every Candidate back to the Attacker. Prove it or demote it to Suspected. Never report an audit guess as a Finding.
5. **Report.** Write the report and `findings.json`. Score, set the Release Verdict, fill the Coverage Matrix and residual risk.
6. **Fix.** The user approves, defers, or risk-accepts each Finding. The Implementer patches approved items minimally, adds a regression test or verification step, and commits once per Finding.
7. **Retest.** The original PoC must fail, the full regression suite must pass, and fresh bypass variants must fail. A failed retest reopens the Finding and consumes a Round.
8. **Verdict.** Recompute score and verdict. Stop at the Retest Gate, the Round cap, or an explicit user decision. Record risk acceptance for anything left open.

## Attack matrix

Every reachable class is mandatory. Open the matching playbook before testing the class, run at least the eight concrete tests it lists, and add app-specific variants. Skipping a test or a class requires a written reason in the Coverage Matrix.

| # | Class | Playbook |
|---|---|---|
| 1 | Recon and surface | `references/playbooks/01-recon-surface.md` |
| 2 | Authentication | `references/playbooks/02-authentication.md` |
| 3 | Session and tokens | `references/playbooks/03-session-tokens.md` |
| 4 | Authorization | `references/playbooks/04-authorization.md` |
| 5 | Injection | `references/playbooks/05-injection.md` |
| 6 | XSS and client-side | `references/playbooks/06-xss-client-side.md` |
| 7 | SSRF and network trust | `references/playbooks/07-ssrf-network-trust.md` |
| 8 | File handling | `references/playbooks/08-file-handling.md` |
| 9 | Deserialization and parsers | `references/playbooks/09-deserialization-parsers.md` |
| 10 | Business logic and state | `references/playbooks/10-business-logic-state.md` |
| 11 | API and realtime | `references/playbooks/11-api-realtime.md` |
| 12 | Infrastructure and config | `references/playbooks/12-infrastructure-config.md` |
| 13 | Secrets and supply chain | `references/playbooks/13-secrets-supply-chain.md` |

## Attacker Posture

This is the difference between a scanner and an intruder. Every behavior is mandatory:

- Think like a system abuser, not a compliance auditor. For every feature, ask how it can be turned against its owner: what it trusts, what it assumes, what it lets you repeat, skip, reorder, or change.
- Do not self-censor an allowed test because it looks aggressive. The ROE and the Proof Cap are the only limits; if a test is inside them, run it.
- Enumerate a feature's intended use, then attack adjacent uses.
- Treat every trust boundary as a target: client/server, tenant, role, parser, state machine, async job.
- Chain findings. Report the Exploit Chain as the unit of impact; two Mediums can be one Critical.
- Escalate read → write → execute → admin within the Proof Cap.
- Prefer the cheapest path to impact.
- Keep attacking after the first hit; one finding often unlocks the next.
- Treat tool output as a lead, never a Finding.
- Never stop at the first confirmed bug, and never pad the report with best-practice nitpicks that have no demonstrated impact.

## Evidence and reporting

A Confirmed Finding carries:

- Exact request and response, or a browser trace with timestamps.
- Identity used and the object owned by another identity.
- `COMMIT` and `BUILD_HASH`.
- Reproduction steps that a second person can follow.
- CVSS 3.1 vector, CWE, WSTG/API Top 10 mapping, confidence, and impact.

Report sections and the `findings.json` contract are in `references/report-schema.md`. Redact secrets and PII. Raw evidence stays local and `0600`; the report is safe to share.

## Score and verdict

Start at 100. Deduct for Confirmed Findings only:

| Severity | Deduction |
|---|---|
| Critical | −35 |
| High | −12 |
| Medium | −4 |
| Low | −1 |

Floor at 0. Fixed-and-retested Findings restore their points. Suspected Findings are unscored but cap the verdict at CONDITIONAL until triaged. Coverage below 90% caps the score at 79.

**Scoring unit.** A Finding that is a step in an Exploit Chain is scored through its chain, not again on its own. Compute the deduction as:

```
deduction = sum(severity weight of each Chain)
          + sum(severity weight of each Confirmed Finding that is in no Chain)
score     = max(0, 100 - deduction)
```

List component Findings in the report and the Findings table, but do not deduct them separately when a Chain covers them. If you cannot decide whether a set of Findings forms a Chain, score the components and record the Chain as unscored narrative; never deduct both.

Verdict precedence overrides the raw score:

- **BLOCK** — any open Critical or High, or score below 70.
- **CONDITIONAL** — any open Medium, unresolved Suspected High/Critical, coverage below 90%, or dynamic testing impossible.
- **PASS** — no open Critical/High/Medium, coverage at least 90%, and the Retest Gate met.

## Fix loop

The user approves each Finding individually. The Implementer patches only approved items, one commit per Finding, with a regression test or concrete verification step. Architecture-level issues become a Remediation Plan with an owner and explicit risk acceptance, not a superficial patch.

Retest Gate: the original PoC fails, the full regression suite passes, and fresh bypass variants fail, with no new Critical or High. A failed retest reopens the Finding and consumes a Round. The default cap is three Rounds.

## Stop conditions

Stop and report immediately on:

- Target unhealthy or unreachable after bring-up.
- Unexpected egress, external callbacks, or a redirect outside the allowlist.
- Real PII, live credentials, production data, or customer secrets.
- A test that could corrupt data or take the host down.
- Scope drift or a request to test a non-local target.

## References

Load only what the current phase needs:

- `references/roe.md` — authorization template and refusal rules.
- `references/glossary.md` — canonical terms for roles, Findings, Rounds, and the verdict.
- `references/methodology.md` — phases, two-lens model, test identities, coverage, scoring, anti-patterns.
- `references/report-schema.md` — report sections, `findings.json`, redaction.
- `references/remediation.md` — approval, fix quality bar, retest, rollback.
- `references/resources.md` — OWASP, Exploit-DB, HackTricks, PayloadsAllTheThings, SecLists, CWE, CVSS, and usage rules.
- `references/chains.md` — exploit-chain recipes and chaining rules.
- `references/playbooks/` — one playbook per attack class.
- `templates/` — ROE, BRIEF, STATE, report, findings schema.
- `scripts/` — bootstrap, reset, suite runner, evidence redactor, CVSS calculator, findings validator.

## Quick start

Run from the target repository; point `SKILL_DIR` at this skill folder.

```bash
SKILL_DIR=/path/to/redteam-self-audit
REPO_PATH="$PWD"

# 0. Protect local evidence
mkdir -p .redteam
cat "$SKILL_DIR/templates/gitignore.redteam" >> .gitignore

# 1. Authorize
cp "$SKILL_DIR/templates/ROE.md" .redteam/ROE.md   # fill it in and attest ownership

# 2. Bring up + seed (Operator)
bash "$SKILL_DIR/scripts/bootstrap-target.sh" "$REPO_PATH" 3000
cp "$SKILL_DIR/templates/BRIEF.md" .redteam/BRIEF.md

# 3. Attack (Black-Box Attacker; give it BRIEF.md only)
# 4. Audit (White-Box Auditor; separate context)
# 5. Report, approve fixes, retest
python3 "$SKILL_DIR/scripts/validate-findings.py" .redteam/findings.json --report .redteam/report.md
```

If the target is already running on loopback, skip bootstrap and write the BRIEF from the known URL and Test Identities.

## Honesty clause

No audit finds everything. This skill reports what was tested, what was blocked, and what remains. A PASS is a statement about the tested surface at a specific commit, not a promise of security.
