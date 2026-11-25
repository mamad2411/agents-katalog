---
name: openmath-lean-theorem
description: Configures Lean environments, installs external proof skills, runs preflight checks, guides the proving workflow, and manages LEAN4 benchmarks. Use when the user wants to set up Lean tooling, prove an OpenMath theorem, or run/evaluate benchmarks.
version: v1.0.0
---

# OpenMath Lean Theorem

## Instructions

Set up the Lean proving environment, validate toolchains, prove downloaded OpenMath theorems, and run LEAN4 benchmarks. Assumes the theorem workspace was already created by the `openmath-open-theorem` skill.

### Workflow checklist

- [ ] **Environment**: Verify `lean`, `lake`, and `elan` are installed and match the workspace `lean-toolchain`.
- [ ] **External skills**: Install required Lean proof skills from [leanprover/skills](https://github.com/leanprover/skills):
  ```bash
  git clone --depth 1 https://github.com/leanprover/skills.git /tmp/leanprover-skills
  cp -R /tmp/leanprover-skills/skills/lean-proof ~/.agents/skills/
  cp -R /tmp/leanprover-skills/skills/mathlib-build ~/.agents/skills/
  ```
- [ ] **Preflight**: Run `python3 scripts/check_theorem_env.py <workspace>` (see [references/preflight.md](references/preflight.md)).
- [ ] **Prove**: Use `lean-proof` / `mathlib-build` skills to complete the proof. See [references/proof_playbook.md](references/proof_playbook.md) for the OpenMath-specific proving loop.
- [ ] **Verify**: Confirm `lake build -q --log-level=info` passes and no `sorry` remains.
- [ ] **Submit**: Use the `openmath-submit-theorem` skill to hash and submit the proof.

### Scripts

| Script | Command | Use when |
|--------|---------|----------|
| Preflight check | `python3 scripts/check_theorem_env.py <workspace>` | After download, before proving; validates toolchain, required skills, and initial build. |
| Preflight (auto) | `python3 scripts/check_theorem_env.py <workspace> --auto-install-skills` | Auto-install missing Lean skills during preflight. |

### Benchmarks

A LEAN4 benchmark subsystem for evaluating AI theorem proving. Full agent guide: [benchmarks/AGENTS.md](benchmarks/AGENTS.md).

| Script | Command | Use when |
|--------|---------|----------|
| Setup | `pip3 install -r benchmarks/utils/requirements.txt` | First-time setup for benchmark scripts. |
| Solve | `python3 benchmarks/utils/solve.py --agent claude-code --benchmark-id <id>` | Generate proofs via AI agent. |
| Check | `python3 benchmarks/utils/check.py` | Verify generated proofs with LEAN compiler. |
| Validate | `python3 benchmarks/utils/validate.py -v` | Ensure benchmark sets compile (expect failure, not error). |
| Analyze | `python3 benchmarks/utils/evaluate_results.py` | Summarize and compare benchmark results. |

Scope benchmarks with `--difficulty easy|medium|hard`, `--topic algebra|combinatorics|logic`, or `--benchmark-id <id>`.

### Notes

- **Lean version**: Scaffolds pin `leanprover/lean4:v4.28.0` and `mathlib4 v4.28.0` (set by `openmath-open-theorem`'s `download_theorem.py`).
- **External skills**: Not bundled; install from [leanprover/skills](https://github.com/leanprover/skills) by cloning the repo and copying the needed skill directories into your active skills directory. Required: `lean-proof`, `mathlib-build`. Optional: `lean-mwe`, `lean-bisect`, `nightly-testing`, `mathlib-review`, `lean-setup`.
- **Benchmark status**: `success` = no sorry, `failure` = compiles with sorry, `error` = compilation failed.
- **Benchmark config**: Timeouts and paths in `benchmarks/utils/config.py`.

## References

Load when needed (one level from this file):

- **[references/preflight.md](references/preflight.md)** — Preflight command and Lean/Rocq checks.
- **[references/proof_playbook.md](references/proof_playbook.md)** — Step-by-step workflow for proving a downloaded Lean theorem locally.
- **[references/languages.md](references/languages.md)** — Lean and Rocq/Coq versions and standard libraries.
- **[benchmarks/AGENTS.md](benchmarks/AGENTS.md)** — Full agent guide for the LEAN4 benchmark subsystem.
