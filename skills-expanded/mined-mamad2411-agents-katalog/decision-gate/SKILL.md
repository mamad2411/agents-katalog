---
name: decision-gate
description: "Phán quyết go/no-go + ưu tiên cho một hạng mục kỹ thuật, xác minh bằng chứng read-only trước khi kết luận. Xử lý bug, feature, techdebt, hoặc task mơ hồ — verify trước, kết luận sau, chấm điểm RICE/ICE/WSJF, output decision brief. Trigger: nên làm không, có đáng làm không, go/no-go, đánh giá priority, ưu tiên task, bug này nghiêm trọng không, feature này có đáng không, techdebt này cần fix không, triage, đánh giá hạng mục, should we do this, prioritize this. Dùng khi cần quyết định CÓ NÊN LÀM hay không + mức ưu tiên cho MỘT item cụ thể."
---

# Decision Gate — Phán quyết go/no-go có bằng chứng

Skill đóng vai trò trợ lý ra quyết định cho **một** hạng mục công việc kỹ thuật: Bug, Feature, Techdebt, hoặc Task thường. Input thường mơ hồ (chưa chắc là bug thật, chưa chắc đáng làm), nên skill **xác minh trước, kết luận sau**, rồi đưa ra khuyến nghị go/no-go kèm ưu tiên.

Sản phẩm cuối là một **decision brief**. Skill dừng tại đó.

## Tư thế cốt lõi: không phán xét vội

Đây là guard quan trọng nhất. Mọi bước sau phục vụ nguyên tắc này:

- **Input mơ hồ là mặc định.** Chưa chắc là bug, chưa chắc đáng làm. Đừng tin lời mô tả ban đầu là sự thật.
- **Cấm kết luận go/no-go trước khi có bằng chứng từ pha xác minh.** Một verdict không bằng chứng là phỏng đoán đội lốt quyết định.
- **Mọi verdict gắn với bằng chứng cụ thể hoặc giả định được ghi rõ.** Không có "tôi nghĩ chắc là...". Hoặc chứng minh được, hoặc ghi thành giả định có nhãn.
- **Gate chỉ mở (Go) khi giả định *then chốt* đã thành bằng chứng.** Giả định *phụ* được phép tồn tại (ghi rõ), nhưng kéo Confidence xuống thấp khi chấm điểm.

> Phân biệt giả định **then chốt** vs **phụ**: then chốt là giả định mà nếu sai thì verdict đảo chiều (vd "bug này thật sự xảy ra ở production"). Phụ là giả định ảnh hưởng độ chính xác của điểm số nhưng không đảo verdict (vd "ước lượng Reach khoảng 2000 user/tháng").

## Phạm vi

Trong phạm vi: xử lý **một** hạng mục mỗi lần, output là decision brief văn bản.

Ngoài phạm vi (tuyệt đối không làm): triage hàng loạt nhiều hạng mục; tự tạo issue / lập kế hoạch / gọi hoặc gợi ý skill khác; sửa code để reproduce (chỉ read-only); tích hợp issue tracker bên ngoài (chỉ đọc nếu có sẵn trong repo).

## References — đọc khi cần

| Khi cần | Đọc |
|---------|-----|
| Công thức RICE/ICE/WSJF, map khung↔loại, map điểm→P-level | `references/frameworks.md` |
| Mẹo đào bằng chứng theo loại (reproduce read-only, tìm root cause, đo techdebt, validate need) | `references/verification-tactics.md` |
| Template decision brief | `templates/decision-brief.md` |

## Luồng 3 pha

Một luồng thống nhất áp cho cả Bug/Feature/Techdebt/Task. Phân loại hạng mục chỉ dùng để (a) đặt đúng câu hỏi xác minh ở pha 1 và (b) chọn khung chấm điểm ở pha 3. Đây vẫn là **một luồng chung**: "rẽ nhánh" chỉ là chọn công thức trong cùng `frameworks.md`, không có playbook riêng từng loại.

```
Pha 1: Xác minh (research, read-only)  →  thu fact, có thể hỏi user NHIỀU lần
Pha 2: Cổng Go/No-Go (checkpoint MỘT lần)  →  chốt diễn giải, gán loại, ra verdict
Pha 3: Ưu tiên (chỉ khi Go)  →  chọn khung theo loại → điểm → P-level
Output: Decision Brief  →  dừng tuyệt đối
```

### Pha 1 — Xác minh (research)

Chế độ **lai**: tự đào trước, bí thì hỏi. Ranh giới đào/hỏi theo **bản chất thông tin**, không theo thời gian bỏ ra.

| Loại thông tin | Hành động |
|---|---|
| Có trong repo (code, `git log` / `git blame`, grep, test, issue/PR sẵn) | **Tự đào, bắt buộc.** Không hỏi user thứ mình tự đào được |
| Hành vi runtime (reproduce bug) | Chạy test/lệnh **read-only** để verify. **Cấm sửa code.** Nếu reproduce cần sửa code hoặc cần env không có → ghi "chưa verify được" + hỏi user "bạn đã gặp lỗi này chưa, trong tình huống nào?" |
| Context sản phẩm (Reach thật, business impact, ưu tiên chiến lược) | **Hỏi user**, hoặc đánh dấu giả định. Không bịa |

Mẹo đào cụ thể theo từng loại hạng mục: đọc `references/verification-tactics.md`.

**Hỏi trong pha 1 có thể diễn ra nhiều lần** — đây là thu thập fact tự nhiên, KHÔNG tính là checkpoint. Cứ hỏi khi thiếu fact.

