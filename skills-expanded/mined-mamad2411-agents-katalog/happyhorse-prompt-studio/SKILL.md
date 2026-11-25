---
name: happyhorse-prompt-studio
description: Interactive prompt studio for HappyHorse 1.0 video generation. Guides users through scenario discovery with vivid examples, then assembles production-ready prompts in JP/CN/EN. Use when someone wants to create AI video content with HappyHorse but doesn't know where to start, or when they have a specific scenario and need a polished prompt. Covers manga drama, character PV, manga motion, virtual idol MV, and free-form scenarios.
---

# HappyHorse Prompt Studio

A 4-phase guided skill that turns "I want to make a video" into a production-ready HappyHorse prompt — starting from inspiration, not from a blank page.

## Overview

This skill guides the Agent through a structured conversation:

```
Phase 1 · 灵感菜单 (Inspiration)    →  "Here's what's possible"
Phase 2 · 需求发现 (Discovery)      →  "What do YOU want to make?"
Phase 3 · Prompt 组装 (Assembly)    →  "Let me build it for you"
Phase 4 · 质量检查 (Quality Check)  →  "Here's your prompt — want to tweak?"
```

## Phase 1 · Inspiration Menu (灵感菜单)

**Start every conversation here.** Before asking any questions, show the user what HappyHorse can do. Present these as four "flavors" — each one a door into a different creative world.

Use the language the user is using (JP/CN/EN). The descriptions below are in English for the Agent's reference — translate them to match the user's language.

---

### Flavor A · "让你的角色开口说话"
**Voiced Manga Drama (漫画配音剧 / ボイスコミック)**

> You have a manga, a webtoon, or an original story. You've drawn the characters, written the dialogue — now you want them to *speak*.
>
> Upload 2-3 character reference images + a short script. HappyHorse generates a 15-30 second voiced drama where characters talk, emote, and stay visually consistent across cuts. Lip-sync included.
>
> **Vibe:** Movie dub meets manga animation. Your characters, their voices.

### Flavor B · "一张立绘，开口自我介绍"
**Character Voice PV (角色语音 PV / キャラボイス PV)**

> You have a game character, a VTuber, or an original OC. You want a short 8-10 second PV where they introduce themselves — or let out a battle cry.
>
> Upload 1-3 character art images + a line or two. HappyHorse generates a voiced, lip-synced character PV.
>
> **Vibe:** Character reveal trailer. One illustration, one voice, one PV.

### Flavor C · "让一格漫画活过来"
**Manga Panel Motion (漫画分格动态化 / コマ動画化)**

> You have manga panels, comic pages, or illustrated scenes. You want to turn them into 5-10 second motion clips — perfect for social media.
>
> Upload one panel as the first frame. HappyHorse animates it while preserving your art style.
>
> **Vibe:** Your drawing, but it breathes. Hair moves, eyes blink, wind blows.

### Flavor D · "你的虚拟偶像，30 秒成 MV"
**Virtual Idol MV (虚拟偶像 MV / バーチャルアイドル MV)**

> You have a virtual idol, a VTuber group, or an original idol project. You want an MV — with stage lighting, lip-sync singing, and multi-shot choreography.
>
> Upload 3-5 multi-angle character images + a licensed song segment. HappyHorse generates a 30-second MV clip.
>
> **Vibe:** Your idol, center stage. No Live2D. No MMD. Just one prompt.
>
> ⚠️ **Note:** This scenario requires the strongest compliance guardrails. We'll check together.

---

### How to present the menu

Present the four flavors conversationally, not as a dry list. Something like:

> "HappyHorse can bring your characters to life in a few different ways. Think of it as four flavors:
>
> A · **Voiced Drama** — your manga characters talk to each other, with voice and lip-sync
> B · **Character PV** — your game character or OC introduces itself out loud
> C · **Panel Motion** — a single manga panel starts moving, hair blowing, eyes blinking
> D · **Idol MV** — your virtual idol performs a 30-second MV on stage
>
> Which one sounds closest to what you're imagining? Or tell me about your project and I'll suggest."

If the user already knows what they want, skip to Phase 2.

---

## Phase 2 · Discovery (需求发现)

Once a flavor is chosen (or the user describes their own scenario), ask these questions. **Ask them conversationally, not as a form.** Group related questions together.

### 2.1 Character & World (角色与世界)

- What's your character's name and role? (protagonist / antagonist / side character)
- What do they look like? (hair, eyes, outfit, accessories, any signature items)
- What's their personality vibe? (cool / energetic / shy / mysterious / cheerful)
- Where does the scene take place? (school rooftop / fantasy castle / neon city / café / etc.)

