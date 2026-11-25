---
name: optics
description: "Geometric and wave optics, interference, diffraction, polarization, lasers, fiber optics, and optical instruments"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/optics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Optics

## Scope
Optics describes the behavior of light and its interaction with matter. This skill covers geometric optics, wave optics, and modern photonics including lasers and fiber optics.

## Geometric Optics

### Reflection & Refraction
- **Law of reflection**: θᵢ = θᵣ
- **Snell's Law**: n₁ sin θ₁ = n₂ sin θ₂
- **Critical angle**: θ_c = arcsin(n₂/n₁) for n₁ > n₂ (total internal reflection)
- **Brewster's angle**: θ_B = arctan(n₂/n₁) (reflected light fully polarized)

### Thin Lens / Mirror Equation
1/f = 1/dₒ + 1/dᵢ
- **Magnification**: m = -dᵢ/dₒ
- **Lensmaker's equation**: 1/f = (n-1)[1/R₁ - 1/R₂]
- Sign convention: Real images have positive dᵢ (converging), virtual have negative

### Optical Instruments
- **Microscope**: M = (L/fₒ)(25cm/fₑ) where L = tube length
- **Telescope**: M = fₒ/fₑ (angular magnification)
- **Camera**: f-number = f/D, depth of field ∝ f²/(ND)

## Wave Optics

### Interference
- **Young's double slit**: d sin θ = mλ (bright), d sin θ = (m+½)λ (dark)
- **Thin film**: 2nt cos θ = (m+½)λ (constructive, with phase change on reflection)
- **Michelson interferometer**: ΔN = 2Δd/λ (fringe count)

### Diffraction
- **Single slit**: a sin θ = mλ (dark fringes, m ≠ 0)
- **Circular aperture (Airy)**: θ = 1.22λ/D (Rayleigh criterion)
- **Diffraction grating**: d sin θ = mλ, resolving power R = mN

### Polarization
- **Malus's Law**: I = I₀ cos²θ
- **Quarter-wave plate**: Converts linear to circular polarization
- **Fresnel equations**: Reflection/transmission amplitudes at interfaces

## Lasers
- **Population inversion**: N₂ > N₁ (required for stimulated emission to dominate)
- **Gain medium**: Determines wavelength (HeNe: 632.8nm, Nd:YAG: 1064nm, CO₂: 10.6μm)
- **Cavity modes**: Δν = c/(2L), linewidth determined by gain bandwidth and cavity finesse
- **Types**: Gas, solid-state, semiconductor (diode), fiber, excimer, free-electron

## Fiber Optics
- **Numerical aperture**: NA = √(n₁² - n₂²) = n₀ sin θₐ
- **Attenuation**: α (dB/km), minimum at 1550nm for silica (~0.2 dB/km)
- **Dispersion**: Material + waveguide; compensated with DCF or chirped FBG
- **Single-mode condition**: V = (2πa/λ)NA < 2.405

## Computational Tools
- **Zemax/OpticStudio**: Optical system design and ray tracing
- **COMSOL Wave Optics**: FEM for diffractive and guided-wave optics
- **Lumerical**: FDTD for nanophotonics
- **Python**: `poppy` (physical optics), `rayopt` (ray tracing)

## Standards & References
- Hecht — *Optics* (5th ed.)
- Saleh & Teich — *Fundamentals of Photonics*
- Born & Wolf — *Principles of Optics*
