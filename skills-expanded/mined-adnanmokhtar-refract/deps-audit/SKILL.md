---
name: deps-audit
description: Run the ecosystem's dependency audit (npm / pip / cargo / composer / go) and triage the findings, separating blockers from noise. Run before every release, after a fresh install, when a new advisory lands, and weekly in CI. Scans the manifest and lockfile — `release-security` is what scans the built container image's OS layer.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# deps-audit

Run the package-manager audit and convert raw CVE noise into prioritized actions.

## Premise

Find real issues, no hand-waves. Every finding cites the advisory id (CVE / GHSA), the affected package + version range, the fixed version, and the consumer site (`<path:line>` for runtime deps; "transitive via `<parent>`" for indirect). Severity is the advisory's severity AND the surface analysis ("runtime path reachable from user input" vs "dev-only build script"); "high CVE" alone is not a verdict. Risk-accepted findings name the unreachable code path and what would change that. Triage that says "upgrade everything" without surface analysis is noise.

## Halt conditions

- Halt on findings missing CVE/GHSA id or fixed-version field.
- Halt on severity escalation ("CRITICAL — fix today") without naming the reachable consumer path (`<path:line>` or "transitive via X, unreachable").
- Halt on `audit fix --force` recommendations that cross majors without a regression-test plan.
- **Halt on any advisory id you did not re-read.** Package, class and fixed version all come from the advisory record, never from recall — see § Reading the output, "the class is part of the finding".

## Prerequisites

- Project's package-manager CLI (`pnpm`, `npm`, `yarn`, `pip`, `cargo`, `composer`, `go`, `bundle`).
- `osv-scanner` 2.x, or docker for the `ghcr.io/google/osv-scanner` one-shot.
- `jq` for JSON parsing.
- Internet access — audit DBs, EPSS and the KEV feed are remote. Without it, § Offline mode.

## Procedure

1. Run the right tool for the stack — **osv-scanner plus the package manager's own audit**, not one or the other: `pnpm audit` / `npm audit` cannot see a dependency resolved from a URL or tarball (measured: a CDN-pinned `xlsx` tarball was invisible to `pnpm audit` and matched two advisories in osv-scanner), and osv-scanner has no reachability or `--prod` view.
   ```bash
   # Cross-ecosystem (osv-scanner 2.x; the 1.x form `osv-scanner --lockfile=<path>` is still accepted by 2.6):
   osv-scanner scan source --lockfile=<path> --format json > /tmp/osv.json     # or: osv-scanner scan source -r .
   # Not installed → the image, only when it is already local (an audit never pulls it); neither → print
   # NOT-RUN (osv-scanner not installed — to enable: brew install osv-scanner, or docker pull ghcr.io/google/osv-scanner). Pipe the lockfile in: a bind mount from a path Docker Desktop does not share comes up
   # empty and osv exits 127 "could not determine extractor". The image's binary is /osv-scanner, not on PATH.
   docker run --pull=never --rm -i --entrypoint sh ghcr.io/google/osv-scanner -c \
     'mkdir /w && cat > /w/pnpm-lock.yaml && /osv-scanner scan source --lockfile=/w/pnpm-lock.yaml --format json' \
     < pnpm-lock.yaml > /tmp/osv.json            # name the file as the lockfile type, or prefix it: --lockfile=pnpm-lock.yaml:/w/lock
   # Node — NOTE the schema differs by tool/version:
   npm audit --json --omit=dev > /tmp/audit.json     # npm 7+ → top-level `.vulnerabilities` (NOT `.advisories`)
   pnpm audit --json > /tmp/audit.json               # pnpm → legacy `.advisories`; run it once more with --prod and diff
   # Python
   pip-audit --format json --output /tmp/audit.json
   # Rust
   cargo audit --json > /tmp/audit.json
   # PHP
   composer audit --format=json > /tmp/audit.json
   # Go
   govulncheck -json ./... > /tmp/audit.json
   # Ruby
   bundler-audit check --update --format json > /tmp/audit.json
   ```
   A docker row is RAN only when stderr says `found N packages` with N > 0.
