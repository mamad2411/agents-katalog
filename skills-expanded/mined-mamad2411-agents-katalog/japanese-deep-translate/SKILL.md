---
name: japanese-deep-translate
description: 'Use this skill whenever the user provides Japanese text (song lyrics, articles, dialogue, anime/drama lines, tweets, messages, textbook sentences) OR names a Japanese song and wants to study it. Generates an HTML study page with a per-sentence 5-row alignment table (原文 / 假名 / 罗马音 / 拆解 / 翻译), a ▶ 跟读 button (edge-tts), and when the input is a song, also fetches the original MP3 + LRC timestamps from tonzhon.com so the page has a top player that auto-highlights the currently playing sentence plus a 🎵 原曲 button per sentence that jumps to that timestamp. Use PROACTIVELY whenever the user pastes Japanese content and shows any learning intent — even if they do not say the word "skill". Trigger phrases include "拆解这段日语", "帮我学这首歌", "学一下 <歌手> 的 <歌名>", "这句日语什么意思", "翻译这段", "逐词讲一下", or simply pasting Japanese text and asking a question about it.'
---

# Japanese Deep Translate

Build a sentence-by-sentence Japanese study page that a Chinese-speaking learner can read AND listen to. For songs, the page syncs with the original audio.

## Two entry modes

**Mode A — song by name.** User says "拆解 YOASOBI 群青" or similar. Use `scripts/fetch_song.py` to auto-fetch LRC lyrics + original MP3, which gives you a timestamped skeleton JSON. Then fill in the per-word breakdowns.

**Mode B — raw Japanese text.** User pastes any Japanese. Skip the fetcher; build the sentence list yourself. No original audio, no timestamps — just per-sentence tables + TTS.

## Output format — non-negotiable

For each Japanese sentence, produce a 5-row table. One word per column. Particles and sentence-final particles get their own columns — that is the whole point of this format.

| 原文 | word₁ | word₂ | … |
|---|---|---|---|
| **假名** | reading₁ | reading₂ | … |
| **罗马音** | romaji₁ | romaji₂ | … |
| **拆解** | meaning₁ | meaning₂ | … |
| **翻译** | full smooth Chinese translation of the whole sentence (spans all columns) |

### Row rules

- **原文**: the original Japanese unit. Kanji stays as kanji. Punctuation can be its own column or skipped.
- **假名**: hiragana/katakana reading of that unit. For units already in kana, repeat it.
- **罗马音**: Hepburn. `つ→tsu`, `し→shi`, `ち→chi`, `じ→ji`, `ん→n`, long vowels spelled out (`ou`, `ei`).
- **拆解**: ONLY the Chinese meaning of that unit. **No grammar labels.** Do not write "名词"/"动词连体形"/"主语助词"/"副词化助词". Just meaning or feel.
  - Particles: pick the closest Chinese connective/modal word:
    - が → 就 / 是 / 偏 · は → 嘛 / 呢 · を → 把 · に → 朝 / 向 / 对 / 在 · の → 的
    - で → 用 / 在 · と → 和 / 跟 / 〔引用〕 · へ → 向 / 往 · も → 也
    - から → 因为 / 从 · まで → 到
    - ね → 呢 · よ → 哦 / 呀 · さ → 嘛 / 啦 · か → 吗 · なあ → 啊 · ほら → 你看
  - Verbs: plain Chinese meaning. "出る" → "出来", not "自动词'出来'"。
  - Inflected forms: just translate meaning. "過ぎる（连体形修饰后）" → write "流逝（的）" or just "流逝".
  - **片假名外来语 ALWAYS show the source word.** When the unit is a katakana loanword, put the source word (usually English, sometimes French/German/etc.) in front of the Chinese meaning, in the form `"source → meaning"`. This lets the learner anchor the word to vocabulary they already know and catches cases where the Chinese gloss alone is misleading. Drop the source only when it's a genuinely Japanese-coined katakana word (和製語 like アニメ, カラオケ, サラリーマン — but even then, annotate `"和製 → …"` if the construction is non-obvious).
    - `ニュース` → `news → 新闻`
    - `サバンナ` → `savanna → 热带草原`
    - `シュール` → `surréaliste(法) → 超现实的`（不是"很酷"；用源词钉住原义）
    - `イメージ` → `image → 想象`
    - `ゴール` → `goal → 终点`
    - `コンビニ` → `convenience(store) → 便利店`（解释截短来源）
    - `カラオケ` → `和製：空 + orchestra → 卡拉OK`
  - This rule applies to the 拆解 column only. 假名 / 罗马音 stay as the katakana reading / its romaji.
