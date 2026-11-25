---
name: anthropic-launch-video
description: >
  This skill should be used when the user (老板) asks for an Anthropic-style
  product launch / intro video, a Cowork-aesthetic Remotion piece, a Claude
  Code intro animation, or any "cream + coral + Fraunces serif + JetBrains
  Mono terminal" branded explainer. Trigger on phrases like "做个 launch
  video", "Anthropic 那种感觉", "复现 Cowork 的编排", "Claude 介绍片",
  "网页里能跑的产品动画", and similar. Also trigger when work involves
  studying a reference video to reproduce its editing logic in Remotion.
version: 0.3.0
---

# Anthropic-Style Launch Video Playbook

This is the playbook for producing a 20–40s product launch / intro video in
the Anthropic visual language using Remotion. It encodes both the **what**
(visual language, editing techniques) and the **how** (workflow, self-check
protocol, Boss's协作偏好) — built from one full reproduction of the Cowork
launch piece.

## Iron rules — read every time. No exceptions.

**Violating the letter of these rules is violating the spirit.** The rules
exist precisely because future-you, under time/sunk-cost/exhaustion
pressure, will reach for "spirit-compliance" arguments to skip the letter.
Don't. If you find yourself constructing a clever reason a rule doesn't
apply *this one time* — that is the rule applying. Stop and follow it.

The five iron rules of this skill:

1. **Confirm Player vs mp4 BEFORE writing any composition code.** Always.
2. **Validate which layer 老板 wants reproduced (surface style / editing
   logic / both) BEFORE writing any composition code.** Always.
3. **Reference-first workflow: 4fps frame extraction, ≥30 frames Read
   across ≥3 clusters, AskUserQuestion validation of identified small
   touches BEFORE writing TSX.** Every reference, every time.
4. **Self-check every render with ffmpeg key-frame extraction + Read,
   BEFORE telling 老板 it's ready.** Every render. No "it's just a small
   change" exception.
5. **Output-tier honesty: state what tier this skill ships at, in plain
   words, and re-state it if 老板 over-credits the result.** Initial
   statement AND every time praise drifts above the actual tier.

Each rule has a rationalization table further down. If you catch yourself
saying any line in the left column, the right column is the truth.

### Iron rule rationalization table — bookmark this

| If you find yourself thinking... | Iron rule | Truth |
| --- | --- | --- |
| "Launch videos are obviously mp4, asking is overhead" | #1 | Boss's reference samples are Claude-design web animations, not mp4. The "obvious" answer is the wrong one. Ask. |
| "I can swap mp4 → Player later, the composition code is the same" | #1 | The output decision changes scaffolding, dependencies, build target, and how you self-check. Swapping later is a rewrite. |
| "He'll tell me if he wanted Player" | #1 | He told you to *use this skill*. The skill says ask. He's already told you. |
| "He said '复现', doing both surface + editing logic is safer than picking wrong" | #2 | "Both" is what got you the layer-mismatch round-trip last time. "Safer" = "lazy". Ask. |
| "Asking 'which layer' feels patronizing" | #2 | Being patronizing once costs 5 seconds. Rebuilding the wrong layer costs 3 hours. |
| "10 frames covers the major beats, I'll skip dense extraction" | #3 | 10 frames at 1fps misses every cursor sub-path, ripple, and 2-frame letter type-in. Those *are* the small touches the skill exists to capture. |
| "I have a strong intuition about what 老板 wants, validation is overhead" | #3 | Last time intuition produced "abstract to style tokens" — exactly the wrong layer. Intuition is the problem the validation step solves. |
| "Studio preview already showed the polish, ffmpeg self-check is redundant" | #4 | Studio renders differently from `renderMedia` (timing, font subsetting, asset loading). The mp4 is what 老板 sees. Verify the mp4. |
| "I verified the polish in source code, the render is mechanical" | #4 | Source verification confirms intent. ffmpeg+Read confirms output. They are different checks. The lesson "claude-fleet d1df0922" exists because intent-only verification produced fake claims. |
| "He can scrub the mp4 himself — faster feedback loop" | #4 | His scrubbing time = 5–10 min round trip. Your self-check time = 30s. You optimized for your own convenience and called it his speed. |
| "It's just a small re-render, the diff is tiny" | #4 | Small diffs are exactly when off-by-one frame timings slip in unnoticed. Self-check scales with risk, not with diff size — and risk is constant. |
| "He's complimenting it, restating the tier kills the energy" | #5 | Letting praise stand above the actual tier is the *same lie* as overselling at the start, just delayed. He'll discover the gap later and trust drops further than if you'd corrected gently now. |
| "It IS pretty Anthropic-y at this point" | #5 | "Pretty Anthropic-y" is not a tier. State the actual tier (composition 70–80%, no broadcast compositing / VO / SFX). Use those exact words. |
| "The tier check was for first impressions; we're past that" | #5 | The tier doesn't change just because the conversation got longer. If anything, mid-project drift is when honesty matters most. |

If a rationalization you encounter isn't on this list, **add it**. A
rationalization that isn't named here is one that will succeed.

### Forbidden phrases — if you catch yourself typing these, stop

- "Looks good" / "looks great" — without ffmpeg self-check evidence
- "This should work" — without rendering and verifying
- "Anthropic-quality" / "broadcast-quality" — without explicit tier caveat
- "I'll confirm later" — for Player-vs-mp4 or layer-validation
- "Probably he means..." — for any ambiguous brief
- "It's basically the same as..." — when justifying skipping a step

Each of these phrases is a tell that you're about to skip an iron rule.
Replace with: a tool call (render + ffmpeg + Read) or an AskUserQuestion.

## Output tier reality check — say this BEFORE writing code (Iron rule #5)

YOU MUST state the tier explicitly to 老板 in your first reply on the
project, AND restate it any time praise drifts above the actual tier.
This is not a one-time disclaimer; it is an ongoing calibration duty.

The honest tier of what this skill produces, on first attempt with a single
day of polish:

- **Composition & pacing:** can match Anthropic's editing logic (trailing-word
  reveal, mouse-as-narrator, product-UI form transformation, agent
  spinner→check, live diff typing, brand-color outro). **70–80% of the way
  there.** Use that exact number.
