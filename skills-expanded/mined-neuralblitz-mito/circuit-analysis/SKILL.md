-----

## name: circuit-analysis
description: >
  Expert circuit analysis assistant for electrical engineers and students. Use this skill whenever the user needs:
  help with circuit analysis using Kirchhoff's laws, nodal and mesh analysis, Thevenin/Norton equivalents,
  op-amp circuit design, filter design, frequency response analysis, or simulation of analog and digital circuits.
  Includes both theoretical foundations and practical design guidance.
trigger: Any electrical engineering problem involving circuits - from simple DC analysis to complex AC networks and filter design.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: electrical-engineering

# Circuit Analysis — Theory and Design

Covers: **DC Analysis · AC Analysis · Network Theorems · Circuit Simulation · Filters · Operational Amplifiers · Transient Response**

-----

## Fundamental Laws

### Kirchhoff's Current Law (KCL)

At any node (junction): the algebraic sum of currents entering equals sum leaving.

```
Σ I_in = Σ I_out
```

### Kirchhoff's Voltage Law (KVL)

Around any closed loop: the algebraic sum of voltage drops equals zero.

```
Σ V = 0
```

### Ohm's Law

```
V = IR
```

In generalized form (for any two-terminal element):
```
V = ZI
```

Where Z is impedance (complex in AC).

### Power

Instantaneous power:
```
p(t) = v(t)i(t)
```

Average power (periodic):
```
P_avg = (1/T) ∫ p(t) dt = VI cos(θ_v - θ_i) = VI cos(φ)
```

For purely resistive: P = VI = I²R = V²/R

### Energy

```
W = ∫ p(t) dt
```

-----

## Circuit Elements

### Passive Elements

| Element | v-i Relation | Impedance Z | Power |
|---------|--------------|-------------|-------|
| Resistor | v = iR | R | P = I²R |
| Inductor | v = L di/dt | jωL | Stores energy: W = ½LI² |
| Capacitor | i = C dv/dt | 1/jωC = -j/ωC | Stores energy: W = ½CV² |

### Energy Storage Comparison

| Element | Current lags voltage by... | Voltage lags current by... |
|---------|--------------------------|---------------------------|
| Inductor | 90° | - |
| Capacitor | - | 90° |

### Active Elements

- **Voltage source**: Fixed voltage, current determined by circuit
- **Current source**: Fixed current, voltage determined by circuit
- **Dependent sources**: Output depends on another voltage/current

### Equivalent Circuits

**Series combination**:
- Resistors: R_eq = R₁ + R₂ + ...
- Inductors: L_eq = L₁ + L₂ + ...
- Capacitors: 1/C_eq = 1/C₁ + 1/C₂ + ...

**Parallel combination**:
- Resistors: 1/R_eq = 1/R₁ + 1/R₂ + ...
- Inductors: 1/L_eq = 1/L₁ + 1/L₂ + ...
- Capacitors: C_eq = C₁ + C₂ + ...

-----

## Analysis Methods

### Nodal Analysis

1. Select a reference node (ground)
2. Write KCL at each non-reference node
3. Express voltages in terms of node voltages
4. Solve resulting equations

**Procedure**:
```
At node V₁: (V₁ - V₂)/R₁ + V₁/R₂ = I₁
At node V₂: (V₂ - V₁)/R₁ + (V₂ - V₃)/R₃ = 0
```

### Mesh Analysis

1. Define mesh currents for each independent loop
2. Write KVL around each mesh
3. Solve for mesh currents
4. Find branch currents from mesh currents

**Procedure**:
```
Mesh I₁: -V₁ + I₁R₁ + (I₁ - I₂)R₂ = 0
Mesh I₂: (I₂ - I₁)R₂ + I₂R₃ + V₂ = 0
```

### Choosing Method

| Method | Best For |
|--------|----------|
| Nodal | Voltage sources, many components to ground |
| Mesh | Current sources, planar circuits |

### Systematic Solution

For linear circuits with n nodes or m meshes:
- Write equations in matrix form
- Use Cramer's rule or matrix inversion
- Consider symbolic vs. numerical solutions

-----

## Network Theorems

### Superposition

For linear circuits: total response = sum of responses from each source acting alone.

**Steps**:
1. Deactivate all independent sources except one
2. Find circuit response
3. Repeat for each source
4. Sum all responses

**Deactivation rules**:
- Voltage source → short circuit (V = 0)
- Current source → open circuit (I = 0)

### Thevenin's Theorem

Any linear two-terminal network can be replaced by:
- **Thevenin voltage** V_th: open-circuit voltage
- **Thevenin resistance** R_th: resistance with sources deactivated