2. Parse (schema-aware — pick the shape your tool emits):
   ```bash
   # npm 7+  (top-level .vulnerabilities, keyed by package):
   jq '.vulnerabilities | to_entries[] | {name:.key, sev:.value.severity, via:.value.via, range:.value.range, fix:.value.fixAvailable}' /tmp/audit.json
   # pnpm / npm 6  (.advisories) — GHSA-only advisories have an empty `cves`; `paths` is the "transitive via X" line:
   jq '.advisories | to_entries[] | {name:.value.module_name, sev:.value.severity, ghsa:.value.github_advisory_id, cve:.value.cves, vuln:.value.vulnerable_versions, fix:.value.patched_versions, via:[.value.findings[].paths[]]}' /tmp/audit.json
   # osv-scanner  (.results[].packages[]) — max_severity is a CVSS score, aliases carry the CVE:
   jq '.results[].packages[] | {name:.package.name, version:.package.version, ids:[.vulnerabilities[].id], aliases:[.vulnerabilities[].aliases[]?], cvss:[.groups[].max_severity]}' /tmp/osv.json
   ```
3. **Read it — see § Reading the output.** This is the step that turns a scanner dump into an audit; skipping it produces a re-formatted dump.
4. Score exploitability for every CVE that survives step 3 — EPSS takes a comma-separated list; KEV is one JSON feed:
   ```bash
   curl -s 'https://api.first.org/data/v1/epss?cve=CVE-2024-28849,CVE-2021-23337' | jq -r '.data[] | "\(.cve)  epss \(.epss)  pct \(.percentile)"'
   curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json -o /tmp/kev.json
   jq -r --arg ids 'CVE-2024-28849 CVE-2021-23337' '.catalogVersion as $v | .vulnerabilities[] | select(.cveID as $c | $ids | split(" ") | index($c)) | "\(.cveID) in KEV since \(.dateAdded) (catalog \($v))"' /tmp/kev.json
   ```
   A GHSA with no CVE alias has no EPSS or KEV entry — say so in the row rather than leaving the field blank.
5. Classify each finding:
   - **Critical/High on a runtime dep with a reachable path** → blocker, fix today.
   - **Medium on runtime dep** → fix this sprint.
   - **Any severity on dev-only dep** → backlog. Exception: a build-time dep executes on your CI runner with your CI secrets — a post-install-script or build-tool RCE is *not* dev-only risk.
   - **Transitive dep where the vulnerable function is never called from your code** → risk-accepted, and name the import that would change that.
   - **Direct dep whose vulnerable configuration is off** (a fix for an HTTP/2-only crash on a server that never enables HTTP/2) → risk-accepted **and** take the patch when it stays inside the declared range; name the setting or call (`http2: true`, `reply.trailer()`) that would make it reachable.
