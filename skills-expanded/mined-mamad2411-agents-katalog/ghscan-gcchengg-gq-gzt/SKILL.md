# FAW PRD Word Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and install a reusable `faw-prd-word` Codex skill that creates confirmed, editable PRD Word documents in the visual style of the supplied FAW Equity presentation.

**Architecture:** The skill contains concise workflow instructions, separate brand/content references, authentic icon assets extracted from the reference PPTX, and deterministic Python scripts for DOCX generation and validation. The generator consumes confirmed Markdown and emits an editable `.docx`; the validator checks content, image embedding, colors, and unresolved markers.

**Tech Stack:** Codex Skills, Python 3, python-docx, Pillow, OOXML, pytest, LibreOffice rendering.

## Global Constraints

- Install to `~/.codex/skills/faw-prd-word`.
- Output format is `.docx`.
- Generate and confirm Markdown before generating Word.
- Do not invent unconfirmed business rules.
- Mark genuinely unclear rules as “待确认”.
- Do not expand items the user says not to address.
- Use FAW blue `#152A8C`, FAW red `#C00000`, and Microsoft YaHei.
- Use original user screenshots; never fabricate business screenshots.
- Render every final DOCX to PNG and inspect every page before delivery.

---

### Task 1: Initialize the Skill and Preserve Brand Assets

**Files:**
- Create: `~/.codex/skills/faw-prd-word/SKILL.md`
- Create: `~/.codex/skills/faw-prd-word/agents/openai.yaml`
- Create: `~/.codex/skills/faw-prd-word/references/brand-style.md`
- Create: `~/.codex/skills/faw-prd-word/references/prd-content-rules.md`
- Create: `~/.codex/skills/faw-prd-word/assets/icons/*.png`
- Create: `~/.codex/skills/faw-prd-word/assets/reference/一企一策工作台优化方案20260709.pptx`

**Interfaces:**
- Consumes: `/Users/guocc/Documents/guquan/files/gq-gzt/需求/一企一策/一企一策工作台优化方案20260709.pptx`
- Produces: discoverable skill metadata, brand references, and authentic source assets.

- [ ] **Step 1: Record the failing baseline**

Use the observed failure from the current task history: without the skill, an agent generated a PRD containing unconfirmed download formats, approval fields, permissions, and notification behavior.

Expected: baseline violates the “confirmed content only” requirement.

- [ ] **Step 2: Initialize the skill**

Run:

```bash
python /Users/guocc/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  faw-prd-word \
  --path /Users/guocc/.codex/skills \
  --resources scripts,references,assets \
  --interface display_name="一汽 PRD Word" \
  --interface short_description="生成一汽风格的正式 PRD Word 文档" \
  --interface default_prompt="请根据需求和截图整理 PRD，先输出 Markdown 待确认稿，确认后生成一汽风格 Word。"
```

Expected: the skill folder and `agents/openai.yaml` are created.

- [ ] **Step 3: Extract authentic icon assets**

Extract embedded media from the reference PPTX, identify reusable blue single-color title icons, and copy only authentic assets into `assets/icons/`.

Expected: at least one reusable icon exists; no generated or traced logo is used.

- [ ] **Step 4: Write the brand and content references**

Record exact palette, typography, heading hierarchy, image rules, confirmation gate, and prohibited content expansion.

Expected: the references explicitly contain `152A8C`, `C00000`, `微软雅黑`, `Markdown`, and `待确认`.

### Task 2: Implement and Test the DOCX Generator

**Files:**
- Create: `~/.codex/skills/faw-prd-word/scripts/generate_prd_docx.py`
- Create: `~/.codex/skills/faw-prd-word/scripts/validate_prd_docx.py`
- Create: `/Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/test_generate_prd.py`
- Create: `/Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/confirmed-example.md`

**Interfaces:**
- Produces: `generate(input_md: Path, output_docx: Path) -> Path`
- Produces: CLI `generate_prd_docx.py --input INPUT.md --output OUTPUT.docx`
- Produces: CLI `validate_prd_docx.py INPUT.docx [--source-markdown INPUT.md]`

- [ ] **Step 1: Write failing generator tests**

Tests must assert:

```python
assert output_docx.exists()
assert "152A8C" in unpacked_document_xml
assert "C00000" in unpacked_styles_or_document_xml
assert "需求背景" in extracted_text
assert "待确认" not in extracted_text_when_source_has_none
assert embedded_image_count == source_local_image_count
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
pytest -q /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/test_generate_prd.py
```

Expected: FAIL because the generator module does not exist.

- [ ] **Step 3: Implement the Markdown-to-DOCX generator**

Support:

- `#`, `##`, and `###` headings.
- Plain paragraphs.
- Bulleted lists.
- Markdown tables.
- Local image syntax.
- Cover metadata.
- FAW-branded header, footer, title rules, and editable Word styles.

- [ ] **Step 4: Implement structural validation**

Fail when:

- DOCX is missing or unreadable.
- No heading exists.
- A referenced local image was not embedded.
- `TODO`, `TBD`, or an unresolved template marker remains.
- Expected FAW colors are absent.

- [ ] **Step 5: Run tests and verify GREEN**

Run:

```bash
pytest -q /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/test_generate_prd.py
```

Expected: all tests pass.

### Task 3: Author, Validate, and Forward-Test the Skill

**Files:**
- Modify: `~/.codex/skills/faw-prd-word/SKILL.md`
- Modify: `~/.codex/skills/faw-prd-word/agents/openai.yaml`
- Create: `/Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/output/example-prd.docx`
- Create: `/Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/rendered/page-*.png`

**Interfaces:**
- Consumes: confirmed Markdown plus local screenshots.
- Produces: a validated and visually reviewed PRD DOCX.

- [ ] **Step 1: Write the skill workflow**

The workflow must require:

1. Inspect all source files and screenshots.
2. Draft Markdown using only explicit user requirements.
3. Pause for explicit confirmation.
4. Generate Word only after confirmation.
5. Validate structurally.
6. Render with the bundled document renderer.
7. Inspect every rendered page and iterate.

- [ ] **Step 2: Run official skill validation**

Run:

```bash
python /Users/guocc/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  /Users/guocc/.codex/skills/faw-prd-word
```

Expected: `Skill is valid!`

- [ ] **Step 3: Generate a representative PRD**

Run:

```bash
python /Users/guocc/.codex/skills/faw-prd-word/scripts/generate_prd_docx.py \
  --input /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/confirmed-example.md \
  --output /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/output/example-prd.docx
```

Expected: editable DOCX with headings, list items, a table, and an embedded screenshot.

- [ ] **Step 4: Validate and render**

Run:

```bash
python /Users/guocc/.codex/skills/faw-prd-word/scripts/validate_prd_docx.py \
  /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/output/example-prd.docx \
  --source-markdown /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/confirmed-example.md

env TMPDIR=/private/tmp \
  /Users/guocc/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  /Users/guocc/.codex/plugins/cache/openai-primary-runtime/documents/26.723.12215/skills/documents/render_docx.py \
  /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/output/example-prd.docx \
  --output_dir /Users/guocc/Documents/guquan/files/gq-gzt/tmp/faw-prd-word-tests/rendered
```

Expected: validation passes and PNG pages are produced.

- [ ] **Step 5: Inspect every page**

Confirm:

- No clipping, overlap, or broken tables.
- All Chinese glyphs render correctly.
- FAW blue dominates headings and separators.
- FAW red is restrained and used for emphasis.
- Screenshots retain aspect ratio.
- No unconfirmed rules appear.

