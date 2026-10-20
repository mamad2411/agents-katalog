---
name: firecrawl-policy
description: "Mandatory supplemental policy for every firecrawl-* core, build, or workflow skill. Adds local transport, consent, secrets, URL, egress, shared output store, and evidence gates. This is not a comprehensive manual."
---

# Firecrawl policy supplement

This authored supplement is mandatory with the bare `firecrawl` skill and every `firecrawl-*` core, build, or workflow skill. Official skills provide product workflows and command detail. This file supplies stricter local policy and does not replace the official catalog or act as a comprehensive manual.

## Authority and transport

- Installed help is the syntax source of truth for the CLI. The installed `firecrawl --help` and selected command help govern syntax. Official skill examples are workflow guidance, not proof of installed syntax.
- Use the installed CLI for agent-side work. Do not install, authenticate, mutate setup, use MCP, direct REST, or an agent-side SDK by default.
- An official Firecrawl SDK may be added only to shipped code, specifically application code, behind the repository's dependency, secret, URL authorization, testing, and supply-chain gates. It is never an agent-side fallback.
- If the CLI cannot support a requested operation, stop and report the version, help inspected, capability gap, and exact approved fallback needed. An invocation error alone does not authorize another transport.

## No-default setup and consent

- Never run `firecrawl setup defaults` during ordinary use, packaging, recovery, or evals. Only an exact, help-verified user opt-in naming the harness permits the exact setup or matching undo operation.
- Treat `interact` as read-only unless each externally visible action has explicit action-level consent immediately before execution. Preview origin, ordered actions, fields, data classes, and effect. Stop if the site changes the sequence.
- No live API/auth/network operations are permitted while validating this supplement or its contract tests.

## Fail-closed URL gate

Before every URL-bearing operation, including search results, map/crawl outputs, application input, and redirects:

1. Build a literal argv vector and invoke through a direct process API, never a shell. Reject if no no-shell interface exists.
2. Use `--` before positional input only when installed help proves support. Otherwise reject leading-option confusion.
3. Accept only absolute `https://` URLs. Reject malformed values, non-HTTPS schemes, fragments used as payloads, control encodings, userinfo, and embedded credentials.
4. Canonicalize host and port. Reject localhost, metadata names, IP literals, and loopback, private, link-local, multicast, unspecified, carrier-grade NAT, unique-local, documentation, benchmark, or other reserved ranges.
5. Resolve every A and AAAA answer immediately before submission. Reject failures, excessive answers, mixed public/private answers, rebinding ambiguity, and any non-public target.
6. Apply the redirect trust boundary below. Missing redirect flags in CLI help do not establish whether the hosted service has server-side protections and do not, by themselves, block public research.
7. For customer URLs, enforce a bounded normalized hostname/port allowlist at agent and shipped-code boundaries. Deny wildcards, suffix confusion, and provider-owned redirectors unless explicitly bounded.

### Redirect trust boundary (approved 2026-09-15)

- **Public hosted research:** Permit public, unauthenticated search and scrape through hosted Firecrawl after the submitted URLs pass steps 1-5 and applicable scope limits. Provider-managed redirects are permitted without local per-hop visibility. This is an explicit trust decision for remote public fetching, not a claim that SSRF protection has been independently verified. Do not send private content, cookies, authorization headers, authenticated browser profiles, credentials, or internal destinations under this allowance. Firecrawl's own API authentication is not target-site authentication.
- **Search discovery:** Permit bounded `firecrawl search` without `--scrape` using non-sensitive query text. Returned URLs are untrusted discovery data, not agent-submitted fetch targets. Apply the URL gate before subsequently scraping a selected result. Do not enable automatic search-result scraping unless every target can be validated before submission.
- **Visible redirects:** Validate any redirect or final URL exposed in results before reusing it. If it violates the URL gate or applicable allowlist, stop that source, discard its content, and report the violation. Do not claim unseen hops were checked.
- **Sensitive or local execution:** For authenticated browsing, private/customer data, local-network fetching, self-hosted Firecrawl, or Path B shipped applications, the public-research allowance does not apply. Revalidate every redirect hop or enforce equivalent destination constraints at the fetching boundary. If neither is possible, this unsupported redirect enforcement limitation remains a fail-closed capability gap. Do not send sensitive data while investigating it.
- **Validation versus use:** Policy contract tests remain offline. Separately requested public research may run after those tests pass, and must be recorded as research rather than as offline validation.