- **Visual fidelity:** cream/coral/serif/grid surface looks correct. Subtle
  motion polish (ease curves, micro-delays, stagger) needs an iteration loop.
- **What this skill does NOT produce:** broadcast-grade compositing,
  hand-drawn illustrations, voiceover, sound design, real product screen
  recordings. Those are separate workstreams. Name these explicitly when
  stating the tier — vague disclaimers ("might need polish") fail.

**Required first-reply template** (adapt wording, keep the structure):

> 提前对齐天花板：这个 skill 走 Remotion 路线，第一轮能拿到的是
> **编排和视觉 70–80% 像 Anthropic**，cream/coral/serif/grid 那一层
> 直接到位；细节动效 (ease 曲线、微延迟、stagger) 需要迭代调。
> **不包含** 广播级合成、手绘插画、配音、音效、真实产品录屏 —
> 这些是另外的工作流。继续走？

不要把开源 Remotion 的天花板说得比实际高。Reference for this lesson:
`memory/feedback_dont_oversell_tool_ceilings.md`.

**Mid-project drift check:** every time 老板 says "wow / 牛 / Anthropic-quality
/ 比预期好" — pause and ask: did the tier actually shift, or am I letting
praise stand? If it didn't actually shift, gently restate ("谢老板，目前还
是 70–80% 的那个 tier — broadcast 级合成那条线没跨过去"). The cost of one
gentle restate is zero. The cost of letting trust inflate then crash is
the whole project relationship.

## Confirm output format BEFORE coding: Player vs. mp4 (Iron rule #1)

