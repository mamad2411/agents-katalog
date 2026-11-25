---
name: mrtkeyword
description: "Dựng video dọc 9:16 (TikTok, Reels, Shorts) tự động từ A đến Z từ MỘT video quay người nói hoặc MỘT file giọng đọc: nghe lời, cắt chỗ vấp và khoảng lặng, tự chọn hiệu ứng keyword cho từng câu (62 hiệu ứng có code), tự viết nội dung hiệu ứng, phụ đề, nhạc nền, âm thanh, ảnh bìa, render MP4. Dùng khi người dùng gọi /mrtkeyword hoặc $mrtkeyword, nói 'dựng video này', 'làm video từ video quay / file ghi âm', 'chèn hiệu ứng keyword', '/effects <tên>'. Không dùng để sửa video có sẵn hiệu ứng hay làm video ngang."
---

# MRT Keyword — đưa video hoặc âm thanh vào, ra video hoàn chỉnh

Skill này chạy trên **Claude Code** (gọi `/mrtkeyword`) và **Codex** (gọi `$mrtkeyword`); chỗ nào ghi "Agent" là trợ lý đang chạy skill. Trả lời bằng tiếng Việt. Người dùng chỉ cần đưa **một file**: video quay người nói (dọc hoặc ngang) hoặc âm thanh giọng đọc (mp3/wav/m4a). Nhạc nền, ảnh minh hoạ là tuỳ chọn.

**Mặc định chạy thẳng từ A đến Z, không hỏi gì**: tự đặt tên dự án, tự chọn keyword, tự viết nội dung hiệu ứng, tự kiểm ảnh tĩnh và sửa lỗi, render, giao file. Chỉ dừng lại gửi ảnh tĩnh để duyệt khi người dùng nói muốn xem trước ("cho tôi duyệt", "gửi ảnh trước"). Không có nhạc nền thì làm không nhạc; không có lời kêu gọi trong video thì CTA mời theo dõi kênh. Trong lúc chạy, báo tiến độ ngắn gọn sau mỗi bước.

```
SK  = <thư mục skill này>                     (thư mục chứa SKILL.md)
PY  = "$SK/tools/.venv/Scripts/python.exe"    (do CAI-DAT.bat tạo; chạy MỌI script bằng python này)
OUT = "%USERPROFILE%/Videos/Keyword FX"       (mỗi video một thư mục dự án; thành phẩm vào "$OUT/Thanh pham")
PRJ = "$OUT/<ten-video>"                      (tên kebab-case không dấu, tự đặt từ nội dung)
```

Nếu thiếu `$SK/tools/.venv` hoặc `$SK/template/node_modules`: báo người dùng chạy lại `CAI-DAT.bat` trong thư mục gói, không tự cài thứ khác.

**Chạy trên Codex**: mọi bước chạy được offline (mô hình và trình duyệt render đã tải sẵn khi cài). Nếu sandbox chặn ghi ra `%USERPROFILE%/Videos`, dùng `OUT = "<thư mục đang làm việc>/Keyword FX"` và báo người dùng đường dẫn; lệnh nào bị chặn thì xin người dùng duyệt chứ không tìm cách lách. Xem ảnh tĩnh ở bước 6 bằng công cụ xem ảnh của Codex.

## Quy trình

1. **Chuẩn bị đầu vào**: tạo `$PRJ`, chép file người dùng đưa vào `$PRJ/input/`, rồi
   `"$PY" "$SK/scripts/prep_input.py" "$PRJ/input/<file>" "$PRJ" --vocab "<tên riêng, thuật ngữ trong video>"`
   → nghe lời, cắt từ đệm / lặp / nói lại / khoảng lặng dài, chia đoạn 3,5–9 giây theo câu → `clips/01.mp4…` (video, đã đưa về 1080×1920) hoặc `voice/vo_01.wav…` (âm thanh), `work/asm/{master.wav, timeline.json, master/words.json, captions.json}`.
   Đọc `work/raw/edl_review.txt`: câu hỏng giữa chừng, đoạn nói lại cả ý, câu lạc đề → chạy lại với `--remove-words a-b`; chữ bị cắt nhầm → `--keep-words a-b` (giữ lần nói sau cùng của một ý). Không muốn cắt gì → `--no-cut`.
