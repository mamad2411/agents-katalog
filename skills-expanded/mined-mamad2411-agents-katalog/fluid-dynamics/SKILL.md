-----

## name: fluid-dynamics
description: >
  Expert fluid dynamics assistant for engineers and physicists. Use this skill whenever the user needs:
  analysis of fluid flow, solving Navier-Stokes equations, calculating boundary layer behavior,
  understanding laminar and turbulent flow, analyzing aerodynamic forces, or designing systems
  involving fluid transport. Includes both theoretical foundations and practical engineering applications.
trigger: Any engineering problem involving fluid flow - from aerospace to civil engineering to biomedical applications.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: physics

# Fluid Dynamics — Theory and Engineering Applications

Covers: **Fluid Kinematics · Navier-Stokes · Laminar and Turbulent Flow · Boundary Layers · Compressible Flow · Aerodynamics**

-----

## Fundamental Equations

### Continuity Equation (Mass Conservation)

Differential form:
```
∂ρ/∂t + ∇·(ρv) = 0
```

For incompressible flow (ρ = constant):
```
∇·v = 0
```

Integral form (control volume):
```
d/dt ∫_CV ρ dV = -∫_CS ρ v·n̂ dA
```

### Momentum Equation (Navier-Stokes)

For Newtonian fluid:
```
ρ(Dv/Dt) = -∇p + μ∇²v + ρg
```

Where Dv/Dt = ∂v/∂t + (v·∇)v is the substantial (material) derivative.

In component form (x-momentum):
```
ρ(∂u/∂t + u∂u/∂x + v∂u/∂y + w∂u/∂z) = -∂p/∂x + μ(∂²u/∂x² + ∂²u/∂y² + ∂²u/∂z²) + ρg_x
```

### Energy Equation

```
ρ C_p DT/Dt = k ∇²T + Φ + Q
```

Where Φ is the viscous dissipation function:
```
Φ = μ[2(∂u/∂x)² + 2(∂v/∂y)² + 2(∂w/∂z)² + (∂v/∂x + ∂u/∂y)² + ...]
```

### Equation of State

- **Ideal gas**: p = ρRT
- **Incompressible**: ρ = constant
- **Real gas**: Use tables or compressibility factor Z

-----

## Fluid Properties

### Viscosity

| Property | Symbol | Definition | Units |
|----------|--------|------------|-------|
| Dynamic viscosity | μ | τ = μ(∂u/∂y) | Pa·s |
| Kinematic viscosity | ν = μ/ρ | Momentum diffusivity | m²/s |

**Temperature dependence**:
- Gases: μ ∝ T^0.7 (approx)
- Liquids: μ decreases with T (typically exponential)

### Compressibility

**Bulk modulus**:
```
K = -V(dp/dV)
```

**Speed of sound**:
```
c = √(dp/dρ)|_s = √(γRT) for ideal gas
```

### Surface Tension

```
σ = dγ/dT (Gibbs adsorption equation basis)
```

Capillary rise: h = 2σ cosθ/(ρgr)

-----

## Hydrostatics

### Pressure Variation

In static fluid:
```
dp/dz = -ρg
```

For incompressible (ρ constant):
```
p = p₀ + ρg(h - z)
```

For compressible (ideal gas, isothermal):
```
p = p₀ exp(-Mgz/RT)
```

For compressible (adiabatic):
```
p = p₀[1 + (γ-1)gz/(c₀²)]^{γ/(γ-1)}
```

### Buoyancy (Archimedes' Principle)

```
F_b = ρ_fluid V_displaced g
```

Stability: Center of buoyancy vs. center of gravity.

### Pressure Measurement

- **Manometer**: p = p_ref + ρgΔh
- **Bourdon gauge**: Mechanical deformation
- **Piezoelectric**: Crystal deformation

-----

## Kinematics of Flow

### Streamlines, Pathlines, and Streaklines

