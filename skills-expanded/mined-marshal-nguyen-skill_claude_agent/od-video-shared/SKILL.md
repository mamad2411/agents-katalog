---
name: od-video-shared
description: Dựng video marketing bằng HyperFrames trong Open Design — render local trên máy mình, không tốn credit API, kèm lồng tiếng và nhạc nền có ducking. Dùng khi cần tạo reel, promo, explainer, video quảng cáo từ tài liệu/ảnh/Figma; khi sửa hoặc render lại một composition HyperFrames; hoặc khi thêm voiceover/nhạc vào video có sẵn. Chứa hướng dẫn cài đặt từ đầu và danh mục lỗi thường gặp.
---

# Dựng video trong Open Design bằng HyperFrames

> Skill này không giả định máy nào. Mọi đường dẫn đều có cách tự dò. Nếu bạn thấy
> một lệnh không chạy, tra `references/troubleshooting.md` trước khi tự chế cách khác.

## 1. Đây là gì và tại sao chọn nó

HyperFrames render một trang HTML/CSS/GSAP thành MP4 bằng Chrome headless + ffmpeg,
**chạy trên máy bạn, không gọi API, không tốn credit**. Trong Open Design nó là một
provider của media dispatcher, và là provider video **duy nhất không cần API key**:

```
apps/daemon/src/media/models.ts
{ id: 'hyperframes', integrated: true, credentialsRequired: false, settingsVisible: false }
```

Mọi renderer video khác (Volcengine Seedance, fal Veo/Sora, Grok, OpenRouter, MiniMax)
đều nhận `credentials: ProviderConfig` và ném lỗi nếu thiếu `apiKey`. HyperFrames là
renderer duy nhất không có tham số đó.

**Giới hạn phải nói trước với người đặt hàng.** HyperFrames không phải AI video.
Nó dựng motion graphics, kinetic typography, slideshow ảnh động, mock giao diện,
biểu đồ động — tức mọi thứ vẽ được bằng HTML/CSS. Nó **không** sinh được cảnh quay
thật, người thật, b-roll. Cần video AI cinematic thì phải dùng provider trả phí.
Nói rõ trước khi bắt tay, đừng để khách kỳ vọng sai.

## 2. Cài đặt một lần

### 2.1 Node ≥ 22

HyperFrames yêu cầu Node 22 trở lên. Kiểm tra:

```bash
node --version
```

Nếu thấp hơn, cài Node 22+ bằng cách bạn quen dùng (nvm / fnm / volta / installer
chính thức). Với nvm:

```bash
nvm install 24 && nvm use 24
```

Nhiều máy có Node cũ ở `PATH` mặc định trong khi bản mới nằm nơi khác. Trước mỗi
phiên làm việc hãy xác nhận lại `node --version` ngay trong shell đang dùng, đừng
tin vào lần cài trước.

### 2.2 ffmpeg

```bash
ffmpeg -version
```
Thiếu thì cài qua package manager (`apt install ffmpeg`, `brew install ffmpeg`, …).
Dùng cho chuẩn bị nhạc và kiểm chứng kết quả.

### 2.3 Lồng tiếng — chỉ cần khi có voiceover

Tạo một virtualenv riêng, **đừng cài vào python hệ thống**:

```bash
python3 -m venv .venv-tts
.venv-tts/bin/pip install kokoro-onnx soundfile numpy
```

Cần thêm thư viện `espeak-ng` của **hệ thống** (bản trong wheel python thường hỏng,
xem `references/troubleshooting.md` mục C):

```bash
sudo apt install espeak-ng        # Debian / Ubuntu
brew install espeak-ng            # macOS
```

Model Kokoro (~350 MB) tải một lần. Cách đơn giản nhất là chạy lệnh tts của
HyperFrames một lần — nó tải model về cache rồi mới báo lỗi phiên âm:

```bash
npx hyperframes tts "test" --output /tmp/t.wav      # tải model, có thể báo lỗi espeak
```

Sau đó `templates/gen-vo.py` sẽ tự tìm model trong cache. Script cũng in ra chỗ nó
tìm nếu không thấy, để bạn tải thủ công từ trang release của `kokoro-onnx`.

## 3. Thư mục làm việc

Composition sống trong thư mục dữ liệu của daemon Open Design. Tìm nó:

```bash
echo "${OD_DATA_DIR:-chưa đặt OD_DATA_DIR}"
```

Nếu chưa đặt, daemon dùng đường dẫn mặc định của bản cài đặt bạn đang chạy — mở
project trong giao diện OD rồi xem đường dẫn file hiển thị ở đó. Cấu trúc bên trong:

```
<thư-mục-project>/
├── <ten-video>.mp4              # output — copy ra ngoài mà dùng
└── .hyperframes-cache/
    ├── .venv-tts/               # venv Kokoro dùng chung cho các composition
    └── <ten-composition>/
        ├── index.html           # toàn bộ nội dung + timeline
        ├── hyperframes.json / meta.json / package.json
        ├── assets/              # ảnh, logo, wav
        └── vo-script/gen.py
```

