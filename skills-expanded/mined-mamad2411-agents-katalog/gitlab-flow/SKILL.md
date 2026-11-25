---
name: gitlab-flow
description: Standard end-to-end workflow for shipping a feature/bugfix from a Jira task to a merged GitLab MR. Use when the user references a Jira task ID (WRA-XX, etc.), asks to "start a task", "create branch from task", "rename branch", "review the last change" / "review change" (optionally with "simplify" keyword, e.g. "review change simplify", to auto-clean before review), "review the whole branch", "commit and push", "create a merge request", "review the MR !N", "post review result to the MR", "fix all issues", or "merge the request".
---

# GitLab Flow (Jira → Code → MR → Merge)

Quy trình chuẩn cho một feature/bugfix mới. Có 2 vai trò: **Developer** (người làm task) và **Reviewer** (người review MR). Skill này hướng dẫn Claude thực hiện đúng từng bước theo prompt mà user gọi.

## Conventions

### Branch naming
- **Default: mọi branch dùng `feature/`** — bất kể task là feature, bug fix, hay hotfix.
- Format: `feature/<TASK-ID>-<short-desc>`
- Bug-fix branches dưới `feature/`: mô tả **trạng thái bug** bằng direction marker (`Duplicate`, `Stale`, `Missing`, `Broken`, `Wrong`, `Slow`) thay vì verb "Fix" — vd `feature/HNCW-311-Duplicate-survey-log`
- **Override**: user chủ động gõ `bugfix/...` hoặc `hotfix/...` trong prompt (Mode A) → skill respect và tạo đúng prefix đó. Skill **KHÔNG** tự động chọn `bugfix/` hay `hotfix/` dựa trên nội dung task.

**Quy tắc `<short-desc>`** (đủ để hiểu task ở first glance, chi tiết để Jira giữ):

| Rule | Detail |
|---|---|
| Độ dài tổng | ≤ 50 ký tự cả branch (target ≤ 40). Vượt → rút thêm |
| Số từ | 2-4 từ key. Filler bị drop |
| Ngôn ngữ | Tiếng Việt không dấu, kebab-case (`-` ngăn cách) |
| Capitalization | **Sentence case STRICT**: chỉ chữ cái đầu của từ đầu tiên trong description viết hoa. **Mọi từ sau (KỂ CẢ viết tắt như `NVKD`, `VAT`, `API`, `JWT`)** đều lowercase. Vd `Bao-cao-ngay-nvkd` (KHÔNG `Bao-cao-ngay-NVKD`), `Vat-discount` (KHÔNG `VAT-discount`), `Gioi-han-domain-account`. TASK-ID giữ nguyên uppercase per Jira convention |
| Drop **type filler** | "Cai-tien", "Update", "Improve", "Fix", "Sua", "Sua-loi", "Them", "Tao", "Add", "Create", "Bo-sung" — đều bỏ. Với bug fix, mô tả **trạng thái bug** (`Duplicate`, `Stale`, `Missing`, `Broken`) thay vì verb "Fix" |
| **KEEP direction marker** | "Cho-phep"/"Allow", "Khong-cho-phep"/"Disallow", "Validate", "Block", "Restrict", "Enforce" — chúng nói **WHAT** behavior. Không có chúng → ambiguous (allow? disallow? validate?) |
| **KEEP context marker** | "Show"/"Display"/"Hide" (UI layer), "Filter"/"Sort"/"Search"/"Calculate" (logic layer), "Sync"/"Migrate"/"Schedule"/"Export"/"Import" (system layer) — chúng nói **TẦNG/CÁCH THỨC** của feature, mà `feature/` prefix không cover. Vd `Show-order-info` rõ hơn `Order-info` (display? backend? API?) |
| Drop scope marker | Tag dạng `[Supermarket - AU]` ở đầu task title KHÔNG đưa vào branch (giữ cho commit scope) |
| Drop constraint phụ | Implementation detail như "áp dụng cho sp non-weight" — bỏ. Đó thuộc commit body / Jira description |
| Ưu tiên giữ | **Direction/Context + Action/Object + Phạm vi** (vd `Allow-qty-0-checkin-checkout`, `Show-order-info-uber-doordash`). Mục tiêu: đọc 1 phát hiểu ngay, không cần Jira |

**Ví dụ áp dụng**:

| Task title (Jira) | ✓ Good branch | ✗ Quá dài / sai |
|---|---|---|
| `WRA-40 Giới hạn domain account khi login` | `feature/WRA-40-Gioi-han-domain` | `feature/WRA-40-Gioi-han-domain-account-khi-login` |
| `SMT-460 [Supermarket - AU] Cải tiến checkin/checkout cho phép sửa số lượng = 0. Áp dụng cho sp KHÔNG phải hàng đổi trọng lượng` | `feature/SMT-460-Allow-qty-0-checkin-checkout` | `feature/SMT-460-Cai-tien-cho-phep-sua-so-luong-0-checkin-checkout-non-weight` |
| `WRA-334 Bug: tính sai VAT đơn có discount` | `feature/WRA-334-Wrong-vat-discount` | `bugfix/WRA-334-Fix-tinh-sai-VAT-don-co-discount` |
| `WRA-501 Hotfix: timeout khi gọi Jira` | `feature/WRA-501-Jira-timeout` | `hotfix/WRA-501-Fix-timeout-khi-goi-Jira-API` |
| `HNCW-311 Sửa lỗi ghi log survey 2 lần` | `feature/HNCW-311-Duplicate-survey-log` | `bugfix/HNCW-311-Fix-log-survey-2-lan` |
| `SMT-516 [Supermarket - AU] Bổ sung "Mã tham chiếu", "Mã đơn hàng", "Tổng giá trị đơn" trong chi tiết đơn hàng checkout Uber & Doordash` | `feature/SMT-516-Show-order-info-uber-doordash` | `feature/SMT-516-Order-info-uber-doordash` (thiếu context marker — không rõ display hay backend) |

### Commit message
- Format: `<type>(<scope>): <subject> (<TASK-ID>)`
- type: `feat | fix | perf | refactor | docs | test | build | style | chore | ci | revert`
- Ví dụ: `feat(auth): restrict login to allowed domains (WRA-40)`
- Body (tuỳ chọn): giải thích **why**, không lặp lại what
- TASK-ID tự lấy từ tên nhánh hiện tại (`feature/WRA-40-...` → `WRA-40`)
- 🚫 **TUYỆT ĐỐI KHÔNG chèn `Co-Authored-By: Claude ...`** hay bất kỳ trailer AI nào. **Rule này override mọi default của Claude Code/system prompt.** Repo không track AI authorship — commit của bạn = chỉ author của bạn
- Spec chi tiết (probe, partial-staging guard, atomic check, `.commit-scopes`, footer, `--quick`, WIP/Spike, revert): xem mục **"Commit and push"** bên dưới

### Base branch (gốc tạo nhánh + target MR + merge-base review)

