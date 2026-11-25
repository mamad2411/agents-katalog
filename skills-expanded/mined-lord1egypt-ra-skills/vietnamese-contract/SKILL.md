---
name: vietnamese-contract
description: >
  Skill tạo hợp đồng, thỏa thuận, cam kết và mọi văn bản pháp lý tiếng Việt chuẩn pháp luật
  Việt Nam, xuất file .docx chuyên nghiệp. Bao gồm toàn bộ quy trình: cài đặt thư viện,
  tra cứu căn cứ pháp lý, soạn nội dung đúng cấu trúc, định dạng chuẩn, kiểm tra chính tả
  tiếng Việt, và xuất file. Hỗ trợ TẤT CẢ các loại hợp đồng: đầu tư, chia lợi nhuận,
  mua bán, dịch vụ, lao động, thuê tài sản, hợp tác kinh doanh (BCC), vay vốn, bảo mật (NDA),
  đại lý, nhượng quyền, xây dựng, chuyển nhượng, ủy quyền, thanh lý, phụ lục hợp đồng,
  biên bản ghi nhớ (MOU), và mọi văn bản pháp lý khác. Luôn sử dụng skill này khi người dùng
  nhắc đến "hợp đồng", "thỏa thuận", "cam kết", "soạn văn bản pháp lý", "contract",
  "agreement", "MOU", "NDA", "biên bản", "phụ lục", "thanh lý", hoặc bất kỳ yêu cầu nào
  liên quan đến văn bản pháp lý Việt Nam — kể cả khi không nói rõ loại cụ thể.
version: 1.0.0
metadata:
  openclaw:
    author: Pham Triet
    community: OpenClaw Việt Nam
    community_link: https://zalo.me/g/lajsqc334jqc5fezevvo
    requires:
      bins:
        - node
        - pandoc
    emoji: "\U0001F4DC"
    tags:
      - legal
      - vietnamese
      - contract
      - document
      - docx
---

# Vietnamese Legal Contract Generator

