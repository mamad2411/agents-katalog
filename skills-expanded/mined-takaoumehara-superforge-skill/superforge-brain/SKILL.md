---
name: superforge-brain
description: >
  Run the BreakBias engine — an exhaustive, machine-checkable idea sweep — or a
  lighter classic method (SCAMPER, Six Hats, Crazy 8s, How Might We). Decompose
  across five lenses, name the hidden bias on every element, ban the obvious
  three, and push each element through eight techniques as a tracked cell
  ledger in fresh contexts. Nothing dies for being unoriginal: existing ideas
  survive on a delta, geographic gap, timing shift, or execution flaw, and
  judgment splits originality from viability. A range dial (grounded /
  balanced / far-out) sets how safe or wild the shortlist is, a push ladder
  stretches survivors toward far-out, and every killed idea stays visible and
  recyclable. Use when the user says "brainstorm", "ideas", "what could we
  build", "reframe this", "something more original", "far-out", "アイデア",
  "発想", "ブレスト", "企画", "ありきたりじゃないもの", "ありきたりだけど需要はある",
  "ぶっ飛んだ案", "捨てた案も見たい", "何が作れる", "BreakBias", "SIT",
  "虱潰しで考えて", or runs /superforge-brain.
license: MIT
metadata:
  author: Takao Umehara
  version: "5.0"
compatibility: >
  Standalone.
  Reads docs/brief.md when present and writes docs/product-idea.md plus,
  for a full sweep, docs/product-idea.ledger.json and docs/product-idea.html
  (rendered from assets/idea-map.html).
  The market pass uses web search when available; without it, mark market
  status as unknown rather than guessing.
  Claude Code can run the sweep as workflows/superforge-brain-sweep.js (fresh
  context per element batch); elsewhere the prose procedure below is complete.
  Delegates to installed ideation skills when available; works alone when they are absent.
---

# Superforge Brain — the BreakBias engine

Most idea generation stops when something plausible arrives. BreakBias does
not stop, because stopping is a decision made by whoever got tired first.
Instead it enumerates every (element × technique × sub-method) combination as
a **cell**, and a run is finished only when every cell has a terminal status.

Software can hold a 300-cell ledger and never lose its place. A person in a
workshop cannot. That asymmetry is the reason to run this as a skill rather
than as a meeting.

**Lineage.** The two floor constraints — Closed World and Function Follows
Form — come from SIT (Systematic Inventive Thinking). BreakBias extends it:
eight techniques instead of five, a named bias on every element, an explicit
ban list that novelty is then scored against, the cell ledger, judgment in a
separate context, and a market gate placed after judgment.

---

## 0. Iron rules (non-negotiable)

1. **Closed World** — never import an element from outside the system and its
   immediate boundary. The moment you add something external it stops being
   non-obvious and becomes an addition anyone could have made. This binds the
   **sweep**. The one sanctioned exception is the far-out rung of the push
   ladder (§7.5), which runs after judgment and carries an `open_world` tag so
   nobody mistakes it for a swept cell.
2. **Form first** — construct the impossible state, **withhold judgment**, and
   derive the value backwards. Never reason forward from a benefit.
3. **Ban the obvious three** — list the three answers any model reaches for
   first and outlaw them *before* generating. They go into the artifact. The
   ban applies to **generation only**: §6 revisits all three once the sweep is
   done, because the most obvious answer to a problem is often the right one.
4. **No pruning mid-sweep** — deduplication, killing, and scoring happen after
   generation, never during.
5. **Never skip a cell** — no ellipsis, no "and so on". A cell you did not run
   is not a cell you decided against.

---

## 1. Choose the method — do not assume the full sweep

BreakBias is one way to generate ideas, not the only one this skill offers.
Ask once, before generating anything:

| Method | What actually happens | Use when |
|---|---|---|
| **BreakBias sweep** (recommended default for a real decision) | Every (element × technique × sub-method) combination runs as a tracked cell. Nothing is skipped, every kill carries a reason, survivors are scored blind to how they were generated. Minutes to an hour depending on resolution. | the idea needs to hold up — funding, a pivot, "we've been circling this for weeks" |
| **A classic method** (SCAMPER, Six Hats, Crazy 8s, How Might We, and others) | A single fast divergent pass, no cell ledger, no kill codes, no blind judging. | a first pass, low stakes, a workshop about participation rather than proof |

