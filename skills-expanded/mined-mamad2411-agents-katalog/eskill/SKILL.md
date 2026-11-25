---
name: eskill
description: >
  Skill mẹ tạo skill (meta-skill) — quy trình sản xuất Agent Skills chuẩn top-1:
  theo spec chính thức agentskills.io, Cursor Agent Skills (create-skill), quy trình
  eval của anthropics/skills (skill-creator), và kinh nghiệm thực chiến build
  egram/eseed. Dùng khi cần TẠO skill mới, CẢI THIỆN skill cũ, validate/kiểm tra
  skill, chuẩn bị skill bán thương mại, skill cho Cursor (~/.cursor/skills), hoặc
  khi user nói "tạo skill", "làm eskill", "viết SKILL.md", "skill ngon nhất",
  "skill Cursor".
license: UseOnly
compatibility: Python 3.10+
metadata:
  author: hedra
  version: "2.5.0"
---

# eskill — Quy trình tạo Agent Skill (12 trụ cột)

## 12 trụ cột — mỗi trụ 1 kim chỉ nam top-1

```
1. Core         · agentskills.io + Cursor create-skill — format, discovery, chỗ cài
2. UX/UI        · Apple HIG                — cấu trúc skill, quickstart, naming Apple-style
3. Validation   · agentskills.io validator — bắt lỗi sớm bằng máy
4. Docs & Bẫy   · docs chính thức          — docs-driven HARD GATE 100% + bẫy thực chiến
5. Vận hành     · 12-Factor App            — skill gọn, tự chứa, idempotent
6. Eval         · skill-creator Anthropic  — test prompts → forward-test → improver
7. Nội dung     · Apple Writing            — câu ngắn, động từ, không thừa chữ
8. Tăng trưởng  · AARRR                    — description chống undertrigger, adoption
9. Thương mại   · OKX                      — leak scan, LICENSE, marketplace, PnL bán skill
10. Tư vấn      · SPIN + Mom Test          — hỏi đúng nỗi đau, skill theo đúng ý user
11. Thị trường · JTBD + Mom Test + Demand Validation — research trước, build sau
12. Logic gốc   · Pre-mortem + Simulation  — đặt vị thế người dùng, mô phỏng, quét MỌI biến số trước khi build
```

## Quickstart (3 câu — user mới bắt đầu từ đây)

1. `Tạo một skill để <việc gì đó> và kiểm tra nó chạy được` → eskill hỏi ít câu rồi build
2. `Cải thiện skill này: <đường dẫn>` → áp eval loop, tìm lỗi, sửa
3. `Validate skill này: <đường dẫn>` → chạy validator

