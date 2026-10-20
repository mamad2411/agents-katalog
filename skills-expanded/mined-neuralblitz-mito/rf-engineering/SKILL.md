---

## name: rf-engineering
description: >
  Radio frequency engineering expert for RF and microwave circuit design, wireless
  communication systems, antenna design, and electromagnetic analysis. Use this
  skill whenever the user needs: designing RF and microwave circuits, working with
  transmission lines and waveguides, analyzing RF systems and signal integrity,
  understanding antenna fundamentals and design, calculating propagation losses,
  working with S-parameters and network analysis, or any task involving radio
  frequency electronics from audio frequencies through microwave frequencies
  (approximately 20 kHz to 300 GHz). This skill covers both analog RF design
  and modern digital wireless communication systems.
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  category: electrical-engineering

# Radio Frequency Engineering

Covers: **Transmission Line Theory · S-Parameters · RF Amplifiers · Mixers & Oscillators · Antenna Design · Smith Charts · RF Propagation · Network Analysis**

-----

## Transmission Line Theory

### Fundamental Parameters

Transmission lines are characterized by four primary distributed parameters:

| Parameter | Symbol | Unit | Description |
|-----------|--------|------|-------------|
| Resistance | R | Ω/m | Conductor losses per unit length |
| Inductance | L | H/m | Magnetic field energy storage |
| Capacitance | C | F/m | Electric field energy storage |
| Conductance | G | S/m | Dielectric losses per unit length |

Derived parameters:
- **Characteristic impedance**: Z₀ = √((R + jωL)/(G + jωC))
- **Propagation constant**: γ = √((R + jωL)(G + jωC)) = α + jβ
- **Velocity of propagation**: v = 1/√(LC) = c/√(εᵣ)

### Lossless Line Equations

For lossless lines (R = G = 0):

```
Z₀ = √(L/C)
v = 1/√(LC)
β = ω√(LC)
```

### Terminated Transmission Line

When a transmission line of characteristic impedance Z₀ is terminated with load Z_L:

**Reflection coefficient:**
```
Γ = (Z_L - Z₀) / (Z_L + Z₀)
```

**Voltage Standing Wave Ratio (VSWR):**
```
VSWR = (1 + |Γ|) / (1 - |Γ|)
```

**Input impedance at distance d from load:**
```
Z_in(d) = Z₀ * (Z_L + jZ₀ tan(βd)) / (Z₀ + jZ_L tan(βd))
```

### Transmission Line Types

| Type | Frequency Range | Typical Z₀ | Applications |
|------|-----------------|-------------|--------------|
| Coaxial | DC - 110 GHz | 50Ω, 75Ω | Test equipment, CATV |
| Microstrip | 1 - 100 GHz | 30 - 100Ω | PCB circuits, IC interconnects |
| Stripline | 1 - 40 GHz | 50Ω | Filters, couplers |
| Waveguide | 1 - 110 GHz | N/A | High-power, millimeter-wave |
| Twin-lead | VHF | 300Ω | Antenna feed (legacy) |
| Parallel wire | HF - VHF | 600Ω | Balanced transmission |

-----

## S-Parameters (Scattering Parameters)

### Definition

S-parameters describe the input-output relationship of electrical networks at high frequencies where traditional voltage/current measurements are impractical. They measure power waves rather than voltages.

| Parameter | Definition | Description |
|-----------|------------|-------------|
| S₁₁ | b₁/a₁ (a₂=0) | Input return loss |
| S₂₁ | b₂/a₁ (a₂=0) | Forward transmission (gain) |
| S₁₂ | b₁/a₂ (a₁=0) | Reverse isolation |
| S₂₂ | b₂/a₂ (a₁=0) | Output return loss |

### Interpreting S-Parameters

**Return Loss (S₁₁, S₂₂):**
```
RL = -20 log₁₀|Γ| dB
```
- 0 dB = total reflection (open/short)
- -10 dB = 90% power absorbed
- -20 dB = 99% power absorbed

**Insertion Loss (S₂₁, S₁₂):**
```
IL = -20 log₁₀|S₂₁| dB
```
- 0 dB = unity gain (passive)
- Negative values indicate gain

### S-Parameter Measurement

