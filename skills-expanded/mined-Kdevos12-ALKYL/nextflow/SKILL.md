---
name: nextflow
description: Use when writing, debugging, or optimizing Nextflow pipelines for computational chemistry, bioinformatics, or HPC workflows. Covers DSL2 syntax, process/channel/workflow composition, configuration, containers, and execution on HPC/cloud.
---

# Nextflow

Workflow language for scalable and reproducible computational pipelines — write once, run anywhere (local, HPC, AWS, GCP, Azure).

## When to Use This Skill

- Writing or debugging Nextflow DSL2 pipelines (`.nf` files)
- Composing processes into workflows with channel dataflow
- Configuring executors (SLURM, LSF, AWS Batch, Google Batch)
- Managing containers (Docker, Singularity/Apptainer, Conda) for reproducibility
- Building chemistry/bioinformatics pipelines (BLAST, aligners, RDKit, ORCA, Gaussian)
- Understanding `-resume` / cache behavior
- Modularizing pipelines with `include` / module aliases

## Quick Start — Minimal DSL2 Pipeline

```nextflow
// main.nf
params.input  = 'data/*.sdf'
params.outdir = 'results'

process RUN_ORCA {
    publishDir params.outdir, mode: 'copy'
    container  'quay.io/biocontainers/orca:5.0.4--h2f1ea3e_0'

    input:
    path mol

    output:
    path "*.out"

    script:
    """
    orca ${mol}.inp > ${mol}.out
    """
}

workflow {
    mols = channel.fromPath(params.input)
    RUN_ORCA(mols)
}
```

Run it:
```bash
nextflow run main.nf -profile docker -resume
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Processes, channels, input/output qualifiers, script types | `references/core-concepts.md` |
| Workflows, named workflows, pipe/and operators, modules, composition | `references/pipeline-patterns.md` |
| `nextflow.config`, executors, profiles, HPC/cloud, cache/resume | `references/execution-config.md` |
| Docker, Apptainer/Singularity, Conda, Wave, reproducibility | `references/containers-envs.md` |
| Channel factories, operators, file handling, remote files | `references/files-channels.md` |
| Chemistry/bioinformatics patterns (BLAST, RDKit, ORCA, MD) | `references/chem-bioinformatics.md` |

## Key Concepts at a Glance

| Concept | What it is |
|---------|------------|
| `process` | Runs a script/command; defines `input`, `output`, directives |
| `workflow` | Composes processes and operators via dataflow channels |
| `channel` | Asynchronous stream of values connecting processes |
| `val` / `path` | Input qualifiers — `val` for data, `path` for staged files |
| `publishDir` | Copies task output to a user-visible results directory |
| `executor` | Where tasks run: local, slurm, awsbatch, google-batch… |
| `-resume` | Reuses cached task results; skips unchanged tasks |
| `module` | Reusable `.nf` file included with `include { X } from './module'` |

## Installation

```bash
# Requires Java 11+
curl -s https://get.nextflow.io | bash
./nextflow self-update          # upgrade to latest
nextflow -version               # verify

# Enable DSL2 strict parser (recommended for new pipelines)
export NXF_SYNTAX_PARSER=v2
```

## Related Skills

- `rdkit` — Molecular preprocessing before pipeline ingestion
- `deepchem` — ML models on molecular datasets (can be wrapped in NF processes)
- `cheminformatics` — SMILES, molecular file formats (SDF, MOL2, XYZ)
