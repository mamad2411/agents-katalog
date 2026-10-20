---

## name: biomedical-engineering
description: >
  Expert biomedical engineering assistant for engineers, medical professionals, and researchers. Use this skill whenever the user needs:
  designing medical devices, modeling physiological systems, developing imaging systems, creating prosthetics, analyzing biosignals,
  or any rigorous academic treatment of biomedical engineering. Covers device design, biomechanics, and regulatory compliance.
license: MIT
compatibility: opencode
metadata:
  audience: engineers, medical professionals, researchers
  category: engineering

# Biomedical Engineering — Academic Research Assistant

Covers: **Medical Device Design · Biomechanics · Biosignal Processing · Biomedical Imaging · Prosthetics · Tissue Engineering · Regulatory Affairs**

---

## Medical Device Design

### Design Control Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN CONTROLS                               │
├─────────────────────────────────────────────────────────────────┤
│  1. Design Input → 2. Design Output → 3. Design Review         │
│         ↓                    ↓                    ↓            │
│  4. Design Verification → 5. Design Validation               │
│         ↓                                                     │
│  6. Design Transfer → 7. Design History File                  │
└─────────────────────────────────────────────────────────────────┘
```

### Biocompatibility Testing (ISO 10993)

|Test|Biological Effect|Test Method|
|-----|-----------------|-----------|
|Cytotoxicity|Cell death|In vitro cell culture|
|Sensitization|Allergic response|Guinea pig maximization|
|Irritation|Local irritation|rabbit skin test|
|Systemic toxicity|Whole body effects|Acute toxicity study|
|Implant implantation|Tissue response|Subcutaneous implant|

```python
class BiocompatibilityAssessment:
    """Biomaterial evaluation"""
    
    # Common implant materials
    IMPLANT_MATERIALS = {
        "titanium": {
            "biocompatible": True,
            "corrosion_resistance": "Excellent",
            "osseointegration": "Good",
            "modulus_gpa": 110,
            "applications": ["Orthopedic implants", "Dental implants"]
        },
        "stainless_steel_316L": {
            "biocompatible": True,
            "corrosion_resistance": "Good",
            "modulus_gpa": 200,
            "applications": ["Temporary implants", "Vascular stents"]
        },
        "cobalt_chromium": {
            "biocompatible": True,
            "corrosion_resistance": "Excellent",
            "modulus_gpa": 240,
            "applications": ["Joint replacements", "Heart valves"]
        },
        "peek": {
            "biocompatible": True,
            "corrosion_resistance": "Excellent",
            "modulus_gpa": 3.6,
            "applications": ["Spinal implants", "Cranial"]
        },
        "silicone": {
            "biocompatible": True,
            "corrosion_resistance": "Excellent",
            "modulus_gpa": 0.001,
            "applications": ["Breast implants", "Catheters"]
        }
    }
    
    def select_material(self, requirements):
        """
        Select appropriate implant material
        based on mechanical and biological requirements
        """
        candidates = []
        
        for material, properties in self.IMPLANT_MATERIALS.items():
            match = True
            for req, value in requirements.items():
                if properties.get(req) != value:
                    match = False
                    break
            
            if match:
                candidates.append(material)
        
        return candidates
```

---

## Biomechanics

### Joint Mechanics

|Joint|Motion|Plane|Flexion (°)|Extension (°)|
|-----|-------|-----|-----------|-------------|
|Elbow|Flexion/Extension|Sagittal|0-150|150-0|
|Shoulder|Flexion/Extension|Sagittal|0-180|180-0|
|Hip|Flexion/Extension|Sagittal|0-120|120-0|
|Knee|Flexion/Extension|Sagittal|0-135|135-0|

```python
class Biomechanics:
    """Biomechanical analysis"""
    
    # Inverse kinematics
    def calculate_joint_angles(self, end_effector_pos, segment_lengths):
        """
        Calculate joint angles for planar mechanism
        Using Law of Cosines
        """
        import numpy as np
        
        # Two-link planar arm
        L1, L2 = segment_lengths
        x, y = end_effector_pos
        
        # Elbow angle
        cos_elbow = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
        elbow_angle = np.arccos(np.clip(cos_elbow, -1, 1))
        
        # Shoulder angle
        k1 = L1 + L2 * np.cos(elbow_angle)
        k2 = L2 * np.sin(elbow_angle)
        shoulder_angle = np.arctan2(y, x) - np.arctan2(k2, k1)
        
        return {"shoulder": shoulder_angle, "elbow": elbow_angle}
    
    # Inverse dynamics
    def calculate_joint_torque(self, force, moment_arm):
        """τ = r × F"""
        return force * moment_arm
    
    def impact_analysis(self, mass, velocity, contact_time):
        """
        Impact force calculation
        """
        impulse = mass * velocity
        force_peak = impulse / contact_time
        
        return {
            "impulse_Ns": impulse,
            "peak_force_N": force_peak,
            "impulse_Ns": impulse
        }