```python
# Converting S-parameters to other formats
import numpy as np

def s_to_z(s, z0=50):
    """Convert S-parameter to Z-parameter"""
    z = z0 * (1 + s) / (1 - s)
    return z

def s_to_y(s, z0=50):
    """Convert S-parameter to Y-parameter"""
    y = (1 - s) / (z0 * (1 + s))
    return y

def s_to_abcde(s):
    """Convert S21/S11 to ABCD parameters"""
    s11, s12, s21, s22 = s[0,0], s[0,1], s[1,0], s[1,1]
    a = ((1 + s11) * (1 - s22) + s12 * s21) / (2 * s21)
    b = z0 * ((1 + s11) * (1 + s22) - s12 * s21) / (2 * s21)
    c = ((1 - s11) * (1 - s22) - s12 * s21) / (2 * s21)
    d = z0 * ((1 - s11) * (1 + s22) - s12 * s21) / (2 * s21)
    return np.array([[a, b], [c, d]])
```

### Smith Chart

The Smith Chart is a graphical tool for solving transmission line problems:

```python
# Mapping impedance to Smith Chart
def normalize_z(z, z0=50):
    """Normalize impedance to Smith Chart"""
    return z / z0

def gamma_from_z(z_norm):
    """Calculate reflection coefficient from normalized impedance"""
    return (z_norm - 1) / (z_norm + 1)

def z_from_gamma(gamma):
    """Calculate normalized impedance from reflection coefficient"""
    return (1 + gamma) / (1 - gamma)

def gamma_to_smith(gamma):
    """Convert gamma to Smith Chart coordinates"""
    r = gamma.real
    i = gamma.imag
    mag = np.abs(gamma)
    return r, i  # Plot at (r, i) on the gamma plane
```

Common Smith Chart operations:
- Series impedance: Move right along constant resistance circles
- Shunt admittance: Move left along constant conductance circles
- Transmission line: Rotate around center (constant VSWR circle)
- Stub: Combination of rotation and impedance movement

-----

## RF Amplifiers

### Amplifier Classes

| Class | Conduction Angle | Efficiency | Typical Use |
|-------|-----------------|------------|-------------|
| A | 360° | < 25% | Low-power, high linearity |
| AB | 180° - 360° | 25-50% | Moderate power |
| B | 180° | 50-78% | Push-pull amplifiers |
| C | < 180° | 78-90% | Oscillators, FM transmitters |
| D/E/F | Switching | > 90% | High-efficiency RF |

### Amplifier Parameters

**Gain:**
```
G (dB) = P_out/P_in (dB) = 10 log₁₀(P_out/P_in)
```

**1 dB Compression Point (P1dB):**
The output power where gain is 1 dB less than the small-signal gain.

**Third-Order Intercept Point (IP3):**
```
IP3 = P_out + (IM3/2)
```
Where IM3 is the intermodulation distortion level in dBc.

**Noise Figure (NF):**
```
NF (dB) = 10 log₁₀(F)
F = SNR_in / SNR_out
```

### Low-Noise Amplifier Design

```python
# LNA design parameters
def calculate_noise_temperature(nf_db):
    """Convert Noise Figure to Noise Temperature"""
    f = 10**(nf_db/10)
    return 290 * (f - 1)

def cascade_noise_figure(f1, f2, g1_db, g2_db):
    """Calculate cascaded noise figure"""
    f1_val = 10**(f1/10)
    f2_val = 10**(f2/10)
    g1 = 10**(g1_db/10)
    return f1_val + (f2_val - 1) / g1

# Typical LNA specifications
lna_specs = {
    'frequency_range': '1-10 GHz',
    'gain': '20-30 dB',
    'noise_figure': '0.5-2 dB',
    'p1db': '-10 to -5 dBm',
    'ip3': '0 to +10 dBm',
    'input_vswr': '< 2:1'
}
```

### Amplifier Stability

**Stability Factor (K):**
```
K = (1 - |S11|² - |S22|² + |Δ|²) / (2|S12 S21|)
```
Where Δ = S11 S22 - S12 S21

- K > 1: Unconditionally stable
- K < 1: Potentially unstable; may oscillate

**Stabilization techniques:**
- Resistive loading
- Feedback networks
- Neutralization (adding compensation capacitance)
- Circuit bounding

-----

## Mixers and Frequency Conversion

### Mixer Types

| Type | Configuration | Conversion Gain | Noise |
|------|---------------|-----------------|-------|
| Passive (diode) | Single/double balanced | Loss (~6 dB) | Low |
| Active (transistor) | Single/double balanced | Gain (5-15 dB) | Moderate |
| Subharmonic | Using subharmonic mixers | Loss | Moderate |
| Image reject | Single sideband | Loss | Good |

### Mixer Specifications

**Conversion Loss/Gain:**
```
L (dB) = P_IF / P_RF (for passive mixers)
```

**Isolation:**
- RF-IF isolation
- LO-RF isolation  
- LO-IF isolation

**Intermodulation Products:**
```
f_IF = m * f_LO ± n * f_RF
```

### Double-Balanced Mixer Circuit

