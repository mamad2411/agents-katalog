---
name: content-to-skill
description: >
  Convert any content into a Claude skill. Accepts text, documents, audio files, or video files
  and transforms them into a properly structured SKILL.md with optional bundled resources.
  Supports two skill modes: Knowledge-type (analysis frameworks, reference guides, decision trees)
  and Action-type (executable workflows with scripts, API calls, file operations).
  Auto-detects the best mode from content, but user can override.
  Accepts optional user instructions to customize the generated skill's focus and behavior.
  Use this skill whenever the user says "turn this into a skill", "make a skill from this",
  "万物皆可skill", "content to skill", or uploads any file (video, audio, PDF, article, tutorial,
  transcript, documentation) and wants it converted into a reusable skill. Also triggers when
  the user pastes text (a guide, a process, a workflow, tips, a how-to) and asks to skillify it.
  万物皆可 Skill：将任何内容转化为可复用的 Claude 技能。支持知识型和动作型两种模式，
  自动判断素材类型，也接受用户自定义指令。
---

# Content-to-Skill Converter

**万物皆可 Skill** — Turn any content into a reusable Claude skill.

## Supported Inputs

| Input Type | How to Handle |
|---|---|
| **Text / Markdown** | Directly in chat or uploaded .txt/.md file — process inline |
| **PDF** (.pdf) | Extract text: `from pypdf import PdfReader; text = "".join(p.extract_text() for p in PdfReader("f.pdf").pages)`. For scanned PDFs, use OCR. |
| **Word Document** (.docx) | Extract with pandoc: `pandoc doc.docx -t markdown -o output.md` |
| **PowerPoint** (.pptx) | Extract text: `python -m markitdown presentation.pptx`. For visual context: use pptx skill's `thumbnail.py` |
| **Spreadsheet** (.xlsx, .csv) | Read with `openpyxl` — extract headers, formulas, and workflow logic |
| **Audio** (.mp3, .wav, .m4a, .ogg, .flac) | Transcribe with `scripts/transcribe.py`, then convert |
| **Video** (.mp4, .mov, .webm, .mkv) | Extract audio → transcribe with `scripts/transcribe.py`, then convert |
| **URL / Web page** | Fetch content with web_fetch or browser, then convert |
| **Image** (of text/slides/whiteboard) | Read text from image using Claude's vision, then convert |
| **Social media post** (X/Twitter, etc.) | Fetch via browser or API, then convert |
| **Mixed batch** | Multiple inputs of different types — process each, then merge or create separate skills |

## Workflow

### Step 0: Parse User Intent

Before doing anything, determine two things:

1. **Content (素材)**: What raw material did the user provide?
2. **Instructions (指令)**: Did the user specify what the skill should do or focus on?

Three scenarios:
- **Content only**: User provides material without instructions → auto-classify and generate
- **Content + Instructions**: User provides material AND tells you what the skill should do → follow their instructions, use content as the knowledge base
- **Instructions only**: User describes what they want without providing material → ask for content, or search/research to gather it

If instructions are provided, they take priority over auto-classification. For example:
- Content: an article about DEX aggregators
- Instruction: "make a skill that monitors aggregator performance daily"
- Result: Action-type skill (even though the article alone would suggest knowledge-type)

### Step 1: Ingest Content

1. Determine input type from file extension or content.
2. Route to the correct extraction method:

   **For audio/video**: run the transcription script:
   ```bash
   python3 /path/to/content-to-skill/scripts/transcribe.py <input_file> -o /tmp/transcript.txt
   ```
   - Uses OpenAI Whisper (local, free). Install if needed: `pip install openai-whisper --break-system-packages`

   **For PDF**: `from pypdf import PdfReader; text = "\n".join(p.extract_text() for p in PdfReader("f.pdf").pages)`
   Install if needed: `pip install pypdf --break-system-packages`

   **For DOCX**: `pandoc input.docx -t markdown -o /tmp/extracted.md`

   **For PPTX**: `python -m markitdown input.pptx > /tmp/extracted.md`
   Install if needed: `pip install markitdown --break-system-packages`

   **For XLSX/CSV**: `import openpyxl; wb = openpyxl.load_workbook("input.xlsx")` — extract headers, formulas, logic