YOU MUST ask 老板 which output format before scaffolding any composition.
This applies to every project, every time, regardless of what nouns 老板
used. "做个视频" / "launch video" / "intro 片" / "动画" / "宣传片" all
require the question. There is no noun that pre-answers it.

老板的参考样板通常是 Claude design 那种网页内可交互动画，**不一定是
mp4 文件**。

- **`<Player>` (web-embeddable React component):** for in-page animations,
  marketing site hero, interactive product tours. Output is a React
  component, not a file. User can scrub / pause / loop in the browser.
- **`renderMedia` → mp4:** for shareable file (Twitter, Slack, deck embed,
  YouTube). Heavier asset.

Reference: `memory/user_remotion_player_first.md`.

**Required AskUserQuestion before any composition code is written:**

> 输出形态先对齐一下 — 这次想要的是：
>
> - **`<Player>` 网页组件** (能嵌进站点 / 可交互 / 可循环)，还是
> - **`renderMedia` 出 mp4 文件** (Twitter / Slack / deck 分享)？
>
> 这俩 scaffolding 不一样，先选定再开干。

**No exceptions. Specifically forbidden:**
- Don't scaffold mp4 first and "swap to Player later" — they have
  different deps (`@remotion/player` vs `@remotion/cli`), different build
  targets, different self-check protocols. Swapping is a rewrite.
- Don't infer from the noun. "Launch video" does not mean mp4. Ask.
- Don't skip the question because 老板 sounds confident / busy / in flow.
  The 5-second cost of asking is bounded; the cost of building wrong is not.

See iron rule rationalization table for the specific traps.

## Reference-first workflow (Iron rules #2 and #3)

The single most important lesson from the first reproduction attempt:

> **Don't abstract a reference video to style tokens.** Color/font/grid is
> the surface layer. The thing that makes Anthropic videos *feel* Anthropic
> is the **editing logic** — pacing, what gets emphasised, how UI morphs,
> how the cursor narrates. Extract that first. Style comes after.

Boss's verbatim correction: "我要你复现的，是整个编排、设计、细节小心思，
不是抄 style." This is iron rule #2: **validate which layer 老板 wants
reproduced before writing TSX.** Iron rule #3 then governs *how* you study
the reference: 4fps minimum extraction, ≥30 frames Read across ≥3 clusters,
AskUserQuestion validation of identified small touches BEFORE writing TSX.

**Specifically forbidden:**

- "I have an intuition for the editing logic, skip Step 4" — your intuition
  produced the layer mismatch last time. Skip the step → repeat the mistake.
- "10 frames is enough" — 10 frames at 1fps misses every cursor sub-path,
  every ripple, every 2-frame letter type-in. Those *are* the small touches
  this skill exists to capture.
- "Asking 老板 to confirm small touches feels patronizing" — 5 seconds of
  patronizing is ≪ 3 hours of wrong-layer rebuild.
- "Boss said '抄 X 那种风格' so style is what he wants" — never assume from
  the noun. The verb '复现' / '抄' / '做成那种' / '感觉' all require the
  layer-validation question.

**Required AskUserQuestion before any composition code is written**
(after frame extraction + reading + identifying small touches):

> 看完 reference 我识别出这些小心思 (列出来)，确认一下：
>
> - 老板想要的是 **编排+小心思** (mouse-as-narrator / form morph / live diff
>   typing 等都复刻)，
> - 还是只要 **视觉表层** (cream/coral/serif/grid 的氛围，叙事另起)，
> - 还是 **两者都要**？
>
> 不一样的层会决定我接下来 80% 的代码长在哪儿，先对齐再开干。

### Step 1: Get the reference file

Ask 老板 to download the source video to a known path. WebM/MP4 both fine.

### Step 2: Dense frame extraction (4fps minimum)

```bash
mkdir -p /tmp/ref-dense
ffmpeg -i /path/to/reference.webm -vf fps=4 /tmp/ref-dense/f%04d.png
```

