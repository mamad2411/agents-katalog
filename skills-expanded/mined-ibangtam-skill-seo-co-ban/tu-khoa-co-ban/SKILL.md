---
name: tu-khoa-co-ban
description: Nghiên cứu từ khoá SEO tiếng Việt bản cơ bản, KHÔNG cần công cụ trả phí — chỉ dùng tìm kiếm web có sẵn của Claude, cộng số liệu người dùng tự dán vào nếu có (file xuất Google Keyword Planner, Search Console, Google Trends, Ahrefs/Semrush). 3 chế độ theo đầu vào - vài từ gốc (mở rộng) · danh sách từ khoá (phân loại thẳng) · tên miền (dò chủ đề site). Ra bảng từ khoá có ý định tìm kiếm, loại bài nên viết, mức rủi ro ngành nhạy cảm, nhóm từ khoá theo URL, silo và thứ tự ưu tiên. Trigger - nghiên cứu từ khoá, research từ khoá, keyword research, tìm từ khoá, mở rộng từ khoá, gom nhóm từ khoá, search intent, ý định tìm kiếm, lập silo, topic cluster. Đầu ra nối thẳng sang skill dan-y-co-ban.
---

# Nghiên cứu từ khoá — bản cơ bản

Skill này giúp ra một bộ từ khoá **dùng được để lên kế hoạch bài viết**, không cần tài khoản
công cụ SEO trả phí. Bù lại, nó **không có số lượt tìm kiếm chính xác** trừ khi người dùng dán
số vào. Nói rõ điều này với người dùng ngay từ đầu, một câu là đủ.

## Luật không được phá

1. **Không bịa số.** Không có số lượt tìm kiếm (volume) thật thì cột đó ghi `chưa có số`, và dùng
   cột **Mức nhu cầu (ước lượng)** = Cao / Vừa / Thấp kèm lý do. Cấm tự nghĩ ra con số như 1.200,
   5.400 dù "trông hợp lý".
2. **Mọi kết luận về trang kết quả Google phải dựa trên kết quả tìm thật** trong phiên này, không
   dựa trí nhớ. Tìm không được → ghi `chưa kiểm được trang kết quả`.
3. **Giữ nguyên chữ người dùng gõ.** Từ khoá họ đưa vào là từ khoá họ cần — không tự đổi sang
   từ khác "vì nghe phổ biến hơn". Muốn gợi ý biến thể thì thêm dòng mới, ghi rõ là gợi ý.
4. **Một nhóm từ khoá = một URL.** Hai từ khoá cần hai trang khác loại thì tách nhóm.

## Biết trước giới hạn của tìm web (đừng tốn công tìm thứ không có)

- Công cụ tìm web của Claude trả về **danh sách link + đoạn tóm tắt**, thường KHÔNG hiện
  "Mọi người cũng hỏi", "Tìm kiếm liên quan", quảng cáo, hộp trả lời nhanh. Mọi chỗ dưới đây ghi
  "nếu thấy" là vậy — không thấy thì dùng nguồn thay thế đã ghi kèm, không báo lỗi.
- Thứ tự link **không chắc là thứ hạng Google Việt Nam**. Coi mọi phép đếm "top 10" là gần
  đúng: chỉ đếm các kết quả tiếng Việt, bỏ trang rác/lạc đề, ghi "ước theo kết quả tìm web".
- Nguồn tốt nhất miễn phí và ổn định là **gợi ý tự hoàn thành** (link `suggestqueries` ở Bước 1)
  và **tiêu đề/heading bài đối thủ**.
- **Ngân sách lượt tìm** (để một lần chạy không kéo dài): ~15–25 lượt tìm/đọc cho cả bộ từ khoá.
  Kiểm trang kết quả chỉ cho **từ khoá chính của các nhóm "Làm ngay" và trang trụ của mỗi silo**;
  các nhóm còn lại ghi `chưa kiểm trang kết quả` là bình thường.

## Bước 0 — Nhận diện chế độ và hỏi đủ thông tin

