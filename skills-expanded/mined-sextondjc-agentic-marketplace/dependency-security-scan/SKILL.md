---
name: dependency-security-scan
description: Use when scanning workspace or target repository dependencies for known CVEs, outdated packages, and license risks with deterministic SBOM generation and remediation-ready findings.
---

# dependency-security-scan

## Specialization

Deterministic dependency vulnerability scanning covering CVE identification, SBOM generation, severity classification, and remediation-ready findings for .NET (NuGet), JavaScript/TypeScript (npm/yarn), and Python (pip) ecosystems.

## Objective

Scan all resolvable dependency manifests in scope, produce an authoritative Software Bill of Materials (SBOM), identify known CVEs against current advisory databases, classify findings by severity, and output a remediation-ready findings artifact with an explicit gate signal: **PASS / CONDITIONAL / BLOCK**.

## Trigger Conditions

- Phase P7a (Security Review) in the workspace delivery pattern when the change includes code or configuration that references packages
- CI/CD pipeline gate requiring dependency-clean evidence before merge or promotion
- Periodic posture audit of a repository's dependency estate
- Before onboarding a new package dependency into a workspace asset or target repository
- Any delivery requiring evidence of dependency hygiene for release readiness

## Scope Boundaries

**In scope:**
- NuGet packages (`*.csproj`, `packages.lock.json`, `Directory.Packages.props`)
- npm / yarn packages (`package.json`, `package-lock.json`, `yarn.lock`)
- Python packages (`requirements.txt`, `pyproject.toml`, `Pipfile.lock`)
- Transitive dependency analysis (depth-mode dependent)
- SBOM generation (CycloneDX-compatible table or structured markdown format)
- CVE lookup against NVD, GitHub Advisory Database, and OSV
- Severity classification (CRITICAL / HIGH / MEDIUM / LOW / INFORMATIONAL)
- Remediation recommendations (upgrade path, replacement, risk-acceptance rationale)

**Out of scope:**
- Runtime application security testing (DAST) — use `security-research`
- Source code static analysis (SAST) — use `security-research`
- Infrastructure and network security — use `security-research`
- License compliance checking — `license-compliance` skill (future, gap G2)
- Secrets scanning — use a dedicated secrets detection tool; outside this skill's scope

## Inputs

| Input | Required | Description |
|---|---|---|
| Repository path or manifest file list | Yes | Root path to scan, or explicit list of manifest files |
| Severity threshold | No | Minimum severity to report (default: HIGH — includes HIGH and CRITICAL) |
| Scan scope | No | `direct` (default) or `transitive` |
| Ecosystem filter | No | `nuget`, `npm`, `pip`, or `all` (default: all detected) |
| Depth mode | No | L1–L4 (default: L2 for delivery gates; L3 for release promotion) |

## Required Outputs

| Artifact | Path | Description |
|---|---|---|
| Dependency findings report | `.docs/changes/[date]-[task]-security-scan.md` | Full findings with CVE IDs, severity, affected version, fix version, recommendations, and gate signal |
| SBOM inventory (L3+) | `.docs/changes/[date]-[task]-sbom.md` | Full dependency inventory in scope; includes transitive packages |

## Depth Modes

| Mode | When to Use | Coverage |
|---|---|---|
| L1 — Manifest Inventory | Quick triage or preliminary scoping | Enumerate all manifests and direct dependency counts; no CVE lookup |
| L2 — CVE Scan (direct) | Standard delivery gate (Phase P7a default) | Scan direct dependencies; classify findings by severity; produce gate signal |
| L3 — Full SBOM + Transitive | Release promotion or >3-file change gate | Full SBOM; transitive dependency scan; upgrade path analysis per finding |
| L4 — Multi-DB Cross-Reference | Critical path, regulated context, or conflicting advisories | L3 plus cross-reference NVD + GitHub Advisory + OSV; flag advisory conflicts; note CVSS score discrepancies |

**Default depth:** L2 for Phase P7a. L3 when `release-simulation` is triggered (>3 asset file changes). L4 on explicit escalation or when advisory conflicts are detected in L3.

## Deterministic Workflow

1. **Detect manifests.** Enumerate all dependency manifests matching the configured ecosystem filter under the provided path. Record each manifest's type, path, and ecosystem. If no manifests are found, report and stop — do not produce a PASS signal on an empty scan.

2. **Resolve dependency list.** Parse direct dependencies from each manifest. If a lock file exists alongside the manifest, prefer it for pinned version resolution; flag any unpinned manifest without a lock file as a finding (INFORMATIONAL). For L3+, recursively resolve transitive dependencies.

3. **Generate SBOM (L3+).** Produce a structured inventory of all packages in scope: package name, version, ecosystem, direct vs transitive flag. Record whether each version is pinned or floating.

4. **Query CVE databases.** For each package@version in scope, look up known CVEs:
   - L2: NVD and GitHub Advisory Database
   - L4: NVD + GitHub Advisory + OSV; record all three results and flag any score conflict
   Record: CVE ID, CVSS score (v3.1 preferred), affected version range, patched version (if available), advisory URL.

5. **Classify findings.** Apply severity tiers:
   | Tier | CVSS Range |
   |---|---|
   | CRITICAL | ≥ 9.0 |
   | HIGH | 7.0 – 8.9 |
   | MEDIUM | 4.0 – 6.9 |
   | LOW | < 4.0 |
   | INFORMATIONAL | No CVSS score; advisory-only notice |

6. **Apply threshold filter.** Suppress findings below the configured severity threshold. Record suppressed count but do not enumerate suppressed findings unless explicitly requested.

