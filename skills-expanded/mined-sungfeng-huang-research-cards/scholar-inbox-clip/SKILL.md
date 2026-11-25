---
name: scholar-inbox-clip
description: >-
  Read all unread Scholar Inbox emails from Mac Mail.app (Scholar Alert Digests
  and Trending Papers), fetch each paper's AI overview from alphaXiv (or fall
  back to the raw paper), translate to the configured output language (default Traditional Chinese), apply color
  highlights, and create Heptabase cards. Use when the user asks to process
  Scholar Inbox papers, clip papers from alphaXiv, or update Heptabase with
  new research. Invoked with NO paper URL, it instead runs a BACKFILL
  maintenance pass: find existing alphaXiv cards whose Tasks property is empty
  (an automated run may have skipped semantic tagging), annotate them, and
  re-sync the affected comparison-overview cards. An explicit "re-audit" /
  「重審 Tasks」 ask runs the RE-AUDIT pass instead: semantic review of
  already-set Tasks values, proposing mis-tag removals for user approval.
allowed-tools: Bash(osascript *) Bash(heptabase *) Bash(python3 *) Bash(mktemp *) Bash(curl *) mcp__alphaxiv__get_paper_content mcp__alphaxiv__discover_papers WebFetch WebSearch
---

# Scholar Inbox → Heptabase Clip Skill

## Agent（claude / codex）

本 skill 可由 Claude Code 或 Codex 駕駛（Codex 端：`research-cards@private-plugins` plugin 的 scholar-inbox-clip skill）。
差異：Codex 排程的 `run.py` 透過 Codex app-server 的 model-free
`mcpServer/tool/call` 呼叫 `alphaxiv.get_paper_content`，直接重用 Codex 的 MCP
設定與 OAuth；MCP 初始化／呼叫失敗時，該輪才退回內建 HTTPS 抓取，避免無人值守
漏信。Claude 腳本路徑維持 HTTPS（互動 Claude 可直接用 alphaXiv MCP）。cron/scripts
的文字生成呼叫依 config `agent` 分流（claude --print / codex exec），互動 session
一律由駕駛中的 agent 本人生成。

## Backend（heptabase / obsidian / both）

讀 `~/.config/research-cards/config.json`（樣板：plugin 根目錄 `config.example.json`）。
`heptabase`/`both`（或無 config）：原 heptabase CLI 路徑，行為不變（自動化流程安全）。
`obsidian`：卡片＝vault `Papers/` 的 .md（frontmatter 存 arxiv_id/source_type/tasks），
journal＝每日筆記 `<date>.md`（資料夾由 `obsidian.journal.folder` 設定，空＝vault 根），顏色標記＝`<span style="color:…">`、
toggle＝`- ⏵ `字首 bullet（plugin markdown 方言，Obsidian 可渲染、不可誤點）。`check-tasks` 的選項清單在
obsidian 模式改為「OVERVIEW_TASKS ∪ vault 既有 tasks 值」（無 tag database 可查）。

## 互動模式的兩條硬規則（cron 以外的每一次 clip，任何 backend）

1. **卡片必須直接以教學式格式產出**（card-rewrite 的 8 點清單：一句話／為什麼〈config profile.reader〉該讀／0. 先備知識／教學式正文／中英並列／快速摘要／圖片／上色／Source）。
   「baseline 翻譯卡＋日後 retrofit」只是 cron（run.py 無人值守）的權宜——互動 clip 沒有理由產出半成品。
2. **圖片放置不要 shell 出 claude CLI**（巢狀呼叫在互動 session 內會失敗）：先
   `headings, figs = run.figure_candidates(cid, arxiv_id)` 看候選，
   自行決定後 `run.insert_figures_into_card(cid, arxiv_id, placements=[...])`。
   cron 路徑仍走 call_claude，失敗時自動降級為無圖並進 retry 記錄，不會中斷管線。

Automates the full pipeline: read digest emails → fetch alphaXiv AI
overview per paper → translate to the output language → color-highlight key
text → create Heptabase cards.

**Sources（同一信箱資料夾、逐封自動分流）**：
- **Scholar Inbox / Scholar Alert digests**——個人化清單，信裡的論文全數
  進管線（分數／連結解析）。
- **HuggingFace Daily Papers**（主旨「Daily papers of …」）——arxiv ID 直
  取自 `huggingface.co/papers/<id>` 連結、讚數取自「(N ▲)」行。榜單**非**
  個人化，入選前兩層選文：`email.hf_min_upvotes` 讚數門檻（預設 0）→
  config `profile.field` 領域相關性（`call_claude` 依標題挑；明確回 NONE
  ＝整封略過並標記已處理；呼叫失敗＝保守全收、大聲記錄）。
- 其他帶 arxiv/alphaXiv 連結的信件走通用萃取。

---

## Invocation modes — pick by what the user passed

| Invocation | Mode | What runs |
|------------|------|-----------|
| **explicit paper URL(s)** (`/research-cards:scholar-inbox-clip https://arxiv.org/abs/…`) | **Clip** | Build a card per URL: Steps 2–6 + 6.5 (auto-tag + overview sync) + 7. Skip Step 1 (no email scan). |
| **no argument** (`/research-cards:scholar-inbox-clip`) | **Backfill** | Do **NOT** scan email (the scheduled desktop routine already does that). Jump to **「Backfill mode」** below: tag any cards whose Tasks is empty, then sync overviews. |
| **"re-audit" / 「重審 Tasks」** | **Re-audit** | Semantic review of EXISTING Tasks values (mis-tags / drift). Jump to **「Re-audit mode」** below — proposals first, removals only after user approval. |
| **"掃信件" / explicit email request** | **Email clip** | The full Steps 1–8 email loop (same as the scheduled routine). |

A **Claude Code desktop-app routine** runs the email loop on a schedule (with a
model in the loop, so Step 6.5 tagging + overview sync happen in the same pass
— unlike the retired launchd cron, which could only create untagged cards). A
bare manual `/research-cards:scholar-inbox-clip` is for **maintenance**, not
re-scanning mail.

---

## Backfill mode (no URL) — tag untagged cards + maintain overviews

An automated pipeline run sets `study/paper` + `Source Type=alphaXiv` + `arxiv
ID` on every card, but a run without a model in the loop can't set `Tasks`
(semantic judgment is Claude's job). The retired launchd cron always left
Tasks empty; the desktop routine tags in-pass, so this mode is now a **safety
net** (routine failures, legacy backlog), not a daily queue. It finds untagged
cards and finishes them.

### B1 — List the untagged targets
```bash
cd ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/scholar-inbox-clip
python3 run.py --list-untagged          # Source Type=alphaXiv, Tasks empty, newest-first
# python3 run.py --list-untagged all    # also legacy non-alphaXiv hand-made notes
```
Scope is **alphaXiv (pipeline-made) cards only** by default — legacy hand-made
notes are left alone unless `all` is passed.

**Tasks vocabulary self-check** — after renaming any Tasks option in Heptabase, run:
```bash
python3 run.py check-tasks              # exit 0 = consistent; 1 = mismatch
```
It cross-checks the routing map (`OVERVIEW_TASKS`) and per-card usage against the
property's LIVE options, so a rename left stale in code (or a typo'd/orphan value
on cards) is caught. `[warn]` on options with 0 cards is informational.

### B2 — Read each card and annotate `Tasks` (additive)
For each listed card, read it (`heptabase note read <id>`) and apply the Step
6.5a rubric: pick a primary task + any clear cross-cutting axis from the
**existing** options, union via `set_tasks()` (never removes). **Many clipped cards
are off-topic** (LLM/vision/agent papers like *Qwen3*, *DeepSeek-V4*, *Seedance*,
*World Action Models*) — those get **no speech/audio Task**, but DO get
`Topics`（`set_topics()`：LLM / Foundation Model、Agentic AI 等主軸分類，
0–2 個）。Only the genuinely speech/audio ones get **Tasks**.

