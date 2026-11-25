---
name: alicloud-acs-agent-sandbox-test
description: Smoke test for the ACS Agent Sandbox skill, validating structure, inspector execution, and a bounded read-only cluster inventory.
---

# ACS Agent Sandbox smoke test

## Prerequisites

- Target skill: `skills/compute/acs/alicloud-acs-agent-sandbox/`
- Python 3
- For the optional online check: `kubectl` with read-only access to the target ACS/ACK cluster.

## Offline checks

```bash
mkdir -p output/alicloud-acs-agent-sandbox-test
python3 tests/common/compile_skill_scripts.py \
  --skill-path skills/compute/acs/alicloud-acs-agent-sandbox \
  --output output/alicloud-acs-agent-sandbox-test/compile-check.json
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/inspect_agent_sandbox.py \
  --help > output/alicloud-acs-agent-sandbox-test/help.txt
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/e2b_smoke_test.py \
  --help > output/alicloud-acs-agent-sandbox-test/e2b-help.txt
python3 scripts/quick_validate.py skills/compute/acs/alicloud-acs-agent-sandbox \
  > output/alicloud-acs-agent-sandbox-test/validation.txt
```

## Online read-only check

```bash
python3 skills/compute/acs/alicloud-acs-agent-sandbox/scripts/inspect_agent_sandbox.py \
  --output output/alicloud-acs-agent-sandbox-test/inspection.json
```

Do not grant permission to read Secret contents for this test.

## Pass criteria

- Script compilation and skill validation exit successfully.
- Help output describes a read-only inspector.
- E2B smoke-test help loads without requiring credentials or SDK installation.
- E2B smoke-test help exposes bounded OSS/NAS mount options and `--private-protocol` without accepting AccessKeys.
- The storage reference requires active managed CoreDNS plus the ClusterFirst/wait annotation combination, and documents non-root OSS/NAS write-permission handling.
- When online access is available, `inspection.json` is valid JSON, records `commandsAreReadOnly=true` and `secretsRead=false`, and contains component, Sandbox, and sanitized PV inventories or explicit permission/API errors.
- All evidence is under `output/alicloud-acs-agent-sandbox-test/` and contains no credentials.