2. **Gợi ý keyword**: `"$PY" "$SK/scripts/suggest.py" "$PRJ"` → bảng "đoạn → keyword (điểm)" + `work/plan_draft.json`. Đoạn đầu = hook (chỉ sticker + punch-in), đoạn cuối = CTA (`cta-circle`; video chỉ có âm thanh thì `comment-pop`).
3. **Agent tự hoàn thiện kế hoạch** → `work/plan.json` (khuôn: `references/plan-example.json`):
   - Đọc lời từng đoạn (`work/asm/timeline.json`), đổi keyword gợi ý nếu chưa hợp ý câu. Luật: 6–10 keyword/phút, không lặp liền, với đoạn có người: ≥ 3 kiểu `layout` (full · half · cutout · circle), một kiểu không quá 2 đoạn liền, hiệu ứng nặng (cần tách người) xen hiệu ứng nhẹ.
   - **cues**: điền TỪ ĐƯỢC NÓI trong chính đoạn đó cho từng mốc (vd glass-graph `run` = từ "tăng"), hoặc `"+1.5"` (giây sau đầu đoạn). Cue phải khớp chữ **Whisper nghe được** trong `work/asm/master/words.json` — Whisper ghi sai chính tả thì cue theo chữ Whisper; sửa chính tả phụ đề bằng `fix` (regex → chữ đúng).
   - **params**: viết nội dung riêng của video theo đúng lời nói — số liệu thật trong câu, việc được liệt kê, bình luận hợp chủ đề, chữ con dấu… Không bịa số liệu không có trong lời. Tôn trọng giới hạn ký tự ghi trong `keywords.json`.
   - `stickers` (2–6 chữ, tô từ khoá bằng `*…*`) cho hook/CTA, `punch` cho hook, `cover` (ảnh bìa: label, line1, line2, tag, clip, at — video chỉ âm thanh thì `clip: null`), `compounds` (từ ghép không tách trong phụ đề), `music` (đường dẫn nhạc nền nếu người dùng đưa).
   - CTA: dùng đúng lời kêu gọi người dùng nói trong video (từ khoá comment, theo dõi kênh…).
4. **Nguyên liệu**: `"$PY" "$SK/scripts/prepare_assets.py" "$PRJ"` → dự án Remotion, clip, thumbnail, vị trí mặt, **tự tách người** cho đoạn cần, ảnh bìa, nhạc nền tự nhỏ lại khi có lời.
5. **Dữ liệu + âm thanh hiệu ứng**: `"$PY" "$SK/scripts/build_data.py" "$PRJ"` → `remotion/src/data.json` + `work/sfx_events.json` (sửa dòng "không thấy từ …" rồi chạy lại); rồi
   `"$PY" "$SK/scripts/sfx_plan.py" "$PRJ/work/sfx_events.json" --voice "$PRJ/remotion/public/master.wav" --words "$PRJ/work/asm/master/words.json" --sfx-dir "$PRJ/remotion/public/sfx" --out "$PRJ/remotion/src/sfx.json"` → hết cảnh báo ⚠ "quá dày" (bỏ bớt event trong `sfx_events.json` — làm SAU mỗi lần build_data vì build_data ghi đè file này).