### 2.2 Scene Intent (场景意图)

- What's happening in this scene? (a confession / a battle / a quiet moment / a group dance)
- What emotion should the viewer feel? (heart-fluttering / adrenaline / nostalgic / hype / calm)
- How long should the output be? (5s / 10s / 15s / 30s)

### 2.3 Voice & Sound (声音与音频)

- Does your character speak? If yes:
  - What language? (Japanese / Chinese / English)
  - Voice type? (young woman / young man / child / mature / elderly)
  - Voice color? (bright / low / soft / powerful / cool)
  - What do they say? (provide the exact line, or ask me to suggest)
- Background audio? (silence / ambient sounds / BGM style)

### 2.4 Visual Style (视觉风格)

- Art style reference? (anime / photorealistic / Pixar / watercolor / pixel art / etc.)
- Color palette? (warm / cool / neon / pastel / high-contrast)
- Camera preference? (close-up / medium / wide / rotating / slow push / static)

### 2.5 Compliance Quick-Check (合规快检)

Before proceeding, verify:

- ☐ Is the character **your own original creation** or properly licensed?
- ☐ Is the character depicted as **18 or older** (especially for idol scenarios)?
- ☐ Is the outfit **SFW** (no suggestive or revealing clothing)?
- ☐ Is the scene **SFW** (no sensitive locations like bedrooms/pools)?
- ☐ If there's music, is it **licensed or original** (not a commercial song)?

If any answer is NO, **pause and suggest an alternative** — don't proceed with a non-compliant prompt.

---

## Phase 3 · Prompt Assembly (Prompt 组装)

Now build the prompt using the **HappyHorse Formula**:

```
场景 (Scene) + 主体 (Subject) + 動き (Motion) + 音声 (Audio) + 品質修飾 (Quality)
```

### 3.1 The Formula (公式)

| Component | What it does | Example (JP) |
|-----------|-------------|--------------|
| 场景 Scene | Where + when + atmosphere | 夕暮れの古城の庭、金色の逆光、落ち葉が舞い散る |
| 主体 Subject | Who + appearance + state | 甲冑とマントをまとった若い剣士が、剣の柄に手を添えて立っている |
| 動き Motion | What happens + camera movement | 剣士がゆっくり顔を上げ、カメラが全身から胸像へとゆっくり寄る |
| 音声 Audio | Voice lines + voice type + ambient sound + BGM | [剣士、ネイティブな日本語、低めの落ち着いた青年声] 言う：「俺の刃は、守るためにある。」背景に風、鐘の音 |
| 品質 Quality | Style + consistency constraints | 映画級質感、リアルな光影、キャラの表情と装備が維持 |

### 3.2 R2V Character Consistency Syntax

When the user provides multiple reference images, use this syntax:

```
参考「Image 1」=[正面立绘]、「Image 2」=[侧面]、「Image 3」=[表情差分]
```

Or when referencing a specific character in a multi-character scene:

```
@「Image 1」のキャラが [action]、@「Image 2」のキャラが [reaction]
```

