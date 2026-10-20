# Uplifting Biomolecular Modeling — Inference Optimization Kits

36 drop-in optimization kits for open protein- and genomics-ML tools. Each kit accelerates a pinned upstream release (structure prediction, cofolding, binder/sequence design, protein/genomic language models) under a named **mode** without changing how you call the tool.

**Source:** `anthropics/uplifting-biomolecular-modeling` (reference release; Apache-2.0; not maintained)
**Local clone:** `/home/user/anthropics/uplifting-biomolecular-modeling`

---

## Modes (universal vocabulary)

| Mode | Behaviour |
|------|-----------|
| `off` | Stock upstream, nothing engaged |
| `exact` | Identical outputs to `off`, faster |
| `fast` | Small documented numeric differences, faster still (usually default) |
| `big` | Lowest peak GPU memory; `--n_gpu P` splits across P GPUs |

What runs prints one `[<kit>-opt] ACTIVE mode=…` line on stderr. Failure to engage prints `NOT ACTIVE: <reason>` and exits 3 — never a silent fallback.

---

## Install & run pattern (every kit)

```bash
# 1. Get the pinned stack (pick one route — each kit's README says which it ships)
#    A — Docker   B — Apptainer   C — Python venv (uv)

# 2. From the kit directory:
bash run.sh install [--weights /weights/<kit>]
export <KIT>_WEIGHTS=/weights/<kit>   # as the kit's Setup shows

# 3. Dry-run (resolves mode, prints what would engage):
bash run.sh check

# 4. Run (upstream args pass through verbatim):
bash run.sh <command> --config <card> --mode <mode> [upstream args…]
```

Library-style kits (`enformer`, `enformer_deepmind`, `esmc`, `gpnstar`, `flashzoi`) use an env-var instead:
```bash
<KIT>_OPT=exact python your_script.py
# or call kit.enable() from inside the script
```

---

## Kit catalogue

### Structure prediction & cofolding

| Kit | Upstream | Task | Modes |
|-----|----------|------|-------|
| `af2ig` | AF2 initial guess (dl_binder_design) | Binder–target interface scoring | off · exact · fast · big |
| `af3_jax` | AlphaFold 3 (JAX) on OpenFold3 weights | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `af3_torch` | xfold (PyTorch AF3) on OpenFold3 weights | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `atlasfold` | atlasfold 1.0.0 | Structure prediction | off · exact · fast · big |
| `boltz2` | Boltz-2 2.2.1 | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `chai1` | Chai-1 0.6.1 | Cofolding | off · exact · fast · big |
| `colabfold` | ColabFold 1.6.1 (AF2-Multimer v3) | Structure prediction from MSAs | off · exact · fast · big · `--n_gpu P` |
| `esmfold2` | ESMFold2 / ESMFold2-Fast | Structure prediction | off · exact · fast · big · `--n_gpu P` |
| `opendde` | OpenDDE 1.1.1 | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `openfold3` | OpenFold3 0.4.1 (preview2 weights) | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `openfold3_ob0` | OpenFold3 0.5.0 (OpenBind-0) | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `protenix_v1` | Protenix 1.1.0 | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `protenix_v2` | Protenix 2.0.0 | Cofolding | off · exact · fast · big · `--n_gpu P` |
| `rosettafold3` | RoseTTAFold3 (foundry rf3) | Cofolding | off · exact · fast · big · `--n_gpu P` |

### Binder & sequence design

| Kit | Upstream | Task | Modes |
|-----|----------|------|-------|
| `boltzgen` | BoltzGen 0.3.2 | Binder design | off · exact · fast · big |
| `caliby` | Caliby / SolubleCaliby | Sequence design | off · exact · fast |
| `colabdesign` | BindCraft on ColabDesign 1.1.3 | Binder hallucination | off · exact · fast |
| `complexa` | Proteina-Complexa 1.1.0 | Binder generation | off · exact · fast · big |
| `ef2inv` | ESM cookbook through ESMFold2 | Gradient-based binder design | off · exact · fast · big |
| `esm_if1` | ESM-IF1 (fair-esm 2.0.1) | Inverse folding | off · fast |
| `genie3` | Genie 3 (aqlaboratory) | Backbone diffusion, binder design | off · exact · fast |
| `mosaic` | mosaic (escalante-bio) → Boltz-2 via joltz | Binder hallucination | off · exact · fast · big |
| `proteinmpnn` | ProteinMPNN (dauparas) | Sequence design | off · exact |
| `pxdesign` | PXDesign (Protenix 0.5.0+pxd) | Binder diffusion | off · exact · fast · big |
| `rfdiffusion1` | RFdiffusion 1.1.0 | Backbone generation | off · exact · fast |
| `rfdiffusion3` | RFdiffusion3 (foundry rfd3) | All-atom backbone generation | off · exact · fast |