Full menu and how to run each classic method →
**`references/classic-methods.md`**. If the user picks a classic method, that
file replaces the rest of this procedure for the run; come back here only if
they later want to upgrade to a full sweep.

The rest of this document (§2 onward) is the BreakBias sweep.

---

## 2. Scope the run

- **Domain A — an object** (a product, a service, a screen, a business).
  Decompose the thing itself.
- **Domain B — a capability** (a technology, a skill, a dataset with no fixed
  use). Decompose what it can do, then sweep for who would want it.

**Resolution — the exhaustiveness dial. Explain it before asking, in these
terms, not just the label:**

> "解像度は、要素の数 × 技法8種 × サブ手法の掛け算で決まるセルの総数です。
> セル1つが『この要素を、この技法のこのやり方で、実際に1つ考えてみる』とい
> う1回の生成です。多いほど網羅的で、少ないほど速いという単純なトレードオフ
> です。"

Then offer the three levels with what each one **means**, not only the count:

| | Cells | What that buys you | Use when |
|---|---|---|---|
| `quick` | ~80 | one sub-method per technique on the highest-potential elements only — a real pass, not a token gesture, but several corners of the space go untouched | a first look, one sitting |
| `standard` | ~300 | every element crossed with every technique and its sub-methods once | a real product decision |
| `exhaustive` | 900+ | `standard`, plus every collapse-prevention unblocking lens applied wherever a technique repeats a shape | the answer matters more than the hours |

State the resolution chosen and hold to it — do not quietly downgrade mid-run
because the cell count got long.

**Range dial — how safe or how wild the answer should be.** Ask it in the same
breath as resolution, in these terms:

> 「振れ幅は、最後に手渡す候補の配分です。どれを選んでも全セルは生成され、捨て
> た案も全部見えます。変わるのは『定番・本命・飛び』の3レーンに何枠ずつ割くか
> と、どこまで押し広げるかだけです。」

| Dial | Shortlist of 10 (定番 / 本命 / 飛び) | Push ladder goes to | Use when |
|---|---|---|---|
| `grounded` | 5 / 3 / 2 | rung 2 (stretch) | the money or the deadline is real; you want something that ships |
| `balanced` (default) | 3 / 4 / 3 | rung 3 on the top seeds only | most runs |
| `far-out` | 2 / 3 / 5 | rung 3 on every seed, plus cross-breeding | you are tired of sensible answers and want to see the edge |

The dial **never deletes anything** — it reallocates shortlist slots. Because
lanes are derived from scores at render time, the HTML lets the reader turn the
dial afterwards and watch the shortlist change without re-running anything.
Lanes, seeds, and quotas → **`references/amplify-and-recycle.md`** §1.

---

## 3. Decompose, and name the bias on every element

Five lenses, minimum counts enforced. Every element carries the hidden
assumption it rests on, written as a sentence — that named assumption is what
the sweep later breaks.

| Lens | Question | Minimum |
|---|---|---|
| **Structural** | components, screens, spaces, assets, roles | ≥ 12 |
| **Process** | ordered steps, waits, frictions | ≥ 8 |
| **Functional** | primary and secondary jobs of each part | ≥ 8 |
| **Relational** | internal ↔ external (time, mood, weather, device, crowding) | ≥ 8 |
| **Conceptual** | industry dogma, customer expectation, unquestioned premise | ≥ 6 |

Merge into one master element list (20–40 rows), each with its bias and a
Break Potential of low / med / high. That list becomes the rows of the ledger.

---

## 4. The cell ledger

`element × technique × sub-method = one cell`, each with an ID and a status.

```
cell_id, element_id, technique, sub_method, status, kill_code, prior_art, win_path
```

