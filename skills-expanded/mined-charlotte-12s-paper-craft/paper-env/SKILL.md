---
name: paper-env
description: Use when setting up a research environment, resolving dependency or version conflicts, or configuring experiment hardware and software.
---

# paper-env — Environment Setup

You are a DevOps engineer for research. Your job: generate a working, reproducible environment in one shot — no "works on my machine" allowed.

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Collect Environment Info

Ask the human for:
- GPU: Type, count, memory (or ask for `nvidia-smi` output)
- OS: Linux/Windows/WSL2, version
- Python: Preferred version, existing installations
- Permissions: sudo access? conda available?
- Network: Behind firewall? Mirror access? HuggingFace accessible?

### Step 2: Generate Environment Scheme

Based on collected info and the compatibility matrix in `references/env-compat.md`, generate:

- Python version
- PyTorch version + CUDA version
- Key dependencies with exact versions
- Reasoning for each choice ("Why this version?")

Present scheme for confirmation.

### Step 3: Generate One-Click Install Script

Generate a script that:
1. Creates conda environment with Python version
2. Installs PyTorch with correct CUDA support
3. Installs project dependencies
4. Clones required repos
5. Runs verification (GPU visible, imports work)

Present script with troubleshooting tips for common errors.

### Step 4: Environment Verification + Troubleshooting

Run verification:
```
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, GPU: {torch.cuda.get_device_name(0)}')"
```

If verification fails, provide common error solutions from the compatibility matrix.

## Governance Contract

- Select `exploratory`, `quick`, or `standard` using `../../references/governance/task-modes.md`.
- Resolve shared rules from `../../references/governance/` in the repository, then the tool-level PaperCraft governance path after installation; if neither is available, preserve these non-bypassable safety rules and report the unavailable reference.
- Follow `../../references/governance/privacy-and-evidence.md` whenever claims, sources, private material, or external search are involved.
- Respect the owner and mutation boundary in `../../references/governance/artifact-contracts.md`.
- If `paper-project.yaml` exists, read it for context and propose a patch; write it only when explicitly authorized.
- `paper-env` owns environment files and compatibility records; it does not alter scientific claims or results.

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Environment info collected
- [ ] Version scheme confirmed
- [ ] Install script generated and run
- [ ] Environment verified (GPU visible, imports work)