For scale (dozens of cards), fan out with parallel subagents: each reads a batch
and returns `{card_id, tasks:[…], topics:[…]}` decisions; then in the main loop
apply `set_tasks()` **and `set_topics()`** for each（off-topic 卡 tasks 為空、
topics 必有值——這正是它的完成標記，漏掉會永遠留在 backfill 佇列）and
collect the union of `overviews_to_sync()` results. `--list-untagged` 的每筆
帶 `missing`（`["topics"]`＝只補 Topics 的舊卡；`["tasks","topics"]`＝全新
未標卡），照它決定要跑哪幾步。

### B3 — Sync every affected overview once
```python
import run as R
affected = set()
for card_id, chosen in decisions:                 # chosen = the tags you picked
    applied = R.set_tasks(card_id, chosen)        # additive
    affected.update(R.overviews_to_sync(applied))
# → affected = topic keys of the unified `overview` skill（見 Step 6.5b 路由表；single source of truth = run.py OVERVIEW_TASKS）
```
Run the **`overview`** skill once per topic key in `affected` at the end (each
run does its own `status` → author missing sections → `sort`). Then report a summary
(how many cards tagged, how many left empty as off-topic, which overviews synced).

---

## Re-audit mode（重審既有 Tasks 值）— explicit ask only

Backfill only fills EMPTY Tasks (additive, never removes). This mode is the
other direction: review cards whose Tasks are **already set** and correct
mis-tags. Run it only when the user explicitly asks (re-audit / 重審 / 清理
Tasks) — removals are judgment-heavy and rare.

### R1 — List the targets
```bash
python3 run.py --list-tagged          # alphaXiv cards with non-empty Tasks + their values
# python3 run.py --list-tagged all    # also legacy hand-made notes
```

### R2 — Triage, then judge (title-level first, read only the suspicious)
Most (title, values) pairs are obviously fine — don't read every card. Flag a
card only when a value looks semantically WRONG for the paper (e.g. a vision
paper carrying `ASR`). Two verdicts, only the first is a removal:
- **Mis-tag** — the value does not describe the paper → propose removal.
- **Deliberate delegation / drift** — the value is accurate but the owning
  topic has no own-angle for the paper (e.g. AudioLM carrying `Audio LM` while
  its only section lives in Spoken (A1)). **NOT a removal**: that is what the
  `overview` skill's `[elsewhere]` marker + the topic doc's 已判分工 record
  are for. Never remove a true value to tidy a status listing.
For scale, fan out subagent batches like B2.

**Known deliberate conventions（勿當 mis-tag；2026-07-05 首輪 re-audit 265 張全
乾淨時歸納）**：
1. **前驅標記** — 通用生成方法論文（DDPM/Score-SDE/CFG/Edit Flows）掛其語音應用
   值，作為 G 卡的機制前驅段落。
2. **他山之石** — vision tokenizer/表示論文（TiTok/RAE/MANZANO…）掛
   `Tokenizer/Codec/Representation`，Tok (III) 的既定範圍。
3. **文字推理入 R** — 純文字推理論文（DeepSeek-R1/GRAM/NF-CoT/MAI-Thinking-1…）
   掛 `Reasoning`；R 卡明訂涵蓋語音・音訊・文字推理。
4. **效率桶** — infra 論文（FlashAttention/GQA/speculative decoding…）掛非路由值
   `Streaming / Low-latency` 作一致分類。

### R3 — Present proposals, WAIT for approval
Report a table `card / current Tasks / remove / add / reason`. Do NOT apply
anything yet — removals need the user's explicit go-ahead (additions alone may
proceed, they're backfill-equivalent).

### R4 — Apply + resync
```python
import run as R
before, after = R.retag_tasks(card_id, remove=[...], add=[...])
affected.update(R.overviews_to_sync(set(before) ^ set(after)))
```
Run the `overview` skill per affected topic key once at the end. Note: a
removal shrinks that topic's corpus enumeration only — existing overview
sections are untouched (prune a section separately if it no longer belongs,
via the `overview` skill). Finish with `python3 run.py check-tasks`.

---

## Step 1 — Read Scholar Inbox Emails (Multi-Email Loop)

Use AppleScript via `osascript` to read Scholar Inbox digests from Mac Mail.app.
The mailbox is in the iCloud account and is named "Scholar Inbox".