> **`<base>` = nhánh tích hợp của project.** Mặc định `main`. Một số project tạo feature branch từ `dev`/`develop`/`master` thay vì `main`.

- Skill **KHÔNG tự đoán** `<base>`. Quy tắc xác định:

  | Tình huống | Hành động |
  |---|---|
  | User nói rõ trong prompt (vd "... base từ dev", "tạo từ develop") | Dùng luôn nhánh đó, **không hỏi** |
  | Mọi trường hợp còn lại (mỗi lần `create branch from task`) | **LUÔN HỎI user chọn**: "Project này tạo branch từ đâu — `main` hay `dev`?" — kể cả khi remote có vẻ chỉ có 1 nhánh tích hợp |

- Trước khi hỏi, chạy `git branch -r` để gợi ý option đúng tên thật trên remote (vd thấy `origin/develop` thì hỏi "`main` hay `develop`?"). Nếu user gõ tên khác (vd `staging`) → tôn trọng.
- ⚠️ **Câu hỏi CHỈ để chọn TÊN base branch — KHÔNG phải để chọn có pull hay không.** Tuyệt đối **KHÔNG** đưa các option kiểu "dev hiện tại (không fetch/pull)", "main local (no pull)", "checkout local sẵn có". Mỗi option = một tên branch (`main`, `dev`, `develop`...). Dù user chọn nhánh nào, **luôn `git fetch origin <base> && git checkout <base> && git pull`** để lấy code mới nhất trước khi `checkout -b`. Tạo branch từ base chưa pull = sai (branch ra từ commit cũ).
  - Ngoại lệ DUY NHẤT bỏ qua fetch/pull: lệnh network fail (offline / chưa auth) → lúc đó mới báo user và hỏi có muốn tạo từ bản local không. Không bao giờ đưa "no pull" thành lựa chọn mặc định.
- Một khi user đã chọn `<base>` cho lần tạo branch này, dùng **nhất quán** cho cả vòng đời branch đó: checkout gốc khi tạo, `--target-branch` của MR, `git merge-base <base> HEAD` khi review whole branch, và checkout sau khi merge.
- ⚠️ **Bộ nhớ `<base>` chỉ tồn tại trong 1 session.** Nếu trigger sau (vd `create a merge request`, `review the whole branch`, `merge the request`) chạy ở **session khác** với lúc tạo branch → skill **KHÔNG còn nhớ** `<base>`. Lúc này **phải HỎI lại** user (`main` hay `dev`), tuyệt đối **không mặc định `main`**. Chỉ bỏ qua hỏi nếu `<base>` đã được xác lập trong chính session đang chạy.

### Target branch
- MR luôn merge vào `<base>` (mặc định `main`) trừ khi user chỉ định khác

### Output language (review & report)

**Mặc định tiếng Việt** cho mọi output của các trigger review/report — kể cả khi user gõ trigger bằng tiếng Anh ("review the last change", "review change simplify", "review the whole branch", "review the MR !N", "post review result to the MR"...). User KHÔNG cần phải nhắc lại bằng tiếng Việt mới nhận được output tiếng Việt.

| Áp dụng cho | Phần phải tiếng Việt |
|---|---|
| `review the last change` / `review change` (± simplify) | Tóm tắt Step 0 simplify pass + danh sách issue `#1`, `#2`... (vấn đề + đề xuất fix) |
| `review the whole branch` | Tóm tắt aggregate từ 3 agent + danh sách fix đã làm + status test/typecheck |
| `review the MR !<N>` | Verdict + danh sách issue (cả "trạng thái issue cũ" và "issue mới") |
| `post review result to the MR` | Nội dung Markdown comment đăng lên GitLab |
| Tóm tắt sau `fix all issues` | Danh sách issue đã fix + đề xuất commit message |

**Ngoại lệ giữ tiếng Anh** (không Việt hóa):
- `type`/`scope` trong commit message (chuẩn CC: `feat`, `fix`, `auth`, `billing`...)
- Tên technical/identifier: tên file, function, biến, branch, MR title prefix
- Status keyword cố định: `APPROVE` / `REQUEST_CHANGES` / `COMMENT`, `✓ Resolved` / `❌ Still open` / `⚠️ Partially`
- Tên agent / role / tool: `Reuse`, `Quality`, `Efficiency`, `glab`, `git`

**Switch language**: user trả lời / tiếp tục bằng ngôn ngữ khác (English chẳng hạn) → từ message đó trở đi mới đổi sang ngôn ngữ user dùng. Không tự đoán "trigger English ⇒ output English".

## Triggers & Procedures

### "create branch <name>" hoặc "create branch from task <TASK-ID>..."

**Step 1 — Detect input mode** (parse phần text sau `create branch ...`):

| Input pattern | Mode | Hành động |
|---|---|---|
| Có prefix branch type + slug, vd `feature/HNCW-313-Bao-cao-ngay-nvkd` | **A — Full branch** | Dùng **nguyên si**, KHÔNG đề xuất, KHÔNG sửa (kể cả nếu input violate convention — chỉ warn) |
| Slug kebab-case không prefix, vd `HNCW-313-Bao-cao-ngay-nvkd` | **B — Pre-formatted slug** | Auto thêm `feature/` (convention nội bộ chỉ dùng `feature/`). **KHÔNG** bóc tách lại |
| Raw Jira title (có dấu / space / `[...]` / `(...)`), vd `HNCW-313 [Vận hành] Tạo báo cáo ngày cho NVKD(IT-10212)` | **C — Raw title** | Bóc tách → đề xuất 1-2 candidate → hỏi user pick |
| Chỉ TASK-ID, vd `HNCW-313` | **D — Bare ID** | Hỏi user description ngắn (2-4 từ) |

**Technical detection** — phần text sau `<TASK-ID>`:
- Match `^-[A-Za-z0-9-]+$` (gạch đầu, alphanumeric + gạch nối, không space/dấu) → **Mode B**
- Match `^/[A-Za-z0-9-/]+$` với prefix `feature|bugfix|hotfix/` → **Mode A**
- Có space / dấu tiếng Việt / `[`, `(`, ... → **Mode C**
- Trống → **Mode D**

> **NGUYÊN TẮC**: Mode A và B = user đã chủ động format → **respect tuyệt đối**, không tự sinh khác. Mode C và D mới được phép bóc tách + đề xuất.

**Step 2 — Bóc tách** (chỉ Mode C):

- Tách `TASK-ID` (pattern `[A-Z][A-Z0-9]+-\d+`)
- **Branch type: luôn `feature/`** — bất kể task là feature, bug fix, hay hotfix. Convention nội bộ chỉ dùng 1 prefix. Chỉ tạo `bugfix/` hoặc `hotfix/` khi user **chủ động gõ rõ** prefix đó trong Mode A (vd `create branch from task bugfix/HNCW-311-Duplicate-survey-log`).
- Bỏ scope marker đầu title (`[Supermarket - AU]`, `[Mobile]`...)
- Bỏ reference ticket khác (`(IT-12468)`, `(linked WRA-9)`)
- Drop type filler (xem rule mục Branch naming)
- **KEEP direction marker** (`Cho-phep`, `Allow`, `Validate`, `Block`, `Disallow`, `Restrict`, `Enforce`)
- Lấy 2-4 từ key: **direction + action + phạm vi**