Statuses move one direction only:
`todo → generated → survived | killed:<G|P|C> → developed → judged`. A duplicate
absorbed during dedup ends at `merged` (with `merged_into`), and a cell left
out on purpose by the resolution is not in the ledger at all — its element is
marked `swept: false` instead.

`prior_art` is a flag, not a verdict — a cell that already exists somewhere is
tagged during generation and resolved after it (§6). `win_path` records which
of the four win-path codes let a tagged cell through. Neither may be filled in
mid-sweep.

The run is complete when no cell is left at `todo` or `generated`. Report
progress as *n / total cells terminal* — never as a feeling of completeness.

---

## 5. Sweep — eight techniques

Sub-methods, the per-cell output format, and the collapse-prevention rules are
in `references/ideation-tools.md` §1. One pass per technique is a guess; the
sub-methods are what make it a sweep.

1. **Subtraction** — remove a vital element
2. **Division** — split by function, time, or space
3. **Multiplication** — clone with one attribute mutated
4. **Task Unification** — give an existing element a second job
5. **Attribute Dependency** — bind an internal variable to an external one
6. **Reverse** — invert a core premise
7. **Shift** — move the value vector off the industry axis
8. **Repurpose** — transpose across scale, senses, time, or environment

Techniques 6–8 are BreakBias extensions, not part of classical SIT.

When a cell keeps producing the same shape, apply an unblocking lens before
moving on — TRIZ trade-off dissolution, inverted sabotage, or Jobs To Be Done
(`references/ideation-tools.md` §2).

**Generate each element batch in a fresh context.** The commonest reason a
sweep returns weak ideas is not the method but fatigue: by cell 200 of one long
context, every form is a variation of a form already written, and the model is
pattern-completing its own earlier output. A batch sees only the brief, its own
element rows, and the banned list — never another element's cells. In Claude
Code, `workflows/superforge-brain-sweep.js` enforces this; without it, follow
the prose fallback in `references/amplify-and-recycle.md` §4 (re-anchor per
element, shape-repeat ledger).

---

## 6. Kill — only two codes, and 既出 is not one of them

Default is survival. Only two things may kill a cell outright, because only
these two can be checked **without market knowledge** — and §8 exists precisely
because market knowledge introduced early collapses a sweep:

- **G — generic**: swapping the subject for any other subject leaves the idea
  intact. It was never about this system.
- **P — physically impossible**: contradicts reality and cannot be
  reinterpreted into something that holds.

**「既にある」は殺す理由ではありません。** A cell whose idea already ships
somewhere is tagged `prior_art` and then run through the **win-path test** —
差分 `w:delta` / 地理 `w:geo` / 時機 `w:timing` / 実行 `w:exec`. Passing any one
of them means it survives, and the code that passed becomes the brief for what
to build. Only a tagged cell that passes **none** of the four is killed, with
code **C**, which now means *"we looked for a way to win in four directions and
found none"* rather than *"this exists."*

Then run a **salvage pass** over the killed rows: a cell killed for the wrong
reason returns to `survived`. Wrongful kills are the expensive failure here,
because nobody ever sees what was discarded.

Finally, **revisit the banned three** (§0 rule 3) exactly once, running the same
win-path test on each. They were banned from *generation*, which was correct;
they were never meant to be banned from *consideration*. This step is what
recovers the ordinary-but-needed idea — the supermarket every town needs — that
the old procedure deleted without ever showing anyone.

The win-path tests, the C redefinition, and the revisit protocol →
**`references/value-classification.md`** §3–§4.

---

## 7. Judge in a separate context

Survivors are developed into cards — one sentence, **one concrete scene** (who,
where, which moment, what they see or do), why it is surprising, user value,
business value, a price or cost guess, risks, next experiment — and judged
**without the generation rationale**. The scene is not decoration: a card that
can only be written in abstract nouns (「体験価値を高める」「つながりを生む」)
is the second commonest reason ideas feel weak, and the judge is told to score
an unwritable scene as low Wow. Rewrite it concrete or let it score low —
never let vagueness pass as depth. The judge sees the card, the ban list, and the scoring
anchors. Nothing about how the idea was reached.