- **翻译**: the full sentence in smooth, natural 简体中文. Emotional particles (啊/呢/嘛/呀) fine here.

### Optional 日本人思路 note

Add a note below the table ONLY when there is something a Chinese learner would actually miss — a自动词 quirk (「哈欠自己出来」), a fixed idiom, a cultural nuance, or a literal reading that misleads. **Skip the note when the sentence is straightforward.** Empty noise is worse than missing commentary.

## Splitting the input

Split into **grammatically complete thoughts**, not breath-points. A learner needs to see a finished idea in one table — translating half-sentences loses the nuance that makes learning worthwhile.

- For raw text: split by 。？！ or line breaks.
- For lyrics (Mode A): the LRC breaks lines at **musical phrasing**, not at sentence boundaries. So the fetcher's 76 LRC lines often correspond to ~40 real sentences. **Merge consecutive LRC lines into one sentence** whenever the syntax requires it:
  - Merge when the previous line ends with a dangling connector: a non-terminal particle (に / で / を / が / は / の / と / へ / も), a conjunction (けど / から / ので / し / って), a 連用中顿 form (～て / ～で / 連用形 without final), a 連体形 modifying the next line's noun (ような / 動詞-ru / 形容詞-i), or an incomplete expression (～ば、～ほど, 名詞 alone expecting a predicate).
  - **Also merge runs of short inner-monologue fragments** even when each fragment is grammatically complete. If 2–4 neighbouring LRC lines are each short (≤ 3 words) and share one emotional beat — e.g. 「つまらないな / でもそれでいい / そんなもんさ / これでいい」 or 「何枚でも / ほら何枚でも / 自信がないから描いてきたんだよ」 — they belong to the same thought and should share one study table. The test: if the translator has to repeat the subject or restate the context in every row, it's the same thought.
  - Keep independent only when the line ends on a terminal form **and** stands on its own semantically — e.g. a single long sentence with a clear subject/predicate like 「大丈夫行こうあとは楽しむだけだ」 or 「もう今はあの日の透明な僕じゃない」.
  - Keep the **first** merged line's `timestamp_ms` — that's when highlight should start.
  - The merged `raw` is the concatenation of the LRC texts; `words` is the concatenation of your per-line breakdowns. `translation` covers the whole merged thought in one smooth sentence.
- Within a sentence, one column per meaningful unit (word / particle / sentence-final particle). Don't over-fuse and don't under-split.

Why this matters: if you keep 76 LRC-line-length boxes, every other row is a half-thought like "怖くて仕方ないけど" whose only translation is "虽然害怕得不行" with no object, and the learner can't see the connection to "本当の自分に出会えた". Merging restores the sentence the songwriter actually wrote.

## Pipeline — Mode A (song)

1. Run the fetcher:
   ```bash
   <skill>/.venv/bin/python3 <skill>/scripts/fetch_song.py "<query>" <output_dir>
   ```
   - `<query>`: free-form search string, e.g. `"YOASOBI 群青"` or `"米津玄師 Lemon"`.
   - `<output_dir>`: **`<repo-root>/song/<slug>/`** (e.g. `/home/adam/japan_skill/song/qunqing/`). Don't write songs to `/tmp` — they get wiped on reboot, and we actively collect them under the project's `song/` folder as a growing library. Use a short kebab-case slug for the directory name (`qunqing`, `get-along`, `one-vision`).
   - Produces `skeleton.json` (with sentence list + `timestamp_ms` + `raw` text), `lyrics.lrc`, and (if available) `original.mp3`.

