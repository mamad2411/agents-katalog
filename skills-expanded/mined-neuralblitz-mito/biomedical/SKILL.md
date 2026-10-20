---

## name: biomedical
description: >
  Expert biomedical assistant for healthcare professionals, engineers, and researchers. Use this skill whenever the user needs:
  understanding biomedical concepts, medical devices, biological signals, healthcare technology, medical terminology,
  or any rigorous academic treatment of biomedical science. Covers vital signs, medical devices, and health data standards.
license: MIT
compatibility: opencode
metadata:
  audience: healthcare professionals, engineers, students
  category: engineering

# Biomedical — Academic Research Assistant

Covers: **Vital Signs · Biological Signals · Medical Devices · Healthcare Data Standards · Clinical Measurements · Biomedical Instrumentation**

---

## Vital Signs

### Normal Ranges by Age

|Age|HR (bpm)|RR (breaths/min)|SBP (mmHg)|Temp (°C)|
|---|---------|-----------------|----------|----------|
|Newborn (0-1m)|100-180|30-60|60-90|36.5-37.5|
|Infant (1-12m)|80-120|20-40|70-100|36.5-37.5|
|Toddler (1-3y)|80-130|20-30|90-110|36.5-37.5|
|Child (3-12y)|70-110|15-25|95-120|36.5-37.5|
|Adult|60-100|12-20|90-120|36.5-37.5|
|Geriatric|60-100|12-20|90-140|36.0-37.5|

### Blood Pressure Classification

|Category|Systolic (mmHg)|Diastolic (mmHg)|
|--------|---------------|-----------------|
|Normal|<120|<80|
|Elevated|120-129|<80|
|Stage 1 HTN|130-139|80-89|
|Stage 2 HTN|≥140|≥90|
|Hypertensive Crisis|>180|>120|

---

## Biological Signals

### Electrocardiogram (ECG)

```python
class ECGAnalysis:
    """ECG signal processing"""
    
    # Wave components
    WAVES = {
        "P": {"duration": "0.08-0.10s", "amplitude": "0.1-0.2 mV"},
        "QRS": {"duration": "0.06-0.10s", "amplitude": "1.0-2.0 mV"},
        "T": {"duration": "0.10-0.25s", "amplitude": "0.1-0.3 mV"},
        "U": {"duration": "0.16-0.24s", "amplitude": "0.05-0.2 mV"}
    }
    
    # Heart rate calculation
    def calculate_heart_rate(self, rr_interval_ms):
        """Calculate BPM from RR interval"""
        return 60000 / rr_interval_ms
    
    # Rhythm analysis
    def analyze_rhythm(self, rr_intervals):
        """
        HRV metrics
        - SDNN: Standard deviation of NN intervals
        - RMSSD: Root mean square of successive differences
        - pNN50: % of successive intervals > 50ms
        """
        import numpy as np
        
        # RMSSD
        successive_diffs = np.diff(rr_intervals)
        rmssd = np.sqrt(np.mean(successive_diffs ** 2))
        
        # pNN50
        nn50 = sum(1 for d in successive_diffs if abs(d) > 50)
        pnn50 = (nn50 / len(successive_diffs)) * 100 if len(successive_diffs) > 0 else 0
        
        return {"RMSSD": rmssd, "pNN50": pnn50}
    
    # QRS detection
    def detect_qrs(self, ecg_signal, fs):
        """
        Pan-Tompkins algorithm
        1. Bandpass filter (5-15 Hz)
        2. Differentiate
        3. Square
        4. Moving window integrate
        5. Adaptive threshold
        """
        pass
```

### Electroencephalogram (EEG)

|Band|Frequency|Associated State|
|-----|----------|-----------------|
|Delta|0.5-4 Hz|Deep sleep|
|Theta|4-8 Hz|Light sleep, meditation|
|Alpha|8-12 Hz|Rest, eyes closed|
|Beta|12-30 Hz|Active thinking|
|Gamma|30-100 Hz|High-level processing|

### Electromyogram (EMG)

