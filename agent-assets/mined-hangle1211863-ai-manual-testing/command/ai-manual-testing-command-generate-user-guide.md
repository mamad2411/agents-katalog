---
description: Sinh Hướng dẫn sử dụng (User Guide) cho người dùng cuối từ requirements và evidence đã khảo sát. Hỗ trợ 2 mode — DOC (từ tài liệu có sẵn) và LIVE (chạy thật trên browser, chụp ảnh mới).
skills:
  - skills-user-guide-writer
  - skills-requirements-analyzer
  - skills-manual-test-executor
---

# Workflow: Sinh Hướng Dẫn Sử Dụng

> **BẮT BUỘC (MANDATORY SKILL):** Bạn PHẢI nạp và đọc kỹ **`skills-user-guide-writer`** (tại `.claude/skills/skills-user-guide-writer/SKILL.md`) — đặc biệt mục **Ranh giới**, **Quy Tắc Chống Bịa** và **Quality Gate** — trước khi viết dòng đầu tiên.

Tài liệu để **người dùng cuối làm được việc**, không phải để QA/dev hiểu hệ thống.

## ⚠️ Chọn đúng workflow

| User cần | Workflow đúng | Người đọc |
|---|---|---|
| *"Hệ thống phải làm gì, ràng buộc nào"* | `/generate-requirements-from-website` | QA · Dev · BA |
| *"Kịch bản kiểm thử"* | `/generate-testcases-manual-rbt` | Tester |
| *"Tài liệu hướng dẫn khách hàng dùng phần mềm"* | **Workflow này** | **Người dùng cuối** |

> Ba tài liệu này **không thay thế nhau** và **không chép qua lại được**. Xem bảng Ranh giới trong skill.

## ⚠️ Nguyên tắc thực thi

- **Tất cả output bằng Tiếng Việt**, viết cho người **không biết thuật ngữ hệ thống**
- **KHÔNG BỊA bước.** Mọi bước truy được về: một tấm ảnh evidence đã mở · một REQ ID · một lần thao tác thật trong phiên này. Không truy được → gắn `⚠️ Chưa xác minh`, liệt kê ở mục 6
- **Chép nguyên văn** nhãn nút, tên menu, thông báo — không diễn đạt lại
- 🔒 **Ảnh phải dùng dữ liệu mẫu.** Tài liệu này phát ra ngoài — ảnh có tên/email/số tiền khách hàng thật là rò rỉ dữ liệu
- **Write-first:** ghi thẳng vào file, chat chỉ hiện tiến độ. Không render cả tài liệu ra chat

## 2 Chế độ (Mode)

| Mode | Khi nào | Nguồn bước & ảnh |
|---|---|---|
| **DOC** (mặc định) | Module đã recon đủ, evidence đầy đủ, không truy cập được hệ thống lúc này | Requirements + ảnh trong `evidence/` |
| **LIVE** | Có quyền truy cập hệ thống · cần ảnh sạch dùng dữ liệu mẫu · evidence cũ thiếu hoặc UI đã đổi | Chạy thật từng việc qua Playwright MCP, chụp ảnh mới |

> **Mặc định đề xuất LIVE khi có tài khoản test.** Ảnh recon cũ chụp để chứng minh REQ — thường full-page, thường có dữ liệu thật, dùng làm minh hoạ hướng dẫn là sai mục đích.

---

## Bước 0: Chốt phạm vi (CHECKPOINT — hỏi user)

| Cần chốt | Vì sao không suy ra được |
|---|---|
| **Module** | Một lần một module |
| **Đối tượng đọc + role** | Cùng module nhưng người dùng role Sales và role Admin thấy hai giao diện khác nhau. Không chốt thì viết lẫn quyền |
| **Phiên bản phần mềm** | Ghi ở đầu tài liệu. Không có thì tài liệu vô giá trị sau 2 sprint |
| **Mode** | DOC hay LIVE — xem bảng trên |
| **Bản này gửi ra ngoài không** | Có → mục 6 *Vùng chưa xác minh* phải gỡ ở bản phát hành, và soát ảnh kỹ hơn |

