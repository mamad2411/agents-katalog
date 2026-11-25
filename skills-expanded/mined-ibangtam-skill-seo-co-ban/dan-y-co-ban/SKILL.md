---
name: dan-y-co-ban
description: Lên dàn ý (outline) bài SEO tiếng Việt bản cơ bản cho MỘT từ khoá, KHÔNG cần công cụ trả phí — đọc top 10 Google bằng tìm kiếm web có sẵn của Claude, rút heading đối thủ, chốt dạng bài theo trang kết quả, gom câu hỏi thường gặp, rồi ra dàn ý H1/H2/H3 có ghi chú viết cho từng mục + Meta Title/Description + URL + gợi ý liên kết nội bộ + brief giao người viết. Trigger - lên dàn ý, lên outline, outline bài viết, outline SEO, dàn ý bài viết, content brief, brief viết bài, hoặc khi đưa một từ khoá kèm yêu cầu viết bài SEO. Nhận thẻ từ khoá từ skill tu-khoa-co-ban nếu có; đầu ra nối thẳng sang skill viet-bai-co-ban.
---

# Lên dàn ý bài SEO — bản cơ bản

Đầu vào tối thiểu: **một từ khoá chính**. Tốt hơn nếu có thêm thẻ từ khoá từ `tu-khoa-co-ban`
(từ phụ, ý định, loại bài, rủi ro), tên website, và vài dòng về thương hiệu.

## Luật không được phá

1. **Khoá từ khoá.** Từ khoá người dùng đưa = từ khoá chính, dùng cho H1, đoạn mở đầu, URL.
   Không đề xuất thay dù thấy "ít người tìm". Từ biến thể phổ biến hơn → đưa vào H2/H3 làm từ phụ.
2. **Dạng bài theo trang kết quả, không theo ý thích.** Top 10 toàn trang sản phẩm thì không
   lên dàn ý blog dài — báo người dùng và đề xuất dàn ý trang sản phẩm/dịch vụ.
3. **Không bịa về đối thủ.** Chỉ ghi heading đã đọc được thật. Trang không đọc được (chặn, chạy
   bằng JavaScript, trả về khung rỗng) → ghi `không đọc được`, bỏ qua, lấy trang kế tiếp.
4. **Không từ tuyệt đối** trong H1, Meta Title, Meta Description: "nhất, tốt nhất, duy nhất, số 1,
   hàng đầu, dẫn đầu" — trừ khi người dùng có chứng cứ (giải thưởng, chứng nhận, số liệu có nguồn).
   Luật Quảng cáo Việt Nam cấm dùng khi không chứng minh được.

## Giới hạn của tìm web

Công cụ tìm web trả về danh sách link + đoạn tóm tắt, thường **không hiện** "Mọi người cũng hỏi",
quảng cáo, hộp trả lời nhanh, và thứ tự link không chắc là thứ hạng Google Việt Nam. Vì vậy:
- Câu hỏi người dùng lấy từ: **gợi ý tự hoàn thành dạng câu hỏi** (đọc
  `https://suggestqueries.google.com/complete/search?client=firefox&hl=vi&gl=vn&q=<từ+khoá>`,
  thử thêm đuôi "có", "bao nhiêu", "nên", "là gì"…) + **H2/H3 dạng câu hỏi trong bài đối thủ**.
- Mọi phép đếm "top 10 / ≥3/5 đối thủ" là gần đúng — ghi "ước theo kết quả tìm web".
- Ngân sách: ~8–12 lượt tìm/đọc cho một dàn ý. Trang đối thủ không đọc được → lấy trang kế tiếp,
  tối đa thử 6 trang.

## Bước 0 — Hỏi đủ thông tin (gộp 1 lần, chỉ hỏi cái thiếu)

- Từ khoá chính? Website (nếu có)?
- Bài cho ai đọc, họ đang ở giai đoạn nào: mới tìm hiểu · đang so sánh · sắp mua?
- Giọng văn: chuyên gia nghiêm túc · thân thiện dễ hiểu · ngắn gọn thực dụng?
- Có điều gì cấm nói / bắt buộc nói (cam kết, chính sách, thông tin pháp lý)?

