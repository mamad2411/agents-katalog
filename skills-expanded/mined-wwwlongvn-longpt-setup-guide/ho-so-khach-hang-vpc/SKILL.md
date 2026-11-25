---
name: ho-so-khach-hang-vpc
description: Dẫn dắt anh Long xây Hồ sơ Khách hàng (Customer Profile) chuẩn Value Proposition Canvas của Strategyzer cho mọi khóa / sản phẩm / pillar / lead page / sale page của hệ sinh thái Phạm Thành Long. Có 2 mode — Mode A xây hồ sơ từ trí nhớ / kiến thức khóa (5 bước hỏi-đáp); Mode B trích xuất hồ sơ từ raw (comment YouTube, post Facebook, email khách, transcript cuộc gọi sale, form Pancake, review CH Play, transcript livestream, survey/NPS feedback) và tự phân loại từng câu khách vào 4 loại Job (chức năng/xã hội/cảm xúc/hỗ trợ) × 3 loại Pain (kết quả/rào cản/rủi ro) × 4 mức Gain (thiết yếu/kỳ vọng/khao khát/bất ngờ), giữ quote nguyên văn. Xuất ra file `persona-<brand>-<slug>.md` trong vault Marketing và đồng bộ ngược target_persona vào asset liên quan. Sử dụng skill này BẤT CỨ KHI NÀO anh Long yêu cầu "xây hồ sơ khách hàng", "viết persona", "phác chân dung khách", "Customer Profile", "VPC profile", "Value Proposition Canvas", "JTBD", "Jobs to be Done", "Pains Gains của khách", "phân khúc khách hàng", "trích xuất pain gain từ comment", "phân loại review khách", "đọc raw đi tổng hợp persona", "pain mining", "voice of customer", hoặc nhắc tên một khóa/sản phẩm + "khách của khóa này là ai", "ai mua khóa này", "ai là target", "ai là persona". Kích hoạt cả khi chỉ nói "trước khi viết landing tôi cần hiểu khách", "tôi sắp launch khóa X", "lead page của tôi không chuyển đổi - xem lại persona", "audit lại persona DTSGC", "tôi có 500 comment YouTube đây, đọc đi tổng hợp", "đây là transcript cuộc gọi sale, phân loại pain", hoặc đưa file/text raw kèm yêu cầu "trích insight khách hàng". KHÔNG dùng cho kế hoạch marketing tổng thể (dùng ips-cmo), kịch bản video (dùng video-marketing-28-ngay), hay khi anh chỉ cần content pillar (đã có sẵn trong vault).
---

# Hồ sơ Khách hàng VPC — Skill dẫn dắt xây persona chuẩn Strategyzer

Skill này biến **quy trình xây Hồ sơ Khách hàng** trong [[quy-trinh-xay-dung-ho-so-khach-hang]] thành một phiên hỏi-đáp tuần tự, output ra file `wiki/entities/persona-<brand>-<slug>.md` trong vault Marketing của anh Long.

## Bối cảnh — đọc trước khi bắt đầu

Vault Marketing của anh Long ở:
```
/Users/longpt/Library/Mobile Documents/iCloud~md~obsidian/Documents/Longpt's Marketing/
```

Vault Brain (kiến thức 34 khóa) ở:
```
/Users/longpt/Library/Mobile Documents/iCloud~md~obsidian/Documents/Longpt's Brain/
```

Vault Books (nguồn lý thuyết VPD) ở:
```
/Users/longpt/Library/Mobile Documents/iCloud~md~obsidian/Documents/Books/Thiet ke giai phap gia tri/
```

Quy trình chuẩn 5 bước nằm tại:
```
Longpt's Marketing/wiki/concepts/quy-trinh-xay-dung-ho-so-khach-hang.md
```

**Bắt buộc đọc** quy trình này trước khi bắt đầu phiên (chỉ 1 lần), để biết:
- 6 thành phần hồ sơ
- Quy tắc số lượng tối thiểu (≥8 Jobs / ≥6 Pains / ≥6 Gains)
- Anti-patterns PTL hay vấp (mục 10)
- Template gốc (mục 11)

## Triết lý phiên

