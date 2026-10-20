---
name: science-category-pointer
description: "Pointer to a library of 10 specialized Science skills. Use when working on science-related tasks."
risk: none
---

# Science Capability Library 🎯

This is a **pointer skill**. The 10 specialized Science skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **astropy** — Astropy is the core Python package for astronomy, providing essential functionality for astronomical research and data analysis.
- **biopython** — Biopython is a comprehensive set of freely available Python tools for biological computation. It provides functionality for sequence manipulation, file I/O, database access, structural bioinformatics, phylogenetics, and many other bioinformatics tasks.
- **cirq** — Cirq is Google Quantum AI's open-source framework for designing, simulating, and running quantum circuits on quantum computers and simulators.
- **matplotlib** — Matplotlib is Python's foundational visualization library for creating static, animated, and interactive plots.
- **networkx** — NetworkX is a Python package for creating, manipulating, and analyzing complex networks and graphs.
- **qiskit** — Qiskit is the world's most popular open-source quantum computing framework with 13M+ downloads. Build quantum circuits, optimize for hardware, execute on simulators or real quantum computers, and analyze results. Supports IBM Quantum (100+ qubit systems), IonQ, Amazon Braket, and other providers.
- **scanpy** — Scanpy is a scalable Python toolkit for analyzing single-cell RNA-seq data, built on AnnData. Apply this skill for complete single-cell workflows including quality control, normalization, dimensionality reduction, clustering, marker gene identification, visualization, and trajectory analysis.
- **seaborn** — Seaborn is a Python visualization library for creating publication-quality statistical graphics. Use this skill for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures with minimal code.
- **statsmodels** — Statsmodels is Python's premier library for statistical modeling, providing tools for estimation, inference, and diagnostics across a wide range of statistical methods.
- **sympy** — SymPy is a Python library for symbolic mathematics that enables exact computation using mathematical symbols rather than numerical approximations.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/science/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/science`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
