---
name: tutorial-authoring
description: >-
  Author, revise, reorganize, or review step-by-step tutorials (software,
  hardware, any tool) to minimize cognitive load and maximize first-attempt
  success rate. Use when writing a new guide, improving an existing one,
  auditing tutorial structure, or reorganizing course content. Apply multimedia
  learning theory and minimalism automatically. Triggers on: 'tutorial',
  'step-by-step guide', 'hands-on guide', 'walkthrough', 'how-to', 'reorganize
  tutorial', 'revise guide', 'improve tutorial quality', 'review tutorial
  structure', 'チュートリアル', '整理し直す', 'マルチメディア学習'.
---

# Tutorial authoring

Use this skill when writing, revising, or auditing any document where a reader
follows steps to build or achieve something.

## Scientific foundations

All authoring rules derive from these established principles. Apply them actively
when both writing new tutorials and reviewing existing ones.

| Principle | Source | Core insight | Authoring implication |
|---|---|---|---|
| **マルチメディアの原理 (Multimedia)** | Mayer, 2009 | テキスト単体より、テキスト＋画像の組み合わせが学習を促進する | 全ての操作ステップには対応する画像を付ける |
| **空間的接近の原理 (Spatial contiguity)** | Mayer, 2009 | 画像とテキストが空間的に近い方が効果的 | 画像は説明テキストの直前に配置する。画像を手順の前にまとめて置かない |
| **時間的近接の原理 (Temporal contiguity)** | Mayer, 2009 | テキストと画像は継続的に提示されるよりも同時に提示される方が効果的 | 音声ナレーション付き動画では、対応する画像のタイミングに合わせてナレーションを流す |
| **一貫性の原理 (Coherence)** | Mayer, 2009 | 教示内容と無関係な文書・画像・音は学習を阻害する | 装飾的な画像・面白い余談・BGMはすべて除去する。教材が楽しくなっても学習効率は下がる |
| **モダリティの原理 (Modality)** | Mayer, 2009 | 視覚＋視覚より、視覚＋聴覚など異なるモダリティの組み合わせが有効 | ナレーション付き動画では、テキストをナレーションと被せず、画像に集中させる |
| **冗長性の原理 (Redundancy)** | Mayer, 2009 | 同じ情報を複数フォーマットで提示すると学習を阻害する | 画像が示している内容をテキストで繰り返さない。ナレーションと同一の文章を画面に表示しない |
| **セグメンティングの原理 (Segmenting)** | Mayer, 2009 | 学習者がペースを制御できる方が学習効果が高い | 工程を小さな段階に区切り、一度に一つの概念を提示する |
| **ミニマリズム (Minimalism)** | Carroll, 1990 | すぐに行動開始・doing で学ぶ | コンセプト説明を最小化し、最初のアクションをできるだけ早める |

## Information hierarchy

Every tutorial is composed of exactly these layers:

```
Tutorial (page)
 └── Step (milestone: "when done, you can X")
      ├── goal — 1 sentence declaring the end state
      ├── Concept × N — term/background, always collapsible, before first use
      ├── Reference × N — lookup tables, always collapsible, near relevant procedure
      ├── Procedure × N — a group of actions toward one sub-goal
      │    ├── why — 1 sentence: why this procedure exists (optional)
      │    ├── Action × N — the atomic unit (image + instruction + result)
      │    └── Verify — "→ expected result" (1 line)
      ├── Recovery — error recovery, inline, after the action that can fail
      └── Checkpoint — end-of-step checklist (exactly one per Step)
```

## Five information types and display rules

| Type | Content | Display | Placement |
|---|---|---|---|
| **Action** | Image + instruction + result | Always visible. Image above text, 1:1 mapping | Inside Procedure |
| **Verify** | Success confirmation | Always visible, `→` prefix, 1 line | End of Procedure |
| **Concept** | Term definition, background | Collapsible (`<details>`) | Before procedure that first uses it |
| **Reference** | Key tables, panel lists | Collapsible (`<details>`) | Near procedure that needs it |
| **Recovery** | Error recovery steps | Always visible, short | After action that can fail |

## Image / text / video hierarchy

| Subject | Primary | Secondary | Rationale |
|---|---|---|---|
| UI operation (where to click) | Annotated screenshot | Label text only | Unknown UI requires visual anchor |
| Result (what happened) | Text (`→` 1 line) | Screenshot (optional) | State changes are faster to judge via text |
| Concept (why) | Text only | — | Abstraction does not benefit from images |
| Multi-step continuous flow | Video/GIF | Text (supplement) | Motion cannot be conveyed in stills |

