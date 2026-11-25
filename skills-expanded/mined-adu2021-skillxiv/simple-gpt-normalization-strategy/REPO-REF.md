# Repo Ref
- source: https://github.com/adu2021/skillxiv (path: skills/skillxiv-v0.0.2-claude-opus-4.6/simple-gpt-normalization-strategy/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: Place RMSNorm immediately after every linear layer to stabilize activation scales at O(sqrt(d)) and reduce Hessian spectral norm. Enables 3-10x larger learning rates and faster convergence without arc