```python
# Mixer spur calculation
def calculate_if_frequency(f_rf, f_lo, mode='upper'):
    """Calculate IF output frequency"""
    if mode == 'upper':
        return abs(f_lo + f_rf)
    elif mode == 'lower':
        return abs(f_lo - f_rf)
    else:
        raise ValueError("Mode must be 'upper' or 'lower'")

def mixer_intermods(f_rf, f_lo, max_order=5):
    """Calculate intermodulation products"""
    intermods = []
    for m in range(-max_order, max_order + 1):
        for n in range(-max_order, max_order + 1):
            if m == 0 and n == 0:
                continue
            f_im = abs(m * f_lo + n * f_rf)
            if f_im > 0:
                intermods.append({
                    'order': abs(m) + abs(n),
                    'frequency': f_im,
                    'coeffs': (m, n)
                })
    return sorted(intermods, key=lambda x: x['order'])
```

### Oscillator Design

**Oscillation Conditions (Barkhausen):**
1. Loop gain ≥ 1 (|βA| = 1)
2. Phase shift = 0° or 360° (∠βA = 0)

**Oscillator Topologies:**
- Colpitts (LC tank)
- Crystal (series/parallel)
- Ring (odd number of stages)
- Dielectric resonator (DRC)
- Voltage-controlled (VCO)

```python
# Phase noise calculation (Leeson's equation)
def phase_noise(f_offset, f_carrier, Q, f_n, P_out_dbm, F_noise):
    """Calculate phase noise in dBc/Hz"""
    # Leeson's equation
    k = 1.38e-23  # Boltzmann constant
    T = 290       # Temperature in Kelvin
    P_in = 1e-3   # Input power (1 mW)
    
    f_offset = max(f_offset, f_n)  # Must be above flicker corner
    
    pn = 10 * np.log10(
        (k * T * F_noise / P_in) * 
        (f_carrier / (2 * Q * f_offset))**2
    )
    return pn
```

-----

## Antenna Fundamentals

### Basic Antenna Parameters

| Parameter | Symbol | Unit | Description |
|-----------|--------|------|-------------|
| Gain | G | dBi/dBd | Directive gain minus losses |
| Directivity | D | None | Ratio of max radiation to isotropic |
| Efficiency | η | % | Radiation efficiency |
| Bandwidth | BW | % or Hz | Operating frequency range |
| VSWR | - | Ratio | Impedance match |
| Polarization | - | Linear/Circular | E-field orientation |

### Common Antenna Types

| Antenna Type | Gain | Bandwidth | Applications |
|--------------|------|-----------|--------------|
| Dipole (λ/2) | 2.1 dBi | ~10% | HF-VHF, rabbit ears |
| Monopole (λ/4) | 0 dBi | ~10% | Mobile, whip antennas |
| Yagi-Uda | 5-15 dBi | ~10% | TV, point-to-point |
| Helical | 10-15 dBi | Wideband | Circular polarization |
| Microstrip | 3-10 dBi | Narrow | Arrays, satellites |
| Parabolic | 20-40 dBi | Narrow | Point-to-point, radar |
| Horn | 10-20 dBi | Wideband | Feed horns, measurement |
| Loop | 0-3 dBi | Narrow | Direction finding |

### Antenna Pattern Metrics

```python
# Calculate antenna pattern parameters
def calculate_directivity(phi_hpbw, theta_hpbw):
    """Calculate directivity from beamwidths (degrees)"""
    # Approximate formula
    D = 41253 / (phi_hpbw * theta_hpbw)
    return 10 * np.log10(D)

def calculate_gain(efficiency, directivity):
    """Calculate gain from efficiency (decimal)"""
    return efficiency * directivity

def beam_efficiency(main_lobe, total_power):
    """Calculate beam efficiency"""
    return main_lobe / total_power * 100

# Example pattern
antenna_pattern = {
    'hpbw_azimuth': 30,  # degrees
    'hpbw_elevation': 30,
    'front_to_back': 20,  # dB
    'side_lobe_level': -15,  # dB
    'efficiency': 0.9
}
```

### Friis Transmission Equation

```python
def friis_path_loss(freq_mhz, dist_m, tx_gain_dbi, rx_gain_dbi):
    """Calculate free space path loss and received power"""
    # Wavelength in meters
    wavelength = 300 / freq_mhz
    
    # Free space path loss
    fspl = 20 * np.log10(4 * np.pi * dist_m / wavelength)
    
    # Total path loss
    path_loss = fspl - tx_gain_dbi - rx_gain_dbi
    
    return path_loss

def received_power(tx_power_dbm, path_loss_dbi):
    """Calculate received power"""
    return tx_power_dbm - path_loss_dbi

# Example
tx_power = 30  # dBm
freq = 2400    # MHz
distance = 100  # meters
tx_gain = 3     # dBi
rx_gain = 2     # dBi

loss = friis_path_loss(freq, distance, tx_gain, rx_gain)
rx_pwr = received_power(tx_power, loss)
print(f"Path Loss: {loss:.1f} dB")
print(f"Received Power: {rx_pwr:.1f} dBm")
```

