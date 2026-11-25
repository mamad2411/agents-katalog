---

## name: photonics
description: >
  Expert photonics assistant for engineers and researchers. Use this skill whenever the user needs:
  understanding optical systems, lasers, fiber optics, optical communications, or any rigorous academic treatment of photonics.
  Covers optical fibers, waveguides, photodetectors, and integrated photonics.
license: MIT
compatibility: opencode
metadata:
  audience: students
  category: electrical-engineering

# Photonics — Academic Research Assistant

Covers: **Optics Fundamentals · Lasers · Fiber Optics · Waveguides · Photodetectors · Optical Communications · Integrated Photonics**

---

## Optics Fundamentals

### Electromagnetic Spectrum

|Wavelength|Region|Photon Energy|
|-----------|-------|-------------|
|100-400 nm|UV|3.1-12.4 eV|
|400-700 nm|Visible|1.8-3.1 eV|
|700 nm - 1 mm|IR|0.001-1.8 eV|

### Snell's Law

```python
class OpticsFundamentals:
    """Optics calculations"""
    
    def snells_law(self, n1, n2, theta1):
        """
        n1 × sin(θ1) = n2 × sin(θ2)
        """
        import numpy as np
        
        sin_theta2 = (n1 / n2) * np.sin(theta1)
        
        if abs(sin_theta2) <= 1:
            theta2 = np.arcsin(sin_theta2)
            return theta2
        else:
            return "Total internal reflection"
    
    def critical_angle(self, n1, n2):
        """
        θc = arcsin(n2/n1) for n1 > n2
        """
        import numpy as np
        
        if n1 > n2:
            return np.arcsin(n2 / n1)
        else:
            return "No critical angle"
    
    def fresnel_reflection(self, n1, n2, theta_i):
        """
        Fresnel equations for reflection
        """
        import numpy as np
        
        # Perpendicular polarization
        r_s = (n1 * np.cos(theta_i) - n2 * np.sqrt(1 - (n1/n2 * np.sin(theta_i))**2)) / \
              (n1 * np.cos(theta_i) + n2 * np.sqrt(1 - (n1/n2 * np.sin(theta_i))**2))
        
        # Parallel polarization
        r_p = (n2 * np.cos(theta_i) - n1 * np.sqrt(1 - (n1/n2 * np.sin(theta_i))**2)) / \
              (n2 * np.cos(theta_i) + n1 * np.sqrt(1 - (n1/n2 * np.sin(theta_i))**2))
        
        return r_s, r_p
```

---

## Lasers

### Laser Types

|Type|Active Medium|Output|Examples|
|----|--------------|------|--------|
|Solid-state|Nd:YAG, Ti:Sapphire|1064 nm, 800 nm|Laser pointers|
|Dye|Rhodamine 6G|Tunable|CW, pulsed|
|Gas|CO₂, HeNe|10.6 μm, 632 nm|Materials processing|
|Semiconductor|Diode lasers|635-1550 nm|Communications|
|Fiber|Erbium-doped|1550 nm|Telecom amplifiers|

### Laser Cavity

```python
class LaserPhysics:
    """Laser theory"""
    
    def gain_threshold(self, R1, R2, L, alpha):
        """
        Gain threshold: g_th = α + (1/2L) × ln(1/√(R1R2))
        """
        import numpy as np
        
        return alpha + (1 / (2 * L)) * np.log(1 / np.sqrt(R1 * R2))
    
    def output_power(self, P_pump, R_out, g_th, g_0):
        """
        Output power above threshold
        """
        if g_0 <= g_th:
            return 0
        
        return (P_pump * (g_0 - g_th) * R_out)
    
    def beam_divergence(self, wavelength, beam_waist):
        """
        Gaussian beam divergence
        θ = λ / (π × w₀)
        """
        return wavelength / (np.pi * beam_waist)
```

### Laser Safety

|Class|Hazard|Maximum Output|
|-----|-------|---------------|
|1|Safe|No hazard|
|2|Visible only|< 1 mW|
|3R|Direct eye hazard|< 5 mW|
|3B|Eye hazard|< 500 mW|
|4|Skin, fire hazard|> 500 mW|

---

## Optical Fibers

### Fiber Types

|Type|Structure|Applications|
|----|---------|------------|
|SM fiber (single-mode)|Core 8-10 μm|Telecom long-haul|
|MM fiber (multi-mode)|Core 50-100 μm|Short distance, LANs|
|Step-index|Rapid index change|Simple systems|
|Graded-index|Continuous index|High bandwidth|

### Fiber Attenuation

