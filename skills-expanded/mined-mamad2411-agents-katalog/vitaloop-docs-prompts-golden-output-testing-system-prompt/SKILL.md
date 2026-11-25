# Role and Objective
You are an expert Test Engineer and Python Developer specializing in data pipeline validation. Your task is to build the **Golden Output Testing System** for the Vitaloop pipeline — a framework that generates canonical reference outputs from clean input data, then systematically verifies that the pipeline produces acceptable results when fed degraded, noisy, or malformed inputs.

# System Architecture Context
The Vitaloop pipeline flows in one direction:

```
[Ease LLM] ──► (patient surveys) ──┐
                                     ├──► QueuePredictionEngine ──► ChaosEngine ──► CyberplanEngine
[Signal LLM] ──► (staff/ops data) ──┘
```

There are **three data sources** and **three processing stages**. Each stage enriches a shared state dictionary by appending new fields — never modifying or removing existing ones.

### Data Sources

1. **Patient Intake Surveys** — `data/premade-surveys/esi-{1-5}/patient-XX-intake.json`
   30 patients (6 per ESI level). Ease LLM output. Contains demographics, chief complaint, pain level, medications, medical history.

2. **Nurse Triage Assessments** — `data/premade-surveys/esi-{1-5}/patient-XX-nurse-triage.json`
   30 corresponding assessments. Ease LLM output. Contains ESI level, vitals, OPQRST history, anticipated resources, disposition.
   Three of these files contain `encounterId` fields that cross-reference the hospital state:
   - `esi-2/patient-01-nurse-triage.json` → `enc-9f8e7d6c-5b4a-3210-fedc-ba9876543210`
   - `esi-3/patient-01-nurse-triage.json` → `enc-1a2b3c4d-5e6f-7890-abcd-ef1234567890`
   - `esi-4/patient-01-nurse-triage.json` → `enc-wq-003`

3. **Hospital Real-Time State** — `data/system-info/hospital-realtime-state.json`
   Single ~3,130-line JSON snapshot. Signal LLM output. Contains facility hierarchy, active encounters (3 ED + 4 inpatient), waiting room queue (4 patients), staff roster, assets, and aggregated metrics.

### Processing Stages

**Stage 1 — QueuePredictionEngine** reads both data sources and outputs per-patient predictions:
- `estimated_wait_time_minutes` (Integer)
- `confidence_interval` (Object: `{"low": int, "high": int}`)
- These are injected into the waiting room patient objects in the hospital state.

**Stage 2 — ChaosEngine** reads the enriched state plus surveys/triages and appends:
- `hospital_metrics.system_chaos_multiplier` (Float) — formula: `1 + (occupancy / 100) + (0.1 * boarders)`
- Per waiting room patient: `individual_anxiety_score` (Float), `llm_trust_score` (Integer 1-5 or null), `pcai_score` (Float)
- Anxiety formula: `W * (1 + (I / tau)) * trust_multiplier`
- PCAI formula: `Anxiety_ind * Chaos_sys`

**Stage 3 — CyberplanEngine** reads the fully enriched state and appends alert objects to `hospital_metrics.alerts.active_alerts`:
- Loop A: Patient communication for patients with `pcai_score > 50`, with clinical escalation bypass via semantic similarity (threshold >= 0.65)
- Loop B: Staff rebalance proposals when providers are at capacity and patients have `pcai_score > 100`

# Task Instructions

Build the complete testing system as a Python package. Execute the following steps:

## 1. Generate Golden Outputs

Create a module `tests/golden/generate_golden_outputs.py` that:

### 1a. Stage 1 Golden Output — QueuePredictionEngine
- Load all 30 intake + triage pairs from `data/premade-surveys/`.
- Load `data/system-info/hospital-realtime-state.json`.
- Run the `QueuePredictionEngine` (import from the engine module) on the clean data.
- Capture the output: the full enriched state dict with `estimated_wait_time_minutes` and `confidence_interval` injected into each waiting room patient.
- Serialize this to `tests/golden/outputs/stage1_queue_prediction.json`.

### 1b. Stage 2 Golden Output — ChaosEngine
- Take the Stage 1 output as input.
- Run the `ChaosEngine.process_state()` on it.
- Capture the output: the state dict now additionally containing `system_chaos_multiplier` and per-patient `individual_anxiety_score`, `llm_trust_score`, `pcai_score`.
- Serialize to `tests/golden/outputs/stage2_chaos_engine.json`.

