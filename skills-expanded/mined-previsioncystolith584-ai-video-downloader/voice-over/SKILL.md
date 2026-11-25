---
name: voice-over
description: >
  Tự động hoá toàn bộ pipeline: transcript.json (tiếng Trung) → AI tự dịch sang tiếng Việt →
  TTS (OmniVoice / Vbee / ElevenLabs / OpenAI) → ghép audio vào video gốc → xuất output_vi.mp4.
  AI tự chọn voice phù hợp từ voice/<provider>.csv dựa trên nội dung video — không hỏi user.
  Trigger khi user cung cấp đường dẫn folder chứa transcript.json + index.mp4 và yêu cầu
  "dịch", "lồng tiếng", "generate", "xuất video tiếng Việt", "/voice-over <path>".
  Cú pháp: /voice-over <path> [--voice <code>] [--provider omnivoice|vbee|elevenlabs|openai]
metadata:
  version: 1.1.0
  license: MIT
---

# Voice Over

## QUAN TRỌNG — KHÔNG BAO GIỜ HỎI LẠI USER

**Tuyệt đối không hỏi user bất cứ điều gì.** Tự xử lý toàn bộ pipeline từ đầu đến cuối:
- Thiếu `transcript.json` → tự chạy Whisper
- Thiếu `transcript-vi.json` → AI tự dịch
- Không có `--voice` → AI tự chọn voice từ CSV
- Bất kỳ file nào thiếu → tự tạo, không hỏi

## QUAN TRỌNG — KHÔNG TỰ VIẾT PYTHON CODE

**Tuyệt đối không tự viết inline Python để transcribe hay xử lý file.**
Chỉ được phép dùng đúng các lệnh CLI sau đây:
- Transcribe: `backend/.venv/bin/python3 -m backend transcribe "$FOLDER/index.mp4"`
- TTS: dùng đúng đoạn code ở Bước 4

Lý do: CLI đã được cấu hình đúng (`word_timestamps=False`, output format chuẩn). Tự viết code sẽ tạo ra file sai format (có `words`, sai encoding, v.v.).

Pipeline đầy đủ: **index.mp4 → transcript.json → transcript-vi.json → dub_vi.mp3 → output_vi.mp4**

## Cấu trúc thư mục chuẩn

```
downloads/<author>/<video-folder>/
  ├── index.mp4           ← video gốc (bắt buộc)
  ├── transcript.json     ← transcript tiếng Trung (bắt buộc)
  ├── transcript-vi.json  ← bản dịch tiếng Việt (nếu đã có → bỏ qua bước dịch)
  ├── dub_vi.mp3          ← audio TTS (tạo mới mỗi lần)
  └── output_vi.mp4       ← output cuối (ghi đè nếu đã có)
```

## Khi nào trigger

```
/voice-over <path>
voice-over <path>
lồng tiếng <path>
dịch video <path>
xuất tiếng Việt <path>
```

`<path>` có thể là:
- Đường dẫn tuyệt đối tới folder video
- Đường dẫn tương đối từ project root (`downloads/<author>/<folder>`)

## Quy trình từng bước

### Bước 1 — Validate đầu vào và tự transcribe nếu cần

```bash
FOLDER="<path được truyền vào>"
test -f "$FOLDER/index.mp4" || { echo "✗ Thiếu index.mp4"; exit 1; }
```

**Nếu `$FOLDER/transcript.json` chưa tồn tại** → **tự chạy Whisper ngay**, không hỏi:

```bash
cd /Users/thinhlevan/Downloads/douyin-downloader
backend/.venv/bin/python3 -m backend transcribe "$FOLDER/index.mp4"
```

Whisper sẽ tạo ra `$FOLDER/transcript.json`. Sau khi xong tiếp tục Bước 2.

**Nếu `$FOLDER/transcript.json` đã có** → đọc thông tin và tiếp tục:

```bash
backend/.venv/bin/python3 -c "
import json
d = json.load(open('$FOLDER/transcript.json'))
print(f'Segments: {len(d[\"segments\"])}')
print(f'Text: {d[\"text\"][:120]}...')
"
```

**KHÔNG hỏi user** ở bước này hay bất kỳ bước nào — tự xử lý hết.

### Bước 2 — Dịch transcript (bỏ qua nếu transcript-vi.json đã tồn tại)

**Nếu `$FOLDER/transcript-vi.json` đã tồn tại** → thông báo "Dùng bản dịch có sẵn" và bỏ qua bước này.

**Nếu chưa có** → **AI tự dịch** bằng Read/Write tool (không gọi script, không cần API key):

1. Dùng **Read tool** đọc `$FOLDER/transcript.json`
2. **Tự dịch** toàn bộ nội dung sang tiếng Việt tự nhiên, phong cách vlog trẻ:
   - Dịch field `text` ở cấp top-level
   - Dịch từng `text` trong mỗi phần tử `segments[]`
   - Giữ nguyên toàn bộ cấu trúc JSON: `language`, `language_probability`, `segments[].start/end/probability`
   - **KHÔNG có field `words`** trong transcript — script transcribe chạy `word_timestamps=False`, đừng tự thêm hay generate lại
