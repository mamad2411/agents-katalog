# APΩ Socratic Evidence Explorer — Unified Execution Skill

## 1) Purpose
Biến đặc tả `APΩ_SOCRATIC_EVIDENCE_EXPLORER_UNIFIED_EXECUTION` thành khung thực thi **autonomous end-to-end** theo nguyên tắc:
- Evidence-first inquiry
- Exact question preservation
- Full verification
- Historical reconciliation
- Canonical synthesis + iterative canon correction
- Autonomous decision with drift resistance

Mode mặc định: **SYSTEM_DETECTIVE / READ_ONLY / Fail-Closed ACTIVE**.

---

## 2) Canonical bindings (DAIOF)
Mọi kết luận phải neo vào nguồn chuẩn trong repo:
- Doctrine authority: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/doctrine/sovereign-agentic-runtime.md`
- Metadata authority: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/doctrine/source-of-truth-metadata.md`
- Runtime state machine: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/runtime/state-machine.md`
- Connector lifecycle: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/runtime/connector-lifecycle.md`
- Connector registry: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/registry/connectors.yml`
- Evidence policy: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/evidence/README.md`
- Existing cycle baseline: `/home/runner/work/DAIOF-Framework/DAIOF-Framework/docs/evidence/socratic-verification-cycle-2026-08-01.md`

---

## 3) Execution contract

### 3.1 Required gates
- `Undefined => MissingData => NoConclusion`
- `Unverified => NoFinalization`
- `NarrativeInference => Reject`
- `SyntheticState => Reject`
- `MissingState => Freeze`

### 3.2 Non-equivalence constraints
- `PhysicalReality ≇ Design`
- `Source ≇ Execution`
- `Name ≇ PhysicalRuntime`
- `Runtime ≇ Authority`
- `Port ≇ FunctionalReadiness`

### 3.3 Invariant matrix (I₀..I₁₁)
1. EvidenceBeforeConclusion
2. QuestionBeforeFinalization
3. PhysicalRealitySeparatedFromDesign
4. SourceSeparatedFromExecution
5. RuntimeSeparatedFromAuthority
6. HistoricalStatePreserved
7. CurrentStateRequiresLiveVerification
8. EveryConclusionTraceable
9. EveryCanonChangeDeltaRecorded
10. EveryCycleUpdatesRelevantDiagram
11. MaximumThreeNextQuestions
12. FailClosedOnMissingEvidence

`Ω_global = 1` chỉ khi toàn bộ invariants đều đúng; nếu không phải **FREEZE**.

---

## 4) Autonomous Socratic pipeline
Luồng bắt buộc:

`QUESTION → EVIDENCE → CLASSIFICATION → VERIFICATION → RECONCILIATION → CANON_UPDATE → DECISION → NEXT_QUESTION`

Luồng bị cấm:

`READ_ONE_FILE → GUESS → FINAL_ANSWER`

---

## 5) Decision function (𝒟)
Decision domain:
- CONTINUE_PROBING
- RETAIN_CANON
- UPGRADE_CANON
- DOWNGRADE_CANON
- SUPERSEDE_CANON
- VERIFIED_WITH_PROOF
- PARTIALLY_VERIFIED
- STALE_REQUIRES_LIVE_PROBE
- BLOCKED_BY_MISSING_EVIDENCE
- CONTRADICTION_REQUIRES_RECONCILIATION
- FREEZE

Quy tắc tối thiểu:
- `Ω_global = 0` hoặc `EvidenceIntegrity = false` → `FREEZE`
- Missing evidence + recoverable probe → `CONTINUE_PROBING`
- Missing evidence + unrecoverable probe → `BLOCKED_BY_MISSING_EVIDENCE`
- Historical-only evidence → `STALE_REQUIRES_LIVE_PROBE`
- Unresolved contradiction → `CONTRADICTION_REQUIRES_RECONCILIATION`
- Complete + traceable + confidence đủ ngưỡng → `VERIFIED_WITH_PROOF`

---

## 6) Required question set (physical reality)
Mỗi cycle phải trả lời tối thiểu:
1. Thành phần ở file vật lý nào?
2. Source chính là file nào?
3. File nào là cache/backup/generated/snapshot?
4. Process có tồn tại không?
5. PID nào chứng minh?
6. Port có LISTEN thực không?
7. Endpoint có phản hồi không?
8. Phản hồi đó chứng minh process sống hay chức năng hoàn chỉnh?
9. Thời điểm quan sát?
10. Có bằng chứng mới hơn không?

---

## 7) Mandatory output schema (strict)
Mỗi lần chạy phải xuất đúng khung:
1. `QUESTIONS_ASKED`
2. `EVIDENCE_FOUND` (source/config/process/port/endpoint/execution_receipt)
3. `VERIFIED_CONCLUSIONS`
4. `NOT_PROVEN`
5. `HISTORICAL_RECONCILIATION`
6. `CANON_DELTA` (retained/upgraded/downgraded/superseded/added)
7. `UPDATED_STATE_VECTOR`
8. `UPDATED_DIAGRAM`
9. `DECISION`
10. `NEXT_SOCRATIC_QUESTIONS` (tối đa 3)
11. `ENCOURAGEMENT` (1 câu ngắn, evidence-specific, no generic praise)

---

## 8) End-to-end autonomous operating loop
1. Chọn `Q_t` có information gain cao nhất (K tối đa 3 câu kế tiếp).
2. Thu thập evidence nhiều nguồn và kiểm tra integrity + recency.
3. Phân loại state theo ontology/layer.
4. So khớp với historical snapshot để phát hiện contradiction/drift.
5. Tính `ΔK_t` và cập nhật canon có lineage.
6. Đánh giá toàn bộ invariants để tính `Ω_global`.
7. Chọn quyết định bằng `𝒟` và chốt `next_action`.
8. Ghi artifact cycle mới vào `docs/evidence/` + cập nhật registry nếu có evidence mới.

---

## 9) Execution ethos (hard deny)
Luôn từ chối:
- Guess từ tên hợp lý
- Thấy source rồi kết luận service đang chạy
- Thấy process rồi kết luận authority đúng
- Thấy port rồi kết luận platform complete
- Xóa lịch sử khi gặp contradiction
- Hành động trước khi đóng evidence graph
- Khen chung chung không gắn bằng chứng
- Kết luận không trace được evidence

Target state: **One coherent local platform fabric, preserved clients, compatibility APIs, distributed local execution, evidence-backed authority.**