6. **Diff against the last recorded audit** (`ai/audits/*-security*.md`, or the CI job's previous run): mark each id `new since <date>` or `carried`, and give each carried id's age. An advisory published after the last audit is why that audit was clean — the row says so instead of reading as a regression.
7. Confirm the upgrade path won't break, then apply the minimal bump:
   ```bash
   pnpm why <package>          # transitive ancestry — who forces the old version
   npm outdated <package>      # current vs wanted vs latest
   pnpm up <package>@<fixed-version> && pnpm test
   ```

## Offline mode (`--offline`)

When the audit may not reach the network (a read-only audit rule, an air-gapped runner, no registry credentials), the advisory lane needs a database already on disk, and everything else still runs. Never call `pnpm audit` / `npm audit` (they query the registry), `pnpm why` (it may touch the store in a read-only target), or the EPSS and KEV `curl`s.

- **Advisories, only from a local DB.** `osv-scanner scan source --offline --lockfile=<path>` reads a database downloaded earlier (`--download-offline-databases` on a networked run; the directory is `$OSV_SCANNER_LOCAL_DB_CACHE_DIRECTORY`, else Go's user cache dir) and errors when none is present (google.github.io/osv-scanner offline-mode, read 2026-10-15). trivy needs its vulnerability DB in its cache (`~/Library/Caches/trivy/db/trivy.db` on macOS); a cache holding only `policy/` has no advisories. No DB → the advisory row is **NOT-RUN (offline: no local advisory DB)**, never clean, and every carried id from the last audit is re-checked by version only.
- **What the offline run still emits:** (a) the resolved versions of the packages that matter — each prior finding's package, the overrides, the HTTP framework, the parsers and sanitizers; (b) each override or resolution against the version it was meant to force (`pnpm.overrides` `>=5.12.1` with 5.12.3 locked is carried, not new); (c) every dependency resolved from a URL or tarball, which the registry audits cannot see; (d) § Supply-chain settings.
- **pnpm lockfile v9** (`lockfileVersion: '9.0'`): the `packages:` keys carry `name@version(peer…)`, and `importers:` says which workspace declares a dependency directly. The reader below prints both, and the tarball resolutions, without pnpm:

```bash
python3 -I - pnpm-lock.yaml '^(fastify|dompurify|xlsx|lodash)$' <<'PY'   # second arg: a package-name regex
import re, sys, collections
pat = re.compile(sys.argv[2] if len(sys.argv) > 2 else '.')
sec = imp = dep = None; ver = collections.defaultdict(set); direct = collections.defaultdict(set); url = []
for line in open(sys.argv[1], encoding='utf-8'):
    line = line.rstrip('\n')
    if re.match(r'\S', line): sec = line.rstrip(':'); continue
    if sec == 'importers':
        m = re.match(r"^  (\S.*):$", line)
        if m: imp = m.group(1).strip("'"); continue
        m = re.match(r"^      '?([^':]+)'?:$", line)
        if m: dep = m.group(1); continue
        m = re.match(r"^        version: '?([^'(\s]+)", line)
        if m and dep and pat.search(dep): direct[dep].add(imp + ' -> ' + m.group(1))
    elif sec == 'packages':
        if re.match(r"^  \S.*:$", line):
            k = line.strip()[:-1].strip("'").split('(')[0]; i = k.find('@', 1)
            if i > 0 and pat.search(k[:i]): ver[k[:i]].add(k[i + 1:])
        if re.match(r'^\s+resolution: \{[^}]*tarball:', line): url.append(line.strip())
for n in sorted(ver): print(f"{n}: {', '.join(sorted(ver[n]))}" + ("   direct in " + '; '.join(sorted(direct[n])) if n in direct else ''))
for u in url: print('URL/TARBALL', u)
PY
```
Measured 2026-10-15 on a real NestJS + React monorepo's v9 lockfile (1,596 packages): it printed the framework and sanitizer versions the prior findings named, the direct importer of each, and the one CDN tarball dependency (`xlsx`) that the CI `pnpm audit` gate never covers. The advisory lane was NOT-RUN there (no local DB).

## Reading the output

The scanner answers "does a published advisory match a version in my lockfile". It does not answer "am I exploitable". Five things it will not tell you, in the order they cause wrong verdicts:

- **Reachability is yours, with one exception.** `npm audit`, `pip-audit`, `composer audit` and `bundler-audit` match the manifest — they flag a package, not a call. **`govulncheck` is the exception**: it does call-graph analysis, "prioritizing vulnerabilities in functions that your code is actually calling" (<https://go.dev/blog/govulncheck>). So on Go a clean report means more than it does anywhere else, and everywhere else "reachable" is a claim you make with a `<path:line>`, not one the tool made for you.
- **The class is part of the finding, and recall gets it wrong.** Open the advisory record and copy the package, the class and the fixed version from it. Two ids that live next to each other in every triage list: **CVE-2021-23337** is lodash *command injection via the `template` function* (fixed 4.17.21) — not prototype pollution, which is a different pair of ids; **CVE-2024-28849** is *follow-redirects* leaking the `proxy-authorization` header across a cross-domain redirect (fixed 1.15.6) — not axios, not SSRF. A report that mislabels the class sends the reader to audit the wrong code path, which is worse than no report.
- **"Fix available" is not always a patch.** The fix field may point at a major bump. Check whether the fixed version satisfies your declared range before you promise a one-line upgrade, and whether the version is reachable at all — a transitive pin (`pnpm.overrides` / `resolutions`) may be the only path when the parent has not released.
- **Severity is the advisory's blast radius, not yours.** Prioritize by CVSS **+ EPSS** (probability of exploitation in the next 30 days) **+ CISA KEV** (known-exploited-in-the-wild): a KEV-listed or high-EPSS Medium outranks a theoretical Critical. Then adjust down for an unreachable path — and record which of the two moved the row.
- **A match with no `fixed` event is not proof the installed version is affected.** When the fix shipped outside the registry (SheetJS publishes to its own CDN, not npm), the record's npm range is `introduced: 0` with no `fixed`, so osv-scanner matches every version. Read `affected[].database_specific.last_known_affected_version_range` (`curl -s https://api.osv.dev/v1/vulns/<id>`) before believing it: measured, `xlsx` 0.20.3 matched two advisories whose last affected versions were `< 0.19.3` and `< 0.20.2` — refuted on version.

CI wiring: `npm audit`'s exit code is governed by `--audit-level` ("the minimum level of vulnerability for `npm audit` to exit with a non-zero exit code" — <https://docs.npmjs.com/cli/v11/commands/npm-audit>). A job that never fails is usually a threshold, not a clean tree. A gate like `pnpm audit --prod --audit-level=high` narrows twice: `--prod` drops the build-time deps that run with CI credentials, and `high` lets every moderate through — two advisories published the day before one measured run passed such a gate silently. Report the gate's blind spots as a row, and add an `osv-scanner` step so URL and tarball deps are covered at all.

## Supply-chain settings

`sast-scan` files semgrep's `package_managers.*` hits here (CWE-829 / CWE-1104). They are not CVEs; they are the settings that decide how fast a hijacked release reaches the lockfile. Read the setting the **installed** manager version honours, in the file it reads it from, before filing: npm `min-release-age` (npm ≥ 11.10, `.npmrc`), pnpm `minimumReleaseAge` (minutes, ≥ 10.16), `trustPolicy: no-downgrade` (≥ 10.21) and `blockExoticSubdeps: true` (≥ 10.26) in `pnpm-workspace.yaml`, Yarn `npmMinimalAgeGate`, uv `exclude-newer`, Dependabot `cooldown`, Renovate `minimumReleaseAge`. A rule written for one manager fires on another manager's file — a pnpm repo's `.npmrc` trips the npm rule. Each row: the setting, its current value or absence at `<file:line>`, the manager version from `packageManager` / the lockfile, and the value to set. Low, Hardening — unless the gap already let a known-bad version in.

## Output

```
Dependency audit — 3 findings

CRITICAL:
  follow-redirects@1.15.5   CVE-2024-28849   proxy-authorization header retained on cross-domain redirect (credential leak)
    Fixed:  1.15.6
    Used:   transitive via <http client dep> → runtime, reachable
    Surface: outbound requests configured with a proxy + user-influenced target host — the
             credential leaves to a host we do not control.
    Action: pin the fixed version (transitive override if the parent lags); re-run outbound tests.

MEDIUM:
  lodash@4.17.20   CVE-2021-23337   command injection via the `template` function
    Fixed:  4.17.21
    Used:   transitive via <lint plugin>
    Surface: dev-only — `template` is not called on any runtime path (no import found).
    Action: upgrade with the next dep refresh; re-check if `template` ever enters runtime code.

LOW:
  semver@5.7.1   CVE-2022-25883   ReDoS in `new Range` on untrusted range strings
    Fixed:  5.7.2 / 6.3.1 / 7.5.2
    Used:   transitive (deep), build-time only
    Surface: no untrusted string reaches a range parse.
    Action: bundle with the next routine dep refresh.
```

Every row is (advisory id → class copied from the record → fixed version → consumer path → surface sentence → action). A row missing the surface sentence is a scanner line, not a finding.

## False positives / gotchas

- Vulnerable but unreachable: a CVE in a sub-feature you don't import is real risk only if the import surface changes — flag with the import that would change it, don't panic.
- `npm audit fix --force` upgrades across majors — read the changelog, run tests, never apply blindly.
- Some advisories are duplicates from different sources (GHSA + npm + Snyk) — dedupe by CVE id (by GHSA id when the record has no CVE alias), and keep the record you actually read.
- `--omit=dev` narrows the *scope of the scan*, not the risk: it hides build-time deps that run on CI with CI credentials.
- A docker one-shot that scanned an empty mount still exits non-zero and looks like a run. Measured on macOS with a repo under `/private/tmp`: `-v "$PWD:/src:ro"` gave osv exit 127, "could not determine extractor"; piping the lockfile in (§ Procedure step 1) scanned 1,706 packages.
- Pinned transitive overrides (`pnpm.overrides`, `resolutions`) can fix vulns without waiting on the parent dep — preferred when a parent is slow to release, and the only lever when it is abandoned.

## Related

- `/dependency-vuln-check` — the periodic session that wraps this skill: license compatibility, maintainer health, supply-chain markers, and the persisted report. This skill is its CVE dimension; run the skill for a scan, the command for an audit of record.
- `@security-auditor` — names this skill as its vulnerable-components executor; an A0x supply-chain finding without a resolved advisory id from here is not shippable.
- `rules/security-principles.md` — the vulnerable-components MUSTs this skill enforces.