3. For URLs: try web_fetch first, then browser if blocked.
4. For images: read text directly from the image using Claude's vision.
5. For text: use directly.

### Step 2: Classify → Knowledge-type or Action-type

Analyze the content and auto-detect which skill type fits better.

**Knowledge-type skill (知识型)** — The skill serves as a structured reference that Claude draws on during conversation.

Signals that suggest knowledge-type:
- Content is an article, opinion piece, analysis, or research paper
- Content explains concepts, frameworks, or theories
- Content compares options or evaluates alternatives
- No clear repeatable "do this then that" workflow
- The value is in the *understanding*, not the *execution*

What a knowledge-type skill looks like:
- Analysis frameworks with decision trees
- Comparison matrices and evaluation criteria
- Structured reference material organized by topic
- Trigger conditions tied to conversation topics

**Action-type skill (动作型)** — The skill drives Claude to execute a concrete workflow that produces tangible output.

Signals that suggest action-type:
- Content is a tutorial, how-to guide, or step-by-step process
- Content describes tools, commands, or APIs
- Content includes code examples or configuration files
- There's a clear input → process → output pattern
- The value is in the *execution*, not just the *understanding*

What an action-type skill looks like:
- Numbered executable steps with exact commands
- Scripts in `scripts/` for deterministic tasks
- Input/output specifications
- Verification steps to confirm success

**Present the classification to the user:**

```
📋 素材分析:
- 内容类型: [文章/教程/视频/笔记/...]
- 检测语言: [中文/English/...]
- 推荐模式: [知识型 / 动作型]
- 推荐理由: [一句话解释]

你可以:
1. 接受推荐 → 直接执行 /skill-generate
2. 切换模式 → /skill-knowledge 或 /skill-action
3. 补充指令 → /skill-generate [你的指令]
```

If the user doesn't respond or says "go ahead", use the recommended mode.

### Step 3: Determine Language

- Detect the primary language of the input content.
- Write the SKILL.md body in **that same language**.
- Exception: YAML frontmatter keys (`name`, `description`) are always in English.
- Exception: If the input language is not well-supported for technical writing, default to English.
- The `description` field should be bilingual if the content is non-English:
  write the English description first, then append the native language version.

### Step 4: Generate the Skill

Create a skill folder. The structure depends on the skill type and complexity:

```
<skill-name>/
├── SKILL.md          # Main instructions (required)
├── references/       # (optional) Detailed docs, lookup tables
├── scripts/          # (optional) Helper scripts for deterministic tasks
├── commands/         # (optional) Slash commands for quick invocation
├── hooks/            # (optional) Auto-triggers on specific events
└── agents/           # (optional) Sub-agent definitions for complex workflows
```

#### When to generate each component for the OUTPUT skill