**Finding R_th**:
- Deactivate sources → find equivalent resistance
- Or: R_th = V_th / I_sc (open-circuit / short-circuit current)

### Norton's Theorem

Complement to Thevenin:
- **Norton current** I_N: short-circuit current
- **Norton resistance** R_N = R_th

**Equivalence**: V_th = I_N R_th

### Maximum Power Transfer

For a given Thevenin equivalent, maximum power to load occurs when:
```
R_L = R_th
```

Maximum power:
```
P_max = V_th²/(4R_th)
```

### Source Transformation

Voltage source V with series R ↔ Current source I = V/R with parallel R

### Delta-Wye (Δ-Y) Transformation

**Δ to Y**:
```
R₁ = (R_ab R_ac)/(R_ab + R_ac + R_bc)
```

**Y to Δ**:
```
R_ab = (R₁ R₂ + R₂ R₃ + R₃ R₁)/R₃
```

### Millman's Theorem

For n parallel branches with series voltages:
```
V_out = (Σ V_i/R_i) / (Σ 1/R_i)
```

-----

## AC Circuit Analysis

### Phasor Representation

```
v(t) = V_m cos(ωt + θ) → V = V_m ∠θ
```

Euler's relation: e^(jθ) = cos θ + j sin θ

### Impedance

| Element | Impedance |
|---------|----------|
| Resistor R | R ∠ 0° |
| Inductor jωL | jωL = ωL ∠ 90° |
| Capacitor 1/jωC | -j/ωC = 1/ωC ∠ -90° |

### Complex Power

```
S = VI* = P + jQ
```

- Real power: P = VI cos φ [W]
- Reactive power: Q = VI sin φ [VAR]
- Apparent power: |S| = VI [VA]

Power factor: pf = cos φ = P/|S|

### AC Circuit Analysis Procedure

1. Convert all sources to phasors
2. Replace L and C with jωL and 1/jωC
3. Solve using KCL/KVL (complex algebra)
4. Convert results back to time domain

### Resonance

At resonance, imaginary part of impedance = 0.

**Series resonance**:
```
ω₀ = 1/√(LC)
```

- Minimum impedance (resistive)
- Current maximum
- Q = ω₀L/R = 1/(ω₀CR)

**Parallel resonance**:
```
ω₀ = 1/√(LC) × √(1 - 1/Q²)
```

- Maximum impedance
- Current minimum

### Quality Factor Q

```
Q = energy stored / energy dissipated per cycle
```

For series RLC: Q = ω₀L/R = 1/(ω₀CR)

-----

## Operational Amplifiers

### Ideal Op-Amp Characteristics

| Property | Ideal Value |
|----------|-------------|
| Open-loop gain A | ∞ |
| Input impedance Z_in | ∞ |
| Output impedance Z_out | 0 |
| Bandwidth | ∞ |
| Input bias current | 0 |
| Input offset voltage | 0 |

### Golden Rules

1. Inputs draw no current (Z_in = ∞)
2. Inputs at same voltage (V+ = V- for negative feedback)

### Basic Configurations

| Configuration | Gain | Formula |
|--------------|------|--------|
| Inverting | V_out/V_in | -R_f/R₁ |
| Non-inverting | V_out/V_in | 1 + R_f/R₁ |
| Voltage follower | V_out/V_in | 1 (buffer) |
| Summing | V_out | -(R_f/R₁)V₁ - (R_f/R₂)V₂ |
| Differential | V_out | (R_f/R₁)(V₂ - V₁) |

### Op-Amp Specifications (Real)

| Parameter | Typical Value | Impact |
|-----------|---------------|--------|
| A (open-loop gain) | 10⁵ - 10⁷ | Closed-loop gain error |
| f_T (gain-bandwidth) | 1-100 MHz | Bandwidth limitation |
| Input offset voltage | μV - mV | Output offset |
| Input bias current | nA - μA | Bias current errors |
| Slew rate | 1-100 V/μs | Max dV/dt |

### Common Op-Amp Circuits

**Instrumentation amplifier**: High CMRR, high input impedance

**Integrator**: V_out = -(1/RC) ∫ V_in dt

**Differentiator**: V_out = -RC dV_in/dt

**Log/Anti-log**: Using diode/transistor characteristics

**Active filters**: Sallen-Key, Multiple Feedback

-----

## Frequency Response

### Transfer Function

```
H(jω) = Y(jω)/X(jω) = |H(jω)| e^{j∠H(jω)}
```

- Magnitude: |H(jω)|
- Phase: ∠H(jω)