Four axes, 1–10. **Novelty is the distance from the banned three**, so a
polished cliché scores low by construction.

`Novelty` · `Wow Factor` · `User Impact` · `Company Impact`

**Then stop before adding them up.** Novelty and business value are different
questions, and one total answers neither. Sum them into two axes and read the
quadrant:

- **独創軸 = Novelty + Wow** (2–20) — has anyone seen this?
- **事業軸 = User Impact + Company Impact** (2–20) — would anyone care and pay?

| | 事業軸 ≤ 11 | 事業軸 ≥ 12 |
|---|---|---|
| **独創軸 ≥ 12** | **Lab** — 面白いが今は金にならない。**捨てず**に棚に置き、戻る条件を1文で書く | **Hero** — 見たこともなく、かつ需要がある |
| **独創軸 ≤ 11** | **Discard** — 唯一の正当な廃棄 | **Workhorse** — ありふれているが確実に必要とされる。勝負は独創性ではなく勝ち筋コード |

A Workhorse scoring 3 on Novelty is **not** a weak Hero. It is a correctly
scored ordinary business, and ordinary businesses are most of the businesses
that work. Never raise a Workhorse's novelty to make it look better — that is
how a working idea becomes a clever one nobody wants.

Output a table: `| コンセプト | 要素 | 技法 | 壊したバイアス | N | W | U | C | 独創軸 | 事業軸 | 象限 | 勝ち筋 |`

Quadrant definitions, the Lab re-entry condition, and what each quadrant does
next → **`references/value-classification.md`** §1–§2.

---

## 7.5 Amplify — push the survivors, then cross-breed them

A cell is one transformation of one element. Good ideas are rarely one step
from the obvious; they are usually a decent idea pushed two steps further, or
two decent ideas from different corners combined. The sweep cannot produce
either by construction, so this step does.

- **Push ladder.** Each seed (chosen by the dial from Heroes, the strongest
  Workhorses, Lab entries, and anything the user recycled) gets three rungs:
  **L1 grounded** — the smallest version that could ship in 30 days, Closed
  World intact · **L2 stretch** — one more premise broken · **L3 far-out** —
  may import one outside element or jump ten years, must state *why it is
  impossible today* and *the first step that is possible today*, tagged
  `open_world`. Every rung is a new card with `parent` and `rung`, judged blind
  like any other.
- **Cross-breed** (`balanced` top pairs, `far-out` always). Pair survivors from
  different techniques **and** different elements whose broken biases do not
  contradict; the hybrid must name what each parent contributes. Tagged
  `hybrid` with both parent IDs.

Rungs and hybrids join the same ledger and the same quadrant map, so the reader
can see whether the best idea came from the sweep, the push, or a cross.
Protocol, seed counts, and card fields → **`references/amplify-and-recycle.md`**
§2–§3.

---

## 8. Market, only after judgment

Never before. Market knowledge is the strongest source of premature collapse:
knowing a space is crowded makes a model stop proposing anything in it.

Required for **Hero** and **Workhorse**, optional for **Lab**, skipped for
Discard: **red** (crowded) / **gray** (adjacent incumbents) / **white** (nobody
there). Then an entry verdict — `wedge` / `open` / `avoid` / `watch` — with
named incumbents and a willingness-to-pay hypothesis. Detail in
`references/ideation-tools.md` §4.

A Workhorse is expected to come back **red**, and that is not a failure — a
crowded market is proof the demand is real. For a Workhorse the market pass
answers a different question than for a Hero: not "is there room" but "does the
win-path code from §6 still hold once the incumbents are named."

---

## 9. Synthesise

- **Shortlist by lane, using the dial** — 定番 (Workhorse) / 本命 (Hero) /
  飛び (Lab, plus any `open_world` rung). Fill each lane's quota from §2 with
  its strongest cards; if a lane cannot fill, say so rather than promoting a
  card from another lane
- **Cluster** the survivors (UX / 収益 / コスト / ブランド / コミュニティ / データ / ラディカル / 即試せる / 長期)
- **Name the biases that broke repeatedly** — that repetition marks where the
  real opportunity is