```python
class FiberOptics:
    """Fiber optic calculations"""
    
    # Loss mechanisms
    ATTENUATION = {
        " Rayleigh scattering": "~0.15 dB/km at 1550 nm",
        " Material absorption": "Depends on purity",
        " Microbending": "Mechanical stress",
        " Macrobending": "Bend radius too small"
    }
    
    def fiber_loss_dB(self, P_in, P_out, length):
        """
        Loss (dB) = 10 × log₁₀(P_in/P_out)
        Loss (dB/km) = Loss (dB) / length (km)
        """
        import numpy as np
        
        loss_dB = 10 * np.log10(P_in / P_out)
        loss_dB_per_km = loss_dB / length
        
        return loss_dB_per_km
    
    def power_after_distance(self, P_0, alpha_dB, distance):
        """
        P(z) = P₀ × 10^(-αz/10)
        """
        return P_0 * 10 ** (-alpha_dB * distance / 10)
    
    def bandwidth_distance_product(self, bandwidth, distance):
        """
        B × L = constant for graded-index fiber
        """
        return bandwidth * distance
```

### Dispersion

|Dispersion Type|Cause|Compensation|
|----------------|-----|------------|
|Chromatic|Different wavelengths|DCFB, gratings|
|Modal|Different modes|GRIN fiber|
|Polarization mode|PMD|PMD compensators|

---

## Waveguides

### Planar Waveguide Parameters

```python
class Waveguides:
    """Waveguide calculations"""
    
    def mode_condition(self, n_core, n_clad, d, wavelength):
        """
        Waveguide condition for single mode:
        V = (2π/λ) × a × NA < 2.405
        
        V = normalized frequency
        a = core radius
        NA = numerical aperture
        """
        import numpy as np
        
        NA = np.sqrt(n_core**2 - n_clad**2)
        V = (2 * np.pi / wavelength) * d * NA
        
        return {
            "V_number": V,
            "single_mode": V < 2.405
        }
    
    def numerical_aperture(self, n_core, n_clad):
        """
        NA = √(n₁² - n₂²)
        """
        import numpy as np
        return np.sqrt(n_core**2 - n_clad**2)
    
    def propagation_constant(self, n_eff, wavelength):
        """
        β = 2πn_eff/λ
        """
        return 2 * np.pi * n_eff / wavelength
```

---

## Photodetectors

### Detector Types

|Detector|Responsivity|Speed|Application|
|--------|------------|-----|-----------|
|PIN|0.7-0.9 A/W|Fast|Communications|
|APD|10-100 A/W|Fast|Remote sensing|
|PMT|10⁶ A/W|Very fast|Weak signals|
|Bolometer|Thermal|Slow|Power meter|

```python
class Photodetectors:
    """Detector calculations"""
    
    def responsivity(self, wavelength, quantum_efficiency):
        """
        R = η × q / (hν) = η × λ / 1.24
        """
        return quantum_efficiency * wavelength / 1.24
    
    def signal_to_noise(self, P_signal, P_dark, R, B):
        """
        SNR = (R × P_signal)² / (2qB(P_signal + P_dark))
        """
        import numpy as np
        
        i_signal = R * P_signal
        i_dark = R * P_dark
        
        noise_current = np.sqrt(2 * 1.6e-19 * B * (i_signal + i_dark))
        
        return i_signal / noise_current
    
    def noise_equivalent_power(self, i_dark, R, B):
        """
        NEP = i_n / R
        """
        import numpy as np
        
        i_n = np.sqrt(2 * 1.6e-19 * i_dark * B)
        
        return i_n / R
```

---

## Optical Communications

### WDM Systems

|WDM Type|Channels|Spacing|
|-------|--------|--------|
|CWDM|8-18|20 nm|
|DWDM|40-96|100 GHz/50 GHz|

### Link Budget

```python
class OpticalCommunications:
    """Link budget calculations"""
    
    def link_power_budget(self, P_tx, L_fiber, alpha, L_conn, margin):
        """
        P_rx = P_tx - L_fiber - L_conn - margin
        """
        total_loss = L_fiber * alpha + L_conn + margin
        
        return P_tx - total_loss
    
    def received_power_dBm(self, P_tx_dBm, loss_dB):
        """
        Convert to dBm
        """
        return P_tx_dBm - loss_dB
    
    def bit_error_rate(self, Q):
        """
        BER = ½ × erfc(Q/√2)
        """
        from scipy.special import erfc
        
        return 0.5 * erfc(Q / np.sqrt(2))
```

---

## Common Errors to Avoid

1. **Ignoring fiber bending losses** — Micro/macro-bends matter
2. **Wrong connector type** — APC vs. PC matters for return loss
3. **Not accounting for dispersion** — Limit data rate/distance
4. **Confusing laser classes** — Safety critical
5. **Ignoring polarization effects** — PMD in fibers
6. **Wrong detector for application** — Speed vs. sensitivity
7. **Not checking wavelength range** — Detectors have limits
8. **Ignoring coupling losses** — Connectors, splices add loss