Đừng sửa hay xoá trực tiếp trong thư mục dữ liệu daemon ngoài phạm vi composition
của mình. Output thì copy ra ngoài rồi dùng.

**Tạo composition mới**: nếu đã có một composition chạy được, **clone nó** rồi viết
lại `index.html` — nhanh và an toàn hơn (giữ nguyên pin phiên bản CLI, giữ scaffold
hợp lệ). Nhớ đổi `id`/`name` trong `meta.json` và `package.json`. Chưa có cái nào
thì:

```bash
npx hyperframes init "<đường-dẫn>" --example blank --skip-skills --non-interactive
```

## 4. Luồng chuẩn

```
1. Khảo sát tài liệu nguồn (docx/Figma/ảnh) → rút nội dung thật, không bịa số liệu
2. Hỏi người đặt hàng 2 điều nếu chưa rõ: góc nội dung, và tỉ lệ khung (9:16 hay 16:9)
3. Clone scaffold → chuẩn bị assets vào assets/
4. Viết index.html theo hợp đồng ở mục 5
5. npm run check          ← BẮT BUỘC, sửa hết error trước khi render
6. npm run render         ← chạy nền, vài phút
7. Verify bằng frame thật + đo audio  ← BẮT BUỘC, xem mục 8
```

Bước 5 và 7 không được bỏ. `check` bắt lỗi kỹ thuật (chồng chữ, tương phản dưới
chuẩn, audio câm), nhưng **không bắt lỗi thẩm mỹ** — chữ mồ côi cuối dòng, chữ đè
lên mặt người trong ảnh, logo sai màu trên nền. Chỉ nhìn frame thật mới thấy.

## 5. Hợp đồng composition — tối thiểu phải đúng

**Ba tầng bắt buộc:**

```html
<!-- 1. Root composition: đặt thẳng trong <body>, TUYỆT ĐỐI không bọc <template> -->
<div id="root" data-composition-id="main"
     data-start="0" data-duration="45" data-width="1080" data-height="1920">

  <!-- 2. Clip: mọi phần tử có timing cần class="clip" + 3 attribute -->
  <div id="s1" class="scene clip" data-start="0" data-duration="6" data-track-index="1">
    <div class="scene-inner"> ... </div>   <!-- xem phần quan trọng bên dưới -->
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
seek phi tuyến sẽ để lại trạng thái cũ. Lint **chỉ báo khi có clip khác bắt đầu đúng
mốc fade kết thúc** — nghĩa là composition chưa có audio vẫn dính lỗi này nhưng im
lặng. Làm đúng ngay từ đầu, đừng chờ lint nhắc.

**Luật bất di bất dịch** (vi phạm = render hỏng hoặc treo):

1. Deterministic tuyệt đối — cấm `Math.random()`, `Date.now()`, network fetch
2. Cấm `repeat: -1`. Tính hữu hạn bằng **`Math.floor`**, không phải `Math.ceil`
   (ceil làm tràn quá độ dài scene, lint báo `gsap_repeat_ceil_overshoot`)
3. Cấm dựng timeline trong `async`/`setTimeout`/Promise — engine đọc
   `window.__timelines` đồng bộ ngay sau page load
4. Chỉ animate thuộc tính thị giác; cấm `visibility`, `display`, cấm gọi
   `video.play()`/`audio.play()`
5. Không exit animation trừ scene cuối — transition chính là exit
6. Ảnh Ken Burns cần `data-layout-allow-overflow` (phóng vượt khung là có chủ ý)
7. Không cần thẻ `<link>` Google Fonts — compiler tự resolve từ `font-family` và
   nhúng `@font-face` tất định. Để thẻ link vào chỉ tổ nhận warning

## 6. Lồng tiếng

Copy `templates/gen-vo.py` vào `<composition>/vo-script/gen.py`, sửa `VOICE` và
`LINES`, rồi chạy bằng python của venv:

```bash
<đường-dẫn>/.venv-tts/bin/python vo-script/gen.py
```

Script in ra độ dài từng câu so với khung scene và **báo lỗi nếu câu nào tràn**.
Nó cũng tự dò thư viện espeak-ng của hệ thống nên không phụ thuộc máy cụ thể.

**Giọng Kokoro**: `af_heart` `af_nova` `af_sky` (nữ Mỹ), `am_adam` `am_michael`
(nam Mỹ), `bf_emma` `bf_isabella` (nữ Anh), `bm_george` (nam Anh), thêm vài giọng
ES/FR/JA/ZH.

**Hai giới hạn cứng**: Kokoro **không clone giọng** và **không có tiếng Việt**
(chỉ en-us, en-gb, es, fr-fr, hi, it, pt-br, ja, zh). Cần tiếng Việt hoặc giọng
riêng thì xem bảng lựa chọn trong `references/troubleshooting.md` mục C.

**Chọn cấu trúc track theo việc có nhạc hay không:**

- **Chỉ có tiếng** → cắt từng câu thành file rời, mỗi câu một thẻ `<audio>` với
  `data-start` riêng. Dễ chỉnh từng câu về sau.
- **Có cả nhạc** → ghép một track liền mạch với offset nhúng sẵn. Bắt buộc, vì
  sidechain ducking cần một tín hiệu liên tục làm khoá điều khiển.

Đặt `SINGLE_TRACK` trong script theo lựa chọn trên.

## 7. Nhạc nền và ducking

HyperFrames **không có sidechain ducking**. Phải tiền xử lý bằng ffmpeg, kết quả là
một file nhạc đã trộn sẵn — tất định, render lại bao nhiêu lần cũng giống nhau.

```bash
# 1. Cắt về đúng độ dài video + chuẩn hoá + fade hai đầu
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

