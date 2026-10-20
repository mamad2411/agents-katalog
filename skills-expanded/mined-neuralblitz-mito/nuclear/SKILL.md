-----

## name: nuclear
description: >
  Expert nuclear physics assistant for physicists and students. Use this skill whenever the user needs:
  help with nuclear structure, radioactive decay, nuclear reactions, fusion and fission energy, or radiation
  detection. Includes both theoretical foundations and applications.
trigger: Any nuclear physics question - from structure to reactions to medical and energy applications.
license: MIT
compatibility: opencode
metadata:
  audience: physicists
  category: physics

# Nuclear Physics — Structure, Decay, and Reactions

Covers: **Nuclear Structure · Radioactive Decay · Nuclear Reactions · Fusion · Fission · Radiation Detection**

-----

## Nuclear Structure

### Nuclear Composition

Nucleus = protons + neutrons (nucleons):
- **Atomic number** Z: number of protons
- **Neutron number** N: number of neutrons
- **Mass number** A = Z + N

Isotopes: same Z, different N.
Isotones: same N, different Z.
Isobars: same A, different Z.

### Nuclear Sizes

Charge radius:
```
R = r₀ A^{1/3}, r₀ ≈ 1.2 fm
```

Matter radius slightly larger: r₀ ≈ 1.4 fm.

### Nuclear Density

Roughly constant inside nucleus:
```
ρ ≈ 0.16 nucleons/fm³
```

Uniform density → Fermi gas model.

### Nuclear Spin

Total angular momentum I = combination of:
- Orbital angular momentum l of each nucleon
- Spin s of each nucleon (½)

### Nuclear Moments

**Magnetic dipole moment**:
```
μ = g_I μ_N I
```

μ_N = eℏ/2m_p (nuclear magneton)

**Electric quadrupole moment**:
Q measures deviation from spherical.

### Nuclear Shell Model

Nucleons in shells (like electrons):
- Magic numbers: 2, 8, 20, 28, 50, 82, 126
- Extra stability at magic numbers

Spin-orbit interaction causes shell splitting.

### Magic Numbers and Shell Closures

| Magic | Protons | Neutrons |
|-------|---------|-----------|
| 2 | He | n |
| 8 | O | O |
| 20 | Ca | Ca |
| 28 | Ni | Ni |
| 50 | Sn | Sn |
| 82 | Pb | Pb |
| 126 | - | - |

### Collective Model

Deformed nuclei:
- Vibrational states
- Rotational bands
- Quadrupole moments

### Liquid Drop Model

Semi-empirical mass formula:
```
B(A,Z) = a_V A - a_S A^{2/3} - a_C Z²/A^{1/3} - a_A (A-2Z)²/A + δ(A,Z)
```

| Term | Description | Typical Value |
|------|-------------|----------------|
| Volume | a_V A | 15.8 MeV |
| Surface | a_S A^{2/3} | 18.3 MeV |
| Coulomb | a_C Z²/A^{1/3} | 0.714 MeV |
| Asymmetry | a_A (A-2Z)²/A | 23.2 MeV |
| Pairing | δ | ±12 MeV |

### Mass Excess and Binding Energy

Mass excess: ΔM = [M - A u] c²
Binding energy: B = Z m_p + N m_n - M

### Nuclear Forces

Short-range (~1 fm):
- Strong interaction
- Spin-dependent
- Charge independent
- Spin-orbit term

NN potential: Reid, Argonne, Nijmegen.

### Deuteron Properties

- Bound state: B = 2.22 MeV
- Quadrupole moment
- Spin triplet (S=1)

### Nucleon-Nucleon Scattering

Phase shift analysis:
- Singlet, triplet channels
- Partial wave expansion

-----

## Radioactive Decay

### Decay Modes

| Mode | Description | Particles |
|------|-------------|----------|
| α | He nucleus emitted | ⁴He |
| β⁻ | neutron → proton + e⁻ + ν̅_e | e⁻ |
| β⁺ | proton → neutron + e⁺ + ν_e | e⁺ |
| EC | e⁻ capture | ν_e |
| γ | Photon emission | γ |
| n | neutron emission | n |
| Fission | Split | Fragments |

### Alpha Decay

Tunneling through Coulomb barrier:
```
T ∝ exp(-2G), G = (2m|Q|R/ℏ²)^{1/2}
```

