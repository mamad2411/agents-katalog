---
name: book-to-skill
description: >-
  Converts books and documents (PDF, EPUB, DOCX, HTML, Markdown, plain text,
  RTF, MOBI/AZW) into structured agent skills, extracting frameworks, mental
  models, principles, techniques, and anti-patterns. Use when the user wants to
  study a document through an agent, apply an author's frameworks while
  working, or build a reusable knowledge base from a file.
license: MIT
metadata:
  version: "1.0"
  source: virgiliojr94/book-to-skill (MIT)
  port: >-
    Clean methodology-only port. Upstream blocked by SkillSpector (CRITICAL,
    100/100) due to bundled Python extraction scripts (subprocess calls, dynamic
    imports) and root/privilege references in docs. This port keeps the full
    prose workflow but replaces the bundled extract.py with the bundle's existing
    `markitdown` CLI/MCP for text extraction. No scripts, no deps.
  relates: markitdown
---

# Book-to-Skill Converter

Transform written knowledge into actionable agent skills by extracting structure — not producing summaries.

## Philosophy

Books contain crystallized expertise: frameworks, principles, and techniques that took years to develop. This skill extracts that knowledge into a format an agent can leverage repeatedly.

**Extract structure, not summaries.** A skill isn't a book report. It's a toolkit of:
- Named frameworks (mental models with clear application)
- Actionable principles (rules that guide decisions)
- Techniques (step-by-step methods)
- Anti-patterns (what to avoid and why)
- Voice calibration (how the author thinks and communicates)

**Preserve the author's precision.** Frameworks often have specific names for reasons. "The 5 Whys" isn't interchangeable with "ask why multiple times." Capture the exact formulation.

**Layer depth appropriately.** Simple books → simple skills. Complex books with 10+ frameworks → skills with reference files and on-demand chapters.

---

## Modes of Operation

Four paths available. Route based on what the user asks:

### 1. Full Conversion (Default)
**Trigger:** User provides one or more document/directory/glob paths without special instructions
**Action:** Run all steps below (Steps 0–9)
**Output:** Complete skill with SKILL.md, chapters/, glossary, patterns, cheatsheet

### 2. Analyze Only
**Trigger:** User says "analyze", "just extract", or "I want to review before generating"
**Action:** Run Steps 0–3, then produce a structured extraction report. Stop — do NOT generate skill files.
**Output:** Analysis report for user review

### 3. Generate from Prior Analysis
**Trigger:** User has existing analysis notes or previously ran analyze-only
**Action:** Skip Steps 0–3, use the provided analysis as input, run Steps 4–9
**Output:** Skill files from the provided analysis

### 4. Update / Fold-in (Existing Skill)
**Trigger:** User provides new source paths and indicates they want to update an existing skill
**Action:** Run Step 0 (out-of-scope check), Step 1 (validate inputs), Step 1.5 (identify book type), and Step 2 (extract). Then run the **Update / Fold-in Workflow** to merge the new content into the existing skill files.

---

## Skill Locations

When writing the generated book skill, prefer these locations in order:
1. `~/.agents/skills/` (cross-agent personal skills)
2. `~/.copilot/skills/` (Copilot CLI personal skills)
3. `~/.claude/skills/` (Claude Code personal skills)
4. Project-local `.agents/skills/` or `.claude/skills/`

When more than one valid root exists, ask the user once and remember the answer for the session — do not silently default.

---

## Step 0 — Out-of-scope check

If no arguments are provided, stop and respond:
> "book-to-skill requires a supported document path, folder, or glob pattern. Usage: `book-to-skill <path-to-document-folder-or-glob>... [skill-name-slug]`"

- Identify the input paths and the optional skill slug.
- If the last argument is not a file/folder/glob that exists, and it looks like a skill slug (lowercase hyphens, alphanumeric), treat it as `SKILL_NAME`.
- Treat all other arguments as `INPUT_PATHS`.
- If any input path is an existing skill directory (contains `SKILL.md` and `chapters/`), or `SKILL_NAME` matches an existing skill slug, flag as **Update/Fold-in** (Mode 4).

---

## Step 1 — Validate input