**Step 3 — Đề xuất** (Mode C, D):

- Đưa 1-2 candidate kèm length character count
- **DỪNG, hỏi user pick option nào** (hoặc override description bằng tên user tự gõ)
- **KHÔNG được tự tạo branch** trước khi user xác nhận. Tránh tình huống user phải rename sau

**Step 4 — Tạo branch** (mọi mode):

1. Đảm bảo working tree sạch (`git status`); có thay đổi chưa commit → hỏi user trước khi tiếp tục
2. Xác định `<base>` theo mục **Base branch**: trừ khi user đã nói rõ trong prompt, **HỎI user chọn TÊN base branch (`main` hay `dev`)** (chạy `git branch -r` trước để gợi ý đúng tên nhánh thật). Câu hỏi chỉ chọn tên nhánh — **KHÔNG** đưa option "không pull"/"local sẵn có". Sau khi chọn, **LUÔN** lấy code mới nhất rồi mới tạo branch: `git fetch origin <base> && git checkout <base> && git pull` (áp dụng cho mọi base, kể cả `dev`)
3. Tạo branch (luôn nhánh `<base>` đang checkout):
   - Mode A/B: `git checkout -b <input-nguyên-si>` (Mode B: thêm prefix `feature/` mặc định)
   - Mode C/D: `git checkout -b <branch-user-pick>` (chỉ sau khi user đã chọn ở Step 3)
4. Báo lại tên branch + length character count

**Edge case**:

| Tình huống | Xử lý |
|---|---|
| Mode A/B branch >50 chars | Warn user nhưng **KHÔNG ép sửa** — user đã chủ động chọn |
| Mode C sau khi trim vẫn >50 chars | Đề xuất viết tắt (`qty` thay `so-luong`, `co` thay `checkout`) hoặc bỏ phạm vi |
| TASK-ID không match pattern `[A-Z][A-Z0-9]+-\d+` | STOP, hỏi user |
| Cần branch type khác `feature/` | User phải **gõ rõ prefix** trong input, vd `create branch from task bugfix/HNCW-311-Duplicate-survey-log` (Mode A — skill dùng nguyên si). Skill **KHÔNG** tự suy đoán `bugfix/`/`hotfix/` từ nội dung task |
| User muốn đổi tên branch sau khi skill đã tạo | Dùng trigger riêng `rename branch <new-name>` (xem mục bên dưới). Không tự rename bằng `git branch -m` mà không update upstream → sẽ phá `commit and push` |

### "rename branch <new-name>" hoặc "rename branch sang <new-name>"

User không thích tên branch skill vừa tạo và muốn đổi. Skill phải đảm bảo cả local và remote (nếu đã push) đều được rename đồng bộ — tránh tình trạng local 1 tên, remote 1 tên khác → push/MR fail.

**Step 1 — Detect trạng thái**:

```bash
git branch --show-current                              # tên local hiện tại
git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null  # upstream (nếu có)
```

| Trạng thái | Hành động |
|---|---|
| Branch chưa push (chưa có upstream) | Rename local thuần: `git branch -m <new-name>`. Xong, không cần đụng remote |
| Branch đã push (có upstream) | Cần rename cả 2 phía (Step 2-3) |

**Step 2 — Rename local + push tên mới**:

```bash
git branch -m <new-name>
git push -u origin <new-name>
```

**Step 3 — Xóa branch cũ trên remote**:

Hỏi user: "Branch cũ `<old-name>` còn tồn tại trên remote. Xóa không?"
- Yes → `git push origin --delete <old-name>`
- No → giữ lại (nhưng warn: 2 remote branch trỏ cùng commit, có thể confuse reviewer)

**Step 4 — Verify**:
```bash
git branch -vv                  # xem local + upstream mới
git ls-remote --heads origin    # check remote không còn old-name (nếu đã xóa)
```

**Lưu ý**:
- KHÔNG dùng `git branch -m` thuần khi branch đã push — sẽ break upstream tracking
- Nếu đã có MR mở trên branch cũ: rename remote sẽ làm MR đứng (URL không đổi nhưng source branch không tồn tại). Phải đóng MR cũ + tạo MR mới với branch mới, hoặc dùng `glab mr update <N> --source-branch <new-name>` nếu glab support

### Sinh code từ mô tả task
- Khi user paste mô tả task Jira làm prompt, đọc kỹ và xác nhận lại scope trước khi code nếu có chỗ mơ hồ
- Code theo convention của project (tham khảo CLAUDE.md nếu có, hoặc đọc file gần khu vực sửa để bắt chước style)
- Không thêm tính năng/refactor ngoài scope task
- Sau khi xong, tóm tắt ngắn các file đã thay đổi

### "review the last change" / "review change" (+ optional "simplify")

Trigger match là lenient: thêm từ `simplify` bất kỳ vị trí trong câu để bật Step 0; không có thì bỏ qua Step 0.

**Step 0 — Simplify pass** (chỉ chạy khi trigger chứa `simplify`):

1. Capture uncommitted + staged diff (`git diff` và `git diff --cached`). Empty → báo skip Step 0 và sang Step 1.

2. Scan diff theo 3 góc nhìn **Reuse / Quality / Efficiency** — danh sách flag chi tiết dùng chung với bảng Phase 2 của `review the whole branch` (xem section bên dưới). Inline Claude, không spawn agent vì scope hẹp.

3. **Auto-fix trực tiếp** mọi finding rõ ràng — false positive thì skip, không cãi, không hỏi user từng issue. Fix độc lập ở các file khác nhau → batch parallel trong 1 message.

4. Báo tóm tắt số issue đã fix + file đã đụng (hoặc "code đã sạch") rồi sang Step 1. **KHÔNG tự commit** — fix nằm ở working tree, gộp chung với review issues user fix sau.

**Step 1 — Capture diff + NẠP CONTEXT** (đừng review diff trong "ống hút"):

1. Capture diff: `git diff` (hoặc `git diff HEAD` nếu đã staged). Trong simplify mode, đây là diff sau-fix.
2. **Đọc FULL các file đã đổi** (không chỉ diff hunk) — để thấy code xung quanh, import, hàm gọi tới. Review chỉ-diff là nguyên nhân #1 gây finding sai (đoán những thứ không nhìn thấy).
3. **Grounding convention**: đọc `CLAUDE.md` (nếu có) + 1-2 file lân cận cùng thư mục/module để học convention THẬT của repo — đừng áp convention generic.
4. **Grounding task**: nếu mô tả task (Jira) đã có trong hội thoại → dùng làm chuẩn "logic đúng/đủ chưa". Nếu CHƯA có và định đánh giá logic/edge-case → hỏi user 1 câu ngắn về mục tiêu task, hoặc nói rõ "review này chỉ xét quality/efficiency, không phán logic vì thiếu spec".

