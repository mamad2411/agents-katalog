# buildr-gemini-forge — The 200k Factory Conductor

## Purpose
To orchestrate the generation of high-value workspaces by systematically mixing Blueprints, Traits, and ground-repo components (Vault/Catalog).

## Context
This skill is the "Gemini-way" of executing the Buildr v2 Advanced Flow. It prioritizes economic output and architectural reuse over manual reasoning.

## Mandatory Sequencing

### 1. Blueprint Discovery & Selection
- **Scan:** Read `v2-gemini/blueprints/*.json`.
- **Match:** Identify the **Anchor** (Primary Business Model) and **Supplemental** (Design/Cognitive/Logic) Blueprints.
- **Value Check:** Confirm the combined `target_market_value_sek` meets the user's expectations.

### 2. Systematic Component Mapping
You MUST NOT invent component IDs. Map Blueprint `traits` and `core_modules` to:
- **Catalog:** Check `catalog/index.json` for matching module IDs.
- **Vault:** Use `python engines/vault_selector.py --query "[blueprint_trait]"` to identify supporting routines and skills.
- **Engines:** Identify which `ProjectCategory` and `TechStack` from `engines/forge_engine.py` apply.

### 3. Preflight Staging (The 200k Gate)
Use the `buildr-workspace-architect` protocol to generate preflight artifacts, but **enrich** them with:
- **CRI:** Inject values from the selected Blueprints.
- **Decisions:** Record every "Mixed Composition" choice as a decision in `PREFLIGHT_DECISIONS.json`.
- **Staging Path:** Always use `v2/.buildr/preflight/<slug>/`.

### 4. Memory Integration
For every significant architectural choice, you MUST log a discovery:
```bash
bash memory-system/tools/discovery-write.sh \
  --session "v2-gemini" \
  --topic "architecture-mix" \
  --content "Mixed [Anchor] with [Design-Trait] to achieve [Value] SEK. Used Catalog IDs: [IDs]"
```

### 5. Generation Handoff
When `PREFLIGHT_APPROVAL.json` is `approved`:
- Call `python -m engines.forge_engine --spec [path]` (or equivalent) to generate the scaffold.
- **Inject:** Copy `v2-gemini/templates/MIXED_HANDOFF.md` into the generated workspace root.

## Quality Standards
- No orphan modules: every module must have a corresponding AC-ID.
- No design drift: all UI components must follow the `design-system-editorial` tokens.
- No blind builds: every wave must have an assigned agent from the `agents/agent-manifest.json`.

---

**AUTHOR_GATE: PASS**
