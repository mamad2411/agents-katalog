---

## name: analytical
description: >
  Expert analytical chemistry assistant for scientists and researchers. Use this skill whenever the user needs:
  understanding analytical techniques, quantitative analysis, method validation, quality assurance, or any rigorous academic 
  treatment of analytical chemistry. Covers spectroscopy, chromatography, electrochemistry, and data analysis.
license: MIT
compatibility: opencode
metadata:
  audience: scientists, analysts, researchers
  category: chemistry

# Analytical Chemistry — Academic Research Assistant

Covers: **Spectroscopy · Chromatography · Electrochemistry · Method Validation · Quality Assurance · Statistical Analysis · Sample Preparation**

---

## Analytical Workflow

### Steps in Analysis

```
1. Problem Definition
   └─> What needs to be measured?

2. Method Selection
   └─> Choose appropriate technique

3. Sampling
   └─> Representative sample collection

4. Sample Preparation
   └─> Extraction, digestion, cleanup

5. Measurement
   └─> Instrumental analysis

6. Data Analysis
   └─> Calibration, calculations

7. Reporting
   └─> Results, uncertainty, conclusions
```

---

## Spectroscopy

### Electromagnetic Spectrum

|Region|Wavelength|Energy|Transitions|
|------|----------|------|-----------|
|UV-C|100-280 nm|High|Valence electrons|
|UV-Vis|280-700 nm|Medium|Valence, d-d|
|IR|0.7-1000 μm|Vibrational|Molecular bonds|
|Microwave|1-1000 mm|Rotational|Rotation|
|Radio|<1 m|Nuclear spin|NMR|

```python
class SpectroscopicAnalysis:
    """Spectroscopy calculations"""
    
    # Beer-Lambert Law
    def beer_lambert(self, absorbance, path_length, concentration):
        """
        A = ε × b × c
        A = absorbance
        ε = molar absorptivity (L/mol·cm)
        b = path length (cm)
        c = concentration (mol/L)
        """
        return absorbance / (path_length * concentration)
    
    def concentration_from_absorbance(self, A, epsilon, b):
        """
        c = A / (ε × b)
        """
        return A / (epsilon * b)
    
    def multiple_wavelength(self, wavelengths, absorbances):
        """
        Simultaneous determination (multi-component)
        [A] = ε⁻¹ × A_total
        """
        pass
```

### Atomic Spectroscopy

|Technique|Atomization|Detection|Application|
|---------|------------|----------|-----------|
|AAS|Flame/Graphite|Furnace trace metals|
|ICP-OES|Plasma|Optical emission|Multi-element|
|ICP-MS|Plasma|Mass spectrometry|Ultra-trace|
|AFS|Furnace|Fluorescence|Mercury, arsenic|

---

## Chromatography

### Column Chromatography

```python
class ChromatographicAnalysis:
    """Chromatography calculations"""
    
    def retention_factor(self, t_r, t_0):
        """
        k' = (t_R - t_0) / t_0
        
        t_R = retention time
        t_0 = dead time
        """
        return (t_r - t_0) / t_0
    
    def selectivity_factor(self, k1, k2):
        """
        α = k2 / k1 (for k2 > k1)
        """
        return k2 / k1
    
    def number_of_theoretical_plates(self, t_r, w):
        """
        N = 16 × (t_R/w)²
        
        w = peak width at baseline
        """
        return 16 * (t_r / w) ** 2
    
    def resolution(self, t_r1, t_r2, w1, w2):
        """
        R_s = 2(t_R2 - t_R1)/(w1 + w2)
        
        R_s < 1: Overlapping
        R_s = 1: Partially resolved  
        R_s > 1.5: Baseline resolved
        """
        return 2 * (t_r2 - t_r1) / (w1 + w2)
    
    def plate_height(self, L, N):
        """
        H = L / N
        """
        return L / N
```

### HPLC Parameters

|Parameter|Typical Range|
|---------|--------------|
|Backpressure|1000-3000 psi|
|Flow rate|0.1-2.0 mL/min|
|Column temperature|25-40°C|
|Injection volume|1-100 μL|

---

## Electrochemistry

### Electroanalytical Methods

|Method|Measurement|Application|
|------|-----------|------------|
|Potentiometry|Potential (Nernst)|pH, ions|
|Coulometry|Charge (Faraday)|Quantitative|
|Voltammetry|Current vs. potential|Kinetics, mechanism|
|Amperometry|Current at fixed potential|Biosensors|