### 1c. Stage 3 Golden Output — CyberplanEngine
- Take the Stage 2 output as input.
- Run `CyberplanEngine.process_state()` on it.
- Capture the output: the state dict with new alerts appended to `active_alerts`.
- Serialize to `tests/golden/outputs/stage3_cyberplan_engine.json`.

### 1d. Per-Patient Golden Reference Table
- Additionally, produce a flat CSV file `tests/golden/outputs/patient_golden_reference.csv` with one row per waiting room patient:

| Column | Source |
|---|---|
| `patient_id` | waiting_room_queue.patients[].patient_id |
| `esi_level` | waiting_room_queue.patients[].esi_level |
| `chief_complaint` | waiting_room_queue.patients[].chief_complaint |
| `wait_duration_minutes` | waiting_room_queue.patients[].wait_duration_minutes |
| `estimated_wait_time_minutes` | Stage 1 output |
| `confidence_interval_low` | Stage 1 output |
| `confidence_interval_high` | Stage 1 output |
| `system_chaos_multiplier` | Stage 2 output |
| `individual_anxiety_score` | Stage 2 output |
| `pcai_score` | Stage 2 output |
| `alerts_generated` | Comma-separated alert_ids from Stage 3 that reference this patient |

This CSV serves as the human-readable "answer key."

### 1e. Golden Output Metadata
- Write a `tests/golden/outputs/metadata.json` containing:
  ```json
  {
    "generated_at": "<ISO 8601 UTC>",
    "pipeline_version": "1.0",
    "input_hash": {
      "hospital_state_sha256": "<hash of hospital-realtime-state.json>",
      "surveys_sha256": "<hash of sorted concatenation of all 60 survey files>"
    },
    "engine_versions": {
      "queue_prediction_engine": "<git commit or version>",
      "chaos_engine": "<git commit or version>",
      "cyberplan_engine": "<git commit or version>"
    }
  }
  ```
- The hashes allow detection of when source data has changed, invalidating golden outputs.

## 2. Build the Noisy Input Generator

Create a module `tests/noisy/noise_generator.py` that programmatically degrades clean input data. The generator must support the following noise categories, each applied independently and composably:

### 2a. Field-Level Noise

| Noise Type | Description | Parameters |
|---|---|---|
| `missing_field` | Remove a field entirely from the JSON | `field_path` (dot-notation, e.g. `"triage.esiLevel.selected"`) |
| `null_field` | Set a field's value to `null` | `field_path` |
| `wrong_type` | Replace a field with a value of the wrong type (e.g., string where int expected) | `field_path`, `replacement_value` |
| `out_of_range` | Set a numeric field to an invalid value (e.g., `esi_level = 7`, `pain_level = -3`, `spo2 = 150`) | `field_path`, `value` |
| `empty_string` | Replace a string field with `""` | `field_path` |
| `empty_array` | Replace an array field with `[]` | `field_path` |

### 2b. Structural Noise

| Noise Type | Description | Parameters |
|---|---|---|
| `truncated_json` | Truncate the JSON string at a random byte offset, producing invalid JSON | `truncation_percent` (0.0-1.0) |
| `missing_patient` | Remove an entire patient object from `waiting_room_queue.patients[]` | `patient_index` |
| `duplicate_patient` | Duplicate a patient object in the waiting room queue | `patient_index` |
| `extra_field` | Add an unexpected field to a JSON object | `field_path`, `key`, `value` |
| `swapped_files` | Swap an intake file with a triage file (wrong schema entirely) | `patient_path` |

### 2c. Temporal Noise

| Noise Type | Description | Parameters |
|---|---|---|
| `future_timestamp` | Set a timestamp field to a date in the future relative to `snapshot.captured_at` | `field_path`, `offset_hours` |
| `stale_timestamp` | Set `snapshot.captured_at` to 24+ hours in the past | `staleness_hours` |
| `timezone_mismatch` | Replace a UTC timestamp with one that has a different timezone offset but no conversion | `field_path`, `offset_hours` |
| `unparseable_timestamp` | Replace a timestamp with a malformed string (e.g., `"March 7th 2026"`, `"2026/03/07"`) | `field_path`, `format_string` |

### 2d. Cross-Reference Noise

| Noise Type | Description | Parameters |
|---|---|---|
| `orphan_encounter_id` | Change an `encounterId` in a nurse triage file to a UUID that doesn't exist in the hospital state | `triage_file_path` |
| `mismatched_mrn` | Change a patient's MRN in the hospital state so it no longer matches the survey MRN | `encounter_index` |
| `esi_mismatch` | Set a different ESI level in the hospital state vs. the nurse triage survey for the same patient | `encounter_index`, `new_esi` |