**Step 2 — Review** theo các tiêu chí (chỉ flag khi đã đọc đủ context ở Step 1):
- Logic đúng với mô tả task không *(chỉ phán khi có task context — xem Step 1.4)*
- Có edge case nào chưa cover không
- Có vi phạm convention/coding standard không *(theo convention thật đã đọc, không generic)*
- Có code thừa, dead code, hoặc abstraction không cần thiết
- Có lỗ hổng bảo mật (input validation, auth bypass, injection) không
- Có ảnh hưởng performance đáng kể không

**Step 3 — Verify findings (lọc false positive TRƯỚC khi báo)**: với mỗi finding, tự kiểm:
- Gắn được **`file:line` cụ thể** không? Không → bỏ.
- **Chứng minh được bằng code đã đọc** (không phải suy diễn từ diff) không? Không chắc → bỏ hoặc hạ thành "cần xác nhận", đừng list như lỗi chắc chắn.
- Đề xuất fix có **thật sự áp dụng được** với codebase này không (helper/util mình gợi ý có tồn tại không)? → verify rồi mới đề xuất.

> Thà báo 3 issue **chắc** còn hơn 10 issue nửa đoán. Finding không qua được Step 3 thì **không đưa vào danh sách**.

**Step 4 — Báo cáo** dưới dạng danh sách có đánh số: `#1`, `#2`, ... mỗi issue kèm `file:line` + vấn đề + đề xuất fix, để user dễ tham chiếu.

**Lưu ý — chọn đúng độ sâu (đừng kỳ vọng sai vào công cụ nhẹ)**:
- Trigger này cố tình **lightweight** (inline, không spawn agent) → hợp để **liếc nhanh** đoạn vừa sửa. Dù đã nạp context + verify, nó vẫn nông hơn review chuyên sâu.
- Muốn **chính xác/sâu hơn**: dùng skill built-in **`/code-review`** (đọc file thật + adversarial verify, loại false positive mạnh hơn) hoặc trigger **`review the whole branch`** (3 agent song song đọc full file).
- Diff lớn (>500 dòng) hoặc nhiều commit → **bắt buộc** chuyển sang `review the whole branch`, đừng cố review inline.

### "Commit and push"

Spec đầy đủ Conventional Commits + Jira ID + push gate. Self-contained: không cần cài skill `commit` riêng.

> **Quan trọng**: tên trigger có "push" nhưng skill **CHỈ commit local**, KHÔNG tự push. Push là hành động remote → bắt buộc hỏi user xác nhận.

**Trigger phụ**: thêm `--quick` ("commit and push --quick", "quick commit") → kích Quick mode (xem cuối section).

#### Inputs

| Input | Rule |
|---|---|
| TASK-ID | Auto-extract từ tên nhánh hiện tại (`feature/WRA-9-...` → `WRA-9`). Pattern `[A-Z][A-Z0-9]+-\d+`. Không match → STOP, hỏi user |
| Repo language | Tiếng Việt (theo `git log`) — áp dụng cho `subject` và `body` |
| Detect "quick" intent | User nói "nhanh" / "quick" / "tạm" / "small" / "fast" → suggest `--quick` trước khi commit |

#### Behavior

| Rule | Detail |
|---|---|
| Probe trước khi quyết định | Luôn chạy Step 1 đầy đủ — không skip kể cả commit nhỏ |
| Không bao giờ guess `type`/`scope` | Không chắc → STOP, hỏi user. Không coin-flip |
| Quality > speed | 1 câu hỏi xác nhận đỡ 1 commit sai format |

#### Process

**Step 1 — Probe repo state** (parallel calls trong 1 message):

| Call | Mục đích |
|---|---|
| `git status` (không `-uall`) | Untracked + modified files |
| `git diff --cached` | Staged hunks only |
| `git diff` | Unstaged hunks only — tách biệt để detect partial-staging |
| `cat "$(git rev-parse --show-toplevel)/.commit-scopes"` | Scope allowlist (works từ subdir) |

**Step 2 — Partial-staging guard**:

| Khi | Hành động |
|---|---|
| File xuất hiện cả ở index lẫn worktree (`MM` trong `git status`) | STOP, hỏi user |
| User: commit staged-only | Tiến hành với index hiện tại |
| User: stage rest then combine | `git add <files>` rồi commit |
| Default | KHÔNG tự `git add` unstaged hunks (user có thể đã `git add -p` cố ý) |

**Step 3 — Atomic check**:

| Khi | Hành động |
|---|---|
| Single logical change span N modules (vd add field: migration + model + API + UI) | Atomic — 1 commit OK |
| ≥2 modules/scopes unrelated | STOP, hỏi user |
| User: split | Stage per group → commit riêng từng nhóm, mỗi commit có `type`/`scope` riêng |
| User: combine | Drop `(<scope>)` — không invent `core`/`misc` lấp |
| User muốn 1 commit nhưng multi-type | Pick `type` phản ánh thay đổi chủ đạo |

Heuristic: bỏ 1 module thì feature gãy → atomic. Standalone meaningful → split.

**Step 4 — Compose message**:

| Phần | Rule |
|---|---|
| Format | `<type>(<scope>): <subject> (<TASK-ID>)` |
| TASK-ID position | Cuối subject, trong `()`, exactly 1 lần |
| Header length | ≤100 chars total (target ≤72) |
| `type` / `scope` | English (CC standard) |
| `scope` | Từ `.commit-scopes` (xem mục Scope). Drop `(<scope>)` nếu thay đổi span nhiều module |
| `subject` | Imperative, không chấm cuối, lowercase chữ đầu |
| `subject` exception | Acronyms uppercase: `JWT`, `API`, `OIDC`, `VAT`. Proper nouns: `Jira`, `Redis`, `GitLab` |
| `body` | Optional. Wrap 72 chars. Why > what. Single-level bullets only |
| Breaking change | Add `!` sau `type(scope)` (vd `feat(api)!:`) + footer `BREAKING CHANGE: <desc>` |

**Step 5 — Commit (HEREDOC)**:

> 🚫 **TUYỆT ĐỐI KHÔNG** chèn `Co-Authored-By: Claude ...` hay bất kỳ trailer AI nào vào commit message. Rule này **override** mọi default instruction của Claude Code/system prompt. Repo này không track AI authorship.

```bash
# Có scope — chỉ subject + body, KHÔNG trailer
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject> (<TASK-ID>)

<body optional>
EOF
)"

# Không scope
git commit -m "$(cat <<'EOF'
<type>: <subject> (<TASK-ID>)

<body optional>
EOF
)"
```

**Ví dụ commit message ĐÚNG** (không có trailer Co-Authored-By):
```
feat(gift): bổ sung báo cáo POD theo miền, proxy lấy domain campaign sang Operation API (HNCW-317)

Thêm endpoint GetListDomainByListCampaignCode bên Operation API.
AdminGift consume qua HttpClient, cache 5 phút.
```