6. **Kiểm ảnh tĩnh** (bắt buộc): trong `$PRJ/remotion`: `npx remotion bundle src/index.ts --out-dir=<tạm>/b` rồi `npx remotion still <tạm>/b Main f.png --frame=N --scale=0.4` — mỗi đoạn 1 khung lúc hiệu ứng đầy đủ nhất + ảnh bìa (frame 6); ghép lưới (ffmpeg hstack/vstack) và XEM: chữ tràn mép, đè mặt, đè phụ đề, thẻ chồng nhau. Sửa params/cues tới khi sạch (tự làm, không hỏi). Chỉ gửi lưới ảnh chờ duyệt khi người dùng đã yêu cầu xem trước.
7. **Render + kiểm + giao**: `npx remotion render src/index.ts Main out/<ten>.mp4 --codec=h264 --crf=18`; kiểm độ to cả bài ≈ -14 LUFS, đỉnh ≤ -1 dBFS (vượt thì `alimiter`); ảnh bìa `npx remotion still src/index.ts Thumb "$OUT/Thanh pham/<ten>_cover.png"`; chép mp4 vào `$OUT/Thanh pham/`. Gửi kèm **tiêu đề** (≤ 60 ký tự), **caption Facebook** (câu mở + 3–5 ý + lời kêu gọi + 3–5 hashtag) và **caption TikTok** (≤ 150 ký tự + 4–6 hashtag), ghi vào `$OUT/Thanh pham/<ten>_caption.md`.

## Thư viện

- `keywords.json` — 206 mục (169 hiệu ứng khác nhau + 37 tên trùng đã gộp, `status: merged`, `alias_of` = keyword gốc — dùng tên nào cũng được), mỗi mục: `effect`, `fits` (câu nói hợp), `status` (`built` = có code / `planned` = mới có mô tả), `layout`, `needs_matte`, `cues` (mốc cần + ý nghĩa), `params` (nội dung cần điền + giới hạn), `triggers`, `sfx`.
- `template/src/fx/library.tsx`, `library2.tsx`, `library3.tsx` — code 62 hiệu ứng; `fx/common.tsx` — phần dùng chung; `Main.tsx` — bộ dựng đọc `data.json`.
- Chỉ dùng keyword `built`. Câu hợp một keyword `planned` → chọn keyword built gần nhất và báo người dùng; họ muốn thì dựng thêm (mục dưới).

## Đoạn chỉ có âm thanh

- Đoạn `voice/` không có người: nền cam, các keyword dạng thẻ tự đặt giữa màn hình.
- KHÔNG dùng keyword bám mặt cho đoạn âm thanh: text-behind, locked-on, scribble, reel-orbit, edit-timeline, face-scan, neon-outline, stamp-hit, clone-crowd, spotlight, end-wall, cta-circle (suggest.py đã tự loại).
- Ảnh thật được nhắc tới (ảnh chụp bài đăng, sản phẩm…): người dùng đưa ảnh → đặt vào `$PRJ/img/`, dùng `photo-snap` với `"img": "img/<file>"` (photo-snap không có ảnh thì không dùng cho đoạn âm thanh).
- Đoạn đầu (hook) của video chỉ âm thanh: nền trống, nên LUÔN thêm 1–2 sticker câu hook to giữa màn hình (`"y": 700`).

## Thêm keyword mới

1. Viết component trong `template/src/fx/library3.tsx` theo khuôn `React.FC<FxProps>` (mốc bằng `cue(c, "ten", fallback)`, nội dung từ `p`, chữ to dùng `fitSize`, vị trí khối dùng `place`), thêm vào `FX3`.
2. Đổi mục đó trong `keywords.json` sang `"status": "built"` và điền `layout`, `needs_matte`, `cues`, `params`, `triggers`, `sfx`.
3. Kiểm ảnh tĩnh bằng một kế hoạch nhỏ trên dự án có sẵn trước khi dùng thật.

## Quy tắc

- Không chèn chữ lên mặt (thẻ, sticker tự tránh theo `faces.json`); vùng phụ đề y 1440–1560 chỉ cho phụ đề.
- Phong cách cố định: nền cam, chữ Montserrat Black trắng/vàng viền navy, phụ đề 2–4 chữ, nhạc nền nhỏ dưới lời.
- Không có card NVIDIA vẫn chạy được (nghe lời và tách người chạy bằng CPU, chậm hơn).
