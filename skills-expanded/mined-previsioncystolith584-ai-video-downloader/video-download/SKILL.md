---
name: video-download
description: >
  Tải video từ bất kỳ link nào người dùng đưa bằng yt-dlp (YouTube, TikTok,
  Facebook, Instagram, Twitter/X, Bilibili, Vimeo, và 1000+ trang khác).
  Dùng skill này khi người dùng paste một link video (không phải Douyin) và muốn
  tải về, download, lưu video — kể cả khi họ không gõ chữ "tải".
  Với link douyin.com hãy dùng skill douyin-crawler thay vì skill này.
metadata:
  version: 1.0.0
  license: MIT
---

# Video Download Skill

Tải video từ link người dùng đưa bằng **yt-dlp** → **tải luôn** (không hỏi lại).

## Mặc định

- **Tải luôn** link người dùng đưa, chất lượng tốt nhất, xuất ra `.mp4`.
- **Nhiều link** → tải lần lượt từng link.
- **Không tải cả playlist/channel** trừ khi user yêu cầu rõ ("tải cả playlist", "tải hết kênh") — lúc đó bỏ cờ `--no-playlist`.
- Với link **douyin.com** → KHÔNG dùng skill này, chuyển sang `/douyin-crawler`.

## Bước 0 — Kiểm tra yt-dlp đã cài chưa

```bash
which yt-dlp || echo "CHƯA CÀI"
```

**Nếu chưa cài** → cài ngay, không hỏi:

```bash
# Ưu tiên Homebrew (macOS)
brew install yt-dlp 2>/dev/null \
  || backend/.venv/bin/pip install -U yt-dlp   # fallback: cài vào venv backend
```

Nếu cài vào venv thì gọi bằng `backend/.venv/bin/python3 -m yt_dlp` thay cho `yt-dlp` ở các bước sau.

> Cần `ffmpeg` để ghép video+audio chất lượng cao. Nếu thiếu: `brew install ffmpeg`.

## Bước 1 — Tải video

Chạy từ project root. Mỗi link người dùng đưa chạy một lệnh:

```bash
yt-dlp \
  -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" \
  --merge-output-format mp4 \
  --no-playlist \
  --write-info-json \
  --write-thumbnail \
  --restrict-filenames \
  -o "downloads/%(extractor)s/%(title).80B__%(id)s/index.%(ext)s" \
  "<URL>"
```

Giải thích cờ:
- `-f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"` — video + audio tốt nhất, fallback file đơn.
- `--merge-output-format mp4` — ghép thành `.mp4`.
- `--no-playlist` — chỉ tải đúng video trong link (bỏ cờ này nếu user muốn cả playlist).
- `--write-info-json` — lưu metadata thành `index.info.json` (giống `metadata.json` của douyin).
- `--write-thumbnail` — lưu ảnh thumbnail.
- `-o "downloads/%(extractor)s/%(title).80B__%(id)s/index.%(ext)s"` — cấu trúc thư mục giống douyin: `downloads/<trang>/<title>__<id>/index.mp4`.

**Nhiều link**: lặp qua từng URL, mỗi URL một lệnh `yt-dlp` như trên.

**Tải cả playlist/kênh** (khi user yêu cầu): bỏ `--no-playlist`, đổi output template để tránh đè file:

```bash
-o "downloads/%(extractor)s/%(uploader)s/%(playlist_title|)s/%(title).80B__%(id)s/index.%(ext)s"
```

## Bước 2 — Báo cáo kết quả

Sau khi tải xong, liệt kê file và báo cáo:

```bash
ls -lh "downloads/<extractor>/<folder>/"
```

Mẫu báo cáo:
```
✅ Đã tải xong!

📁 downloads/<trang>/<title>__<id>/
  ├── index.mp4            ← video (<size> MB)
  ├── index.info.json      ← metadata
  └── index.<ext>          ← thumbnail

Nguồn: <URL>
Mở xem: open "downloads/<trang>/<title>__<id>/index.mp4"
```

## Cấu trúc downloads

```
downloads/<extractor>/<title>__<id>/
  ├── index.mp4           ← video đã ghép
  ├── index.info.json     ← metadata yt-dlp
  └── index.webp/jpg      ← thumbnail
```

`<extractor>` là tên trang yt-dlp nhận diện (youtube, tiktok, facebook, instagram...).

## Liên kết với pipeline khác

Folder tải về có `index.mp4` nên **dùng được luôn với `/voice-over`** để dịch + lồng tiếng Việt:

```
/voice-over downloads/<extractor>/<title>__<id>
```

## Xử lý lỗi

| Triệu chứng | Nguyên nhân | Fix |
|---|---|---|
| `yt-dlp: command not found` | Chưa cài | `brew install yt-dlp` (xem Bước 0) |
| `ERROR: ... Requested format is not available` | Format filter quá chặt | Đổi `-f` thành `-f best` |
| `ffmpeg not found` / không ghép được | Thiếu ffmpeg | `brew install ffmpeg` |
| `ERROR: ... Sign in to confirm / login required` | Trang cần đăng nhập | Thêm `--cookies-from-browser chrome` (hoặc safari/firefox) |
| Video tải về thiếu tiếng | Stream audio riêng chưa ghép | Đảm bảo có ffmpeg + `--merge-output-format mp4` |
| Bị chặn theo vùng / rate limit | Server chặn | Thêm `--geo-bypass` hoặc thử lại sau |

## Khi nào KHÔNG dùng skill này

| Tình huống | Dùng gì |
|---|---|
| Link `douyin.com` | `/douyin-crawler` |
| Đã có folder + muốn dịch/lồng tiếng Việt | `/voice-over <path>` |
