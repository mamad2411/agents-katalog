---

## name: synthetic-systems
description: >
  Synthetic biology expert for engineering biological systems. Use this skill whenever the
  user needs: designing synthetic gene circuits, modeling genetic networks, applying
  systems engineering to biology, working with DNA assembly methods, optimizing bioprocesses,
  creating biosensors, or any task involving the design and construction of novel
  biological systems. This skill covers the Design-Build-Test-Learn cycle, computational
  modeling, DNA assembly techniques, and applications in biotechnology.
license: MIT
compatibility: opencode
metadata:
  audience: synthetic biologists
  category: biology

# Synthetic Biology — Engineering Biological Systems

Covers: **Gene Circuit Design · Mathematical Modeling · DNA Assembly · Genetic Parts · DBTL Cycle · Biosensors · Metabolic Engineering · CRISPR Systems**

-----

## Systems Engineering in Biology

### Design-Build-Test-Learn (DBTL) Cycle

The DBTL cycle is the core framework for synthetic biology:

```python
# DBTL workflow structure
class DBTLCycle:
    def __init__(self):
        self.design = DesignPhase()
        self.build = BuildPhase()
        self.test = TestPhase()
        self.learn = LearnPhase()
    
    def run_cycle(self, objective, iterations=10):
        """
        Execute DBTL cycles until objective is met.
        """
        results = []
        
        for i in range(iterations):
            print(f"\n=== Cycle {i+1} ===")
            
            # 1. Design
            design = self.design.create_design(objective)
            print(f"Design: {design['parts']}")
            
            # 2. Build
            construct = self.build.assemble(design)
            print(f"Built: {construct['name']}")
            
            # 3. Test
            measurements = self.test.measure(construct)
            print(f"Measurements: {measurements}")
            
            # 4. Learn
            insights = self.learn.analyze(measurements, design)
            print(f"Insights: {insights}")
            
            results.append({
                'cycle': i,
                'design': design,
                'measurements': measurements,
                'insights': insights
            })
            
            # Update objective based on learning
            objective = self.update_objective(objective, insights)
        
        return results
    
    def update_objective(self, objective, insights):
        """Refine objective based on cycle insights"""
        # Modify design parameters based on what was learned
        return objective

# Design phase components
design_phase = {
    'parts_selection': 'Choose genetic parts (promoters, RBS, CDS, terminators)',
    'circuit_topology': 'Design circuit architecture',
    'parameter_estimation': 'Set expected values for parameters',
    'simulation': 'Model expected behavior',
    'safety_check': 'Verify biosafety considerations'
}
```

### Abstraction Levels in Synthetic Biology

| Level | Description | Examples |
|-------|-------------|----------|
| **DNA** | Sequence of nucleotides | A, T, G, C |
| **Part** | Functional unit | Promoter, RBS, CDS, terminator |
| **Device** | Combination of parts | AND gate, oscillator |
| **System** | Multiple devices | Toggle switch, repressilator |
| **Chassis** | Host organism | E. coli, S. cerevisiae, mammalian cells |

```python
# Standard biological parts
class GeneticPart:
    def __init__(self, name, part_type, sequence):
        self.name = name
        self.part_type = part_type  # promoter, rbs, cds, terminator
        self.sequence = sequence
    
    def get_sequence(self):
        return self.sequence

# Part types with properties
part_registry = {
    'promoter': {
        'function': 'RNA polymerase binding site',
        'types': ['constitutive', 'inducible', 'repressible'],
        'examples': ['BBa_J23100', 'BBa_R0040', 'BBa_T7']
    },
    'rbs': {
        'function': 'Ribosome binding site',
        'properties': ['strength', 'spacing'],
        'examples': ['BBa_B0034', 'BBa_B0030']
    },
    'cds': {
        'function': 'Coding sequence',
        'features': ['start_codon', 'stop_codon', 'codon_optimization']
    },
    'terminator': {
        'function': 'Transcription termination',
        'types': ['rho-dependent', 'rho-independent']
    }
}
```

-----

## Mathematical Modeling of Gene Circuits

### Ordinary Differential Equation (ODE) Models