Không ai trả lời → tự chọn theo trang kết quả và ghi rõ "giả định: …" ở đầu dàn ý.

## Bước 1 — Đọc trang kết quả (quan trọng nhất)

Tìm từ khoá chính. Ghi lại:

```
BÁO CÁO TRANG KẾT QUẢ — [từ khoá]
Dạng chiếm ưu thế: [blog / sản phẩm-danh mục / dịch vụ / video / so sánh / top N / tin tức / lẫn]
Ý định: [Thông tin / Thương mại / Giao dịch / Điều hướng / Địa phương]
Có hộp trả lời nhanh (featured snippet)? [có – dạng đoạn/danh sách/bảng | không | không thấy]
Câu hỏi "Mọi người cũng hỏi": [liệt kê]
Tìm kiếm liên quan: [liệt kê]
Top domain: [liệt kê]
⇒ QUYẾT ĐỊNH: viết [dạng bài] vì [lý do từ trang kết quả]
```

Cách đọc nhanh:
| Thấy gì | Làm gì |
|---|---|
| Top 10 chủ yếu blog | Cạnh tranh bằng chiều sâu + góc riêng |
| Toàn video | Bài viết dễ chen vào; gợi ý chèn video |
| Toàn trang sản phẩm/danh mục | Đừng viết blog — làm trang sản phẩm/danh mục |
| Có bản đồ / cửa hàng | Cần tên – địa chỉ – điện thoại, góc địa phương |
| Có hộp trả lời nhanh | Đoạn đầu bài và đầu H2 đầu tiên trả lời 40–60 từ |

## Bước 2 — Rút heading đối thủ + tìm khoảng trống

Đọc 3–5 bài đứng đầu (bỏ sàn TMĐT, video, diễn đàn nếu không cùng dạng). Với mỗi bài ghi:
H2/H3, có FAQ không, có bảng không, độ dài ước (ngắn <1.000 · vừa 1.000–2.000 · dài >2.000 từ).

Lập **bảng phủ chủ đề**:

| Chủ đề / câu hỏi | Bài 1 | Bài 2 | Bài 3 | Bài 4 | Bài 5 | Đưa vào dàn ý? |
|---|---|---|---|---|---|---|

- Có ở **≥3/5 bài** → chủ đề **bắt buộc** (người đọc mong đợi).
- Có ở 1–2 bài → cân nhắc, lấy nếu đúng ý định.
- **0/5 bài có nhưng người đọc cần** (lấy từ "Mọi người cũng hỏi", tìm kiếm liên quan, hoặc
  hiểu biết ngành) → **điểm khác biệt** ★ — đây là lý do bài mình đáng xếp trên.

**FAQ:** nếu ≥2/5 đối thủ có FAQ, hoặc gom được ≥3 câu hỏi thật (từ "Mọi người cũng hỏi" nếu
thấy, gợi ý tự hoàn thành dạng câu hỏi, H3 dạng câu hỏi của đối thủ) → bài cần mục câu hỏi
thường gặp 4–6 câu.

## Bước 3 — Chọn khung dàn ý theo loại bài

**Bài giải thích:** Trả lời ngắn → Bối cảnh / vì sao quan trọng → Đi sâu (3–5 H3) → Ví dụ → FAQ.

**Bài hướng dẫn:** Vì sao cần làm → Chuẩn bị gì → Các bước (mỗi bước 1 H3, đánh số) →
Lỗi hay gặp → Mẹo → FAQ.

**Bài so sánh A và B:** Tổng quan A, B → Bảng so sánh 8–15 tiêu chí → Ưu/nhược A → Ưu/nhược B
→ Khi nào chọn A, khi nào chọn B → Kết luận theo từng nhu cầu.

**Bài danh sách top N:** Tiêu chí chọn → Bảng tổng quan → mỗi mục 1 H2 (đặc điểm · giá · ưu
nhược · hợp với ai) → Gợi ý theo nhu cầu. Mỗi mục phải có lý do cụ thể, không khen chung.

**Bài review:** Kết luận ngắn đặt đầu bài → từng khía cạnh người mua quan tâm (hiệu năng, giá,
độ bền, dịch vụ…) mỗi khía cạnh có nhận định + bằng chứng → Ưu / nhược → Hợp với ai → So với
lựa chọn khác → FAQ.

