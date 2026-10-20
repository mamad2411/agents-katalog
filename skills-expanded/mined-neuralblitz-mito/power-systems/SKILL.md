---

## name: power-systems
description: >
  Expert power systems assistant for engineers and researchers. Use this skill whenever the user needs:
  understanding power generation, transmission, distribution, load flow analysis, fault analysis, or any rigorous academic 
  treatment of power systems engineering. Covers grid analysis, stability, and renewable integration.
license: MIT
compatibility: opencode
metadata:
  audience: students
  category: electrical-engineering

# Power Systems — Academic Research Assistant

Covers: **Power Generation · Transmission Lines · Load Flow · Fault Analysis · System Stability · Grid Operation · Renewable Integration**

---

## Power System Fundamentals

### Three-Phase Systems

```python
class PowerSystemBasics:
    """Power system calculations"""
    
    def apparent_power(self, V, I):
        """
        S = √3 × V_L × I_L (three-phase)
        S = V × I (single-phase)
        """
        return 3 ** 0.5 * V * I
    
    def real_power(self, S, pf):
        """
        P = S × cos(φ) = S × PF
        """
        return S * pf
    
    def reactive_power(self, S, pf):
        """
        Q = S × sin(φ)
        """
        import math
        return S * math.sin(math.acos(pf))
    
    def power_factor(self, P, S):
        """
        PF = P/S
        """
        return P / S
    
    def balanced_three_phase(self, V_phase, phase_sequence='abc'):
        """
        Phase-to-phase: V_LL = √3 × V_LN
        """
        return {
            "line_to_line": 3 ** 0.5 * V_phase,
            "line_to_neutral": V_phase,
            "phase_angle": 0 if phase_sequence == 'abc' else -120
        }
```

---

## Transmission Lines

### Line Parameters

|Parameter|Definition|Units|
|---------|-----------|-----|
|R|Resistance|Ω/km|
|L|Inductance|H/km|
|G|Conductance|S/km|
|C|Capacitance|F/km|

### Line Models

```python
class TransmissionLines:
    """Transmission line analysis"""
    
    def characteristic_impedance(self, L, C):
        """
        Z₀ = √(L/C)
        """
        return (L / C) ** 0.5
    
    def propagation_constant(self, R, G, L, C, omega):
        """
        γ = √((R + jωL)(G + jωC))
        """
        import cmath
        import math
        
        Z = complex(0, omega * L) + R
        Y = complex(0, omega * C) + G
        
        gamma = cmath.sqrt(Z * Y)
        
        return {
            "alpha": gamma.real,  # Attenuation
            "beta": gamma.imag    # Phase constant
        }
    
    def voltage_regulation(self, V_send, V_receive, pf):
        """
        VR = (|V_send| - |V_receive|) / |V_receive| × 100%
        """
        return (abs(V_send) - abs(V_receive)) / abs(V_receive) * 100
    
    def power_flow_line(self, V1, V2, X, delta):
        """
        P12 = (V1 × V2 / X) × sin(δ)
        """
        return (V1 * V2 / X) * math.sin(delta)
```

### Short, Medium, Long Lines

|Model|Length|Parameters|
|-----|-------|-----------|
|Short|< 80 km|R only|
|Medium|80-250 km|R + jX|
|Long|> 250 km|π-equivalent|

---

## Load Flow Analysis

### Newton-Raphson Method

```python
class LoadFlowAnalysis:
    """Power flow calculations"""
    
    def y_bus_admittance(self, bus_data, line_data):
        """
        Build Y-bus matrix
        Y_ij = ΣY_ij for all connections
        """
        import numpy as np
        
        n_buses = len(bus_data)
        Y = np.zeros((n_buses, n_buses), dtype=complex)
        
        # Add line admittances
        # Self-admittances and mutual admittances
        
        return Y
    
    def newton_raphson(self, Y_bus, P_spec, Q_spec, V_mag, n_iter=10):
        """
        Solve load flow iteratively
        """
        # Initialize voltages
        n = len(Y_bus)
        V = np.ones(n) * V_mag  # Flat start
        delta = np.zeros(n)  # Angle
        
        for iteration in range(n_iter):
            # Calculate P and Q
            P_calc = np.zeros(n)
            Q_calc = np.zeros(n)
            
            for i in range(n):
                for j in range(n):
                    P_calc[i] += V[i] * V[j] * abs(Y_bus[i,j]) * \
                                math.sin(math.angle(Y_bus[i,j]) - delta[i] + delta[j])
                    Q_calc[i] += V[i] * V[j] * abs(Y_bus[i,j]) * \
                                -math.cos(math.angle(Y_bus[i,j]) - delta[i] + delta[j])
            
            # Power mismatches
            dP = P_spec - P_calc
            dQ = Q_spec - Q_calc
            
            # Check convergence
            if max(abs(dP), abs(dQ)) < 0.0001:
                print(f"Converged in {iteration} iterations")
                break
            
            # Jacobian update (simplified)
            # Would update V and delta here
            
        return V, delta
```