### Bode Plots

**Magnitude** (log-log):
- 20 log₁₀|H(jω)| in dB
- Slope changes at poles/zeros

**Phase** (log-linear):
- ∠H(jω) in degrees
- -45°/decade per pole, +45°/decade per zero

### Bode Plot Rules

| Corner Frequency | Magnitude Change | Phase Change |
|-----------------|------------------|--------------|
| Pole | -20 dB/dec | -45° to -90° |
| Zero | +20 dB/dec | +45° to +90° |

### Filter Types

| Filter | Passband | Stopband | Application |
|--------|----------|----------|-------------|
| Low-pass | 0 to f_c | f > f_c | Anti-aliasing |
| High-pass | f > f_c | 0 to f_c | DC blocking |
| Band-pass | f₁ to f₂ | Outside | Select frequencies |
| Band-stop | Outside | f₁ to f₂ | Notch filter |

### First-Order Filters

**RC Low-pass**:
```
H(s) = 1/(1 + sRC)
f_c = 1/(2πRC)
```

**RC High-pass**:
```
H(s) = sRC/(1 + sRC)
f_c = 1/(2πRC)
```

### Second-Order Filters

**Sallen-Key low-pass**:
```
H(s) = 1/(1 + s(3-k)/ω₀ + s²/ω₀²)
```

Where k = R_f/R₁ (gain).

**Butterworth**: Maximally flat magnitude
**Chebyshev**: Ripple in passband
**Elliptic**: Ripple in both bands

### Bandwidth and Q

```
BW = f_c / Q
```

For second-order: Q determines peaking at resonance.

-----

## Transient Analysis

### Time Domain Solution

For RC circuits:
```
v(t) = V_final + (V_initial - V_final)e^{-t/τ}
```

Where τ = RC (time constant)

For RL circuits: τ = L/R

### First-Order Step Response

| Circuit | v(t) for t > 0 |
|---------|----------------|
| RC (voltage source) | V_s(1 - e^{-t/RC}) |
| RL (voltage source) | V_s/R (1 - e^{-Rt/L}) |

### Second-Order Systems

For series RLC:
```
s² + (R/L)s + 1/(LC) = 0
```

**Damping ratio**:
```
ζ = R/(2)√(C/L) = R/(2)√(C/L)
```

| ζ Value | Response |
|---------|----------|
| ζ > 1 | Overdamped |
| ζ = 1 | Critically damped |
| ζ < 1 | Underdamped (oscillations) |

### Underdamped Response

```
v(t) = A e^{-αt} cos(ω_d t + φ)
```

Where:
- α = ζω_n
- ω_d = ω_n √(1 - ζ²)
- ω_n = 1/√(LC) (natural frequency)

### Laplace Transform Solution

```
V(s) = H(s)V_in(s)
```

Transform pairs:
- 1/s → u(t)
- 1/(s+a) → e^{-at}u(t)
- ω/(s² + ω²) → sin(ωt)u(t)

-----

## Circuit Simulation

### SPICE Basics

```
.Title: Circuit Name
* Comments
R1 1 2 1k
C1 2 0 1uF
V1 1 0 DC 5 AC 1
.AC DEC 10 1 10k
.PROBE
.END
```

### Analysis Types

| Directive | Purpose |
|-----------|---------|
| .DC | DC sweep |
| .AC | AC frequency sweep |
| .TRAN | Transient analysis |
| .NOISE | Noise analysis |
| .TF | Transfer function |

### Model Parameters

- **Resistor**: R = value, TC1 = temp coefficient
- **Capacitor**: C = value, V = voltage coefficient
- **MOSFET**: LEVEL, L, W, VTO, KP...

### Simulation Best Practices

- Check convergence options
- Use appropriate time steps
- Include initial conditions (.IC)
- Verify with hand calculations
- Model parasitics for accuracy

-----

## Common Errors to Avoid

- Forgetting to deactivate sources when finding Thevenin resistance
- Confusing series and parallel combinations
- Using wrong reference for nodal analysis
- Applying superposition to power (not linear)
- Forgetting to use complex numbers in AC analysis
- Confusing ω and f in reactance calculations
- Not considering op-amp saturation
- Using wrong filter cutoff formula
- Ignoring load effects in source transformation
- Confusing transient and steady-state responses

-----

## Key References

- **Fundamentals of Electric Circuits** by Sadiku — Standard textbook
- **Microelectronic Circuits** by Sedra/Smith — Op-amps and more
- **SPICE for Circuits and Electronics** by Rashid — Simulation
- **The Art of Electronics** by Horowitz & Hill — Practical design

