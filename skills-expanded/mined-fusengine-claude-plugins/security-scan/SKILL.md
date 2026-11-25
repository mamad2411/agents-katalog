---
name: security-scan
description: Use when scanning a codebase or a change for XSS, injection, command execution, SSRF, path traversal, weak crypto, hardcoded secrets, insecure deserialization or any OWASP Top 10:2025 vulnerability, and reporting verified findings.
argument-hint: "[--full|--diff [base]] [path]"
user-invocable: true
---

<objective>
This skill finds and reports application-code vulnerabilities. It combines a first-pass
pattern scanner shipped in `@fusengine/harness`, manual per-language patterns, optional
presence-checked tools (secret scanners, SAST engines), and a read-only refutation pass that keeps
only findings with confidence ≥ 8 and a concrete exploit scenario. Findings are mapped to CWE and
OWASP Top 10:2025 (plus the API Security Top 10 2023 for API code) and written to
`docs/security/YYYY-MM-DD-<scope>.md` in the audited repository.

It reports; it never fixes. Verified findings, each with a re-test check, go back to the caller.
</objective>

# Security Scan Skill

## Workflow

1. **Scope.** Full repository by default. When asked to review a change (`--diff`, a PR, a
   branch), limit the scan to the files changed against the merge base and say so in the report
   header:
   `git diff --name-only $(git merge-base HEAD <base>)` (default `<base>`: the branch the caller
   names, else `origin/HEAD`). Unchanged files are read only to trace data flow, not reported.
2. **Detect** languages and frameworks from project markers (`package.json`, `composer.json`,
   `pyproject.toml`, `requirements.txt`, `Package.swift`, `*.xcodeproj`, `go.mod`, `Cargo.toml`,
   `Gemfile`, `pom.xml`, `build.gradle*`, `*.csproj`) and from the file extensions actually present
   (`git ls-files | rg -o '\.[A-Za-z0-9]+$' | sort | uniq -c`).
3. **Automated first pass:**
   `bun ${CLAUDE_PLUGIN_ROOT}/../node_modules/@fusengine/harness/dist/cli/bin.mjs scan <dir>`
   This is a first-pass pattern scanner (one regex per line), not a complete audit. It prints one
   JSON report and always exits 0. Since `@fusengine/harness` 0.1.115 the report ends with a
   `coverage` block: that block is the coverage summary. The top-level `language` field is the
   first root marker found, in this order: `package.json`, `composer.json`, `requirements.txt` or
   `pyproject.toml`, `Package.swift`, `go.mod`, `Cargo.toml`, else `unknown`. It is not the list of
   scanned languages, but it decides which files get that language's legacy rules (18 in all) and
   are exempt from the skip rules and caps: only files with that marker's extension (`.js` for
   `package.json`, `.php`, `.py`, `.swift`; none for Go, Rust or `unknown`). Every other file gets
   only the precise rules (a bare `child_process` import is flagged in such a `.js` file, not in a
   `.ts` file). Each finding carries `id`, `cwe`, `owasp` (Top 10:2025, omitted when not verified)
   and `language`.
   - **Scanned with rules** (each also gets the secret rules): JS/TS family (`.js .jsx .mjs .cjs
     .ts .tsx .mts .cts .vue .svelte .astro`), PHP (`.php .phtml .inc`), Python (`.py .pyw`), Swift
     (`.swift`), Go (`.go`), Rust (`.rs`), Ruby (`.rb .rake .erb`), Java (`.java`), Kotlin
     (`.kt .kts`), C# (`.cs`).
   - **Scanned for secrets only** (reported as language `text`): `.env` and `.env.*` (not
     `*example`/`*sample`/`*template`, counted as `generated`), `.npmrc`, `.pypirc`,
     `.netrc`, and `.json .yaml .yml .toml .ini .cfg .conf .properties .xml .plist .gradle .sh
     .bash .zsh .tf .tfvars .pem .key`.
   - **Rule families per language** (pattern set `2026.11.2`; secrets and keys apply to every
     scanned file): JS/TS family — code execution, command injection, XSS, SQL injection,
     deserialization, weak crypto/randomness, TLS; PHP — code execution, command injection,
     deserialization, SQL injection, `include` of `$_GET`/`$_POST`/`$_REQUEST`/`$_COOKIE`, weak
     password hash, weak randomness; Python — code execution, command injection, deserialization,
     SQL injection, weak hash/randomness, TLS; Go — command injection, SQL injection, XSS
     (`template.HTML` & co.), weak crypto/randomness, TLS; Rust — `unsafe`, command injection, SQL
     injection, weak hash, TLS; Ruby — code execution, command injection, deserialization, SQL
     injection, weak hash, TLS; Java/Kotlin and C# — command injection, deserialization, SQL
     injection, weak crypto/randomness, TLS; Swift — `NSKeyedUnarchiver` deserialization,
     `UserDefaults` secret keys, weak hash. Swift `"http://` literals and `kSecAttrAccessibleAlways`
     are legacy-only rules: they run only when the root marker is `Package.swift` (never for an
     `*.xcodeproj`-only app). XSS has rules only for JS/TS and Go (none for PHP `echo`, Python,
     Ruby, Java, Kotlin, C# templates). Not covered by any rule: SSRF, open redirect, path traversal
     other than that PHP `include`, and anything outside these families (auth, access control,
     CSRF, GraphQL, ...).
   - **Reading `coverage`**: `languages`, `filesScanned` and `patternsApplied` (the largest rule
     count applied to one file of that language) list what was scanned. `totals.files: 0` or an
     empty `languages` means nothing was scanned (also the output for a wrong or missing path), never
     "clean". "Scanned" with no finding means no pattern matched, not "clean": the manual pass still
     applies. A language or extension found in step 2 but absent from `languages`
     was NOT scanned: other extensions (`.md`, `.html`, `.sql`, `.css`, ...) are ignored without
     being counted; `unsupported` lists only known code extensions with no rules (`.c .cpp .m
     .dart .lua .scala ...`, at most 10). `skipped` counts what was not scanned, by reason:
     excluded directories (`excludedDirs`), files (`binary`, `minified`, `oversize`, `unreadable`,
     `lockfiles`, `generated`), lines longer than the line limit whose tail was not matched by the
     non-legacy rules (`longLines`), and `capped: true`
     when the file or byte budget stopped the scan. `node_modules vendor .git dist build` are never
     scanned; framework and tool caches (`.next .venv Pods coverage`, `target` beside `Cargo.toml`,
     ...) are skipped except for files with the root marker language's extension (`.js` with
     `package.json`, `.php`, `.py`, `.swift`).
   Every language or file type present but not scanned, and every vulnerability class outside the
   rule families, is covered with the manual patterns below. An older harness prints no `coverage`
   block: then treat every detected language as not covered and apply the manual patterns to all
   of them.