2. Read `skeleton.json`. **Do NOT fill it 1-to-1**. Apply the merge rules from "Splitting the input" to collapse the N LRC lines into ~(0.5·N) full-sentence study units, then write those directly to `input.json`:
   - For each merged group, emit **one** sentence object. Use the first LRC line's `id` and `timestamp_ms`. Concatenate its constituent lines' `raw` into one string. Build `words` as a single list covering the whole merged sentence (particles and all). Write `translation` as one smooth Chinese sentence covering the whole merged thought. Add `note` only when it pays rent.
   - A group of 1 (line already a complete sentence on its own) just becomes one sentence object unchanged.
   - Every LRC line from the skeleton must end up inside exactly one group — no drops, no duplicates.
   - Concretely: skip writing a merge-script. Look at the skeleton, decide the groups in your head (or in a scratch comment at the top of input.json), then produce input.json once with the merged sentence list.

3. Run the builder:
   ```bash
   <skill>/.venv/bin/python3 <skill>/scripts/build_study.py <output_dir>/input.json <output_dir>
   ```
   This writes `index.html` and generates per-sentence TTS MP3s (`s1.mp3`, `s2.mp3`, …) for sentences that have `words` filled. Pre-existing TTS MP3s are not regenerated (use `--overwrite-tts` to force).

4. Tell the user the path. On WSL they can open via `explorer.exe $(wslpath -w <path>)`.

## Pipeline — Mode B (raw text)

Skip step 1. Write `input.json` directly (no `timestamp_ms`, no `audio` block, or `audio.file = null`). Then run the builder. The page will omit the top player and the 🎵 原曲 buttons, only showing ▶ 跟读 per sentence.

## JSON schema

```json
{
  "title": "群青 · YOASOBI",
  "source": {
    "provider": "tonzhon.com / netease",
    "netease_id": "1472480890",
    "tonzhon_url": "https://tonzhon.com/?wd=...&source=netease"
  },
  "audio": {
    "file": "original.mp3",
    "source": "soundcloud"
  },
  "sentences": [
    {
      "id": "s2",
      "timestamp_ms": 3516,
      "raw": "過ぎる日々にあくびが出る",
      "words": [
        {"text": "過ぎる", "kana": "すぎる", "romaji": "sugiru", "meaning": "流逝（的）"},
        {"text": "日々",  "kana": "ひび",   "romaji": "hibi",   "meaning": "日子"},
        {"text": "に",    "kana": "に",    "romaji": "ni",     "meaning": "朝着"},
        {"text": "あくび","kana": "あくび","romaji": "akubi",  "meaning": "哈欠"},
        {"text": "が",    "kana": "が",    "romaji": "ga",     "meaning": "就"},
        {"text": "出る",  "kana": "でる",  "romaji": "deru",   "meaning": "出来"}
      ],
      "translation": "面对这样如常流逝的日子，忍不住就打起了哈欠。",
      "note": "「あくびが出る」——哈欠是自己出来的，人只是容器。别翻成「我打哈欠」。"
    }
  ]
}
```

- `audio.source` values: `"netease"` (outer URL worked), `"soundcloud"` / `"youtube"` (yt-dlp fallback), `"local"` (user-supplied file), `"none"` (no audio).
- `timestamp_ms`: when to highlight this sentence. Omit for prose / Mode B.
- `raw`: the original LRC line. Used as a rendering fallback if you haven't filled `words` yet.

## Audio source fallback (inside fetch_song.py)

1. **NetEase outer URL** — fastest. Works for most Chinese pop and some international tracks. Fails (302→/404) for version-restricted titles (most YOASOBI, Ado, Vaundy, etc).
2. **yt-dlp / SoundCloud** (`scsearch1:`) — works reliably without auth; has most Japanese chart music. Default fallback.
3. **yt-dlp / YouTube** (`ytsearch1:`) — often triggers "sign in to confirm you're not a bot" from headless environments. Tried last.
4. **None** — `skeleton.json.audio.source = "none"`. The page shows a fallback notice: "listen on tonzhon.com" link + instruction to drop a local MP3 as `original.mp3`.

If the user provides their own MP3, tell them to place it in the output dir as `original.mp3`, then edit `input.json` → `audio: {"file": "original.mp3", "source": "local"}` before running the builder.

## HTML page behavior

