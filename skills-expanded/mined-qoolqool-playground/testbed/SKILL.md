---
name: gated-testbed
description: "Gated AI Testbed — structured spec parsing, validation, and feedback for autonomous testbed creation. Use when creating a new testbed, improving an existing one, or validating testbed specifications."
---

# Gated AI Testbed Skill

A gated architecture for creating, validating, and iterating on AI-generated
testbed specifications. Each gate produces structured, machine-readable feedback
that enables autonomous iteration.

## When to Use

- Creating a new testbed from scratch
- Improving an existing testbed (e.g. `/workspace`)
- Validating a testbed specification for completeness and correctness
- Iterating on a spec that failed validation
- Before running any testbed deployment

## Architecture

```
[ USER SPEC ] ──→ Gate 1: Spec Parser ──→ Gate 2: Code Validator
                                              ↓
                    [ REPO BASE ] ←── Gate 4: Runtime Test ←── Gate 3: Guardrail Vetting
```

**Current MVP implements:** Gate 1 (Spec Parsing & Linting) + Gate 2 (Code / Artifact Validator) + Gate 3 (Security & Policy Guardrails) + shared contracts.

## Location

All code lives at `/project/tooling/testbed/`.

## Quick Start

```bash
# Check the environment first
./testbed.sh check

# Create a new testbed spec from template
./testbed.sh init my-testbed

# Validate a JSON spec directly (preferred — avoids weak fallback parser)
./testbed.sh validate /workspace/quic-edge-spec.json

# Parse a markdown spec through Gate 1 (uses LLM if available)
./testbed.sh parse examples/success_spec.md

# Pretty-print a feedback JSON
./testbed.sh feedback /tmp/feedback.json

# Show example specs
./testbed.sh example success
./testbed.sh example failure

# Run Gate 3 — Security & Policy Guardrails
./testbed.sh gate3 --spec /workspace/quic-edge-v2-spec.json --workspace /workspace

# Run the full demo
python3 /project/tooling/testbed/examples/demo.py

# Run tests
cd /project/tooling/testbed && python3 -m pytest tests/ -v
```

## Procedure

### Phase 0: Critical Service Analysis

Before writing a spec, critically examine every proposed service:

1. **Does it belong in this phase?** If the service supports a future phase's requirements, remove it. Each phase should be self-contained and testable independently.
2. **Is it redundant?** Can two services be consolidated? (e.g., health-api merged into mock-payment-api)
3. **Is it the right tool?** Question every choice:
   - Why Envoy over Nginx? (observability, xDS, gRPC support)
   - Why a STUN server? (Phase 3 concern, not Phase 1)
   - Why a dedicated client? (essential — without it you can't verify the service works)
4. **What's missing?** If you can't test a deliverable without a service, add it. (e.g., quic-client is essential for H3 handshake testing)
5. **Document the decision.** Every service should have a `description` field explaining why it exists and what alternatives were considered.

### Phase 1: Extract Spec from User Request

1. Collect the user's natural language description of the testbed
2. Perform Phase 0 analysis on the proposed services
3. Write the spec as a JSON file (preferred — avoids weak fallback parser)
4. Validate:
   ```bash
   ./testbed.sh validate /workspace/my-spec.json
   ```
5. Read the feedback and iterate

### Phase 2: Handle Feedback

**If status=pass:**
- Review warnings (non-blocking but informative)
- The validated TestbedSpec is ready for downstream gates

**If status=fail:**
- Read the diagnostics to understand what's wrong
- Read the suggested actions for guidance
- Fix the spec and re-run Gate 1
- Repeat until pass

### Phase 4: Run Gate 3 (Security & Policy Guardrails)

After Gate 2 passes and before claiming HARDEN / runtime-ready:

1. Run Gate 3:
   ```bash
   ./testbed.sh gate3 --spec /workspace/quic-edge-v2-spec.json --workspace /workspace
   ```
2. Read the feedback

**If status=pass:**
- Review info-level diagnostics (allowlisted exceptions, awareness notes)
- The testbed is safe to run under policy
- Proceed to HARDEN / runtime testing

**If status=fail:**
- Read the diagnostics to understand which security/policy issues exist
- Read the suggested actions for guidance
- Fix the issues (remove privileged mode, replace secrets with references, etc.)
- Re-run Gate 3
- Repeat until pass

**Hard rule: Do NOT claim HARDEN / runtime-ready while Gate 3 is failing.**

### Phase 5: Use the Spec

The validated TestbedSpec can be:
- Passed to Gate 2 (Code Validator) — validates generated code matches spec
- Passed to Gate 3 (Guardrail Vetter) — checks security/compliance policies
- Passed to Gate 4 (Runtime Test) — runs the testbed and reports results
- Serialized to JSON for storage or transmission

## Key Contracts

### TestbedSpec Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Human-readable testbed name |
| `version` | ❌ | Semantic version (default: 0.1.0) |
| `description` | ✅ | Purpose, scope, and phase boundaries |
| `tags` | ❌ | Categorization tags |
| `services` | ✅ | Docker services (min 1) |
| `test_suites` | ❌ | Test suites |
| `infrastructure` | ❌ | Networks, volumes |
| `constraints` | ❌ | Resource constraints |
| `guardrails` | ❌ | Security guardrails |

### GateFeedback Fields

| Field | Description |
|-------|-------------|
| `gate_id` | Which gate produced this |
| `status` | pass / fail / error / skip |
| `diagnostics` | Issues found, ordered by severity |
| `actions` | Suggested fixes, ordered by priority |
| `spec_snapshot` | The spec at time of evaluation |
| `attempt_number` | Which attempt (for iteration tracking) |

## Pitfalls

- **The fallback keyword parser is weak.** When Ollama is unavailable, `parse` with markdown produces garbage. Always use `validate` with a JSON spec for reliable results.
- **PYTHONPATH must be set.** Use `./testbed.sh` (wrapper script) or `export PYTHONPATH=/project/tooling` before running commands.
- **pip install is blocked** by PEP 668. Use `--break-system-packages` or set PYTHONPATH instead.
- **Gate 1 validates the *spec*, not the *code*.** Code validation comes in Gate 2.
- **Gate 3 validates security posture, not spec completeness.** Do not skip Gate 1 or Gate 2 because Gate 3 passes.
- **Memory limits on services** are critical for resource-constrained hosts.
- **Don't add future-phase services.** Each phase should be self-contained. Premature services add complexity without testable benefit.
- **Every service needs a `description` field.** This forces you to justify why the service exists and document design decisions.
- **Gate 3 uses an explicit allowlist.** Known exceptions (netem NET_ADMIN, otel distroless healthcheck) are in `gates/policy_allowlist.py`. Do not add silent code branches for new exceptions — update the allowlist instead.
- **Gate 3 does not replace image CVE scanning.** It checks policy compliance, not runtime vulnerabilities.

## Verification

After running Gate 1:
1. Check that `status=pass` in the feedback
2. Review all warnings — they indicate missing optional fields
3. Verify the extracted services match the user's intent
4. Run the test suite: `cd /project/tooling/testbed && python3 -m pytest tests/ -v`
5. Run the environment check: `./testbed.sh check`

After running Gate 3:
1. Check that `status=pass` in the feedback
2. Review info-level diagnostics for allowlisted exceptions
3. Verify no unexpected privileged containers, dangerous mounts, or hardcoded secrets
4. Confirm the allowlist in `gates/policy_allowlist.py` is up to date with known decisions
5. Only then proceed to HARDEN / runtime-ready claims

## ADD Cross-Reference

The ADD (Audit-Driven Delivery) pipeline owns build work. Gate 3 is a quality gate checkpoint:
- Run Gate 3 after Gate 2 passes, before HARDEN
- If Gate 3 fails, do not HARDEN — fix the issues first
- Gate 3 does not replace ADD phases; it validates that the output is safe to run

See `add-audit-driven-delivery` skill for the full delivery pipeline.