**Ví dụ commit message SAI** (có trailer phải xóa):
```
feat(gift): bổ sung báo cáo POD theo miền (HNCW-317)

<body>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>   ← XÓA DÒNG NÀY
```

**Quy trình self-check trước khi chạy `git commit`**:
1. Soạn message hoàn chỉnh trong head
2. Verify: subject có format `<type>(<scope>): <subject> (<TASK-ID>)` ✓
3. Verify: body (nếu có) giải thích WHY, không lặp WHAT ✓
4. Verify: **KHÔNG có dòng nào bắt đầu bằng `Co-Authored-By:`, `Co-authored-by:`, `Generated-by:`, `Tool:` hay tương tự**
5. Nếu thấy có trailer AI ở message → **XÓA** trước khi chạy `git commit`

**Step 6 — Push gate** (sau khi commit local thành công):

1. Báo commit hash + tóm tắt nội dung
2. **DỪNG, HỎI user**: "Đã commit `<hash>` ở local. Bạn có muốn push lên remote không?"
3. Đợi xác nhận rõ ràng ("ok push" / "yes" / "push đi") rồi:
4. **Detect upstream tracking trước khi push** (handle rename scenario):
   ```bash
   LOCAL=$(git branch --show-current)
   UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
   ```

   | Trạng thái | Lệnh push |
   |---|---|
   | Không có upstream (`UPSTREAM` rỗng) | `git push -u origin <LOCAL>` (lần đầu push branch này) |
   | `UPSTREAM` = `origin/<LOCAL>` (tên local match remote) | `git push` (bình thường) |
   | `UPSTREAM` = `origin/<old-name>` (tên local KHÁC upstream) | **Rename scenario detected**. STOP, báo user: "Local branch `<LOCAL>` đang track `<UPSTREAM>` — có vẻ branch đã được rename. Cần dùng trigger `rename branch <LOCAL>` để sync remote, KHÔNG nên push trực tiếp" |

5. Sau khi push thành công: báo URL push + gợi ý bước tiếp (vd `review the whole branch` hoặc `create a merge request`)
6. **KHÔNG tự push** kể cả khi trigger có "push" trong tên
7. **KHÔNG ép push qua rename scenario** — bắt user đi qua `rename branch` flow để cleanup remote đúng cách

#### Allowed types

| Type | Ý nghĩa | Version bump |
|---|---|---|
| `feat` | Tính năng mới | MINOR (1.X.0) |
| `fix` | Sửa bug | PATCH (1.0.X) |
| `perf` | Cải thiện performance | PATCH |
| `refactor` | Refactor không đổi behavior | — |
| `docs` | Tài liệu | — |
| `test` | Thêm/sửa test | — |
| `build` | Build system / dependency / packaging | — |
| `style` | Format code (whitespace, lint) | — |
| `chore` | Maintenance, không fit type khác | — |
| `ci` | CI/CD config | — |
| `revert` | Revert commit cũ | — |

> Breaking change là *modifier*, không phải type riêng. Suffix `!` hoặc footer `BREAKING CHANGE:` → MAJOR bump (X.0.0).

#### Footer

Vị trí: sau body, ngăn bằng dòng trắng. Format: `Token: value` (CC) hoặc `Token #issue` (GitHub-style).

| Footer | Khi dùng |
|---|---|
| `BREAKING CHANGE: <desc>` | Bắt buộc khi header có `!`. Mô tả impact + migration |
| `Closes <TASK-ID>` | Trigger Jira-GitLab auto-close khi merge. Skip nếu đã auto-close từ subject mention (kiểm tra 1-2 ticket merged gần đây để confirm) — tránh trigger 2 lần |
| `Refs <TASK-ID>` | Reference Jira khác (related nhưng không close) |
| `Co-authored-by: Name <email>` | Real pair-programming. KHÔNG auto-insert AI |
| `Reviewed-by: Name <email>` | Optional — chỉ nếu team convention |

| Rule | Áp dụng |
|---|---|
| Đừng lặp Task ID | Đã có trong subject `(<TASK-ID>)` rồi → bỏ ở footer trừ khi cần keyword `Closes`/`Refs` |
| Token case | PascalCase hoặc kebab-case (`Reviewed-by`, `Co-authored-by`); `BREAKING CHANGE` uppercase per spec |

#### Scope

**Lookup**: đọc `.commit-scopes` ở repo root → fallback `git log --pretty=format:%s | grep -oE '\([^)]+\):' | sort -u`.

| Convention | Detail |
|---|---|
| Case | lowercase, kebab-case (`-`, không `_`) |
| Token count | Prefer 1 token; compound `<primary>-<sub>` để narrow (vd `admin-jobs`, `team-digest`) |
| Suffix drop | `email_service` → `email`, `ai_engine` → `ai`, Java/.NET `Service`/`Manager` tương tự |

| Quyết định new scope | Hành động |
|---|---|
| Synonym đã có trong `.commit-scopes` | Reuse — đừng coin trùng (`auth` vs `authentication` vs `login`) |
| Genuinely new concept | Add vào `.commit-scopes` cùng PR với commit đầu tiên dùng nó |
| Không update file được lúc đó (hotfix, fast flow) | Drop `(<scope>)` (valid CC) hoặc dùng `--quick`. Update `.commit-scopes` trước khi merge |

> 🚫 Đừng invent generic scope (`core`, `misc`) để fill format. No-scope flags "needs categorization"; invented scope masks the gap.

**`.commit-scopes` file**: plain text — 1 scope/dòng, dòng `#` là comment, blank/whitespace trimmed.

#### Quick mode

**Trigger**: thêm `--quick` ("commit and push --quick" / "quick commit").

| Aspect | Rule |
|---|---|
| Format | `<type>: <subject> (<TASK-ID>)` — không scope, ever |
| Body | Skip, kể cả meaningful |
| Header length | ≤72 chars (chặt hơn normal) |
| Mandatory | `type`, TASK-ID, imperative subject, không chấm cuối |

**Use for**: hotfix · dep bump · typo fix · internal tool · small chore
**Don't use for**: `feat`/`refactor` cần why-body · breaking change · multi-module change (drop `--quick`, dùng no-scope normal)

> Dep bump → `build` (build system / packaging) per CC spec, không `chore`. `chore` chỉ cho housekeeping không fit type khác.

#### WIP / Spike

| Element | Rule |
|---|---|
| Type | `chore` (always) |
| Keyword | `wip` hoặc `spike` — lowercase, từ đầu của subject |
| Scope | None |
| Format | `chore: <wip\|spike> <desc> (<TASK-ID>)` |

```
chore: wip refactor luồng auth (WRA-123)
chore: spike test kết nối Redis (WRA-999)
```

| Lifecycle | Rule |
|---|---|
| WIP → main | **Bắt buộc** squash/rebase trước merge. Main không bao giờ giữ chuỗi `wip` raw |
| Spike → main | Giữ nếu document được decision; xóa nếu throwaway — quyết trong PR review |
| Hotfix | KHÔNG — đó là `fix:` thật |