3. Dùng **Write tool** ghi kết quả ra `$FOLDER/transcript-vi.json`

### Bước 3 — Phát hiện provider từ `.env`, rồi chọn voice

#### 3.1 — Đọc `.env` TRƯỚC TIÊN để biết đang có key của supplier nào

**Bắt buộc làm bước này đầu tiên.** Mục đích: chọn đúng provider ngay từ đầu, **KHÔNG thử lần lượt từng supplier** (đỡ đi vòng vòng, đỡ timeout server không bật).

```bash
# từ project root — liệt kê các key đang set trong .env (ẩn value)
test -f .env && grep -vE '^\s*#' .env | grep -E '^[A-Z]' | sed -E 's/=.*/=set/' || echo "KHÔNG có .env"
```

Quy tắc chọn provider dựa trên key có trong `.env`:

| Key có trong `.env` | → Provider | CSV dùng |
|---|---|---|
| `VBEE_TOKEN` + `VBEE_APP_ID` | `vbee` | `voice/vbee.csv` |
| `ELEVENLABS_API_KEY` | `elevenlabs` | `voice/elevenlabs.csv` |
| `OPENAI_API_KEY` | `openai` | `voice/openai.csv` |
| (không có key nào) | `omnivoice` (server LAN, không cần key) | `voice/omnivoice.csv` |

Quy tắc quyết định:
- User **chỉ định `--voice <code>`** → dùng luôn, bỏ qua cả 3.1 lẫn 3.2.
- User **chỉ định `--provider`** → ưu tiên cái đó, bỏ qua phát hiện từ `.env`.
- `.env` có key của **nhiều** supplier → ưu tiên: `vbee` > `elevenlabs` > `openai` (đặt `omnivoice` cuối vì cần server LAN bật, dễ timeout).
- **CHỈ đọc đúng 1 CSV** của provider đã chọn — tuyệt đối không mở nhiều CSV / không thử nhiều provider lần lượt.

> Ví dụ thực tế: `.env` chỉ có `VBEE_TOKEN` + `VBEE_APP_ID` → provider = **vbee**, chỉ chọn voice trong `voice/vbee.csv`.

#### 3.2 — Chọn voice từ `voice/<provider>.csv` (chỉ provider đã chọn ở 3.1)

**Tiêu chí tự chọn voice** (AI đọc CSV và quyết định):
1. Dùng **Read tool** đọc `voice/<provider>.csv`
2. Phân tích nội dung video từ `transcript-vi.json` (vlog / review / tin tức / kể chuyện...)
3. Chọn voice phù hợp nhất dựa trên các cột: `category`, `gender`, `age_group`, `use_case`, `description`
   - Vlog trẻ, đời thường → ưu tiên `young`, `female` hoặc `male`, region phù hợp
   - Review phim → ưu tiên category `review`
   - Tin tức → ưu tiên category `news`
4. Thông báo cho user voice đã chọn + lý do ngắn gọn

Ví dụ output:
```
→ Tự chọn voice: sg_female_thaotrinh_full_44k-phg.mp3 (SG - Thảo Trinh)
  Lý do: vlog trẻ, giọng nữ Nam Bộ tự nhiên, category=vlog
```

Cú pháp đầy đủ skill chấp nhận:
```
/voice-over <path>
/voice-over <path> --voice <voice_code>
/voice-over <path> --provider vbee
/voice-over <path> --provider omnivoice --voice <voice_code>
```

### Bước 4 — TTS

**Dùng đúng provider đã chọn ở Bước 3.1** — chỉ chạy 1 script tương ứng, không thử provider khác.

Script inline `-c` KHÔNG qua `__main__.py` nên phải tự `load_dotenv('.env')` để đọc key trong `.env` (vbee/elevenlabs/openai cần key; omnivoice không cần nhưng để vẫn vô hại). `cd "$(git rev-parse --show-toplevel)"` về đúng project root (nơi có `.env` + `backend/`).

**Vbee** (khi `.env` có `VBEE_TOKEN` + `VBEE_APP_ID`):
```bash
cd "$(git rev-parse --show-toplevel)"
backend/.venv/bin/python3 -c "
import asyncio, json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env')
from backend.voices.vbee import run_tts

async def main():
    folder = Path('$FOLDER')
    vi_text = json.loads((folder / 'transcript-vi.json').read_text())['text']
    result = await run_tts(text=vi_text, voice_code='$VOICE_CODE',
                           output=str(folder / 'dub_vi.mp3'), log=print)
    print(f'TTS done: {result[\"bytes\"]:,} bytes, mode={result[\"mode\"]}')
asyncio.run(main())
"
```