- **Một hồ sơ = một phân khúc.** Đừng cố gộp 2 phân khúc vào 1 hồ sơ — sẽ ra giải pháp trung bình không cắn vào ai.
- **Mỗi item trong hồ sơ phải cụ thể.** "Tốn quá nhiều thời gian" → định lượng. "Sợ thất bại" → thất bại gì cụ thể?
- **Anh Long phán đoán cuối — anh là người biết khách rõ nhất.** Skill đề xuất, anh xác nhận / sửa.
- **Khuyến khích anh sửa hơn đồng ý.** Nếu anh "ok" mọi đề xuất → có thể chưa nghĩ kỹ. Hỏi ngược 1 câu để thách thức.
- **Đầu ra cụ thể trên 1 file markdown.** Không tổng kết miệng. Mọi phiên kết thúc bằng 1 file `persona-*.md` lưu vào vault.
- **Khi có raw thực tế của khách — luôn ưu tiên trích từ raw (Mode B) thay vì đoán từ trí nhớ (Mode A).** Pain/Gain trong raw có quote nguyên văn → mạnh hơn pain/gain do anh em phán đoán.

## Hai mode

Skill có **2 mode**, anh Long chọn (hoặc tự phán đoán dựa trên đầu vào):

| | Mode A — Xây từ trí nhớ | Mode B — Trích từ raw |
|---|---|---|
| **Khi dùng** | Chưa có raw / khóa mới chưa launch / phác giả thuyết nhanh | Có comment, post, email, transcript, form, review của khách thật |
| **Tốc độ** | 30-60 phút phỏng vấn anh Long | 1-4h tùy lượng raw |
| **Status xuất ra** | `draft` hoặc `hypothesis` | `hypothesis` (nếu N≥10 raw) hoặc `validated` (nếu N≥30 raw + đủ 6 vai trò) |
| **Bằng chứng** | Section 7+8 trống / sample size = 0 | Section 7+8 đầy quote nguyên văn |

Có thể **kết hợp**: chạy Mode B trước để có insight + quote, sau đó qua Mode A để bổ sung Gain Bất ngờ (khách hiếm khi tự nói).

---

# MODE A — Xây hồ sơ từ trí nhớ / kiến thức khóa (8 bước hỏi-đáp)

### Bước 0 — Xác định scope phiên (1-2 câu hỏi)

Hỏi anh Long:

1. **"Anh muốn xây hồ sơ cho phân khúc nào? Hãy đưa tên một khóa / pillar / lead page / event / sale page cụ thể."**

Sau khi nhận tên, dùng Bash + Read để kiểm tra:
- Tên khóa → đọc `Longpt's Brain/wiki/courses/<...>.md` để hiểu kiến thức gốc khóa.
- Tên pillar → đọc `Longpt's Marketing/wiki/concepts/pillars/<...>.md`.
- Tên asset → đọc `Longpt's Marketing/wiki/assets/<kind>/<...>.md`.

Nếu một khóa phục vụ **nhiều phân khúc khác Jobs** (vd IPS phục vụ cá nhân tự học + doanh nghiệp), hỏi tiếp:

2. **"Khóa này phục vụ nhiều phân khúc khác Jobs không? Nếu có, anh muốn xây hồ sơ cho phân khúc nào *trước*?"** (Khuyên chọn phân khúc lớn nhất / mạng tay nhất / đang launch.)

3. **"Đây là B2C, B2B, hay marketplace (2 mặt)?"** — quyết định có cần điền Vai trò (Roles) hay không.

### Bước 1 — Phân khúc 1 câu (AskUserQuestion + đề xuất)

Đề xuất **1-3 câu mô tả phân khúc** theo cấu trúc *"Người [loại] đang ở [bối cảnh] muốn [Job cốt lõi]"*. Lấy đề xuất từ:
- Kiến thức khóa trong Brain vault
- Trang pillar có sẵn (target persona)
- Hiểu biết chung của anh về thị trường giáo dục doanh nhân Việt Nam 2026

Dùng AskUserQuestion cho anh chọn 1 trong 3 (kèm "Other" để anh viết tay).

**Kiểm tra anti-pattern**:
- Câu có chứa "tất cả" / "mọi người" / "chủ doanh nghiệp Việt Nam" → quay lại, hỏi cụ thể hơn.
- Câu thuần nhân khẩu học (chỉ "phụ nữ 25-35 thu nhập X") → quay lại, hỏi *họ đang cố làm gì*.

### Bước 2 — Bối cảnh 6 câu 5W1H (hỏi 1 lần, anh điền)

