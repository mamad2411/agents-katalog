---
name: text-cat-chunk
description: Cắt mọi loại file text dài (SRT có timecode, sách txt có chương, transcript thô, bài viết) thành các file txt chunk ~15000 ký tự có YAML metadata, marker auto-detect (BÀI TẬP, CASE STUDY, CÂU CHỐT, CÂU HỎI HV, BREAK), và timecode (cho SRT). Vòng 1 trong pipeline 3 vòng xử lý nội dung của Phạm Thành Long. Script tự phát hiện loại file. Sử dụng skill này BẤT CỨ KHI NÀO người dùng tải lên file .srt hoặc .txt và yêu cầu "cắt nhỏ", "chia chunk", "xử lý transcript", "xử lý sách", "đóng gói nội dung", "chuẩn bị dữ liệu cho AI", "Vòng 1", "cắt sách thành chunk". Kích hoạt cả khi chỉ tải file lên và nói "xử lý cho tôi", "làm bước 1", hoặc đưa file SRT/txt khóa SSS/IPS/Eagle/LTVM/DTSGC/UT/YES, sách kinh doanh, ghi chú dài. KHÔNG dùng cho tag chủ đề (Vòng 2) hay viết module đào tạo (Vòng 3).
---

# Text Cắt Chunk - Vòng 1 Pipeline Nội Dung PTL

Cắt mọi loại text dài thành chunk có YAML chuẩn để AI xử lý tiếp ở Vòng 2 (tag chủ đề) và Vòng 3 (viết module).

## 3 loại input được hỗ trợ

Script tự phát hiện loại file:

| Loại | Dấu hiệu | Use case |
|---|---|---|
| **SRT** | Có timecode `00:00:00,000 --> ...` | Transcript khóa học từ CapCut |
| **BOOK** | Có cấu trúc `Chapter X`, `Phần Y`, `Bài Z` | Sách giáo trình, ebook |
| **PLAIN** | Không có cấu trúc rõ | Transcript thô, bài viết, ghi chú |

## Quy trình thực hiện

### Bước 1: Xác nhận file

Khi người dùng upload file `.srt` hoặc `.txt`:
- File nằm ở `/mnt/user-data/uploads/`
- Có thể nhiều file cùng lúc

### Bước 2: Detect loại file (tự động)

Script `scripts/text_to_chunks.py` tự phát hiện loại. Có thể override bằng `--loai SRT|BOOK|PLAIN`.

### Bước 3: Chuẩn bị metadata theo loại

**Nếu SRT (transcript khóa):**
- Mã khóa: SSS, IPS, EAGLE, LTVM, DTSGC, UT, YES
- Ngày trong khóa, địa điểm, ngày giảng

Nếu tên file đúng format `[KHOA]_[YYYY]_[MM]_[DIA-DIEM]_D[X].srt` → script tự đoán. Nếu không, hỏi người dùng.

**Nếu BOOK (sách):**
- Tiêu đề, tác giả, thể loại, ngôn ngữ

**Nếu PLAIN (text thuần):**
- Nguồn (ghi chú, bài viết, ai nói/viết...), mô tả ngắn

Hỏi nhanh người dùng các thông tin này nếu chưa rõ. Có thể để mặc định nếu họ không quan tâm.

### Bước 4: Chạy script

**Cú pháp tự động (đa số trường hợp):**
```bash
python3 scripts/text_to_chunks.py /mnt/user-data/uploads/<file> \
    --output-dir /home/claude/output
```

**Với SRT có metadata khóa:**
```bash
python3 scripts/text_to_chunks.py /mnt/user-data/uploads/SSS_2024_08_HN_D1.srt \
    --ngay-giang 2024-08-15 \
    --output-dir /home/claude/output
```

**Với sách:**
```bash
python3 scripts/text_to_chunks.py /mnt/user-data/uploads/the_system.txt \
    --loai BOOK \
    --tieu-de "The System" \
    --tac-gia "Eric Lofholm" \
    --ngon-ngu en \
    --output-dir /home/claude/output
```

**Với text thuần:**
```bash
python3 scripts/text_to_chunks.py /mnt/user-data/uploads/raw_transcript.txt \
    --loai PLAIN \
    --nguon "Buổi nói chuyện Eagle SG 2024" \
    --output-dir /home/claude/output
```

### Bước 5: Kiểm tra & giao file

Sau khi script chạy xong, kiểm tra `summary_report.md` để xác nhận chất lượng:
- Delta < 5%: ✅ TỐT, sẵn sàng dùng
- Delta 5-15%: ⚠️ CHÚ Ý, spot-check vài chunk
- Delta > 15%: ❌ LỖI, không dùng được, cần debug

Sau đó:

**Ít file (≤5):** dùng `present_files` đưa trực tiếp.

