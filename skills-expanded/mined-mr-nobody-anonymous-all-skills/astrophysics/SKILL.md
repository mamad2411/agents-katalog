---
name: astrophysics
description: "Stellar evolution, galaxies, cosmology observational techniques, dark matter, dark energy, and computational astrophysics"
category: physics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/physics/astrophysics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Astrophysics

## Scope
Astrophysics applies physics to understand celestial objects, from stars and planets to galaxies and the large-scale structure of the universe.

## Stellar Physics

### Stellar Structure Equations
1. **Hydrostatic equilibrium**: dP/dr = -Gm(r)ρ/r²
2. **Mass continuity**: dm/dr = 4πr²ρ
3. **Energy generation**: dL/dr = 4πr²ρε (nuclear reaction rate ε)
4. **Energy transport**: dT/dr depends on radiative vs. convective transport

### Stellar Classification
| Type | Temperature | Color | Example |
|------|------------|-------|---------|
| O | > 30,000 K | Blue | 10 Lacertae |
| B | 10,000-30,000 K | Blue-white | Rigel |
| A | 7,500-10,000 K | White | Sirius |
| F | 6,000-7,500 K | Yellow-white | Procyon |
| G | 5,200-6,000 K | Yellow | Sun |
| K | 3,700-5,200 K | Orange | Arcturus |
| M | < 3,700 K | Red | Proxima Centauri |

### Stellar Evolution
- **Main sequence**: Hydrogen fusion, lifetime τ ~ M⁻²·⁵ × 10¹⁰ yr
- **Red giant**: Core contracts, envelope expands after H exhaustion
- **White dwarf**: M < 1.4 M☉ (Chandrasekhar limit), electron degeneracy support
- **Neutron star**: 1.4-3 M☉, neutron degeneracy, r ~ 10 km
- **Black hole**: M > 3 M☉, Schwarzschild radius rₛ = 2GM/c²

### Nuclear Reactions
- **pp chain**: 4¹H → ⁴He + 2e⁺ + 2νₑ + 26.7 MeV (Sun)
- **CNO cycle**: Dominates for M > 1.3 M☉, T > 1.5 × 10⁷ K
- **Triple-alpha**: 3⁴He → ¹²C (red giant core)

## Cosmology
- **Hubble's Law**: v = H₀d, H₀ ≈ 67.4 km/s/Mpc (Planck 2018)
- **Friedmann equations**: (ȧ/a)² = 8πGρ/3 - kc²/a² + Λc²/3
- **Critical density**: ρ_c = 3H²/(8πG) ≈ 9.47 × 10⁻²⁷ kg/m³
- **Composition**: ~5% baryonic, ~27% dark matter, ~68% dark energy (Λ)
- **CMB**: T = 2.725 K, anisotropies δT/T ~ 10⁻⁵
- **Age of universe**: 13.8 ± 0.02 Gyr

## Observational Techniques
- **Photometry**: Apparent magnitude m, absolute magnitude M, distance modulus m-M = 5 log₁₀(d/10pc)
- **Spectroscopy**: Radial velocity (Doppler), chemical abundances, temperature
- **Astrometry**: Parallax distance d(pc) = 1/p(arcsec)
- **Multi-messenger**: EM + gravitational waves + neutrinos

## Computational Tools
- **Astropy**: Python library for astronomy (coordinates, units, FITS, cosmology)
- **MESA**: Modules for Experiments in Stellar Astrophysics
- **Gadget/Arepo**: N-body + hydrodynamic cosmological simulations
- **ds9/SAOImageDS9**: FITS image viewer
- **HEALPix**: Pixelization of the sphere for CMB analysis

## Standards & References
- Carroll & Ostlie — *An Introduction to Modern Astrophysics*
- Ryden — *Introduction to Cosmology*
- Weinberg — *Cosmology*
- NASA/IPAC Extragalactic Database (NED)
