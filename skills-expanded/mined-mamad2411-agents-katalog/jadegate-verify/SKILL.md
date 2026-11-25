---
name: jadegate-verify
description: Run 5-layer security verification on MCP skill files. Checks schema integrity, code injection patterns, dangerous commands, network leaks, and DAG integrity.
---

# Skill Security Verifier

Run 5-layer security verification on MCP skill files. Checks schema integrity, code injection patterns, dangerous commands, network leaks, and DAG integrity.

## When to Use

- User wants to verify if a skill file is safe
- User wants to check a skill before installing it
- User asks about skill security or validation

## Usage

```bash
jadegate verify ./my_skill.json        # Verify a local skill file
jadegate verify slack                  # Verify a skill by name from registry
```

## 5 Security Layers

1. **Schema validation** - Structural integrity against jade-schema-v1
2. **Code injection scan** - 22 dangerous patterns (eval, exec, subprocess, etc.)
3. **Dangerous command detection** - 25 patterns covering destructive ops, permission escalation, etc.
4. **Network/data leak analysis** - Whitelist-based URL and domain filtering
5. **DAG integrity** - Circular dependency and reachability analysis

## Output

Pass/fail for each layer with detailed findings.