⏸️ Chốt xong mới sang Bước 1.

---

## Bước 1: Đọc nguồn — mở HẾT evidence trước khi viết

1. `docs/requirements/README.md` — xác nhận module đã recon (⬜ Chưa recon → **dừng**, đề nghị chạy `/generate-requirements-from-website` trước)
2. `docs/requirements/<module>/REQUIREMENTS_<TÊN_MODULE>_SUMMARY.md` — luồng, trường bắt buộc, thông báo, ma trận phân quyền
3. **Mở 100% ảnh** trong `docs/requirements/<module>/<nền-tảng>/evidence/` — nhìn thật, không đọc tên file rồi đoán
4. Ghi lại: nhãn nút/menu **nguyên văn**, thông báo **nguyên văn**, trường bắt buộc, thao tác không hồi lại được (→ cảnh báo ⚠️)

> Requirements ghi có tính năng nhưng không ảnh nào cho thấy nó → **không viết**, đưa vào mục 6.

---

## Bước 2: Lập danh sách việc người dùng cần làm (CHECKPOINT)

Đây là bước quyết định chất lượng cả tài liệu. **Chuyển từ tư duy màn hình sang tư duy việc:**

| ❌ Theo màn hình (sai) | ✅ Theo việc (đúng) |
|---|---|
| Màn hình danh sách khách hàng | Tìm một khách hàng đã có |
| Form thêm/sửa khách hàng | Thêm khách hàng mới · Sửa thông tin khách hàng |
| Popup xác nhận xoá | Xoá khách hàng không còn giao dịch |

Trình bày cho user duyệt:

```
Danh sách việc — module Khách hàng · role Sales (8 việc)
1. Thêm một khách hàng mới          (REQ-CUST-01,02,05)
2. Tìm khách hàng đã có             (REQ-CUST-11)
3. Sửa thông tin khách hàng         (REQ-CUST-07)
...
⚠️ Chưa xác minh: Xuất Excel — REQ-CUST-15 có nêu, không ảnh nào thấy nút
```

⏸️ **Hỏi user:** thiếu việc nào người dùng hay làm không · việc nào bỏ được. Chờ duyệt rồi mới viết.

---

## Bước 3 (Mode LIVE): Chạy thật & chụp ảnh

Theo thứ tự bắt buộc của `CLAUDE.md` mục Browser Rules: `navigate → wait_for → snapshot → interact → screenshot`.

1. Đăng nhập bằng tài khoản **đúng role** đã chốt ở Bước 0
2. Với mỗi việc: làm **đúng** trình tự sẽ viết trong tài liệu — phát hiện luôn bước thừa/thiếu mà nhìn ảnh không thấy
3. Chụp ảnh **chỉ ở bước khó tìm** (menu lồng nhau, nút nhỏ, trạng thái đặc biệt), đặt tên theo việc: `them-khach-hang-buoc-2.png`
4. **Mở lại từng ảnh vừa chụp xác nhận đúng trạng thái** trước khi đưa vào tài liệu
5. 🔒 Dữ liệu nhập vào phải là **dữ liệu mẫu** (`Công ty Mẫu ABC`, `demo@example.com`) — ảnh này sẽ đi ra ngoài

> ⚠️ **Môi trường dùng chung:** không chạy việc phá huỷ (xoá, huỷ, đóng). Viết hướng dẫn cho thao tác đó dựa trên evidence và gắn `⚠️ Chưa xác minh` nếu chưa từng thấy màn hình xác nhận.
>
> 📌 Playwright MCP có thể ghi ảnh sai cwd — chụp bằng **tên file trần** rồi copy về `docs/user-guides/<module>/images/`.

---

## Bước 4: Viết theo batch

Theo **Cấu Trúc Tài Liệu** trong skill. Ghi thẳng vào file, mỗi batch 2–3 việc, chat chỉ báo tiến độ.

