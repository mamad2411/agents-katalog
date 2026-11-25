---
name: od-video
description: Dựng video marketing dọc/ngang bằng HyperFrames trong Open Design — render local 0 credit, kèm lồng tiếng Kokoro và nhạc nền có ducking. Dùng khi cần tạo reel, promo, explainer, video quảng cáo từ tài liệu/ảnh/Figma; khi sửa hoặc render lại một composition HyperFrames; hoặc khi thêm voiceover/nhạc vào video có sẵn. Chứa toàn bộ bẫy môi trường và lỗi đã gặp thật để không lặp lại.
---

# Dựng video trong Open Design bằng HyperFrames

## 1. Đây là gì và tại sao chọn nó

HyperFrames render một trang HTML/CSS/GSAP thành MP4 bằng Chrome headless + ffmpeg,
**chạy trên máy, không gọi API, không tốn credit**. Trong Open Design nó là một
provider của media dispatcher, và là provider video **duy nhất không cần API key**:

```
apps/daemon/src/media/models.ts:38
{ id: 'hyperframes', integrated: true, credentialsRequired: false, settingsVisible: false }
```

Mọi renderer video khác (Volcengine Seedance, fal Veo/Sora, Grok, OpenRouter, MiniMax)
đều nhận `credentials: ProviderConfig` và ném lỗi nếu thiếu `apiKey`. HyperFrames là
renderer duy nhất không có tham số đó.

**Giới hạn phải nói trước với user.** HyperFrames không phải AI video. Nó dựng
motion graphics, kinetic typography, slideshow ảnh động, mock UI, data viz — tức là
mọi thứ vẽ được bằng HTML/CSS. Nó **không** sinh được cảnh quay thật, người thật,
b-roll. Nếu user cần video AI cinematic thì phải dùng provider trả phí. Nói rõ điều
này trước khi bắt tay, đừng để user kỳ vọng sai.

## 2. Môi trường — ba bẫy phải xử lý trước mọi thứ

Ba cái này làm hỏng lệnh đầu tiên nếu bỏ qua. Xử lý trước, đừng debug sau.

**Node mặc định là v20, HyperFrames đòi ≥22.** Luôn mở đầu bằng:
```bash
export PATH="$HOME/.nvm/versions/node/v24.18.0/bin:$PATH"
```

**`npx` bị hook rewrite thành `npm`** → `npx hyperframes@X render` báo
`Unknown command: hyperframes@X`. Không gọi `npx` trực tiếp. Dùng script trong
`package.json` (`npm run render`), bên trong đó npx hoạt động bình thường. Cần
subcommand chưa có script thì thêm vào `package.json` rồi gọi qua `npm run`.

**Render qua daemon OD bị giết ở 5 phút.** `apps/daemon/src/media/index.ts:3981`
đặt `HYPERFRAMES_RENDER_TIMEOUT_MS = 5*60*1000` và pin `--workers 1`. Video 45s
1080×1920 nền ảnh mất ~4.5 phút — sát trần. **Mặc định render trực tiếp bằng
`npm run render`**: không giới hạn thời gian, tự dùng 5 worker.

## 3. Vị trí file trong Open Design

```
~/open-design/.od/projects/<project-uuid>/         # thư mục dữ liệu daemon
├── <ten-video>.mp4                                # output — copy ra ngoài mà dùng
└── .hyperframes-cache/
    ├── .venv-tts/                                 # venv Kokoro dùng chung
    └── <ten-composition>/
        ├── index.html      # toàn bộ nội dung + timeline
        ├── hyperframes.json / meta.json / package.json
        ├── assets/         # ảnh, logo, wav
        └── vo-script/gen.py
```

Đừng sửa/xoá trực tiếp trong `.od/projects/` ngoài phạm vi composition — đó là
thư mục dữ liệu daemon. Output thì copy ra `~/Downloads`.

Tạo composition mới: **clone một composition đã chạy được** rồi viết lại
`index.html`. Nhanh hơn và an toàn hơn `hyperframes init` (giữ nguyên pin phiên
bản CLI, giữ scaffold hợp lệ). Nhớ đổi `id`/`name` trong `meta.json` và
`package.json`.

