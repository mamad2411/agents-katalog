---
name: security-review-gate
description: Security review for changes that cross a sensitive boundary. Use when a change or pull request adds or alters authentication, authorization, permissions, sharing or tenancy, private or personal data, secrets, untrusted input, payments, or file and network access, and before merging it.
---

# Security review gate

Works beside `review-gate`, which holds the pull request protocol, reviewer independence, the two review rings and finding dispositions; install both (`npx skills add finolabs/vibecode --skill review-gate`).

## Triggers

Every pull request gets a security review (`review-gate` "Pull requests"). Inside a pull request's work, a change needs security scrutiny of its own when it touches any of:

- authentication, sessions, tokens or credentials handling;
- authorization: permissions, roles, grants, tenancy, sharing, scopes;
- private or personal data, its storage, export, logging or deletion;
- untrusted input: parsing, queries, templates, uploads, paths, deserialization, prompts sent to models;
- payments or other irreversible effects;
- network, file system or process boundaries opened to outside callers;
- data leaving the system: bulk export, webhooks and calls to third parties.

Name the triggered boundaries in the receipt. A trigger raises depth to at least NORMAL (`coding-router`).

## Scope of the review

- **Diff review** covers an exact diff or commit range; **audit** covers an authorized wider scope. Fixing findings or verifying fixes needs its own explicit scope.
- The reviewer is independent, as `review-gate` says, with the security coverage named in the packet.
- A diff review uses the two rings of `review-gate` "Review scope", with the second ring traced along **trust paths**: every entry point that reaches the changed code (API routes, CLI commands, background jobs, tool calls and model prompts), the authentication and authorization checks on each path, and every store and output the changed code writes (databases, caches, search indexes, logs, exports).
- When no trigger matches, the report is short: the trust paths checked and the verdict.
- Code and security review run as separate reviewers in parallel by default; one reviewer covers both only when scoped policy permits and the packet names both coverages.

## Instruments

- **Diff review**: when a trigger matches or the diff is about 500 changed lines or more, `security-audit` in its focused mode on the diff, where it is installed; that mode supplies method, not findings, so follow it while you read the diff yourself, and only a tool that reports findings counts as an engine. Otherwise, and for a small diff with no trigger, the host's native security review: Claude Code `/security-review`; Codex `codex review` with the triggered boundaries named in the prompt. Antigravity has none: its reviewer works through this gate by hand, and a native pass runs on one of those two where reachable.
- **Audit**: recommend `security-audit` from [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) (MIT; `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit`). It runs reconnaissance, coverage-led hunting and independent verification of every finding. Recommend it before a repository goes public, before a first release, after a change to the authentication, authorization or tenancy design, and on a regular schedule for services that hold private data. It spends many agent runs: give it its own budget and the owner's go.
- Without these, an independent reviewer runs the permission-boundary review and other checks below by hand and tells the caller that `/setup` guides installing the missing instrument.

## Permission-boundary review

For every protected resource and action the change touches:

1. List each actor class: owner, permitted member, other member, other tenant, anonymous, revoked or expired grant.
2. For each, state the expected result of read, list, search, write and delete.
3. **Negative tests** prove denial for every actor that must be denied, through every entry point that reaches the resources and actions the change touches (API, CLI, tool, search, export, background job), not through every entry point of the system. A missing negative test for a denial the change relies on is MEDIUM; for a path the change does not touch, LOW.
4. **No existence leak**: a denied caller gets the same response as for a resource that does not exist: same status, same error shape, no count, timing or field that tells them otherwise. Search, list and count paths never include hidden items.
5. Revocation takes effect on the next request, including cached and long-lived paths.

## Other checks

- Secrets never appear in code, commands, logs, test fixtures or commits; credentials come through the approved injection mechanism.
- Untrusted input is validated at the boundary and parameterized at the sink.
- Errors and logs carry no secrets or personal data beyond what the purpose needs.
- New dependencies are pinned, from a trusted source, and justified.

## Findings

Dispositions, regression tests, re-review and the severity scale (CRITICAL, HIGH and MEDIUM block, LOW does not) follow `review-gate`. A finding rated MEDIUM or higher names a concrete exploit scenario through a real trust path; a general hypothesis is LOW. A concern on a triggered boundary that the repository cannot settle, because it depends on a fact outside it (a proxy rule, an identity provider setting), is **NEEDS-VALIDATION**: it blocks like MEDIUM until the owner validates it or accepts the risk. A security finding that is accepted as risk needs the owner's explicit approval. On any secret or personal-data leak: stop, tell the owner, keep the traces for rotation.