## Atomic unit: Action

The smallest learning unit is:

```
[Image: WHERE to interact] → [Text: WHAT to do] → [Text: WHAT happens (optional)]
```

Rules:
- One image per action. Never batch images.
- Image is always above/before text (spatial contiguity).
- Do not describe in text what the image already shows (redundancy elimination).
- If the action produces a visible result, state it inline; **do not** create a
  separate Verify — those are for Procedure-level confirmation only.

## Writing rules

### Action text
- Use imperative: 「〜をクリックします」「〜と入力します」
- Name the exact UI element in bold: 「**コンパイル**」をクリック
- Panel/location names appear inline on first use:
  「画面下部の**コンテンツブラウザ**（Content Browser）から〜」

### Concept text
- Max 5 sentences or 1 short table.
- Must answer: "what is it?" and "why does the learner need to know right now?"
- If it takes more than 5 sentences, split into multiple Concepts.

### Verify text
- Always starts with `→`
- Describes observable state, not internal mechanics:
  ✅ 「→ キューブが消えれば成功です」
  ❌ 「→ Destroy Actor が実行されました」

### Checkpoint
- Bullet list of observable behaviors.
- No internal state or jargon.

## Anti-patterns (do NOT do)

| Anti-pattern | Violated principle | Fix |
|---|---|---|
| Images batched before steps | Spatial contiguity | 1 image per Action, placed directly before its text |
| Text restating what image shows | Redundancy | Remove the text or remove the image |
| Decorative images, fun sidebars, background music | Coherence | Remove entirely; they impair learning |
| Same content in narration AND on-screen text | Redundancy / Modality | Use narration OR on-screen text, not both |
| `:::note` for concepts | Segmenting | Not collapsible; use Concept component |
| `---` between sub-steps | — | Visual noise; only between Steps |
| Verify after every action | Segmenting | Verify at Procedure end only |
| Front-loading reference tables | Minimalism | Use Reference, near first use |
| Term introduced before it's needed | Minimalism | Concept before first-use Procedure |

## Component system (course-docs-platform)

When writing for `@metyatech/course-docs-platform`-based sites, use the
provided MDX components. They are globally available (no import needed):

```mdx
<Step goal="アイテムに触れると消えてスコアが増える">

  <Concept title="コリジョンとは">
    当たり判定のこと。ブロック＝壁、オーバーラップ＝すり抜け＋検知。
  </Concept>

  <Procedure why="触れたことを検知できるようにする">
    <Action img="./img/overlap-events-on.png">
      **Generate Overlap Events** をオンにする
    </Action>
    <Action img="./img/overlap-all-dynamic.png">
      **コリジョンプリセット**を **OverlapAllDynamic** に変更する
    </Action>
    <Verify>アイテムをすり抜けて通れる</Verify>
  </Procedure>

  <Checkpoint>
    - アイテムに触れるとスコアが増える
    - アイテムに触れると消える
  </Checkpoint>

</Step>
```

### Components

| Component | Props | Purpose |
|---|---|---|
| `<Step>` | `goal` (string) | Milestone wrapper |
| `<Procedure>` | `why` (string, optional) | Groups actions into a logical task |
| `<Action>` | `img` (string, optional), `alt` (string, optional) | Atomic operation with image |
| `<Verify>` | children | Procedure success confirmation |
| `<Concept>` | `title` (string) | Collapsible background/term |
| `<Reference>` | `title` (string) | Collapsible lookup table |
| `<Checkpoint>` | children | End-of-step checklist |

## Non-component tutorials

When components are not available (plain Markdown, Docusaurus, etc.), apply the
same information hierarchy using native syntax:

| Component equivalent | Plain Markdown |
|---|---|
| `<Step goal="...">` | `## Step N：タイトル` + first line = goal sentence |
| `<Concept>` | `<details><summary>💡 Title</summary>...</details>` |
| `<Reference>` | `<details><summary>📖 Title</summary>...</details>` |
| `<Procedure>` | `### N-M. Title` |
| `<Action>` | `![alt](img)` on its own line, then numbered list item |
| `<Verify>` | `**→ expected result**` |
| `<Checkpoint>` | `:::tip[確認ポイント]` or equivalent admonition |

The hierarchy and writing rules remain identical regardless of tooling.
