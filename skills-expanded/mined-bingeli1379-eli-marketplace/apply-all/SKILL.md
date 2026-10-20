---
name: apply-all
description: >
  Use when the user has several prepared changes and wants to batch-implement
  them unattended, running /apply on each of them sequentially.
user-invocable: true
---

Run `/apply` on multiple changes sequentially. The main Claude acts as orchestrator for the entire batch — dispatching worker agents in the background while remaining responsive to user messages.

Repo topology (single-repo / multi-repo / no-git) is detected **once at batch start** — run `/apply` Step 0 against cwd before the first change, and reuse the result for every change in the batch (cwd does not move between changes). Per-change task groups are then bound to their target repos exactly as in `/apply`. `/apply-all` adds nothing topology-specific; it just sequences the changes.

---

**Input**: Optionally specify change names in order (e.g., `/apply-all add-user-registration add-user-profile add-user-roles`). If omitted, auto-detect. An optional `dev-mode` token may appear anywhere in the arguments (e.g., `/apply-all add-user-registration dev-mode add-user-profile`) — see Step 1 for parsing rules.

**Steps**

1. **Discover active changes and parse mode flags**

   **Mode flag parsing**: split arguments on whitespace. If any token equals `dev-mode` (case-insensitive), set the internal `DEV_MODE = true` flag and remove the token from the argument list. Pass `dev-mode` through to each per-change `/apply` invocation in Step 3 so its retrospective is surfaced too. The remaining tokens go through normal name resolution. `DEV_MODE` defaults to `false` — the batch `事後檢討` block in Step 4 is suppressed unless the flag is set.

   List all directories under `feature-spec/changes/` (excluding `archive/`).
   Filter to only changes that have pending tasks (`- [ ]` in `tasks.md`).

   If no pending changes found:
   - Report: "No pending changes found. Run `/propose` first."
   - Stop.

2. **Determine execution order**

   **If names are provided as arguments:** use that exact order.

   **If no arguments — auto-resolve dependencies:**

   a. Read each change's `proposal.md` and look for the `## Dependencies` section.
   b. Build a dependency graph from all `Depends on` fields across all active changes. If a `Depends on` names a change **not in the active set** (already `/complete`d, or a typo), warn once — `⚠ <change> depends on <X>, not in this batch — its ordering is not guaranteed` — and treat that one edge as already satisfied (do not add a phantom node).
   c. **Topological sort** — order changes so dependencies come first.
   d. If circular dependencies are detected, report the cycle and ask the user to resolve.
   e. **Decide whether to ask or auto-execute:**

   - **Order is deterministic** (all changes form a single dependency chain, or there is only one change): announce the order and **execute immediately without asking**.
   - **Order is ambiguous** (multiple independent changes exist at the same topological level — i.e., they have no dependency relationship and could run in any order): show the resolved order and **ask the user** which order to use:

     ```
     ## 批次套用

     發現 N 個待處理的變更（已依相依性排序）：

     1. add-user-registration（5 待處理 / 8 總計）
     2. add-user-profile（3 待處理 / 3 總計）← depends on: add-user-registration
     3. add-user-roles（4 待處理 / 4 總計）← depends on: add-user-registration

     ⚠️ 2 和 3 互相獨立，無法判斷先後順序。
     按此順序執行？或指定不同順序（例如 "3, 1, 2"）：
     ```

     Use **AskUserQuestion** to let the user confirm or reorder.
     This is the **only** question asked — after confirmation, execution begins automatically.

   **If no Dependencies sections found** — all changes are independent. List them in alphabetical order and ask the user to confirm or reorder (same format as the ambiguous branch above).

