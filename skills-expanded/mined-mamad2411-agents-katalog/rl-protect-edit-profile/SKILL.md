---
name: rl-protect-edit-profile
description: Creates or modifies rl-protect scanning profiles (rl-profile JSON). Use when the user wants to configure scan policy, set assessment severity levels, add governance allow/block rules, or apply policy overrides.
---

## Profile editing (rl-protect)

Use this skill when the user wants to create a new profile or change an existing one. Profiles are JSON files that control how rl-protect evaluates packages — what counts as a failure, which packages are always allowed or blocked, and which policy rules are overridden.

### Profile location

The profile is loaded from a file passed to `rl-protect scan` via `--profile={path}`. If the user does not specify a path, rl-protect will use its default profile. Read the file before making any changes if it already exists.

---

### Schema reference

```
rl-profile
  .schema                          — always 1, do not change
  .name                            — human-readable profile name
  .info                            — description string (free text)
  .timestamp                       — ISO-8601, set to current time on every save
  .configuration.policy
    .min_catalogue                 — minimum required catalogue level (integer, 1–10)
    .rl_scan_level                 — scan depth level (integer, 1–10)
    .rl_auto_approval              — auto-approve packages that pass (boolean)
    .assessments{}                 — one entry per check category (see below)
    .governance.community          — age gates and allow/block pattern lists
    .acceptance{}                  — natural language risk acceptance statements, keyed by assessment category (see below)
    .overrides{}                   — keyed by policy rule ID (SQ- or TH-prefixed; not CVE)
    .modeling                      — threat model: a single free-text prose string giving the AI triager general judgment context (trust boundaries, deployment, priorities). Optional; default absent/empty (see below)
```

---

### Assessment configuration

Each assessment can be ignored entirely or configured with per-detection-type severity levels.

**Valid severity values:** `pass` | `warning` | `fail`

```
assessments.secrets
  .ignored                         — true suppresses the entire check

assessments.licenses
  .ignored                         — true suppresses the entire check

assessments.vulnerabilities
  .ignored
  .detections
    .mandate                       — CVEs under active government mandate
    .exploit                       — CVEs with known exploits
    .malware                       — CVEs used in malware campaigns
    .critical                      — CVEs with CVSS ≥ 9.0

assessments.hardening
  .ignored

assessments.tampering
  .ignored
  .ml_hunting                      — ML-based anomaly detections

assessments.malware
  .ignored
  .rl_analyst                      — findings from RL analyst vetting
  .rl_scanner                      — findings from RL scanner
  .suspicious                      — suspicious (unconfirmed) detections
  .dependency
    .develop                       — malicious dependency in dev context
    .release                       — malicious dependency in release context
  .detections                      — affects specified malware types
    .adware
    .riskware
    .protestware
    .spam
```

---

### Governance configuration

Governance rules control package-level allow and block decisions independently of assessment findings.

```
governance.community
  .min_package_age                 — minimum days since first package release (integer)
  .min_version_age                 — minimum days since this version was published (integer)
  .allow[]                         — packages always approved regardless of findings
    .pattern                       — PURL pattern (exact or wildcard, e.g. pkg:npm/lodash@*)
    .audit.author                  — who added the rule
    .audit.timestamp               — when the rule was added
    .audit.reason                  — stated justification
  .block[]                         — packages always rejected regardless of findings
    .pattern                       — PURL pattern
    .audit.author                  — who added the rule
    .audit.timestamp               — when the rule was added
    .audit.reason                  — stated justification
```

**PURL pattern matching:**
- Exact version: `pkg:npm/lodash@4.17.21`
- Wildcard version range: `pkg:npm/ua-parser-js@0.7.*`
- All package versions: `pkg:gem/rack@*`
- Specific artifact: `pkg:pypi/flask@3.1.2?artifact=flask-3.1.2-py3-none-any.whl`

---

### Risk acceptance configuration

