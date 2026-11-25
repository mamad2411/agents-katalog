---
alwaysApply: true
---
# Project Rules – BDO Market Tracker

## 1. Scope & Sources of Truth
- **Owner docs**: `instructions.md` (master spec) + this `PROJECT_RULES.md` summary. When they differ, follow `instructions.md` and sync this file.
- **Code reality**: Rules below match the current repo (EasyOCR primary, content-hash dedupe, 29/32 tests with 3 deprecated, ROI top-75%). Update both files whenever behavior changes.
- **Out-of-date docs**: Anything under `docs/archive/`, `docs/archived/`, or `scripts/archive/` is historical only.

## 2. Operational Modes
- **Primary use**: Tkinter GUI (`python gui.py`) for capture + tracking. CLI scripts in `scripts/` are test/support tooling only.
- **Platform**: Windows 10+, Python 3.10-3.13. Tesseract installed locally. GPU (CUDA) optional but supported.
- **Focus guard**: Scans run only when a BDO window title contains `"Black Desert"`; foreground check is required.

## 3. Capture & OCR
- **Region**: `DEFAULT_REGION = (734, 371, 1823, 1070)` (top-left and bottom-right). ROI trimming keeps top 75% of the capture (transactions appear near the top). Do not shrink ROI without verifying logs remain visible.
- **OCR pipeline**: EasyOCR is the primary engine (GPU if available, CPU fallback). PaddleOCR support exists but is disabled by default (`OCR_ENGINE = 'easyocr'`, `OCR_FALLBACK_ENABLED = False`). Tesseract is final fallback.
- **Preprocessing**: Balanced CLAHE + mild sharpening. No aggressive binarization. Fast mode available but defaults to quality mode.
- **Caching**: Screenshot hash cache (MD5) with 5s TTL, max 20 entries. Applies after ROI cropping.

## 4. Window Detection & Valid Contexts
- Window types are mutually exclusive per scan: `sell_overview`, `buy_overview`, `sell_item`, `buy_item`.
- Only overview windows contain logs. Detail windows must trigger burst rescans and produce no DB writes.
- Window detection relies on tolerant keyword checks (`Sales Completed`, `Orders Completed`, etc.). Keep these keywords in sync with `utils.detect_window_type`.

## 5. Parsing & Event Classification
- `parsing.py` splits OCR text into timestamped entries and extracts events (`transaction`, `purchased`, `listed`, `placed`, `withdrew`, `collect`).
- Anchor priority is `transaction > purchased > placed > listed`; never let UI-only rows (qty=None) anchor clusters.
- Timestamp queue maps newest→oldest ordering. Use game timestamps exclusively; do not substitute system time.
- Quantity bounds: `1 ≤ qty ≤ 5000`. Reject out-of-range or missing quantities unless UI delta inference fills them.
- Item names must pass through `market_json_manager`. Exact matches bypass fuzzy correction; unknown names reject saves.

## 6. Transaction Grouping & Cases
- Evaluate only new lines relative to `last_overview_text` baseline (persisted in `tracker_state`).
- Cluster within ±3s (transactions/listed/placed) or ±8s (withdrew). First snapshot allows up to 10 minutes for historical logs.
- Supported cases: `sell_collect`, `sell_relist_full`, `sell_relist_partial`, `buy_collect`, `buy_relist_full`, `buy_relist_partial`.
- UI delta inference (orders/ordersCompleted, salesCompleted/price) may synthesize missing collect transactions but only when overview metrics changed and log lines are absent.

## 7. Deduplication & Storage
- Database schema (`transactions` table): `id`, `item_name`, `quantity`, `price`, `transaction_type`, `timestamp`, `tx_case`, `occurrence_index`, `content_hash`.
- Unique index on `(item_name, quantity, price, transaction_type, timestamp, occurrence_index)` remains in place; do not drop.
- Runtime dedupe: session signature deque (max 1000) plus `content_hash` with a 20-minute tolerance window. If same hash reappears >20 minutes later, treat as new legitimate transaction.
- Always update persistent occurrence state (`tx_occurrence_state_v1`) when storing to keep repeated same-second events distinct.
- Database access must go through `database.get_connection()` / `get_cursor()` (thread-local). No sharing of SQLite objects across threads.

## 8. Price Validation & Fallbacks
- Unit price plausibility uses live BDO API data (`bdo_api_client`). Accept prices within ±10% of current min/max; mark outside range as implausible unless API data missing.
- Price fallback allowed only when collect/relist action is confirmed in the active overview window and all required metrics were captured. Never apply to historical snapshots.
- Division-by-zero or missing metrics cancel the fallback.

## 9. Focus, Polling & Performance
- Poll interval defaults to 0.15s; `GAME_FRIENDLY_MODE` increases to ≥0.8s when GPU mode is active.
- Burst scanning (80ms interval) engages after returning from detail windows to catch freshly appended log lines.
- Interruptible sleep is mandatory; auto-loop must stop within ~200ms upon user request.
- Keep screenshot cache, LRU caches (`correct_item_name`, market data), and regex pools intact to maintain performance (≈99 scans/min on GPU, ≈60 CPU).

## 10. Testing Expectations
- Current status: 29/32 active tests pass; 3 tests remain deprecated (see `scripts/archive/test_*` for legacy cases). Do not claim full pass until those are addressed.
- Run `python scripts/run_all_tests.py` before shipping meaningful changes. Tests rely on real OCR dependencies—ensure EasyOCR/Tesseract models are installed.
- Add or update tests alongside feature/bugfix changes. Place new scripts under `scripts/` (active) or `scripts/utils/` for helpers. Archive obsolete tests instead of deleting history outright.

## 11. Debug Artefacts
- Maintain up-to-date `debug_orig.png`, `debug_proc.png`, and `ocr_log.txt`. When investigating issues, capture and reference them first.
- Log rotation at 10MB is active; avoid removing the rotation logic.

## 12. Documentation Hygiene
- This file plus `instructions.md` constitute the living spec. Update both whenever behavior or expectations change.
- `WARP.md` summarizes quick-run instructions; keep its commands consistent with current behavior (EasyOCR primary, 29/32 test status, etc.).
- README should reflect actual feature/test counts—adjust when these change.

## 13. No-Go Items
- Do **not** evaluate logs in item detail windows.
- Do **not** shorten the ROI or disable burst scans without data proving no regressions.
- Do **not** bypass market whitelist or quantity bounds to force saves; fix OCR/parsing instead.
- Do **not** disable content-hash dedupe or occurrence_index tracking—duplicate handling depends on them.
- Do **not** introduce system-time-based fallbacks for timestamps.

## 14. When In Doubt
- Reproduce using GUI auto-track with debug logging enabled.
- Inspect `ocr_log.txt` and both debug screenshots before adjusting parsing or window detection.
- Verify outcomes against database entries (`check_db.py` / `inspect_db.py`) to confirm saved transactions match expectations.