## 4. Luồng chuẩn

```
1. Khảo sát tài liệu nguồn (docx/Figma/ảnh) → rút nội dung thật, không bịa số liệu
2. Hỏi user 2 điều nếu chưa rõ: góc nội dung, và tỉ lệ khung (9:16 hay 16:9)
3. Clone scaffold → chuẩn bị assets vào assets/
4. Viết index.html theo hợp đồng ở mục 5
5. npm run check          ← BẮT BUỘC, sửa hết error trước khi render
6. npm run render         ← chạy nền, ~2-5 phút
7. Verify bằng frame thật + đo audio  ← BẮT BUỘC, xem mục 8
```

Bước 5 và 7 không được bỏ. `check` bắt lỗi kỹ thuật (overlap, contrast, audio câm),
nhưng **không bắt lỗi thẩm mỹ** — chữ mồ côi cuối dòng, chữ đè lên mặt người, logo
sai màu. Chỉ có nhìn frame thật mới thấy.

## 5. Hợp đồng composition — tối thiểu phải đúng

**Ba tầng bắt buộc:**

```html
<!-- 1. Root composition: đặt thẳng trong <body>, TUYỆT ĐỐI không bọc <template> -->
<div id="root" data-composition-id="main"
     data-start="0" data-duration="45" data-width="1080" data-height="1920">

  <!-- 2. Clip: mọi phần tử có timing cần class="clip" + 3 attribute -->
  <div id="s1" class="scene clip" data-start="0" data-duration="6" data-track-index="1">
    <div class="scene-inner"> ... </div>   <!-- xem mục quan trọng bên dưới -->
  </div>
</div>

<!-- 3. Timeline: paused, đăng ký theo đúng composition-id -->
<script>
  window.__timelines = window.__timelines || {};
  const tl = gsap.timeline({ paused: true });
  ...
  window.__timelines["main"] = tl;
</script>
```

| Attribute | Ý nghĩa |
|---|---|
| `data-start` | giây, hoặc tham chiếu clip khác (`"intro + 2"`) |
| `data-duration` | giây — **quyết định độ dài**, không phải độ dài GSAP timeline |
| `data-track-index` | số nguyên; **cùng track không được chồng thời gian**. KHÔNG phải z-index |

**Tách vỏ clip khỏi lớp nội dung.** Đây là lỗi kiến trúc dễ mắc nhất:

```css
.scene { position: absolute; inset: 0; }        /* clip — framework tự quản visibility */
.scene-inner { position: absolute; inset: 0; }  /* nội dung — GSAP fade ở đây */
```

```js
function scene(sel, inAt, outAt) {
  const inner = sel + " .scene-inner";
  tl.fromTo(inner, {opacity:0}, {opacity:1, duration:0.45, ease:"power2.out"}, inAt);
  if (outAt !== null) {
    tl.to(inner, {opacity:0, duration:0.45, ease:"power2.in"}, outAt);
    tl.set(inner, {opacity:0}, outAt + 0.45);   // hard kill — bắt buộc
  }
}
```

Fade `opacity` thẳng lên phần tử `class="clip"` là đang giành quyền với framework;
seek phi tuyến sẽ để lại trạng thái cũ. Lint chỉ bắt khi có clip khác bắt đầu đúng
mốc fade kết thúc — tức là lỗi tồn tại âm thầm cho tới khi bạn thêm audio.

**Luật bất di bất dịch** (vi phạm = render hỏng hoặc treo):

1. Deterministic tuyệt đối — cấm `Math.random()`, `Date.now()`, network fetch
2. Cấm `repeat: -1`. Tính hữu hạn bằng **`Math.floor`**, không phải `Math.ceil`
   (ceil làm tràn quá độ dài scene, lint báo `gsap_repeat_ceil_overshoot`)
3. Cấm dựng timeline trong `async`/`setTimeout`/Promise — engine đọc
   `window.__timelines` đồng bộ ngay sau page load