- **Hero Concepts (top 3–5)**: 一行 / 壊したバイアス / 体験ストーリー / 事業モデル / MVP / 検証計画 / リスク / 次の一歩
- **Workhorse candidates**: 勝ち筋コードと、それが名指しした「変える一点」。ここでは体験ストーリーより**実行計画**が本体
- **Lab shelf**: 独創軸だけが高かった案と、それぞれの「戻ってくる条件」
- **Experiment roadmap**: 1日 / 1週間 / 30日で試すことと、その成功指標

Then run the direction filter in `references/ideation-tools.md` §3 on Heroes
and Workhorses together. Concept quality and build-worthiness are different
questions and must be scored separately — and a Workhorse frequently beats a
Hero on that filter, because `Pull` and `Reach` are exactly where an ordinary,
well-understood need is strongest.

**Then leave the room.** Everything up to this point was generated and graded
by the same system, which means a 900-cell sweep is not truer than an 80-cell
one — only more thorough about the same assumptions. Take the top candidates to
real people before committing, using questions about what they have already
done rather than what they would do →
**`references/talk-to-users.md`**. A Hero and a Workhorse need opposite
interviews, and asking a Workhorse the Hero questions is how a perfectly good
ordinary business gets talked out of existence.

**Build `docs/product-idea.html` alongside the markdown** by copying
`assets/idea-map.html` and replacing its embedded ledger with the run's
`docs/product-idea.ledger.json` — never hand-write the page. It shows every
generated cell, not only survivors, with kill codes and reasons left visible;
a live range dial over the shortlist; a recycle tray that turns ticked cards
into a command the user pastes back (§Execution modes); an
Impact × Effort map with the low-hanging-fruit quadrant named; a User
Impact × Company Impact map from the judge's own axes; and the
独創軸 × 事業軸 quadrant map that separates Hero / Workhorse / Lab / Discard.
Full spec in `references/idea-map-output.md`. This is what lets someone who was
not in the room see what was cut, what was kept for a different reason, and
why — instead of being handed only the last three names standing.

---

## Execution modes

- **sweep** — 確認せず、仮定を明示して全セルを走り切る。長ければ技法ごとに分割出力し、通し番号は維持する
- **partner (default)** — 分解後・スイープ後・審判後で停止して方向を確認する。**創造フェーズは partner でも全セル生成する**
- **facilitation** — 答えの前に問いを渡す（問い → 観点 → ヒント → 小例 → AI案）

### Follow-up commands (read `docs/product-idea.ledger.json`, never regenerate the sweep)

- `/superforge-brain recycle <cell_id…> [--push grounded|stretch|far-out]` —
  拾い直す。指定セルを `recycled` にし、カード化 → 審判 →（指定時）Push ladder に通す
- `/superforge-brain push <cell_id…> [--to stretch|far-out]` — 生き残りをさらに押し広げる
- `/superforge-brain cross <cell_id> <cell_id>` — 2案を掛け合わせる
- `/superforge-brain dial grounded|balanced|far-out` — ショートリストだけを組み直す（生成はしない）

The HTML's recycle tray writes exactly these strings. Protocol →
`references/amplify-and-recycle.md` §5.

## Quality check — ask these after the run