| Đầu vào | Chế độ |
|---|---|
| 1–9 từ/cụm từ gốc | **MỞ RỘNG** — tìm thêm biến thể rồi phân loại |
| ≥10 từ khoá (dán, file CSV/Excel) | **DANH SÁCH** — phân loại thẳng, chỉ mở rộng khi được yêu cầu |
| Tên miền / URL | **SITE** — đọc site trước, rút chủ đề, rồi chạy như MỞ RỘNG |

Hỏi gộp một lần (chỉ hỏi cái còn thiếu):
- Ngành / sản phẩm / dịch vụ chính là gì? Bán ở đâu (toàn quốc hay khu vực)?
- Mục tiêu: kéo lượt đọc, ra đơn, hay ra liên hệ tư vấn?
- Có sẵn số liệu nào không (file Keyword Planner, Search Console, Ahrefs…)? Có thì dán/đính kèm.
- Muốn khoảng bao nhiêu từ khoá (mặc định 50–150)?

Từ gốc **nhập nhằng nghĩa** (trùng tên người, tên thương hiệu trùng từ thường…) → chốt nghĩa đúng
một câu ("nghĩa đang làm: …") rồi giữ nghĩa đó suốt phiên.

## Bước 1 — Thu thập từ khoá (miễn phí)

Dùng công cụ tìm web có sẵn. Mỗi từ gốc làm các việc sau, dừng khi đủ số lượng cần:

1. **Tìm chính từ gốc** → ghi lại: tiêu đề + loại trang top 10, câu hỏi "Mọi người cũng hỏi"
   nếu thấy, "Tìm kiếm liên quan" cuối trang nếu thấy.
2. **Gợi ý tự hoàn thành** — tìm thêm các mẫu: `từ gốc + là gì / cách / giá / bao nhiêu /
   loại nào / so sánh / review / mua ở đâu / có tốt không / cho người mới / [tỉnh thành]`.
   Nếu môi trường cho phép đọc URL, có thể đọc gợi ý Google trực tiếp:
   `https://suggestqueries.google.com/complete/search?client=firefox&hl=vi&gl=vn&q=<từ+gốc>`
   (không đọc được thì bỏ qua, đừng báo lỗi dài).
3. **Phương pháp bảng chữ cái** khi cần nhiều đuôi dài: `từ gốc a`, `từ gốc b`… (chọn 6–10 chữ
   cái hay gặp, không cần đủ 29).
4. **Đối thủ** (chế độ SITE hoặc khi người dùng nêu tên): đọc menu, danh mục, tiêu đề bài của
   2–3 site đang đứng top → rút chủ đề họ có mà mình chưa có.

**Chuẩn hoá trước khi đi tiếp:** gộp trùng, sửa chữ gõ tắt/không dấu về dạng chuẩn
(`ko → không`, `j → gì`, `bn → bao nhiêu`, `ntn → như thế nào`), bỏ từ lạc nghĩa. Dạng gõ sai
vẫn giữ lại làm biến thể nếu người dùng có số volume cho nó, nhưng **tên nhóm luôn dùng dạng chuẩn**.

### Có số liệu người dùng dán vào

- **Keyword Planner:** lấy cột volume trung bình tháng (thường là khoảng, ví dụ "1K–10K" — ghi
  đúng khoảng đó, không quy về một số).
- **Search Console:** từ khoá đã có lượt hiển thị → cột *Đang có hạng* = vị trí trung bình.
  Vị trí 8–20 = **cơ hội gần** (đã có hạng, đẩy lên trang 1 dễ hơn viết mới).
- **Ahrefs/Semrush:** lấy volume + độ khó (KD).
- **Google Trends:** chỉ dùng để thấy mùa vụ / đang lên / đang xuống, không dùng thay volume.

## Bước 2 — Ước lượng mức nhu cầu (khi không có số)

Chấm theo tín hiệu thấy được, ghi lý do ngắn:

| Tín hiệu | Nghiêng về |
|---|---|
| Gợi ý tự hoàn thành hiện ngay khi gõ nửa cụm | Cao |
| Có nhiều quảng cáo trả tiền trên đầu trang | Cao + có giá trị thương mại |
| Top 10 toàn site lớn, nhiều bài chuyên sâu | Cao + cạnh tranh mạnh |
| Chỉ hiện khi gõ đủ cụm, đuôi dài 5+ chữ | Thấp |
| Top 10 lẫn diễn đàn, bài cũ, trang không liên quan | Thấp–Vừa + **dễ chen vào** |

Ghi thêm cột **Độ cạnh tranh (ước lượng)**: Mạnh / Vừa / Yếu — nhìn top 10 là site lớn chuyên
ngành, báo lớn, sàn TMĐT (mạnh) hay blog nhỏ, diễn đàn, bài mỏng (yếu).

## Bước 3 — Ý định tìm kiếm

Mỗi từ khoá BẮT BUỘC có 1 ý định chính (+ ý định phụ nếu lẫn). Đủ 5 loại, viết đầy đủ:
`Thông tin` · `Thương mại` (đang cân nhắc) · `Giao dịch` (sẵn sàng mua/liên hệ) · `Điều hướng`
(tìm thương hiệu cụ thể) · `Địa phương`.

### Ý định con (giúp chọn đúng loại bài)

| Ý định | Ý định con | Dấu hiệu chữ |
|---|---|---|
| Thông tin | Giải thích | là gì, tại sao, khác gì |
| | Quy trình / thời gian | bao lâu, khi nào, quy trình |
| | Hướng dẫn | cách, làm sao, hướng dẫn |
| | Xử lý lỗi | lỗi, không chạy, sửa |
| | Đánh giá an toàn | có tốt không, có hại không, có nên |
| Thương mại | So sánh | vs, so sánh, khác nhau |
| | Tìm review | review, đánh giá, trải nghiệm |
| | Danh sách chọn lọc | top, loại nào, nên chọn |
| | Tìm hiểu sản phẩm | tên sản phẩm + đặc điểm |
| Giao dịch | Mua | mua, giá, đặt hàng, báo giá |
| | Đăng ký / thuê | đăng ký, tư vấn, thuê, đặt lịch |
| Điều hướng | Thương hiệu | tên hãng, tên hãng + tính năng |
| Địa phương | Tìm nơi cung cấp | dịch vụ + tỉnh/quận, gần đây |

### Bẫy phân loại hay sai (sửa lại cho đúng)

- `X tốt nhất / top X` → **Thương mại – Danh sách chọn lọc**, không phải Thông tin.
- `X giá bao nhiêu` → **Giao dịch – Mua** (đang dự trù tiền), không phải Thông tin.
- `X có an toàn không / có hại không` → **Thương mại – Đánh giá** (đang cân nhắc trước khi mua).
- `[hãng] review` → **Thương mại – Tìm review**, không phải Điều hướng.
- `cách chọn X` → **Thương mại** (sắp mua), dù có chữ "cách".

**Kiểm bằng trang kết quả** cho các từ quan trọng (từ trụ của mỗi nhóm, từ có nhu cầu Cao):
đếm loại trang top 10. Một loại chiếm **≥6/10** → theo loại đó. Không loại nào áp đảo → ghi
`kết quả lẫn` và chọn theo 3 kết quả đầu.

## Bước 4 — Loại bài nên viết

| Loại bài | Dùng cho |
|---|---|
| Bài giải thích | Giải thích, Quy trình |
| Bài hướng dẫn từng bước | Hướng dẫn, Xử lý lỗi |
| Bài so sánh | So sánh |
| Bài danh sách chọn lọc (top N) | Danh sách chọn lọc |
| Bài review | Tìm review, Đánh giá an toàn (khi đang sắp mua) |
| Trang sản phẩm / danh mục | Tìm hiểu sản phẩm, Mua (hàng hoá) |
| Trang dịch vụ | Mua (dịch vụ), Đăng ký/thuê, Tìm nơi cung cấp |
| Trang thương hiệu / hỗ trợ | Thương hiệu |

