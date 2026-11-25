---
name: opencode-ssot-provider-ext-sync
description: >-
  Extend SSOT base provider configs (models.json) into per-account opencode
  provider entries with API keys from a key-value file, synced to opencode.json,
  auth.json, and account.json.
category: OpenCode-Configuration
---

# SSOT Provider Extension Sync (v1)

This composer skill documents the workflow for extending SSOT (Single Source of
Truth) base provider definitions into multiple per-account provider entries for
OpenCode, with API keys resolved from a key-value secrets file.

It composes the generic [`kv-line-parse`](../../general/kv-line-parse/SKILL.md)
base skill for parsing the key-value secrets format.

***

## Composition Rationale

This skill is a composer: it orchestrates a multi-step sync across three target
files (opencode.json, auth.json, account.json) using the existing sync script.
It does NOT re-implement the key-value parsing logic — that is delegated to the
[`kv-line-parse`](../../general/kv-line-parse/SKILL.md) base skill.

The composer's value-add is:

1. **Domain-specific file mappings** — models.json to opencode.json/auth.json/account.json.
2. **Tracking file format** — provider-extensions.json with ssot/active/disabled sections.
3. **Naming convention** — extended provider ID format and suffix derivation.
4. **Idempotency protocol** — diff-based change detection, dry-run preview.
5. **Stale cleanup** — prefix-based managed detection for removed extensions.

***

## Scripts

| Script | Purpose |
|---|---|
| [`scripts/sync-provider-extensions.py`](scripts/sync-provider-extensions.py) | Main sync script — reads SSOT, tracking file, key-value storage; writes opencode.json, auth.json, account.json |
| [`scripts/provider-extensions.json`](scripts/provider-extensions.json) | Tracking file format reference — documents the ssot/active/disabled structure (redacted for public reference; operational copy in the private config repo) |

***

## Prerequisites

- Access to the private config repo containing:
    - `opencode/cache/models.json` — SSOT base provider definitions
    - `opencode/config/opencode.json` — target provider config
    - `opencode/share/auth.json` — auth entries
    - `opencode/share/account.json` — account entries
    - `<key-file>` — key-value storage with quoted or unquoted descriptions per `kv-line-parse` base skill
- Python 3.12+
- `scripts/provider-extensions.json` — tracking file defining which extensions to create
  (operational copy lives alongside SSOT in the private config repo)

All file paths are configurable via CLI flags (see Script Invocation).

***

## Tracking File Format

The tracking file (`provider-extensions.json`) organizes extensions by base
provider ID:

```json
{
  "ssot": {
    "base_provider_id": "Key description (reference only, not synced)"
  },
  "base_provider_id": [
    {"suffix": "ext-suffix", "key": "Key description"}
  ],
  "another_provider": {
    "active": [
    {"suffix": "ext-suffix", "key": "Key description"}
    ],
    "disabled": [
      "ext-suffix-plain-string"
    ]
  }
}
```

**Rules:**

- The `"ssot"` section maps base provider IDs to their corresponding
  key descriptions for documentation purposes only — the sync script
  skips this key entirely.
- Active extensions use `{"suffix": "...", "key": "..."}` objects where `key`
  references the description line from the key-value file (not the actual key value).
- Disabled extensions are plain suffix strings — kept for reference, removed
  from synced config.
- Two container formats are supported: a simple list (for providers with only
  active entries) and a `{"active": [...], "disabled": [...]}` dict.

***

## Naming Convention

Extended provider IDs follow the pattern:

```text
<provider>-<account>[-<account-number>]-<platform>-<platform-project>
```

- `<provider>` — the base provider ID (e.g., `google`, `openrouter`)
- `<account>` — the account name or identifier (e.g., `acct`)
- `<account-number>` — included only when multiple accounts share the same
  person or entity name (e.g., `1` in `acct-1`)
- `<platform>` — the platform name; Google normally uses `ai-studio`
- `<platform-project>` — the specific project within the platform
  (e.g., `proj-x`, `proj-y`)
- When platform or platform-project is unknown, use `unknown`

Examples:

- `google-acct-1-ai-studio-proj-x`
- `google-acct-1-ai-studio-proj-y`
- `openrouter-acct-1-proj-a` (provider without platform: `openrouter`-`acct`-`1`-`proj-a`)
- `google-acct-2-unknown-unknown` (acct-2 account, platform not known)

***

## Sync Workflow

### Step 1 — Read SSOT