4. **Manual patterns** for the languages not covered (or to complete the first pass):
   - JS/TS family (`.js .jsx .mjs .cjs .ts .tsx .mts .cts .vue .svelte .astro`), Next.js, TanStack
     Start, React, Astro → [scan-patterns.md](references/scan-patterns.md)
   - PHP / Laravel → [scan-patterns-php.md](references/scan-patterns-php.md)
   - Python, Swift/iOS, Go, Rust → [scan-patterns-extra.md](references/scan-patterns-extra.md)
   - Ruby, Java, Kotlin/Android, C# → [scan-patterns-other.md](references/scan-patterns-other.md)
   - GraphQL endpoint present → [graphql-security.md](references/graphql-security.md)
5. **Secrets** in every repository, any language → [secrets-patterns.md](references/secrets-patterns.md)
   (single source of secret patterns; optional git-history scan with a presence-checked tool).
6. **Optional SAST** when an engine is already installed (`command -v semgrep opengrep codeql`),
   with its licence conditions → [sast-tools.md](references/sast-tools.md). Never install a tool.
7. **Triage** every candidate → [triage.md](references/triage.md): refutation pass (source → sink,
   framework protections, reachability, test/doc/generated file), confidence 1-10, report only
   ≥ 8 with an exploit scenario, 5-7 to "needs manual review", then a second read-only pass.
   Severity is set by impact and exploitability there; it overrides the scanner's raw label and the
   "max severity" columns of the pattern references.
8. **Map** to CWE and OWASP Top 10:2025 → [owasp-top10.md](references/owasp-top10.md).
9. **Report** with [the report template](references/templates/scan-report.md): shared finding
   fields, scanner coverage (what really ran, what was absent), needs manual review, and a
   re-test check per finding. A secret value is never printed.

## Hand-off

The skill does not edit code and does not dispatch fixes. Return the report path and the
verified findings (id, severity, confidence, CWE, standard reference, `file:line`, evidence,
exploit scenario, recommendation, re-test check) to the caller, which decides who fixes them.

## Out of scope (peer skills)

Dependencies and lockfiles → [dependency-audit](../dependency-audit/SKILL.md); single-package CVE
lookups → [cve-research](../cve-research/SKILL.md); JWT/session/OAuth/password flows →
[auth-audit](../auth-audit/SKILL.md); HTTP headers, CSP, CORS →
[security-headers](../security-headers/SKILL.md); AI-agent configuration (hooks, MCP, skills) →
[agentic-security](../agentic-security/SKILL.md).

## References

- [OWASP Top 10:2025 mapping + API Security Top 10 2023](references/owasp-top10.md)
- [Patterns - JavaScript / TypeScript family](references/scan-patterns.md)
- [Patterns - PHP / Laravel](references/scan-patterns-php.md)
- [Patterns - Python, Swift/iOS, Go, Rust](references/scan-patterns-extra.md)
- [Patterns - Ruby, Java, Kotlin, C#](references/scan-patterns-other.md)
- [Secret patterns and git-history scanning](references/secrets-patterns.md)
- [GraphQL security patterns](references/graphql-security.md) — load when the target exposes a GraphQL endpoint.
- [Optional SAST engines and licences](references/sast-tools.md)
- [Triage: refutation, confidence, severity](references/triage.md)
- [Report template](references/templates/scan-report.md)