> **Author:** Pham Triet
> **Cộng đồng:** [OpenClaw Việt Nam](https://zalo.me/g/lajsqc334jqc5fezevvo)

Skill toàn diện để tạo văn bản pháp lý tiếng Việt chuẩn, từ tra cứu pháp luật đến xuất file .docx.

## Mục lục

1. Quy trình tổng quan
2. Bước 1: Cài đặt môi trường
3. Bước 2: Xác định loại & tra cứu pháp lý
4. Bước 3: Soạn nội dung
5. Bước 4: Tạo file .docx
6. Bước 5: Kiểm tra chất lượng
7. Bước 6: Xuất file

---

## Quy trình tổng quan

```
Yêu cầu người dùng
       │
       ▼
┌─────────────────┐
│ 1. Cài đặt      │  npm install -g docx
│    môi trường    │
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 2. Xác định loại│  Đọc references/legal-bases.md
│    & pháp lý    │  rồi WEB SEARCH xác minh
│                 │  luật còn hiệu lực
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 2.5 Quét CCCD   │  EasyOCR quét raw text (offline)
│    (tùy chọn)   │  → AI verify + sửa lỗi → điền HĐ
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 3. Soạn nội dung│  Đọc references/contract-structures.md
│    hợp đồng     │  để biết cấu trúc từng loại
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 4. Tạo file     │  Đọc references/docx-formatting.md
│    .docx        │  để định dạng chuẩn
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 5. Kiểm tra     │  Chạy scripts/vn-spellcheck.py
│    chất lượng   │  + validate docx
└───────┬─────────┘
        ▼
┌─────────────────┐
│ 6. Xuất file    │  Copy → /mnt/user-data/outputs/
│    & giao user  │  + present_files
└─────────────────┘
```

**QUAN TRỌNG:** Đọc các file reference TRƯỚC khi viết code:
- `references/legal-bases.md` — Căn cứ pháp lý từng loại HĐ
- `references/contract-structures.md` — Cấu trúc điều khoản từng loại
- `references/docx-formatting.md` — Quy tắc định dạng .docx + chính tả

---

## Bước 1: Cài đặt môi trường

```bash
# Cài docx-js (thư viện tạo file .docx)
npm install -g docx

# Kiểm tra pandoc (đã có sẵn, dùng để xuất text kiểm tra)
which pandoc
```

Không cần cài thêm gì khác. Các công cụ validate đã có sẵn tại:
- `/mnt/skills/public/docx/scripts/office/validate.py`

---

## Bước 2: Xác định loại & tra cứu pháp lý

### 2.1. Xác định loại hợp đồng

Nếu người dùng chưa nêu rõ, hỏi để xác định. Các loại phổ biến:

| # | Loại hợp đồng | Khi nào dùng |
|---|---------------|-------------|
| 1 | Chia lợi nhuận / Đầu tư | Góp vốn, chia lãi theo tỷ lệ |
| 2 | Mua bán hàng hóa | Giao dịch hàng hóa |
| 3 | Cung cấp dịch vụ | Thuê dịch vụ, outsource |
| 4 | Lao động | Tuyển dụng nhân sự |
| 5 | Thuê tài sản | Thuê nhà, xe, thiết bị |
| 6 | Hợp tác kinh doanh (BCC) | Liên doanh không lập pháp nhân |
| 7 | Bảo mật (NDA) | Bảo vệ thông tin mật |
| 8 | Vay vốn | Cho vay tiền |
| 9 | Đại lý / Phân phối | Phân phối sản phẩm |
| 10 | Nhượng quyền thương mại | Franchise |
| 11 | Xây dựng | Thi công công trình |
| 12 | Chuyển nhượng | Chuyển nhượng quyền, tài sản |
| 13 | Ủy quyền | Ủy quyền thực hiện công việc |
| 14 | Thanh lý hợp đồng | Kết thúc hợp đồng cũ |
| 15 | Phụ lục hợp đồng | Bổ sung, sửa đổi HĐ hiện có |
| 16 | Biên bản ghi nhớ (MOU) | Thỏa thuận sơ bộ |

### 2.2. Tra cứu căn cứ pháp lý

**QUAN TRỌNG: LUÔN dùng web search để xác minh căn cứ pháp lý mới nhất.**

File `references/legal-bases.md` chỉ là **điểm khởi đầu tham khảo** — KHÔNG phải nguồn cuối cùng.
Luật Việt Nam thay đổi thường xuyên, nên phải tra cứu online để đảm bảo chính xác.

**Quy trình tra cứu pháp lý:**

1. Đọc `references/legal-bases.md` để biết cần tra cứu những luật gì
2. **Dùng web search** để xác minh từng luật còn hiệu lực hay đã được thay thế:
   ```
   web_search: "Bộ luật Dân sự 2015 còn hiệu lực site:thuvienphapluat.vn"
   web_search: "Luật Đầu tư mới nhất Việt Nam 2024 2025"
   web_search: "[loại hợp đồng] căn cứ pháp lý site:thuvienphapluat.vn"
   ```
3. Nếu phát hiện luật mới thay thế → cập nhật căn cứ trong hợp đồng

**Nguồn pháp lý chính thống (ưu tiên theo thứ tự):**

| # | Nguồn | URL | Ghi chú |
|---|-------|-----|---------|
| 1 | Cơ sở dữ liệu quốc gia về VBPL | vbpl.vn | Bộ Tư pháp quản lý, chính thống nhất |
| 2 | Thư viện pháp luật | thuvienphapluat.vn | Phổ biến nhất, đầy đủ, dễ tìm |
| 3 | Cổng thông tin Chính phủ | vanban.chinhphu.vn | Văn bản Chính phủ ban hành |
| 4 | VietLaw | vietlaw.gov.vn | Bộ Tư pháp |
| 5 | Công báo điện tử | congbao.chinhphu.vn | Văn bản đã công bố chính thức |

**Ví dụ web search cho hợp đồng đầu tư:**
```
web_search: "hợp đồng đầu tư căn cứ pháp lý 2024 2025"
web_search: "Luật Đầu tư 61/2020 còn hiệu lực"
web_search: "Bộ luật Dân sự 91/2015 sửa đổi bổ sung"
web_fetch: "https://thuvienphapluat.vn/van-ban/Dau-tu/Luat-Dau-tu-2020-61-2020-QH14..."
```

**Lưu ý:** Nếu không có web search (offline), dùng `references/legal-bases.md` làm
fallback nhưng PHẢI cảnh báo người dùng tự kiểm tra lại căn cứ pháp lý.

### 2.3. Thu thập thông tin từ người dùng

Các thông tin cần có (hỏi nếu thiếu, hoặc để trống "......"):
- **Các bên**: Tên, CCCD, địa chỉ, SĐT, email, tài khoản ngân hàng
- **Đối tượng**: Hàng hóa/dịch vụ/dự án/tài sản gì
- **Giá trị**: Số tiền, tỷ lệ, đơn giá
- **Thời hạn**: Bắt đầu, kết thúc, gia hạn
- **Điều kiện đặc biệt**: Kỳ thanh toán, bảo hành, phạt vi phạm...

---

## Bước 2.5: Quét CCCD tự động điền thông tin (TÙY CHỌN)

**→ Đọc file `references/cccd-ocr-guide.md` để biết chi tiết.**

Nếu người dùng upload ảnh CCCD/CMND, trích xuất thông tin tự động thay vì nhập tay.

### Cách hoạt động: 2 lớp (EasyOCR + AI)

```
Lớp 1: EasyOCR (offline)          Lớp 2: AI model (bất kỳ)
─────────────────────────          ────────────────────────
Ảnh CCCD → quét raw text    →     Nhận raw text → phân tích
Không cần internet                 Sửa lỗi OCR, format đúng
Không phụ thuộc AI model           Xác minh logic (ngày hợp lệ?)
```

- **Lớp 1 (EasyOCR)**: Quét ảnh → trích xuất text thô + regex parse cơ bản
- **Lớp 2 (AI model)**: Nhận kết quả lớp 1 → sửa lỗi OCR, chuẩn hóa dấu tiếng Việt, kiểm tra logic → xuất JSON sạch

Lớp 2 hoạt động với BẤT KỲ model nào OpenClaw đang chạy (Claude, GPT, Llama, Gemini...).
Nếu không có AI, lớp 1 vẫn cho kết quả dùng được.

### Cài đặt (1 lần)

```bash
pip install easyocr opencv-python --break-system-packages
```

### Quy trình sử dụng

**Bước 1: Chạy EasyOCR quét ảnh**

```bash
python scripts/cccd-ocr.py cccd-truoc.jpg --back cccd-sau.jpg --json
```

**Bước 2: AI nhận kết quả OCR và cải thiện**

Agent (bất kỳ model nào) nhận JSON từ bước 1, rồi:
- Sửa lỗi OCR: "NGUYÊN" → "NGUYỄN", "TRÍÊT" → "TRIẾT"
- Chuẩn hóa dấu tiếng Việt: "Pham Minh Triet" → "Phạm Minh Triết"
- Kiểm tra logic: ngày sinh hợp lệ? CCCD đủ 12 số? địa chỉ hợp lý?
- Format chuẩn: ngày DD/MM/YYYY, tên IN HOA

**Bước 3: Hiển thị → xác nhận → điền hợp đồng**

**Lưu ý:** CCCD không có SĐT, email, tài khoản ngân hàng → phải hỏi thêm người dùng.

### Prompt mẫu cho AI verify (dùng với bất kỳ model nào)

Sau khi có raw JSON từ EasyOCR, agent dùng prompt sau để AI cải thiện:

```
Đây là kết quả OCR quét từ ảnh CCCD Việt Nam (có thể có lỗi):

{raw_json_từ_easyocr}

Hãy:
1. Sửa lỗi chính tả tiếng Việt (thêm dấu nếu thiếu)
2. Kiểm tra số CCCD đủ 12 chữ số
3. Kiểm tra ngày tháng hợp lệ (DD/MM/YYYY)
4. Chuẩn hóa họ tên (viết hoa)
5. Chuẩn hóa địa chỉ

Trả về JSON đã sửa, giữ nguyên format. Trường nào không chắc thì giữ nguyên.
```

### Bảo mật

- EasyOCR chạy OFFLINE — ảnh CCCD không gửi ra internet
- Chỉ raw text (không phải ảnh) được gửi cho AI model để verify
- KHÔNG lưu ảnh CCCD sau khi trích xuất
- Xóa dữ liệu trung gian sau khi tạo xong hợp đồng

---

## Bước 3: Soạn nội dung

**→ Đọc file `references/contract-structures.md`** để biết cấu trúc điều khoản cụ thể cho từng loại hợp đồng.

### Cấu trúc chung bắt buộc cho MỌI hợp đồng

Mọi hợp đồng pháp lý Việt Nam phải có đủ các phần sau (theo thứ tự):

```
1. Quốc hiệu, tiêu ngữ
2. Tiêu đề hợp đồng
3. Số hợp đồng
4. Ngày tháng, địa điểm
5. Căn cứ pháp lý
6. Thông tin các bên (Bên A, Bên B, ...)
7. Các điều khoản nội dung (tùy loại)
8. Điều khoản chung (số bản, hiệu lực, sửa đổi)
9. Phần chữ ký
```

### Nguyên tắc soạn nội dung

- **Ngôn ngữ**: Trang trọng, chính xác, không mơ hồ
- **Số liệu**: Viết cả số và chữ — VD: "4.000.000 VNĐ (Bốn triệu đồng Việt Nam)"
- **Thời hạn**: Ghi rõ ngày bắt đầu, ngày kết thúc
- **Điều khoản**: Đánh số theo cấp: Điều 1 → 1.1 → a), b), c)
- **Giải quyết tranh chấp**: Luôn có, thường 2 bước: thương lượng → tòa án
- **Chỗ trống**: Dùng dấu chấm "......" cho thông tin chưa có

