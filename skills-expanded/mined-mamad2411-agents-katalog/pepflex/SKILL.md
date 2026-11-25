---
name: pepflex
description: Use when working with PepFlex for in silico peptide screening and evolutionary optimization. Handles peptide population management, mutation, crossover, custom evaluation pipelines, and multi-round evolutionary simulation.
---

# PepFlex

Python framework for in silico peptide evolution: random generation, mutation/crossover, custom fitness evaluation, and multi-round population optimization.

**Repo:** github.com/Kdevos12/PepFlex | **PyPI:** `pepflex==0.0.4`

## When to Use This Skill

- Running evolutionary / genetic algorithm optimization on peptide sequences
- Screening peptide libraries with custom fitness functions (ML models, physicochemical filters)
- Generating, mutating, and recombining SMILES-based peptide representations
- Building multi-round directed evolution simulations in silico
- Integrating ML activity predictors into a peptide optimization loop

## Installation

```bash
pip install pepflex==0.0.4
# Python ≥ 3.8
```

## Core Classes at a Glance

| Class | Role |
|-------|------|
| `PeptideGenerator` | Generate random peptide sequences |
| `Peptide` | Single peptide with sequence, metadata, properties |
| `PeptidePoolManager` | Population container (add, retrieve, size) |
| `PeptideMutator` | Register and apply mutation rules |
| `Evaluator` | Pipeline of fitness functions + ranker |
| `PoolRoundProcessor` | Orchestrate one full evolution round |

---

## Quick Start — Full Evolutionary Loop

```python
from pepflex import (
    PeptideGenerator, Peptide, PeptidePoolManager,
    PeptideMutator, Evaluator, PoolRoundProcessor
)
import pandas as pd

# 1. Generate initial pool
gen = PeptideGenerator()
initial_smiles = gen.generate_random_peptides(num_peptides=50, min_length=5, max_length=15)

pool = PeptidePoolManager()
for i, smiles_list in enumerate(initial_smiles):
    pool.add_peptide(Peptide(smiles_list, peptide_id=f"pep_{i}"))

print(f"Initial pool: {pool.get_pool_size()} peptides")

# 2. Configure mutations
mutator = PeptideMutator()
mutator.add_mutation_rule(mutation_type='n_terminal_addition', probability=0.3)
mutator.add_mutation_rule(mutation_type='inter_mutation',       probability=0.5)

# 3. Define evaluation pipeline (DataFrame-based)
def add_length(df): df["length"] = df["sequence"].str.len(); return df
def filter_min7(df): return df[df["length"] >= 7]
def my_scorer(df):   df["score"] = df["length"] * 0.1; return df  # replace with ML model

pipeline = [add_length, my_scorer, filter_min7]
ranker   = lambda df: df.nlargest(20, "score")

evaluator = Evaluator(evaluation_pipeline=pipeline, ranker_function=ranker)

# 4. Set up round processor
rp = PoolRoundProcessor()
rp.set_generation_function(
    lambda n: [Peptide(s, source_generation_params={"type": "replenishment"})
               for s in gen.generate_random_peptides(n, 5, 15)]
)

rp.add_pipeline_step('mutation',     rp._execute_mutation_step,
                     name='Mutate',  mutator=mutator, probability_of_application=0.8)
rp.add_pipeline_step('crossover',    rp._execute_crossover_step,
                     name='Crossover', num_crossovers=10, crossover_probability_per_pair=0.7)
rp.add_pipeline_step('evaluation',   rp._execute_evaluation_step,
                     name='Evaluate', evaluator_instance=evaluator)
rp.add_pipeline_step('replenishment',rp._execute_replenishment_step,
                     name='Replenish', target_size=50)
rp.add_pipeline_step('truncation',   rp._execute_truncation_step,
                     name='Truncate',  max_size=50)

# 5. Run N rounds
all_logs = pd.DataFrame()
for i in range(5):
    pool, logs = rp.run_round(pool, round_name=f"Round_{i+1}")
    all_logs = pd.concat([all_logs, logs], ignore_index=True)
    print(f"Round {i+1} — pool size: {pool.get_pool_size()}")

# 6. Inspect final population
top = pool.get_all_peptides()[:10]
for p in top:
    print(f"  {p.peptide_id[:8]}  1L={p.one_letter_sequence}  len={p.length}")
```

---

## PeptideGenerator

```python
gen = PeptideGenerator()

# Generate random peptides → list of SMILES lists
smiles_lists = gen.generate_random_peptides(
    num_peptides=100,
    min_length=5,
    max_length=20
)
# smiles_lists[i] = list of amino-acid SMILES for peptide i
```

---

## Peptide

```python
pep = Peptide(
    smiles_list,                              # list of AA SMILES
    peptide_id="my_pep_001",                 # optional unique ID (uuid if omitted)
    source_generation_params={"type": "de_novo"}  # optional provenance
)

# Properties
pep.one_letter_sequence   # e.g. "ACDEFG"
pep.three_letter_sequence # e.g. "Ala-Cys-Asp-Glu-Phe-Gly"
pep.length                # int
pep.peptide_id            # str
```

---

## PeptidePoolManager

```python
pool = PeptidePoolManager()

pool.add_peptide(pep)                  # add one peptide
pool.get_pool_size()                   # → int
all_peps = pool.get_all_peptides()     # → List[Peptide]
```