Verify at least one supported file, directory, or glob pattern among `INPUT_PATHS`. Expand directories and globs to find supported files (`.pdf`, `.epub`, `.docx`, `.txt`, `.md`, `.markdown`, `.rst`, `.adoc`, `.html`, `.htm`, `.rtf`, `.mobi`, `.azw`, `.azw3`).

If no supported files are found, stop with a clear error message.

---

## Step 1.5 — Identify content type

Before extracting, ask the user:

> "What kind of content do these sources have?
> 1. **Technical** — has code blocks, tables, formulas, diagrams
> 2. **Text-heavy** — mostly prose, few or no tables/code
> 3. **Not sure** — I'll use the fast method and warn you if quality seems limited"

Store the answer as `BOOK_TYPE` (1→technical, 2→text, 3→text).

---

## Step 2 — Extract text from the source documents

**Use the bundle's `markitdown` tool** to convert each source to Markdown. `markitdown` handles PDF, EPUB, DOCX, HTML, RTF, and plain text with no OCR needed for text-based files.

```bash
# For each input path, convert to Markdown:
markitdown <input-path> -o <tempdir>/book_skill_work/<slug>.md
```

For `.mobi`/`.azw` (Kindle formats), note that markitdown may not handle them directly — ask the user to convert to EPUB first, or extract with a standard tool.

Combine the per-file outputs into `<tempdir>/book_skill_work/full_text.txt` with clear visually demarcated boundaries between sources.

Also write `<tempdir>/book_skill_work/metadata.json` recording: combined size, words, pages, token counts, and a detailed list of processed sources.

---

## Step 2.5 — Pre-flight cost estimate

Read `metadata.json` and present the user with an estimate **before doing any generation**:

```
📖 Sources detected: <N> source(s)
📄 Combined Pages/Sections: ~<N> | Words: ~<N> | Total tokens: ~<N>K

💰 Estimated token cost (Full Conversion / Update):
   Input  (reading + prompts): ~<N>K tokens
   Output (skill files generated):  ~<N>K tokens
   Total: ~<N>K tokens

   Cost: multiply the token counts by your model's current per-1M-token rates.
   (Prices change often — quote today's rate and label it as an estimate.)

⏱  Estimated time: ~<N> minutes

📁 Files to be generated: SKILL.md + chapter files + glossary + patterns + cheatsheet

➡  Proceed with Full Conversion / Update? (or type "analyze only" to preview first)
```

**How to estimate:**
- Input tokens ≈ `estimated_tokens` from metadata × 1.3 (prompt overhead per chapter pass)
- Output tokens ≈ chapters × per-chapter budget + 4,000 (SKILL.md) + 4,500 (glossary + patterns + cheatsheet)
- Per-chapter budget midpoint by `BOOK_TYPE`: `text` ≈ 1,000, `technical` ≈ 1,800.

Wait for the user to confirm before proceeding. If they say "analyze only", switch to Mode 2.

---

## Step 2.6 — REPL-style access for large books (> 50k tokens)

For books over ~50k tokens, treat `full_text.txt` as a queryable corpus, not a single read. Prefer programmatic probes over unbounded reads:
- Size check before any read
- Find chapter offsets via grep without loading the whole file
- Pull only the chapter you need via line ranges
- Verify a framework is actually mentioned before claiming it in SKILL.md

On books under 50k tokens, a single read is fine.

Why this matters: a 200-page book is ~75k tokens. Re-reading it once per chapter (28 passes) costs ~2M input tokens; pulling only relevant slices keeps generation cost proportional to the output, not the source.

---

## Step 3 — Analyze book structure

Read the first ~8,000 characters of `full_text.txt` to identify:
- Book **title** and **author(s)**
- **Chapter structure** (look for "Chapter N", "PART I", numbered headings, table of contents)
- **Core themes** and subject domain
- Approximate number of chapters

**If mode is "Analyze Only":** produce the extraction report now and stop:

```
## Extraction Report — <Title>
### Author's Core Frameworks
- **<Framework Name>**: <what it is and when to apply>
### Key Principles
- <Principle>: <actionable rule>
### Techniques & Methods
- <Technique>: <step-by-step or how-to>
### Anti-patterns
- <What to avoid>: <why>
### Suggested Skill Name
`{author-lastname}-{core-concept}` — e.g. `cialdini-influence`
### Chapters Detected
| # | Title | Main Frameworks |
```

