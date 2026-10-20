-----

## name: high-energy-physics
description: >
  Expert high-energy physics assistant for particle physicists and students. Use this skill whenever the user needs:
  help with the Standard Model, particle accelerators, detector physics, collision analysis, or fundamental
  interactions. Includes both theoretical foundations and experimental techniques.
trigger: Any particle physics question - from theoretical calculations to experimental data analysis to accelerator design.
license: MIT
compatibility: opencode
metadata:
  audience: physicists
  category: physics

# High-Energy Physics — Particles and Interactions

Covers: **Standard Model · Fundamental Forces · Particle Detectors · Accelerator Physics · Cross Sections · Data Analysis**

-----

## The Standard Model

### Fundamental Fermions

**Quarks** (6 flavors, 3 generations):

| Generation | Flavor | Charge | Mass |
|------------|--------|--------|------|
| 1 | up (u) | +2/3 | ~2.2 MeV |
| 1 | down (d) | -1/3 | ~4.7 MeV |
| 2 | charm (c) | +2/3 | ~1.28 GeV |
| 2 | strange (s) | -1/3 | ~95 MeV |
| 3 | top (t) | +2/3 | ~173 GeV |
| 3 | bottom (b) | -1/3 | ~4.18 GeV |

**Leptons** (6 flavors):

| Generation | Flavor | Charge | Mass |
|------------|--------|--------|------|
| 1 | electron (e) | -1 | 0.511 MeV |
| 1 | neutrino (ν_e) | 0 | < 2 eV |
| 2 | muon (μ) | -1 | 105.66 MeV |
| 2 | neutrino (ν_μ) | 0 | < 0.19 MeV |
| 3 | tau (τ) | -1 | 1.777 GeV |
| 3 | neutrino (ν_τ) | 0 | < 18.2 MeV |

### Gauge Bosons (Force Carriers)

| Force | Boson | Mass | Charge | Spin |
|-------|-------|------|--------|------|
| Electromagnetic | γ (photon) | 0 | 0 | 1 |
| Weak | W± | 80.38 GeV | ±1 | 1 |
| Weak | Z⁰ | 91.19 GeV | 0 | 1 |
| Strong | gluon (g) | 0 | 0 | 1 |

### The Higgs Boson

- Mass: ~125 GeV
- Discovered 2012 at LHC
- Spin: 0 (scalar)
- Responsible for electroweak symmetry breaking

### Fundamental Interactions

**Electromagnetic**: QED, U(1)_EM gauge
**Weak**: SU(2)_L, charged + neutral currents
**Strong**: QCD, SU(3)_C gauge

### Quantum Chromodynamics (QCD)

- Color charge: 3 colors (r, g, b)
- 8 gluons (color octet)
- Asymptotic freedom: α_s decreases at high energy
- Confinement: quarks cannot be isolated at low energy
- Running coupling:
```
α_s(Q²) = α_s(μ²) / [1 + (α_s(μ²)/12π) β₀ ln(Q²/μ²)]
```

### Electroweak Theory

Glashow-Weinberg-Salam model:
- SU(2)_L × U(1)_Y → U(1)_EM after symmetry breaking
- W mixing gives physical W±, Z⁰, γ
- Weinberg angle: sin²θ_W ≈ 0.231

### Conservation Laws

| Quantity | Conserved in |
|----------|--------------|
| Energy, momentum | All |
| Angular momentum | All |
| Electric charge | All |
| Baryon number | Strong, EM (violated in EW?) |
| Lepton number | Strong, EM (violated in EW?) |
| Flavor (u,d,s,c,b,t) | Strong, EM |
| Flavor (e,μ,τ) | Weak (neutrino mixing) |

-----

## Relativistic Kinematics

### Four-Vectors

```
p^μ = (E/c, p)
p² = (E/c)² - p² = m²c²
```

Metric: (+,-,-,-) or (-,+,+,+) — be consistent.

### Lorentz Transformations

For boost along x with velocity β = v/c, γ = 1/√(1-β²):
```
E' = γ(E - β p_x)
p'_x = p_x - βE/c
p'_⊥ = p_⊥
```

### Mandelstam Variables

For 2→2 scattering: a + b → c + d
```
s = (p_a + p_b)² = m_a² + m_b² + 2(E_a E_b - p_a·p_b)
t = (p_a - p_c)² = m_a² + m_c² - 2(E_a E_c - p_a·p_c)
u = (p_a - p_d)² = m_a² + m_d² - 2(E_a E_d - p_a·p_d)
```

s + t + u = m_a² + m_b² + m_c² + m_d²

### Center-of-Mass Frame

Total momentum = 0.
Total energy: √s = E_cm