The script scans the **newest `MAX_SCAN` (40) emails** with an index-based loop
(message 1 = newest), stopping early only on `---OUT_OF_RANGE---`. Already-seen
emails are skipped cheaply via the `subject|recv_date` dedup, with **no
"N-consecutive-skips" early stop** — a paper-bearing email can have a subject
that looks nothing like a digest (e.g. *"Introducing alphaXiv Assistant 2.0 +
Pro Plan"* embeds 5 paper links) and may sit *below* several already-processed
emails; an early stop would never reach it. Detection is **content-based, not
subject-based**: every non-skipped email is scanned for paper links regardless
of subject.

```applescript
on run argv
  set msgIndex to (item 1 of argv) as integer
  tell application "Mail"
    set targetAccount to first account whose name contains "iCloud"
    set inboxFolder to first mailbox of targetAccount whose name is "Scholar Inbox"
    if msgIndex > (count of messages of inboxFolder) then
      return "---OUT_OF_RANGE---"
    end if
    set theMessage to message msgIndex of inboxFolder
    set msgSubject to subject of theMessage
    set msgContent to content of theMessage
    set d to date received of theMessage
    set isoDate to (year of d as string) & "-" & ¬
      (text -2 thru -1 of ("0" & (month of d as integer))) & "-" & ¬
      (text -2 thru -1 of ("0" & (day of d as integer)))
    return msgSubject & "\n---DATE---\n" & isoDate & "\n---BODY---\n" & msgContent
  end tell
end run
```

Call with: `osascript -e '...' "$INDEX"` where INDEX starts at 1. `message 1` is
the **newest** email; higher indices are older.

The AppleScript also returns the email's **received date** (ISO `YYYY-MM-DD`)
between `---DATE---` markers — used for journal headings and the dedup key (see
below). Same-subject emails (e.g. repeated "Trending Papers + Weekly Seminar")
recur on different dates, so the dedup key is `"{subject}|{recv_date}"`, NOT the
subject alone — otherwise the second occurrence is wrongly skipped.

**Important:** Scholar Inbox emails do NOT contain direct `arxiv.org` URLs in
plain text. However:
- **Scholar Alert Digests**: plain text body has this format per paper:
  ```
  <score>
  ArXiv YYYY (Month DD)        ← arxiv preprints
  <title>
  <authors>
  ```
  **Conference proceedings papers use a different venue line with NO
  parenthetical date** (e.g. `ICLR 2026`, `EACL 2026`, `Findings of EACL 2026`,
  `AAAI 2026`). The regex MUST accept a multi-word venue and an optional `(Month
  DD)`, or ~40% of a digest's papers are silently dropped:
  ```python
  r'\n(\d{2,3})\s*\n[A-Za-z][A-Za-z .]*?\s\d{4}\s*(?:\([^)]+\))?\s*\n([^\n]+)\n([^\n]+)\n'
  ```
- **Trending Papers**: plain text has no arxiv URLs, but the **HTML source**
  contains `alphaxiv.org/abs/XXXX.XXXXX` links — extract these to get arxiv IDs.

**CRITICAL — Quoted-printable decoding of HTML source:** The email HTML source
is MIME quoted-printable encoded. Long lines are wrapped with a soft line break
`=\n` (equals sign + newline) that can fall **in the middle of an arxiv ID**,
e.g. `alphaxiv.org/abs/2606.=\n05405`. You MUST strip `=\n` from the source
**before** running any regex, or those IDs are silently dropped:

```python
decoded_source = source.replace("=\n", "")
```

This was a real bug — `2606.05405` and others were being missed until decoded.

**Non-arxiv paper IDs:** Not every paper is on arxiv. A paper ID is therefore
one of these forms, and the whole pipeline keys off `id_kind()` / `bare_id()`
helpers in `run.py`:

| ID form | source | example |
|---------|--------|---------|
| `XXXX.XXXXX` | arxiv | `2604.00292` |
| `alphaxiv:{slug}` | alphaXiv-only (not on arxiv) | `alphaxiv:deepseek-v4` |
| `openreview:{id}` | OpenReview | `openreview:JbLmIoWwDC` |
| `aclanthology:{id}` | ACL Anthology conference paper | `aclanthology:2026.eacl-short.18` |

- **alphaXiv-only slugs** (`alphaxiv.org/abs/deepseek-v4`): `run.py`'s
  `resolve_named_alphaxiv_id()` first tries the page `<title>` → arxiv API; if
  not on arxiv it **keeps `alphaxiv:{slug}`** (the alphaXiv overview still
  exists, so a card can be built). Earlier versions dropped these.
- **ACL Anthology conference papers** (EACL/Findings, not on arxiv/alphaXiv):
  resolve the title via Semantic Scholar / DBLP (`api.semanticscholar.org`,
  `dblp.org/search/publ/api`) to get the abstract + anthology ID, then build a
  card from the abstract with `arxiv ID = aclanthology:{id}`.
- For non-arxiv IDs: `fetch_arxiv_images()` returns `[]` and
  `append_arxiv_html_link()` is skipped (no arxiv HTML), but **figures still come
  from the PDF** via `fetch_pdf_figures()` (see Step 5a.2 — openreview /
  aclanthology / alphaXiv-slug all have downloadable PDFs). The Source link /
  fetch use `bare_id()`.

Parse `(score, title, authors)` tuples (Scholar Alert Digests) with the
conference-aware regex shown above.

Then resolve each title to an arxiv ID. **Try in this order:**

1. **Extract numeric IDs from HTML source** — after `=\n` decode, regex for
   `alphaxiv.org/(abs|overview|zh/overview)/XXXX.XXXXX` and `arxiv.org/(abs|pdf)/XXXX.XXXXX`
2. **Resolve non-numeric alphaxiv slugs** — fetch page `<title>` → arxiv API;
   keep as `alphaxiv:{slug}` if not on arxiv
3. **arxiv API search by title** — `https://export.arxiv.org/api/query?search_query=ti:"title"&max_results=3`
4. **Semantic Scholar / DBLP** — for conference-only papers (EACL/Findings),
   gives the abstract + `aclanthology:{id}`
5. **Claude fallback** — ask Claude via `mcp__alphaxiv__discover_papers`

---

## Step 2 — For Each Paper: Fetch alphaXiv AI Content

Use `mcp__alphaxiv__get_paper_content` with the alphaXiv overview URL:

```
url: https://alphaxiv.org/overview/{arxiv_id}
```

**Codex scheduled `run.py` path (MCP-first):** `fetch_alphaxiv()` starts one
ephemeral, read-only Codex app-server thread per pipeline run and calls
`mcpServer/tool/call` directly — no model turn, no per-paper model-token cost. It
reuses the logged-in `alphaxiv` MCP OAuth. If startup, OAuth, server, protocol, or
tool output fails, MCP is disabled for the rest of that run and the pipeline uses
the HTTPS path below. Set `SCHOLAR_CLIP_ALPHAXIV_TRANSPORT=http` only as an
emergency/debug override. A fresh Desktop conversation is not required.

**HTTPS fallback / Claude scripted path:** `run.py` fetches the overview page
directly. **The page is
a client-rendered SPA — the report is NOT in the rendered HTML** (tag-stripping
yields ~250 chars of nav chrome). It lives in the serialized JS payload as the
value of an `intermediateReport:"..."` key, JSON-string-escaped. `run.py` calls
`_extract_intermediate_report()` to pull and unescape it. If you ever fetch the
overview with plain `curl`/`urllib`, do the same — do NOT translate the raw
HTML, or the model receives only `<head>` CSS/JS-preload boilerplate and the
whole report (especially late sections) is lost.

**Detecting whether an AI report was returned vs. raw text:**

- **AI report** (structured): begins with a phrase like
  `"This report provides a detailed analysis"` or
  `"The following report provides"`, and contains numbered sections
  (`### 1. Authors`, `### 2. How This Work Fits`, etc.)
- **Raw text** (fallback): begins directly with the paper title, abstract,
  author affiliations — no report framing

If the result is an **AI report**: proceed to Step 3a.  
If the result is **raw text**: proceed to Step 3b.

---

## Step 3a — AI Report Available: Translate to Chinese

> **Card style = the `card-rewrite` skill (single source of truth).** The target
> card format is the teaching-style spec defined in `${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/card-rewrite/SKILL.md`
> (一句話 + 為何該讀 / 先備知識 glossary / teach the WHY / bilingual terms /
> filled 快速摘要 / preserved figures / colorization). For an **interactive**
> `/research-cards:scholar-inbox-clip`, after creating the baseline card, invoke **`/research-cards:card-rewrite`**
> on it to produce the final teaching-style version (it mandates fetching the
> alphaXiv original via MCP as the grounding source). The scripted `run.py` keeps
> emitting the baseline translated card below; a later `/research-cards:card-rewrite` retrofit
> upgrades it. Do not duplicate the style spec here — change it only in card-rewrite.

Translate the full English AI report to the output language (see the Language rule below; default Traditional Chinese), preserving:
- All section headings and numbering
- All numerical results, percentages, model names (keep in original form)
- Table structure (convert to markdown tables)
- Technical terms: keep English term first, add Chinese in parentheses on
  first occurrence, e.g. "副語言（paralinguistic）"

**CRITICAL — do not over-compress the report's later subsections.** Reports for
papers with a primary task plus a secondary one (e.g. ASR as the main result and
TTS/generation as a "preliminary" exploration) put the secondary topic near the
END of sections 4 (Methodology) and 5 (Findings). These late subsections carry
real mechanism detail — for TTS that means the **next-token VAE decoder**
(linear → μ/log σ², reparameterization `z = μ + σ·ε`, residual MLP → Mel frame,
Conv1D Postnet, stop-token head) and its **training losses** (L1+MSE, KL, stop,
flux). Translate these at the SAME fidelity as the primary task; never collapse a
multi-step pipeline into a single sentence like "採用 next-token VAE 進行初步探索".
Two failure modes cause this loss, both now guarded in `run.py`:
1. **Content truncation:** the report is ~15-20K chars; `translate_content`,
   `generate_summary`, and `generate_color_rules` previously capped at
   10K/6K/8K, silently dropping sections 5-6. Caps are now 24K/12K/12K so the
   full report (incl. the trailing secondary-task subsections) is translated.
2. **Over-summarization:** even with full content in the prompt, do not editorialize
   a late subsection down to one line because it reads as "preliminary."

Structure the card content as follows:

```markdown
# [alphaXiv] {Paper Title}

**作者**：{Authors}（{Institution}）

**關鍵詞**：{3-5 key terms from paper}

---

## 1. 作者與機構
{translated content}

## 2. 研究背景與定位
{translated content}

## 3. 核心目標與動機
{translated content}

## 4. 研究方法
{translated content}

## 5. 主要發現與結果
{translated content — include all numbers and tables}

## 6. 研究意義與影響
{translated content}

---

Source: https://www.alphaxiv.org/zh/overview/{arxiv_id}
```

**CRITICAL — strip translation preamble:** `claude --print` (and Claude in
general) sometimes ignores the "直接從 # 開始輸出" prompt instruction and
prepends a preamble line such as:

> *"I have the full report. Now I'll translate it to the output language
> following the rules and insert the 4 most important figures."*

If this leaks into the card, it becomes the card **title** (Heptabase derives
the title from the first content node). Do NOT rely on the prompt alone —
**enforce it in code** by discarding everything before the first `# ` (h1)
heading. `run.py` does this in `_strip_translate_preamble()`, applied to every
`translate_content()` return value:

```python
def _strip_translate_preamble(markdown):
    """Drop any preamble before the first `# ` h1 — the true start of the card."""
    if not markdown:
        return markdown
    lines = markdown.splitlines()
    for i, line in enumerate(lines):
        if re.match(r'^#\s+', line):
            return "\n".join(lines[i:]).strip()
    return markdown.strip()
```

**Backfill fix for existing cards:** if old cards already have this preamble,
read each card, find the first `heading` node with `level == 1`, and remove all
`doc["content"]` nodes before it, then save. The title auto-updates to the h1.

---

## Step 3b — No AI Report: Generate from Raw Paper

When `get_paper_content` returns raw text (no structured report), read the
paper content and generate your own structured Chinese summary following the
same 6-section format above.

You can also try fetching the static arxiv HTML page for fuller content:
```
https://arxiv.org/html/{arxiv_id}
```

Use WebFetch with prompt: "Extract the full paper content including abstract,
introduction, methods, experiments, and conclusion."

Generate the card in the same format as Step 3a.

---

## Step 4 — Create Initial Card

Write the markdown to a temp file and create the Heptabase card:

```bash
TMPFILE=$(mktemp /tmp/paper_XXXXXX.md)
# write markdown content to $TMPFILE
heptabase note create --content-file "$TMPFILE"
# capture the returned card ID
```

---

## Step 4.5 — Insert Quick Summary Block

After creating the card, insert a structured summary section **before** the
AI content (right after the first `horizontal_rule` separator). This gives
readers a fast overview at the top of each card.

The summary contains five parts:
- **AI 摘要** — 2–3 sentence description of the paper
- **問題** — 3 bullet points on what problems the paper addresses
- **方法** — 3 bullet points on the methods proposed
- **結果** — 3 main experimental results with numbers
- **要點** — 3 key takeaways

**IMPORTANT: ProseMirror node constraints for Heptabase:**
- Use `"type": "strong"` for bold marks (NOT `"type": "bold"`)
- Use `"type": "horizontal_rule"` for dividers (NOT `"type": "horizontalRule"`)
- `attrs: {"id": null}` is acceptable for new nodes
- **Supported list node types** (confirmed from "List blocks" card):
  - `bullet_list_item` — attrs: `{"id": null, "folded": false, "format": null}`, first child is `paragraph`
  - `numbered_list_item` — attrs: `{"id": null, "order": null, "format": null}`
  - `toggle_list_item` — attrs: `{"id": null, "folded": false}`, first child is `paragraph` (the label), remaining children are content nodes
  - `todo_list_item` — attrs: `{"id": null, "checked": false}`

Each section (AI 摘要, 問題, 方法, 結果, 要點) is a **`toggle_list_item`** with a bold label and nested content:

```python
def make_para(text):
    return {"type": "paragraph", "attrs": {"id": None},
            "content": [{"type": "text", "text": text}]}

def make_hr():
    return {"type": "horizontal_rule", "attrs": {"id": None}}

def make_bullet_item(text):
    return {
        "type": "bullet_list_item",
        "attrs": {"id": None, "folded": False, "format": None},
        "content": [{"type": "paragraph", "attrs": {"id": None},
                     "content": [{"type": "text", "text": text}]}]
    }

def make_toggle(label_text, content_nodes, folded=False):
    label_para = {"type": "paragraph", "attrs": {"id": None},
                  "content": [{"type": "text",
                                "marks": [{"type": "strong"}],
                                "text": label_text}]}
    return {
        "type": "toggle_list_item",
        "attrs": {"id": None, "folded": folded},
        "content": [label_para] + content_nodes
    }

def build_summary_nodes(ai_summary, problems, methods, results, takeaways):
    return [
        {"type": "heading", "attrs": {"level": 2, "id": None},
         "content": [{"type": "text", "text": "快速摘要"}]},
        make_toggle("AI 摘要", [make_para(ai_summary)]),
        make_toggle("問題",    [make_bullet_item(p) for p in problems]),
        make_toggle("方法",    [make_bullet_item(m) for m in methods]),
        make_toggle("結果",    [make_bullet_item(r) for r in results]),
        make_toggle("要點",    [make_bullet_item(t) for t in takeaways]),
        make_hr(),
    ]

# Find insertion point: after first horizontal_rule (metadata separator)
insert_after = next(
    (i for i, n in enumerate(doc["content"]) if n.get("type") == "horizontal_rule"),
    None
)
if insert_after is None:
    insert_after = next(
        (i for i, n in enumerate(doc["content"])
         if n.get("type") == "heading" and n.get("attrs", {}).get("level") == 1),
        0
    )

doc["content"] = (
    doc["content"][:insert_after + 1] +
    build_summary_nodes(ai_summary, problems, methods, results, takeaways) +
    doc["content"][insert_after + 1:]
)
```

Generate the summary content based on the translated card content created in
Step 3a/3b. All content in the output language.

---

## Step 5 — Colorize + Insert Figures (one pass)

After creating the card, do colorization and figure insertion in a **single
Python script** that reads the card once, modifies the ProseMirror JSON, and
saves once.

### 5a — Fetch Figure List from arxiv HTML (with ar5iv fallback)

**Primary source**: `https://arxiv.org/html/{arxiv_id}` — available for most papers from 2024+.

**Fallback**: `https://ar5iv.org/abs/{arxiv_id}` — used when arxiv HTML returns 404
(older papers, ~2023 and earlier). ar5iv is a third-party LaTeX→HTML converter.

Figure source formats `_parse_figures` handles (all need `rsvg-convert` —
`brew install librsvg` — for the SVG cases):

1. **PNG/JPG** (most common): `<img src="...png">` inside `<figure>`.
2. **External SVG file**: `<img src="...svg">` → fetch the file and convert to a
   PNG data URL (`_svg_url_to_data_url`).
3. **Inline SVG**: `<svg>…</svg>` embedded directly in the `<figure>` → convert
   to a PNG data URL (`_svg_to_data_url`). Max 2 SVG figures per card.

Only `<figure>`-wrapped elements count — bare inline `<svg>` elsewhere in the
page (mobile-nav toggle icons, logos) and `<figure class="ltx_table">` (tables)
are correctly ignored. Papers whose only "figures" are LaTeX tables therefore
yield zero images — that is expected, not a bug.

The implementation in `run.py` uses `_parse_figures(html, base_url, arxiv_id)` shared
by both sources, with `fetch_arxiv_images()` orchestrating the fallback:

```python
def fetch_arxiv_images(arxiv_id):
    # Primary: arxiv HTML
    try:
        html = _fetch_html(f"https://arxiv.org/html/{arxiv_id}")
        results = _parse_figures(html, "https://arxiv.org", arxiv_id)
        if results:
            return results
    except urllib.error.HTTPError as e:
        if e.code != 404:
            return []
    except Exception:
        return []

    # Fallback: ar5iv (for papers without HTML version on arxiv)
    try:
        html = _fetch_html(f"https://ar5iv.org/abs/{arxiv_id}")
        return _parse_figures(html, "https://ar5iv.org", arxiv_id)
    except Exception:
        return []
```

**Image URL resolution** (`_resolve_fig_url`) — the page lives at
`{base_url}/html/{arxiv_id}/`, so **every relative src must be rooted there**:
- src starts with `http` → use as-is
- src starts with `/` (ar5iv relative, e.g. `/html/2203.16502/assets/x1.png`) →
  `{base_url}/html/2203.16502/assets/x1.png`
- src contains `/` AND its first segment is an arxiv id (e.g. `2605.27772v1/x1.png`) →
  `{base_url}/html/2605.27772v1/x1.png` (already paper-rooted)
- src contains `/` but is a relative subpath (e.g. `extracted/5314337/images/x.png`
  or `image/y.png`) → `{base_url}/html/{arxiv_id}/extracted/5314337/images/x.png`
- bare filename (e.g. `x1.png`) → `{base_url}/html/{arxiv_id}/x1.png`

**Skip**: srcs containing `static`, `icon`, `logo`, or `ar5iv.png` (ar5iv logo).

**Never** drop the arxiv_id. This was a real, widespread bug: relative subpaths
like `extracted/.../x.png` were rooted at `…/html/extracted/.../x.png` (no
arxiv_id) → **HTTP 404 broken images on ~11 cards**. `_resolve_fig_url`
centralizes the correct logic for both the PNG/JPG and external-SVG branches;
the audit (5a.3) caught and fixed the already-stored broken URLs in bulk.

### 5a.3 — Image-health detection & repair (broken / blank / missing)

A figure can be embedded yet still render as a broken-image icon (dead URL) or a
blank box (bad crop). `run.py` detects and repairs these:

- `image_health(src)` → `ok | broken_url | blank | corrupt`:
  - **http(s) URL** → `_url_is_image()` does a 2 KB ranged GET, accepts only
    `200/206` with an image content-type or image magic bytes.
  - **data-URL** → `_data_url_is_blank()` decodes it and runs
    `_pixmap_is_low_content` (needs PyMuPDF); near-uniform ⇒ `blank`.
- `repair_card_images(card_id, arxiv_id)`:
  1. **broken_url whose only fault is a missing arxiv_id** → `_corrected_html_url()`
     inserts the arxiv_id and, if the corrected URL resolves, fixes the src **in
     place** (keeps placement + caption — cheap, no re-fetch).
  2. **otherwise broken / blank / corrupt** → the image and its italic caption
     paragraph are removed.
  3. if the card is left with **zero images** → `insert_figures_into_card`
     re-fetches fresh figures (HTML → ar5iv → **PDF screenshot fallback**).
- `audit_and_repair_all(dry_run=False)` sweeps every alphaXiv card and repairs
  the deficient ones. Network-heavy (one ranged GET per URL image) — run
  manually/periodically, not every scheduled run.

**Why blank / label-poor SVG figures happen:** `rsvg-convert` silently drops
some text labels when rasterizing inline `<svg>` (observed on 2606.10231 — the
architecture boxes rendered but the `m₁/t₁/prompt` token labels vanished). The
PDF screenshot path (`fetch_pdf_figures`, vector text rendered by PyMuPDF)
preserves all labels, so **prefer a PDF render over an SVG-converted figure**
when a figure looks label-poor.

**`fetch_pdf_figures` known limits — when to crop manually.** The auto-extractor
locates a figure as the union of image/vector blocks above a `Figure N` caption.
Two layouts still defeat it; for these, render the region by hand (locate the
caption's `y0`, crop the visual band just above it at full content width, ~900px
JPEG ≤ ~50K chars, insert + Chinese caption):
1. **Full-page-width figures** (caption spanning both columns) — *partly* handled
   now: a caption wider than 60% of the page triggers a full-width bound, and the
   render width/quality steps down until it fits the card's char budget. But a
   figure taller/denser than the budget allows is still skipped.
2. **Fine-grained vector figures** (e.g. radar/spider charts, observed on
   2604.14148 — 33 separate line-segment drawing blocks): the body-text `floor`
   above the figure clips the block union, so the crop comes back empty. These
   need a manual crop bounded by the figure's actual `y0..caption.y0`.

**Heptabase content size limit: 100,000 characters.** data URL images (~37KB
each at 600px) count toward this. Max 2 SVG figures per card. Always use
`--content-file` instead of `--content` when saving cards with data URLs.

### 5a.2 — PDF figure fallback (no HTML figures)

When no HTML figure source is available, `run.py`'s `fetch_pdf_figures(paper_id)`
renders figures **straight from the paper PDF**. This covers brand-new arxiv
papers (PDF only), vector/table-only HTML papers, AND every **non-arxiv** source
— each has a downloadable PDF via `pdf_url_for()`:

| kind | PDF URL |
|------|---------|
| arxiv | `https://arxiv.org/pdf/{id}` |
| openreview | `https://openreview.net/pdf?id={id}` |
| aclanthology | `https://aclanthology.org/{id}.pdf` |
| alphaxiv slug | `https://pdfs.assets.alphaxiv.org/{id}v1.pdf` (alphaXiv hosts a copy) |

Requires **PyMuPDF** — `/usr/bin/python3 -m pip install --user pymupdf` (scripted
runs use `/usr/bin/python3`); the function degrades to `[]` if missing.
Algorithm:

1. For each `Figure N` caption block, the figure region = union of image +
   vector-drawing blocks above the caption within its column (bounded below by
   the nearest body-text block, so prose isn't swallowed).
2. Render that region to a width-capped (600px) **JPEG data URL** — PDFs have no
   hostable image URL.
3. **Low-content filter** (`_pixmap_is_low_content`): skip near-uniform crops —
   a bad bounding box renders mostly one color. The signal is *distinct colors*,
   NOT the dominant fraction: real architecture diagrams are >85% white yet have
   many box/text/icon colors, so the test is `dominant ≥ 0.97 OR ≤4 significant
   colors` (a blank heatmap fragment fails; a sparse diagram passes).
4. **Dynamic size budget**: data URLs count toward the 100k limit, so
   `insert_figures_into_card` passes `char_budget = 96000 − current_card_size`
   and inserts nothing if the card is already near-full (e.g. a long Technical
   Report at ~99k leaves no room).

Known limits: full-width / multi-panel figures whose layout defeats the
column-bounding heuristic yield 0 (acceptable — recorded for no retry benefit);
table-only papers correctly yield 0.

**Select 2–4 figures per paper:**
- Architecture/overview diagram → place after the method section heading
- Key results chart or evaluation figure → place after the results heading
- Skip logos, decorative icons, or figures with no caption

**Image candidate cap:** Pass at most 6 images to `translate_content` (first 6 from `fetch_arxiv_images`).
Papers with many figures (e.g. GPT-3 has 29) will cause the translation prompt to timeout otherwise.
Claude selects the best 2–4 from the candidates.

**CRITICAL — `translate_content` only embeds http(s)-URL figures.** It omits
`data:` URLs from the placement prompt (an inline base64 image is far too long
to put in a prompt). So when `fetch_arxiv_images` returns **inline-SVG figures**
(converted to PNG `data:` URLs), translate embeds *none* of them — and because
the fetched `images` list is non-empty, the old post-create guard `if not
images:` wrongly concluded "figures present" and skipped the retrofit/record.
Net effect: SVG-only papers silently ended up with **zero figures** (observed:
"From Self-Supervised Speech Models to MoE for Robust Anti-Spoofing", 2606.14639).

Fix: after card creation, decide by the card's **actual** image count
(`card_has_images()`), NOT the fetched list. If zero, `insert_figures_into_card`
retrofits using its caption-based placement path (which CAN insert `data:` URLs),
with this **source priority** (it also handles the 100k budget — see Step 5a.2):
1. hosted **http(s) PNG/JPG** from HTML — best, ~no size cost
2. **PDF-rendered JPEG** — compact; preferred over SVG (a 58k SVG-PNG of a key
   figure may not fit the budget, while the same figure is ~25k as a PDF JPEG)
3. **inline-SVG `data:` URL** — last resort, only those that fit the budget

### 5b — Identify Exact Heading Texts for Image Placement

**CRITICAL:** Heading node text in Heptabase ProseMirror JSON does **not**
include `#` prefix characters. The heading text is the bare string, e.g.
`"4. 研究方法"` not `"## 4. 研究方法"`.

First inspect the actual heading texts in the card:

```bash
heptabase note read $CARD_ID | python3 -c "
import json, sys
data = json.load(sys.stdin)
doc = json.loads(data['content'])
for node in doc['content']:
    if node.get('type') == 'heading':
        text = ''.join(c.get('text','') for c in node.get('content',[]) if c.get('type')=='text')
        print(repr(text))
"
```

Use **exact equality** (`==`) when matching heading text, not substring
`in`. The card headings follow the 6-section template:
`"4. 研究方法"`, `"4.1 ..."`, `"5. 主要發現與結果"`, etc.

### 5c — Color Strategy

| Color  | Apply to |
|--------|----------|
| 🔴 red | Bad baseline numbers, failure modes, named limitations (low accuracy, high error rate, identified problems) |
| 🟡 yellow | Paper's own key names: model, benchmark, method, central technical terms |
| 🟢 green | Improvements, gains, SOTA scores, best results |

**In run.py (automated):** Color rules are generated automatically by calling
`claude --print` with the card content and asking Claude to return a JSON list
of `[text_span, color]` pairs. No manual `COLOR_RULES` needed.

**In interactive skill:** Fill in `COLOR_RULES` manually after reviewing the
translated card, or ask Claude to suggest rules based on the content.

### 5d — Combined Python Script

```python
import json, re, copy, subprocess

CARD_ID = "<id from Step 4>"

# --- For interactive use: fill these in manually ---
# In run.py, COLOR_RULES are auto-generated via Claude
COLOR_RULES = [
    # (exact_substring, "red" | "yellow" | "green")
]
IMAGES = [
    # (exact_heading_text, full_image_url, chinese_caption)
    # heading_text must == actual heading (no ## prefix)
]
# ---------------------------------------------------

def make_color_mark(color):
    return {"type": "color", "attrs": {"type": "text", "color": color}}

def get_node_text(node):
    if node.get("type") == "text":
        return node.get("text", "")
    return "".join(get_node_text(c) for c in node.get("content", []))

def colorize_text_node(node, rules):
    text = node.get("text", "")
    marks = node.get("marks", [])
    hits = []
    for pattern, color in rules:
        for m in re.finditer(re.escape(pattern), text):
            hits.append((m.start(), m.end(), color))
    if not hits:
        return [node]
    hits.sort(key=lambda x: x[0])
    clean, last = [], 0
    for s, e, c in hits:
        if s >= last:
            clean.append((s, e, c)); last = e
    result, pos = [], 0
    for s, e, c in clean:
        if pos < s:
            n = {"type": "text", "text": text[pos:s]}
            if marks: n["marks"] = list(marks)
            result.append(n)
        result.append({"type": "text", "text": text[s:e],
                       "marks": list(marks) + [make_color_mark(c)]})
        pos = e
    if pos < len(text):
        n = {"type": "text", "text": text[pos:]}
        if marks: n["marks"] = list(marks)
        result.append(n)
    return result

def process_nodes(nodes, rules):
    result = []
    for node in nodes:
        if node.get("type") == "text":
            result.extend(colorize_text_node(node, rules))
        else:
            new = copy.deepcopy(node)
            if "content" in new:
                new["content"] = process_nodes(new["content"], rules)
            result.append(new)
    return result

def insert_images(nodes, images):
    """
    images: list of {"src": url_or_data_url, "caption": str}
    Use image_N placeholders when calling Claude for placement to avoid
    sending data URLs in the prompt (too long). Example prompt:

      image_1: Figure 1: Architecture overview of ...
      image_2: Figure 2: Comparison results on ...

    Then map image_N back to real src before calling this function.
    Always insert a caption paragraph (italic) after each image node.
    """
    # Build placement_map: {heading_text: [src, ...]}
    # (from Claude's JSON: [{"src": "image_N", "after_heading": "..."}])
    # after resolving image_N → real src
    placement_map = {}
    for p in images:
        placement_map.setdefault(p["after_heading"], []).append(p["src"])

    result = []
    for node in nodes:
        result.append(node)
        if node.get("type") == "heading":
            heading_text = get_node_text(node)
            for src in placement_map.get(heading_text, []):
                caption_text = next(
                    (img["caption"] for img in images if img.get("src") == src), "")
                result.append({"type": "image",
                               "attrs": {"id": None, "src": src, "alignment": "center"}})
                if caption_text:
                    result.append({"type": "paragraph", "attrs": {"id": None},
                                   "content": [{"type": "text",
                                                "marks": [{"type": "em"}],
                                                "text": caption_text}]})
    return result

# Read
raw = subprocess.run(["heptabase", "note", "read", CARD_ID],
                     capture_output=True, text=True)
data = json.loads(raw.stdout)
md5 = data["contentMd5"]
doc = json.loads(data["content"])

# Apply colors then insert images
doc["content"] = process_nodes(doc["content"], COLOR_RULES)
doc["content"] = insert_images(doc["content"], IMAGES)

# Save — use --content-file to avoid 100K char limit with data URL images
import tempfile, os
content_str = json.dumps(doc, ensure_ascii=False)
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    f.write(content_str); tmp = f.name
subprocess.run(["heptabase", "note", "save", CARD_ID,
                "--content-md5", md5, "--content-file", tmp], check=True)
os.unlink(tmp)
print("Done")
```

---

## Step 6 — Tag Card and Set Source Type Property

After colorization and figure insertion, apply the `study/paper` tag and set
the `Source Type` property to `"alphaXiv"` for every newly created card:

```bash
# Add study/paper tag
heptabase tag add --card-id "$CARD_ID" --tag-name "study/paper"

# Set Source Type property
heptabase card set-property "$CARD_ID" \
  --property-id $(config heptabase.props.source_type) \
  --value "alphaXiv"
```

**Property IDs:**
- `Source Type` (select): `$(config heptabase.props.source_type)`
- `arxiv ID` (text): `$(config heptabase.props.arxiv)`

---

## Step 6.5 — Auto-annotate `Tasks` + auto-sync overview cards

Every new card gets its `Tasks` property annotated automatically, and if any
assigned Task owns a comparison-overview card, that overview is re-synced.

### 6.5a — Classify the paper into existing `Tasks` options (ADDITIVE)

**You (Claude) pick the tags by reading the paper** — this needs semantic
judgment, so it lives here, not in the scripted loop. Use the just-translated card
content (title + 快速摘要 + the 6 sections) plus the taxonomy card
*「Speech / Audio / Spoken Language Model 的術語與分類（2023–2025 文獻）」* as the
rubric. Two kinds of tag, both additive:
- a **primary task** (e.g. `TTS`, `Voice Conversion`, `ASR`, `Tokenizer/Codec/Representation`, `Duplex S2S`, `Spoken Dialog`, …)
- any **cross-cutting axis** that clearly applies (`Discrete Tokens` / `Continuous Features`,
  `End-to-End`, `Audio LM`, …)

Rules:
- **Additive only** — `set_tasks()` unions with whatever is already there and
  **never removes** an existing tag.
- **Pick only from existing options.** The CLI cannot create new `Tasks`
  options ("Unknown option" error); `set_tasks()` silently drops + logs unknown
  values. If a paper genuinely needs a brand-new task type, tell the user to
  create it in the Heptabase UI first, then re-run.
- A paper with no speech/audio task (off-topic) gets **no** Tasks — leave empty.
- **Every card also gets `Topics`**（`set_topics()`，config `props.topics`）——
  非語音的主軸分類（如 `LLM / Foundation Model`、`Agentic AI`、
  `Diffusion / Flow Matching`）。off-topic 卡 Tasks 留空但 **Topics 必挑**
  （0–2 個、只從既有選項；真的無一適用才留空並回報）；語音卡也可掛交叉軸
  （例：diffusion TTS → Topics 加 `Diffusion / Flow Matching`）。Topics
  **不**參與總覽路由——那是 Tasks 的職責。

```python
import sys, os; sys.path.insert(0, os.environ.get("CLAUDE_PLUGIN_ROOT", os.path.expanduser("~/.claude/skills/research-cards")) + "/skills/scholar-inbox-clip")
import run as R
# print(sorted(R.valid_task_options()))   # the current options, for reference
applied = R.set_tasks(CARD_ID, ["Tokenizer/Codec/Representation", "Discrete Tokens"])  # additive
R.set_topics(CARD_ID, ["Diffusion / Flow Matching"])   # 主軸分類（additive，同語義）
overviews = R.overviews_to_sync(applied)   # → ['tokenizer-codec-overview'] (or [] / both)
```

### 6.5b — Auto-sync the owning overview card(s)

All comparison overviews are maintained by the single **`/research-cards:overview`**
skill — `overviews_to_sync(applied)` returns its **TOPIC KEY(s)** to run, driven
by `OVERVIEW_TASKS` in `run.py`:

| if `Tasks` contains | topic key |
|---------------------|-----------|
| `Duplex S2S` | `duplex` |
| `Tokenizer/Codec/Representation` | `tokenizer` |
| `Spoken LM` / `Speech LLM` | `spoken` |
| `Audio Understanding` / `Reasoning` / `Audio LM` | `auditory`（nested under `spoken`） |
| `TTS` / `Instructed TTS` / `Speech Editing` / `Voice Conversion` / `Singing Voice Synthesis` / `Text-to-Sound` / `Text-to-Music` | `speech-generation` |
| `ASR` | `asr` |
| `Anti-Spoofing` / `Speaker Verification` / `Speech Enhancement` / `Target Speech Extraction` | `frontend-security` |

（single source of truth = `OVERVIEW_TASKS` in `run.py` — 上表若與程式不符，以程式為準並回頭修這張表。）

For each returned topic key, **invoke the `overview` skill with that topic** (it runs `status` → authors a section for
the now-missing new paper → updates its tables/synthesis bullets → `sort`). If
both tasks were applied, invoke both. `overviews_to_sync()` is empty only
for genuinely unowned values (e.g. `MLLM`, `MOS / Perceptual Quality`, `S2ST`,
`Spoken Dialog`) — a pure `TTS`/`Voice Conversion` paper DOES route (→ topic
`speech-generation`). Collect all newly-tagged cards across the email batch
and sync each affected topic **once at the end**, not per-card.

---

## Step 7 — Link Cards to Today's Journal

After all cards are created and colorized, write a journal entry where each
card is a **`toggle_list_item`**: the label is the card mention, and the
nested content is the AI 摘要 paragraph. This lets the journal serve as a
scannable digest.

Use `journal read` + `journal save` (not `journal append`) so the entry can
be constructed as proper ProseMirror JSON with toggle nodes:

```python
import json, subprocess
from datetime import date

def make_card_toggle(card_id, ai_summary_text):
    return {
        "type": "toggle_list_item",
        "attrs": {"id": None, "folded": True},
        "content": [
            {
                "type": "paragraph",
                "attrs": {"id": None},
                "content": [{"type": "card", "attrs": {"cardId": card_id}}]
            },
            {
                "type": "paragraph",
                "attrs": {"id": None},
                "content": [{"type": "text", "text": ai_summary_text}]
            }
        ]
    }

today = date.today().isoformat()
raw = subprocess.run(["heptabase", "journal", "read", today],
                     capture_output=True, text=True)
data = json.loads(raw.stdout)
md5 = data["contentMd5"]
doc = json.loads(data["content"])

# Append a heading + one toggle per card. The heading shows the email's
# RECEIVED date (recv_date), not today's processing date — so repeated
# same-subject emails ("Trending Papers + Weekly Seminar") stay distinguishable.
heading = {"type": "heading", "attrs": {"level": 2, "id": None},
           "content": [{"type": "text",
                        "text": f"Scholar Inbox — {email_subject}（{recv_date}）"}]}
toggles = [make_card_toggle(cid, ai_summaries[cid]) for cid in card_ids]
doc["content"].extend([heading] + toggles)

import tempfile, os
content_str = json.dumps(doc, ensure_ascii=False)
with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
    f.write(content_str); tmp = f.name
subprocess.run(["heptabase", "journal", "save", today,
                "--content-md5", md5, "--content-file", tmp], check=True)
os.unlink(tmp)
```

The `ai_summaries` dict maps card ID → the AI 摘要 text generated in
Step 4.5. Use `folded: True` so the journal stays compact by default.

---

## Step 7.5 — Set arxiv ID Property

Every newly created card should have its arxiv ID set as a structured property.
This enables filtering, sorting, and lookup by paper ID directly within Heptabase.

**arxiv ID property ID:** `$(config heptabase.props.arxiv)` (type: text)

### Set the property for a single card:

```bash
heptabase card set-property "$CARD_ID" \
  --property-id $(config heptabase.props.arxiv) \
  --value "2605.27772"
```

### Batch set for multiple new cards:

```python
import subprocess

ARXIV_PROP_ID      = "$(config heptabase.props.arxiv)"
SOURCE_TYPE_PROP_ID = "$(config heptabase.props.source_type)"

# arxiv_id_map: dict of card_id -> arxiv_id
# For OpenReview papers (no arxiv ID), use "openreview:{id}" format
arxiv_id_map = {
    "59aeef84-...": "2506.00885",
    "e8ab0f7e-...": "openreview:JbLmIoWwDC",
}

for card_id, arxiv_id in arxiv_id_map.items():
    subprocess.run(["heptabase", "tag", "add",
                    "--card-id", card_id, "--tag-name", "study/paper"], check=True)
    subprocess.run(["heptabase", "card", "set-property", card_id,
                    "--property-id", SOURCE_TYPE_PROP_ID, "--value", "alphaXiv"], check=True)
    subprocess.run(["heptabase", "card", "set-property", card_id,
                    "--property-id", ARXIV_PROP_ID, "--value", arxiv_id], check=True)
```

### Verify the properties were set:

```bash
heptabase card properties "$CARD_ID"
# Returns tags with properties including Source Type: alphaXiv, arxiv ID: XXXX.XXXXX
```

---

## Step 7.6 — Append arxiv HTML Link

After setting properties, append a clickable `原文 HTML` link paragraph at the
bottom of every alphaXiv card. This provides a one-click path to the full
paper for formula details, bilingual term lookup, and original context.

**Link format (ProseMirror):**

```python
def append_arxiv_html_link(card_id, arxiv_id):
    if arxiv_id.startswith("openreview:"):
        return  # No arxiv HTML page for OpenReview papers
    url = f"https://arxiv.org/html/{arxiv_id}"
    md5, doc = read_card(card_id)
    # Idempotent: skip if link already present
    for node in doc["content"][-5:]:
        for inline in node.get("content", []):
            for mark in inline.get("marks", []):
                if mark.get("type") == "link" and url in mark.get("attrs", {}).get("href", ""):
                    return
    doc["content"].append({
        "type": "paragraph",
        "attrs": {"id": None},
        "content": [
            {"type": "text", "text": "原文 HTML："},
            {
                "type": "text",
                "marks": [{"type": "link", "attrs": {
                    "href": url,
                    "title": None,
                    "data-internal-href": None,
                    "edited": False,
                }}],
                "text": url,
            },
        ],
    })
    save_card(card_id, md5, doc)
```

**Result:** Each card ends with a clickable `原文 HTML：https://arxiv.org/html/{arxiv_id}` line below the `Source: alphaxiv.org/...` paragraph.

**Batch backfill** (for existing cards): run `/tmp/add_arxiv_html_links.py`.

---

## Automated Execution

Scheduling is a **Claude Code desktop-app routine** that invokes this skill's
email-clip mode — with a model in the loop, so the run does the FULL chain in
one pass: clip → Step 6.5 tagging → overview sync (→ 導讀 refresh → graph
audit, per the `overview` skill's workflow). The pipeline is idempotent
(subject|recv_date dedup + per-paper check_duplicate), so most runs are cheap
no-ops — only runs where a new email has arrived create cards.

**Routine closing step — hung-yi-lee graph freshness:** end every routine run
with

```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/overview-graph/scripts/hungyi_query.py --refresh-only
```

It refreshes the LECTURE side (sync-metadata / sync-transcripts / tracked
graph build — TTL-throttled to once per 24h) and then the card corpus
(incremental). If it reports the lecture data was refreshed, the hung-yi-lee
fork tree has regenerated tracked files — **commit the fork + bump the
submodule pointer in the same routine run** (data-only diff; per the push
rules that may go out directly). Interactive queries stay fast because
lecture sync lives HERE, not in query mode (see overview-graph Operation 4).

（History: 2026-07-05 之前由兩個 launchd agents 排程——`com.<user>.scholar-
inbox-clip` 每 3 小時跑純腳本 `run.py`（無 model、不標 Tasks，因此才需要 backfill
每日提醒 `com.<user>.scholar-backfill-report`）。兩個 plist 已於 2026-07-05
卸載刪除，`--backfill-report` 功能同日自 run.py 移除。）

**Script:** `${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/scholar-inbox-clip/run.py`  
**Logs:** `~/Library/Logs/Claude/research-cards:scholar-inbox-clip.log` (stdout)  
         `~/Library/Logs/Claude/research-cards:scholar-inbox-clip-error.log` (stderr)  
**State:** `~/.config/research-cards/scholar_inbox_state.json（既有安裝若 ~/.claude/scholar_inbox_state.json 存在則沿用 legacy 路徑）` — stores the last 50 processed
           **`"{subject}|{recv_date}"`** dedup keys (NOT bare subjects — same
           subject recurs on different dates). `message 1` is newest, so when
           rebuilding state keep the FIRST N keys, not the last N.  
**No-image record:** `~/.config/research-cards/scholar_inbox_no_images.json（legacy：~/.claude/ 同名檔優先）` — cards created
           without figures `[{card_id, arxiv_id, title, last_checked}]`. Each run
           retries the arxiv-ID entries via `insert_figures_into_card` (HTML →
           ar5iv → **PDF render fallback**) and drops an entry once a figure is
           inserted. Stays pending when: the paper truly has no figures
           (table-only), the card is already near the 100k limit (no room), the
           figure layout defeats the PDF heuristic, or the entry is non-arxiv
           (alphaxiv:/openreview:/aclanthology: — no arxiv source at all).

The Python script bypasses interactive tool approvals (避免無人值守跳權限提示).
For Codex, alphaXiv text retrieval uses the app-server's direct MCP call with an
ephemeral read-only thread; image retrieval remains direct arxiv/ar5iv/PDF HTTPS
because the alphaXiv text tool does not provide figure assets. The configured
agent CLI is invoked only for text→text tasks (translation, summary, colorize,
image placement).

**Minimal-PATH gotcha:** a non-login-shell run can get a minimal PATH
(`/usr/bin:/bin:/usr/sbin:/sbin`) that omits Homebrew, so a bare `heptabase`
(in `/opt/homebrew/bin`) fails with `No such file or directory: 'heptabase'` —
and the failure is silent unless there are new papers to clip (a no-new-email
run only touches heptabase in the figure-retry step, whose errors are caught).
`run.py` guards against this by prepending `/opt/homebrew/bin:/usr/local/bin` to
`os.environ["PATH"]` at import. It also resolves `claude`, `codex`, and
`rsvg-convert` to absolute paths. On Mac, `codex` deliberately prefers the
current ChatGPT Desktop app bundle before `PATH`: a stale npm CLI can reject a
model already configured by the newer app. Set `SCHOLAR_CLIP_CODEX_BIN` only
for an explicit nonstandard/debug override; non-Mac resolution falls back to
`PATH`, `~/.local/bin`, then `~/.node_modules/bin`. Only `heptabase` remains
bare after the PATH repair. Verify with:
`env -i HOME=$HOME PATH=/usr/bin:/bin /usr/bin/python3 -c "import run, subprocess; print(subprocess.run(['heptabase','--version']).returncode)"`

Pipeline order in `run.py`:
1. Scan newest MAX_SCAN (40) emails (index 1 = newest), until OUT_OF_RANGE
2. Skip already-processed `subject|recv_date` keys (no early stop — see Step 1)
3. For each email: extract arxiv IDs (HTML alphaxiv pattern → arxiv API → Claude fallback)
4. For each paper: fetch alphaXiv overview → fetch arxiv HTML images
5. Translate with images embedded (Claude auto-places figures by caption)
6. Create card (`heptabase note create`)
7. Insert quick summary block
8. Auto-colorize (Claude returns JSON color rules)
9. Add study/paper tag + set Source Type: alphaXiv + set arxiv ID property
9b. **(model-in-the-loop runs — interactive OR desktop routine)** Auto-annotate
    `Tasks` via `set_tasks()` AND `Topics` via `set_topics()`（additive;
    existing options only；off-topic 卡 Tasks 留空但 Topics 必填）and re-sync
    any owning overview topic returned by `overviews_to_sync()` — see Step 6.5. The
    bare scripted `run.py` main loop does NOT do this (it has no semantic
    judgment and the overview workflows are Claude-driven); the helpers live in
    `run.py` so the model-driven flow can call them.
10. Append arxiv HTML link to card bottom
11. If no figures were found, record the card in the no-image record
12. Append to today's journal with h2 heading per email source (received date)
13. **After all emails:** `retry_no_image_cards()` — re-fetch figures for
    previously image-less cards and insert any now available (`insert_figures_into_card`)

To run manually:
```bash
python3 ${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/research-cards}/skills/scholar-inbox-clip/run.py
```

To force reprocess (clear duplicate guard):
```bash
echo '{}' > ~/.config/research-cards/scholar_inbox_state.json（既有安裝若 ~/.claude/scholar_inbox_state.json 存在則沿用 legacy 路徑）
```

---

## Step 8 — Confirm and Report

After all cards are created and linked, report:
- How many cards were created
- Card titles and IDs
- Which papers used AI report vs. raw paper fallback
- Which papers used arxiv figure fallback (no AI overview yet)
- Any papers that failed (with reason)

---

## Important Notes

- **Duplicate detection**: Before creating a card, search Heptabase for an
  existing card with the same ID in its Source link:
  ```bash
  heptabase card list -q "{bare_id}" --limit 5
  ```
  **But free-text search gives FALSE POSITIVES for named slugs** — e.g.
  `deepseek-v4` matches any card that merely *mentions* DeepSeek-V4 in its body,
  not just the DeepSeek-V4 paper's own card. So after the search, confirm a
  candidate is genuinely this paper: read each hit and require the ID to appear
  inside a paper URL (`/overview/{id}`, `/abs/{id}`, `/html/{id}`). `run.py`'s
  `check_duplicate()` does this. (Numeric arxiv IDs rarely collide; slugs do.)

- **Verify fetched content matches the paper**: `alphaxiv.org/overview/{id}`
  for a paper with **no generated overview** silently returns a generic
  *fallback/featured* page (e.g. "Cosmos 3"). Before creating a card, check the
  fetched `<title>` actually contains the expected paper title — otherwise you
  create a card with the wrong paper's content.

- **alphaXiv overview generation**: Some papers may not yet have a generated
  overview. The first time `get_paper_content` is called for such a paper it
  returns raw text. After the user manually visits and generates the overview
  on alphaxiv.org, a subsequent call will return the structured report. The
  skill should note which papers used the fallback and suggest the user visit
  the alphaXiv page to generate the overview for future runs.

- **Language**: All card content must be in the **configured output language** —
  config `profile.language`; when unset, Claude Code's `language` setting
  (mapped, e.g. chinese→繁體中文); default Traditional Chinese (繁體中文).
  run.py resolves this via `hbconfig.output_language()`; agent-driven
  (interactive) runs MUST follow the same resolution. Everything is written
  in that language, except for model names, benchmark names, and quoted
  metric values which stay in their original form.

- **Card title format**: Always `[alphaXiv] {Original English Paper Title}`
  (title stays in English, matching the alphaXiv convention).