Read `models.json` to extract base provider definitions (env keys, name, npm,
api, doc, models blocks).

### Step 2 — Read tracking file

Parse `provider-extensions.json` — extract active extensions, disabled suffixes,
and key reference mappings. The `"ssot"` key is skipped.

### Step 3 — Parse key-value file

Delegate to the `kv-line-parse` base skill:

```bash
python3 .agents/skills/general/kv-line-parse/scripts/parse_keywords.py \
  --file /path/to/<key-file>
```

This produces a JSON dict mapping each description to its actual secret value.

### Step 4 — Build extended providers

For each active extension:

- Clone the base provider's config
- Transform env keys: `GOOGLE_API_KEY` -> `GOOGLE_{SUFFIX}_API_KEY`
  where `{SUFFIX}` is the extension suffix with hyphens replaced by underscores
  and uppercased (e.g., `acct-1-ai-studio-proj-x` -> `ACCT_1_AI_STUDIO_PROJ_X`)
- Inherit npm, api, doc, and models blocks from the base provider
- Set the provider name to include the suffix title

### Step 5 — Merge into opencode.json

- Preserve existing extra keys on each provider entry
- Remove managed entries that are no longer active (detected by prefix:
  all entries starting with `google-`, `openrouter-`, etc.)
- Write only if changes detected (diff-based idempotency)

### Step 6 — Sync auth.json

For each active extension:

- Look up the key description -> actual value via the key-value file
- Create or update `{"type": "api", "key": "<actual_value>"}` entry
- Remove stale managed entries

### Step 7 — Sync account.json

For each active extension:

- Reuse existing account ID if present (preserves stability)
- Generate deterministic account ID via `sha256(serviceID)` for new entries
- Set credential with actual key value
- Update active pointer
- Remove stale managed accounts

***

## Script Invocation

```bash
# Run from the ai-suite skill directory (all paths to private config repo via flags):
python3 scripts/sync-provider-extensions.py \
  --ssot <private-config-repo>/opencode/cache/models.json \
  --extensions <private-config-repo>/scripts/provider-extensions.json \
  --config <private-config-repo>/opencode/config/opencode.json \
  --auth <private-config-repo>/opencode/share/auth.json \
  --account <private-config-repo>/opencode/share/account.json \
  --keywords <private-config-repo>/<key-file>

# Dry-run (preview changes without writing):
python3 scripts/sync-provider-extensions.py \
  --ssot <private-config-repo>/opencode/cache/models.json \
  --extensions <private-config-repo>/scripts/provider-extensions.json \
  --config <private-config-repo>/opencode/config/opencode.json \
  --auth <private-config-repo>/opencode/share/auth.json \
  --account <private-config-repo>/opencode/share/account.json \
  --keywords <private-config-repo>/<key-file> \
  --dry-run
```

All six paths are required when running from ai-suite — the script has no
built-in defaults for the private config repo layout when invoked from
outside that repo.

***

## Idempotency

The sync script is idempotent:

- Reads all four target files before making any changes
- Compares existing vs. new content via Python equality
- Skips writing when no difference is detected
- `--dry-run` flag provides a full change preview without any writes
- Stale managed entries (removed from tracking file) are cleaned up via
  prefix-based detection: the script identifies all entries starting with
  known base provider prefixes (`google-`, `openrouter-`, etc.) that are no
  longer in the active list

***

## Disabled Entries

Extensions listed as `"disabled"` in the tracking file are kept for reference
but are NOT synced. The sync script removes them from all three targets
(opencode.json, auth.json, account.json) if they already exist from a
previous sync. To re-enable, move the suffix from `"disabled"` to `"active"`
in the tracking file.

***

## Related Skills

- [`opencode-config-preserve`](../../opencode-config-preserve/SKILL.md) —
  Companion skill for preserving OpenCode XDG directories.
- [`opencode-provider-persistence-config`](../../opencode-provider-persistence-config/SKILL.md)
  — Base skill for auth.json persistence model.
- [`opencode-jsonc-util`](../../opencode-jsonc-util/SKILL.md) — Base JSONC utility
  for OpenCode config files.

***

## Traceability

- Created: 2026-07-05
- Source: development session in the private config repo covering
  `sync-provider-extensions.py` and `provider-extensions.json`.
- Script delivery: `sync-provider-extensions.py` is a workflow script
  shipped in this skill per the Script Delivery Mandate. The tracking file
  (`provider-extensions.json`) is delivered as a redacted format reference;
  the operational copy lives in the private config repo.