3. **Run each change sequentially**

   Maintain a **paused/failed set** across the batch (changes that ended PAUSED via 3f/3g). For each change in order:

   **Prerequisite gate (check before running each change)**: if any change in this change's `## Dependencies` → `Depends on` is in the paused/failed set, do **NOT** run it — its tasks reference prerequisite code (API/types/schema) that was never completed, so its agents would hit missing symbols and produce broken output. Park it as PAUSED (reason: `prerequisite <X> not complete`), add it to the paused/failed set (so its own dependents park transitively down the chain), announce the skip, and continue to the next change. Do not dispatch its agents. Otherwise proceed:

   a. Announce: `[N/M] Applying: <change-name>` and record the start time and `git rev-parse HEAD` (the branch tip before this change — 3f reads it).

   b. Execute the full `/apply` logic (Steps 2–9 from `apply/SKILL.md` — Step 0 topology already ran once at batch start, and Step 1 change selection is this skill's Steps 1–2):
      - **Cache `config.yaml` once at batch start; re-read `orchestrator.md` per change**: read the project `config.yaml` once before the first change — single-repo `feature-spec/config.yaml`; **multi-repo** the per-child-repo `<repo>/feature-spec/config.yaml` of every repo the batch touches (there is no umbrella config — see `/apply` Step 2, the grounding read). Config is invariant across the batch — reuse it for every change. `orchestrator.md` is not cached: `/apply` Step 6 re-reads it every time because context may have been compressed, and a batch running for hours is exactly where that happens — the second change would otherwise run on whatever the compaction kept.
      - **Re-read change-specific files fresh for each change** (proposal.md, design.md, tasks.md, specs/). Each change has different specs — do NOT reuse these from the previous change. Prior context may also have been compressed.
      - Read context → parse tasks → act as orchestrator → sequential single-writer dispatch with in-place squash → all phases (implementation → review+security parallel read-only, then QA alone → docs) → verify checkboxes and commit history
      - **Do NOT ask implementation questions** — make reasonable choices, flag ambiguities in report

   c. **Mandatory completion checkpoint — Do NOT proceed to next change until ALL are satisfied:**
      - [ ] Every phase dispatched, or skipped with its reason recorded for the change's report (`/apply` Step 7 — review-engineer + security-engineer are never skipped)
      - [ ] Phase 2's Fix → Re-verify Loop exited on its own terms (`agents/orchestrator.md` → *Fix → Re-verify Loop*, step 5): no `blocker` / `major`, no FAILED QA, no newly introduced `WILL NOT SCALE` — a verdict carrying only `minor`s (`APPROVED WITH COMMENTS`, `ISSUES FOUND` with minors) satisfies it; the round limit reached with one of those still standing is PAUSED (3f)
      - [ ] Step 9 tasks.md re-read from disk and checkboxes verified
      - [ ] Final commits are clean conventional-commit messages with no task numbers

   d. Record end time, duration, and result (COMPLETE or PAUSED with reason).

   e. Announce: `[N/M] <change-name>: COMPLETE (8/8 tasks, 25m, 10 派工, diff 8 檔/+13−9)` — the same cost figures `/apply` prints (`skills/apply/SKILL.md` → Step 9), which matter more here because an unattended batch multiplies them — and **automatically proceed to next change**.

   f. **If a change pauses** (review/QA failure after retries): record the reason, **add it to the paused/failed set** (the prerequisite gate above then parks its dependents transitively), and **continue to next change** — do NOT stop the batch. User can fix later with `/apply <name>`. **One condition stops the batch instead**: when the paused change left task-number-prefixed per-task commits unsquashed on the branch (`git log --oneline <HEAD recorded at 3a>..HEAD` shows any `<type>: N.M …`), stop after it and report — task numbers restart at `1.1` in every change, so the next change's `/apply` Step 5b reconcile would match those commits as its own and skip work never done. The user squashes or removes them, then resumes with `/apply-all`.

   g. **Unresolvable NEEDS in unattended mode**: when a worker emits a `NEEDS:` (see `skills/agent-guidelines/SKILL.md` → *Signaling Unknowns*), resolve it with the tools available and resume the agent as in `/apply`. But because the batch runs unattended, if a NEEDS can only be answered by the user and no resolving tool is available, do NOT hang waiting — **park that change as PAUSED** (reason: `unresolved NEEDS: <question>`), add it to the paused/failed set, and continue to the next. The user resolves it later with `/apply <name>`. 3f's unsquashed-commit stop applies here too — a `NEEDS` is emitted after the agent committed what it safely could, so this is the path most likely to leave numbered commits behind.

4. **Show final batch report**

   ```
   ## 批次實作完成

   **總耗時：** Xh Ym

   **結果：**
   - [x] add-user-registration — 完成 (8/8 任務, 25m)
   - [ ] add-user-profile — 暫停 (code review failed after 2 retries, 18m)
   - [x] add-user-roles — 完成 (4/4 任務, 12m)

   **摘要：** 2/3 changes 完成, 1 暫停

   **略過的階段：**          ← omit when no change skipped a phase
   - `add-user-roles`: Phase 3 technical-writer — [原因]

   **暫停的 changes：**
   - `add-user-profile`: [原因]. 執行 `/apply add-user-profile` 重跑

   **接下來由你執行：**      ← aggregate every change's handoff items here; omit the block when there are none
   - `add-user-registration`: [該 change 的 `## 交付後由你執行` 逐條，加上任何 `MOCKED:` 的替換動作]

   **事後檢討：**            ← include this entire block ONLY when DEV_MODE = true; omit silently otherwise
   [彙整所有 changes 中遇到的錯誤、意外狀況、手動介入]
   - 每個問題：哪個 change、發生什麼、根因、如何解決
   - 預防建議：針對未來任何人使用此 plugin 時可複用的通用做法
   - 若無問題：「乾淨執行，所有 changes 無問題。」
   ```

   **Retrospective gating**: when `DEV_MODE = false` (the default), drop the `**事後檢討：**` line and its body entirely from the batch report. End users get a clean batch summary; plugin authors re-run with `dev-mode` to surface aggregated lessons learned.

---

## Interactive Control

While the batch is running, the user can send messages at any time. Respond to them:

- **"status" / "進度"** — show batch progress: which change is active, current phase, running agents, overall N/M changes
- **"skip" / "跳過"** — skip the current change, move to next
- **"stop" / "停止"** — stop dispatching new agents/changes after current agents finish, show partial report
- **"skip <change-name>"** — remove a specific upcoming change from the queue
- **Any other message** — interpret as orchestrator instruction for the current change

After responding to the user, **resume batch execution automatically** — do NOT wait for further input.

---

## Guardrails

- **A skipped phase is printed with its reason, never silent** — see the Step 3c checkpoint
- If a change has no pending tasks (all `- [x]`), skip it and note in the report