### Protein language models

| Kit | Upstream | Task | Modes |
|-----|----------|------|-------|
| `e1` | E1 (Profluent) 150m/300m/600m | Mutant scoring | off · exact |
| `esmc` | ESM C 300m/600m/6b | Protein LM inference | off · exact |
| `progen2` | ProGen2 (salesforce) | Sampling and likelihood | off · exact |

### Genomics & variant effect

| Kit | Upstream | Task | Modes |
|-----|----------|------|-------|
| `borzoi` | Borzoi (calico, TensorFlow) | Variant effect scoring | off · exact |
| `chrombpnet` | ChromBPNet 1.0.1 | Chromatin accessibility prediction | off · exact · fast |
| `enformer` | enformer-pytorch 0.8.12 | Genomic track prediction | off · exact |
| `enformer_deepmind` | Enformer TensorFlow (TF-Hub) | Genomic track prediction | off · exact |
| `evo2` | Evo 2 7b/40b | Genomic LM scoring and generation | off · exact · fast |
| `flashzoi` | Flashzoi (borzoi-pytorch 0.5.1) | Genomic track prediction | off · exact |
| `gpnstar` | GPN-Star (whole-genome alignments) | Variant effect scoring | off · exact |

---

## Key files per kit

```
<kit>/
  README.md       — setup, run commands, notes
  STOCK.md        — exact upstream pin, software stack, env vars
  CHANGES.md      — what each mode changes
  run.sh          — entry point: install / check / run commands
  opt/            — kit's own Python package
  stock/          — pinned upstream release (never edited)
  environment/    — Dockerfile, apptainer.def, requirements.lock
  configs/        — per-GPU-card env files (h100.env, a100.env, …)
```

`common/opt_core/` — shared runtime (mode resolution, ACTIVE line, memory/multi-GPU, FlashPairformer, triangle-attention kernels).

---

## Hardware

- Primary target: NVIDIA H100 80 GB, Linux x86-64.
- NVIDIA driver floor: 525–580 (kit-specific; stated in each Setup).
- A100 / H200 / B200 / B300: kits that ship `configs/<card>.env` support those cards.

---

## Compile caches

- First run per mode compiles kernels (seconds to minutes); subsequent runs load from cache.
- JAX kits (`af2ig`, `colabdesign`, `mosaic`) recompile per new input length/shape.
- Set `MODEL_OPT_JIT_ROOT` to a persistent directory to keep compiled kernels across sessions.
- Default cache: `${TMPDIR:-/tmp}/model_opt_jit-uid<uid>` (mode 0700, per-user).

---

## Prompts

### Decide which kit to use for a task

```
I want to [TASK: cofolding / binder design / structure prediction / variant scoring / sequence design].
My GPU is [H100 / A100 / other] with [X] GB VRAM.
I need [exact reproducibility / best speed / lowest memory].
Which kit should I use and what mode?
```

### Set up and run a kit

```
Walk me through setting up [KIT_NAME] using [route A Docker / route B Apptainer / route C venv].
My GPU: [card], driver version: [X].
Show the exact commands from install through a sample run.
```

### Compare two kits for the same task

```
Compare [KIT_A] vs [KIT_B] for [TASK]:
- Upstream model and version
- Modes available
- Typical speedup in fast/exact vs off
- Memory requirements
- When to prefer one over the other
```

### Explain a mode's trade-offs

```
Explain the difference between exact and fast modes in [KIT_NAME]:
- What numeric differences are documented?
- Are they within seed-to-seed variation?
- When is exact required vs fast acceptable?
```

### Troubleshoot a NOT ACTIVE exit

```
[KIT_NAME] printed: [NOT ACTIVE: <reason>]
My environment: [GPU, driver, OS, Python version].
What does this mean and how do I fix it?
```

### Security checklist before deploying a kit

```
I want to deploy [KIT_NAME] in [production / shared cluster / cloud].
Review the security considerations relevant to this kit and flag anything I need to address.
```