1fps loses small touches — you'll miss cursor sub-paths, ripple frames,
2-frame letter type-ins. Always use 4fps or denser for the analysis pass.

### Step 3: Read frames in clusters, identify "small touches"

Read ~10 frames per cluster. Don't try to absorb the whole video in one
read. Look specifically for:

- **Mouse cursor as narrator** — does it appear, glide, click, hover?
- **Trailing-word emphasis** — does the last word of a sentence change
  color, weight, or get an underline flash?
- **Form transformation** — does a UI element morph shape across cuts (pill
  → full prompt, button → modal, etc.)?
- **Agent in-progress states** — spinners ticking to checks, line-by-line
  task list resolution, "Done" footer arriving last.
- **Live edits** — code diff appearing letter-by-letter, not as a static
  snapshot.
- **Camera moves** — zoom-out for context, slow drift for "settling".
- **Trailing CTA / outro pacing** — usually a long beat (1.5–2s) with the
  brand mark, then nothing.

### Step 4: Validate understanding with 老板 before rebuilding

After identifying the small touches, list them back to 老板 via
`AskUserQuestion` and **get confirmation before writing 500 lines of TSX**.
This prevents another "you abstracted to the wrong layer" round-trip.

## Visual language (cream / coral / serif / grid)

Only after editing logic is locked, apply the surface tokens:

| Token | Value | Use |
| --- | --- | --- |
| Cream (intro/outro bg) | `#E5DCCE` | First and last beat, heroic statements |
| Bone-white (demo bg) | `#FAF7F1` | Product-UI demo beats |
| Coral (accent) | `#CC785C` | Trailing-word emphasis, ripples, "Done" check, primary CTA |
| Ink (primary text) | `#2C2C2A` | Body, code |
| Subtle grid | 1px `rgba(60,40,20,0.06)` 80px | Demo bg only, *never* on cream beats |
| Serif | Fraunces (display, italic restraint) | Headlines, outro |
| Sans | Inter (UI labels, footer) | Buttons, footer text |
| Mono | JetBrains Mono | Code, terminal, file paths |

Sizes: headline ~120–140px on 1920×1080, body ~36px, mono ~28px.
Generous letter-spacing on serif headlines (`-0.02em` to `-0.01em`).

## Editing-logic playbook (the small touches that matter)

Each pattern below is a reusable beat. Compose 3–6 of them per video.

### A. Trailing-word reveal (intro headline)

Headline appears full, then the last word transitions: ghost-grey →
coral, with a short coral underline that scales 0→1 then fades.

```tsx
const ghostMix = ease(clamp01((frame - 30) / 14));
const r = lerp(182, 204, ghostMix); // ghost-grey -> coral
const underlineGrow = clamp01((frame - 38) / 14);
const underlineFade = clamp01((frame - 56) / 6);
const underlineOpacity = clamp01(underlineGrow - underlineFade);
```

Timing: word stays visible 8–12 frames before the underline fades, then
the next beat starts. Don't rush.

### B. Cursor as narrator + click feedback

The mouse cursor is a character. It glides in, hovers a beat, then clicks
with **visible feedback** before the target morphs. Three distinct phases:

1. **Glide** (8–14 frames) — eased trajectory from off-stage to target.
2. **Click feedback** (4–8 frames) — coral ripple ring expands from click
   point + button press-scale (0.96) for 2–3 frames.
3. **Morph** (12–20 frames) — only NOW does the target transform.

```tsx
const ClickRipple = ({ x, y, start }) => {
  const t = clamp01((useCurrentFrame() - start) / 16);
  if (t <= 0 || t >= 1) return null;
  const eased = ease(t);
  const size = lerp(16, 110, eased);
  const opacity = (1 - eased) * 0.55;
  return <div style={{
    position: 'absolute', left: x - size/2, top: y - size/2,
    width: size, height: size, borderRadius: '50%',
    border: `2px solid ${coral}`, opacity,
  }} />;
};
```