### Array Antenna Design

```python
# Linear array factor
def array_factor(n_elements, d_wavelength, theta_deg, phase_diff=0):
    """Calculate array factor for linear array"""
    theta = np.radians(theta_deg)
    k = 2 * np.pi  # Wave number (wavelength = 1)
    
    # Element spacing in wavelengths
    beta = k * d_wavelength * np.cos(theta) + phase_diff
    
    # Array factor
    af = np.abs(np.sin(n_elements * beta / 2) / 
                (n_elements * np.sin(beta / 2)))
    
    return af

# Beam steering
def beam_steering_angle(d_wavelength, theta_desired):
    """Calculate phase shift for beam steering"""
    k = 2 * np.pi
    phase_shift = k * d_wavelength * np.cos(np.radians(theta_desired))
    return phase_shift
```

-----

## RF Propagation

### Propagation Mechanisms

| Mechanism | Frequency | Description |
|-----------|-----------|-------------|
| Free space | All | Inverse square law attenuation |
| Ground wave | < 3 MHz | Surface wave follows Earth curvature |
| Sky wave | 3-30 MHz | Ionospheric reflection |
| Line-of-sight | > 30 GHz | Direct path, Fresnel zones |

### Path Loss Models

```python
# Free space path loss
def free_space_path_loss(f_mhz, dist_km):
    """Calculate FSPL in dB"""
    return 20 * np.log10(dist_km) + 20 * np.log10(f_mhz) + 32.44

# Okumura-Hata model (urban)
def okumura_hata(f_mhz, h_b, h_m, dist_km):
    """Calculate path loss in urban environment"""
    # Valid for 150-1500 MHz, 1-20 km
    a_h_m = 3.2 * (np.log10(11.75 * h_m))**2 - 4.97
    
    path_loss = 69.55 + 26.16 * np.log10(f_mhz) - \
                13.82 * np.log10(h_b) - a_h_m + \
                (44.9 - 6.55 * np.log10(h_b)) * np.log10(dist_km)
    
    return path_loss

# Log-distance path loss model
def log_distance_path_loss(n, d_ref, d, pl_ref):
    """Calculate path loss using log-distance model"""
    # n: path loss exponent
    # d_ref: reference distance
    # d: actual distance
    # pl_ref: path loss at reference distance
    return pl_ref + 10 * n * np.log10(d / d_ref)
```

### Fresnel Zones

```python
def fresnel_radius(n, freq_mhz, dist_km):
    """Calculate n-th Fresnel zone radius"""
    wavelength = 300 / freq_mhz
    r = 547.7 * np.sqrt(n * dist_km / wavelength)
    return r

def fresnel_clearance(d1, d2, h_obstacle, freq_mhz):
    """Calculate Fresnel clearance"""
    height = fresnel_radius(1, freq_mhz, d1 * d2 / (d1 + d2))
    clearance = h_obstacle / height
    return clearance

# Typical clearance requirements
clearance_requirements = {
    '0%': 'Edge just touches LOS',
    '20%': 'Minor effect, acceptable',
    '40%': 'Good clearance',
    '60%': 'Excellent clearance',
    '100%': 'Full Fresnel clearance'
}
```

### Atmospheric Effects

- **Rain attenuation**: Significant above 10 GHz
- **Gas absorption**: Oxygen (~60 GHz) and water vapor (~22 GHz)
- **Tropospheric scattering**: Above 1 GHz, enables beyond-horizon paths
- **Building penetration**: Varies with frequency and material

-----

## Common Errors to Avoid

- **Ignoring impedance matching**: VSWR > 3:1 causes significant power loss
- **Forgetting connector types**: SMA, N, BNC, F type are not interchangeable
- **Neglecting ground planes**: Many antennas require proper ground for operation
- **Using wrong cable at frequency**: Loss increases dramatically with frequency
- **Ignoring EMI/EMC**: RF circuits are susceptible to interference
- **Not considering temperature effects**: Component values change with temperature
- **Confusing dBm and dB**: dBm is absolute power, dB is relative
- **Oversimplifying filters**: Real filters have parasitic elements
- **Ignoring skin effect**: Conductor loss increases with frequency
- **Not accounting for VSWR in power measurements**: Always use proper detection
