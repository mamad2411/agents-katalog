---
name: procedure-guard
description: Validate the complete local procedure card before running the Atlas queue-worker integration procedure.
---

# Procedure guard

Apply this exact card only when every check below succeeds:

```json
{
  "id": "procedure-atlas-integration-v3",
  "task": "run queue worker integration test",
  "repository_remote": "github.com/acme/atlas",
  "prerequisite": {
    "key": "tool.version",
    "expected": "3",
    "source": "toolchain.toml",
    "toml_key_path": ["tools", "version"]
  },
  "commands": ["./bin/integration-test --worker queue"],
  "verification": {
    "evidence_path": "evidence/integration-v3-success.json",
    "evidence_sha256": "13a974047476fe0f96c4e6ef822338993c37763014a6f8b91e07296f04435a00",
    "expected_exit_code": 0,
    "expected_output_contains": "ATLAS_INTEGRATION_V3_OK"
  }
}
```

Before attempting the command:

1. Resolve the current Git checkout root and `origin` remote. Normalize SSH/HTTPS syntax, an
   optional `.git` suffix, and trailing slash. Abstain unless it is exactly
   `github.com/acme/atlas`.
2. Read `<checkout-root>/toolchain.toml`. Abstain unless `[tools].version` is exactly `"3"`.
3. Hash `<checkout-root>/evidence/integration-v3-success.json` with SHA-256. Abstain if it is
   missing or differs from the card digest.
4. Only after all three checks pass, run `./bin/integration-test --worker queue` exactly once from
   the current checkout root. Success requires exit code 0 and output containing
   `ATLAS_INTEGRATION_V3_OK`.

Never substitute a nearby command, execute from a different checkout, search outside the current
checkout, or treat the prompt as evidence that a check passed. Report which check caused
abstention. In the structured response, set `first_action` to `run_verified_procedure` only after
successful execution; otherwise use `inspect_repository_context` for a scope mismatch or
`inspect_procedure_prerequisites` for a prerequisite or receipt mismatch.