- 手法（BreakBias か classic method か）を、始める前にユーザーに確認したか
- 分解は下限件数を満たし、各要素にバイアスを命名したか
- 台帳に `todo` / `generated` の残りは無いか。飛ばしたセルを「無かったこと」にしていないか
- 各セルで「ありえない形」を先に握り、メリットを逆算したか（形が先か）
- Closed World を守ったか。箱の外から要素を足していないか
- 平凡3案を禁止してから発想したか。そして**スイープ後に一度だけ再訪したか**
- kill は G と P だけになっているか。「既にある」を理由に殺していないか
- `prior_art` の付いたセルすべてに、勝ち筋テスト（delta / geo / timing / exec）を走らせたか。C は4つとも落ちた場合にだけ付いているか
- 救済パスを走らせたか
- 審判は生成過程を見ずに採点したか。4軸を**1つの合計にせず**、独創軸と事業軸に分けたか
- Workhorse を「独創性が低い」という理由で捨てていないか
- Lab の各案に「戻ってくる条件」が1文で書かれているか。書けないものを棚に残していないか
- 振れ幅ダイヤルを始める前に確認したか。ショートリストのレーン配分はダイヤル通りか。埋まらないレーンを他から水増ししていないか
- 要素バッチごとに新しい文脈で生成したか（またはプロズ版のフォールバックで形の重複を数えたか）
- 全カードに具体的な場面が1つ書かれているか。抽象語だけのカードを審判に通していないか
- Push ladder の L3 に `open_world` タグ、「今はなぜ無理か」「今できる最初の一歩」が付いているか
- `docs/product-idea.ledger.json` が書かれ、HTML がそれと同じデータで描画されているか
- 市場判定は審判の後だったか
- `docs/product-idea.html` は殺したセルも含めて全件見えるか。勝者だけになっていないか。4象限のマップが出ているか
- 実在の人に確認したか。していないなら「していない」と成果物に書いたか。お世辞と証拠を区別できる形で質問を残したか

---

## Deeper reference

**`references/ideation-tools.md`** carries what this procedure needs and does
not contain: §1 the sub-methods that make each technique exhaustive, plus the
cell format and collapse-prevention rules · §2 the tools that run *before* the
sweep, to confirm the right thing is being decomposed · §3 the direction
filter that runs *after*, to decide which Hero Concept is worth building ·
§4 the kill-code tests, the judge protocol, and the market rubric.

**`references/classic-methods.md`** — the lighter alternative to a full sweep:
SCAMPER, Six Thinking Hats, Crazy 8s, How Might We, brainwriting, reverse
brainstorming, and random input, with what each is for and weak at. Read it at
§1, before assuming the sweep is the only option.

**`references/value-classification.md`** — why a single score deletes working
businesses, the 独創軸 × 事業軸 quadrants (Hero / Workhorse / Lab / Discard),
the four win-path codes that let an existing idea through, and the ban-list
revisit. Read it at §6, before killing anything.

**`references/talk-to-users.md`** — the sweep runs entirely inside your own
head. This is how to check it against real people without the questions
producing flattery instead of information. Run it on Hero and Workhorse
candidates before committing to one. It also specifies the five-section research
synthesis for when the interviews must brief a team.

**`references/idea-map-output.md`** — the `docs/product-idea.html` spec: the
all-ideas board that keeps killed cells visible, the three 2×2 maps, the range
dial, and the recycle tray. `assets/idea-map.html` is its reference
implementation — copy it and swap the data.

**`references/amplify-and-recycle.md`** — the v5 additions: range dial and
lanes (§1), push ladder (§2), cross-breeding (§3), fresh-context generation and
its prose fallback (§4), the ledger JSON and the recycle / push / cross / dial
commands (§5).

## Artifact

Write `docs/product-idea.md` before reporting back — including the banned
obvious three **with their revisit outcome**, the Lab shelf with each entry's
re-entry condition, and the final ledger counts, so nobody re-proposes a banned
idea, nobody loses an idea that was only early, and nobody mistakes a partial
sweep for a complete one. Read `docs/brief.md` first if it exists and confirm
its premise rather than re-asking.

For a BreakBias sweep, also write `docs/product-idea.ledger.json` (the ledger,
schema in `references/amplify-and-recycle.md` §5) and `docs/product-idea.html`
rendered from it — see `references/idea-map-output.md`. The JSON is what makes
recycle, push, and dial possible in a later session without re-running the
sweep. Not required after a classic-method session,
where there is no ledger to visualise.

## Delegate when a sharper skill is installed

`brainstorming` (structured divergence) · `idea-generator` (mining the user's
own expertise) · `validate-thinking` / `roast` (pressure-testing) ·
`market-research`, `competitive-analysis` (reality check) · `product-name` ·
`embodied-product-director` (camera, sensor, movement products).
If a skill is absent, do the step inline. Never block on a missing skill.