**OmniVoice** (khi `.env` không có key nào — dùng server LAN):
```bash
cd "$(git rev-parse --show-toplevel)"
backend/.venv/bin/python3 -c "
import asyncio, json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv('.env')
from backend.voices.omnivoice import run_tts

async def main():
    folder = Path('$FOLDER')
    vi_text = json.loads((folder / 'transcript-vi.json').read_text())['text']
    result = await run_tts(text=vi_text, voice_code='$VOICE_CODE',
                           output=str(folder / 'dub_vi.mp3'), log=print)
    print(f'TTS: {result[\"bytes\"]:,} bytes')
asyncio.run(main())
"
```

Timeout: 180 giây.

### Bước 5 — Tạo file SRT subtitle

Chạy ngay sau khi có `transcript-vi.json`, **trước khi** ghép video:

```bash
cd /Users/thinhlevan/Downloads/douyin-downloader
backend/.venv/bin/python3 -c "
import json
from pathlib import Path

def fmt(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int((s - int(s)) * 1000)
    return f'{h:02d}:{m:02d}:{sec:02d},{ms:03d}'

folder = Path('$FOLDER')
data = json.loads((folder / 'transcript-vi.json').read_text())
lines = []
for i, seg in enumerate(data['segments'], 1):
    lines.append(f'{i}\n{fmt(seg[\"start\"])} --> {fmt(seg[\"end\"])}\n{seg[\"text\"].strip()}\n')
(folder / 'subtitle_vi.srt').write_text('\n'.join(lines), encoding='utf-8')
print(f'SRT: {len(data[\"segments\"])} dòng → subtitle_vi.srt')
"
```

### Bước 6 — Ghép video + audio bằng ffmpeg

```bash
ffmpeg -y \
  -i "$FOLDER/index.mp4" \
  -i "$FOLDER/dub_vi.mp3" \
  -filter_complex "[0:a]volume=0.10[orig];[1:a]volume=1.0[dub];[orig][dub]amix=inputs=2:normalize=0[mix]" \
  -map 0:v -map "[mix]" \
  -c:v copy -c:a aac -b:a 192k \
  "$FOLDER/output_vi.mp4"
```

Tham số:
- `volume=0.10` cho tiếng gốc (giảm còn 10% làm nền)
- `volume=1.0` cho dub tiếng Việt (full volume)
- `-c:v copy` giữ nguyên video stream, không re-encode

### Bước 6 — Báo cáo kết quả

```
✅ Xong!

📁 $FOLDER/
  ├── transcript-vi.json   ← bản dịch tiếng Việt
  ├── subtitle_vi.srt      ← subtitle tiếng Việt
  ├── dub_vi.mp3           ← audio TTS (<size> bytes)
  └── output_vi.mp4        ← video hoàn chỉnh (<size> MB)

Giọng: <voice_name>
Thời lượng: <duration>
```

Gợi ý tiếp theo:
```
Mở xem: open "$FOLDER/output_vi.mp4"
```

---

## Xử lý lỗi

| Triệu chứng | Nguyên nhân | Fix |
|---|---|---|
| `ConnectionError: Không kết nối được OmniVoice` | Server TTS tắt | Kiểm tra `http://192.168.1.61:8002` có chạy không |
| `ModuleNotFoundError: No module named 'httpx'` | Chạy sai Python | Dùng `backend/.venv/bin/python3` thay vì `python3` |
| `ffmpeg: No such file` | ffmpeg chưa cài | `brew install ffmpeg` |
| `output_vi.mp4` = 0 bytes | ffmpeg lỗi | Chạy lại ffmpeg tay, xem stderr |
| Giọng đọc nghe sai | Voice không phù hợp | Chạy lại với `--voice <code>` khác |
| `transcript-vi.json` chất lượng kém | AI dịch sai do thiếu context | Sửa tay file JSON rồi chạy lại từ Bước 4 |

---

## Ví dụ end-to-end

User gõ:
```
/voice-over downloads/jingxuan/Natsu__花火大会__7648442197494222131 --voice sg_female_thaotrinh_full_44k-phg.mp3
```

Skill làm:
1. Validate `index.mp4` + `transcript.json` tồn tại ✓
2. `transcript-vi.json` đã có → bỏ qua dịch
3. Voice đã chỉ định → bỏ qua hỏi
4. Chạy TTS → `dub_vi.mp3` (~2MB)
5. ffmpeg merge → `output_vi.mp4`
6. Báo cáo xong + gợi ý `open output_vi.mp4`

---

## Khi nào KHÔNG dùng

| Muốn | Làm gì |
|---|---|
| Chỉ dịch transcript, không xuất video | Dừng sau Bước 2 |
| Dùng lại bản dịch cũ nhưng đổi giọng | Xóa `dub_vi.mp3`, giữ `transcript-vi.json`, chạy lại với `--voice` khác |
| Batch nhiều video cùng lúc | Lặp qua nhiều folder, gọi skill này cho từng folder |
| Thêm subtitle | Skill này chưa hỗ trợ — cần SRT workflow riêng |