Nguồn chuẩn: [agentskills.io/specification](https://agentskills.io/specification) · Cursor `create-skill` (`references/cursor-skills.md`) · `anthropics/skills` (skill-creator) · kinh nghiệm egram/eseed.

## 6 bước — BƯỚC 0 quan trọng nhất

1. **BƯỚC 0 — Tư vấn → sinh file → quét biến số (Trụ 10 + 12)**, làm tuần tự 3 việc:
   a. **Hỏi đúng (Trụ 10 — sales-discovery.md)**: trích mục tiêu từ hội thoại hiện có (tool đã dùng, input/output, lỗi user sửa). Hỏi 1 câu/lượt, tối đa 6 câu SPIN + Mom Test; thêm 1 câu persona nếu dự án public (bán / portfolio / dev / nội bộ). Tóm tắt gap → user XÁC NHẬN trước khi viết. Auto-mode (không có user): tự quyết rồi TIẾN HÀNH — đừng kẹt chờ hỏi (đã vấp: agent kẹt cứng ở BƯỚC 0 — forward-test 2026-08-19).
   b. **Sinh bộ file 0→n (bắt buộc — numbered-output.md)**: tạo `0-goal.txt → 1-market.txt → 2-plan.txt → 3-SKILL.md → 4-eval.md → 5-check.md → 6-observed-variables.md` + `docs/` (skeleton trước, điền dần). Ghi TỪNG câu trả lời user vào `0-goal.txt` NGAY khi nhận — state trên disk, restart/compact không mất.
   c. **Mô phỏng + quét biến số (Trụ 12 — simulation-variables.md)**: ĐỌC `6-observed-variables.md` của skill cùng họ TRƯỚC (vòng lặp khép kín — 2.2.0) → đặt vị thế người dùng → mô phỏng 5 kịch bản (chính · biên · lỗi · vòng đời · ra mắt) → quét 6 nhóm biến số (input · lỗi · vòng đời · người đọc · môi trường · quy trình) → biến số chưa phủ → mảng/Bẫy. **BẮT BUỘC ghi vào 2-plan.txt dòng `VÒNG ĐỜI: semver=…, changelog=…`** rồi mới viết. Delivery: lên GitHub → gọi `ehub` · bot Telegram → `egram` — eskill không lo. Nếu build skill bán: làm Trụ 11 (market-research.md) TRƯỚC.
2. **Chọn kim chỉ nam**: mỗi mảng lớn = 1 chuẩn ĐÃ CHỨNG MINH, không viết theo ý kiến. Egram đã dùng: BotFather · Apple HIG · Stripe · Telegram docs · 12-Factor · GitHub Actions · Apple Writing · AARRR · OKX. Tìm nguồn: docs chính thức + `gh search repos --sort stars`. Quy trình tìm/verify/lưu đầy đủ: `references/top1-benchmark.md`.
3. **Viết SKILL.md theo spec** (chi tiết: `references/spec-rules.md` + **Cursor**: `references/cursor-skills.md`):
   - Frontmatter: `name` (1-64, chữ thường + gạch nối, **= tên thư mục**) · `description` ≤1024 — ngôi **thứ 3**, CẢ "làm gì" LẪN "khi nào dùng", trigger keyword, pushy chống undertrigger
   - Cursor: quyết định `disable-model-invocation: true` (chỉ khi gọi tên) **hoặc** omit (auto từ context) — xem cursor-skills.md §3
   - Body < 500 dòng: **quy tắc → code mẫu → checklist**; chỉ viết điều agent chưa biết (Cursor: concise)
   - Chi tiết → `references/` — ref **1 cấp**; cài vào `~/.cursor/skills/<name>/` hoặc `<repo>/.cursor/skills/<name>/` — **CẤM** `~/.cursor/skills-cursor/`
   - **Bắt tay tạo file NGAY**: copy `template/SKILL.md` → điền dần. **KHÔNG** mở `examples/` khi TẠO mới
4. **Đóng gói bẫy đã biết**: mục "Bẫy — đừng lặp" — mỗi bẫy 1 dòng: triệu chứng + fix.
5. **Test + validate**: `references/eval-loop.md` · `scripts/validate-skill.py` · Cursor smoke: session mới + câu trigger → agent đọc SKILL.md
6. **Pin kích hoạt**:
   - **Cursor**: personal `~/.cursor/skills/<name>` (symlink → repo GitHub) hoặc project `.cursor/skills/`; hiến pháp → rule `alwaysApply` nhắc đọc skill (`cursor-skills.md` §5)
   - **DeepSeek** (nếu dùng): `.deepseek/instructions.md` của project

## Quy tắc vàng (học từ sai lầm egram — đừng lặp)

- **DOCS-DRIVEN — HARD GATE 100%**: trước khi code/đo với 1 API/service, PHẢI có docs chính thức trong `references/` (tự fetch được HOẶC user đưa vào). **KHÔNG có docs = KHÔNG code, KHÔNG chạy — DỪNG lại yêu cầu user đưa docs** (file/URL/export). Không dựa vào trí nhớ model — nó sai (bẫy thật: field `views` của Graph API không có trong docs Video object nhưng model tin là có → đo sai lệch 10×: 74.714 vs 7.400 thật). Quy trình chi tiết: `references/docs-driven.md`
- **Doc phải tự kiểm chứng**: mọi lệnh/đường dẫn trong SKILL.md/README phải chạy được. Lỗi kinh điển: egram v1 tuyên bố references là symlink nhưng thực tế là copy + thư mục đích không tồn tại.
- **Idempotent + backup**: mọi patch/script chạy lại 100 lần an toàn, có `.bak` trước khi sửa.
- **Smoke test đóng gói**: 1 script chạy 1 lệnh = bằng chứng skill hoạt động, không cần tin lời.
- **Sanitize trước khi public**: grep secret/path/brand/chat_id/token — làm hệ thống, không làm tay (egram lộ chat_id thật + path home cá nhân khi chuẩn bị bán (bài học: thay placeholder `<chat_id>`, `<project_root>`)).
- **Đổi tên/version đồng bộ mọi file**: README/SKILL/frontmatter — validate chéo (egram v1 README ghi "8 trụ/Hedragram" khi skill đã 9 trụ/egram).

- **Bộ file 0→n BẮT BUỘC, TỰ ĐỘNG (học egram — 0-logic → 5-month)**: ngay khi bắt đầu, agent TỰ TẠO bộ file đánh số trong thư mục dự án (skill: 0-goal → 1-market → 2-plan → 3-SKILL.md → 4-eval → 5-check; dự án khác: 0-goal → 1-plan → ... theo thứ tự build) — skeleton trước, điền dần. MỌI câu trả lời user ghi vào file NGAY khi nhận, không giữ trong hội thoại (state trên disk — restart/compact không mất). Mỗi bước xong → cập nhật file tương ứng; user duyệt từng lớp trước khi sang lớp sau; máy kiểm tra được (đủ file? thiếu file nào?). Chi tiết: `references/numbered-output.md`

- **Chạy đội agent tối đa 2/lượt**: agent con ghi kết quả GỌN vào file .md đánh số, /compact giữa lượt, CẤM spawn lồng nhau — spawn 4-10 song song làm treo UI (đã vấp 2026-08-20; chi tiết: `references/eval-loop.md`)

## Giới hạn (trung thực — khi nào KHÔNG dùng)

- Skill **không thay thế test trên máy thật** của user — eval loop là agent chạy thử, user vẫn phải tự verify trên môi trường thật
- Skill quốc tế → SKILL.md + README nên viết tiếng Anh (eskill bản VN là chuẩn nội bộ của tác giả)
- eskill **chỉ BUILD skill** — không tự đẩy repo lên GitHub / không deploy. Xong skill → muốn lên GitHub gọi `ehub`, bot Telegram gọi `egram` (skill cuối lo delivery)

## References

- `references/spec-rules.md` — Trụ 1+3: frontmatter + progressive disclosure + file refs (spec agentskills.io)
- `references/cursor-skills.md` — Trụ 1 (Cursor): chỗ cài `~/.cursor/skills`, description ngôi 3, `disable-model-invocation`, pin, checklist ship
- `references/naming.md` — Trụ 2: đặt tên kiểu Apple/e-family (brand ≠ prefix, `e` + 1 từ chính, ≤3 âm tiết)
- `references/sales-discovery.md` — Trụ 10: hỏi đúng nỗi đau (SPIN + Mom Test + Gap) — skill theo ý user
- `references/eval-loop.md` — Trụ 6: vòng lặp test prompts → eval → sửa (skill-creator Anthropic)
- `references/test-prompts-template.md` — Trụ 6: 5 kiểu test prompt giả lập user thật (chính/biên/sai/nhanh/lớn)
- `references/rubric.md` — Trụ 6: tiêu chí pass/fail mã hóa TRƯỚC (4 loại: artifact · string · behavior · LLM-judge)
- `references/docs-driven.md` — Trụ 4: docs là HARD GATE 100% (không docs = không code, yêu cầu user đưa)
- `references/12-factor-skills.md` — Trụ 5: vận hành skill bền (tự chứa, idempotent, state disk)
- `references/apple-writing.md` — Trụ 7: viết SKILL.md ngắn gọn (câu ngắn, động từ, specific)
- `references/openai-yaml.md` — Trụ 9: agents/openai.yaml cho marketplace/UI (display_name, short_description, default_prompt)
- `references/checklist-thuong-mai.md` — Trụ 9: chuẩn bị bán: sanitize rò rỉ + LICENSE + README đồng bộ + an toàn khi cài skill lạ
- `references/ban-tren-github.md` — Trụ 9: funnel bán skill trên GitHub (tham khảo) — thực thi delivery gọi `ehub` (repo/release) · `egram` (funnel Telegram)
- `template/SKILL.md` — khung SKILL.md copy dùng ngay (frontmatter đủ field + quy tắc → code mẫu → ví dụ → checklist + Bẫy)
- `examples/echeck/` — SKILL MẪU HOÀN CHỈNH (kiểm tra URL sống) — hình mẫu đối chiếu cho mọi skill tạo ra
- `scripts/validate-skill.py` — validator: frontmatter, quy tắc name, độ dài, refs; `--leak` quét rò rỉ; `--brand "a,b"` quét brand nội bộ
- `scripts/eval-skill.py` — eval harness: static check + test set versioned (eval-results.json) + trace verdict · `--verify` tổng kết pass rate/trigger rate + rubric bắt buộc per case

- `references/market-research.md` — Trụ 11: research trước build sau (nỗi đau user, kênh phân phối, pricing, demand validation)
- `references/numbered-output.md` — pattern file 0→n (học từ egram): sinh tự động, ghi ngay, duyệt từng lớp + thư mục `docs/` tủ tài liệu dự án
- `references/top1-benchmark.md` — Trụ 2: quy trình tìm + verify + lưu kim chỉ nam top-1 (tiêu chí → 3+ ứng viên → 2 nguồn độc lập → benchmark file)
- `references/simulation-variables.md` — Trụ 12: đặt vị thế → mô phỏng 5 kịch bản → quét 5 nhóm biến số → khung kiểm tra output (inside + bố trí)