```python
import numpy as np
from scipy.integrate import odeint

# Basic gene expression model
def gene_expression_model(y, t, params):
    """
    Simple model of gene expression.
    y = [mRNA, Protein]
    params = [k_tx, k_tl, d_m, d_p]
    """
    mRNA, protein = y
    k_tx, k_tl, d_m, d_p = params
    
    # Transcription: mRNA production
    dm_dt = k_tx - d_m * mRNA
    
    # Translation: Protein production from mRNA
    dp_dt = k_tl * mRNA - d_p * protein
    
    return [dm_dt, dp_dt]

# Simulate
def simulate_gene_expression(t_max=100, params=None):
    if params is None:
        params = [1.0, 0.5, 0.1, 0.05]  # k_tx, k_tl, d_m, d_p
    
    t = np.linspace(0, t_max, 1000)
    y0 = [0, 0]  # Initial conditions: [mRNA, protein]
    
    solution = odeint(gene_expression_model, y0, t, args=(params,))
    
    return t, solution

# Example: Repressible gene circuit (negative feedback)
def repressible_circuit(y, t, params):
    """
    Repressible circuit with negative feedback.
    """
    R, G, P = y  # Repressor, GFP, Protein
    k_prod_R, k_deg_R, k_prod_G, k_deg_G, k_prod_P, k_deg_P = params
    K_d = 10  # Dissociation constant
    
    # Hill function repression
    repression = K_d**n / (K_d**n + P**n)
    
    dR_dt = k_prod_R * repression - k_deg_R * R
    dG_dt = k_prod_G - k_deg_G * G
    dP_dt = k_prod_P * G - k_deg_P * P
    
    return [dR_dt, dG_dt, dP_dt]
```

### Stochastic Modeling

```python
# Stochastic simulation (Gillespie algorithm)
def gillespie_simulation(stoichiometry, propensity_fn, initial_state, t_max):
    """
    Gillespie algorithm for stochastic simulation.
    """
    state = np.array(initial_state)
    t = 0
    trajectory = [state.copy()]
    times = [t]
    
    while t < t_max:
        # Calculate propensities
        a = propensity_fn(state)
        a0 = sum(a)
        
        if a0 == 0:
            break
        
        # Time to next reaction
        tau = np.random.exponential(1.0 / a0)
        
        # Select reaction
        r = np.random.choice(len(a), p=a/a0)
        
        # Update state
        state = state + stoichiometry[r]
        t += tau
        
        trajectory.append(state.copy())
        times.append(t)
    
    return np.array(times), np.array(trajectory)

# Example: Simple gene expression (constitutive)
def constitutive_expression_stochastic():
    stoichiometry = [
        [1, 0],   # Transcription: +1 mRNA
        [-1, 0],  # mRNA degradation
        [0, 1],   # Translation: +1 protein
        [0, -1]   # Protein degradation
    ]
    
    def propensity(state, params):
        k_tx, k_deg_m, k_tl, k_deg_p = params
        mRNA, protein = state
        return [
            k_tx,                    # Transcription
            k_deg_m * max(mRNA, 0),  # mRNA decay
            k_tl * max(mRNA, 0),     # Translation
            k_deg_p * max(protein, 0)  # Protein decay
        ]
    
    params = [1.0, 0.1, 0.5, 0.05]
    initial = [0, 0]
    
    return gillespie_simulation(stoichiometry, propensity, initial, 100)
```

### Boolean Network Models

```python
# Boolean network for gene regulation
class BooleanNetwork:
    def __init__(self, genes, update_functions):
        self.genes = genes
        self.update_fn = update_functions
        self.state = {g: 0 for g in genes}
    
    def update(self):
        """Synchronous Boolean update"""
        new_state = {}
        for gene in self.genes:
            new_state[gene] = self.update_fn[gene](self.state)
        self.state = new_state
        return self.state
    
    def simulate(self, steps):
        """Run simulation"""
        trajectory = [self.state.copy()]
        for _ in range(steps):
            self.update()
            trajectory.append(self.state.copy())
        return trajectory

# Example: Toggle switch
toggle_switch = BooleanNetwork(
    genes=['A', 'B'],
    update_functions={
        'A': lambda s: 1 - s['B'],  # A is ON when B is OFF
        'B': lambda s: 1 - s['A']   # B is ON when A is OFF
    }
)
```

-----

## DNA Assembly Methods

### Common Assembly Strategies

```python
# Golden Gate Assembly (Type IIS restriction)
class GoldenGateAssembly:
    def __init__(self, overhangs):
        self.overhangs = overhangs  # Dictionary of overhangs
    
    def design_primers(self, part, destination_overhang):
        """
        Design primers with overhangs.
        """
        forward = part.sequence[:20] + self.overhangs[destination_overhang]
        reverse = self.reverse_complement(
            part.sequence[-20:] + self.overhangs[destination_overhang]
        )
        return {'forward': forward, 'reverse': reverse}
    
    def assemble(self, parts):
        """
        Combine parts in correct order.
        """
        # All parts have compatible overhangs
        return ''.join([p.sequence for p in parts])

# Gibson Assembly (overlap-based)
class GibsonAssembly:
    def __init__(self, overlap_length=20):
        self.overlap_length = overlap_length
    
    def generate_overlaps(self, part1_seq, part2_seq):
        """
        Generate overlapping regions for Gibson.
        """
        overlap = part1_seq[-self.overlap_length:]
        return overlap
    
    def design_primers_for_ Gibson(self, part, direction):
        """
        Design primers with overlaps for Gibson.
        """
        # Forward primer adds overlap to next part
        # Reverse primer adds overlap to previous part
        pass

# BioBricks Assembly (Standard assembly)
class BioBricksAssembly:
    def __init__(self):
        self.prefix = 'GAATTCGCGGCCGCTTCTAG'  # EcoRI-XbaI
        self.suffix = 'TACTAGTAGCGGCCGCTGCAG'  # SpeI-PstI
    
    def prefix_parts(self, part):
        """Add prefix to part"""
        return self.prefix + part.sequence
    
    def suffix_parts(self, part):
        """Add suffix to part"""
        return part.sequence + self.suffix
```