Nếu top 10 toàn **video** → ghi chú "nên kèm video" (bài viết vẫn có cơ hội vì ít đối thủ chữ).
Nếu top 10 toàn **trang sản phẩm/danh mục** → đừng đề xuất viết blog cho từ đó.

## Bước 5 — Cờ rủi ro (ngành nhạy cảm)

Ngành **sức khoẻ, tài chính – ngân hàng – bảo hiểm, pháp lý, an toàn trẻ em** → mọi từ khoá
mặc định rủi ro tối thiểu `Vừa`.

| Mức | Khi nào | Hệ quả |
|---|---|---|
| Cao | Ngành nhạy cảm **và** top 10 gần như toàn cơ quan nhà nước, bệnh viện, ngân hàng lớn, báo lớn | Đừng hứa thời gian lên top; cần tác giả/người duyệt có chuyên môn; cân nhắc chỉ viết góc trải nghiệm/dịch vụ thật của mình |
| Vừa | Ngành nhạy cảm, hoặc top 10 nhiều site rất mạnh | Bài cần nguồn chính thống + tên tác giả |
| Thấp | Còn lại | Bình thường |

## Bước 6 — Gom nhóm từ khoá (mỗi nhóm = 1 URL)

Theo thứ tự ưu tiên:
1. **Cùng ý định** — khác ý định là tách, dù chữ gần giống.
2. **Trang kết quả giống nhau** — với cặp còn phân vân, tìm cả hai: top 5 trùng **≥3 URL** → gộp;
   ít hơn → tách. (Chỉ kiểm các cặp phân vân, không cần kiểm hết.)
3. **Gần nghĩa** — đồng nghĩa ("thuê xe" = "cho thuê xe"), đuôi dài của cùng gốc, cùng mẫu sản phẩm.

Quy tắc:
- Nhóm 2–8 từ. Nhóm >8 từ → xem lại, thường đang ôm 2 loại trang.
- Trong nhóm đánh dấu: `Từ khoá chính` (1 từ) · `Từ khoá phụ` · `Đuôi dài`.
- **Từ khoá chính** = dạng chuẩn chính tả, nhu cầu cao nhất trong nhóm, đúng ý định của nhóm.
- **Tên nhóm** = tên thực thể ngắn gọn ("Máy lọc nước RO"), không phải nguyên cụm tìm kiếm
  ("máy lọc nước ro giá rẻ hà nội" ❌). Phần "giá rẻ, hà nội" là từ khoá trong nhóm.

**Hai câu kiểm sau khi gom:**
- Còn từ nào chưa vào nhóm nào? → lập nhóm mới hoặc ghi "loại vì …". Cấm bỏ rơi im lặng.
- Có từ nào nằm được ở ≥2 nhóm? → chốt về 1 nhóm, ghi chú ở nhóm kia (đây là mầm hai bài
  của mình tự giành hạng của nhau).

Có tên miền của người dùng → tìm `site:tenmien.com <từ khoá chính>` cho từng nhóm để xem
**đã có bài nào cho nhóm này chưa**. Có rồi → ghi `đã có: <URL>` và đề xuất *cập nhật bài cũ*
thay vì viết mới.

## Bước 7 — Silo (nhóm của các nhóm)

Gom các nhóm cùng chủ đề lớn thành silo — silo thường thành **danh mục** trên website:

```
[Silo: Máy lọc nước]
├── Trụ: nhóm "máy lọc nước"            → trang danh mục / bài tổng quan
├── Nhánh: nhóm "máy lọc nước RO"       → trang danh mục con
├── Nhánh: nhóm "giá máy lọc nước"      → bài bảng giá
└── Nhánh: nhóm "cách thay lõi lọc"     → bài hướng dẫn
```

Luồng liên kết nội bộ gợi ý: bài Thông tin → trang Thương mại → trang Giao dịch. Mỗi bài nhánh
link về trang trụ.

## Bước 8 — Thứ tự ưu tiên (công thức đơn giản)

Chấm mỗi **nhóm** theo thang 1–5 rồi cộng:

| Tiêu chí | 5 điểm | 1 điểm |
|---|---|---|
| Nhu cầu | Cao (hoặc volume lớn nhất bộ) | Thấp |
| Dễ chen vào | Cạnh tranh Yếu | Cạnh tranh Mạnh |
| Gần tiền | Giao dịch / Địa phương | Thông tin chung chung |
| Khớp mục tiêu người dùng | Đúng mục tiêu đã hỏi ở Bước 0 | Lệch |

Cộng thêm: **+3** nếu là cơ hội gần (đang hạng 8–20 trong Search Console) · **+1** nếu đang lên
(Trends). Trừ: **−2** nếu rủi ro Cao · **−2** nếu trùng nhóm với bài đã có mà chưa xử lý.

Xếp thành 3 đợt: **Làm ngay** (điểm cao nhất ~20%) · **Làm tiếp** · **Để sau**.
Bảng nhóm **sắp theo điểm giảm dần**. Không có số volume thì điểm Nhu cầu chỉ là ước lượng —
nói rõ điều này trong tóm tắt. Cụm không có tín hiệu nhu cầu nào (không hiện trong gợi ý, không
thấy bài nào nhắm tới) thì không được làm từ khoá chính của nhóm.

Đợt "Làm ngay" nên có **ít nhất 1–2 nhóm dạng bài viết** (thông tin / thương mại) chứ không chỉ
toàn trang sản phẩm–dịch vụ, để có bài chuyển sang lên dàn ý.

## Đầu ra

### 1. Bảng từ khoá (bảng chính)

| Từ khoá | Nhóm | Vai trò | Volume | Mức nhu cầu (ước lượng) | Cạnh tranh | Ý định | Ý định con | Loại bài | Rủi ro | Ghi chú |
|---|---|---|---|---|---|---|---|---|---|---|

Cột *Volume* chỉ điền khi có số thật từ người dùng, kèm nguồn (`KP`, `GSC`, `Ahrefs`…).

### 2. Bảng nhóm (mỗi dòng = 1 URL sẽ làm)

| # | Silo | Tên nhóm | Từ khoá chính | Số từ phụ | Loại bài | Rủi ro | Điểm | Đợt | Đã có bài? |
|---|---|---|---|---|---|---|---|---|---|

### 3. Sơ đồ silo (dạng cây như Bước 7)

### 4. Tóm tắt 5–7 dòng
Bao nhiêu từ khoá · bao nhiêu nhóm · 3–5 nhóm nên làm ngay và vì sao · điều gì chưa kiểm được.

### 5. Thẻ chuyển sang lên dàn ý (cho mỗi nhóm "Làm ngay")

```
THẺ TỪ KHOÁ
Từ khoá chính: …
Từ khoá phụ: …, …, …
Ý định: … / Ý định con: …
Loại bài: …
Rủi ro: …
Câu hỏi người dùng hay hỏi (thấy được khi tìm): …
```

Người dùng muốn file: xuất **Excel** (mỗi bảng 1 sheet) nếu môi trường tạo được file, không
được thì xuất CSV hoặc để bảng trong chat.

## Tự kiểm trước khi giao

- [ ] Không có con số volume nào không có nguồn từ người dùng.
- [ ] 100% từ khoá có Ý định + Loại bài.
- [ ] Từ khoá chính của mọi nhóm đã kiểm trang kết quả thật (hoặc ghi rõ chưa kiểm được).
- [ ] 0 từ bỏ rơi, 0 từ nằm 2 nhóm.
- [ ] Tên nhóm là tên thực thể ngắn, không phải cụm tìm kiếm dài.

## Giới hạn của bản cơ bản (nói thật với người dùng khi được hỏi)

Không có volume/độ khó chính xác nếu không dán số · không đo hạng thật theo ngày · không quét
toàn bộ từ khoá của đối thủ · không tự phát hiện bài trùng chủ đề trên site ở quy mô lớn.
Muốn chính xác hơn: dán thêm file xuất Keyword Planner (miễn phí khi có tài khoản Google Ads)
hoặc Search Console của chính site.
