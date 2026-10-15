---
name: mne-python
description: MNE-Python for MEG/EEG/iEEG/fNIRS analysis pipelines, from loading raw signals to epoching, preprocessing, time-frequency analysis, inverse modeling, and reporting. Use when working with mne.create_info, mne.io.RawArray, mne.Epochs, mne.compute_covariance, mne.preprocessing.ICA, mne.time_frequency.psd_array_welch, mne.make_sphere_model, mne.Report, sensor/source-space workflows, or electrophysiology quality control.
---

# MNE-Python

MNE-Python is a scientific Python toolkit for electrophysiology analysis (MEG, EEG, iEEG, fNIRS), covering data structures, preprocessing, spectral analysis, source modeling, and visualization.

## Version

Built against: `mne==1.11.0`
Python: `3.13.5`
> If using a different version, check `assets/version.txt` and consult `doc/changes/v1.11.rst` for API differences.

## Scope

This skill is intentionally scoped to common workflows for day-to-day analysis:
- Included: `mne.io`, `mne.epochs`, `mne.preprocessing`, `mne.time_frequency`, `mne.viz`, `mne.report`, basic forward/inverse setup.
- Out of scope: exhaustive coverage of all format-specific readers, every dataset helper, all advanced beamformer/minimum-norm variants, and low-level internals under `mne._fiff` / `mne.commands`.

## Coverage Profile

Coverage profile is `hybrid`:
- Workflow coverage: curated day-to-day analysis paths in `references/*.md`.
- Dictionary coverage: broad symbol lookup assets for API discovery without opening source files first.

Dictionary assets:
- `assets/symbol-index.md`
- `assets/symbol-index.jsonl`
- `assets/symbol-cards/`

## Installation

```bash
pip install mne

# optional but commonly needed for decoding / ICA workflows
pip install scikit-learn
```

---

## Data Containers and I/O

```python
import numpy as np
import mne

# tested against mne==1.11.0
info = mne.create_info(["Fz", "Cz"], sfreq=100.0, ch_types="eeg")
raw = mne.io.RawArray(np.random.randn(2, 300), info)
print(raw.get_data().shape)
```

See `references/data-containers-and-io.md` for signatures, parameter details, and shape conventions.

---

## Events, Epochs, and Evoked

```python
import numpy as np
import mne

# tested against mne==1.11.0
info = mne.create_info(["EEG 001"], sfreq=100.0, ch_types="eeg")
raw = mne.io.RawArray(np.random.randn(1, 1000), info)
events = mne.make_fixed_length_events(raw, duration=0.5)
epochs = mne.Epochs(raw, events, event_id={"stim": 1}, tmin=0.0, tmax=0.2, baseline=None, preload=True, verbose=False)
print(len(epochs))
```

See `references/events-epochs-and-evoked.md` for event construction and epoching pitfalls.

---

## Preprocessing and Artifacts

```python
import mne

# tested against mne==1.11.0
ica = mne.preprocessing.ICA(n_components=2, method="fastica", random_state=0)
print(ica.method)
```

See `references/preprocessing-and-artifacts.md` for covariance estimation and ICA usage notes.

---

## Spectral and Time-Frequency

```python
import numpy as np
import mne

# tested against mne==1.11.0
sfreq = 200.0
t = np.arange(0, 2, 1 / sfreq)
signal = np.sin(2 * np.pi * 10 * t)
psd, freqs = mne.time_frequency.psd_array_welch(signal, sfreq=sfreq, fmin=1, fmax=40)
print(psd.shape[0], round(float(freqs[psd.argmax()]), 1))
```

See `references/spectral-and-time-frequency.md` for Welch parameters and PSD workflow patterns.

---

## Forward, Inverse, and Source Basics

```python
import mne

# tested against mne==1.11.0
sphere = mne.make_sphere_model(head_radius=0.09)
print(type(sphere).__name__)
```

See `references/forward-inverse-and-source.md` for sphere/BEM context and covariance setup.

---

## Visualization and Reporting

```python
import mne

# tested against mne==1.11.0
report = mne.Report(title="Synthetic QC")
report.add_html("<p>ok</p>", title="status")
print(len(report))
```

See `references/visualization-and-reporting.md` for report and plotting patterns.

---

## Verification (Medium+)

```bash
python .opencode/skills/opensci-skill/scripts/verify-snippets.py --root .opencode/skills/mne-python --fail-fast
```

## API Dictionary (Dictionary/Hybrid)

- `assets/symbol-index.md` - Module-level symbol navigation for quick browsing.
- `assets/symbol-index.jsonl` - Machine-readable symbol lookup records.
- `assets/symbol-cards/` - Per-module symbol cards with signatures and anchors.

## Quick Reference

| Function / Class | Purpose |
|-----------------|---------|
| `mne.create_info()` | Build channel metadata used by all core containers. |
| `mne.io.RawArray()` | Wrap in-memory continuous data as Raw. |
| `mne.make_fixed_length_events()` | Create regular event markers for windowing. |
| `mne.Epochs()` | Segment continuous raw data into event-locked trials. |
| `mne.compute_covariance()` | Estimate noise/data covariance from epochs. |
| `mne.preprocessing.ICA()` | Configure ICA decomposition for artifact handling. |
| `mne.time_frequency.psd_array_welch()` | Compute PSD from arrays with Welch method. |
| `mne.make_sphere_model()` | Build simple head conductivity model. |
| `mne.Report()` | Build HTML QC/report artifacts. |

---

## Module Map

| Submodule | Contents | Notes |
|-----------|----------|-------|
| `mne.io` | Raw classes and format readers/writers | Core ingest path |
| `mne.preprocessing` | Artifact detection/correction, ICA, filtering helpers | High-use preprocessing APIs |
| `mne.time_frequency` | PSD/TFR/CSD estimators | Spectral workflows |
| `mne.viz` | Sensor/source plotting backends | Large surface area |
| `mne._fiff.meas_info` | Metadata internals (`Info`) | `[LARGE]` (>500 lines) |

Import style: lazy `__getattr__` + stub-driven `__all__` via `lazy_loader.attach_stub()`.

See `assets/module-map.md` for complete submodule inventory and large-module flags.

---

## References

- `references/data-containers-and-io.md` - Metadata creation, in-memory Raw objects, and shape contracts.
- `references/events-epochs-and-evoked.md` - Event generation, trial segmentation, and evoked averaging basics.
- `references/preprocessing-and-artifacts.md` - Covariance estimation and ICA setup for artifact workflows.
- `references/spectral-and-time-frequency.md` - Welch PSD and common spectral workflow patterns.
- `references/forward-inverse-and-source.md` - Sphere models, ad-hoc covariance, and source pipeline entry points.
- `references/visualization-and-reporting.md` - Report generation and quick visualization artifacts.