Acceptance statements are natural language expressions of risk tolerance that the AI triager uses to automatically accept findings within the stated bounds. They are grouped by assessment category — the same categories as `assessments` (`secrets`, `licenses`, `vulnerabilities`, `hardening`, `tampering`, `malware`).

```
acceptance.{category}[]
  .enabled                         — true/false; false suspends the statement without deleting it
  .statement                       — natural language risk tolerance (what the AI reasons against)
  .audit.author                    — who added the statement
  .audit.timestamp                 — ISO-8601, when it was added
  .audit.reason                    — human justification for adding this statement (paper trail)
```

**Example:**
```json
"acceptance": {
  "vulnerabilities": [
    {
      "enabled": true,
      "statement": "We accept ReDoS vulnerabilities in npm packages. At our request volumes worst case is a ~100ms delay.",
      "audit": {
        "author": "user@example.com",
        "timestamp": "2026-05-22T10:00:00+02:00",
        "reason": "Reviewed with security team — no user-controlled input reaches the affected regex paths."
      }
    }
  ],
  "hardening": [
    {
      "enabled": true,
      "statement": "All hardening findings are acceptable — this is an internal CLI tool, not a public-facing service.",
      "audit": {
        "author": "user@example.com",
        "timestamp": "2026-05-22T10:00:00+02:00",
        "reason": "Threat model reviewed — no external attack surface."
      }
    }
  ]
}
```

Valid categories: `secrets`, `licenses`, `vulnerabilities`, `hardening`, `tampering`, `malware`.

---

### Policy overrides

Overrides change the effective status of specific policy rule violations by their rule ID.

```
overrides.{SQxxxxx | THxxxxx}
  .enabled                         — true to activate the override
  .blocker                         — the status to apply instead: pass | fail
  .apply_to[]                      — scope: "organization" | "group" | "any"
  .audit.author
  .audit.timestamp                 — must use current timestamp in ISO-8601 format
  .audit.reason
```

Setting `blocker` to `pass` means the rule never blocks a scan. Setting it to `fail` elevates a warning to a failure.

---

### Threat model configuration

`configuration.policy.modeling` is a single free-text **prose string** — the project's threat model. It gives the AI triager *general* judgment context (the counterpart to acceptance's *targeted* per-finding rules): which inputs an attacker can control (trust boundaries), the deployment/exposure, and priorities. It is **not** a rule set — no categories, no audit block, just the string. Default is absent/empty (no threat model).

```
modeling                           — a free-text string, e.g.
  "Internal CLI tool run by operators. Config files and CLI args are
   operator-controlled, not attacker-reachable. No inbound network."
```

The triager uses it to shape verdicts/severity and, most importantly, trust-boundary reachability (a taint source the model designates operator-controlled makes a finding not-attacker-controllable). It never auto-accepts a finding — that stays acceptance's job.

#### Set or clear the threat model

**Trigger:** user wants to set, change, or remove the project threat model / "what an attacker can control" context.

1. To set: write the prose to `configuration.policy.modeling` (overwrite any existing value). If the user describes their deployment loosely, compose a concise paragraph covering deployment, trust boundaries (which inputs are attacker-controlled vs operator-controlled), and priorities.
2. To clear: remove the `modeling` key (or set it to `""`).
3. Save and validate as usual (`modeling` must be a string).

### Tasks

---

#### Create a new profile

**Trigger:** user wants to create a profile from scratch, or no profile file exists.

**Steps:**
1. Ask the user for a profile name and any initial settings they want to configure.
2. Generate a valid profile JSON with `schema: 1` and the current timestamp.
3. Set sensible defaults for any fields the user did not specify (see defaults below).
4. Write the file and confirm the path.

**Default values for new profiles:**