Đưa ra 6 câu rõ ràng, anh trả lời từng câu:

- **When**: khoảnh khắc/giai đoạn trong đời họ tìm tới PTL?
- **Where**: đang ở đâu khi gặp PTL? (kênh nào)
- **Who**: ai ảnh hưởng đến quyết định?
- **What**: đã thử gì khác trước khi gặp PTL?
- **Why**: vì sao hành động *bây giờ*?
- **How (constraint)**: ràng buộc tài chính / thời gian / địa lý / niềm tin?

Có thể đề xuất câu trả lời gợi ý lấy từ Brain vault, anh sửa.

### Bước 3 — Việc cần làm (Jobs), 4 loại

Đề xuất **8-15 việc** chia 4 nhóm:

- **Chức năng** (cụ thể, đo được)
- **Xã hội** (cách họ muốn được nhìn nhận)
- **Cảm xúc** (trạng thái nội tâm)
- **Hỗ trợ** (so sánh / đánh giá / giới thiệu / cộng đồng — vòng đời 3 vai trò: mua / cùng tạo giá trị / chuyển giao giá trị)

Trình bày dưới dạng danh sách checkbox để anh tích / sửa / xóa / thêm.

**Nguyên tắc**:
- Tối thiểu 1 job/loại (đủ 4 loại).
- Mỗi job 1 dòng, ngắn gọn, dùng động từ.
- Hỏi "tại sao" ít nhất 1 lần để đào sâu (vd: "tại sao họ muốn 'có hệ thống bán hàng'?" → có thể vì muốn nghỉ tay 4 ngày/tuần → có thể vì muốn dành thời gian cho con).

### Bước 4 — Nỗi đau (Pains), 3 loại

Đề xuất **6-10 pain** chia 3 nhóm:

- **Kết quả không mong muốn** (đã thử, không ăn — functional/social/emotional pain).
- **Rào cản** (blockers: ngân sách / thời gian / địa lý / niềm tin).
- **Rủi ro** (risks: hệ quả tiềm năng xấu nếu chọn sai).

**Quy tắc bắt buộc khi đề xuất**:
- KHÔNG đặt pain đối lập với gain (vd Pain "không có hệ thống bán hàng" / Gain "có hệ thống bán hàng" → sai). Đọc references/anti-patterns.md.
- Cụ thể hóa & định lượng nếu được. "Tốn quá nhiều thời gian" → "tốn 30 phút mỗi sáng soạn post FB mà không ai tương tác."
- Ít nhất **1 pain cảm xúc / xã hội** — không chỉ functional.
- Hỏi anh về **người đã hủy** (status 6 trong Pancake) — pain mạnh nhất thường nằm ở đây.

### Bước 5 — Lợi ích (Gains), 4 mức

Đề xuất **6-10 gain** chia 4 mức rõ ràng:

- **Thiết yếu** (Required): phải có để giải pháp hoạt động.
- **Kỳ vọng** (Expected): mặc nhiên có ở khóa cùng đẳng cấp.
- **Khao khát** (Desired): khách sẽ nói nếu hỏi, nhưng không tự nêu.
- **Bất ngờ** (Unexpected): khách không nghĩ ra trước — vũ khí cạnh tranh.

**Bắt buộc đề xuất ít nhất 2 Gain Bất ngờ** — đây là nơi PTL có lợi thế lớn nhất (cộng đồng cũ, AI Long Bot, mentor trực tiếp, chứng nhận, group VIP, học viên thành công làm reference...).

### Bước 6 — Vai trò (Roles, chỉ B2B)

Nếu Bước 0 xác định B2B, hỏi anh 5 vai trò DMU:

- Người ảnh hưởng (Influencer)
- Người mua (Buyer)
- Người dùng (User)
- Người phê duyệt (Approver)
- Người chi trả (Economic Buyer)

Mỗi vai trò ghi 1-2 dòng về Jobs/Pains/Gains riêng (KHÔNG copy lại toàn bộ hồ sơ — chỉ ghi điểm khác biệt).

Nếu B2C → bỏ qua bước này.

### Bước 7 — Validate và đặt status

Trước khi xuất file, kiểm tra:

| Tiêu chí | Yêu cầu | Pass? |
|---|---|---|
| Phân khúc 1 câu | Có, không chung chung | |
| Bối cảnh | Đủ 6 câu 5W1H | |
| Jobs | ≥ 8, đủ 4 loại | |
| Pains | ≥ 6, đủ 3 loại, có ≥ 1 cảm xúc/xã hội | |
| Gains | ≥ 6, đủ 4 mức, có ≥ 2 Bất ngờ | |
| Vai trò (B2B only) | Đủ 5 vai, mỗi vai 1-2 dòng khác biệt | |

Nếu thiếu → quay lại bước thiếu, bổ sung. KHÔNG xuất file nếu chưa pass.

Status mặc định: `hypothesis` (đã đủ 6 thành phần nhưng chưa kiểm chứng bằng phỏng vấn / A/B test). Nếu anh nói "đây là dự đoán thuần" → `draft`. Nếu anh đưa quote nguyên văn từ phỏng vấn / dữ liệu A/B → có thể `validated` (kèm bảng bằng chứng).

### Bước 8 — Xuất file + đồng bộ ngược

1. **Tạo file** `wiki/entities/persona-<brand>-<slug>.md` theo template trong `references/template-persona.md` (đầy đủ 9 section + frontmatter).

2. **Đặt tên slug** theo quy tắc:
   - Kebab-case, không dấu
   - Mô tả Jobs/context — không phải nhân khẩu học
   - Ví dụ tốt: `persona-dtsgc-nguoi-di-lam-30-45-muon-khoi-nghiep.md`
   - Ví dụ tốt: `persona-sss-chu-shop-online-doanh-thu-50-500tr.md`
   - Ví dụ xấu: `persona-dtsgc-nam-30-45.md` (chỉ nhân khẩu)

3. **Cập nhật `wiki/index.md`** — thêm dòng ở mục Entities (tạo mục mới "Entities — Personas" nếu chưa có).

4. **Append `wiki/log.md`** với format:
   ```
   ## [YYYY-MM-DD] manual | persona | <slug>
   - Tạo persona: [[<slug>]] (status: hypothesis/draft/validated)
   - Phân khúc: <câu mô tả 1 dòng>
   - Brand/course: <code>
   ```

5. **Đề xuất đồng bộ ngược** vào các asset đang phục vụ phân khúc này:
   - Liệt kê tất cả `wiki/assets/lead-pages/*.md`, `wiki/assets/events/*.md` có `brand` match.
   - Hỏi anh "Tôi cập nhật `target_persona: [[<slug>]]` vào những asset nào?"
   - Sau xác nhận, Edit từng asset thêm field này vào frontmatter.

6. **In tóm tắt cuối phiên** (≤ 6 dòng):
   - Tên file đã tạo + đường dẫn
   - 3 dòng tóm tắt phân khúc
   - Asset đã đồng bộ
   - Gợi ý bước tiếp theo (vd "Tuần tới phỏng vấn 5 học viên DTSGC 73 để upgrade status → validated").

---

# MODE B — Trích xuất hồ sơ từ raw

**Mode B kích hoạt khi anh Long cung cấp một trong các đầu vào sau**:

- File / thư mục raw trong `Longpt's Marketing/raw/` (vd transcript phỏng vấn, comment export, email forward, survey CSV)
- Path đến file trong `Longpt's Brain/raw/` (vd transcript khóa cũ — học viên Q&A)
- URL của post / video YouTube → fetch comment qua tool có sẵn
- Pancake order list với note / form response (truy `manage_orders` MCP)
- Đoạn text dài anh paste trực tiếp vào chat
- Câu nói lỏng lẻo "tôi có 500 comment đây, đọc đi tổng hợp"

**Mục đích**: Đọc raw → phân loại từng câu / từng đoạn → đặt vào **đúng các mục con** của hồ sơ (4 loại Job × 3 loại Pain × 4 mức Gain × 5W1H × Vai trò) — giữ **quote nguyên văn**.

## Tham chiếu bắt buộc

**Bắt buộc đọc `references/extraction-rules.md` trước khi bắt đầu Mode B.** File này chứa:
- Bảng marker chi tiết tiếng Việt để phân loại từng câu vào từng mục con
- Quy trình phân loại 1 đoạn raw (6 bước)
- Quy tắc handle 7 loại nguồn khác nhau (YouTube comment, Facebook, email, transcript sale, livestream Q&A, review CH Play, NPS feedback)
- Cảnh báo không trộn speaker khác phân khúc, không "đẹp hóa" quote