| Concept | Definition | Construction |
|---------|------------|--------------|
| **Streamline** | Tangent to velocity at fixed time | dy/dx = v/u |
| **Pathline** | Actual trajectory of a particle | Integrate r(t) |
| **Streakline** | All particles released from a point | Connect markers |

In steady flow: all three coincide.

### Velocity Potential

For irrotational flow (∇×v = 0):
```
v = ∇φ
```

φ satisfies Laplace's equation: ∇²φ = 0

### Stream Function

For 2D incompressible flow:
```
u = ∂ψ/∂y, v = -∂ψ/∂x
```

Constant ψ = streamlines. For 2D, ψ exists automatically if ∇·v = 0.

### Circulation

```
Γ = ∮_C v·dl = ∬_S (∇×v)·n̂ dS
```

Kelvin's theorem: Circulation constant for barotropic flow with conservative body forces.

-----

## Inviscid Flow

### Bernoulli's Equation

Along a streamline (steady, incompressible, inviscid):
```
p/ρ + v²/2 + gz = constant
```

With head loss (in real fluids):
```
p₁/ρ + v₁²/2 + gz₁ = p₂/ρ + v₂²/2 + gz₂ + h_L
```

### Euler's Equations (Differential)

```
Dv/Dt = -∇p/ρ + g
```

### Potential Flow Solutions

Superposition of elementary solutions:

| Flow | Stream Function | Velocity |
|------|-----------------|----------|
| Uniform | ψ = U_∞ y | (U_∞, 0) |
| Source | ψ = Qθ/(2π) | (Q/(2πr), 0) |
| Vortex | ψ = Γ ln r/(2π) | (0, Γ/(2πr)) |
| Doublet | ψ = -K y/r² | See formula |

### Flow Around a Cylinder

Without circulation:
- Symmetric pressure distribution
- Zero lift

With circulation (Kutta-Joukowski):
```
L = ρU_∞Γ (per unit span)
```

### Lift and Drag

**Lift coefficient**:
```
C_L = L/(½ρU²_∞ A)
```

**Drag coefficient**:
```
C_D = D/(½ρU²_∞ A)
```

-----

## Laminar Flow

### Reynolds Number

```
Re = ρVL/μ = UL/ν
```

| Re Range | Flow Type |
|----------|-----------|
| < ~2000 | Laminar (pipes) |
| ~2000-4000 | Transitional |
| > ~4000 | Turbulent (pipes) |

### Poiseuille Flow (Pipe)

For laminar flow in circular pipe:
```
u(r) = (Δp/L)(R² - r²)/(4μ)
```

Average velocity: ū = (Δp/L)(R²)/(8μ)

Pressure drop:
```
Δp = 32μLū/D² = 128μLQ/(πD⁴)
```

Friction factor (Darcy):
```
f = 64/Re (laminar)
```

### Couette Flow

Flow between parallel plates, one moving:
```
u(y) = U(y/h)
```

### Laminar Boundary Layer (Flat Plate)

Blasius solution for laminar BL on flat plate:
```
δ(x) ≈ 5.0 √(νx/U_∞)
```

Boundary layer thickness grows as √x.

Shear stress:
```
τ_w = 0.664 μ U_∞ √(U_∞/νx)
```

### Entrance Length

**Laminar**: L_e ≈ 0.05 Re D
**Turbulent**: L_e ≈ 50 D

-----

## Turbulent Flow

### Characteristics

- Random, chaotic, 3D
- Vortical structures at many scales
- Enhanced momentum/heat/mass transfer
- Statistically described

### Turbulent Viscosity

Reynolds decomposition: u = ū + u'
Boussinesq hypothesis:
```
-ρ<u'u'> = μ_t ∂ū/∂y
```

where μ_t >> μ

### Velocity Profile

**Log-law** (inner region):
```
u⁺ = (1/κ) ln y⁺ + B
```

Where:
- u⁺ = u/u_τ
- y⁺ = yu_τ/ν
- u_τ = √(τ_w/ρ)
- κ ≈ 0.41 (von Kármán constant)
- B ≈ 5.0