| Field | Default |
|---|---|
| `min_catalogue` | `5` |
| `rl_scan_level` | `5` |
| `rl_auto_approval` | `false` |
| All assessment `.ignored` | `false` |
| `vulnerabilities.detections.mandate` | `fail` |
| `vulnerabilities.detections.exploit` | `fail` |
| `vulnerabilities.detections.malware` | `fail` |
| `vulnerabilities.detections.critical` | `fail` |
| `malware.rl_analyst` | `fail` |
| `malware.rl_scanner` | `fail` |
| `malware.suspicious` | `warning` |
| `malware.dependency.release` | `fail` |
| `malware.dependency.develop` | `warning` |
| `min_package_age` | `90` |
| `min_version_age` | `3` |

---

#### Configure assessment severity

**Trigger:** user wants to change what counts as a failure or warning for a specific check, or wants to ignore a check entirely.

**Steps:**
1. Identify which assessment and detection type the user wants to change.
2. Confirm the new severity value (`pass`, `warning`, or `fail`).
3. Update only the affected field. Do not alter other assessments.
4. Update `.timestamp` to the current time in ISO-8601 format.
5. Write the file and show a summary of what changed.

**Output summary format:**

```
### Profile updated — {profile name}

| Assessment | Detection | Previous | New |
|---|---|---|---|
| {assessment name} | {detection type or "ignored"} | {old value} | {new value} |
```

---

#### Add a governance rule

**Trigger:** user wants to always allow or always block a specific package or version range.

**Steps:**
1. Ask for: the PURL pattern, whether it is an allow or block rule, and a reason.
2. Check whether a rule for the same pattern already exists. If so, warn the user and ask whether to replace it.
3. Populate `audit.author` from context if known, otherwise ask. Prefer emails. Set `audit.timestamp` to the current time in ISO-8601 format.
4. Append the rule to the appropriate list (`allow[]` or `block[]`).
5. Update `.timestamp` and write the file.

**Output summary format:**

```
### Governance rule added — {profile name}

| Field | Value |
|---|---|
| Action | {Allow / Block} |
| Pattern | {purl pattern} |
| Reason | {reason} |
| Author | {author} |
```

---

#### Remove a governance rule

**Trigger:** user wants to remove an existing allow or block rule.

**Steps:**
1. List all current rules in the relevant list and ask the user to confirm which to remove.
2. Remove the matching entry by pattern.
3. Update `.timestamp` and write the file.

---

#### Add a risk acceptance statement

**Trigger:** user wants to express a risk tolerance that the AI triager should apply automatically.

**Steps:**
1. Ask for: the assessment category, the risk tolerance statement, and the reason for accepting this risk.
2. Ask for the author if not known from context. Prefer email addresses.
3. Check whether a statement with the same or very similar wording already exists in that category. If so, warn the user and ask whether to replace or add alongside it.
4. Append the new entry to `acceptance.{category}[]` with `enabled: true` and `audit` fields populated. Set `audit.timestamp` to the current ISO-8601 time.
5. Update `.timestamp` and write the file.

**Output summary format:**

```
### Risk acceptance statement added — {profile name}

| Field | Value |
|---|---|
| Category | {category} |
| Statement | {statement} |
| Reason | {reason} |
| Author | {author} |
```

---

#### Disable or remove a risk acceptance statement

**Trigger:** user wants to suspend or permanently remove an acceptance statement.

**Steps:**
1. List all current statements across all categories and ask the user to identify which one.
2. If suspending: set `enabled: false` and confirm. The statement remains in the file but will be ignored by the triager.
3. If removing: delete the entry from the list entirely.
4. Update `.timestamp` and write the file.

---

#### Add or update a policy override

**Trigger:** user wants to suppress or downgrade a specific policy rule violation by its SQ rule ID.

**Steps:**
1. Ask for: the SQ rule ID, the target status (`pass` or `warning`), the scope (`organization`, `group`, or `any`), and a reason.
2. If an override for that rule ID already exists, show the current values and ask the user to confirm the update.
3. Set `enabled: true`, populate the audit fields, and update `.timestamp` in ISO-8601 format.
4. Write the file and confirm.