### Lorentz-Invariant Phase Space

```
dΦ_n = (2π)⁴ δ⁴(P_in - P_out) ∏ d³p_i/(2E_i)(2π)³
```

### Cross Section

```
σ = (1/Flux) |M|² × (phase space)
```

### Luminosity

```
L = (N_b N_t f)/(A)
```

Integrated luminosity: ∫L dt [fb⁻¹]

### Parton Distribution Functions (PDFs)

Momentum distribution of partons inside hadron:
```
f_i(x, Q²) = probability of finding parton i with momentum fraction x at scale Q²
```

Need for LHC calculations.

-----

## Feynman Diagrams

### Rules for QED

1. External lines: spinors (fermions), polarization vectors (photons)
2. Propagators: i/(p - m) for fermions, -ig_{μν}/q² for photons
3. Vertices: -ieγ^μ
4. Integrate over internal momenta, sum over spins

### Leading Order (LO), NLO, NNLO

- LO: Lowest order in α
- NLO: One additional loop or emission
- Required for precision predictions

### Decay Widths

For 1→2 decay: Γ = (1/8πm) |M|² × p_f

Total width = sum of partial widths.

Branching ratio = Γ_i/Γ_total

### Matrix Elements

Spin-averaged squared amplitudes:
```
|M|²_avg = (1/(2s+1)(2s'+1)) Σ_{spins} |M|²
```

### Cross Section Calculation

```
dσ/dΩ = (1/64π²s) |M|²
```

For non-relativistic: use standard formulas.

-----

## Particle Detectors

### Detector Systems

| Layer | Purpose | Technology |
|-------|---------|------------|
| Vertex detector | Track reconstruction | Silicon pixels/strips |
| Tracking system | Momentum measurement | Drift chambers, TPC |
| Particle ID | Identify particles | dE/dx, Cherenkov, TOF |
| Electromagnetic calorimeter | Photons, electrons | Pb/Scint, LAr |
| Hadronic calorimeter | Hadrons | Fe/Scint, Cu/Scint |
| Muon system | Muon identification | Muon chambers |
| Solenoid | Magnetic field | Superconducting coil |

### Tracking Detectors

**Silicon strip**: Position resolution ~10 μm
**Drift chamber**: Gas-based, larger volume
**Time projection chamber (TPC)**: 3D tracking

### Calorimetry

**Electromagnetic**: Measure EM showers from e/γ
**Hadronic**: Measure hadronic showers

Energy resolution:
```
σ/E ∝ A/√E
```

### Particle Identification

| Method | Measures | Particles |
|--------|----------|----------|
| dE/dx | Energy loss | All charged |
| Cherenkov | Velocity | Different masses |
| Transition radiation | γ factor | e/π separation |
| Muon chambers | Penetration | Muons only |

### Trigger Systems

Hardware + software selection of interesting events.
L1: fast hardware (μs)
L2: fast software (ms)
L3: full event reconstruction (s)

### Data Acquisition

- Readout electronics
- Event building
- Storage and processing

-----

## Accelerator Physics

### Synchrotron

Magnetic guide fields increase with energy to keep particles on circular path.

Radius: R = p/(0.3B)
Momentum: p[GeV/c] = 0.3 B[T] R[m]

### Linear Accelerators (Linacs)

Cavities accelerate particles in straight line.
Coulomb/excited state ~few hundred MeV/m.

### LHC Design

- Circumference: 27 km
- Proton energy: 7 TeV (design), 6.5 TeV (run)
- Bending field: 8.3 T (dipoles)
- Peak luminosity: 10³⁴ cm⁻²s⁻¹

### Beam Parameters

- **Bunch spacing**: 25 ns ( LHC)
- **Bunch population**: ~10¹¹ protons/bunch
- **Emittance**: transverse beam size
- **Beta function**: focusing strength

### Lattice Design

Alternating gradient (FOODO) focusing:
- Quadrupoles for focusing
- Dipoles for bending
- Sextupoles for chromaticity correction

### RF Acceleration

Cavities at bunch frequency (400 MHz LHC):
- Accelerating voltage ~16 MV/beam
- Synchrotron radiation loses energy

### Luminosity

```
L = N_b² n f σ/(4πσ_y)
```

_x σDepends on beam current, crossing angle.

### Beam Cooling

- **Ionization cooling**: For muon colliders
- **Stochastic cooling**: Random beam noise
- **Electron cooling**: Electron beam

### Future Colliders

- FCC-hh: 100 TeV pp (100 km)
- CEPC: Higgs factory
- ILC: Linear e⁺e⁻

-----

## QCD and Strong Interactions

### Running Coupling

```
α_s(μ²) = 12π/[(33-2n_f)ln(μ²/Λ_QCD²)]
```