**Nhiều file:** zip rồi giao:
```bash
cd /home/claude/output && zip -r /mnt/user-data/outputs/<ten>-chunks.zip .
```

Trình bày kết quả gọn cho người dùng:
- Loại file đã phát hiện (SRT/BOOK/PLAIN)
- Tổng số chunk
- **Delta input/output** (từ summary_report.md)
- Trạng thái audit
- Số marker phát hiện được
- Link tải

## File phụ (output bắt buộc)

Mỗi lần chạy, ngoài các file chunk, script tự động sinh thêm 2 file:

### `manifest.json` — bản đồ dataset (cho AI agents)
- Schema version, thời điểm sinh
- Source (file gốc, loại, tổng ký tự)
- Metadata khóa/sách
- Tóm tắt: tổng chunk, avg/min/max ký tự
- Danh sách đầy đủ các chunk với file_id, ký tự, timecode (SRT) hoặc chương (BOOK)

→ Dùng khi: AI agent cần hiểu cấu trúc toàn bộ dataset, Obsidian/Project Knowledge index.

### `summary_report.md` — phiếu kiểm tra (cho người dùng)
- Bảng tổng quan input/output/delta
- Trạng thái: ✅ TỐT / ⚠️ CHÚ Ý / ❌ LỖI
- Diễn giải nguyên nhân chênh lệch
- Cảnh báo hard-split (chunk vượt 130% target)
- Top 5 chunk lệch xa target
- Hành động đề xuất

→ Dùng khi: kiểm tra chất lượng trước khi sang Vòng 2/3.

## Tham số chunk-size

Mặc định **15000 ký tự** (kích thước thực tế output ~18,000 kt do quy luật cắt cuối câu/cuối paragraph). Có thể chỉnh:
- `--chunk-size 10000` cho file dày đặc, cần xử lý chi tiết
- `--chunk-size 20000` cho khóa dài, ít file hơn
- `--chunk-size 25000` để giảm số file tối đa (chấp nhận chất lượng giảm nhẹ)

## Cấu trúc YAML đầu ra (đồng nhất cho 3 loại)

Tất cả file đều có chung 4 nhóm trường:

1. **LOẠI INPUT**: `loai_input: SRT | BOOK | PLAIN`
2. **METADATA FILE**: thông tin nhận dạng (khác nhau theo loại)
3. **TAG CHỦ ĐỀ** + **LIÊN KẾT PHI TUYẾN**: để trống chờ Vòng 2
4. **TÌNH TRẠNG**: trang_thai

Vòng 2 và Vòng 3 dùng chung 1 logic xử lý cho cả 3 loại — vì YAML đồng nhất.

## Marker auto-detect (chung cho 3 loại)

| Marker | Trigger (VN + EN) |
|---|---|
| `>>> BÀI TẬP <<<` | "bài tập", "lấy giấy ra", "exercise" |
| `### CASE STUDY ###` | "ví dụ", "có một anh/chị", "for example" |
| `*** CÂU CHỐT ***` | "nhớ cho", "key point", "remember this" |
| `??? CÂU HỎI HỌC VIÊN ???` | "học viên hỏi", "anh ơi" |
| `--- BREAK ---` | "nghỉ giải lao", "tea break" |

## Mã khóa được hỗ trợ (cho SRT)

| Mã | Tên đầy đủ |
|---|---|
| SSS | Sales Success System |
| IPS | Internet Power System |
| EAGLE | Eagle Camp |
| LTVM | Lập Trình Vận Mệnh |
| DTSGC | Đánh Thức Sự Giàu Có |
| UT | Ultimate Trainer |
| YES | YES Summit |

## Xử lý hàng loạt

```bash
for f in /mnt/user-data/uploads/*.srt /mnt/user-data/uploads/*.txt; do
    [ -f "$f" ] && python3 scripts/text_to_chunks.py "$f" --output-dir /home/claude/output
done
```

## Khi nào KHÔNG dùng skill này

- Người dùng yêu cầu **gắn tag chủ đề** cho chunk đã có → đó là Vòng 2 (skill khác)
- Người dùng yêu cầu **viết module đào tạo hoàn chỉnh** → đó là Vòng 3 (dùng skill `giao-an-module`)
- File quá ngắn (<2000 ký tự) — không cần chia chunk

## Lưu ý kỹ thuật

- File viết liền 1 dòng dài (không có line break) vẫn xử lý được — script tự fallback chia theo câu
- Tiếng Việt và tiếng Anh đều OK (encoding UTF-8)
- File có ký tự đặc biệt (em dash, smart quotes) vẫn parse được
- Với BOOK, script ưu tiên cắt ở ranh giới chương → chunk có thể lệch ±20% size target để không cắt giữa chương