```python
class ElectrochemicalAnalysis:
    """Electrochemistry calculations"""
    
    # Nernst equation
    def nernst_potential(self, E0, R, T, n, activities):
        """
        E = E₀ + (RT/nF) × ln(Q)
        at 25°C: E = E₀ + (0.0592/n) × log(Q)
        """
        import numpy as np
        
        R = 8.314  # J/mol·K
        T = 298.15  # K
        F = 96485   # C/mol
        
        return E0 + (R * T / (n * F)) * np.log(activities)
    
    # Faraday's laws
    def coulomb_to_moles(self, charge, n):
        """
        n = Q / (n × F)
        
        n = moles of electrons
        n = electrons per reaction
        F = Faraday constant
        """
        return charge / (n * 96485)
```

---

## Method Validation

### Validation Parameters

|Parameter|Definition|Acceptable Criteria|
|---------|-----------|-------------------|
|Accuracy|Closeness to true value|95-105% recovery|
|Precision|Repeatability|RSD < 1-3% (instruments), < 5% (methods)|
|Linearity|Correlation coefficient|R² > 0.99|
|LOD|Signal > blank + 3σ|S/N ≥ 3|
|LOQ|Signal > blank + 10σ|S/N ≥ 10|
|Specificity|No interference|Must demonstrate|
|Robustness|Tolerance to changes|Identify critical parameters|

```python
class MethodValidation:
    """Method validation calculations"""
    
    def limit_of_detection(self, blank_measurements, slope):
        """
        LOD = 3 × σ_blank / slope
        """
        import numpy as np
        
        sigma = np.std(blank_measurements)
        lod = 3 * sigma / slope
        
        return lod
    
    def limit_of_quantitation(self, blank_measurements, slope):
        """
        LOQ = 10 × σ_blank / slope
        """
        import numpy as np
        
        sigma = np.std(blank_measurements)
        loq = 10 * sigma / slope
        
        return loq
    
    def recovery(self, measured, spiked, blank):
        """
        Recovery = (measured - blank) / spiked × 100%
        """
        return (measured - blank) / spiked * 100
```

---

## Statistical Analysis

### Error Analysis

```python
class StatisticalAnalysis:
    """Statistical calculations"""
    
    def confidence_interval(self, values, confidence=0.95):
        """
        CI = x̄ ± t × s / √n
        
        t = t-statistic
        s = standard deviation
        n = number of measurements
        """
        import numpy as np
        from scipy import stats
        
        mean = np.mean(values)
        n = len(values)
        s = np.std(values, ddof=1)
        
        t_value = stats.t.ppf((1 + confidence) / 2, n - 1)
        
        margin = t_value * s / np.sqrt(n)
        
        return mean - margin, mean + margin
    
    def outlier_test(self, values, method='grubbs'):
        """
        Grubbs' test for outliers
        """
        import numpy as np
        from scipy import stats
        
        n = len(values)
        mean = np.mean(values)
        s = np.std(values, ddof=1)
        
        G = max(abs(values - mean)) / s
        
        t = stats.t.ppf(0.975, n - 2)
        G_critical = ((n - 1) / np.sqrt(n)) * np.sqrt(t**2 / (n - 2 + t**2))
        
        return G > G_critical
    
    def linear_regression(self, x, y):
        """
        y = mx + b with statistics
        """
        import numpy as np
        from scipy import stats
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_value ** 2,
            "p_value": p_value,
            "standard_error": std_err
        }
```

---

## Quality Assurance

### Quality Control Charts

|Chart|Type|Application|
|-----|----|-----------|
|X-bar chart|Mean|Process location|
|R chart|Range|Process variation|
|S chart|Standard deviation|Larger samples|
|p chart|Proportion|Defectives|
|c chart|Count|Defects|

### Reference Materials

|Standard|Use|
|---------|---|
|CRM (Certified)|Primary calibration|
|Reference|Method validation|
|Working|Daily QC|
|Internal|Spike recovery|

---

## Sample Preparation

### Techniques

|Technique|Application|
|---------|-----------|
|Extraction (LLE)|Liquid-liquid|
|SPE|Solid-phase extraction|
|Soxhlet|Solid extraction|
|Microwave digestion|Dissolution|
|Derivatization|Volatilization|

---

## Common Errors to Avoid

1. **Ignoring uncertainty** — Always quantify measurement uncertainty
2. **Inadequate calibration** — Use appropriate standards
3. **Not validating methods** — Follow validation protocols
4. **Ignoring matrix effects** — Matrix-matched standards
5. **Confusing precision with accuracy** — Different concepts
6. **Insufficient replicates** — Need statistical power
7. **Ignoring detection limits** — Report appropriately
8. **Poor documentation** — GLP requires complete records