4. Chỉ animate thuộc tính thị giác; cấm `visibility`, `display`, cấm gọi
   `video.play()`/`audio.play()`
5. Không exit animation trừ scene cuối — transition chính là exit
6. Ảnh Ken Burns cần `data-layout-allow-overflow` (phóng to vượt khung là có chủ ý)
7. Không cần thẻ `<link>` Google Fonts — compiler tự resolve từ `font-family` và
   nhúng `@font-face` tất định. Để thẻ link vào chỉ tổ nhận warning

## 6. Lồng tiếng — Kokoro chạy local, 0 đồng

Model nằm sẵn ở `~/.cache/hyperframes/tts/`. **Nhưng `hyperframes tts` không chạy
được** vì hai lý do, và cả hai đã có cách chữa trong `templates/gen-vo.py`:

1. Nó gọi một python không có `kokoro_onnx` → dùng `.venv-tts/bin/python` của project
2. `libespeak-ng.so` trong wheel `espeakng_loader` là bản build `_dynamic` hardcode
   đường dẫn data về máy CI (`/home/runner/...`), bỏ qua mọi biến môi trường →
   ghép **lib hệ thống** với **data trong wheel**:

```python
os.environ.setdefault("PHONEMIZER_ESPEAK_LIBRARY", "/usr/lib/x86_64-linux-gnu/libespeak-ng.so.1")
os.environ.setdefault("PHONEMIZER_ESPEAK_DATA_PATH", str(espeakng_loader.get_data_path()))
```

Copy `templates/gen-vo.py` vào `vo-script/gen.py`, sửa dict lời thoại, chạy:
```bash
../.venv-tts/bin/python vo-script/gen.py    # in độ dài từng câu vs khung scene
```

**Giọng**: `af_heart` `af_nova` `af_sky` (nữ Mỹ), `am_adam` `am_michael` (nam Mỹ),
`bf_emma` `bf_isabella` (nữ Anh), `bm_george` (nam Anh), thêm vài giọng ES/FR/JA/ZH.

**Hai giới hạn cứng của Kokoro**: không clone giọng, và **không có tiếng Việt**
(chỉ en-us, en-gb, es, fr-fr, hi, it, pt-br, ja, zh). Cần tiếng Việt hoặc giọng
riêng thì phải đổi engine — xem `references/troubleshooting.md`.

**Chọn cấu trúc track theo việc có nhạc hay không:**

- **Chỉ có tiếng** → cắt từng câu thành file rời, mỗi câu một thẻ `<audio>` với
  `data-start` riêng. Dễ chỉnh từng câu.
- **Có cả nhạc** → ghép một track 45s liền mạch với offset nhúng sẵn. Bắt buộc,
  vì sidechain ducking cần một tín hiệu liên tục làm khoá.

## 7. Nhạc nền và ducking

HyperFrames **không có sidechain ducking**. Phải tiền xử lý bằng ffmpeg, kết quả là
một file nhạc đã trộn sẵn — tất định, render lại bao nhiêu lần cũng giống nhau.

```bash
# 1. Cắt + chuẩn hoá + fade hai đầu
ffmpeg -i nhac-goc.mp3 -t 45 \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=42.5:d=2.5,loudnorm=I=-16:TP=-1.5:LRA=11" \
  -ar 48000 -ac 2 -y assets/music.wav

# 2. Ducking — dùng track VO làm khoá điều khiển
ffmpeg -i assets/music.wav -i assets/vo.wav -filter_complex \
  "[1:a]aresample=48000,aformat=channel_layouts=stereo[key];
   [0:a][key]sidechaincompress=threshold=0.025:ratio=9:attack=25:release=450[d]" \
  -map "[d]" -ar 48000 -ac 2 -y assets/music-ducked.wav

# 3. Chuẩn hoá tiếng nói to hơn nhạc
ffmpeg -i assets/vo.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -ac 2 -y assets/vo-mix.wav
```

Gắn vào composition — **hai track index khác nhau** vì chúng chồng thời gian:

```html
<audio id="bgm" class="clip" src="assets/music-ducked.wav"
       data-start="0" data-duration="45" data-track-index="10" data-volume="1"></audio>
<audio id="vo" class="clip" src="assets/vo-mix.wav"
       data-start="0" data-duration="45" data-track-index="11" data-volume="1"></audio>
```

**`<audio>` thiếu `id` thì render ra CÂM** mà không báo lỗi lúc chạy. Chỉ `check`
mới bắt: *"the renderer requires id to discover media elements — this audio will be
SILENT in renders."*

Đổi lời thoại thì **phải chạy lại bước ducking**. Quên là nhạc sẽ chìm ở những chỗ
không còn tiếng nữa.

## 8. Verify — kỷ luật bắt buộc

"Lệnh chạy xong exit 0" không phải bằng chứng. Ba tầng kiểm:

**Kỹ thuật** — `npm run check` phải sạch 5 tầng: lint / runtime / layout / motion /
contrast. Không render khi còn error.

**Thị giác** — trích frame thật từ MP4, ghép contact sheet, nhìn:
```bash
for t in 3 10 17 25 33 41; do
  ffmpeg -loglevel error -ss $t -i out.mp4 -frames:v 1 -y /tmp/f_$t.png
done
```
Soi kỹ: chữ có mồ côi cuối dòng không, chữ có đè mặt người không, logo có đúng màu
trên nền không, khoảng trống có bất thường không.

**Âm thanh** — đừng tin `hasAudio:true`.
```bash
# có track không, đúng codec không
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels out.mp4

# tiếng nói có đúng chỗ không (khi KHÔNG có nhạc nền)
ffmpeg -i out.mp4 -af "silencedetect=noise=-45dB:d=0.6" -f null - 2>&1 | grep silence_

# khi CÓ nhạc nền, silencedetect vô dụng → so dải giọng 300-3400Hz
# giữa bản có tiếng và bản chỉ nhạc, ở cửa sổ có lời vs khoảng trống
ffmpeg -ss 1.5 -t 2.5 -i out.mp4 -af "highpass=f=300,lowpass=f=3400,volumedetect" -f null -

# kiểm ducking: nhạc phải lùi ~8dB khi có lời, nguyên mức khi im
ffmpeg -ss 1.5 -t 2.5 -i assets/music-ducked.wav -af volumedetect -f null -
```
Lưu ý: `volumedetect` in ra ở mức INFO — **đừng dùng `-v error`**, nó nuốt mất kết quả.

## 9. Đường qua daemon OD (khi nào dùng)

Mặc định render trực tiếp. Chỉ đi qua daemon khi cần agent trong OD tự dispatch và
stream progress vào chat:

```bash
"$OD_NODE_BIN" "$OD_BIN" media generate --project "$OD_PROJECT_ID" \
  --surface video --model hyperframes-html \
  --output ten.mp4 --composition-dir ".hyperframes-cache/<ten>"
# → trả 202 {taskId} ngay, KHÔNG chờ render xong
"$OD_NODE_BIN" "$OD_BIN" media wait <taskId>
# exit 0 = xong (stdout có {"file":{...}}) · exit 2 = còn chạy, gọi lại · exit 5 = lỗi
```

Nhớ trần 5 phút và `--workers 1` ở mục 2.

## 10. Số liệu tham chiếu

| | |
|---|---|
| 45s @1080×1920 30fps | 1350 frame |
| nền gradient, ít ảnh | ~107s render, MP4 ~8 MB |
| 8 ảnh full-bleed + backdrop blur | ~266s render, MP4 ~19 MB |
| worker | 5 (render trực tiếp) / 1 (qua daemon) |

## Tài liệu kèm theo

- `references/troubleshooting.md` — danh mục đầy đủ lỗi đã gặp, thông điệp lint
  thật và cách chữa. Đọc khi `check` báo lỗi hoặc render ra sai.
- `templates/gen-vo.py` — script sinh voiceover Kokoro đã xử lý sẵn bẫy espeak,
  tự cảnh báo câu nào dài quá khung scene.
