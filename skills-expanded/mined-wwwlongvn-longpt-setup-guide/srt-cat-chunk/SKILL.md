---
name: srt-cat-chunk
description: Cắt file SRT (transcript khóa học) thành các file txt nhỏ ~10000 ký tự có YAML metadata, timecode mỗi 3 phút và marker tự động phát hiện (BÀI TẬP, CASE STUDY, CÂU CHỐT, CÂU HỎI HỌC VIÊN, BREAK). Đây là Vòng 1 trong pipeline 3 vòng xử lý transcript khóa học của Phạm Thành Long. Sử dụng skill này BẤT CỨ KHI NÀO người dùng tải lên 1 hoặc nhiều file .srt và yêu cầu "cắt nhỏ", "chia chunk", "xử lý transcript", "chuẩn bị dữ liệu", "convert SRT thành txt", "đóng gói transcript", hoặc nhắc đến "Vòng 1", "pipeline transcript", "xử lý file SRT khóa học". Kích hoạt cả khi người dùng chỉ tải file SRT lên và nói "xử lý cho tôi", "làm bước 1", "cắt giúp", "chuẩn bị cho AI xử lý tiếp", hoặc đưa file SRT của các khóa SSS, IPS, Eagle, LTVM, DTSGC, Ultimate Trainer, YES Summit và yêu cầu chuẩn hóa thành module dữ liệu. KHÔNG dùng skill này cho việc tag chủ đề (Vòng 2) hay viết module đào tạo (Vòng 3) — đó là các bước riêng.
---

# SRT Cắt Chunk - Vòng 1 Pipeline Transcript PTL

Cắt file SRT khóa học thành các file txt chuẩn hóa để AI xử lý tiếp ở Vòng 2 (tag chủ đề) và Vòng 3 (viết module đào tạo).

## Quy trình thực hiện

### Bước 1: Xác nhận file đầu vào

Khi người dùng tải lên file `.srt`, kiểm tra:
- File nằm ở `/mnt/user-data/uploads/`
- Có thể có 1 hoặc nhiều file SRT cùng lúc

### Bước 2: Trích xuất metadata từ tên file

Format tên file chuẩn: `[KHOA]_[YYYY]_[MM]_[DIA-DIEM]_D[X].srt`

Ví dụ: `SSS_2024_08_HN_D1.srt`

Mã khóa được hỗ trợ:

| Mã | Tên đầy đủ |
|---|---|
| SSS | Sales Success System |
| IPS | Internet Power System |
| EAGLE | Eagle Camp |
| LTVM | Lập Trình Vận Mệnh |
| DTSGC | Đánh Thức Sự Giàu Có |
| UT | Ultimate Trainer |
| YES | YES Summit |

Nếu tên file không khớp format, hỏi người dùng:
- Mã khóa là gì?
- Ngày thứ mấy trong khóa?
- Địa điểm tổ chức?
- Ngày giảng (YYYY-MM-DD)?

### Bước 3: Chạy script cắt chunk

Script chính: `scripts/srt_to_chunks.py`

Cú pháp đầy đủ:
```bash
python3 scripts/srt_to_chunks.py /mnt/user-data/uploads/<ten-file>.srt \
    --khoa SSS \
    --ngay 1 \
    --dia-diem "Hà Nội" \
    --ngay-giang 2024-08-15 \
    --chunk-size 10000 \
    --output-dir /home/claude/output
```

Cú pháp tối giản (script tự đoán metadata từ tên file):
```bash
python3 scripts/srt_to_chunks.py /mnt/user-data/uploads/SSS_2024_08_HN_D1.srt \
    --ngay-giang 2024-08-15 \
    --output-dir /home/claude/output
```

### Bước 4: Kiểm tra kết quả

Xem 1-2 file output để xác nhận:
- YAML hợp lệ
- Timecode được chèn
- Marker được phát hiện (nếu có)
- Số ký tự nằm trong khoảng 8,000-12,000

### Bước 5: Đóng gói và giao file

**Nếu chỉ có vài file (≤5):** Dùng `present_files` đưa trực tiếp.

**Nếu có nhiều file:** Nén thành .zip rồi present:
```bash
cd /home/claude/output && zip -r /mnt/user-data/outputs/<ten-khoa>-chunks.zip .
```

Trình bày kết quả gọn:
- Tổng số chunk đã cắt
- Tổng thời lượng giảng
- Số marker phát hiện được (BÀI TẬP, CASE STUDY, etc.)
- Link file zip

## Tham số chunk-size

- **10000** (mặc định): tối ưu cho AI xử lý ở Vòng 2-3
- **8000**: nếu giảng viên nói nhanh, nội dung dày
- **12000**: nếu giảng viên nói chậm, nhiều câu chuyện kéo dài

Script tự co giãn ±20% để cắt ở ranh giới câu (không cắt giữa câu).

## Xử lý nhiều file cùng lúc

Nếu người dùng tải nhiều file SRT (ví dụ cả 3 ngày của 1 khóa):

```bash
for f in /mnt/user-data/uploads/*.srt; do
    python3 scripts/srt_to_chunks.py "$f" \
        --ngay-giang 2024-08-15 \
        --output-dir /home/claude/output
done
```

Sau đó zip toàn bộ thành 1 file giao cho người dùng.

## Marker auto-detect

Script tự phát hiện và chèn 5 loại marker:

| Marker | Trigger |
|---|---|
| `>>> BÀI TẬP <<<` | "bài tập", "lấy giấy ra", "thực hành ngay", "viết ra" |
| `### CASE STUDY ###` | "ví dụ", "có một anh/chị/học viên", "câu chuyện là" |
| `*** CÂU CHỐT ***` | "nhớ cho", "chốt lại", "quy luật", "điều quan trọng nhất" |
| `??? CÂU HỎI HỌC VIÊN ???` | "học viên hỏi", "anh ơi", "chị ơi" |
| `--- BREAK ---` | "nghỉ giải lao", "tea break" |

Nếu auto-detect bỏ sót, người dùng có thể chỉnh thủ công sau.

## Cấu trúc YAML đầu ra

Mỗi file txt có YAML header với 4 nhóm trường:

1. **METADATA FILE**: thông tin nhận dạng (khoa, ngày, chunk, timecode, ký tự)
2. **TAG CHỦ ĐỀ**: để trống (`[]`) — Vòng 2 sẽ điền
3. **LIÊN KẾT PHI TUYẾN**: để trống (`null`) — Vòng 2 sẽ điền  
4. **TÌNH TRẠNG**: trang_thai = "cleaned" sau khi script chạy xong

Vòng 2 (tag chủ đề) sẽ chuyển trạng thái thành `tagged`. Vòng 3 (viết module) sẽ chuyển thành `module-ready`.

## Khi nào KHÔNG dùng skill này

- Người dùng yêu cầu **gắn tag chủ đề** cho chunk đã có → đó là Vòng 2
- Người dùng yêu cầu **viết module đào tạo hoàn chỉnh** từ chunk → đó là Vòng 3 (dùng skill `giao-an-module`)
- File đầu vào không phải SRT (txt thường, docx, audio thô) → cần convert sang SRT trước (CapCut)