**Trang sản phẩm / danh mục:** Giá trị chính → Cách hoạt động / đặc điểm → Ứng dụng →
Thông số → Giá / gói → Khách đã dùng → FAQ.

**Trang dịch vụ:** Giới thiệu dịch vụ (100–200 từ) → Quy trình 3–5 bước → Bảng giá / gói →
Vì sao chọn chúng tôi (bằng chứng, không tự khen) → Khách hàng / phản hồi → Form liên hệ →
FAQ. Nút liên hệ đặt cả giữa bài và cuối bài.

**Trang tổng quan một chủ đề lớn (trang trụ):** Trả lời ngắn → Bản đồ các bài con (mỗi bài con:
tiêu đề + 1–2 câu "đọc bài này nếu bạn đang…") → nhóm bài con theo giai đoạn → FAQ.
Dưới 5 bài con thì đừng làm trang trụ, viết 1 bài dài.

## Bước 4 — Viết dàn ý theo luật heading

**H1** (1 lần duy nhất): chứa từ khoá chính (ưu tiên đầu câu) + một móc thật của bài (con số có
trong bài, đối tượng cụ thể, câu hỏi trực tiếp). Chỉ ghi năm khi bài có dữ kiện của năm đó.
Không trùng nguyên văn Meta Title.

**Đoạn mở đầu (sapo) 100–200 từ, 3 phần:**
1. Trả lời thẳng câu hỏi trong H1 — 40–60 từ, có từ khoá chính.
2. Vì sao câu trả lời có thể khác nhau tuỳ trường hợp — 30–60 từ.
3. Bài sẽ nói thêm những gì — 30–50 từ.

**H2:** mỗi H2 giải quyết một vấn đề con của H1. Khoảng 1/3 số H2 chứa từ khoá chính hoặc từ phụ,
còn lại dùng câu hỏi / đuôi dài tự nhiên. Chia H2 làm hai loại:
- **Chính** (~70%): trả lời thẳng điều H1 hứa.
- **Phụ** (~30%): bối cảnh, so sánh, FAQ, trường hợp đặc biệt.
Chính <60% → bài loãng; >85% → thiếu bối cảnh.

**H3:** chia nhỏ trường hợp trong H2 cha. Ưu tiên viết H3 dạng **câu hỏi người dùng thật hỏi**.

**Mỗi mục kèm ghi chú viết** trong ngoặc vuông, ví dụ:
```
H2: Giá máy lọc nước RO bao nhiêu?
  [Trả lời ngay 40–60 từ: khoảng giá theo phân khúc]
  [Cần: BẢNG giá theo loại · nguồn giá ghi ngày lấy]
  [Từ phụ: giá máy lọc nước, máy lọc nước giá rẻ]
  H3: Máy dưới 5 triệu có gì?
  H3: Máy trên 10 triệu khác gì?
```
Nhãn gợi ý dùng: `[Trả lời ngay …]` · `[Cần SỐ LIỆU có nguồn]` · `[Cần BẢNG]` ·
`[Cần ý kiến chuyên gia]` · `[Cần ảnh/sơ đồ]` · `[★ Điểm khác biệt]` · `[Link nội bộ → …]`.

**Thực thể nên nhắc:** liệt kê 8–15 khái niệm, thuật ngữ, thông số, tên riêng liên quan mà
các bài top hay dùng (lấy từ bài đối thủ và câu hỏi liên quan). Gắn mỗi H2 chính 2–3 thực thể.

**Ngành nhạy cảm (sức khoẻ, tài chính, pháp lý)** — thêm vào dàn ý:
- Mục "Tác giả / người duyệt / nguồn tham khảo" (người duyệt có chuyên môn, ≥3 nguồn chính thống).
- Mỗi khẳng định chuyên môn gắn sẵn loại nguồn cần trích (Bộ Y tế, WHO, Ngân hàng Nhà nước,
  văn bản pháp luật, biểu phí chính thức…).
- Lưu ý cuối bài: thông tin chỉ tham khảo, không thay tư vấn của chuyên gia.