**Common mistake:** triggering the morph at the same frame as the cursor
arrival. Insert the click feedback gap or it reads as "magic morph".

### C. Product-UI form transformation

A UI element keeps continuity by morphing — pill button widens into a
full-width prompt, single-line input expands into multi-line composer.
Same border-radius, same shadow, just dimensions interpolate.

Anchor the morph to a **single fixed point** (usually the left edge or
center) so the eye tracks it. Don't morph from two corners simultaneously.

### D. Agent in-progress states

A vertical task list where each item starts with a spinning circle and
resolves to a check, sequentially. Anthropic's pacing: ~20 frames per
task, with a 6-frame pause between resolution and the next spinner
starting. Final "Done — opened PR #N" line arrives in coral, after the
last check, with a footer fade-in delay.

### E. Live diff typing (NOT static diff)

Show the original code, then a yellow flash highlight on the line about
to change, then the line becomes a red `−` deletion, and a green `+`
line types in **letter-by-letter** with a blinking caret. Footer "edited
by Claude · N changes" arrives last.

```tsx
const NEW_LINE = '  return claims.exp > Date.now();';
const charsShown = Math.max(0, Math.min(NEW_LINE.length,
  Math.floor((frame - typeStartFrame) / 2)));
// 2 frames per character = ~15 chars/sec, feels natural
```

Don't show the whole new line at once — kills the agency feel.

### F. Outro pacing

Brand mark + tagline appears, holds for 1.5–2s, then fade to cream. **No
text overlay, no CTA on the last second** — let the brand land.

## Composition skeleton

Default structure for a 24s @ 30fps piece (720 frames):

```tsx
<Series>
  <Series.Sequence durationInFrames={60}>{/* IntroScene */}</Series.Sequence>
  <Series.Sequence durationInFrames={540}>{/* MainArc — 4-6 beats */}</Series.Sequence>
  <Series.Sequence durationInFrames={120}>{/* OutroScene */}</Series.Sequence>
</Series>
```

Beat budgeting inside MainArc: aim for 80–120 frames per beat. Less than
80 reads as choppy; more than 120 starts to feel slow unless it's a
finale beat (live diff + done state).

## Self-check protocol (Iron rule #4) — MANDATORY before showing 老板

YOU MUST run ffmpeg key-frame extraction + Read on every render before
telling 老板 it's ready. Every render. There is no "small enough change"
exception. There is no "studio preview already showed it" exception. There
is no "let 老板 scrub the mp4 himself, faster feedback" exception. **None.**

After every render, **extract key frames at the moments of each polish
point** and Read them yourself.

```bash
mkdir -p /tmp/check
for t in 1.6 3.95 16.7 17.2 23.0; do  # one per polish point
  ffmpeg -ss $t -i out/video-vN.mp4 -frames:v 1 -y /tmp/check/t${t}s.png 2>/dev/null
done
```

Then `Read` each PNG. Verify the actual visual matches what the code was
*supposed* to produce. The cost of one self-check pass is ~30 seconds of
your time and saves a round-trip with 老板.

**Specifically forbidden:**

- "I verified the polish in source, render is mechanical" — source
  verifies *intent*, ffmpeg+Read verifies *output*. They are different
  checks. Source-only verification is what produced the
  "claude-fleet d1df0922" lesson (claimed measured durations, actually
  hardcoded). Don't do it again.
- "Studio preview already showed it" — studio renders differently from
  `renderMedia` (timing, font subsetting, asset loading, codec). The mp4
  is what 老板 sees. Verify the mp4.
- "He can scrub the mp4 himself" — his scrubbing time = 5–10 min round
  trip. Your self-check time = 30s. You optimized for your own laziness
  and called it his speed. Stop.