---

## PeptideMutator

```python
mutator = PeptideMutator()

# Supported mutation_type values:
mutator.add_mutation_rule('n_terminal_addition', probability=0.3)  # add AA at N-term
mutator.add_mutation_rule('inter_mutation',       probability=0.5)  # substitution
mutator.add_mutation_rule('insertion',            probability=0.2)  # insert internal
mutator.add_mutation_rule('deletion',             probability=0.2)  # delete internal
mutator.add_mutation_rule('rearrangement',        probability=0.1)  # reorder segment
```

Probabilities are relative weights — they are normalized internally.

---

## Evaluator & Fitness Pipeline

The evaluation pipeline is a list of functions, each accepting and returning a `pd.DataFrame`. PepFlex converts the peptide population to a DataFrame, then passes it through each step in order.

```python
# Typical pipeline step signatures:
def my_step(df: pd.DataFrame) -> pd.DataFrame:
    # add features, filter rows, apply model…
    return df

# Integration with an ML model (example with scikit-learn):
import joblib
model = joblib.load("activity_model.pkl")

def predict_activity(df: pd.DataFrame) -> pd.DataFrame:
    X = df[["length", "mw", "charge"]].values   # pre-computed features
    df["activity_pred"] = model.predict_proba(X)[:, 1]
    return df

# Ranker: takes final DataFrame, returns top-k rows (same columns)
def top_k_ranker(df: pd.DataFrame) -> pd.DataFrame:
    return df.nlargest(30, "activity_pred")

evaluator = Evaluator(
    evaluation_pipeline=[add_length, add_mw, add_charge, predict_activity],
    ranker_function=top_k_ranker
)
```

### Built-in helper functions

```python
from pepflex import (
    add_length_feature,                       # adds "length" column
    add_dummy_score_feature,                  # adds random "score" (for testing)
    filter_by_length_in_df,                   # filter rows by min_len
    rank_by_dummy_score_and_reconstruct,      # rank by "score", keep top n
)

pipeline = [
    add_length_feature,
    add_dummy_score_feature,
    lambda df: filter_by_length_in_df(df, min_len=7),
]
ranker = lambda df: rank_by_dummy_score_and_reconstruct(df, n_to_keep=20)
```

---

## PoolRoundProcessor — Pipeline Steps

```python
rp = PoolRoundProcessor()

# Required: how to generate new peptides for replenishment
rp.set_generation_function(callable)    # callable(n: int) → List[Peptide]

# Add steps in execution order:
rp.add_pipeline_step(
    step_type,       # 'mutation' | 'crossover' | 'evaluation' | 'replenishment' | 'truncation'
    step_function,   # rp._execute_<type>_step
    name,            # human-readable label in logs
    **kwargs         # step-specific parameters (see below)
)
```

### Step parameters

| step_type | Key kwargs | Description |
|-----------|-----------|-------------|
| `'mutation'` | `mutator`, `probability_of_application` | Apply mutator to each peptide with given probability |
| `'crossover'` | `num_crossovers`, `crossover_probability_per_pair` | Pair-wise recombination |
| `'evaluation'` | `evaluator_instance` | Run fitness pipeline + ranker |
| `'replenishment'` | `target_size` | Add new peptides until pool reaches target_size |
| `'truncation'` | `max_size` | Remove lowest-fitness peptides above max_size |

```python
# Run one round
new_pool, logs_df = rp.run_round(pool, round_name="Round_1")
# logs_df: DataFrame with event logs (step, action, peptide_id, …)
```

---

## Integrating RDKit for Feature Computation

```python
from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

def add_rdkit_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add MW and logP from peptide SMILES."""
    def featurize(smiles_list):
        # Join amino-acid SMILES into full peptide (simplified)
        joined = ".".join(smiles_list) if isinstance(smiles_list, list) else smiles_list
        mol = Chem.MolFromSmiles(joined)
        if mol is None:
            return None, None
        return Descriptors.MolWt(mol), Descriptors.MolLogP(mol)

    df[["mw", "logp"]] = df["smiles_list"].apply(
        lambda s: pd.Series(featurize(s))
    )
    return df.dropna(subset=["mw"])
```

---

## Multi-Round Tracking

```python
import pandas as pd

history = []
for round_num in range(10):
    pool, logs = rp.run_round(pool, round_name=f"Round_{round_num+1}")
    top_score = logs["score"].max() if "score" in logs.columns else None
    history.append({"round": round_num+1, "pool_size": pool.get_pool_size(),
                     "top_score": top_score})

history_df = pd.DataFrame(history)
print(history_df)
```

---

## Best Practices

- **Evaluation pipeline is the core customization point** — replace dummy steps with real ML models or RDKit descriptors
- **Ranker controls selection pressure** — aggressive truncation (keep 20%) = fast convergence; gentle (keep 80%) = diversity
- **Replenishment prevents premature convergence** — keep `target_size` ≥ `max_size` for fresh diversity injection
- **Log every round** (`run_round` returns logs) — concatenate and analyze convergence
- **Crossover + mutation order matters** — mutate after crossover to avoid immediately destroying recombinant sequences
- **Validate peptide SMILES** with RDKit after generation before adding to pool