- Top player (only when audio present): plays `original.mp3`. As it plays, the current sentence block highlights (warm background + border). If the user isn't actively scrolling, the page scrolls to keep the active sentence centered.
- Per-sentence **🎵 原曲 M:SS** button: jumps the main player to that timestamp and plays. Cancels any active loop.
- Per-sentence **🔁 循环** button: loops the original-audio segment for that one sentence (from its `timestamp_ms` to the next sentence's `timestamp_ms`, or to the end of track for the last sentence). Click again on the same button to cancel. Clicking another 🔁 switches the loop target. This is the key drill for pronunciation practice — user hears the native performance repeatedly.
- Per-sentence **▶ 跟读** button: plays that sentence's edge-tts MP3 (slower, clearer — for shadowing drills). Pauses the main player while speaking. Does NOT cancel the loop (so when the user hits play again, the loop resumes).

## 五十音字源提示

生成页面自动在顶部挂一个可折叠的 **📖 五十音字源** 面板。数据源是
`references/pronoun.md`，一张 CSV（`行,平假名,罗马音,字源（汉字草书）,中古汉语拟音,
古中日发音演变对比说明`），每个假名给出它取自哪个汉字草书、该字的中古汉语拟音、以及
和现代日语音的演变差异。

对中文母语的学习者来说，这张表把一堆陌生符号重新钩回到"以"、"宇"、"知"、"奈"这些
认识的字上，学起来可以顺着字形记音。

- **不用在每句假名格子里再加 tooltip / 字形注释** —— 太噪。整站共享一张静态表就够。
- 要更新字源数据：编辑 `references/pronoun.md` 即可，构建脚本会原样读入并渲染。
- 有新字源、新考据想加（拗音、片假名偏旁）可以追加到 CSV 里，保持列顺序一致。

## TTS voice

Default `ja-JP-NanamiNeural` (natural female). Pass `--voice ja-JP-KeitaNeural` to `build_study.py` for male. Other edge-tts `ja-JP-*` voices work too.

## First-run / setup

The skill ships with a venv at `<skill>/.venv/` containing `edge-tts` and `yt-dlp`. If the venv is missing:
```bash
python3 -m venv <skill>/.venv
<skill>/.venv/bin/pip install edge-tts yt-dlp
```
Always invoke scripts via the venv's python (`<skill>/.venv/bin/python3`) — system Python on Debian/Ubuntu refuses to install packages (PEP 668).

## Worked example (Mode A)

User: "帮我学 YOASOBI 的群青"

```bash
<skill>/.venv/bin/python3 <skill>/scripts/fetch_song.py \
  "YOASOBI 群青" <repo-root>/song/qunqing
# → skeleton.json with 76 sentences (timestamped), original.mp3 (soundcloud)

# Fill `words`/`translation`/`note` per sentence → write input.json

<skill>/.venv/bin/python3 <skill>/scripts/build_study.py \
  <repo-root>/song/qunqing/input.json <repo-root>/song/qunqing
# → index.html + s1.mp3 ... s76.mp3
```

Report: "已生成 `<repo-root>/song/qunqing/index.html`。打开后，顶部原曲播放时，当前句会自动高亮，每句还能点 🎵 跳到该句 + ▶ 听慢读。"

## Quality guidelines

- **Cover EVERY line the fetcher produced.** When the user asks for a song, they want the whole song, not the first stanza. If the skeleton has 76 LRC lines, every one of them must end up inside some merged study unit — no silent drops. The "（未拆解）" fallback row exists only for debugging; a shipped page should never show it.
- **Merge LRC lines into full sentences.** The fetcher's LRC split follows musical phrasing, not grammar. A page with 76 half-thoughts is worse than a page with ~40 complete ones. See "Splitting the input" above for the merge rules. The merged sentence keeps the first LRC line's `timestamp_ms`, and the highlight behavior still works because the whole grammatical unit lights up together from that start-time onward.
- **Stay lean on grammar labels.** The user wants "就 / 流逝 / 像…地", not "主语助词 / 连体形 / 副词化".
- **Preserve particle visibility.** Never merge a particle into its neighboring word column.
- **Prefer a natural, slightly literary flow in the 翻译 row** — user is reading these for pleasure as much as drilling.
- **Only write 日本人思路 notes when they pay rent.** Auto-verb quirks, fixed phrases, misleading literal reads, honorifics, cultural context — yes. Basic grammar — no.