**Output summary format:**

```
### Policy override saved — {profile name}

| Field | Value |
|---|---|
| Rule | {SQxxxxx | THxxxxx} |
| Overridden to | {pass / warning} |
| Scope | {organization / group / any} |
| Reason | {reason} |
| Author | {author} |
```

---

#### Show current profile

**Trigger:** user wants to review what is currently configured in the profile.

Read the profile file and present it in this format:

```
### Profile — {name}

**Scan settings**
| Setting | Value |
|---|---|
| Min catalogue level | {min_catalogue} |
| Scan level | {rl_scan_level} |
| Auto-approval | {Yes / No} |

**Assessment configuration**
| Assessment | Ignored | Detection severities |
|---|---|---|
| Secrets | {Yes/No} | — |
| Licenses | {Yes/No} | — |
| Vulnerabilities | {Yes/No} | mandate: {v} · exploit: {v} · malware: {v} · critical: {v} |
| Hardening | {Yes/No} | — |
| Tampering | {Yes/No} | ml_hunting: {v} |
| Malware | {Yes/No} | analyst: {v} · scanner: {v} · suspicious: {v} · dep/release: {v} · dep/develop: {v} |

**Governance**
- Min package age: {N} days · Min version age: {N} days
- Allow rules: {N}  ·  Block rules: {N}

**Risk acceptance:** {N} statements across {N} categories

**Policy overrides:** {N} active
```

Follow with a table of governance rules, acceptance statements, and overrides if any exist.

---

### General rules

- Always read the existing profile before making changes. Never overwrite fields the user did not ask to change.
- Always update `.timestamp` to the current ISO-8601 time on every write.
- Never set `.schema` to any value other than `1`.
- When adding audit entries, always require a `reason`. Do not allow empty reason strings.
- If the user tries to set a severity value other than `pass`, `warning`, or `fail`, reject it and list the valid options.
- If the user tries to ignore all six assessments simultaneously, warn them that this would result in every package passing regardless of content.
- When adding an acceptance statement, always require a non-empty `reason` in audit — the statement captures the tolerance, the reason captures the business justification.
- Valid acceptance categories are the same six as assessments: `secrets`, `licenses`, `vulnerabilities`, `hardening`, `tampering`, `malware`. Reject any other category name.
- Before confirming any change, validate the result (see **Validate before finishing**) and fix anything it flags.
- After every write, confirm the file path and summarize only the fields that were changed.

---

### Validate before finishing

The report's profile editor gates every save through a single validator. Hold conversational edits to the same bar, so a change made here can never produce a profile the editor — or `rl-protect scan` — would reject.

After writing the file, validate it:

1. **Run the validator (authoritative).** It ships with the `rl-appsec-agent` plugin. If that plugin is installed, locate its `scripts/validator.py` and run:
   ```
   python {path}/rl-appsec-agent/scripts/validator.py {profile_path}
   ```
   Exit 0 prints `profile is valid`; exit 1 lists every problem. Fix each and re-run until it passes.

2. **If the validator is not reachable, self-check against the same invariants:**
   - `schema` is `1`; `configuration.policy` is present.
   - Every assessment severity is `pass`/`warning`/`fail`. Detection severities may be **omitted** (the scanner's built-in level applies) but never set to anything else.
   - Not all six assessments are `ignored`.
   - `min_catalogue`/`rl_scan_level` are integers 1–10; `min_package_age`/`min_version_age` are non-negative integers.
   - Each allow/block rule has a valid `pkg:` PURL pattern (only `*` is a wildcard) and an `audit.author`.
   - Each acceptance statement has a non-empty `statement` and an `audit.author`.
   - Each override key is a valid `SQ#####` or `TH#####` code (CVE ids can't be overridden — accept those), `blocker` is `pass` or `fail`, and `audit` has both a `reason` and an `author`.

Never leave the user with a profile that fails validation.