7. **Generate remediation recommendations.** For each finding at threshold or above:
   - If a patched version exists: recommend upgrade with specific target version
   - If no patched version exists: recommend replacement package (if known) or produce a risk-acceptance rationale template
   - If the package is transitive: identify the direct dependency that pulls it in and recommend updating that

8. **Compute gate signal.** Apply escalation rules (see Escalation Rules section). Produce one explicit gate signal: PASS, CONDITIONAL, or BLOCK.

9. **Write findings artifact.** Record scan summary, findings table, SBOM (L3+), gate signal, open items requiring owner/date, and recommended next actions.

## Escalation Rules

| Condition | Signal | Required Action |
|---|---|---|
| Any CRITICAL finding | **BLOCK** | Halt delivery; route to `security-researcher` agent for remediation plan; re-run scan before proceeding |
| Any HIGH finding with an available patched version | **BLOCK** | Upgrade to patched version; re-run scan to confirm clean; do not proceed until signal clears |
| Any HIGH finding with no available fix | **CONDITIONAL** | Produce risk-acceptance rationale; require a named approver; record approver and date in findings artifact |
| MEDIUM findings only (no HIGH/CRITICAL) | **CONDITIONAL** | Document each finding; may proceed with explicit deferral and scheduled remediation date |
| LOW / INFORMATIONAL only | **PASS** | Record findings; no gate action required |
| No findings at or above threshold | **PASS** | Record clean scan result with scan date and tool version as promotion evidence |
| Manifest found but lock file absent | **CONDITIONAL** | Flag unpinned manifest; recommend adding lock file before next scan |

## Artifact Contract

| Artifact | Required Sections | Gate Dependency |
|---|---|---|
| Dependency findings report | Scan summary (manifests, packages in scope, scan date, database version used); Findings table (CVE ID, package, installed version, severity, fix version, recommendation); Open items (CONDITIONAL findings with named owner and remediation date); Gate signal (PASS / CONDITIONAL / BLOCK) | Gate signal must be explicit; BLOCK signal stops promotion |
| SBOM inventory (L3+) | Package name, version, ecosystem, direct/transitive flag; lock file status (pinned/unpinned) | Required for L3+ depth modes; absence of SBOM at L3+ = incomplete artifact |

## L4 Coverage Matrix

| Check | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| Manifest detection | ✅ | ✅ | ✅ | ✅ |
| Direct dependency CVE scan | — | ✅ | ✅ | ✅ |
| Transitive dependency CVE scan | — | — | ✅ | ✅ |
| SBOM generation | — | — | ✅ | ✅ |
| NVD lookup | — | ✅ | ✅ | ✅ |
| GitHub Advisory lookup | — | ✅ | ✅ | ✅ |
| OSV lookup | — | — | — | ✅ |
| Advisory conflict flagging | — | — | — | ✅ |
| Upgrade path analysis | — | — | ✅ | ✅ |
| Unpinned manifest detection | ✅ | ✅ | ✅ | ✅ |

## Reasoning Package

**Assumptions:**
- Lock files are treated as the source of truth for pinned versions; manifests without lock files are flagged, not failed
- CVSS v3.1 is the preferred scoring standard; v2 scores are accepted but noted as such
- A clean L2 scan at the point of Phase P7a satisfies the delivery gate; a new L3 scan is required at Phase P10 (release readiness) for >3-file changes
- "No findings" is a valid and complete scan result — the scan must record the clean result as evidence, not simply be skipped

**Trade-offs:**
- L2 (direct only) misses transitive attack surface but is faster; acceptable for incremental delivery gates where the dependency graph has not materially changed
- L4 multi-DB cross-reference adds latency; reserved for critical path or when L3 finds conflicting advisory data
- Requiring a named approver for CONDITIONAL/HIGH-no-fix findings adds friction but prevents silent risk accumulation

**Open blockers:**
- None at time of authoring. Tool-specific scan commands (dotnet list package --vulnerable, npm audit, pip-audit) are ecosystem-standard; no workspace-specific tooling gap blocks this skill.

## Source Governance Summary

Sources are maintained in `references/source-catalog.md`. Default freshness threshold: 30 days. Mark as **Needs Review** when Last Evaluated exceeds threshold.

## Pragmatic Stop Rule

Stop after producing an explicit gate signal (PASS, CONDITIONAL, or BLOCK) with all findings at or above threshold documented and remediation recommendations present for each BLOCK or CONDITIONAL item. Do not re-scan for findings that have been explicitly deferred with documented rationale and a named approver.

## Anti-Patterns

- **Proceeding to promotion with a BLOCK signal** — gate signals exist to prevent exactly this; BLOCK is non-negotiable without documented remediation
- **Scanning direct dependencies only for a release gate** — use L3 for release; transitive packages are a primary CVE attack vector
- **Accepting CRITICAL findings with a one-line comment** — requires a named approver, a remediation plan, and a scheduled date
- **Running a scan once at sprint start and treating it as valid throughout** — re-run at each promotion gate; CVEs are disclosed continuously
- **Treating an unpinned manifest as equivalent to a pinned one** — flag it explicitly; floating versions make the scan non-deterministic
- **Producing a PASS signal on an empty scan** — if no manifests are found, report the absence; do not silently pass

## Done Criteria

- [ ] All manifests in the configured scope detected and listed
- [ ] CVE lookup completed for all dependencies at the configured depth and ecosystem
- [ ] All findings at or above severity threshold classified with CVE ID, severity, and affected version
- [ ] SBOM produced (required for L3+ depth modes)
- [ ] Remediation recommendation present for every BLOCK and CONDITIONAL finding
- [ ] Gate signal (PASS / CONDITIONAL / BLOCK) is explicit and recorded in the findings artifact
- [ ] No CRITICAL or unaddressed HIGH finding is present when gate signal is PASS
- [ ] Unpinned manifests flagged if detected