| Component | When to generate | Example |
|---|---|---|
| **SKILL.md** | Always | Every skill needs this |
| **references/** | Content > 500 lines, or multiple sub-topics | Large tutorials, multi-chapter guides |
| **scripts/** | Deterministic/repeatable tasks that benefit from code | Data processing, file conversion, API calls |
| **commands/** | The generated skill has distinct sub-workflows users might invoke independently | A deploy skill with `/deploy-staging` and `/deploy-prod` |
| **hooks/** | The generated skill should auto-trigger on file edits or tool use | A lint skill that runs on every file save |
| **agents/** | The generated skill's workflow is complex enough for role separation | A review skill with separate architect + security agents |

Whether to generate these components depends on the content being converted. Most skills only need SKILL.md + references/. Scripts, commands, hooks, and agents are only added when the content clearly warrants them.

Use the appropriate template based on the classified type:

#### Template A: Knowledge-type Skill

```markdown
---
name: <kebab-case-name>
description: >
  <English description. Be pushy — list specific trigger phrases and contexts.>
  <If non-English: Native language description here.>
# --- Optional fields (add only when needed) ---
# allowed-tools: Read Grep Glob          # Tools this skill can use without asking permission
# paths: "*.md, docs/**"                 # Only activate when working with matching files
# disable-model-invocation: true         # Set if skill should only be triggered manually via /name
---

# <Skill Title>

<Brief intro: what knowledge this skill gives Claude access to.>

## When to Use
<Explicit trigger conditions — what conversation topics, user phrases, or contexts activate this.>

## When NOT to Use
<Prevent false triggers.>

## Core Framework
<The main analytical framework, organized by dimension or theme.>
<Include decision trees, comparison matrices, evaluation criteria.>

## Key Concepts
<Define important terms and relationships.>

## Analysis Workflow
<When this skill triggers, how should Claude structure its response?>
<Step-by-step thinking process, not execution steps.>

## Output Template
<A structured template for Claude's response when using this skill.>

## Examples
<At least 1-2 concrete input→output examples.>

## Limitations & Caveats
<What this framework can't do, known biases, data freshness issues.>
```

#### Template B: Action-type Skill

```markdown
---
name: <kebab-case-name>
description: >
  <English description. Be pushy — list specific trigger phrases and contexts.>
  <If non-English: Native language description here.>
# --- Optional fields (add only when needed) ---
# allowed-tools: Read Bash Grep Glob Write   # Tools this skill can use without asking permission
# context: fork                               # Run in isolated subagent (for heavy/risky workflows)
# paths: "src/**/*.py"                        # Only activate when working with matching files
# disable-model-invocation: true              # Set if skill should only be triggered manually via /name
---

# <Skill Title>

<Brief intro: what this skill enables Claude to DO.>

## When to Use
<Explicit trigger conditions — what user requests, file types, or contexts activate this.>

## When NOT to Use
<Prevent false triggers.>

## Prerequisites
<Tools, libraries, APIs, permissions needed.>

## Step-by-Step Workflow
<Numbered, executable steps. Each step should be concrete enough to run.>
1. [Step with exact command or action]
2. [Step with exact command or action]
...

## Input/Output Spec
- **Input**: [What the user provides]
- **Output**: [What gets produced — file type, format, location]

## Scripts
<Reference any helper scripts via ${CLAUDE_SKILL_DIR}/scripts/ path.>

## Verification
<How to confirm the skill executed correctly.>

## Edge Cases & Error Handling
<What can go wrong and how to recover.>