## Quy trình 6 bước Mode B

### B0 — Xác định nguồn + phân khúc đích

Trước khi đọc raw, hỏi anh:

1. **"Raw này là của phân khúc nào? Đã có hồ sơ trong vault chưa?"**
   - Đã có → mode "append" — bổ sung quote + insight mới vào persona file có sẵn, status có thể nâng lên `validated`.
   - Chưa có → mode "create" — tạo persona file mới từ raw.

2. **"Speaker_kind chính là gì?"** — buyer (status≥1 Pancake) / canceled (status=6) / non-buyer (subscriber YouTube nhưng chưa đăng ký) / mixed.
   - Nếu `mixed` và speaker khác phân khúc → đề xuất tách 2 hồ sơ.

3. **"Lượng raw bao nhiêu?"** — quyết định batch size:
   - 1-20 items → đọc full, không sample.
   - 20-100 items → đọc full, batch 20 mỗi lần.
   - 100-500 items → sample 30% theo stratified (mỗi loại marker pick top 30%).
   - >500 items → ưu tiên dùng tool tự động (vd grep + LLM phân loại) hoặc chia nhiều phiên.

### B1 — Đọc raw + cắt đơn vị

1. Đọc full một lần để nắm "câu chuyện chung".
2. Cắt thành **đơn vị 1 ý** — thường là 1 câu hoặc 1 mệnh đề (theo dấu phẩy / chấm / xuống dòng).
3. Đặt số thứ tự cho mỗi đơn vị: `[r001]`, `[r002]`, ... để dễ truy lại.
4. Loại noise: emoji thuần (❤️🔥), reaction ngắn ("hay quá", "tuyệt"), comment off-topic — đánh dấu `[NOISE]`.

### B2 — Phân loại từng đơn vị

Mở `references/extraction-rules.md` — bảng marker.

Cho mỗi đơn vị, áp dụng quy trình 5 câu hỏi:

1. Có phải **Job** không? → loại nào (Chức năng / Xã hội / Cảm xúc / Hỗ trợ)?
2. Có phải **Pain** không? → loại nào (Outcome / Obstacle / Risk)?
3. Có phải **Gain** không? → mức nào (Thiết yếu / Kỳ vọng / Khao khát / Bất ngờ)?
4. Có cung cấp **Bối cảnh** (5W1H) không?
5. Có cung cấp **Phân khúc / Vai trò DMU** không?

Một đơn vị có thể `có` cho nhiều câu — ghi vào nhiều mục.

Output cho từng đơn vị (lưu thành bảng tổng hợp):

```yaml
- ref: "[r001]"
  raw: "câu nguyên văn của khách"
  source: "YouTube comment - video XYZ - 2026-05-15"
  speaker_kind: "buyer | canceled | non-buyer | unknown"
  speaker_id: "Pancake 12345 | @username | email hash"
  classifications:
    - kind: "Job-Functional"
      content: "tăng doanh thu lên 500tr/tháng"
      confidence: "high"
    - kind: "Pain-Outcome"
      content: "doanh thu plateau 6 tháng"
      confidence: "high"
  context_hints:
    when: "doanh thu plateau 6 tháng nay"
  segment_hints:
    business_size: "shop online 200tr/tháng"
```

Nếu không chắc → mark `confidence: "low"` + `note: "[suy diễn]"`, không bịa.

### B3 — Tổng hợp tần suất

Sau khi parse N đơn vị, tổng hợp thành **bảng tần suất** cho từng mục con:

**Bảng Jobs**:

| Job | Loại con | Số ref | Quote tiêu biểu |
|---|---|---|---|
| Tăng doanh thu lên 2-3 lần | Chức năng | 8 | "muốn x3 doanh thu trong năm" [r001] |
| Có hệ thống không phụ thuộc mình | Chức năng | 5 | "shop chạy được khi em nghỉ 1 tuần" [r017] |
| Được vợ công nhận thành công | Xã hội | 3 | "vợ em vẫn coi em là 'làm thuê'" [r042] |
| Tự tin chốt sale | Cảm xúc | 7 | "em ngại nói chuyện với khách quá" [r023] |
| ... | ... | ... | ... |

**Bảng Pains** (3 sub-table — Outcome / Obstacle / Risk).