**`<audio>` thiếu `id` thì render ra CÂM** mà không báo lỗi lúc chạy — lệnh vẫn
exit 0. Chỉ `check` mới bắt: *"the renderer requires id to discover media elements —
this audio will be SILENT in renders."*

Đổi lời thoại thì **phải chạy lại bước ducking**. Quên là nhạc sẽ chìm ở những chỗ
không còn tiếng nữa.

**Bản quyền**: bạn tự chịu trách nhiệm về quyền sử dụng nhạc. Video chạy quảng cáo
trên nền tảng lớn mà nhạc không có quyền thương mại sẽ bị gỡ tiếng hoặc chặn.

## 8. Verify — kỷ luật bắt buộc

"Lệnh chạy xong exit 0" không phải bằng chứng. Ba tầng kiểm:

**Kỹ thuật** — `npm run check` phải sạch 5 tầng: lint / runtime / layout / motion /
contrast. Không render khi còn error.

**Thị giác** — trích frame thật từ MP4 rồi nhìn:
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

# khi CÓ nhạc nền, silencedetect vô dụng vì nhạc chạy liên tục → lọc dải giọng
# 300-3400Hz rồi so bản có tiếng với bản chỉ nhạc, ở cửa sổ có lời và cửa sổ trống
ffmpeg -ss 1.5 -t 2.5 -i out.mp4 -af "highpass=f=300,lowpass=f=3400,volumedetect" -f null -

# kiểm ducking: nhạc phải lùi ~8dB khi có lời, nguyên mức khi im
ffmpeg -ss 1.5 -t 2.5 -i assets/music-ducked.wav -af volumedetect -f null -
```
Lưu ý: `volumedetect` in kết quả ở mức INFO — **đừng dùng `-v error`**, nó nuốt mất.

## 9. Hai đường render

**Trực tiếp (mặc định).** Không giới hạn thời gian, tự dùng nhiều worker:

```bash
npm run render -- --output <đường-dẫn>.mp4
```

**Qua daemon Open Design.** Dùng khi cần agent trong OD tự dispatch và stream tiến
độ vào khung chat:

```bash
"$OD_NODE_BIN" "$OD_BIN" media generate --project "$OD_PROJECT_ID" \
  --surface video --model hyperframes-html \
  --output ten.mp4 --composition-dir ".hyperframes-cache/<ten>"
# → trả 202 {taskId} ngay, KHÔNG chờ render xong
"$OD_NODE_BIN" "$OD_BIN" media wait <taskId>
# exit 0 = xong (stdout có {"file":{...}}) · exit 2 = còn chạy, gọi lại · exit 5 = lỗi
```

Đường daemon có **trần thời gian 5 phút** và pin `--workers 1` (xem
`HYPERFRAMES_RENDER_TIMEOUT_MS` trong `apps/daemon/src/media/index.ts`). Video nặng
sẽ bị giết giữa chừng. Lý do OD ép render trong daemon: trên macOS, Bash tool của
một số agent CLI bị bọc `sandbox-exec` làm Chrome của puppeteer treo khi chụp frame;
tiến trình daemon không bị sandbox. Trên Linux thường không cần, cứ render trực tiếp.

## 10. Ước lượng thời gian render

Phụ thuộc số nhân CPU và độ phức tạp composition. Con số dưới đây là mốc tham chiếu
đo trên CPU desktop tầm trung không dùng GPU rời — dùng để ước lượng bậc độ lớn,
không phải cam kết. Máy nhiều nhân hơn sẽ nhanh gần như tuyến tính:

| | |
|---|---|
| 45s @1080×1920 30fps | 1350 frame |
| nền gradient, ít ảnh | ~2 phút, MP4 ~8 MB |
| 8 ảnh full-bleed + backdrop blur | ~4,5 phút, MP4 ~19 MB |

Mỗi worker là một tiến trình Chrome (~256 MB RAM). Máy yếu thì giảm `--workers`.

## Tài liệu kèm theo

- `references/troubleshooting.md` — danh mục lỗi tra theo triệu chứng, kèm thông
  điệp lint nguyên văn. Đọc khi `check` báo lỗi hoặc render ra sai.
- `templates/gen-vo.py` — script sinh voiceover Kokoro, tự dò thư viện espeak của
  hệ thống, tự cảnh báo câu nào dài quá khung scene.