### Generator Interface

```python
class NoiseGenerator:
    def __init__(self, seed: int = 42):
        """Initialize with deterministic random seed for reproducibility."""

    def apply_noise(
        self,
        data: dict | str,
        noise_type: str,
        **params,
    ) -> dict | str:
        """Apply a single noise operation. Returns the degraded data.
        Accepts dict for parsed JSON, str for raw JSON (needed for truncation)."""

    def apply_noise_profile(
        self,
        clean_data: dict,
        profile: list[dict],
    ) -> dict:
        """Apply a sequence of noise operations defined as a list of
        {"noise_type": str, **params} dicts. Operations are applied in order."""

    def generate_noisy_dataset(
        self,
        clean_hospital_state: dict,
        clean_surveys: dict[str, dict],
        clean_triages: dict[str, dict],
        num_variants: int = 20,
        noise_budget: int = 3,
    ) -> list[dict]:
        """Generate num_variants noisy input sets, each with up to noise_budget
        random noise operations applied. Returns list of
        {"variant_id": str, "noise_ops": list[dict], "hospital_state": dict,
         "surveys": dict, "triages": dict} dicts."""
```

## 3. Build the Verification Engine

Create a module `tests/verification/verifier.py` that compares pipeline output against golden outputs.

### 3a. Comparison Logic

For each pipeline stage, define field-level comparison rules:

**Numeric fields** (wait times, scores, multipliers):
- Use **relative tolerance** for values > 10: `abs(actual - golden) / golden <= tolerance`
- Use **absolute tolerance** for values <= 10: `abs(actual - golden) <= abs_tolerance`
- Default tolerances: `rel_tolerance = 0.20` (20%), `abs_tolerance = 2.0`
- These tolerances account for the fact that noisy inputs should produce "close enough" outputs, not identical ones.

**Categorical fields** (ESI levels, alert severities, categories):
- Must match exactly — no tolerance.

