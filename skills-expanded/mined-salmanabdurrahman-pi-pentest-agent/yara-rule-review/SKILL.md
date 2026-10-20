---
name: yara-rule-review
description: YARA rule quality and safety review — validate detection rule structure, string patterns, condition logic, metadata completeness, false-positive risk, and evidence linkage; never execute malware samples, deploy rules to production sensors, or embed proprietary hash lists in distributable rules.
disable-model-invocation: true
risk: passive
allowed-modes: [forensic, blue-team, reverse-engineering]
authorization-required: conditional
evidence-outputs: [rule-review, test-notes, redacted-evidence]
---

# YARA rule review — detection rule quality and safety assessment

Use this skill to review YARA detection rules for correctness, performance, false-positive risk, metadata completeness, evidence linkage, and operational safety. This skill is passive and local-first: review rules against documented threat intelligence, reference samples, and best practices without executing malware, deploying rules to production, or exposing proprietary indicators.

## Required inputs

- The YARA rule file(s) to review (`.yar` or `.yara` extension).
- Rule purpose and intended detection scope: malware family, threat actor, attack technique, artifact type (PE, ELF, Mach-O, script, document, memory, network), or behavioral indicator.
- Reference context if available: threat intelligence report, sample hashes (SHA256), MITRE ATT&CK technique IDs, campaign name, or incident report that motivated the rule.
- If the rule is designed for production deployment: an execution environment (EDR, SIEM, sandbox) and any platform-specific YARA module dependencies (`pe`, `elf`, `math`, `hash`, `console`).
- If the rule references file samples: sample hashes must be provided, but never the samples themselves unless the review is conducted in an isolated forensic environment.

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` before reviewing rules that may contain proprietary or classified indicators.
2. `pentest_agent_parse_scope` when the review is part of a scoped engagement and evidence boundaries exist.
3. `pentest_agent_validate_target` before any live service query or external hash lookup (VirusTotal, MalwareBazaar).
4. `pentest_agent_check_authorization` before any active validation, test execution, or external query.
5. `pentest_agent_build_command` and `pentest_agent_execute_tool` only for approved defensive read-only execution (e.g., running `yara` against authorized test fixtures). Never execute rules against production file systems or live malware.

## Workflow

### Phase 1 — rule intake and metadata audit

Before analyzing the rule body, verify that the rule is well-identified and attributable:

1. **Rule name**: follows a naming convention (`FamilyName_IndicatorType`, `APTXX_Malware_Variant`, `ThreatGroup_Tool_Year`). Rule name should be unique within the rule set.
2. **Metadata section**: check for required metadata fields:
   - `description`: human-readable explanation of what the rule detects.
   - `author`: individual or organization that authored the rule.
   - `date`: rule creation or last-modification date.
   - `reference`: URL to threat report, blog post, sample hash, or MITRE technique.
   - `hash` or `sample_hash`: SHA256 of the sample the rule was tested against (if applicable).
   - `score` or `severity`: rule severity indicator.
   - `mitre_att` or `mitre`: associated MITRE ATT&CK technique ID(s).
3. **Missing metadata**: flag rules that lack a description (cannot assess intent), lack a reference (cannot verify threat intelligence), or lack a date (cannot assess rule freshness). These are quality findings, not blockers, but each missing field reduces the rule's auditability.

### Phase 2 — string pattern review

Analyze every `$string` definition for correctness, specificity, and performance:

1. **String uniqueness**: each `$string` identifier should be unique within the rule. Duplicate identifiers silently overwrite — a common YARA pitfall.
2. **String specificity**: strings should be specific enough to minimize false positives:
   - **Good**: `$mz = { 4D 5A }` (PE header) — highly specific, low FP risk.
   - **Good**: `$cmd = "cmd.exe /c " wide` — narrow with context keyword.
   - **Risky**: `$a = "test"` — too short and generic, will match thousands of benign files.
   - **Risky**: `$sql = "SELECT"` — appears in documentation, log files, and error messages.
3. **Hex pattern correctness**: for hex strings (`{ AB CD ?? EF }`):
   - Confirm byte counts are even (each byte is 2 hex digits).
   - Confirm wildcard (`??`) usage is intentional — wildcards reduce specificity.
   - Confirm jump patterns (`[2-4]`, `[0-]`) have reasonable bounds — unbounded jumps (`[0-]`) can cause performance degradation.
4. **Modifiers**: verify the modifiers applied to each string:
   - `wide`: for UTF-16 strings (Windows binaries, .NET assemblies).
   - `ascii`: for ASCII strings (Unix binaries, scripts).
   - `nocase`: for case-insensitive matching. Use deliberately — `nocase` increases scan time.
   - `fullword`: prevents partial-word matches (important for short strings like `cat`, `bin`, `tmp`).
   - `xor`: for XOR-encoded strings. If used, verify the XOR key or range is documented.
   - `base64` / `base64wide`: for Base64-encoded strings. If used, verify the encoding variant (standard, URL-safe).
5. **Dead strings**: identify strings that are defined but never referenced in the `condition` section — these add scan cost with no detection value.

### Phase 3 — condition logic review

Analyze the `condition` section for logical correctness and performance:

1. **Condition structure**:
   - `all of them` / `any of them` / `N of them`: verify the count threshold is appropriate.
   - `filesize < X`: verify the file-size constraint is intentional — large files require proportionally more scan time.
   - String-at-offset checks (`$a at 0`): verify the offset is correct for the target file format.
   - `for any section in pe.sections`: PE module-specific conditions — verify the PE module is declared (`import "pe"`).
2. **Combination logic**: rules using `and` between strings require all strings to be present in the same file. If the condition should match when any one of several indicators is present, use `any of them` instead.
3. **Negation traps**: `not $a` matches every file that does NOT contain `$a` — including files that were never meant to be scanned. Negated conditions should always be combined with at least one positive condition (`$b and not $a`).
4. **Private rule references**: if the rule uses `private` rule references (`RuleA and RuleB`), verify all referenced private rules are defined in the same file or included via `include`.
5. **Infinite loops**: rules with unbounded regex patterns (`/.*/`) or extremely permissive hex patterns can cause scanning to hang. Flag any condition that could cause exponential backtracking.

### Phase 4 — false-positive risk assessment

Evaluate the rule against common false-positive scenarios:

1. **String collision risk**: for each string, assess whether it is likely to appear in:
   - Operating system files (kernel, system libraries, configuration files).
   - Common software packages (browsers, office suites, development tools, game engines).
   - Compiler runtimes and standard libraries.
   - Legitimate security tools (other YARA rules, antivirus signatures, EDR components).
2. **String length threshold**: strings shorter than 6 bytes have inherently higher false-positive rates. Flag any string under 6 bytes that is not hex-encoded with high specificity.
3. **Over-matching by condition**: a condition that matches on `1 of ($a, $b, $c, ...)` where any single string is generic is dangerous. The rule fires when any one string matches, even if the other indicators are absent.
4. **Context-free patterns**: strings that lack surrounding bytes for context. For example, `$a = "MZ"` matches every PE file, DLL, and kernel driver. The condition must narrow the match (`$a at 0 and pe.is_pe`).

For each identified false-positive risk, suggest a mitigation: add context bytes to hex patterns, raise the string-count threshold, add file-size constraints, use the `pe` module for format-specific conditions, or limit the rule to specific file extensions.

### Phase 5 — rule safety and deployment readiness

Before a rule can be approved for production deployment, verify operational safety:

1. **No embedded secrets**: the rule must not contain API keys, authentication tokens, private IP addresses of internal infrastructure, or customer-specific identifiers in human-readable strings.
2. **No proprietary samples**: hex patterns must not embed entire file segments from proprietary or classified malware samples unless the rule is strictly internal and classified at the appropriate level.
3. **Performance estimate**: rules with many strings (>50) combined with `all of them`, large hex patterns (>500 bytes), or unbounded regex patterns should be flagged for performance testing before production deployment.
4. **Platform dependencies**: if the rule uses YARA modules (`pe`, `elf`, `math`, `hash`, `console`, `magic`, `dex`), document which modules are required and whether the deployment platform supports them.
5. **Rule interaction**: if the rule is part of a rule set, check for conflicts with other rules (duplicate rule names, mutually exclusive conditions, cascade effects where one rule's false positive triggers alerts for another rule).
6. **Sample availability**: for rules referencing specific samples by hash, verify that the sample is accessible to the reviewing team (in a sandbox or isolated forensic environment). If not, note that the rule's testability is limited.

### Phase 6 — evidence and documentation output

Produce a structured rule review record:

1. **Rule identification**: rule name, file path, author, date, reference sources.
2. **Review summary**: one-paragraph assessment of the rule's quality, specificity, and readiness.
3. **Finding inventory**: each issue found during Phases 1–5, categorized as:
   - **Critical**: rule could cause false positives on critical system files, rule contains secrets, rule triggers on benign system binaries, or rule has an infinite-loop risk.
   - **High**: rule has significant false-positive risk on common software, rule lacks required metadata, or rule uses negated conditions without positive anchors.
   - **Medium**: rule has suboptimal string specificity, rule has dead strings, or rule has undocumented module dependencies.
   - **Low**: rule could benefit from additional metadata, more specific string names, or performance optimizations.
   - **Info**: observations about rule style, naming conventions, or documentation completeness.
4. **Test recommendations**: if test fixtures are available, recommend specific test cases:
   - Positive test: the rule should match the known-bad sample (hash provided).
   - Negative test: the rule should NOT match benign files from the same environment (list suggested benign file types).
5. **Approval status**: `approved` (ready for deployment), `approved-with-conditions` (deploy with noted mitigations), or `needs-revision` (fix critical/high issues before deployment).

## Decision points

- **Reject rules with secrets**: if a rule contains API keys, tokens, or private IPs → reject immediately, redact, and notify the rule author.
- **Reject rules with no positive anchor**: a condition that is only `not $a` matches millions of files → reject for operational safety.
- **Flag but don't reject for missing metadata**: missing metadata is a quality issue, not a safety issue. Flag and recommend, but the rule can still be approved with conditions.
- **Flag rules with unbounded regex or hex jumps**: these can cause scanner hangs → flag as High if the target environment has scan-time SLAs.
- **Accept rules tested on available samples**: if the rule was tested on a sample hash that you can verify independently, accept the test evidence. If samples are unavailable, note the gap.

## Prohibited behavior

- Executing malware samples — use only hash verification and static analysis. Malware execution requires an isolated sandbox environment with chain-of-custody procedures (see `re-malware-sandbox`).
- Deploying rules directly to production sensors — rule deployment is an operational action requiring separate change management.
- Querying VirusTotal, MalwareBazaar, or other external threat-intelligence platforms with proprietary or classified sample hashes that could reveal investigation details.
- Embedding customer-specific indicators (hostnames, IPs, usernames) in distributable rules without redaction.
- Copying rule bodies from commercial or classified rule sets without permission.
- Claiming a rule detects a specific threat actor without evidence from a referenced intelligence report.

## Stop conditions

- Rule contains secrets → stop, redact, notify author.
- Rule uses only negated conditions → stop, return for revision.
- Rule has an infinite-loop risk (unbounded regex, unbounded hex jumps, exponential backtracking) → stop, flag as Critical, return for performance testing.
- All phases completed, findings categorized, approval status assigned → review complete.
- Insufficient reference context to assess rule intent → return with a request for the threat intelligence report or sample hash.

## Evidence — YARA rule review record

For each reviewed rule, record:

```text
Rule: <name> | file: <path> | author: <name> | date: <YYYY-MM-DD>
Modules: <pe | elf | math | hash | none>
Strings: <count> | hex: <count> | text: <count> | regex: <count>
Metadata: <description: yes/no> <author: yes/no> <date: yes/no> <reference: yes/no> <hash: yes/no>
Critical findings: <count> | detail: <summary>
High findings: <count> | detail: <summary>
Medium findings: <count> | detail: <summary>
Low findings: <count> | detail: <summary>
False-positive risk: <low | medium | high>
Performance risk: <low | medium | high>
Sample tested: <hash> | match confirmed: <yes | no | not available>
Approval: <approved | approved-with-conditions | needs-revision>
Reviewer: <name> | date: <YYYY-MM-DD>
```

Aggregate into a rule-set review matrix if multiple rules are reviewed together. Never store: raw rule bodies with embedded secrets, sample file content (store only hashes), proprietary threat intelligence references in unredacted form, or API keys/tokens found during review.

## Report handoff

When the review is complete:
1. Save the review record as redacted evidence via `pentest_agent_append_evidence`.
2. For rules approved for deployment, include a deployment recommendation: target environment (EDR, SIEM, sandbox), required YARA modules, expected scan-time impact, and false-positive mitigation steps.
3. For rules needing revision, include a prioritized list of required changes and the rationale for each.
4. If the review identified gaps in the rule set (missing coverage for a known TTP), document the gap as a recommendation for future rule development.

## YARA best-practice reference

Key YARA best practices assessed during review:

- **Rule naming**: consistent naming conventions across the rule set.
- **Metadata completeness**: description, author, date, reference, and hash fields present.
- **String specificity**: no strings under 4 bytes, context bytes included for hex patterns, modifiers applied correctly.
- **Condition quality**: no unbounded negations, no unbounded regex, performance-conscious threshold counts.
- **Module usage**: modules declared only when needed, platform compatibility documented.
- **Test evidence**: each rule tested against at least one positive sample (hash provided) and a representative benign file set.
- **Operational safety**: no embedded secrets, no proprietary indicators in distributable rules, deployment environment documented.

This skill assesses rules against these criteria. It does not author rules, run automated YARA scanning, or test rules against live systems — those actions require separate engagement scoping and approval.