n_f = number of active flavors
Λ_QCD ~ 200 MeV

### Parton Model

Hadron = cloud of nearly free partons at high Q².
Structure function: F₂(x, Q²) = x Σ e²_q f_q(x, Q²)

### DGLAP Evolution

Parton densities evolve with Q² via DGLAP equations:
```
dq_i/dlnμ² = P ⊗ q
```

### Jet Formation

High-energy quarks/gluons hadronize into jets.
Jet algorithms: anti-k_T, Cambridge-Aachen, k_T

### Jet Cross Section

Differential: dσ/dp_T
Total: σ_total

### Underlying Event

Initial state radiation, beam remnants, multiple parton interactions.

### Minimum Bias

Non-diffractive + diffractive collisions.
Cross section ~ 70 mb at LHC.

### Heavy Ion Physics

Quark-gluon plasma (QGP) at high temperature/density.
Flow phenomena, jet quenching.

-----

## Weak Interactions

### Charged Current

W mediates flavor-changing processes:
- β decay: d → u e⁻ ν̅_e
- μ decay: μ⁻ → e⁻ ν̅_e ν_μ
- Quark mixing: CKM matrix

### Neutral Current

Z⁰ mediates flavor-conserving weak interactions.
All fermions couple (including neutrinos).

### CKM Matrix

```
|V| = |V_ud V_us V_ub; V_cd V_cs V_cb; V_td V_ts V_tb|
```

Unitarity: |V|² = 1
Angles: θ_12, θ_23, θ_13, δ

### PMNS Matrix

Neutrino mixing:
```
|ν_e; ν_μ; ν_τ| = U_PMNS |ν_1; ν_2; ν_3|
```

### Parity Violation

Weak interactions maximally violate parity.
Only left-handed particles (right-handed antiparticles) interact at tree level.

### W and Z Widths

W: Γ_W ~ 2.1 GeV
Z: Γ_Z ~ 2.5 GeV
Decays to all kinematically allowed fermions.

### Electroweak Precision Tests

- Z pole observables
- W mass
- sin²θ_W
- Higgs couplings

### Higgs Boson

Production at LHC:
- Gluon fusion (gg → H)
- Vector boson fusion (qq → qqH)
- Associated production (WH, ZH, tH)

Decay modes: γγ, ZZ*, WW*, ττ, bb, etc.

-----

## Data Analysis

### Event Selection

- Triggers to reduce rate
- Object identification (e, μ, τ, γ, jets, b-jets)
- Kinematic cuts
- Isolation requirements

### Background Estimation

- Data-driven methods
- Monte Carlo simulation
- Sidebands

### Statistical Methods

- Maximum likelihood fit
- χ² minimization
- Bayesian inference

### Systematic Uncertainties

- Detector effects (calibration, resolution)
- Theory (PDFs, scales)
- Luminosity

### Significance

Signal significance: Z = √(2 ln(L_s/L_b))
Discovery: Z > 5σ (p < 2.9×10⁻⁷)

### Limits

Upper limits on cross sections.
CLs method for exclusion.

### Unblinding

Procedures to avoid bias in analysis.

-----

## Beyond Standard Model

### Dark Matter

Evidence: galactic rotation curves, CMB, large-scale structure.
WIMPs, axions, sterile neutrinos.

### Neutrino Mass

Oscillation experiments show non-zero mass.
Seesaw mechanism, sterile neutrinos.

### Matter-Antimatter Asymmetry

Baryon asymmetry of universe.
Sakharov conditions: B violation, C and CP violation, out of equilibrium.

### Hierarchy Problem

Why is Higgs mass so low compared to Planck scale?
Supersymmetry, composite Higgs, extra dimensions.

### Grand Unified Theories

Unify strong, weak, EM at ~10¹⁶ GeV.
SU(5), SO(10), E_8 × E_8.

### String Theory

Fundamental objects: 1D strings (instead of 0D particles).
Extra dimensions (10, 11).

-----

## Common Errors to Avoid

- Using non-covariant expressions
- Forgetting factors of 2π, i, signs in matrix elements
- Confusing Mandelstam variables definitions
- Incorrectly applying running coupling
- Mixing natural units conventions
- Forgetting to include all diagrams at given order
- Incorrectly summing/averaging spins
- Not checking phase space limits
- Confusing PDFs with structure functions
- Incorrect interpretation of limits vs. evidence

-----

## Key References

- **Particle Physics** by Martin & Wheeler — Introduction
- **Introduction to Elementary Particles** by Griffiths — More accessible
- **The Standard Model and Beyond** by Drees — Comprehensive
- **Accelerator Physics** by Lee — Accelerator design