---

## Step 4 — Ask purpose (Full Conversion only)

Before generating, ask:

> "What should this skill help you do? (Pick one or more)
> 1. Apply the author's frameworks while working
> 2. Think with the author's mental models
> 3. Reference specific chapters and concepts
> 4. All of the above"

**Derive `DEPTH` from the answer:**
- Only option 3 → `DEPTH=reference` — lean, fast-lookup chapters
- Includes 1, 2, or 4 → `DEPTH=study` — deeper chapters with worked detail

(In Modes 2/3, default `DEPTH=study`.)

---

## Step 5 — Determine skill name

If `SKILL_NAME` was provided, use it as the skill slug. Otherwise propose two options:
- **By author-concept**: `{author-lastname}-{core-concept}` (e.g. `cialdini-influence`, `meadows-systems`)
- **By title**: lowercase hyphens (e.g. `designing-data-intensive-apps`)

Default to author-concept if the book has a strong methodological identity.

Choose the destination skill root (`SKILLS_HOME`). Probe the filesystem for existing skill homes and pick by **the host the user is running in** (Copilot → `~/.agents/skills` / `~/.copilot/skills`; Claude → `~/.claude/skills`).

Selection rules:
1. If exactly one of the host's candidate roots exists, use it without asking.
2. If none exist, ask which root to create — present host-appropriate options.
3. If the user asked for project-local output, prefer the project-local root.
4. If you cannot identify the host, ask.

If `$SKILLS_HOME/<skill_name>/` already exists, prompt: Update / Fold-in (Mode 4), Overwrite, or Rename.

---

## Step 6 — Create skill directory structure

Create `$SKILLS_HOME/<skill_name>/chapters` (and the supporting-file directory).

---

## Step 7 — Generate chapter summaries

**TOKEN BUDGET RULE — CRITICAL (adaptive):**

| | `DEPTH=reference` | `DEPTH=study` |
|---|---|---|
| `BOOK_TYPE=text` | 800–1,200 tokens | 1,000–1,800 tokens |
| `BOOK_TYPE=technical` | 1,200–1,800 tokens | 2,000–3,000 tokens |

- These are per-file targets, not hard caps. Density beats length — never pad.
- Files are loaded on-demand, so a larger chapter only costs tokens when read.
- `DEPTH=study` is earned with content: reproduce a worked example, expand the "How" of each framework, add a "Why it works / failure mode" note — not by padding.

For EACH chapter/section identified in Step 3:
- Read the corresponding section of `full_text.txt`.
- Create `chapters/ch<NN>-<slug>.md` using this structure:

```markdown
# Chapter N: <Full Title>

## Core Idea
<1–2 sentences>

## Frameworks Introduced
- **<Framework Name>**: <exact formulation — preserve the author's naming>
  - When to use: <specific situation>
  - How: <steps or criteria>

## Key Concepts
- **<Term>**: <precise definition in 1 sentence>

## Mental Models
<2–4 thinking tools: "Use X when Y" or "Think of X as Y">

## Anti-patterns
- **<What to avoid>**: <why it fails>

## Code Examples *(technical books only)*
<key code example, indentation preserved>

## Reference Tables *(technical books only)*
<comparison/parameter/decision tables as markdown>

## Worked Example *(DEPTH=study only)*
<one concrete example the author walks through, reconstructed compactly>

## Key Takeaways
1. <Actionable insight>
2. <Actionable insight>
3. <Actionable insight>

## Connects To
- **Ch N**: <why this chapter relates>
- **<Concept>**: <external concept or standard>
```

---

## Step 8 — Generate supporting files

### glossary.md
- Every significant term, alphabetically sorted
- Format: `**Term** — definition (Ch N)`
- Max 1,500 tokens

### patterns.md
- All concrete techniques, design patterns, algorithms
- Format: `## Pattern Name\n**When to use**: ...\n**How**: ...\n**Trade-offs**: ...`
- Max 2,000 tokens

### cheatsheet.md
**The most differentiated layer — a reasoning aid, not a keyword list.** Capture the author's *judgment*: the decisions they'd make and why.