### Friction Factor (Moody Diagram)

**Smooth pipe (Blasius)**:
```
f = 0.316/Re^{0.25} for Re < 10⁵
```

**Rough pipe**:
```
1/√f = -2 log₁₀(ε/(3.7D) + 2.51/(Re√f))
```

### Turbulent Boundary Layer

Thickness:
```
δ ≈ 0.37 x/Re_x^{1/5}
```

99% velocity at approximately δ.

### Turbulence Models

| Model | Description | Best For |
|-------|-------------|----------|
| k-ε | Two-equation, dissipation | General industrial |
| k-ω | Two-equation, omega | Boundary layers |
| SST | Hybrid k-ω/k-ε | Adverse pressure gradients |
| RSM | Reynolds Stress | Strong curvature, rotation |
| LES | Large Eddy Simulation | Unsteady, separated flows |

-----

## Boundary Layers

### Boundary Layer Equations

For steady 2D laminar BL (∂p/∂x known from inviscid flow):
```
u∂u/∂x + v∂u/∂y = U dU/dx + ν ∂²u/∂y²
```

### Momentum Integral Equation (von Kármán)

```
d/dx(∫_0^δ ρ u(u - U) dy) = τ_w + (dU/dx)∫_0^δ ρ(u - U) dy
```

### Thermal Boundary Layer

For constant properties, same structure:
```
δ_T ≈ δ/Pr^{1/3} (laminar)
δ_T ≈ δ/Re_x^{1/5} Pr^{-1/3} (turbulent)
```

Prandtl number Pr = ν/α

### Heat Transfer (Laminar Flat Plate)

Nusselt number:
```
Nu_x = 0.332 Re_x^{1/2} Pr^{1/3}
```

Average over length L:
```
Nu_L = 0.664 Re_L^{1/2} Pr^{1/3}
```

### Separation

Adverse pressure gradient (dU/dx < 0) can cause flow separation:
- Boundary layer thickens
- Velocity gradient at wall becomes zero
- Flow reverses near wall

-----

## Compressible Flow

### Mach Number

```
M = V/a
```

- M < 1: Subsonic
- M = 1: Sonic
- M > 1: Supersonic
- M > 5: Hypersonic

### Isentropic Flow Relations

For ideal gas, γ = C_p/C_v:

| Ratio | Formula |
|-------|---------|
| T/T₀ | (1 + (γ-1)/2 M²)^{-1} |
| p/p₀ | (1 + (γ-1)/2 M²)^{-γ/(γ-1)} |
| ρ/ρ₀ | (1 + (γ-1)/2 M²)^{-1/(γ-1)} |

Area-Mach relation:
```
(A/A*) = (1/M)[(2/(γ+1))(1 + (γ-1)/2 M²)]^{(γ+1)/(2(γ-1))}
```

### Normal Shock Waves

Across shock (Rankine-Hugoniot):
```
p₂/p₁ = 1 + (2γ/(γ+1))(M₁² - 1)
T₂/T₁ = [1 + (2γ/(γ+1))(M₁² - 1)][2 + (γ-1)M₁²]/[(γ+1)M₁²]
M₂² = [1 + (γ-1)/2 M₁²]/[γ M₁² - (γ-1)/2]
```

Entropy increases across shock.

### Oblique Shocks

Shock angle β related to deflection θ:
```
tan θ = 2 cot β (M₁² sin²β - 1)/[M₁²(γ + cos 2β) + 2]
```

### Nozzle Flow

- Subsonic: Area decreases → M increases, p decreases
- Supersonic: Area increases → M increases, p decreases
- Sonic at throat (A = A*)
- Underexpanded/overexpanded nozzles

### Fanno Flow (Friction)

Adiabatic with friction in constant area duct:
- Choking at M = 1
- Maximum entropy at M = 1

### Rayleigh Flow (Heat Transfer)

Constant area with heat addition:
- Maximum temperature at M = 1/√((γ+1)/(γ-1))
- Can lead to thermal choking