Kết quả pha 1 là **Reality check**, nội dung tùy bản chất hạng mục:

- **Bug**: reproduce được không? Root cause ở đâu?
- **Feature / Task**: nhu cầu gốc có thật không? Có align mục tiêu không?
- **Techdebt**: thực sự gây đau không? Đo được cost-of-delay không?

Cuối pha, ghi rõ **giả định** (phân tầng then chốt vs phụ) và **khoảng trống thông tin** còn lại.

### Pha 2 — Cổng Go/No-Go (checkpoint diễn giải, MỘT lần)

Đây là **lần dừng-xác-nhận duy nhất**, khác hẳn việc hỏi-thu-fact ở pha 1. Mục tiêu: chốt *diễn giải*, không phải gom thêm dữ liệu.

Trình bày cho user 3 thứ cùng lúc (gộp, không tách thành nhiều lần dừng):

1. **Loại hạng mục Claude tự gán** (bug/feature/techdebt/task) suy ra từ bằng chứng pha 1. Nêu để user sửa nếu sai — loại này quyết định khung chấm điểm ở pha 3.
2. **Reality check + danh sách giả định** (then chốt / phụ) để user xác nhận hoặc sửa.
3. **Verdict đề xuất**, dựa trên độ vững bằng chứng:

| Tình trạng bằng chứng | Verdict |
|---|---|
| Xác minh được (reproduce / nhu cầu gốc có thật / cost đo được) | **Go** → sang pha 3 |
| Phủ định rõ (không reproduce + không ai cần + không đau) | **No-Go** → dừng, xuất brief ghi rõ lý do |
| Giả định **then chốt** chưa verify được | **Cần thêm thông tin** → refine tại chỗ |

**"Cần thêm thông tin" KHÔNG phải verdict thứ ba ngang hàng.** Nó là trạng thái refine tại cùng một cổng: đào bổ sung đúng chỗ thiếu (hoặc hỏi user đúng câu thiếu), rồi trình lại verdict. Tuyệt đối KHÔNG cho Go khi giả định then chốt còn treo. Giữ nguyên tắc "checkpoint một lần về khái niệm" — vòng refine không phải checkpoint mới.

### Pha 3 — Ưu tiên (chỉ khi Go)

Một trục duy nhất: **Priority → P-level**. Không có trục timing.

**Chọn khung theo loại** (công thức chi tiết: `references/frameworks.md`):

| Loại | Khung | Lý do |
|---|---|---|
| Feature (hướng user) | RICE (Reach × Impact × Confidence ÷ Effort) | Reach có nghĩa thật |
| Bug | ICE (Impact × Confidence × Ease) | Bỏ Reach; Impact = mức đau/tần suất |
| Techdebt | WSJF (Cost-of-Delay ÷ Effort) | Đo "càng để lâu càng đắt" |
| Task / khác | ICE | Nhẹ, đủ dùng |

**Hạng mục lai** (vd "API chậm" vừa bug vừa techdebt): chọn khung theo **quyết định cần ra**, không theo nhãn bề mặt. "Sửa ngay không?" → bug → ICE. "Refactor kiến trúc không?" → techdebt → WSJF. Ghi rõ đã chọn khung nào và vì sao.

**Map điểm → P-level:** P0-P3 neo vào **tiêu chí định tính chung**, điểm số chỉ là đầu vào hỗ trợ xếp hạng và minh bạch lý do. KHÔNG hard-code ngưỡng số kiểu "RICE>300 = P0".

| P-level | Nghĩa định tính (chung mọi khung) |
|---|---|
| **P0** | Đang chảy máu / chặn việc khác / rủi ro nghiêm trọng. Làm ngay |
| **P1** | Giá trị cao, rõ ràng đáng làm sớm |
| **P2** | Đáng làm, chưa gấp |
| **P3** | Biên, làm khi rảnh hoặc gộp dịp khác |

Claude diễn giải điểm + bối cảnh → chốt P-level, **ghi rõ lý do**. Ví dụ: "ICE=320, nhưng là bug chặn checkout của khách → P0 dù điểm chưa cao nhất". Bảng từng yếu tố vẫn phải hiện đủ để minh bạch.

Yếu tố cần context sản phẩm (Reach, business Impact) mà không có dữ liệu → hỏi user, hoặc đánh dấu là giả định **phụ** (kéo Confidence xuống thấp).

## Output: Decision Brief

Artifact cuối, markdown theo `templates/decision-brief.md`.

- **Mặc định: in thẳng ra chat.**
- **Chỉ lưu file khi user yêu cầu.** Khi đó lưu vào `{CWD}/decision-gate/{ten-hang-muc-slug}-{YYMMDD}.md` (tạo thư mục nếu chưa có, báo đường dẫn cho user).

Các phần của brief:

1. Hạng mục + loại (bug/feature/techdebt/task)
2. Reality check: verified hay chưa, bằng chứng, reproduction/root-cause hoặc need-alignment
3. Verdict: Go / No-Go / Cần thêm thông tin + lý do gắn bằng chứng
4. (nếu Go) Priority: bảng khung (RICE/ICE/WSJF theo loại) + điểm số + P-level + lý do diễn giải
5. Giả định (then chốt / phụ) & khoảng trống thông tin

## Điểm dừng tuyệt đối

Skill dừng ở brief. **Không** có phần "bước kế tiếp". **Không** gợi ý skill khác, **không** gọi skill, **không** tạo issue, **không** lập kế hoạch, **không** tạo bất kỳ artifact nào ngoài brief. Phán quyết xong là xong — quyền hành động tiếp thuộc về user.