Prioritize, in order:
1. **Decision rules** — "When X, do Y, because Z."
2. **Decision trees** — for choices with more than two branches
3. **Trade-off matrices** — competing options scored on the dimensions the author cares about
4. **Thresholds & defaults** — the specific numbers/rules of thumb the author commits to
5. **Tells & smells** — fast heuristics ("if you see X, you're probably in trouble Y")

Avoid bare term→definition rows (that's the glossary) and prose (that's the chapters). Max 1,200 tokens.

---

## Step 9 — Generate the master SKILL.md

**CRITICAL TOKEN BUDGET: Keep SKILL.md body under 4,000 tokens.** Compaction truncates from the END — put the most important content FIRST.

```markdown
---
name: <skill_name>
description: "Knowledge base from \"<Full Title>\" by <Author(s)>. Use when applying <author>'s frameworks for <key topics>, studying the book, or referencing its concepts."
---

# <Full Title>
**Author**: <Author(s)> | **Pages**: ~<N> | **Chapters**: <N> | **Generated**: <YYYY-MM-DD>

## How to Use This Skill
- **Without arguments** — load core frameworks for reference
- **With a topic** — find and read the relevant chapter
- **With chapter** — ask for `ch05`; load that specific chapter
- **Browse** — ask "what chapters do you have?"

## Core Frameworks & Mental Models
<~2,000 tokens: the author's most important named frameworks. Preserve exact
names. Write as "Use X when Y". This is a toolkit, not a summary.>

## Chapter Index
| # | Title | Key Frameworks |
|---|-------|----------------|

## Topic Index
- **<Term>** → ch<N>[, ch<N>]

## Supporting Files
- glossary.md, patterns.md, cheatsheet.md

## Scope & Limits
This skill covers the book content only.
```

---

## Step 10 — Cleanup and report

Remove the `<tempdir>/book_skill_work/` directory after generating. Then report:

```
✅ Skill created: $SKILLS_HOME/<skill_name>/
📚 Book: <Full Title> — <Author>
📄 Pages: ~<N> | Chapters: <N>
Files generated: SKILL.md, chapters/ (N files), glossary.md, patterns.md, cheatsheet.md
Usage: ask for <skill_name>, or ask about a topic/chapter.
Reload if your agent doesn't auto-detect new skills.
```

---

## Update / Fold-in Workflow

When updating an existing skill at `$SKILLS_HOME/<skill_name>/`:

1. **Read existing structure** — parse SKILL.md (Chapter Index, Topic Index, metadata, Core Frameworks); list `chapters/` to find the highest chapter number; read glossary/patterns/cheatsheet.
2. **Match content** — new content is either a revision to an existing chapter (merge) or a new addition (create new numbered chapter files after the highest existing).
3. **Generate/update chapters** — follow Step 7 formatting.
4. **Merge supporting files** — alphabetize glossary (append chapter refs to existing terms), append patterns, integrate cheatsheet decision rules.
5. **Regenerate SKILL.md** — increment chapter count, update page count/date, fold in high-impact frameworks, append new chapters to the index, merge Topic Index alphabetically.
6. **Cleanup and report** — Step 10 with a custom update summary.

---

## Quality Rules

1. **Extract structure, not summaries** — named frameworks, exact formulations, anti-patterns
2. **Preserve the author's precision** — keep exact naming
3. **Density over completeness** — a 1,000-token summary beats a 10,000-token excerpt
4. **Practitioner voice** — "Use X when Y", not "The book explains X"
5. **Front-load SKILL.md** — most important content first
6. **Chapter files are on-demand** — don't count against budget until loaded
7. **Never copy raw book text** — always synthesize, summarize, extract signal
8. **Topic index is critical** — it's how the agent navigates to the right chapter

---

## Attribution

This is a clean methodology-only port of `SKILL.md` from [virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill) (MIT). Upstream blocked by SkillSpector (CRITICAL, 100/100) due to bundled Python extraction scripts (subprocess calls, dynamic imports) and privilege references. This port keeps the full prose workflow but replaces the bundled `extract.py` with the bundle's existing `markitdown` CLI/MCP for text extraction. No scripts, no deps.