### Part Design Principles

```python
# Codon optimization
def optimize_codon_usage(gene_sequence, organism='e_coli'):
    """
    Optimize codon usage for expression.
    """
    # Codon usage tables
    codon_usage = {
        'e_coli': {
            'TTT': 0.56, 'TTC': 0.54, 'TTA': 0.14, 'TTG': 0.14,
            'TCT': 0.18, 'TCC': 0.15, 'TCA': 0.15, 'TCG': 0.14,
            # ... complete table
        }
    }
    
    # Replace rare codons with common ones
    optimized = gene_sequence  # Simplified
    return optimized

# RBS Calculator
def calculate_rbs_strength(sequence, model='shine_dalgarno'):
    """
    Calculate RBS strength based on sequence.
    """
    # Shine-Dalgarno: AGGAGGT
    sd_sequence = 'AGGAGGT'
    
    # Calculate binding energy
    # This would use thermodynamic model
    return 0.5  # Placeholder
```

-----

## Gene Circuit Design

### Logic Gates in Biology

```python
# Genetic AND gate
class ANDGate:
    """
    Two-input AND gate using repressors.
    A and B must both be present to activate output.
    """
    def __init__(self):
        self.inputs = ['A', 'B']
        self.output = 'C'
    
    def design_parts(self):
        return {
            'A_promoter': 'repressible_by_A',
            'B_promoter': 'repressible_by_B',
            'C_promoter': 'requires_A_and_B'  # Activated by A and B
        }

# Genetic OR gate
class ORGate:
    """
    Two-input OR gate.
    Either A or B activates output.
    """
    def __init__(self):
        self.inputs = ['A', 'B']
        self.output = 'C'
    
    def design_parts(self):
        return {
            'C_promoter_A': 'activated_by_A',
            'C_promoter_B': 'activated_by_B'
        }

# NOT gate (repressor)
class NOTGate:
    """
    Single-input NOT gate.
    """
    def design_parts(self):
        return {
            'input_promoter': 'repressible',
            'output_promoter': 'constitutive',
            'repressor': 'protein that binds input_promoter'
        }

# Oscillator (Repressilator)
class Repressilator:
    """
    Three repressors in a ring.
    """
    def __init__(self):
        self.repressors = ['TetR', 'LacI', 'cI']
    
    def design(self):
        return {
            'promoter_1': 'repressed_by_cI',
            'promoter_2': 'repressed_by_TetR',
            'promoter_3': 'repressed_by_LacI'
        }
```

### Sensor Design

```python
# Biosensor design
class Biosensor:
    def __init__(self, target):
        self.target = target
        self.receptor = None
        self.reporter = None
    
    def design(self):
        if self.target == 'arsenic':
            return self.arsenic_sensor()
        elif self.target == 'tetracycline':
            return self.tet_sensor()
        else:
            return self.generic_sensor()
    
    def arsenic_sensor(self):
        """
        Arsenic-responsive biosensor using ArsR repressor.
        """
        return {
            'promoter': 'pArs',
            'receptor': 'ArsR',
            'reporter': 'GFP',
            'threshold': '10 ppb arsenic'
        }
    
    def tet_sensor(self):
        """
        Tetracycline-responsive sensor using TetR.
        """
        return {
            'promoter': 'pTet',
            'receptor': 'TetR',
            'reporter': 'mCherry',
            'inducer': 'aTc (anhydrotetracycline)'
        }
```

-----

## Metabolic Engineering

### Pathway Optimization