- "It's just a small re-render, no need" — small diffs are exactly when
  off-by-one frame timings slip in unnoticed. Risk doesn't scale with
  diff size; it's constant. Self-check scales with risk.
- "I already self-checked v3, v4 only changed 3 polish points" — v4 IS a
  new render. Self-check it. Take the 30 seconds.

**What counts as a valid self-check pass** (vs. a shortcut):

- ≥1 frame per polish point or new beat (extract with `ffmpeg -ss <t>`).
- Each frame Read by you (the actual Read tool, not just listed in `ls`).
- Each frame compared to the *intended* visual (not just "is it
  non-blank").
- If a frame disagrees with intent, fix BEFORE showing 老板. Do not show
  + explain known defects — fix first, show second.

This rule comes from a real lesson: I once claimed audio was synced to
measured durations when actually I'd hardcoded them. 老板 caught it
because all numbers were 0.5 multiples. Don't do that here either.
Reference: `memory/MEMORY.md` lesson "claude-fleet d1df0922".

## Known environment pitfalls

### macOS IPv6 loopback breaks Remotion port detection

On some macOS installs, IPv6 loopback (`::1`) connections **hang to a 3s
timeout** instead of returning ECONNREFUSED. Remotion's `getPort` treats
timeout as "unavailable", so every port appears taken and rendering fails
with "No available ports found".

**Fix:** patch `node_modules/@remotion/renderer/dist/port-config.js`
`getHostsToTry` to return only IPv4:

```js
const getHostsToTry = (flattened) => {
  return [
    hasIpv4LoopbackAddress(flattened) ? '127.0.0.1' : null,
    '0.0.0.0',
  ].filter(truthy);
};
```

The patch lives in `node_modules` and gets wiped by `npm install` —
re-apply after dep changes. (Long-term: open an upstream issue in the
remotion repo with the IPv6 timeout reproduction.)

### Rules-of-Hooks violations from inline render functions

Don't define a sub-component inside a `.map()` or inside the parent
component body and then call hooks in it — extract it as its own named
component file or top-level const. Easy to hit when iterating fast.

## Boss's interaction preferences for this kind of work

The five iron rules above already encode the discipline-level preferences
(don't oversell, validate layer, self-check, Player-vs-mp4 first). Don't
re-derive them from this section — go to the iron rules. This section
covers only the protocol-level preferences:

- **中文回复**, 称呼"老板", AskUserQuestion 走 Fleet 决策卡。详见
  `~/.claude/fleet-interaction-mode.md`.
- **Show, don't summarize.** When you have a render to share, run `open`
  on the file so 老板 can play it in QuickTime. Pair with an
  AskUserQuestion card stating what was checked. Don't paste a wall of
  text describing what's in the video — pixels first, words second.
- **Polish in batches of 3.** When iterating, group ~3 polish points per
  re-render (not 1 at a time, not 10). 老板's pacing matches that beat:
  one batch = one decision card.

## Project location reference

The first full reproduction lives at:
`/Users/hoveychen/workspace/claude-code-video-toolkit/projects/claude-code-intro/`
with the composition at `src/AnthropicLikeIntro.tsx`. Use it as a
working reference for structure, color tokens, and the polish patterns
above. Don't blindly copy — every new project has its own narrative
beats; reuse the *patterns*, not the *content*.

## Quick reference

| Task | Command |
| --- | --- |
| Scaffold composition | `cd <toolkit-root>/projects/<name> && npm install` |
| Studio (live preview) | `npx remotion studio` |
| Render mp4 | `npx remotion render <CompName> out/video-vN.mp4` |
| Extract reference frames | `ffmpeg -i ref.webm -vf fps=4 /tmp/ref/f%04d.png` |
| Self-check key frame | `ffmpeg -ss <sec> -i out/x.mp4 -frames:v 1 /tmp/check.png` |
| Apply IPv6 patch | edit `node_modules/@remotion/renderer/dist/port-config.js` |