Key rules:
- Always use `@「Image n」` to lock character identity across shots
- Describe what each reference image shows (正面 / 側面 / 表情差分)
- End with: `キャラの顔・髪・衣装が変わらない` (character's face/hair/outfit stays unchanged)

### 3.3 Video-Edit Style Unification

When the user wants to unify style across multiple shots:

```
参考「Image 1」の画風・筆致・色調に、動画全体のスタイルを変換。
人物の動作、表情、運鏡、セリフのタイミングは 100% 保持。
```

Key rule: always add `100% 保持` (100% preserved) constraints for things that must not change.

### 3.4 Language Rules

| Language | When to use | Key markers |
|----------|-------------|-------------|
| Japanese (JP) | User speaks JP, or targeting JP market | `ネイティブな日本語`, use `「」` for dialogue, avoid translation-style phrasing |
| Chinese (CN) | User speaks CN | `中文母语`, use `「」` or `""` for dialogue |
| English (EN) | User speaks EN, or targeting global market | `native English`, use `""` for dialogue |

**Japanese-specific tips:**
- Use `ネイティブな日本語` to ensure natural Japanese (not translation-style)
- Specify voice color with JP adjectives: `明るく元気な少女声`, `低めの落ち着いた青年声`, `柔らかい囁くような声`
- Keep dialogue in `「」` brackets
- Avoid mixing languages in dialogue unless intentionally bilingual

### 3.5 Prompt Templates by Flavor

#### Flavor A · Voiced Manga Drama

```
[场景描述：时间/地点/光线/氛围]

[角色A描述] と [角色B描述] が [位置关系]。

[角色A动作描述]。
[角色A, 语言, 声色描述, 情绪] 言う：「[台词]」

[角色B反应动作]。
[角色B, 语言, 声色描述, 情绪] 答える：「[台词]」

[镜头运动描述]。
[环境音/BGM描述]。

映画級質感、リアルな光影、キャラの顔・髪・衣装が変わらない。
```

#### Flavor B · Character Voice PV

```
[场景描述：地点/光线/氛围]

[角色外观描述] が [姿态]。

[角色动作 + 镜头运动]。
[角色, 语言, 声色描述, 情绪] 言う：「[台词]」

[环境音/BGM描述]。

映画級質感、キャラの顔・髪・衣装・装備が変わらない。
```

#### Flavor C · Manga Panel Motion

```
[图片中已有内容，无需重复描述]

[角色简短动作：眨眼/头发飘动/微笑/转头]。
[环境动态：风吹/光斑/落叶/雨滴]。
[镜头运动：缓慢推近/横移/拉远/固定]。

[环境音/BGM描述]。

原画風、キャラの顔・髪・衣装・構図・色調が変わらない。
```

#### Flavor D · Virtual Idol MV

```
参考「Image 1」=[正面]、「Image 2」=[侧面]、「Image 3」=[表情差分]
中的虚拟偶像角色形象。

[舞台场景描述]
[灯光描述]

分镜 1（N 秒）：[景别]，角色 [姿态/动作]。
[角色, 语言, 声色, 情绪] 歌う：「[歌词]」

分镜 2（N 秒）：[景别]，角色 [舞蹈动作]。
[歌词]

分镜 3（N 秒）：[景别]，角色 [表情]。
[歌词]

[J-POP MV 美学 / 电影级光影]，キャラの顔・髪・衣装が変わらない。
口型与歌词重音精准匹配。
```

### 3.6 Assembling the Output

Present the final prompt in a code block so the user can copy it directly. Include:

1. **The prompt itself** (in the user's language)
2. **A brief breakdown** of what each part does
3. **Suggested model variant** (t2v / i2v / r2v / video-edit)
4. **Estimated cost** (720P: ¥0.9/sec, 1080P: ¥1.6/sec)

Example output format:

```
Here's your prompt — ready to paste into HappyHorse:

```
[PROMPT HERE]
```

**Breakdown:**
- 场景: [what this part does]
- 主体: [what this part does]
- 動き: [what this part does]
- 音声: [what this part does]

**Model:** happyhorse-1.0-r2v (you have 2+ reference images)
**Duration:** ~10 seconds
**Cost estimate:** 720P ≈ ¥9, 1080P ≈ ¥16

Want me to adjust anything? (voice tone, camera angle, add another character, change the line?)
```

---

## Phase 4 · Quality Check (质量检查)

Before finalizing, run through this checklist silently. If anything fails, fix before presenting.

### 4.1 Prompt Quality

- ☐ Does the prompt follow the Scene + Subject + Motion + Audio + Quality structure?
- ☐ Is the camera movement explicitly stated? (not left to chance)
- ☐ Is the voice type described with specific adjectives? (not vague)
- ☐ Is the dialogue in the correct brackets for the language? (「」 for JP, "" for EN)
- ☐ Is the "stays unchanged" constraint included at the end?
- ☐ Is the prompt length between 150-300 characters? (too short = under-specified; too long = hard to control)

### 4.2 Compliance Check

- ☐ No existing anime/manga/game IP referenced?
- ☐ No real person likeness?
- ☐ Character depicted as adult?
- ☐ Outfit is SFW?
- ☐ Scene location is SFW?
- ☐ If music is involved, it's licensed/original?

### 4.3 Optimization Tips

If the prompt looks good, offer these pro-tips:

- **"Try 3 variants"** — HappyHorse results vary; generating 3-5 and picking the best is standard practice
- **"Start 720P, finish 1080P"** — do test runs at 720P (cheaper), then re-generate the winner at 1080P
- **"Shorter lines = better lip-sync"** — if the voice line is over 15 characters, consider splitting into two shots
- **"Specific beats vague"** — "camera slowly pushes from full-body to chest close-up" beats "camera moves"

---

## Free-Form Mode (自由模式)

If the user's scenario doesn't fit Flavors A-D, use the formula directly:

1. Ask: "What's your scene? Describe it like you're telling a friend about a movie you just watched."
2. Extract: scene, subject, motion, audio, quality from their description
3. Assemble using the formula
4. Apply the quality check

This mode is especially useful for:
- Product advertisements
- Educational explainers
- Abstract / artistic videos
- Non-character-driven content

---

## Common Pitfalls (常见问题)

| Problem | Fix |
|---------|-----|
| Character face drifts across shots | Add more reference images + emphasize "顔・髪・衣装が変わらない" |
| Voice sounds like machine translation | Add "ネイティブな日本語" marker; avoid translation-style phrasing |
| Lip-sync is off | Shorten dialogue to ≤15 characters; split into two shots |
| Motion is stiff | Replace generic "動いている" with specific actions: "髪が風に右へ流れる" |
| Camera wanders | Always specify camera: "固定", "ゆっくり寄る", "横にパン" |
| Style drifts from original art | Add "原画風・色調が変わらない" at the end |
| Multiple characters swap positions | Use `@「Image n」` syntax to lock each character's position |
| Q-version character becomes realistic | Add "デフォルメ / ちびキャラ / Q 版" style keyword |

---

## CLI Quick-Start (for users who want to run it immediately)

If the user has `bailian-cli` installed, they can run the prompt directly:

```bash
# Text-to-video (no input image)
bl video generate --prompt "[PROMPT]" --download output.mp4

# Image-to-video (one input image)
bl video generate --image ./char.png --prompt "[PROMPT]" --download output.mp4

# Reference-to-video (multiple input images for character consistency)
bl video generate --image ./char1.png --image ./char2.png --prompt "[PROMPT]" --download output.mp4

# Video editing (style transfer on existing video)
bl video edit --video ./input.mp4 --image ./style-ref.png --prompt "[PROMPT]" --download output.mp4
```

---

## Example Interactions

### Example 1 · First-time user (flavor A)

```
User: "I have a manga character I want to animate. She's a schoolgirl with pink hair, and I want her to say something cute."

Agent: "That sounds like Flavor B — a Character Voice PV! Let me ask a few things:

1. What's her name and personality? (shy? cheerful? cool?)
2. What's she saying? Got a line in mind, or want me to suggest one?
3. Where is she? (school rooftop? cherry blossom park? classroom?)
4. Voice vibe — bright and cute, or soft and shy?

And quick compliance check: is she your own original character?"

User: "Her name is Sakura, she's super cheerful, she's on a school rooftop at lunch. She says 'Hey! You made it!' in Japanese. Bright voice!"

Agent: [assembles prompt using Flavor B template]

"Here's your prompt:

```
昼休みの学校の屋上、青空と白い雲、風が心地よい。
桜色のロングヘアの少女がフェンスに寄りかかり、こちらを見て笑っている。

少女が手を振り、カメラがゆっくり寄る。
[少女、ネイティブな日本語、明るく元気な若い女性声、嬉しそう] 言う：
「ねえ！来てくれたんだ！」

背景に風の音、遠くで校庭のざわめき、明るいピアノの BGM。
映画級質感、キャラの顔・髪・制服が変わらない。
```

Model: happyhorse-1.0-i2v (one image input)
Duration: ~8 seconds
Cost: 720P ≈ ¥7.2, 1080P ≈ ¥12.8

Want to tweak anything?"
```

### Example 2 · Experienced user (free-form)

```
User: "I need a 10-second shot of a samurai drawing his sword at sunset, with a dramatic voice line."

Agent: "Got it — free-form, single character. Quick questions:

1. What does he say? (Japanese line?)
2. Voice type — deep and gravelly?
3. Camera — slow push to close-up? Or wide shot?
4. Art style — realistic? Anime?

Compliance: original character?"
```

---

## Final Notes for the Agent

- **Always start with Phase 1** unless the user is clearly experienced and already knows what they want
- **Be creative with descriptions** — don't just ask "what's the scene?", say "paint the picture for me — where are we, what time of day, what's the vibe?"
- **Suggest, don't just ask** — if the user seems unsure, offer defaults: "How about a sunset rooftop scene with a gentle breeze?"
- **Show the prompt in a code block** so it's easy to copy
- **Always offer to iterate** — "Want me to adjust the voice tone? Change the camera angle? Add a second character?"
- **Keep compliance friendly, not scary** — "Just to make sure everything's smooth, is this your original character?" not "COMPLIANCE CHECK: CONFIRM IP STATUS"