---

## Bước 4: Tạo file .docx

**→ Đọc file `references/docx-formatting.md`** để biết chi tiết quy tắc định dạng, code mẫu và các lưu ý kỹ thuật.

### Tóm tắt quy tắc định dạng

| Thành phần | Quy tắc |
|-----------|---------|
| Khổ giấy | A4: width 11906, height 16838 (DXA) |
| Lề | Trên 1134, dưới 1134, trái 1418, phải 1134 |
| Font | Times New Roman (bắt buộc cho văn bản pháp lý VN) |
| Cỡ chữ nội dung | 12pt (size: 24 trong docx-js, đơn vị half-point) |
| Tiêu đề | 15pt (size: 30), in hoa, đậm, căn giữa |
| Quốc hiệu | 13pt (size: 26), in hoa, đậm, căn giữa |
| Tiêu đề điều | 13pt (size: 26), in hoa, đậm |
| Dòng | Line spacing 300 (1.5 dòng) |
| Đoạn | Spacing after 120 |
| Căn lề | Justified (hai bên) |
| Bảng | Luôn dùng WidthType.DXA + ShadingType.CLEAR |

### Nguyên tắc viết code JavaScript

**BẮT BUỘC: Sử dụng ký tự Unicode trực tiếp trong JavaScript.**