Geiger-Nuttall law:
```
log T = aZ/√A + b
```

### Beta Decay

Fermi's Golden Rule:
```
λ = (2π/ℏ) |M|² ρ(E)
```

Allowed transitions:
- Fermi: Δπ = no, ΔS = 0
- Gamow-Teller: Δπ = no, ΔS = 1

Forbidden transitions: ΔL > 0, suppressed.

### Neglect of Parity

Weak interaction violates parity:
- Only left-handed neutrinos
- Maximum parity violation

### Electron Capture

p + e⁻ → n + ν_e:
- Competes with β⁺
- Q must be > 0.511 MeV

### Gamma Decay

Electromagnetic transitions:
- E1: Δπ = yes, ΔL = 1
- E2: Δπ = no, ΔL = 2
- M1: Δπ = no, ΔL = 0,1

Weisskopf estimates for transition rates.

### Internal Conversion

Energy → e⁻ instead of γ:
- Competes with γ
- Higher for low-energy transitions

### Decay Chains

Long chains of decays:
- ²³⁸U → ... → ²⁰⁶Pb
- ²³⁵U → ... → ²⁰⁷Pb
- ²³²Th → ... → ²⁰⁸Pb
- ⁴⁰K → ⁴⁰Ar, ⁴⁰Ca

### Decay Constants

Activity:
```
A = λN = A₀ e^{-λt}
```

Half-life: t_{1/2} = ln 2 / λ

Mean lifetime: τ = 1/λ

### Branching Ratios

Multiple decay modes possible:
- Branching ratio = fraction in each mode
- Sum = 100%

### Secular Equilibrium

For daughter with shorter half-life:
N_2(t) = λ_1 N_1 / (λ_2 - λ_1) (e^{-λ_1 t} - e^{-λ_2 t})

### Transient Equilibrium

When parent half-life comparable.

-----

## Nuclear Reactions

### Q-Value

Energy released:
```
Q = (m_initial - m_final) c²
```

Positive: exothermic
Negative: endothermic

### Threshold Energy

For endothermic reactions:
```
E_th = -Q (m_final/m_projectile)
```

For charged particles, must overcome Coulomb barrier.

### Reaction Types

| Type | Example |
|------|---------|
| Elastic | a + A → a + A |
| Inelastic | a + A → a* + A |
| Capture | a + A → B + γ |
| Transfer | a + A → b + B |
| Spallation | p + A → many |
| Fusion | light → heavier |
| Fission | heavy → lighter |

### Cross Section

```
σ = (rate)/(flux × target nuclei)
```

Units: barns (10⁻²⁴ cm²)

### Compound Nucleus

High-energy intermediate:
- Equilibrium reached
- Statistical decay

### Direct Reactions

Peripheral collisions:
- Stripping, pickup
- Few nucleons transferred

### Optical Model

Complex potential:
```
U(r) = V(r) + iW(r)
```

Describes elastic scattering.

### Compound Elastic

Through compound nucleus, interferes with direct.

### Resonance Scattering

 Breit-Wigner formula:
```
σ(E) = σ₀ (E_R/E) [(E_R/2)² + Γ²/4] / [(E-E_R)² + Γ²/4]
```

### Fusion Reactions

D + T → α + n (14.1 MeV)
D + D → T + p (4.0 MeV)
D + D → ³He + n (3.3 MeV)
p + ¹¹B → 3α (8.7 MeV)

### Fission

Nuclei split:
- Heavy (A > 230) typically
- Energy ~200 MeV

Neutrons released → chain reaction.

### Fission Products

Most at probable A ~ 95 and 140.
Neutron-rich → β decay chains.

### Fission Barriers

Double-humped for deformed:
- Outer barrier
- Inner barrier
- Isomeric states

-----

## Nuclear Models

### Shell Model

Independent particles in potential:
- Harmonic oscillator
- Woods-Saxon potential
- Spin-orbit term

### Configuration Mixing

Mix of Slater determinants.
Shell model wavefunctions.

### Cluster Model

Preformed clusters:
- α-clustering in ⁸Be, ¹²C
- α + ¹²C in ¹⁶O

### Mean Field

Hartree-Fock approach:
- Self-consistent potential
- Single-particle states

### RPA (Random Phase Approximation)

Excited states:
- Correlated particle-hole
- Collective modes