```python
# Metabolic pathway modeling
class MetabolicPathway:
    def __init__(self, metabolites, reactions):
        self.metabolites = metabolites
        self.reactions = reactions
        self.stoichiometry = {}
    
    def build_stoichiometry_matrix(self):
        """Build stoichiometry matrix for metabolic model."""
        n_metabolites = len(self.metabolites)
        n_reactions = len(self.reactions)
        
        S = np.zeros((n_metabolites, n_reactions))
        
        for j, rxn in enumerate(self.reactions):
            for metabolite, coeff in rxn['stoich'].items():
                i = self.metabolites.index(metabolite)
                S[i, j] = coeff
        
        return S

# Flux Balance Analysis
def flux_balance_analysis(stoichiometry, objective_reaction, bounds=None):
    """
    FBA optimization problem.
    """
    from scipy.optimize import linprog
    
    # Objective: maximize flux through objective reaction
    c = np.zeros(len(objective_reaction))
    c[objective_reaction] = -1  # Negative for minimization
    
    # Bounds on fluxes
    if bounds is None:
        bounds = [(-1000, 1000) for _ in range(stoichiometry.shape[1])]
    
    # Solve
    result = linprog(c, A_eq=stoichiometry, b_eq=np.zeros(stoichiometry.shape[0]),
                    bounds=bounds)
    
    return result.x
```

### Strain Engineering Strategies

| Strategy | Description | Application |
|----------|-------------|-------------|
| **Knockout** | Remove competing pathways | Increase product yield |
| **Knock-in** | Add new pathways | Produce novel compounds |
| **Overexpression** | Increase gene expression | Boost pathway flux |
| **Promoter swapping** | Tune expression levels | Balance pathway |
| **Codon optimization** | Improve translation | Increase protein yield |
| **Compartmentalization** | Separate pathways | Reduce toxicity |

-----

## CRISPR Systems

### CRISPR-Cas9 Design

```python
# gRNA design
def design_sgRNA(target_sequence, pam='NGG', on_target_score=True):
    """
    Design single guide RNA for CRISPR-Cas9.
    """
    gRNAs = []
    
    for i in range(len(target_sequence) - 22):
        # Find PAM sites
        potential_pam = target_sequence[i+20:i+22]
        
        if potential_pam == 'GG':  # NGG PAM
            protospacer = target_sequence[i:i+20]
            
            gRNA = {
                'protospacer': protospacer,
                'pam': target_sequence[i+20:i+23],
                'position': i,
                'strand': '+'
            }
            
            # Calculate on-target score (simplified)
            if on_target_score:
                gRNA['score'] = calculate_crispr_score(protospacer)
            
            gRNAs.append(gRNA)
    
    return gRNAs

def calculate_crispr_score(protospacer):
    """
    Simplified on-target scoring.
    Real scoring uses position weight matrices.
    """
    # GC content
    gc = (protospacer.count('G') + protospacer.count('C')) / len(protospacer)
    
    # Simple scoring
    if 0.4 < gc < 0.7:
        return 0.8
    else:
        return 0.5

# CRISPRa/CRISPRi
crispr_variants = {
    'Cas9': {
        'function': 'DNA cleavage',
        'application': 'Gene knockout'
    },
    'dCas9': {
        'function': 'DNA binding (no cleavage)',
        'application': 'CRISPRi (repression) or CRISPRa (activation)'
    },
    'Cas12a': {
        'function': 'DNA cleavage',
        'difference': 'Different PAM, staggered cut'
    },
    'Cas13': {
        'function': 'RNA cleavage',
        'application': 'RNA targeting, diagnostics'
    }
}
```

-----

## Design Tools and Resources

### Software Tools

| Tool | Purpose | URL |
|------|---------|-----|
| **SynBioHub** | Part registry | synbiohub.org |
| **Benchling** | Design platform | benchling.com |
| **SnapGene** | Sequence design | snapgene.com |
| **Tale Designer** | TALEN design | talendesign.org |
| **CHOPCHOP** | CRISPR guide design | chopchop.cbu.uib.no |
| **RBS Calculator** | RBS optimization | rbscalculator.org |
| **COPASI** | Modeling | copasi.org |
| **Cello** | Circuit design | celldesigner.org |

### Standards

| Standard | Description |
|----------|-------------|
| **SBOL** | Synthetic Biology Open Language |
| **SBOL Visual** | Visual notation standard |
| **GenBank** | Sequence format |
| **FASTA** | Sequence format |
| **SBML** | Model format |

-----

## Common Errors to Avoid

- **Ignoring context effects**: Genetic context affects part function
- **Not characterizing parts**: Always test individual parts
- **Over-engineering circuits**: Simpler is more robust
- **Neglecting host constraints**: Chassis matters
- **Forgetting burden**: Synthetic circuits compete for resources
- **Ignoring toxicity**: Some parts/products are toxic
- **Not iterating**: DBTL requires multiple cycles
- **Assuming orthogonality**: Parts may interact unexpectedly
- **Not considering escape**: Mutations can break circuits
- **Ignoring ethics**: Biosafety and biosecurity considerations