**Bảng Gains** (4 sub-table — Thiết yếu / Kỳ vọng / Khao khát / Bất ngờ).

**Bảng Context hints** (When / Where / Who / What / Why / How).

**Bảng Segment hints**.

### B4 — Lọc theo ngưỡng đưa vào hồ sơ

Quy tắc đưa vào persona file:

- **Item xuất hiện ≥ 3 lần** trong N raw → bắt buộc đưa vào persona (đủ phổ biến).
- **Item xuất hiện 2 lần** → đưa vào nếu phân khúc đang thiếu coverage cho loại con đó.
- **Item xuất hiện 1 lần** → chỉ đưa vào nếu là `[r-buyer-high-trust]` (vd quote từ học viên top, từ phỏng vấn dài) — quote gold.
- **Item < 1 lần (chỉ 1 raw, low confidence)** → KHÔNG đưa vào persona, lưu separately ở section "Backlog quotes" của file scratch.

Sau khi lọc, đảm bảo persona đủ tối thiểu:
- ≥ 8 Jobs đủ 4 loại
- ≥ 6 Pains đủ 3 loại
- ≥ 6 Gains đủ 4 mức (mức Bất ngờ có thể chỉ có 1-2 quote — bổ sung từ trí nhớ trong Mode A nếu cần)

### B5 — Lấp khoảng trống bằng Mode A

Sau Mode B thường có gap:

- **Job Hỗ trợ** ít xuất hiện trong comment public — bổ sung từ trí nhớ.
- **Gain Bất ngờ** khách hiếm khi tự nêu — bổ sung dựa trên lợi thế ecosystem PTL.
- **Vai trò DMU** chỉ có nếu raw từ B2B inquiry — bổ sung nếu sản phẩm B2B.

Cho từng gap, hỏi anh Long 1-2 câu Mode A để fill.

### B6 — Xuất file persona + bảng raw classification

**Output 1**: `wiki/entities/persona-<brand>-<slug>.md` — file persona chuẩn (như Mode A) với:
- Section 1-6: từ raw + Mode A fills
- Section 7 "Bằng chứng đã thu thập": **bảng trích từ raw** với cột (Vai trò nghiên cứu / Ngày / Mẫu / Insight chính)
- Section 8 "Quote nguyên văn": ≥ 5 quote gold (1 cho mỗi mức Pain + 1 cho mỗi mức Gain Khao khát/Bất ngờ)
- Frontmatter: `status: hypothesis` (N < 30) hoặc `validated` (N ≥ 30 + buyer ≥ 10), `sample_size: N`, `validated_by_roles: ["thám-tử"]` (vai trò Thám tử Dữ kiện)

**Output 2**: `wiki/sources/src-extraction-<brand>-<source>-YYYYMMDD.md` — source file lưu **toàn bộ classification** của từng đơn vị (`[r001]`, `[r002]`...), để truy ngược về quote gốc khi cần. Format:

```markdown
---
title: Trích xuất Hồ sơ Khách hàng từ <nguồn>
type: source
source_kind: extraction
brand: <code>
extraction_date: YYYY-MM-DD
n_raw_items: N
n_classified: M
n_noise: K
feeds_persona: "[[persona-<brand>-<slug>]]"
---

# Trích xuất Hồ sơ Khách hàng từ <nguồn>

## Tóm tắt
- Tổng raw items: N
- Đã phân loại: M
- Noise loại bỏ: K
- Top 3 Jobs / Pains / Gains (tần suất)

## Bảng phân loại đầy đủ
| Ref | Raw | Speaker | Classifications | Note |
|---|---|---|---|---|
| [r001] | "..." | buyer | Job-Functional, Pain-Outcome | high confidence |
| ... | ... | ... | ... | ... |

## Bảng tần suất Jobs / Pains / Gains
...
```

**Output 3** (tùy chọn): `wiki/reports/<YYYY-MM>-pain-mining-<brand>.md` — báo cáo cho anh xem nhanh, nếu N > 50.

### B7 — Đồng bộ ngược

Như Mode A Bước 8 — đề xuất gắn `target_persona` vào các asset liên quan.

Thêm: nếu trong raw có nhiều mention của lead-page / event cụ thể → đề xuất đó là asset chính của persona.

## Sample mini-walkthrough Mode B

**Input raw từ anh Long**:

```
@Linh Nguyễn: "anh ơi em xem video anh 2 năm nay rồi, em làm kế toán 10 năm 
nhưng ko thấy phát triển. Năm nay em 38 rồi, lưng vốn tích được khoảng 500tr, 
muốn nhảy ra khởi nghiệp nhưng sợ mất sạch tiền dưỡng già. Đăng ký DTSGC 73 
mà bận con ốm không đi được, em đợt 74 chắc cũng vậy thôi vì shop bán hàng 
online của em đang loạn"

@Tuấn Anh: "đợt 73 em đã đi rồi anh ạ, học xong em ra được 1 sản phẩm bán 
trên FB, doanh thu tháng đầu 20tr, mong anh mở thêm khóa nâng cao"

@Mai: "nhóm zalo của khóa quá nhiều bot quảng cáo, anh moderate giúp em với. 
Còn lại em rất thích khóa, đặc biệt buổi 3 anh kể chuyện đi bộ xuyên Việt 
em nghe khóc"
```

**B1 — cắt đơn vị**:

- [r001] Linh: "em xem video anh 2 năm nay rồi"
- [r002] Linh: "em làm kế toán 10 năm nhưng ko thấy phát triển"
- [r003] Linh: "Năm nay em 38 rồi"
- [r004] Linh: "lưng vốn tích được khoảng 500tr"
- [r005] Linh: "muốn nhảy ra khởi nghiệp"
- [r006] Linh: "sợ mất sạch tiền dưỡng già"
- [r007] Linh: "Đăng ký DTSGC 73 mà bận con ốm không đi được"
- [r008] Linh: "em đợt 74 chắc cũng vậy thôi vì shop bán hàng online của em đang loạn"
- [r009] Tuấn Anh: "đợt 73 em đã đi rồi"
- [r010] Tuấn Anh: "học xong em ra được 1 sản phẩm bán trên FB"
- [r011] Tuấn Anh: "doanh thu tháng đầu 20tr"
- [r012] Tuấn Anh: "mong anh mở thêm khóa nâng cao"
- [r013] Mai: "nhóm zalo của khóa quá nhiều bot quảng cáo, anh moderate giúp em với"
- [r014] Mai: "buổi 3 anh kể chuyện đi bộ xuyên Việt em nghe khóc"

**B2 — phân loại**:

| Ref | Speaker | Job | Pain | Gain | Context | Segment |
|---|---|---|---|---|---|---|
| [r002] | canceled | Job-CN ("phát triển nghề") | Pain-Outcome ("kế toán 10 năm không phát triển") | | When (10 năm) | nghề: kế toán |
| [r003] | canceled | | | | When (38 tuổi) | tuổi: 38 |
| [r004] | canceled | | | | How constraint (500tr vốn) | tài chính: 500tr |
| [r005] | canceled | Job-CN ("khởi nghiệp") | | | Why (trigger 38 tuổi) | |
| [r006] | canceled | | Pain-Risk ("mất sạch tiền dưỡng già") | | | |
| [r007] | canceled | | Pain-Obstacle ("con ốm không đi được") | | When (con ốm) | có con nhỏ |
| [r008] | canceled | | Pain-Obstacle ("shop online đang loạn") | | | có shop online phụ |
| [r010] | buyer | | | Gain-Required ("ra được sản phẩm bán trên FB") | | |
| [r011] | buyer | | | Gain-Required ("doanh thu 20tr tháng đầu") | | |
| [r012] | buyer | Job-Support-Buyer ("muốn mua khóa nâng cao") | | Gain-Khao khát ("khóa nâng cao") | | |
| [r013] | buyer | | Pain-Outcome ("zalo có bot quảng cáo") | Gain-Expected ("moderate zalo") | | |
| [r014] | buyer | | | Gain-Bất ngờ ("nghe chuyện xuyên Việt em khóc — không nghĩ là phần này") | | |

**B3 — tổng hợp tần suất** (3 raw items chỉ minh họa — thực tế cần ≥ 30):

| Pain | Loại | Count | Quote |
|---|---|---|---|
| Bận gia đình không đi học được | Obstacle | 1 | "con ốm không đi được" [r007] |
| Sợ mất vốn dưỡng già | Risk | 1 | "sợ mất sạch tiền dưỡng già" [r006] |