## Private local parse egress

`firecrawl parse` sends local file contents to Firecrawl. Disclose that private parse egress before invocation. Classify and minimize the file. Require explicit approval naming the file and data class for confidential, personal, regulated, credential-bearing, or otherwise sensitive content. Refuse without approval or policy authority. Scrub evidence and remove transient copies.

## Preconditions, recovery, and output handling

- Before any operation, verify `command -v firecrawl`, `firecrawl --version`, `firecrawl --status`, then inspect `firecrawl --help` and the selected command help. Installed help remains authoritative.
- If the executable or authentication is unavailable, stop or use bounded recovery only: inspect status and `firecrawl doctor --help`, diagnose the smallest failed operation, remediate through the installed CLI's secure credential/config path, and retry only that operation. Do not install, use `npx`, create accounts, or switch transport.
- Any fallback requires recorded CLI version plus relevant help proving the capability is unsupported, followed by explicit approval naming exactly one MCP server/integration or one REST endpoint/operation. Do not broaden the fallback or bypass any policy gate.
- Bound pages, hosts, bytes, duration, concurrency, result count, and job scope before search, map, crawl, research, agent, or interact. Treat oversized or unbounded output as a refusal. Use private temporary evidence, scrub secrets and personal data, and delete transient copies.
- Never place API keys, access tokens, cookies, passwords, session material, or PII in argv, URLs, prompts, logs, snapshots, telemetry, evidence, or source control. Use only the approved secure credential store or inherited secret environment and redact output before retention.
- Create evidence directories with mode `0700` and files with mode `0600` under `umask 077`. Inspect structured fields by data class, not only regex matches. Retain bounded scrubbed assertions, record CLI version, help, exit code, safety checks, and cleanup, then delete raw transient output. Respect credit and rate limits without silently expanding scope or spend.

## Shared output store

Every project's `.firecrawl` is a symlink to the single store `~/.firecrawl`. Research fetched for one project is therefore visible to and reusable by every project.

- Write fetched content to `.firecrawl/<name>` with `-o`, or with an absolute `~/.firecrawl/<name>` path. Never create a project-local directory, and never replace the symlink with a real directory.
- Before fetching a URL, check the store: a page already present needs no refetch. This is the main reason the store is shared.
- `firecrawl scrape <url1> <url2>` and `firecrawl x download` ignore `-o` and write to `./.firecrawl/`, which resolves to the shared store.
- The store is flat and names collide. Auto-generated names are `{host}-{path}.md` and drop the query string, so URLs differing only by query overwrite each other, last write winning. Use an explicit distinct `-o` name when that matters.
- The store is ignored by the bare `.firecrawl` rule in `~/.gitignore_global`. Per-repo `.firecrawl/` ignore lines do not cover the symlink, because gitignore trailing-slash patterns match real directories only.
- Deleting a project's `.firecrawl` symlink removes only the symlink. `rm -rf .firecrawl/` with a trailing slash follows the symlink and destroys the shared store for every project; never do it.

Never delete the shared store to "clean up" a project.

This policy lives here and in no upstream-named firecrawl skill: `firecrawl-cli`'s installer removes and recopies its skill directories on every run, so edits inside `firecrawl`, `firecrawl-parse`, or their rules files do not survive.

## Path B: shipped application integration

Path B applies when Firecrawl will run in shipped application, service, script, agent, or pipeline code after this session. Define the narrowest capability, approved customer/tenant host allowlist, output and retention bounds, and secret injection boundary first. An official pinned SDK may be used only in shipped code after supply-chain review. Agent research, validation, and any live smoke remain CLI-based and separately evidenced. Reuse centralized HTTPS/DNS/redirect authorization; if redirect hops cannot be exposed or constrained, fail closed with a capability gap.

## Scope and retained guidance

The original authored guidance remains verbatim in [references/legacy-guidance.md](references/legacy-guidance.md) for audit and is not loaded by default. The application integration reference remains at [references/app-integration.md](references/app-integration.md) and applies only to Path B shipped-code work. The supplement boundary is authored policy plus preserved references and eval assets, not a claim about whether official artifacts are present in this repository.