File: `docs/user-guides/<module>/user_guide_<module>.md` — **tên index bất biến**, cùng quy ước với `REQUIREMENTS_<TÊN_MODULE>_SUMMARY.md`.

```
docs/user-guides/
├── README.md                              ← DANH MỤC — module nào đã có hướng dẫn, cho role nào
└── <module>/
    ├── user_guide_<module>.md             ← INDEX — TÊN FILE BẤT BIẾN
    ├── images/*.png                        ← ảnh minh hoạ, tên theo việc
    └── parts/part_NN_<slug>.md             ← chỉ khi > 15 việc
```

Mỗi việc viết theo thứ tự: **Khi nào dùng** → **các bước đánh số** → **cảnh báo đặt ngay trước bước gây hậu quả** → **bảng "Nếu không được"**.

⚠️ **Hai phần sau là có điều kiện, không bắt buộc có mặt:** thủ tục không có thao tác nào gây hậu quả thì **không viết cảnh báo**; không có tình huống lỗi nào có bằng chứng thì **bỏ hẳn bảng**. Bảng 1 dòng là hợp lệ — xem *Không độn bảng* trong skill.

> Bảng *"Nếu không được"* là phần người dùng đọc nhiều nhất và là phần AI hay bỏ nhất. Lấy từ thông báo lỗi có trong requirements/evidence — **không bịa** thông báo.

---

## Bước 5: Quality Gate & xuất

Chạy đủ **10 tiêu chí Quality Gate** của skill. Bốn tiêu chí hay trượt nhất:

- [ ] **Tổ chức theo việc** — đọc mục lục mục 2, mọi dòng bắt đầu bằng động từ (*"Thêm…", "Tìm…"*), không có dòng nào là tên màn hình
- [ ] **🔒 Ảnh không có dữ liệu thật** — mở lại **từng** ảnh, soát tên người, email, số điện thoại, số tiền
- [ ] **Nhãn nguyên văn** — đối chiếu lại với ảnh, không diễn đạt lại
- [ ] **Không độn bảng** — mỗi dòng *"Nếu không được"* và mỗi câu FAQ chỉ ra được bằng chứng; dòng nghe hợp lý mà không có nguồn → xoá

Cập nhật `docs/user-guides/README.md`: module · role · phiên bản phần mềm · ngày cập nhật · số việc · số mục còn `⚠️ Chưa xác minh`.

---

## Bàn giao

**Báo cáo cho user:** số việc đã viết · số ảnh · danh sách mục `⚠️ Chưa xác minh` kèm lý do · đường dẫn file.

**Nhắc user 2 việc trước khi gửi khách:**

1. **Gỡ mục 6 (Vùng chưa xác minh)** ở bản phát hành — đó là ghi chú nội bộ
2. Soát lại ảnh lần cuối: không URL nội bộ, không tài khoản, không dữ liệu khách hàng thật

---

## Cập nhật khi UI đổi

**Không viết lại từ đầu.** Theo bảng *Bảo Trì* trong skill: sửa đúng việc bị ảnh hưởng, chụp lại ảnh của **các bước đổi**, tăng **Phiên bản tài liệu**, cập nhật **Áp dụng cho phiên bản phần mềm**. Bản cũ tra bằng lịch sử git — **không** tạo thư mục `archive/`.

> Ticket đổi UI đã chạy `/update-requirements-from-ticket` → đọc **Impact Report** để biết đúng việc nào cần sửa, thay vì rà lại cả tài liệu.

---

## Mối quan hệ với workflows khác

```
/discover-system → /generate-requirements-from-website ──┬──→ /generate-testcases-manual-rbt   (cho Tester)
                                                          └──→ /generate-user-guide            (cho Người dùng cuối)
```

Cùng một lần recon, hai đầu ra cho hai loại người đọc. Đó là lý do skill này **bắt buộc** module đã recon: nó không tự khảo sát hệ thống, nó chuyển hoá thứ đã khảo sát.