| Gain | Mức | Count | Quote |
|---|---|---|---|
| Ra sản phẩm bán được | Required | 1 | "ra được 1 sản phẩm bán trên FB" [r010] |
| Bài kể chuyện cá nhân cảm động | Bất ngờ | 1 | "buổi 3 anh kể chuyện đi bộ xuyên Việt em nghe khóc" [r014] |

**B4 — lọc**: 3 raw items quá ít — chỉ làm baseline, kết hợp Mode A để fill.

**B5 — Mode A fills**: Bổ sung Job Cảm xúc + Gain Bất ngờ từ trí nhớ.

**B6 — xuất file** `persona-dtsgc-nguoi-di-lam-30-45-muon-khoi-nghiep.md` với section 8 có 2-3 quote gold trên + section 7 có row "Thám tử Dữ kiện: 3 comment YouTube ngày..."

---

## Tham khảo chi tiết

- `references/template-persona.md` — template đầy đủ file `persona-*.md` (copy-paste, fill-in).
- `references/extraction-rules.md` — **bộ não Mode B**: bảng marker tiếng Việt chi tiết để phân loại từng câu raw vào từng mục con, quy trình 6 bước phân loại, cảnh báo khi handle 7 loại nguồn khác nhau (YouTube / FB / email / sale call / livestream / review / NPS).
- `references/anti-patterns.md` — 7 sai lầm PTL hay vấp + cách sửa.
- `references/vpd-summary.md` — tóm tắt 3 chương VPD liên quan (Hồ sơ KH / Phù hợp / Thấu hiểu KH).
- `references/customer-research-roles.md` — 6 vai trò kiểm chứng (Thám tử / Phóng viên / Nhà Nhân chủng học / Người Đóng giả / Người Cùng sáng tạo / Nhà khoa học) — dùng khi anh muốn upgrade status `hypothesis → validated`.
- `references/example-personas.md` — 2 persona mẫu (DTSGC + SSS) hoàn chỉnh để tham khảo cấu trúc/giọng văn.

## Giọng văn khi phỏng vấn anh Long

Anh Long thích **câu ngắn, đi thẳng vào vấn đề, lật vấn đề từ góc khác**. Khi đặt câu hỏi cho anh:

- Đặt 1 câu hỏi/lần (không nhồi 3 câu trong 1 lượt).
- Đề xuất 1-3 phương án cụ thể, không hỏi mở "anh nghĩ sao?".
- Thách thức anh nếu thấy câu trả lời chung chung — "anh ơi, 'khách hàng doanh nhân Việt Nam' rộng quá, hẹp lại được không?".
- Lặp lại insight anh vừa nói bằng câu của anh — "vậy là phân khúc này không phải người chưa khởi nghiệp, mà người **đã** khởi nghiệp 1-2 lần thất bại, đúng không anh?".

## Khi anh Long yêu cầu *audit* persona cũ

Đôi khi anh nói "xem lại persona DTSGC, lâu rồi" — đây là audit, không phải tạo mới. Quy trình:

1. Đọc file `persona-*.md` hiện tại.
2. So với quy trình 5 bước — chấm 6 thành phần xem thiếu/sai chỗ nào.
3. Kiểm tra `last_validated`/`updated` — nếu > 6 tháng → bắt buộc refresh.
4. Hỏi anh có dữ liệu mới gì từ Pancake / phỏng vấn / A/B test → đưa vào.
5. Cập nhật file in-place, KHÔNG tạo file mới.
6. Bump `updated` + `last_validated`.
7. Append log với action `manual | persona-audit`.

## Không bao giờ

- **Tạo persona mà chưa hiểu khóa/sản phẩm**. Bắt buộc đọc Brain vault hoặc hỏi anh trước.
- **Gộp 2 phân khúc khác Jobs vào 1 file** (vd cá nhân + doanh nghiệp). Tách 2 file riêng.
- **Phán đoán pain/gain dựa trên định kiến** ("doanh nhân Việt nào cũng sợ thuế"). Nếu chưa có bằng chứng → đánh dấu (GIẢ ĐỊNH).
- **Xuất file khi chưa pass 6 tiêu chí Bước 7**. Quay lại bổ sung.
- **Sửa CLAUDE.md hoặc các trang quy trình** trong phiên — chỉ tạo persona-*.md mới. Nếu phát hiện quy trình cần update → đề xuất riêng sau phiên.