**Độ dài gợi ý:** lấy theo các bài top đã đọc — từ mức trung bình tới cao hơn bài dài nhất ~10%.
Không cố dài hơn bằng cách độn chữ; vượt đối thủ bằng các mục ★ khác biệt. Ngành nhạy cảm: không
vượt trung bình quá ~30%. Trang dịch vụ / sản phẩm: thường ≤1.500 từ.

## Bước 5 — Meta và phần on-page

- **Meta Title:** ~50–60 ký tự, từ khoá chính ở đầu, có móc thật (con số, "hướng dẫn chi tiết",
  "bảng giá"…), có tên thương hiệu cuối nếu còn chỗ. Không trùng H1 nguyên văn.
- **Meta Description:** ~120–150 ký tự, có từ khoá chính + ≥2 thông tin cụ thể (con số, khoảng
  giá, danh sách), trả lời trước, không dùng câu sáo "khám phá ngay", "tìm hiểu thêm".
- **URL:** chữ thường không dấu, gạch ngang, 3–5 từ, chỉ từ khoá chính (+ phần cần thiết).
- **Liên kết nội bộ:** có website → tìm `site:tenmien.com <chủ đề>` để gợi ý 3–5 trang liên quan;
  chữ gắn link 3–7 từ, mô tả đúng trang đích; không link sang trang cùng ý định (tự giành hạng).
- **Nguồn ngoài:** gợi ý 2–3 nguồn uy tín để trích (cơ quan nhà nước, tổ chức ngành, tài liệu
  chính thức của hãng).
- **Schema gợi ý:** bài thường → Article · có FAQ hiện trên trang → FAQPage · trang sản phẩm →
  Product · dịch vụ địa phương → LocalBusiness/Service · luôn kèm BreadcrumbList.

## Bước 6 — Tự kiểm dàn ý

- [ ] H1 có từ khoá chính, đúng 1 H1.
- [ ] Đoạn mở đầu trả lời thẳng câu hỏi chính trong 40–60 từ đầu.
- [ ] Mọi chủ đề "bắt buộc" (≥3/5 đối thủ có) đều đã có mục.
- [ ] Có ít nhất 1–2 mục ★ khác biệt.
- [ ] Có FAQ nếu đủ điều kiện ở Bước 2.
- [ ] Mỗi H2 có câu trả lời ngắn tự đứng được (đọc riêng vẫn hiểu).
- [ ] Không từ tuyệt đối trong H1 / Meta.
- [ ] Ngành nhạy cảm đã có mục tác giả/nguồn + lưu ý cuối bài.

Đạt ≥7/8 → giao. Thiếu → sửa trước khi giao.

## Đầu ra

```
# Dàn ý — [từ khoá chính]

## Tổng quan
| Mục | Nội dung |
|---|---|
| Từ khoá chính | … |
| Từ khoá phụ | … |
| Ý định / dạng bài | … |
| Người đọc / giai đoạn | … |
| Giọng văn | … |
| Độ dài gợi ý | … – … từ (tham khảo) |
| Rủi ro ngành | Thấp / Vừa / Cao |

## 1. Báo cáo trang kết quả   (khối ở Bước 1)
## 2. Bảng phủ chủ đề + điểm khác biệt ★
## 3. Meta Title · Meta Description · URL
## 4. Dàn ý H1 / sapo / H2 / H3 (kèm ghi chú viết)
## 5. Câu hỏi thường gặp (4–6 câu)
## 6. Thực thể nên nhắc
## 7. Liên kết nội bộ + nguồn ngoài gợi ý
## 8. Brief giao người viết
```

**Brief giao người viết** (mục 8) gồm: mục tiêu bài 1 câu · người đọc · giọng văn · 3 điều bắt
buộc có · 3 điều cấm (gồm từ tuyệt đối) · các mục ★ và vì sao · CTA cuối bài phù hợp giai đoạn
(mới tìm hiểu → mời đọc tiếp bài liên quan; đang so sánh → mời xem bảng giá / tư vấn; sắp mua →
nút liên hệ / đặt hàng rõ ràng).

Người dùng muốn file: xuất .md hoặc .docx nếu môi trường tạo được file.