### Interacting Boson Model

IBM:
- s and d bosons
- SU(3), O(6) limits

### Ab Initio Methods

Start from NN interaction:
- No-core shell model
- Green's function Monte Carlo
- Coupled cluster

### Density Functional Theory

EDF approaches:
- Skyrme, Gogny forces
- Global fits to data

-----

## Radiation Detection

### Detector Types

| Detector | Type | Application |
|----------|------|------------|
| Scintillator | Organic/inorganic | γ, β, α |
| Gas proportional | Gas amplification | α, β |
| Semiconductor | e-hole pairs | γ, charged |
| Cerenkov | Light from μ > c/n | μ, neutrinos |
| Calorimeter | Absorber + sensor | Energy measurement |

### Energy Resolution

```
σ/E ∝ 1/√E
```

Better with semiconductor.

### Pulse Height

Proportional to energy deposited.
Calibration needed.

### Photomultiplier Tubes

Light → photoelectron → cascade.
Gain ~10⁶-10⁸.

### Spectroscopy

- HPGe: high resolution
- NaI(Tl): high efficiency
- Si(Li): X-rays

### Particle Identification

| Method | Measures |
|--------|----------|
| dE/dx | Energy loss |
| Time of flight | Velocity |
| Cerenkov | Velocity |
| TRD | Transition radiation |
| Muon chambers | Penetration |

### Neutron Detection

Via reactions:
- ³He(n,p)³H
- B(n,α)
- Fission

### Background

Cosmic rays:
- Muons, neutrons
- Shielding needed

Internal contamination:
- Natural radionuclides
- Cosmogenic activation

### Dead Time

Paralyzable vs. non-paralyzable.
Correct for high rates.

### Coincidence Detection

Reduce background:
- Time coincidence
- Compton suppression

### Pulse Shape Discrimination

Separate particles:
- n/γ in liquid scint
- α/β in some scintillators

-----

## Applications

### Nuclear Energy

- Fission reactors
- Fusion (future)
- Radioisotope generators

### Medical

- Radiotherapy (γ, e⁻)
- Imaging (PET, SPECT)
- Radioisotope production

### Dating

- ¹⁴C dating (t₁/2 = 5730 y)
- K-Ar (t₁/2 = 1.25 Gy)
- U-Pb

### Tracers

- Metabolic studies
- Industrial tracers
- Environmental

### Astrophysics

- Nucleosynthesis (r, s, p processes)
- Solar neutrinos
- Cosmic rays

### Materials

- Ion implantation
- Neutron activation analysis
- Radiation damage studies

### Security

- Portal monitors
- SNM detection
- Arms control verification

-----

## Reactor Physics

### Neutron Economy

- Production: fission
- Loss: absorption + leakage
- Breeding possible with fast reactors

### Criticality

k_eff = 1:
- Prompt critical: exponential growth
- Delayed neutrons needed for control

### Moderation

Slow neutrons:
- Hydrogen, deuterium
- Graphite
- Slowing down power

### Cross Sections

- Capture: σ_γ
- Fission: σ_f
- Scattering: σ_s

Resonances important.

### Reactor Types

| Type | Moderator | Fuel |
|------|-----------|------|
| PWR | H₂O | UO₂ (enriched) |
| BWR | H₂O | UO₂ |
| CANDU | D₂O | UO₂ (natural) |
| graphite | C | U (natural) |
| Fast | none | Pu, MOX |

### Fuel Cycle

- Mining, enrichment
- Burnup in reactor
- Spent fuel
- Reprocessing
- Waste disposal

### Criticality Safety

- Keep systems subcritical
- Double contingency
- Geometry control

-----

## Common Errors to Avoid

- Confusing mass number with atomic mass
- Using wrong units (keV vs MeV)
- Forgetting binding energy in Q-value
- Confusing decay constant with half-life
- Misapplying decay chain equations
- Confusing cross section with probability
- Forgetting Coulomb barrier in fusion
- Using classical instead of quantum tunneling
- Confusing neutrons and protons in strong force
- Ignoring parity violation in weak decays

-----

## Key References

- **Introductory Nuclear Physics** by Krane — Standard text
- **Nuclear Physics** by Wong — Theory
- **Nuclear Physics: Principles and Applications** — Modern
- **Radiation Detection and Measurement** — Knoll — Detection

