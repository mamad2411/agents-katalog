# P0-V2-NEW-2 Strategist Wide-Adjustment Skill

Date: 2026-05-09
Role: PM
Status: SOURCE/TEST CLOSED

## Decision

Operator selected the no-new-gate design:

- keep `RiskConfig.strategist.max_param_delta_pct = 0.50` as the maximum
  Strategist freedom envelope;
- do not add a new supervised/hard gate for 30%-50% moves;
- do not revert the cap to 30%;
- develop the 30%-50% zone as a Strategist skill.

## Scope

Implemented `wide_parameter_adjustment` as a real Rust->Python prompt skill:

- Rust `StrategistScheduler` now sends `strategist_skill` in each
  `strategist_evaluate` payload:
  - `normal_delta_pct = 0.30`
  - `max_delta_pct = <current RiskConfig.strategist.max_param_delta_pct>`
  - `name = "wide_parameter_adjustment"`
- Python `AIService._build_strategist_prompt()` now renders:
  - `normal_range` for ordinary <=30% tuning;
  - `wide_skill_range` for deliberate 30%-50% adjustments;
  - explicit skill guidance that this is Strategist discipline, not an
    approval gate.
- Rust validation still enforces only the configured maximum envelope. The
  30%-50% zone is not a new reject path.

## Verification

- `python3 -m py_compile program_code/exchange_connectors/bybit_connector/control_api_v1/app/ai_service_dispatch.py program_code/exchange_connectors/bybit_connector/control_api_v1/tests/test_p1_audit_smoke.py`
- `python3 -m pytest -q program_code/exchange_connectors/bybit_connector/control_api_v1/tests/test_p1_audit_smoke.py -q`
  -> 13 passed
- `cargo test -p openclaw_engine --lib strategist_scheduler -- --nocapture`
  -> 33 passed
- `cargo fmt --all --check`
- `git diff --check`

## Boundary

Source/test only. No runtime reload, rebuild, DB write, cron/env mutation,
provider traffic, live auth mutation, or true-live API action.

PM SIGN-OFF: APPROVED for source/test close.
