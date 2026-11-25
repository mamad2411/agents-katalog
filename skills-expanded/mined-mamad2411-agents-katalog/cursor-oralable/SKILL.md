# Oralable MAM AI Agent Instructions

## 1. Project Context
- **Device:** Oralable MAM (PPG + Accelerometer).
- **Location:** Cheek (Masseter Muscle).
- **Primary Goal:** Detect Sleep Bruxism (Clenching/Grinding) via Hemodynamic Occlusion.
- **Vitals:** Heart Rate (Green), SpO2 (Red/IR), HRV for Sleep Staging.

## 2. Signal Processing Rules
- **Sampling Rate:** All final data MUST be resampled to exactly 50Hz (20ms intervals) using linear interpolation.
- **PPG Filtering:** Use a Butterworth bandpass (0.5-8.0 Hz) for heart rate. Use a Low-pass (<1 Hz) to extract the DC-shift (Muscle Occlusion).
- **Accelerometer:** Primary use is actigraphy and jaw vibration detection (sampling up to 100Hz, but sync with 50Hz PPG).

## 3. Reference Standards
- Follow **Peter Charlton's** Pulse Waveform Analysis (PWA) for arterial stiffness and HRV.
- Implement **Zhang et al. (2023) PPG-Net 4** morphology for classifying blood flow (Laminar, Stagnant, Turbulent).
- Use **Attia et al. (2024)** standards for 50Hz sleep staging accuracy.

## 4. Coding Constraints (Python & Swift)
- **Python:** Use Pandas for time-series. Always verify Signal-to-Noise Ratio (SNR) after filtering.
- **Swift/iOS:** Prepare models for **Core ML**. Use circular buffers (100 samples) to handle real-time 50Hz streams.
- **Validation:** Every clench detection algorithm must be cross-verified against the DC-trough depth in the IR channel.

## 5. Default Cheek Coupling Config
- **PPG channel order:** R_G_IR (Red, Green, IR) — use when BLE slot1 is constant.
- **IR-DC coupling range:** 10M–70M raw (32-bit firmware). See `docs/IR_DC_ADC_FORMAT.md`.
- **Run** `scripts/check_ir_dc_scaling.py` on new logs to verify.

## 6. Agent Workflow
- **Plan Mode:** When I ask for a new feature, first research the `src/` directory and propose a plan in Markdown.
- **Verification:** Always check for 'Baseline Wander' when calculating SpO2.
- **Sync:** When processing logs, look for 3 consecutive high-G spikes in the Accelerometer (Sync Taps) to anchor the start time.

## 7. Firmware & nRF Connect
- **Any firmware change** (`oralable_nrf/`) must be validated against **nRF Connect** before it is considered complete.
- Firmware GATT/BLE behavior must stay **compatible with what nRF Connect expects** (service/characteristic UUIDs, read sizes, notify payloads, stable connection after CCC enable).
- Use **nRF Connect log exports** (CSV: `Timestamp, Source, Level, Line`) as the primary debug artifact: decode hex reads, note disconnect timing relative to the last CCC/read, and map findings to the next firmware fix.
- See `oralable_nrf/.cursor/rules/nrf-connect-validation.mdc` for the full checklist.