```

### Gait Analysis

```python
class GaitAnalysis:
    """Gait cycle analysis"""
    
    # Gait phases
    PHASES = {
        "stance": {
            "duration": "60% of cycle",
            "subphases": ["Initial contact", "Loading response", 
                         "Mid stance", "Terminal stance", 
                         "Pre-swing"]
        },
        "swing": {
            "duration": "40% of cycle",
            "subphases": ["Initial swing", "Mid swing", "Terminal swing"]
        }
    }
    
    # Normal gait parameters
    NORMAL_VALUES = {
        "cadence": "90-120 steps/min",
        "step_length": "0.6-0.8 m",
        "stride_length": "1.2-1.6 m",
        "walking_speed": "1.2-1.5 m/s"
    }
```

---

## Biosignal Processing

### Filter Design

```python
class BiosignalFilters:
    """Signal processing for biomedical signals"""
    
    def design_ecg_filter(self, fs):
        """
        Design ECG processing filters
        """
        from scipy import signal
        
        # Powerline interference removal (60 Hz)
        b_notch, a_notch = signal.iirnotch(60, 30, fs)
        
        # Baseline wander removal (high-pass, 0.5 Hz)
        b_hp, a_hp = signal.butter(4, 0.5, btype='high', fs=fs)
        
        # Muscle artifact removal (low-pass, 40 Hz)
        b_lp, a_lp = signal.butter(4, 40, btype='low', fs=fs)
        
        return {
            "notch": (b_notch, a_notch),
            "highpass": (b_hp, a_hp),
            "lowpass": (b_lp, a_lp)
        }
    
    def detect_peaks(self, signal_data, threshold):
        """
        R-peak detection for ECG
        """
        import numpy as np
        
        # Simple threshold detection
        peaks = []
        for i in range(1, len(signal_data) - 1):
            if (signal_data[i] > signal_data[i-1] and 
                signal_data[i] > signal_data[i+1] and
                signal_data[i] > threshold):
                peaks.append(i)
        
        return peaks
```

---

## Prosthetic Design

### Lower Limb Prosthetics

|Component|Function|Types|
|---------|--------|-----|
|Socket|Interface|Molded, modular|
|Knee|Weight-bearing, swing|Criteria, polycentric, microprocessor|
|Ankle|Foot motion|Fixed, dynamic, energy storing|
|Adapter|Connection|Rotator, pyramid|

```python
class ProstheticDesign:
    """Prosthetic component selection"""
    
    def select_knee(self, activity_level, weight):
        """
        Knee selection based on patient factors
        """
        recommendations = {
            "K0": {"type": "Fixed", "description": "Limited mobility"},
            "K1": {"type": "Single-axis", "description": "Limited community ambulator"},
            "K2": {"type": "Single-axis with stance control", 
                   "description": "Community ambulator with variable cadence"},
            "K3": {"type": "Microprocessor", 
                   "description": "Community ambulator with variable cadence"},
            "K4": {"type": "High-activity microprocessor",
                   "description": "High impact activities"}
        }
        
        return recommendations.get(activity_level, "Consult specialist")
    
    def calculate_alignment(self, socket_pos, foot_pos, shank_length):
        """
        Prosthetic alignment parameters
        """
        # Sagittal plane alignment
        pfp = socket_pos  # Proximal fitting point
        dfp = foot_pos   # Distal fitting point
        
        # Socket angle
        socket_angle = 0  # Typically 5-10 degrees flexion
        
        # Fore-aft alignment
        mcp = pfp[1]  # Medial compartment position
        
        return {"socket_angle": socket_angle}
```

---

## Regulatory Framework

### FDA Pathways

|Pathway|Timeline|Typical Use|
|-------|---------|-----------|
|510(k)|6-12 months|Legally marketed predicate|
|PMA|12-36 months|Novel Class III devices|
|De Novo|6-12 months|Novel, low-moderate risk|
|EUA|Emergency|COVID-19 type|

```python
class RegulatoryRequirements:
    """Regulatory guidance"""
    
    # US FDA - 21 CFR Part 820
    QSR_REQUIREMENTS = {
        "820.30": "Design Controls",
        "820.50": "Purchasing Controls", 
        "820.70": "Production and Process Controls",
        "820.90": "Nonconforming Product",
        "820.100": "CAPA",
        "820.200": "Complaint Handling",
        "820.250": "Statistical Techniques"
    }
    
    # EU MDR 2017/745
    MDR_CLASSES = {
        "Class I": "Low risk",
        "Class IIa": "Medium-low risk",
        "Class IIb": "Medium-high risk",
        "Class III": "High risk"
    }
    
    # Quality management
    QM_STANDARDS = {
        "ISO 13485": "Medical devices QMS",
        "ISO 14971": "Risk management",
        "IEC 62304": "Software lifecycle",
        "IEC 62366": "Usability engineering",
        "ISO 10993": "Biocompatibility"
    }
```

---

## Common Errors to Avoid

1. **Skipping design controls** — Required for FDA compliance
2. **Ignoring usability testing** — IEC 62366 mandatory
3. **Inadequate risk analysis** — ISO 14971 not optional
4. **Wrong biocompatibility tests** — Use ISO 10993 correctly
5. **Ignoring sterilization** — Method affects material selection
6. **Poor software documentation** — IEC 62304 critical
7. **Not validating manufacturing** — Process validation needed
8. **Forgetting post-market surveillance** — Ongoing requirement