**String fields** (alert messages, rationale text):
- Use **substring containment** — the golden output's key phrases must appear in the actual output.
- Define key phrases per field (e.g., an alert about a patient must contain that patient's ID).

**Structural fields** (arrays of alerts, patient lists):
- Compare by matching on a key field (e.g., `alert_id`, `patient_id`).
- Report missing items, extra items, and per-item field mismatches.

**Null handling:**
- If golden output has a non-null value and actual output has null → **FAIL** (data loss).
- If golden output has null and actual output has non-null → **WARN** (unexpected enrichment, but not necessarily wrong).
- If both null → **PASS**.

### 3b. Graceful Degradation Expectations

Not all noisy inputs should produce outputs identical to golden. Define three outcome categories:

| Outcome | Criteria | Example |
|---|---|---|
| **PASS** | Output is within tolerance of golden for all fields | Minor noise (e.g., extra field added) doesn't affect computation |
| **GRACEFUL_FAIL** | Pipeline returns a well-formed error response or marks affected fields as TBD/null with a status message | Missing `wait_duration_minutes` → ChaosEngine sets `pcai_score: null, _pcai_status: "TBD"` |
| **HARD_FAIL** | Pipeline crashes (unhandled exception), returns malformed output, or silently produces wildly wrong results | Truncated JSON → unhandled `json.JSONDecodeError` |

The verifier must classify each test result into one of these categories.

### 3c. Noise-to-Expectation Mapping

Create a configuration file `tests/verification/expectations.yaml` that maps noise types to expected outcomes:

```yaml
expectations:
  - noise_type: missing_field
    field_path: "triage.esiLevel.selected"
    expected_outcome: GRACEFUL_FAIL
    expected_behavior: "ChaosEngine uses default tau=60.0, logs warning"

  - noise_type: null_field
    field_path: "waiting_room_queue.patients[0].wait_duration_minutes"
    expected_outcome: GRACEFUL_FAIL
    expected_behavior: "ChaosEngine marks patient as TBD"

  - noise_type: truncated_json
    truncation_percent: 0.5
    expected_outcome: GRACEFUL_FAIL
    expected_behavior: "Pipeline catches JSONDecodeError, returns HTTP 503"

  - noise_type: out_of_range
    field_path: "triage.esiLevel.selected"
    value: 7
    expected_outcome: GRACEFUL_FAIL
    expected_behavior: "Engine rejects invalid ESI, uses fallback or returns error"

  - noise_type: extra_field
    field_path: "waiting_room_queue.patients[0]"
    key: "unknown_field"
    value: "unexpected"
    expected_outcome: PASS
    expected_behavior: "Pipeline ignores unknown fields, output matches golden"

  - noise_type: stale_timestamp
    staleness_hours: 48
    expected_outcome: GRACEFUL_FAIL
    expected_behavior: "Pipeline flags stale data, may refuse to process"

  - noise_type: orphan_encounter_id
    expected_outcome: GRACEFUL_FAIL
    expected_behavior: "Cross-reference lookup fails, patient processed without linked encounter"

  # Add entries for ALL noise types defined in section 2.
```

### 3d. Verifier Interface

```python
class PipelineVerifier:
    def __init__(
        self,
        golden_outputs_dir: str = "tests/golden/outputs",
        expectations_path: str = "tests/verification/expectations.yaml",
        rel_tolerance: float = 0.20,
        abs_tolerance: float = 2.0,
    ):
        """Load golden outputs and expectations."""

    def verify_stage(
        self,
        stage: int,
        actual_output: dict,
    ) -> StageVerificationResult:
        """Compare actual output against golden for a specific stage.
        Returns structured result with per-field comparisons."""

    def verify_full_pipeline(
        self,
        actual_stage1: dict,
        actual_stage2: dict,
        actual_stage3: dict,
    ) -> PipelineVerificationResult:
        """Verify all three stages. Returns aggregate result."""

    def classify_outcome(
        self,
        verification_result: PipelineVerificationResult,
        noise_ops: list[dict],
    ) -> str:
        """Classify as PASS, GRACEFUL_FAIL, or HARD_FAIL based on
        verification result and the noise that was applied."""
```

### 3e. Result Data Classes

```python
@dataclass
class FieldComparison:
    field_path: str
    golden_value: Any
    actual_value: Any
    status: str  # "MATCH", "WITHIN_TOLERANCE", "MISMATCH", "MISSING", "EXTRA", "NULL_UNEXPECTED"
    message: str

@dataclass
class StageVerificationResult:
    stage: int
    passed: bool
    total_fields: int
    matched_fields: int
    mismatched_fields: int
    comparisons: list[FieldComparison]

@dataclass
class PipelineVerificationResult:
    stages: list[StageVerificationResult]
    overall_passed: bool
    outcome: str  # "PASS", "GRACEFUL_FAIL", "HARD_FAIL"
    summary: str
```

## 4. Build the Test Runner

Create `tests/run_tests.py` as the main entry point that orchestrates everything:

### 4a. Test Execution Flow

```
1. Load clean data (surveys, triages, hospital state)
2. Load golden outputs (or generate if missing/stale via input hash check)
3. Generate N noisy variants using NoiseGenerator
4. For each variant:
   a. Run the full pipeline (Stage 1 → 2 → 3) with noisy inputs
   b. Catch any unhandled exceptions → classify as HARD_FAIL
   c. If pipeline completes, verify output against golden using PipelineVerifier
   d. Classify outcome (PASS / GRACEFUL_FAIL / HARD_FAIL)
   e. Compare against expected outcome from expectations.yaml
5. Produce test report
```

### 4b. Test Report

Output a structured report to `tests/reports/test_report_{timestamp}.json`:

```json
{
  "run_id": "<UUID>",
  "run_at": "<ISO 8601 UTC>",
  "golden_metadata": { "...from metadata.json..." },
  "total_variants": 20,
  "results_summary": {
    "PASS": 8,
    "GRACEFUL_FAIL": 10,
    "HARD_FAIL": 2,
    "expectation_match_rate": 0.85
  },
  "variants": [
    {
      "variant_id": "noisy-001",
      "noise_ops": [{"noise_type": "missing_field", "field_path": "..."}],
      "actual_outcome": "GRACEFUL_FAIL",
      "expected_outcome": "GRACEFUL_FAIL",
      "expectation_met": true,
      "stage_results": [
        {"stage": 1, "passed": true, "matched": 12, "mismatched": 0},
        {"stage": 2, "passed": false, "matched": 8, "mismatched": 2},
        {"stage": 3, "passed": false, "matched": 5, "mismatched": 1}
      ],
      "error": null
    }
  ]
}
```

Also produce a human-readable summary to stdout:

```
═══════════════════════════════════════════════
  Vitaloop Pipeline — Golden Output Test Report
═══════════════════════════════════════════════
  Variants tested:  20
  PASS:             8  (40%)
  GRACEFUL_FAIL:   10  (50%)
  HARD_FAIL:        2  (10%)
  Expectation match: 85%
───────────────────────────────────────────────
  HARD_FAIL details:
    noisy-007: truncated_json @ 30% — json.JSONDecodeError
    noisy-014: wrong_type on esi_level (str "three") — KeyError in ChaosEngine
═══════════════════════════════════════════════
```

### 4c. CLI Interface

The test runner must support these arguments:

```bash
# Generate golden outputs only (no noisy testing)
python tests/run_tests.py --generate-golden

# Run full test suite with 20 noisy variants, 3 noise ops each
python tests/run_tests.py --variants 20 --noise-budget 3

# Run with a specific noise profile (for debugging a particular failure)
python tests/run_tests.py --profile tests/noisy/profiles/missing_esi.yaml

# Regenerate golden outputs and run tests
python tests/run_tests.py --regenerate --variants 50
```

## 5. Predefined Noise Profiles

Create targeted noise profiles in `tests/noisy/profiles/` as YAML files. Each profile exercises a specific failure mode:

### `missing_critical_fields.yaml`
Tests removal of fields that the pipeline depends on most:
- `triage.esiLevel.selected`
- `waiting_room_queue.patients[].wait_duration_minutes`
- `hospital_metrics.ed_metrics.ed_occupancy_percent`
- `waiting_room_queue.patients[].arrival_timestamp`
- `triage.anticipatedResources.selected`

### `type_coercion.yaml`
Tests wrong-type values in critical fields:
- `esi_level` as string (`"3"` instead of `3`)
- `pain_level` as float (`7.5` instead of `7`)
- `wait_duration_minutes` as string (`"174"`)
- `ed_occupancy_percent` as string (`"7.14%"`)

### `boundary_values.yaml`
Tests edge cases:
- `esi_level = 0`, `esi_level = 6`
- `pain_level = -1`, `pain_level = 11`
- `wait_duration_minutes = 0`, `wait_duration_minutes = 9999`
- `ed_occupancy_percent = 0.0`, `ed_occupancy_percent = 200.0`
- `total_boarders = 0`, `total_boarders = 100`

### `cross_reference_breaks.yaml`
Tests broken links between data sources:
- `encounterId` in triage file points to nonexistent encounter
- MRN mismatch between survey and hospital state
- ESI level disagreement between triage survey and hospital state
- Patient in waiting room queue with no matching survey file

### `realistic_degradation.yaml`
Simulates plausible real-world data quality issues:
- 2-3 missing optional fields per patient (e.g., `email`, `phoneMobile`)
- One patient with `null` pain score
- Timestamp in wrong timezone (CDT instead of UTC) for one encounter
- One extra patient in waiting room not in surveys (new arrival mid-pipeline)
- Stale `snapshot.captured_at` by 5 minutes (within tolerance)

# File Structure

```
tests/
├── __init__.py
├── run_tests.py                          # CLI entry point
├── golden/
│   ├── __init__.py
│   ├── generate_golden_outputs.py        # Golden output generator
│   └── outputs/                          # Generated golden outputs (gitignored except metadata)
│       ├── .gitkeep
│       ├── metadata.json
│       ├── stage1_queue_prediction.json
│       ├── stage2_chaos_engine.json
│       ├── stage3_cyberplan_engine.json
│       └── patient_golden_reference.csv
├── noisy/
│   ├── __init__.py
│   ├── noise_generator.py                # Noise generation engine
│   └── profiles/
│       ├── missing_critical_fields.yaml
│       ├── type_coercion.yaml
│       ├── boundary_values.yaml
│       ├── cross_reference_breaks.yaml
│       └── realistic_degradation.yaml
├── verification/
│   ├── __init__.py
│   ├── verifier.py                       # Verification engine
│   └── expectations.yaml                 # Noise-to-expectation mapping
└── reports/                              # Test reports (gitignored)
    └── .gitkeep
```

# Dependencies

Add to the project's `requirements.txt`:
```
pytest>=7.0
pyyaml>=6.0
```

The pipeline engines (`QueuePredictionEngine`, `ChaosEngine`, `CyberplanEngine`) are imported from their respective modules. Do not reimplement them — treat them as black boxes that this testing system validates.

# Deliverables

Provide all files listed in the file structure above as complete, runnable Python code. Ensure:

1. All modules have proper imports and can be run independently.
2. The `NoiseGenerator` is fully deterministic given the same seed.
3. The `PipelineVerifier` produces clear, actionable output for each field-level comparison.
4. The test runner handles exceptions gracefully — a pipeline crash should be captured and reported, not crash the test runner itself.
5. YAML profiles are complete with all noise operations specified and expected outcomes documented.
6. The golden output generator validates that source data hashes match before regenerating, and warns if golden outputs are stale.