## Examples
<At least 1-2 concrete input→output examples showing the full execution.>
```

#### Writing Guidelines (both types)

- **Be actionable**: Even knowledge-type skills should tell Claude HOW to use the knowledge in responses.
- **Be specific**: Include exact trigger phrases, commands, file paths.
- **Be structured**: Use headers, numbered steps, decision trees.
- **Keep SKILL.md under 500 lines**. If content is too rich, split into `references/` files.
- **Include "when NOT to use"** to prevent false triggers.
- **Include at least 2 examples** — they massively improve skill reliability. Examples are not optional.
- **Explain the why** — don't just say "do X", explain why X matters.
- **Make the name kebab-case** — e.g., `my-cool-skill`, not `My Cool Skill`.
- **Make the description pushy** — include trigger phrases, file types, contexts. Err on over-triggering.
- **Use `${CLAUDE_SKILL_DIR}`** to reference bundled files (scripts, references) so paths resolve correctly regardless of where the skill is installed.
- **Add `allowed-tools`** when the skill needs specific tools (Bash, Write, etc.) to reduce permission prompts.
- **Use `context: fork`** for Action-type skills that run heavy or risky workflows — this runs the skill in an isolated subagent context.

### Step 5: Quality Check

Before presenting the skill, verify every item. Do not skip any:

- [ ] YAML frontmatter has `name` (kebab-case!) and `description`
- [ ] `name` is kebab-case (lowercase, hyphens only)
- [ ] Description is "pushy" — lists specific trigger phrases
- [ ] Description is bilingual if input content is non-English
- [ ] Skill type is appropriate (knowledge vs action)
- [ ] Knowledge-type: has framework, analysis workflow, output template
- [ ] Action-type: has executable steps, input/output spec, verification
- [ ] Language matches input content (with English frontmatter)
- [ ] Under 500 lines (or properly split into references)
- [ ] **At least 2 examples included** (input → output format)
- [ ] Edge cases / limitations covered
- [ ] "When NOT to Use" section present

The most commonly missed items are: **examples**, **kebab-case naming**, and **bilingual descriptions**. Double-check these three.

### Step 6: Package & Deliver

1. Write the skill folder to the appropriate output directory.
2. If the `package_skill.py` script is available, package it:
   ```bash
   cd /mnt/skills/examples/skill-creator && python -m scripts.package_skill /path/to/<skill-name> /output/path/
   ```
3. Present the `.skill` file to the user.
4. Show a summary:
   - Skill name & description
   - **Skill type: Knowledge / Action**
   - Number of files generated
   - Key capabilities
   - Suggested trigger phrases to test

## Special Cases

### Long-form Content (> 30 min video / > 5000 words)

1. Put the core workflow in SKILL.md (under 500 lines)
2. Create `references/` files for detailed sub-topics
3. Add a "Reference Index" section in SKILL.md pointing to each reference file

### Tutorial / Course Content → Usually Action-type

1. Each major section → a step in the workflow
2. Code examples → include inline or in `scripts/`
3. Exercises → convert to "verification steps" or examples
4. Prerequisites → add to a "Dependencies" section

### Article / Opinion / Analysis → Usually Knowledge-type

1. Extract the core analytical framework
2. Identify the author's key claims and evidence
3. Convert opinions into conditional guidance: "When X, consider Y"
4. Build decision trees from the author's reasoning

### Conversational / Interview Content → Depends on content

1. Extract the **actionable insights** — skip the chit-chat
2. If it's "how I built X" → Action-type
3. If it's "my view on the state of X" → Knowledge-type
4. Attribute key ideas: "According to [speaker], ..."
5. Organize by theme, not by chronological order

### Presentation Slides (.pptx) → Usually Knowledge-type

1. Extract text via `markitdown` and visual structure via `thumbnail.py`
2. Treat each slide as a potential section or step
3. Speaker notes often contain richer content than slide text — prioritize them
4. Diagrams/charts → describe their meaning in text form

### Spreadsheet Workflows (.xlsx) → Usually Action-type

1. Extract column headers and their relationships
2. Identify formulas — they encode the business logic
3. Convert the formula chain into step-by-step instructions
4. Note any conditional formatting rules as decision points
5. Create the skill around the *process* the spreadsheet encodes, not the data

### Mixed Content (素材 + 指令 combo)

When user provides content AND instructions:
1. Use the content as the knowledge base / raw material
2. Use the instructions to determine the skill's purpose and behavior
3. Instructions override auto-classification
4. The generated skill should serve the instruction's goal, drawing on the content

Example:
- Content: Ray Dalio article about Big Cycle
- Instruction: "每天帮我扫描新闻，用这个框架分析"
- Result: Action-type skill that monitors news and applies the Big Cycle framework

### Batch Processing (多素材批量处理)

When user provides multiple pieces of content:
1. Analyze each piece individually
2. Determine if they should be:
   - **Merged** into one skill (if same topic, complementary perspectives)
   - **Separate** skills (if different topics)
3. Present the grouping plan to the user before generating

## Troubleshooting

| Problem | Solution |
|---|---|
| Whisper not installed | `pip install openai-whisper --break-system-packages` |
| ffmpeg not found | `apt-get update && apt-get install -y ffmpeg` |
| pypdf not installed | `pip install pypdf --break-system-packages` |
| pandoc not found | `apt-get update && apt-get install -y pandoc` |
| markitdown not installed | `pip install markitdown --break-system-packages` |
| openpyxl not installed | `pip install openpyxl --break-system-packages` |
| Audio too long (>1hr) | Split with: `ffmpeg -i input.mp3 -f segment -segment_time 1800 -c copy chunk_%03d.mp3` |
| Content has no clear structure | Ask the user what they want to use it for, then impose structure around that goal |
| Mixed languages in content | Use the dominant language; note bilingual terms in a glossary section |
| URL blocked by network/safety | Try browser access; if still blocked, ask user to paste content |
| Can't determine knowledge vs action | Ask the user: "这个素材你想用来参考分析，还是自动执行某个流程？" |
| User instructions conflict with content | Instructions take priority; use content as supporting material |
