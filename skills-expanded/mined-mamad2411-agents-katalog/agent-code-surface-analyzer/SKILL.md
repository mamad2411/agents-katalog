---
name: agent-code-surface-analyzer
description: >-
  Statically enumerate an agent or MCP server's declared tools, dangerous
  actions and declared-versus-actual capability surface from its repository
  or image. Use to inventory what a deployment can do before trusting what
  it says it does, to check MCP tool annotations against the code, or to
  baseline tool descriptions for rug-pull detection.
allowed-tools: Read, Grep, Glob, Bash
---

# Agent Code Surface Analyzer

**Controls:** Static basis for controls 1, 2 and 5

## What this establishes

Every other control is about constraining capability. This skill establishes
what the capability actually **is**, from the code rather than from the
manifest — because the manifest is a claim made by the thing being audited.

## When to use this
Before trusting what a deployment says it does — a new MCP server, an agent
framework you are adopting, a vendor integration. Also on a schedule against
anything already deployed: tool descriptions are fetched at connect time and a
server can change one after review, so the baseline this produces is what makes
a rug-pull visible.

## Procedure

1. **Enumerate declared tools.** From the MCP tool manifest, the tool registry,
   or the decorator/registration sites in code.

2. **Classify each tool by what it actually reaches**, by locating sinks:
   - `subprocess`, `os.system`, `exec`, `eval` → **process execution**
   - `open(...,'w')`, file writes, `shutil`, `os.remove` → **filesystem write**
   - HTTP clients, sockets → **network egress**
   - SDK credential reads, environment access → **credential access**
   - `DELETE`, `DROP`, `TRUNCATE` → **destructive downstream**

3. **Cross-check annotations against the code.** MCP tool annotations
   (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) are
   **hints, not guarantees** — the specification says so explicitly, and a
   server can mislabel a destructive tool as read-only. Treat every annotation
   as a claim to verify, never as truth.

   Apply the spec's pessimistic defaults: an **unannotated** tool is assumed
   `destructiveHint: true` and `openWorldHint: true`.

4. **Record the declared-versus-actual delta.** A tool annotated `readOnlyHint`
   whose body writes a file is the highest-value finding this skill produces.

5. **Hash the tool descriptions.** Store `tool_description_hash` per tool. This
   is the rug-pull baseline: a server can change a tool's description after the
   client approved it, and the hash is what detects that.

## Example

**Input** — the fixture committed at the top of [`scripts/agent_code_surface_analyzer.py`](scripts/agent_code_surface_analyzer.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
C1_default_deny_least_privilege   INTENT_EVIDENCED  runtime verdict needs observed usage and the
C2_sandbox_no_egress              PARTIAL           absence of a covert channel is not provable 
C3_identity_chain_obo             INTENT_EVIDENCED  4 signals; enforcement not shown
C4_gateway_guardrails             INTENT_EVIDENCED  runtime verdict needs reachability testing f
C5_injection_screening            PARTIAL           detector presence is verifiable; robustness 

PASS is not in the vocabulary. The strongest static verdict is
INTENT_EVIDENCED, and two controls cannot exceed PARTIAL at all.
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "deployment_id": "str",
  "tools": [
    {"name": "str", "capability_class": ["process|filesystem|network|credential|destructive"],
     "annotations": {"readOnlyHint": "bool|null", "destructiveHint": "bool|null",
                     "idempotentHint": "bool|null", "openWorldHint": "bool|null"},
     "annotations_present": true,
     "declared_vs_actual": "match|understated|overstated",
     "evidence": [{"file": "str", "line": 0, "sink": "str"}],
     "tool_description_hash": "str"}
  ],
  "dangerous_actions": ["str"],
  "unannotated_count": 0,
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Believing the annotations.** They are advisory. Cross-check or do not
  report on them at all.
- **Missing dynamic registration.** Tools registered at runtime from config do
  not appear in a static scan; record that as a `PARTIAL`, not a clean pass.
- **Hashing the tool name instead of the description.** The description is what
  the model reads and what a rug-pull changes.