```python
class EMGProcessing:
    """EMG signal analysis"""
    
    def rect_filter(self, emg_signal, fs):
        """
        Process EMG:
        1. Bandpass filter (20-500 Hz)
        2. Full-wave rectification
        3. Moving average (smoothing)
        """
        pass
    
    def calculate_mav(self, emg_segment):
        """Mean Absolute Value"""
        return sum(abs(x) for x in emg_segment) / len(emg_segment)
    
    def calculate_rms(self, emg_segment):
        """Root Mean Square"""
        import numpy as np
        return np.sqrt(sum(x**2 for x in emg_segment) / len(emg_segment))
    
    def calculate_fatigue(self, emg_segment1, emg_segment2):
        """
        Detect fatigue via frequency shift
        - Median frequency decreases with fatigue
        """
        import numpy as np
        
        freq1 = np.median(np.abs(np.fft.rfft(emg_segment1)))
        freq2 = np.median(np.abs(np.fft.rfft(emg_segment2)))
        
        return freq2 < freq1  # True if fatigue detected
```

---

## Medical Devices

### Device Classification (FDA)

|Class|Risk|Examples|Requirements|
|-----|-----|--------|-------------|
|I|Low|Bandages, stethoscopes|General controls|
|II|Medium|Infection pumps, monitors|510(k) clearance|
|III|High|Pacemakers, heart valves|PMA required|
|IVD (in vitro)|Varies|Glucose meters|Registration|

### Device Categories

|Device|Function|Monitoring Parameters|
|------|--------|---------------------|
|Pulse oximetry|SpO₂ measurement|SpO₂, PR|
|ECG monitor|Heart rhythm|HR, rhythm, ST|
|Sphygmomanometer|Blood pressure|SBP, DBP, MAP|
|Spirometer|Lung function|FVC, FEV₁|
|Glucose meter|Blood glucose|Blood glucose|
|Defibrillator|Cardiac arrest|Energy delivery|

---

## Healthcare Data Standards

### HL7 FHIR Resources

|Resource|Purpose|
|--------|-------|
|Patient|Demographics, identifiers|
|Observation|Vital signs, lab results|
|MedicationRequest|Prescription orders|
|Condition|Diagnoses, problems|
|Encounter|Clinical visits|
|DiagnosticReport|Lab/imaging results|

### DICOM

```python
class DICOMHandler:
    """DICOM file handling"""
    
    # Important tags
    IMPORTANT_TAGS = {
        "0010,0010": "Patient Name",
        "0010,0020": "Patient ID",
        "0008,0060": "Modality",
        "0020,000D": "Study Instance UID",
        "0008,1030": "Study Description",
        "0028,0010": "Rows (image height)",
        "0028,0011": "Columns (image width)",
        "0028,0100": "Bits Allocated",
        "0028,0101": "Bits Stored"
    }
    
    def load_dicom(self, filepath):
        """Load DICOM file"""
        import pydicom
        
        ds = pydicom.dcmread(filepath)
        
        return {
            "patient": ds.PatientName,
            "modality": ds.Modality,
            "rows": ds.Rows,
            "columns": ds.Columns,
            "pixel_data": ds.pixel_array
        }
    
    def window_level(self, image, window, level):
        """
        Apply window/level for viewing
        """
        import numpy as np
        
        lower = level - window / 2
        upper = level + window / 2
        
        return np.clip((image - lower) / (upper - lower), 0, 1)
```

### Medical Terminology

|System|Content|Use Case|
|-------|--------|--------|
|SNOMED CT|Clinical terms|Documentation|
|ICD-10|Disease codes|Billing, statistics|
|LOINC|Lab results|Interoperability|
|RxNorm|Medications|e-Prescribing|

---

## Biomedical Instrumentation

### Amplifier Requirements

|Parameter|Typical Value|Notes|
|---------|--------------|-----|
|Input impedance|>10 MΩ|High to minimize loading|
|Gain|100-10000|Depends on signal|
|Bandwidth|0.05-100 Hz (ECG)|Signal-specific|
|CMRR|>80 dB|Reject common noise|
|Noise|<10 μV|Depends on application|

### Safety Standards

|Standard|Scope|
|--------|------|
|IEC 60601-1|Medical electrical equipment safety|
|IEC 60601-1-2|EMC requirements|
|IEC 60601-1-4|Software|
|IEC 62366|Usability|

---

## Common Errors to Avoid

1. **Ignoring electrode placement** — Standard 12-lead ECG positions critical
2. **Not filtering properly** — Wrong filters distort signals
3. **Confusing correlation with causation** — Signals show association
4. **Ignoring artifact contamination** — Motion, electrical noise
5. **Using wrong device class** — Regulatory implications
6. **Not considering biocompatibility** — Material-tissue interactions
7. **Ignoring calibration** — Regular calibration needed for accuracy
8. **Confusing device standards** — Different regions have different requirements

