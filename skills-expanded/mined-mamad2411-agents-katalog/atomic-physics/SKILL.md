-----

## name: atomic-physics
description: >
  Expert atomic physics assistant for researchers and students. Use this skill whenever the user needs:
  help with atomic structure calculations, spectroscopic analysis, quantum optics problems,
  understanding fine and hyperfine structure, working with cold atom systems, or any
  rigorous treatment of atomic physics phenomena. Covers quantum mechanical descriptions
  of atoms, transition probabilities, selection rules, and experimental techniques.
trigger: Any atomic physics, spectroscopy, quantum optics, or laser physics question where
  quantitative analysis and theoretical rigor are expected.
license: MIT
compatibility: opencode
metadata:
  audience: researchers
  category: physics

# Atomic Physics — Theoretical and Experimental Foundations

Covers: **Quantum Mechanical Atomic Structure · Spectroscopy · Selection Rules · Fine Structure · Hyperfine Structure · Cold Atoms · Laser-Atom Interactions**

-----

## Quantum Mechanical Atomic Structure

### The Schrödinger Equation for Atoms

The foundation of atomic physics is the time-independent Schrödinger equation:

```
ĤΨ(r₁, r₂, ..., rₙ) = EΨ(r₁, r₂, ..., rₙ)
```

For hydrogen-like atoms (single electron), the Hamiltonian includes:

```
Ĥ = -ℏ²/2m ∇² - Ze²/(4πε₀r)
```

This separates in spherical coordinates, yielding solutions characterized by:

- **Principal quantum number**: n = 1, 2, 3, ... (determines energy level)
- **Angular momentum quantum number**: l = 0, 1, 2, ..., n-1 (s, p, d, f, ...)
- **Magnetic quantum number**: m_l = -l, -l+1, ..., +l
- **Spin quantum number**: m_s = ±½

### Electron Configurations and Term Symbols

Atomic term symbols follow the convention:

```
²S+1L_J
```

Where:
- S = total spin quantum number (sum of individual electron spins)
- L = total orbital angular momentum (S, P, D, F, ...)
- J = total angular momentum (L ± S)

**Example**: Ground state of neutral sodium (Na I):
- Electron configuration: [Ne] 3s¹
- Term symbol: ²S₁/₂

**Example**: First excited state:
- Configuration: [Ne] 3p¹
- Term symbol: ²P₁/₂ and ²P₃/₂ (spin-orbit splitting)

### Hydrogen-Like Energy Levels

The exact solution for hydrogen-like atoms gives energy eigenvalues:

```
E_n = -μZ²e⁴/(2(4πε₀)²ℏ²) · 1/n² = -13.6 eV · Z²/n²
```

| n | Energy (eV) | Shell |
|---|-------------|-------|
| 1 | -13.6Z²    | K     |
| 2 | -3.4Z²     | L     |
| 3 | -1.51Z²    | M     |
| 4 | -0.85Z²    | N     |

### Multi-Electron Atoms

For multi-electron atoms, the central field approximation reduces the problem to an effective potential:

```
V_eff(r) = -Ze²/(4πε₀r) + V_screen(r)
```

The **Hartree-Fock method** provides self-consistent field solutions by iteratively solving for the optimal Slater determinant that minimizes total energy.

### Spin-Orbit Coupling

The fine structure splitting arises from the interaction between electron spin and orbital magnetic moments:

```
H_SO = ξ(r) L · S
```

This splits energy levels according to the total angular momentum **J**, with splitting:

```
ΔE_SO = (ξ/2)[j(j+1) - l(l+1) - s(s+1)]
```

### Hyperfine Structure

The interaction between nuclear magnetic moment (I) and electron magnetic moments (J) causes hyperfine splitting:

```
H_hfs = A I · J
```

This produces the **Fermi contact interaction** for s-electrons and **dipole-dipole** interactions for other orbitals. The hyperfine splitting is typically in the MHz-GHz range (radio frequency).

### Landé g-Factor

The Landé g-factor determines the magnetic moment of an atom in a weak magnetic field:

```
g_J = 1 + [j(j+1) + s(s+1) - l(l+1)] / [2j(j+1)]
```

This is essential for analyzing Zeeman splitting in magnetic fields.

-----

## Atomic Spectroscopy

### Electromagnetic Transitions

Transitions between atomic states occur via absorption or emission of photons. The transition rate (Einstein A coefficient) is:

```
A_ij = (4ω³ℏ)/(3ℏc³) |⟨i|d|j⟩|²
```

Where d is the electric dipole moment operator.

### Selection Rules

Electric dipole (E1) transitions obey:

- Δl = ±1 (parity change required)
- Δj = 0, ±1 (but j=0 → j'=0 forbidden)
- Δm_j = 0, ±1 (with polarization dependence)

**Allowed transitions**: Satisfy all selection rules
**Forbidden transitions**: Violate one or more rules but may occur weakly (E2, M1, etc.)

### Transition Wavelengths and Series

Spectral lines are grouped into series (Lyman, Balmer, Paschen, etc.):

| Series | Lower Level | Upper Level | Wavelength Region |
|--------|-------------|-------------|-------------------|
| Lyman  | n = 1       | n ≥ 2       | UV (< 121 nm)     |
| Balmer | n = 2       | n ≥ 3       | Visible/UV        |
| Paschen| n = 3       | n ≥ 4       | Infrared           |
| Brackett | n = 4    | n ≥ 5       | Far infrared      |

### Oscillator Strength and Line Strength

The **oscillator strength** f_ij measures transition probability:

```
f_ij = (2mω_ij)/(3ℏe²) |⟨i|d|j⟩|²
```

Sum rules: Σ_j f_ij = 1 (for complete set of final states)

### Spectral Line Shapes

Natural linewidth (Lorentzian):
```
Γ = Σ A_i (uncertainty principle: ΔE·Δt ~ ℏ)
```

Doppler broadening (Gaussian):
```
Δν_D = (2ν₀/c) √(2kT ln2 / M)
```

Pressure/collisional broadening:
```
Δν_collision = 1/(2πτ_collision)
```

### Frank-Condon Principle

For diatomic molecules, the **Franck-Condon factor** determines vibronic transition probabilities:

```
FC = |⟨v_i|v_f⟩|²
```

This arises from the overlap of vibrational wavefunctions and explains band structure in molecular spectroscopy.

-----

## Quantum Optics and Laser-Atom Interactions

### Rabi Oscillation

When an atom interacts with resonant laser light, the population oscillates between ground and excited states:

```
P_e(t) = (Ω_R t)² sinc²(Ω_R t/2)
```

Where **Rabi frequency** Ω_R = d·E/ℏ depends on the transition dipole moment and electric field amplitude.

### AC Stark Shift (Light Shift)

Off-resonant laser light shifts atomic energy levels:

```
ΔE = (Ω_R²)/(4δ)
```

Where δ = ω_laser - ω_0 is the detuning. This is the basis for optical dipole traps.

### Doppler Cooling

Atoms moving toward a laser absorb photons Doppler-shifted into resonance, then spontaneously emit. The cooling limit:

```
T_Doppler = ℏΓ/(2k_B)
```

For the D2 line of sodium: T_Doppler ≈ 240 μK

### Optical Molasses

Three orthogonal laser beams (two counter-propagating per dimension) create viscous damping:

```
F_drag = -αv
```

The damping coefficient α depends on detuning and intensity.

### Magneto-Optical Trap (MOT)

Combining optical molasses with a spatially varying magnetic field (Zeeman slower principle) provides both cooling and trapping:

```
F_total ∝ -(αv + βr)
```

### Evaporative Cooling

Remove the hottest atoms from a trap, allowing thermalization to cool the remaining population:

```
T_final = T_initial · (N_final/N_initial)^(κ)
```

Where κ depends on the trap geometry and atomic interactions.

-----

## Cold Atom Systems

### Bose-Einstein Condensates

For bosonic atoms below critical temperature T_c:

```
N_0 = N[1 - (T/T_c)³/²]
```

The condensate exhibits macroscopic wavefunction behavior with coherent matter wave properties.

### BEC Equation of State

The Gross-Pitaevskii equation describes the condensate:

```
[-ℏ²∇²/2m + V_ext(r) + g|n(r)|²]ψ(r) = μψ(r)
```

Where g = 4πℏ²a/m is the interaction strength and a is the s-wave scattering length.

### Fermi Degenerate Gases

For fermions, Pauli exclusion prevents collapse. The Fermi temperature:

```
T_F = (ℏ²/2m)(3π²n)²/³ / k_B
```

### Optical Lattices

Periodic potentials from standing wave laser beams:

```
V(x) = V₀ cos²(kx)
```

Bloch's theorem applies, with Bloch bands and bandgaps. Atoms can be loaded into the lowest band ( Mott insulator transition) for bosonic systems when U >> J.

### Atom Interferometry

Matter wave interferometers use beam splitters (Raman pulses or optical lattices) to split and recombine atomic wavepackets:

```
Phase shift = m·g·T² (gravity)
```

Sensitivities approaching 10⁻¹¹ g/√Hz achievable.

### Precision Measurements with Cold Atts

- **Atomic clocks**: Microwave or optical transitions with fractional uncertainty < 10⁻¹⁸
- **Gravimetry**: Measure local gravity with ppb precision
- **Tests of fundamental physics**: Searches for variation of fundamental constants, dark matter signatures

-----

## Experimental Techniques

### Spectroscopy Methods

| Method | Description | Resolution |
|--------|-------------|------------|
| **Absorption** | Measure light attenuation | Medium |
| **Fluorescence** | Detect emitted photons | Medium |
| **Fabry-Perot** | Cavity-enhanced | High |
| **FM spectroscopy** | Frequency modulation | Very high |
| **Laser locking** | Reference to atomic transitions | Extremely high |

### Laser Systems for Atomic Physics

- **Dye lasers**: Tunable across visible spectrum
- **Diode lasers**: Compact, tunable, narrow linewidth
- **Ti:Sapphire**: Broad tunability 650-1100 nm
- **Fiber lasers**: High power, excellent stability
- **Frequency combs**: Precise frequency referencing across wide ranges

### Detection Methods

- **Fluorescence imaging**: Direct photon detection
- **Ionization detection**: State-selective ionization + mass spec
- **Absorption imaging**: Phase contrast or dark ground
- **Time-of-flight**: Measure velocity distributions

### Vacuum Requirements

| Application | Pressure | Technology |
|-------------|----------|------------|
| Room temperature spectroscopy | 10⁻⁶ Torr | Diffusion pump, ion pump |
| Cold atom traps | 10⁻¹¹ Torr | Ion pump, NEG pumps |
| BEC production | 10⁻¹² Torr | Cryopump, titanium sublimation |

### Magnetic Field Control

- **Solenoids**: Generate homogeneous fields for Zeeman splitting
- **Helmholtz coils**: Cancel external fields
- **Quadrupole coils**: Create field gradients for trapping
- **Atom chips**: Integrated wires for miniature traps

-----

## Common Errors to Avoid

- Confusing spectroscopic notation (Russell-Saunders vs. j-j coupling)
- Applying LS-coupling to heavy elements where jj-coupling dominates
- Ignoring nuclear spin effects in hyperfine structure
- Using wrong detuning sign in laser cooling calculations
- Confusing Rabi frequency with general transition rate
- Neglecting Doppler broadening in high-precision spectroscopy
- Forgetting parity selection rules for forbidden transitions
- Using classical instead of quantum expressions for radiation

-----

## Key References

- **Atomic Physics** by C.J. Foot — Excellent introduction to cold atom physics
- **Physics of Atoms and Molecules** by Bransden and Joachain — Comprehensive theoretical treatment
- **Laser Cooling and Trapping** by Metcalf and van der Straten — Cold atom techniques
- **Quantum Optics** by Walls and Milburn — Quantum light-atom interactions

