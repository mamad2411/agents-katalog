# aix — Đánh giá kỹ thuật (Technical Assessment)

> ⚠️ **SNAPSHOT LỊCH SỬ — đa số đã được khắc phục.** Báo cáo này chụp tại commit `08e7f87`.
> Từ đó: **T1–T7** (xem [TASKS.md](./TASKS.md)) đã đóng các khoảng cách §1–§3 (coder ghi file
> thật vào `.aix/generated/`, budget được wire qua `addUsage`, mock mode fail-loud), `private: true`
> cho cả 13 package, thêm smoke test cho `EngineGraph.run()` + CI chạy `pnpm test`, và
> `git filter-repo` đã dọn `imports/` khỏi lịch sử.
>
> **Quan trọng hơn — reframing chiến lược:** báo cáo này coi `@x/engine` là "điểm bán hàng chính",
> nhưng đó là **góc nhìn sai**. aix không phải runtime độc lập; nó là **plugin cài vào agent** (mô hình
> [superpowers](https://github.com/obra/superpowers)) — **host agent là runtime**, engine chỉ là đường
> phụ headless/CI. Xem [MIGRATION.md](./MIGRATION.md) (Phase A–E) và [README.md](./README.md). Vì vậy
> nhiều phê phán "engine rỗng" bên dưới đã **mất trọng số**: engine không còn là lõi.
>
> Phần còn giữ giá trị: Cost (§pricing hardcode), Testing (coverage thật vẫn thấp), Publishing
> (scope `@x` placeholder). Giữ nguyên văn bên dưới làm hồ sơ lịch sử — **không sửa số liệu cũ**.
>
> ---
>
> Đánh giá độc lập với tư cách technical peer, dựa trên kiểm tra trực tiếp source code
> (không dựa vào README/CHANGELOG). Mục tiêu: chỉ ra khoảng cách giữa **tuyên bố** và
> **thực tế** trên mọi khía cạnh — git, coding, plan, cost, preview, testing, publishing, security.
>
> **Ngày:** 2026-06-28 · **Commit nền:** `08e7f87`

---

## TL;DR

> **aix là một skill-registry + provider-compiler tốt, được đóng gói marketing như một
> "autonomous AI engineering platform" — nhưng phần "autonomous" thì không ghi nổi một file,
> không đếm nổi một đô, và không có lấy một test.**

Phần lõi giá trị (163 skills, registry Zod, provider compiler, kb-server) là **thật và chạy được**.
Phần engine tự động (điểm bán hàng chính) **rỗng ở những chỗ quan trọng nhất**.

---

## 🔴 Nghiêm trọng — "Autonomous engine" về cơ bản là rỗng

### 1. Không node nào của engine ghi file
`aix run --auto` chạy graph → gọi LLM → nhận code dạng *string* → nhét vào `task.output` rồi dừng.

```
grep -rn "writeFile|mkdir|fs\." packages/engine/src/nodes/  →  0 kết quả
```

"Autonomous SDLC loop" sản xuất ra code **bay hơi, không chạm filesystem**. Đây là khoảng cách
giữa *"agent tự code"* (tuyên bố) và *"agent in code ra biến rồi vứt đi"* (thực tế).

**File:** `packages/engine/src/nodes/coder.ts`

### 2. Mock provider bịa code và báo "thành công"
Không có API key → `MockRuntimeProvider` trả về:

```ts
export function solution(input: unknown): unknown { return input; }
```

…report `usd: 0.001`, `status: 'done'`. Reviewer chấm điểm cái identity function bịa đó, loop "pass".
Người dùng chạy `aix run --auto` không key sẽ thấy *"Score: 9/10, Auto-run complete"* trong khi
**không có gì thật xảy ra**. Silent-failure kinh điển — nên fail loud hoặc in banner "MOCK MODE".

**File:** `packages/providers/src/runtime.ts` → `generateMockResponse()`

### 3. Budget hard-stop là đồ trang trí
- `BudgetTracker.addUsage()` tồn tại nhưng **không được gọi từ engine**.
- `response.usd` / `response.tokens` từ provider **không feed về session**.
- `checkHardStop` đọc `budget.usdSpent` — luôn = `0` trong path auto.

Tính năng an toàn được quảng cáo to nhất ("budget hard-stop USD") **không bao giờ kích hoạt**
trừ khi seed sẵn giá trị. Với user cắm API key thật → **rủi ro tiền bạc thực sự: vòng lặp không có phanh**.

**File:** `packages/core/src/budget.ts` (đúng) ↔ `packages/engine/src/nodes/coder.ts` (không gọi)

---

## 🟠 Plan vs Reality — tài liệu hứa quá lời

| Tuyên bố (README/CHANGELOG) | Thực tế |
|---|---|
| "@x/context — **Tree-sitter** analysis" | Regex thuần (`analyze.ts` toàn `RegExp`). Không có tree-sitter/WASM. |
| "Autonomous engine ... với checkpoints" | LangGraph chạy, nhưng coder không ghi file (xem §1) |
| "budget hard-stop (USD)" | Không wired vào engine (xem §3) |
| "preview: tiered preview (image/HTML)" | `image.ts` = 4 dòng wrap base64 SVG. Cả package ~100 dòng. Stub khoác áo package. |
| "163+ skills, progressive disclosure" | ✅ **Đúng** — phần thật và tốt nhất |

README mô tả product tham vọng hơn artefact 2–3 cấp. Với user → **mất niềm tin** khi phát hiện.

---

## 🟠 Cost

- **Pricing hardcode**: `$3/$15` (Sonnet), `$2.5/$10` (OpenAI) baked cứng trong `runtime.ts`.
  Giá đổi → số liệu sai âm thầm. Và còn chẳng nối vào budget.
- **Không có cap thực**: vòng auto không phanh chi phí ⇒ task lặp 3 lần × N file gọi API thật mà không ai chặn.
- **Dev-loop đắt**: chi phí để xây/sửa repo qua agent + GateGuard cao — mỗi lần bị block phải
  giải trình lại, tốn round-trip.

---

## 🟡 Git — nợ lịch sử vĩnh viễn

- **754 commits**, trong đó 739 từ 6 repo cũ import qua `git subtree`. Toàn bộ lịch sử đó
  **nung vào `.git` (41M) vĩnh viễn**. `imports/` đã gitignore + xóa khỏi index, nhưng
  *history bloat không biến mất* trừ khi `git filter-repo`.
- `imports/` vẫn chiếm **28M trên đĩa** — về sau ai clone tưởng là source thật.
- Quyết định subtree thay vì submodule/reference riêng là sai về lâu dài: clone nặng,
  lịch sử lẫn lộn, `git log` nhiễu.

---

## 🟡 Testing — vi phạm chính rule của dự án

- **1 file test** trong toàn repo. Không cấu hình vitest/jest.
- CLAUDE.md + rules bắt buộc **80% coverage** → thực tế **~0%**.
- CI (`.github/workflows/ci.yml`) chỉ `lint + build`, **không chạy test**.
  "CI passing" = "compile được", không phải "đúng".
- Engine có routing phức tạp (conditional edges, hard-stop, score gate) mà 0 test →
  mọi refactor đi trên dây. Bug node-name LangGraph từng lọt tới runtime chính vì
  không test nào gọi `EngineGraph.run()`.

---

## 🟡 Publishing — 13 package "public" nhưng không thể publish

`private: false` cho cả 13 `@x/*` nhưng:

- **Không `files`** → `npm publish` đẩy cả `src/`, hoặc lỗi.
- **`workspace:*` deps** → publish thô ra literal `"@x/core": "workspace:*"` ⇒ cài về vỡ.
  Cần changesets / `pnpm publish` đúng cách.
- **Không `repository`, không `license` field, không file `LICENSE`** (dù README ghi MIT).
- **Scope `@x`** gần như chắc chắn không sở hữu trên npm → tên đụng/từ chối. `@x` là placeholder.

→ Nên đặt `private: true` cho tới khi thật sự publish, hoặc làm tử tế. Hiện tại là
"publishable trên giấy, vỡ khi thử".

---

## 🟢 Những điểm thật sự tốt (công bằng)

- **Type discipline thật**: `strict` + `exactOptionalPropertyTypes` + `noUncheckedIndexedAccess`
  đều bật. Hiếm repo chịu khó vậy.
- **Security boundary đúng**: `.env` gitignored, không secret nào commit,
  `redact()` bọc cả error body provider. Không phải đồ trang trí.
- **Skill registry (163 skills, Zod, L1/L2/L3)** + provider compiler — lõi có giá trị thật, chạy được.
- **kb-server** (Neo4j + Redis + Meili, health degraded riêng từng service) — phần chỉn chu nhất.

---

## Lộ trình đề xuất (ưu tiên giảm dần)

1. **Coder node ghi file thật** — hoặc đổi tài liệu sang "engine sinh diff để người review".
   Đóng khoảng cách lớn nhất giữa tuyên bố và thực tế.
2. **Wire budget**: gọi `addUsage()` sau mỗi provider call, feed `usd`/`tokens` về session.
3. **Mock mode fail-loud**: banner rõ ràng thay vì giả "done".
4. **Sửa README/CHANGELOG**: bỏ "tree-sitter", hạ tông "autonomous" cho khớp thực tế.
5. **`private: true`** cho tới khi publish nghiêm túc (hoặc thêm `files`/`license`/`repository` + changesets).
6. **Thêm test cho engine**: ít nhất smoke test `EngineGraph.run()` + routing guards.
7. **(Tùy chọn) `git filter-repo`** dọn lịch sử `imports/` nếu muốn repo gọn để chia sẻ.

---

*Báo cáo này phản ánh trạng thái tại commit `08e7f87`. Các con số (754 commits, 41M .git,
28M imports/, 1 test file, 13 package) được đo trực tiếp tại thời điểm đánh giá.*