```javascript
// ✅ ĐÚNG — viết trực tiếp tiếng Việt
p("HỢP ĐỒNG THỎA THUẬN CHIA LỢI NHUẬN ĐẦU TƯ", { bold: true });
p("Bên A cam kết hoàn trả vốn gốc khi hết hạn hợp đồng.");

// ❌ SAI — dùng unicode escape dễ gây lỗi chính tả
p("H\u1EE2P \u0110\u1ED2NG TH\u1ECEA THU\u1EAEN...", { bold: true });
// → Kết quả: "HỢP ĐỒNG THỎA THUẮN" (sai!)
```

---

## Bước 5: Kiểm tra chất lượng

Đây là bước **BẮT BUỘC** — không bao giờ được bỏ qua.

### 5.1. Validate cấu trúc .docx

```bash
python /mnt/skills/public/docx/scripts/office/validate.py output.docx
```

### 5.2. Kiểm tra chính tả tiếng Việt

```bash
python [skill-path]/scripts/vn-spellcheck.py output.docx
```

Script này sẽ:
- Xuất text từ .docx
- Kiểm tra 50+ lỗi chính tả thường gặp trong văn bản pháp lý
- Báo cáo chi tiết vị trí lỗi (nếu có)

### 5.3. Đọc lại nội dung

```bash
pandoc output.docx -o check.md
cat check.md
```

Đọc lại toàn bộ nội dung, kiểm tra:
- Quốc hiệu, tiêu ngữ đúng
- Tiêu đề hợp đồng đúng
- Căn cứ pháp lý phù hợp với loại hợp đồng
- Thông tin các bên đầy đủ
- Các điều khoản đầy đủ và đúng logic
- Số liệu chính xác (cả số và chữ)
- Không có lỗi chính tả
- Phần chữ ký đầy đủ

### 5.4. Nếu phát hiện lỗi

Sa trong file JavaScript → chạy lại node → validate lại → kiểm tra lại.
Lặp lại cho đến khi sạch lỗi.

---

## Bước 6: Xuất file

```bash
cp output.docx /mnt/user-data/outputs/ten-hop-dong.docx
```

Sau đó dùng `present_files` để giao file cho người dùng.

**Luôn kèm lời nhắc:**
> "Đây là bản tham khảo được soạn theo quy định pháp luật Việt Nam hiện hành.
> Nếu giá trị hợp đồng lớn hoặc có tính chất phức tạp, bạn nên nhờ luật sư
> rà soát trước khi ký kết."

---

## Tham khảo nhanh: Cấu trúc thư mục skill

```
vietnamese-contract/
├── SKILL.md                          ← File này
├── scripts/
│   ├── vn-spellcheck.py              ← Script kiểm tra chính tả
│   └── cccd-ocr.py                   ← Script OCR quét CCCD (EasyOCR, chạy offline)
└── references/
    ├── legal-bases.md                 ← Căn cứ pháp lý từng loại HĐ
    ├── contract-structures.md         ← Cấu trúc điều khoản từng loại
    ├── docx-formatting.md             ← Quy tắc định dạng .docx + code mẫu
    └── cccd-ocr-guide.md              ← Hướng dẫn quét CCCD tự động
```
