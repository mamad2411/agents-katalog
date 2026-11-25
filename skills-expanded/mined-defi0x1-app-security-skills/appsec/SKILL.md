---
name: appsec
description: "Code reviewer with one entry point: /appsec. Use whenever the user wants code reviewed: current-branch work including uncommitted and new files ('review my changes', 'review this branch'), a Merge/Pull Request by number or URL ('review MR 123'), several MRs, or a whole repo/directory ('audit the whole repo', 'pre-pentest sweep'). Auto-detects scope and risk, no questions; runs two equal tracks: SECURITY (OWASP/CWE: injection, access control, auth/session, SSRF, XSS, deserialization, crypto, DoS, race, secrets, supply chain, CI/CD, mobile MASVS, LLM/agent/MCP, domain hunting (HTTP smuggling, OAuth/SAML, tenant isolation, cloud IAM, native memory); invariant-based hunting, 5 verification gates, 'needs validation' verdict) and CODE (correctness, business logic vs spec, migrations/API compatibility, performance, over-engineering, tests, conventions; 4 gates). Large or risky changes get the deep engine: recon, coverage table, parallel hunters, independent verifiers. Returns a merge verdict."
---

# appsec

One purpose: **code review**. One command: **`/appsec`**. Everything after it is optional plain language, not flags:

| Goal | Example |
|---|---|
| Work in progress on this branch (including uncommitted, new files) against the target branch | `/appsec` |
| MR/PR by number or link | `/appsec 123`, `/appsec !123`, `/appsec <URL>` |
| Anything else | `/appsec against develop`, `/appsec uncommitted only`, `/appsec be thorough`, `/appsec audit the whole repo`, `/appsec src/billing`, `/appsec 123. Spec: ...` |

The skill decides scope, standard or deep review, which domains to hunt, and the independent reviewer on its own; it does not ask again unless it cannot continue. It always reviews two equal tracks: **Security** and **Code** (logic, business rules, design, over-engineering, performance, tests, conventions). Respond in the user's language (default English); keep code and identifiers in English.

**Follow [workflows/review.md](workflows/review.md).** Deep review (large/risky diff, whole repo, or the user says "thorough") automatically moves the Security track to [workflows/review-deep.md](workflows/review-deep.md).

If the user asks a single question about secure coding, severity, or CWE instead of requesting a review: answer briefly from the references, citing the specific section.

## References

Read only the file you need, not all of them.

| File | Content |
|---|---|
| [references/code-review.md](references/code-review.md) | Code track: BLOCKER/MAJOR/MINOR/NIT severity, 4 gates, intent sources, 9 hunting groups, over-engineering table |
| [references/secure-coding-patterns.md](references/secure-coding-patterns.md) | Security: wrong, bypass, correct fix; known-safe |
| [references/hunting-method.md](references/hunting-method.md) | Invariant-based hunting, six trust-boundary-outcome points, Needs validation verdict, hardening, safe verification, **domain selection table**, feature abuse, vulnerability chaining, wildcard, anti-patterns |
| [references/domains/](references/domains/) | Domain hunting: `web-auth`, `client-side`, `data-isolation`, `resource-exhaustion`, `protocols-messaging`, `cloud-deployment`, `ci-release`, `local-ipc-desktop`, `native-memory`. Open only the file whose boundary the diff/repo touches |
| [references/severity-cwe.md](references/severity-cwe.md) | Severity anchor scale, severity table, CWE; "not a security finding" |
| [references/change-classification.md](references/change-classification.md) | 10 change groups, sensitive code areas, signal-collecting commands |
| [references/supply-chain-devsecops.md](references/supply-chain-devsecops.md) | Lockfile, dependency sources, CVE, SBOM, CI tokens, pipeline |
| [references/secure-design.md](references/secure-design.md) | Cross-checking a large MR or new integration against security design notes, authz matrix, acceptance criteria |
| [references/ai-llm-security.md](references/ai-llm-security.md) | OWASP LLM Top 10 2025, lethal trifecta, hunting RAG/memory/agent/MCP bugs |
| [references/mobile/](references/mobile/) | `lessons.md`, `android.md`, `ios.md`, `cross-platform.md` |
| [references/report-template.md](references/report-template.md) | Report template |
| [references/multi-mr.md](references/multi-mr.md) | MR by IID (GitLab/GitHub), multiple MRs, multiple repos |
| [references/tob.md](references/tob.md) | Trail of Bits plugin (optional) |

## Fixed principles

1. Every finding must have `file:line` evidence and pass the verification gates of its track (Security 5 gates, Code 4 gates). A Security finding names the less-trusted principal, the control that should have blocked it, the boundary crossed, and the concrete outcome. A serious finding must pass adversarial challenge, ideally by a different subagent from the one that found it. Never report on feeling or taste.
2. Few and correct beats many and noisy. Unsure about business rules: ask a question, do not conclude. Depends on facts outside the repo (proxy, IdP, IAM, ingress, browser): record **Needs validation**, assign no severity, do not guess either way. Missing a defense layer when another layer already blocks it: hardening, not a finding.
3. Controls are decided on the server; identity, tenant, role come from a verified token. Allowlist over blocklist. Fix the root cause.
4. Simple is the default: every abstraction must serve a current requirement; a design proposal always comes with a simpler version.
5. Commit the lockfile; dependencies and base images come from controlled sources. Secrets stay out of code, images, logs, prompts; once on the remote it is exposed: rotate.
6. Block the merge only for issues caused by this change; pre-existing bugs go in the Context section.
7. The report talks only about code: no who ran it, machine, time, email, internal URL.
8. The review is read-only and leaves no trace in the project: do not edit code, create files, config, hooks, refs, worktrees (only `git fetch` updating remote refs is fine), do not checkout, stash or change branches. Do not fix code or post comments unless the user asks. Files that must be saved (report, coverage) go in `~/.claude/appsec-reviews/`.
9. Verification is source-based; do not probe deployed environments, external services, or real data or credentials. Run repo code only when needed to settle a candidate, with fake data, no network, no dependency installation; if that cannot be guaranteed, do not run it and record Needs validation.