-----

## Aerodynamics

### Lift Generation

```
L = ½ ρ V² A C_L
```

For infinite wing:
```
C_L = 2πα (thin airfoil theory)
```

With stall: C_L peaks then drops.

### Drag

```
D = ½ ρ V² A C_D
```

Components:
- **Pressure drag**: Due to pressure differences (form drag)
- **Friction drag**: Due to viscous shear
- **Induced drag**: Due to downwash from finite span
- **Wave drag**: Due to shock waves (supersonic)

### Aspect Ratio Effects

```
C_D = C_D₀ + C_L²/(π e AR)
```

Where e = Oswald efficiency (≈ 0.9 for typical wings).

### Airfoil Nomenclature

- **Chord**: c (leading to trailing edge)
- **Thickness**: t (max as fraction of c)
- **Camber**: mean camber line
- **Angle of attack**: α between chord line and flow

### Thin Airfoil Theory

Lift slope:
```
dC_L/dα = 2π (per radian)
```

Zero-lift angle α₀ (depends on camber).

### Wing Planforms

- Rectangular: Simple, low efficiency
- Tapered: Better, optimized
- Delta: High speed, low supersonic drag
- Swept: Delay wave drag

### Induced Drag

```
C_Di = C_L²/(π AR e)
```

### Compressibility Effects

**Critical Mach number**: First sonic point on airfoil.
**Drag divergence Mach**: Significant drag rise begins.

**Prandtl-Glauert correction**:
```
C_L = C_L,incompressible/√(1 - M²)
```

-----

## Dimensional Analysis

### Buckingham Pi Theorem

If equation involves n variables with k fundamental dimensions:
- Write dimension matrix
- Find rank
- Form n - k dimensionless groups

### Common Dimensionless Numbers

| Number | Definition | Significance |
|--------|------------|--------------|
| Reynolds | Re = ρVL/μ | Inertial/viscous |
| Froude | Fr = V²/(gL) | Inertial/gravitational |
| Weber | We = ρV²L/σ | Inertial/surface tension |
| Mach | M = V/a | Flow compressibility |
| Prandtl | Pr = ν/α = C_p μ/k | Momentum/thermal diffusion |
| Eckert | Ec = V²/(C_p ΔT) | Kinetic/thermal energy |
| Grashof | Gr = gβΔTL³/ν² | Buoyancy/viscous |

### Dynamic Similarity

Two flows similar if Re, M, Fr (as relevant) match.

-----

## Experimental Techniques

### Wind Tunnels

- **Subsonic**: Continuous or intermittent
- **Transonic**: Porous walls, slotted throat
- **Supersonic**: Converging-diverging nozzle
- **Hypersonic**: High M, low density

### Measurement Techniques

| Quantity | Methods |
|----------|---------|
| Velocity | Pitot-static, hot-wire, LDA, PIV |
| Pressure | Manometers, pressure transducers |
| Temperature | Thermocouples, IR, Pitot |
| Flow visualization | Smoke, oil, dye, shadows |

### Similarity Scaling

- Complete similarity: all relevant Pi groups equal
- Partial similarity: critical groups matched

-----

## Common Errors to Avoid

- Confusing static, dynamic, and stagnation pressures
- Applying Bernoulli incorrectly (not along streamline, including friction)
- Using laminar formulas for turbulent flow
- Ignoring compressibility at high Mach numbers
- Incorrectly applying continuity (mass balance)
- Confusing viscosity types (dynamic vs kinematic)
- Using wrong friction factor correlation
- Forgetting to convert to consistent units

-----

## Key References

- **Fluid Mechanics** by Kundu, Cohen, and Dowling — Comprehensive textbook
- **Boundary-Layer Theory** by Schlichting — Definitive BL text
- **Fundamentals of Aerodynamics** by Anderson — Aerodynamics intro
- **Theory of Wing Sections** by Abbott & von Doenhoff — Airfoil data

