# aix — Implementation Tasks (theo ASSESSMENT.md)

> Kế hoạch đóng khoảng cách giữa **tuyên bố** và **thực tế** đã nêu trong [ASSESSMENT.md](./ASSESSMENT.md).
> Trạng thái: `[ ]` chưa làm · `[~]` đang làm · `[x]` xong.

> **✅ HOÀN THÀNH T1–T7** (2026-06-28):
> - T1–T6 trong commit `59c2cad` — engine ghi file, wire budget, mock fail-loud, docs, private, tests.
> - T7 — `git filter-repo` đã strip `imports/` khỏi toàn bộ history; force-push lên `origin/main`
>   (HEAD `8626fe6`). Backup bundle: `scratchpad/aix-backup-20260628-003954.bundle`. `.git` 42M→38M;
>   `imports/` còn trên đĩa (gitignored, làm reference) nhưng 0 refs trong history.

---

## T1 — Coder node ghi file thật 🔴

**Vấn đề:** `aix run --auto` sinh code ra string rồi vứt; không node nào chạm filesystem.

**Giải pháp (an toàn):** Ghi code sinh ra vào **sandbox** `.aix/generated/<sessionId>/`,
KHÔNG ghi đè `src/` của user (vòng auto không có review → ghi thẳng vào source là nguy hiểm).
User tự review rồi apply.

**Cần làm:**
- [ ] `packages/engine/src/state.ts`: thêm `writtenFiles?: readonly string[]` vào `EngineState`.
- [ ] `packages/engine/src/nodes/coder.ts`:
  - Sau khi có `output`, ghi vào `.aix/generated/<sessionId>/<file>` (file lấy từ `ticketPlan.files[0]`,
    fallback `task-<id>.ts`).
  - Sanitize path: chặn `../` và leading `/` (path traversal).
  - Trả về `writtenFiles: [<đường dẫn đã ghi>]` (chỉ file MỚI; graph reducer sẽ cộng dồn).
- [ ] `packages/engine/src/graph.ts`: thêm channel `writtenFiles` vào `GraphAnnotation`
  với reducer cộng dồn (`(a,b)=>[...a,...b]`, default `[]`).

**Acceptance:** `aix run --auto "viết hàm add"` tạo file thật dưới `.aix/generated/<id>/`.

---

## T2 — Wire budget vào engine 🔴

**Vấn đề:** `BudgetTracker.addUsage()` không bao giờ được gọi; `usdSpent` luôn = 0;
hard-stop không bao giờ kích hoạt.

**Cần làm:**
- [ ] `packages/engine/src/nodes/coder.ts`: sau mỗi `provider.call()`, gọi
  `createBudgetTracker().addUsage(state.session, response.usd, response.tokens)` →
  trả `session` đã cập nhật trong state.
- [ ] Xác nhận `graph.ts` `routeLoopStart` đọc `checkHardStop(toEngineState(state))` → giờ thấy `usdSpent` thật.
- [ ] `session` channel trong `GraphAnnotation` phải replace (last-write-wins) — đã đúng.

**Acceptance:** Sau auto-run, `final.session.budget.usdSpent > 0`; nếu vượt `usdLimit` → loop dừng.

---

## T3 — Mock mode fail-loud 🔴

**Vấn đề:** Không có API key → mock bịa `solution(input){return input}`, báo "Score 9/10, done".

**Cần làm:**
- [ ] `packages/cli/src/commands/run.ts` `handleAuto()`:
  - Phát hiện thiếu `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` → in banner ⚠ **MOCK MODE** rõ ràng
    trước VÀ sau khi chạy ("output là placeholder, không phải code thật").
  - In `Budget: $X spent` + danh sách `writtenFiles`.
- [ ] (Tùy chọn) `runtime.ts`: giữ warning hiện có nhưng nâng tông.

**Acceptance:** Chạy auto không key → có cảnh báo mock nổi bật, không thể nhầm là code thật.

---

## T4 — Sửa README/CHANGELOG cho khớp thực tế 🟠

**Cần làm:**
- [ ] `README.md`:
  - Bảng packages, dòng `@x/context`: "Tree-sitter analysis" → "Regex-based code analysis
    (tree-sitter planned)".
  - Hạ tông phần engine: nói rõ "sinh artifacts vào sandbox `.aix/generated/` để review",
    không phải tự sửa source.
- [ ] `CHANGELOG.md`: thêm mục cho các thay đổi T1–T3 (Unreleased).

**Acceptance:** Không còn tuyên bố sai (tree-sitter, "tự code vào repo").

---

## T5 — `private: true` cho packages chưa sẵn sàng publish 🟡

**Vấn đề:** 13 `@x/*` đặt `private: false` nhưng thiếu `files`/`license`/`repository`,
dùng `workspace:*` → publish sẽ vỡ.

**Cần làm:**
- [ ] Đặt `"private": true` cho cả 13 package `packages/*/package.json`.
- [ ] (Để sau khi publish thật) thêm `files`, `license`, `repository`, đổi scope `@x`,
  dùng changesets.

**Acceptance:** `node -e` check tất cả package `private=true`.

---

## T6 — Test cho engine 🟡

**Vấn đề:** 1 test/repo, 0 runner; rule đòi 80%. Bug node-name từng lọt tới runtime.

**Cần làm:**
- [ ] Thêm vitest vào `packages/engine` (devDep + `vitest.config.ts` + script `test`).
- [ ] Smoke test: `EngineGraph.run()` ở mock mode → chạy hết graph không throw,
  trả `reviewScore` number, `writtenFiles` có phần tử.
- [ ] Test budget wiring: sau run, `session.budget.usdSpent > 0`.
- [ ] Thêm task `test` vào `turbo.json` + CI `ci.yml` chạy `pnpm test`.

**Acceptance:** `pnpm test` xanh; CI chạy test.

---

## T7 — (Tùy chọn) Dọn lịch sử git 🟡

**Vấn đề:** 739 commit từ 6 repo cũ nung vào `.git` (41M); `imports/` 28M trên đĩa.

**Cần làm (PHÁ HỦY — cần user xác nhận, KHÔNG tự chạy):**
- [ ] `git filter-repo --path imports/ --invert-paths` để bỏ `imports/` khỏi lịch sử.
- [ ] Xóa `imports/` khỏi đĩa nếu không cần tham chiếu.

**Acceptance:** `.git` nhỏ lại đáng kể. (Chỉ làm khi user đồng ý vì rewrite history.)

---

## Thứ tự thực thi

1. **T1 + T2** (cùng file `coder.ts` + `graph.ts` + `state.ts`) — đóng khoảng cách lớn nhất.
2. **T3** (`run.ts`) — an toàn cho user.
3. **T5** (`package.json`) — nhanh.
4. **T4** (docs) — sau khi hành vi đã đúng.
5. **T6** (tests) — khóa lại để không regress.
6. **T7** — chỉ khi user yêu cầu.