> Pair tự nhiên với `--quick`: "commit and push --quick" (no scope, no body, lightweight).

#### Examples

**feat with body**:
```
feat(auth): thêm JWT refresh token rotation (WRA-201)

Implement sliding expiration cho refresh token, revoke
token cũ khi phát hiện reuse.
```

**fix one-liner**:
```
fix(billing): tính sai VAT cho đơn hàng có discount (WRA-334)
```

**refactor with body**:
```
refactor(order): tách OrderService thành các handler nhỏ (WRA-412)

Không đổi behavior, chuẩn bị cho việc thêm payment provider.
```

**breaking change**:
```
feat(api)!: đổi response format endpoint /users (WRA-450)

BREAKING CHANGE: field `user_id` đổi thành `id`. Clients
phải cập nhật trước khi deploy.
```

**revert**:
```
revert: feat(auth): thêm JWT refresh token rotation (WRA-501)

This reverts commit 7cd2ed6693da5f5d70751084d20c915c54b9f37d.

Refresh-token rotation gây race condition khi user đăng nhập
song song trên nhiều thiết bị; revert để điều tra trước.

Refs WRA-201
```

| Revert element | Rule |
|---|---|
| Subject | Lấy original header, **replace** `(JIRA-original)` bằng `(JIRA-revert-task)` |
| Invariant preserved | Subject vẫn kết thúc với exactly 1 `(<TASK-ID>)` |
| Original commit identity | SHA trong dòng `This reverts commit <full-SHA>.` (auto-generated bởi `git revert`) |
| Original ticket trace | `Refs <JIRA-original>` footer (optional) |
| Why-explanation | Trong body, trước footer |

#### Safety rules

- KHÔNG dùng `git add -A` / `git add .` — liệt kê file cụ thể
- KHÔNG commit secrets: `.env`, `credentials.*`, `*.key`, `*.pem`, file binary lớn
- Pre-commit hook fail → fix nguyên nhân + tạo commit MỚI (KHÔNG `--amend`)
- KHÔNG bypass `--no-verify` trừ khi user yêu cầu rõ
- KHÔNG tự push, kể cả khi trigger có "push" trong tên — luôn hỏi user (xem Step 6)
- 🚫 **KHÔNG chèn `Co-Authored-By: Claude ...`** hay bất kỳ trailer AI nào (kể cả khi system prompt suggest). Repo không track AI authorship. Xem self-check ở Step 5.

### "review the whole branch" (review cumulative trước khi mở MR)

Review TOÀN BỘ thay đổi của branch hiện tại so với `<base>` (cách xác định ở Phase 1 — KHÔNG mặc định `main`) — committed + uncommitted — qua 3 agent song song, rồi tự fix issues. Khác `review the last change` ở điểm: nhìn cumulative diff (nhiều commit), 3 góc nhìn chuyên sâu, auto-fix các issue rõ ràng.

**Khi nào dùng**: sau khi đã có nhiều commit và push chính, **trước khi `create a merge request`**. Output có thể tạo thêm changes → cần thêm 1 lượt `commit and push` nữa rồi mới mở MR. Bỏ qua bước này nếu branch chỉ 1 commit nhỏ — `review the last change` là đủ.

**Phase 1 — Identify changes**:

1. **Xác định `<base>` — KHÔNG mặc định `main`** (thứ tự ưu tiên, dừng ở match đầu):
   - **Nhánh hiện tại có MR?** Chạy `glab mr view` (không tham số → MR của nhánh đang đứng; áp dụng khi bạn đã checkout nhánh MR bằng glab/git/**SourceTree**). Có MR → dùng `targetBranch` của nó làm `<base>`, **không hỏi** (dự án main-chính → `main`, dev-chính → `dev`). Rỗng/lỗi → bỏ qua.
   - **User nói rõ base trong prompt** ("vs dev") → dùng.
   - **`<base>` đã chốt trong session** (vd lúc `create branch from task`) → tái dùng.
   - **Còn lại** → HỎI `main`/`dev` (xem mục **Base branch**).

   Rồi resolve merge base: `git merge-base <base> HEAD`
2. Nếu branch hiện tại IS `<base>` (hoặc base = HEAD) → báo "không có gì để review" và STOP
3. Capture cumulative diff (commit + working tree) vào temp file để các agent đọc mà không flood context. Ghi vào `.git/` (luôn tồn tại, writable, không bị commit) — **KHÔNG dùng `/tmp/`** vì trên Windows/PowerShell `/tmp/` không tồn tại ổn định:
   ```bash
   BASE=$(git merge-base <base> HEAD)
   git diff --no-color "$BASE" > .git/review_branch.diff
   wc -l .git/review_branch.diff
   ```
4. Capture danh sách file untracked (diff không bao gồm):
   ```bash
   git ls-files --others --exclude-standard > .git/review_branch_new.txt
   ```
5. Stat tóm tắt để spot-check:
   ```bash
   git diff --stat "$BASE"
   ```

**Phase 2 — Launch 3 agent SONG SONG** (1 message, 3 Agent tool calls):

Mỗi agent nhận: đường dẫn diff (`.git/review_branch.diff`) + đường dẫn new-files (`.git/review_branch_new.txt`) + context "cumulative diff branch <name> against <base>".

| Agent | Tập trung | Flag điển hình |
|---|---|---|
| **Code Reuse** | Tìm utility/helper đã có để thay function mới viết | New function duplicates existing helper, inline logic could use existing util (string manipulation, path handling, env checks, type guards) |
| **Code Quality** | Hacky patterns | Redundant state, parameter sprawl, copy-paste với biến thể nhỏ, leaky abstraction, stringly-typed (raw strings nơi đã có enum/constant), unnecessary JSX nesting, nested conditionals 3+ levels, unnecessary comments giải thích WHAT |
| **Efficiency** | Performance / resource | N+1, missed concurrency (independent ops chạy tuần tự), hot-path bloat, no-op updates trong polling loops, unnecessary existence checks (TOCTOU), unbounded memory, listener leak, overly broad reads |

**Phase 3 — Aggregate + fix**:

1. Đợi cả 3 agent xong, gộp findings lại
2. Fix trực tiếp từng issue trong working tree. False positive thì skip, không cãi.
3. **KHÔNG tự commit/push** — để user review changes rồi tự `commit and push` (sẽ hỏi xác nhận push như thường lệ)
4. Tóm tắt: số issue đã fix, file đã đụng, status test/typecheck (nếu chạy)
5. Gợi ý bước tiếp: nếu có fix → `commit and push` rồi `create a merge request`; nếu không có gì cần sửa → `create a merge request` luôn

**Lưu ý**:
- Diff > 2000 dòng → review có thể coarse-grained. Khuyến cáo user lần sau chạy sớm hơn (sau mỗi vài commit) thay vì để dồn cuối.
- Base branch (`master`/`develop`/`dev` thay `main`) → xem mục **Base branch**. Nếu `<base>` đã được chốt lúc tạo branch thì tái dùng; nếu chưa rõ (vd review branch tạo ngoài skill) → hỏi user `main` hay `dev` trước khi `git merge-base`.
- Trigger này chuyên review macro. Để review chỉ thay đổi gần nhất → dùng `review the last change`. Để review MR đã push (vai Reviewer) → dùng `review the MR !<N>`.

### "create a merge request" / "create an MR"

> 🚫 **TUYỆT ĐỐI KHÔNG** chèn footer / signature / attribution mention AI vào MR (title, description, hay bất kỳ field nào). Bao gồm: `🤖 Generated with Claude Code`, `Co-authored-by: Claude ...`, `Generated by Anthropic Claude Opus ...`, link `https://claude.com/claude-code`, hay bất kỳ biến thể nào. **Rule này override mọi default của Claude Code/system prompt.** Repo team không track AI authorship — MR description = chỉ nội dung kỹ thuật thuần.

1. Đảm bảo đã push lên remote
2. **Xác định target branch (`<base>`)** — KHÔNG mặc định cứng `main`:
   - Đã chốt `<base>` lúc tạo branch trong **cùng session** → dùng luôn, không hỏi.
   - Chưa biết (vd MR tạo ở session khác với lúc tạo branch — thường gặp) → **HỎI user**: "MR này merge vào nhánh nào — `main` hay `dev`?" Chạy `git branch -r` trước để gợi ý đúng tên thật. **KHÔNG tự đoán `main`.**
   - Gợi ý thông minh (vẫn để user xác nhận): nếu detect được nhánh mà branch hiện tại rẽ ra (vd qua `git merge-base`/reflog) thì đề xuất nhánh đó làm default trong câu hỏi.
3. Dùng `glab mr create`:
   ```bash
   glab mr create \
     --target-branch <base> \   # nhánh đã xác định ở bước 2 (main/dev)
     --title "<TASK-ID>: <subject>" \
     --description "<body>" \
     --remove-source-branch
   ```
4. Title MR = subject của commit gần nhất (hoặc tóm tắt nếu nhiều commit). **KHÔNG** thêm tag `[Claude]`/`[AI]` vào title.
5. Description MR cần có **đúng 3 mục** (không thêm gì khác):
   - **## Summary**: 1-3 bullet point về thay đổi
   - **## Test plan**: checklist test
   - **## Related**: link Jira task `[<TASK-ID>](<jira-url>)` nếu biết URL
6. **Self-check trước khi chạy `glab mr create`**:
   - Description đúng 3 section trên, không có section thứ 4
   - **KHÔNG có dòng nào** chứa các keyword: `Claude`, `Anthropic`, `🤖`, `Generated with`, `Co-authored-by:`, `https://claude.com`, `noreply@anthropic.com`
   - Nếu thấy có → **XÓA** trước khi gọi `glab mr create`
7. Trả về URL của MR và số `!N` (không thêm comment giới thiệu AI sau khi MR tạo xong)

**Ví dụ description ĐÚNG**:
```markdown
## Summary
- Thêm endpoint GetListDomainByListCampaignCode trong Operation API
- AdminGift consume qua HttpClient, cache 5 phút
- Add báo cáo POD theo miền ở RegionPodReport page

## Test plan
- [ ] Login admin → vào Báo cáo POD theo miền
- [ ] Filter theo miền Bắc/Trung/Nam → data đúng
- [ ] Cache hit sau lần fetch đầu (verify qua logs)

## Related
- [HNCW-317](https://jira.fastlink.vn/browse/HNCW-317)
```

**Ví dụ description SAI (phải xóa các dòng có ❌)**:
```markdown
## Summary
- ...

## Test plan
- ...

## Related
- HNCW-317

---  ❌ XÓA
🤖 Generated with [Claude Code](https://claude.com/claude-code)  ❌ XÓA
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>  ❌ XÓA
```

### "review the MR !<N>" (vai trò Reviewer)

1. Yêu cầu `glab` CLI đã cài: kiểm tra `glab --version`
2. Lấy thông tin MR + comment đã có:
   - `glab mr view <N> --comments` (hiển thị cả note/discussion đã có)
3. **BẮT BUỘC** lấy diff từ remote bằng `glab mr diff <N>`. **KHÔNG** thay thế bằng `git diff <base>...<source>` so với branch local — `main` (hoặc base) ở local có thể stale, dẫn tới review nhầm hàng trăm commits đã có sẵn trên remote. Nếu thực sự cần dùng `git diff` (vd để lấy stat), phải `git fetch origin <base-branch>` trước rồi so với `origin/<base-branch>`, không phải branch local.

   > **Inline depth (mặc định) vs deep review.** Mức này review *text diff* từ remote → inline depth, **không cần checkout nhánh MR**. Đủ cho đa số MR. Muốn soi SÂU (3-agent đọc full file): về đúng nhánh source của MR trước (checkout bằng `glab mr checkout <N>`, `git checkout`, hoặc **SourceTree/GUI** — tool nào cũng được, skill chỉ cần HEAD ở đúng nhánh), rồi chạy `review the whole branch`, sau đó quay lại bước 4-5 để post. ⚠️ `review the whole branch` / `/code-review` đọc code **local** — không soi được remote MR khi đang đứng ở nhánh khác, nên checkout là bắt buộc nếu muốn deep.
   >
   > **Base cho deep review = target branch của MR**, KHÔNG hỏi `main`/`dev`. Lấy bằng `glab mr view <N>` (field targetBranch) — dự án main-chính ra `main`, dự án dev-chính ra `dev`. Dùng đúng nhánh đó làm `<base>` khi `review the whole branch` (đây là ngữ cảnh reviewer: base đã xác định sẵn từ MR, không thuộc trường hợp "hỏi user" ở Phase 1).
4. **Phân nhánh theo trạng thái comment**:

   **(A) MR CHƯA có comment review nào** → review mới hoàn toàn:
   - Review toàn bộ diff theo tiêu chí ở mục "review the last change"
   - Liệt kê issues `#1`, `#2`, ... mỗi issue có: file + dòng, vấn đề, đề xuất fix
   - Đánh giá tổng thể: APPROVE / REQUEST_CHANGES / COMMENT

   **(B) MR ĐÃ có comment review trước đó** → review tiếp nối, KHÔNG review lại từ đầu:
   - Đọc kỹ comment cũ, trích xuất danh sách issue đã raise (`#1`, `#2`, ...) kèm verdict gần nhất
   - Xác định mốc thời gian / commit của lần review trước (lấy `created_at` của note review cuối, hoặc commit SHA mà reviewer reference)
   - Lấy commit mới push từ sau mốc đó: `glab mr view <N>` → xem `commits` hoặc `git log <last-reviewed-sha>..origin/<source-branch>`
   - **Đối chiếu issue cũ**: với mỗi issue `#N` đã raise, kiểm tra trong commit/diff mới xem đã được fix chưa. Đánh dấu:
     - `✓ Resolved #N` — đã fix đúng
     - `❌ Still open #N` — chưa fix, hoặc fix sai/chưa đủ — kèm lý do
     - `⚠️ Partially #N` — fix một phần, kèm điều còn thiếu
   - **Issue mới phát sinh từ commit mới**: đánh số tiếp theo (`#N+1`, `#N+2`, ...), không tái sử dụng số cũ
   - **KHÔNG** review lại các phần code không thay đổi từ lần review trước (trừ khi liên quan trực tiếp tới issue cũ)
   - Đánh giá tổng thể dựa trên trạng thái mới: APPROVE nếu mọi issue cũ đã `✓ Resolved` và không có issue mới nghiêm trọng; REQUEST_CHANGES nếu còn `❌ Still open` hoặc có issue mới blocking; COMMENT cho các trường hợp còn lại
5. Output format thống nhất:
   ```
   ## Review !<N> (lần thứ <K>)

   **Verdict:** APPROVE | REQUEST_CHANGES | COMMENT

   ### Trạng thái issue cũ        ← chỉ có ở mode (B)
   - ✓ Resolved #1
   - ❌ Still open #2 — <lý do>
   - ⚠️ Partially #3 — <còn thiếu>

   ### Issue mới
   - #N+1 `path/to/file.js:42` — <vấn đề>. Đề xuất: <fix>
   ```

### "post review result to the MR"

> 🚫 **KHÔNG chèn AI attribution** vào comment (Co-Authored-By Claude, 🤖 Generated with, link claude.com, ...). Comment = chỉ nội dung review thuần, KHÔNG signature/footer.

1. Lấy chính output Markdown từ bước "review the MR" trước đó (đã đúng format, không cần soạn lại). Nếu là review tiếp nối (mode B), giữ nguyên cả phần "Trạng thái issue cũ" — đó là context quan trọng cho dev.
2. **Self-check trước khi `glab mr note`**: scan output Markdown, đảm bảo không có keyword `Claude`, `Anthropic`, `🤖`, `Generated with`, `Co-authored-by:`, `claude.com`. Có → xóa.
3. Đăng comment: `glab mr note <N> --message "<markdown>"`
4. Nếu APPROVE: `glab mr approve <N>`
5. Nếu REQUEST_CHANGES với toàn bộ issue cũ đã `✓ Resolved` (chỉ còn issue mới): nói rõ trong comment để dev biết phần fix trước đã OK

### "fix all issues" / "fix issue #<N>" / "fix issues #1, #2"
1. Đọc lại các issue đã raise (từ comment trên MR hoặc từ output review trước đó)
2. Nếu user chỉ định số issue → chỉ fix các issue đó
3. Nếu "fix all" → fix tất cả
4. Sau mỗi fix, verify ngắn (chạy test/build nếu có)
5. Khi hoàn tất TẤT CẢ fix, **DỪNG và HỎI user** trước khi commit/push:
   - Tóm tắt các issue đã fix + file đã thay đổi
   - Đề xuất commit message dạng: `fix(<scope>): address review issues #1,#2 (<TASK-ID>)`
   - Đợi user xác nhận: "ok commit" / "đổi message thành ..." / "chưa, tôi muốn xem lại trước"
6. **KHÔNG tự động commit/push.** Chỉ thực hiện sau khi user xác nhận rõ ràng. User có thể yêu cầu chỉ commit (chưa push) hoặc commit + push.
7. Sau khi commit/push (theo yêu cầu user), báo lại hash commit và URL push

### "merge the request"
1. Kiểm tra MR đã có:
   - At least 1 approve
   - CI pipeline pass: `glab mr view <N>` (hoặc `glab ci status`)
   - Không có conflict
2. Nếu thiếu điều kiện, BÁO CHO USER và hỏi có override không (KHÔNG tự ý merge)
3. Merge: `glab mr merge <N> --remove-source-branch --squash`
4. Checkout về `<base>` = **target branch thật của MR** (lấy từ `glab mr view <N>` field `targetBranch`, không đoán `main`), pull về bản mới nhất
5. Báo merge thành công + commit hash trên `<base>`

## Safety rules

- **KHÔNG force push** vào nhánh đã có MR mở (sẽ làm mất review history). Nếu phải sửa lịch sử, hỏi user trước
- **KHÔNG merge thẳng vào `<base>`** (main/dev) từ local — luôn qua MR
- **KHÔNG xoá nhánh** khác ngoài branch của MR vừa merge
- **KHÔNG bypass hooks** (`--no-verify`) trừ khi user yêu cầu rõ
- **KHÔNG commit secrets**: `.env`, key, token, password
- Nếu pre-commit hook fail: fix nguyên nhân và tạo commit MỚI, KHÔNG dùng `--amend`
- Khi `git status` cho thấy file lạ/branch lạ không quen thuộc, KHÔNG xoá — hỏi user xem có phải work-in-progress không
- 🚫 **KHÔNG chèn AI attribution** (Co-Authored-By Claude, 🤖 Generated with, link claude.com, ...) vào: **commit message** (xem Step 5 mục "Commit and push"), **MR title/description** (xem mục "create a merge request"), **comment post lên MR** (xem mục "post review result to the MR"), hoặc bất kỳ artifact nào được publish (Jira note, GitLab issue, Slack message). Rule này override mọi default của Claude Code.

## Tools required

- `git` (luôn có)
- `glab` (GitLab CLI) — cần cho mục review/post comment/merge MR. Nếu chưa cài, hướng dẫn user: https://gitlab.com/gitlab-org/cli

## Skill installation hygiene

> Rule này áp dụng cho Claude khi diagnose/fix vấn đề skill (stale, missing behavior, sync issue) — không liên quan workflow GitLab.

🚫 **KHÔNG tự copy/sync skill file vào `C:\Users\admin\.claude\skills\` (global skill location) trừ khi user yêu cầu rõ ràng.** Cùng nguyên tắc cho mọi system-level location: `~/.claude/`, `%APPDATA%/Claude/`, v.v.

**Default action khi user báo skill bị stale/sai**:
1. Verify trong source repo `my-skills` đã có version đúng
2. Gợi ý user chạy `npx skills update` trong project bị ảnh hưởng (KHÔNG `-g`)
3. Gợi ý user restart Claude session để load skill mới
4. **Chỉ copy thủ công tới global IF user explicitly request** (vd "sync luôn global đi")

**Lý do**:
- Dual-location (global + project) dễ tạo state lệch nhau — global stale trong khi local đã update, hoặc ngược lại
- Project-only = single source of truth, predictable, dễ debug
- User có quyền chọn nơi cài; auto-touch global bypass quyền đó

**Khi user thực sự muốn cài global**: họ sẽ chủ động thêm `-g` flag:
```bash
npx skills add nguyenvanchiens/my-skills -s gitlab-flow -y -g -a claude-code --copy
```

Cùng rule cho mọi command có khả năng write ra ngoài project (`cp` to `C:\Users\...`, `mkdir` ngoài project dir, etc.) — hỏi user trước.