### Bus Types

|Bus Type|Known Variables|Unknown|
|--------|---------------|--------|
|Slack (reference)|V, δ|P, Q|
|PV generator|V, P|Q, δ|
|Load|P, Q|V, δ|

---

## Fault Analysis

### Symmetrical Components

```python
class FaultAnalysis:
    """Fault calculations"""
    
    def symmetrical_components(self, V_a, V_b, V_c):
        """
        Convert phase voltages to sequence components
        """
        import numpy as np
        
        a = complex(-0.5, 3**0.5 / 2)
        
        V0 = (V_a + V_b + V_c) / 3
        V1 = (V_a + a * V_b + a**2 * V_c) / 3
        V2 = (V_a + a**2 * V_b + a * V_c) / 3
        
        return {"V0": V0, "V1": V1, "V2": V2}
    
    def fault_current_three_phase(self, V_prefault, Z_f):
        """
        I_f = V / Z_f (three-phase fault)
        """
        return V_prefault / Z_f
    
    def fault_current_line_to_ground(self, V_prefault, Z0, Z1, Z2, Z_f):
        """
        I_f = 3 × V / (Z0 + Z1 + Z2 + 3Z_f)
        """
        Z_total = Z0 + Z1 + Z2 + 3 * Z_f
        return 3 * V_prefault / Z_total
```

### Fault Types

|Type|Impedance|Application|
|----|---------|-----------|
|Three-phase|Z₀ = Z₁ = Z₂|Symmetric|
|Line-to-ground|Z₁ + Z₂ + Z₀|Most common|
|Line-to-line|Z₁ = Z₂|Phase fault|
|Double line-to-ground|Rare|Unbalanced|

---

## Power System Stability

### Stability Types

|Type|Timeframe|Concern|
|----|---------|-------|
|Transient|< 10 s|Fault clearing|
|Dynamic|10-30 s|Control systems|
|Small-signal|Continuous|Oscillations|
|Voltage|< 1 s|Load changes|
|Frequency|Seconds|Generation/load|

```python
class StabilityAnalysis:
    """Stability calculations"""
    
    def swing_equation(self, H, f, delta, P_m, P_e):
        """
        2H/d²δ/dt² = P_m - P_e
        
        d²δ/dt² = (πf/H)(P_m - P_e)
        """
        return math.pi * f / H * (P_m - P_e)
    
    def critical_clearing_time(self, H, f, delta_critical, P_m, P_max):
        """
        Estimate critical clearing angle/time
        """
        # Simplified
        return 0
    
    def frequency_deviation(self, Delta_P, H, f_nom):
        """
        df/dt = ΔP / (2H)
        """
        return Delta_P / (2 * H)
```

---

## Renewable Integration

### Solar PV

```python
class RenewableSystems:
    """Renewable integration"""
    
    def pv_power_output(self, G, A, η_module, η_inverter):
        """
        P = G × A × η_module × η_inverter
        
        G = irradiance (W/m²)
        A = area (m²)
        """
        return G * A * η_module * η_inverter
    
    def wind_power(self, rho, A, v, Cp):
        """
        P = ½ × ρ × A × v³ × Cp
        
        Cp = power coefficient (Betz limit: 0.59)
        """
        return 0.5 * rho * A * v**3 * Cp
    
    def inverter_sizing(self, P_dc, DC_AC_ratio):
        """
        P_ac = P_dc × DC_AC_ratio
        Typical ratio: 1.1-1.4
        """
        return P_dc * DC_AC_ratio
```

### Grid Code Requirements

|Parameter|Typical Requirement|
|----------|-------------------|
|Frequency deviation|± 0.5 Hz|
|Voltage ride-through|0.15-0.3 s at low V|
|Power factor|0.90 lagging to leading|
|THD|< 5%|

---

## Common Errors to Avoid

1. **Ignoring per-unit system** — Always use consistent base
2. **Confusing delta-wye** — Important for transformers
3. **Not checking convergence** — Load flow may not converge
4. **Ignoring fault impedance** — Real systems have Z_f > 0
5. **Wrong bus classification** — Must specify correctly
6. **Neglecting stability limits** — Operating limits matter
7. **Ignoring power factor** — Affects reactive power
8. **Not considering contingencies** — N-1 reliability

