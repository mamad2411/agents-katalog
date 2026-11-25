---
name: factcheck-docs
description: "Deep factcheck of project documentation (README.md, CLAUDE.md, SVG diagrams, skill definitions) against the actual codebase. Finds inaccuracies, stale references, missing information, and bloat. Use after making code changes, when docs may be stale, or when the user says things like \"check the docs\", \"are the docs up to date\", \"factcheck\", \"audit docs\", \"verify documentation\", or \"docs are wrong\"."
argument-hint: "[specific docs or areas to focus on]"
allowed-tools: Agent, Read, Edit, Bash, Glob, Grep, Write, mcp__playwright_*
context: fork
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty). It may specify which docs to check, specific areas of concern, or files to focus on.

## Purpose

Deep factcheck of project documentation (README.md, CLAUDE.md, SVG diagrams, and skill/agent definitions) against the actual codebase. Finds inaccuracies, stale references, missing information, and bloat. Produces a report and then applies fixes.

**Audience distinction:**
- **README.md** is for humans setting up and using Rockport. It should explain what things do and how to use them.
- **CLAUDE.md** is for Claude Code. It should document non-obvious gotchas, exact technical details, and things that would trip up an AI assistant working on the codebase. Don't duplicate what's readable from code.

## Phases

### Phase 1: Build ground truth from code

Read ALL source-of-truth files listed in [sources.md](sources.md). Do not skip any. Use the Agent tool with subagent_type=Explore or parallel Read calls to maximise speed.

### Phase 2: Cross-reference and audit

For each documentation file, check EVERY factual claim against the ground truth gathered in Phase 1. Be methodical — go line by line through each doc file. Use the checklists in [checklists.md](checklists.md).

### Phase 3: Report findings

Present ALL findings in a table. Be exhaustive — every discrepancy matters.

```
| # | File | Location | Type | Description | Fix |
|---|------|----------|------|-------------|-----|
| 1 | README.md | L42 | STALE | References /v1/images/structure (removed) | Remove row |
| 2 | CLAUDE.md | L108 | INACCURATE | Says MemoryMax 512MB, systemd has 256MB | Change to 256MB |
| 3 | arch.svg | sidecar box | MISSING | No stability-* models shown | Add model box |
| 4 | CLAUDE.md | L95,L107 | DUPLICATE | Tunnel routing described twice | Remove one |
```

Issue types:
- **STALE** — references something that no longer exists in code
- **INACCURATE** — states something that contradicts the code
- **MISSING** — omits something important that exists in code
- **BLOAT** — unnecessary verbosity or over-documentation of obvious things
- **DUPLICATE** — same fact stated multiple times
- **INCONSISTENT** — two doc files contradict each other about the same fact

After presenting the table, ask: "Shall I apply all fixes?" and wait for confirmation before proceeding.

### Phase 4: Apply fixes

After user confirms, apply all fixes:
- **STALE**: remove or update the reference
- **INACCURATE**: correct to match code exactly
- **MISSING**: add in the appropriate location (README for users, CLAUDE.md for Claude)
- **BLOAT**: remove the unnecessary content
- **DUPLICATE**: keep the better version, remove the other
- **INCONSISTENT**: use the version that matches code, fix the other

### Phase 5: Verify

After applying fixes:
1. Run `shellcheck` on any modified `.sh` files
2. Run `terraform -chdir=terraform fmt -check` if terraform files were touched
3. Run `python3 -c "import ast; ast.parse(open('file').read())"` on any modified `.py` files
4. Validate modified SVGs are well-formed XML: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')"`
5. Run `python3 -c "import yaml; yaml.safe_load(open('config/litellm-config.yaml'))"` if config was touched
6. Show a git diff summary of all changes made

### Phase 6: Visual audit of SVG diagrams

Use Playwright MCP to render each SVG in a real browser and screenshot it. This catches layout issues (overlapping text, misaligned boxes, clipped content) that XML validation cannot detect.

**CRITICAL: This phase requires actual screenshots. Do NOT fabricate visual analysis from SVG XML source. If you cannot take a screenshot, say so — do not describe what you think the rendering looks like based on reading coordinates.**

#### Availability check

Before starting, test that Playwright is working:

1. Call `mcp__playwright__browser_navigate` with url `about:blank`
2. If the tool call fails or is not found, output: **"Phase 6 skipped: Playwright MCP not available. SVGs were validated as well-formed XML only — no visual rendering was performed."** Then stop. Do NOT write any visual analysis.

#### For each SVG file in `docs/`:

1. **Resize viewport** — call `mcp__playwright__browser_resize` with width and height matching the SVG's `width`/`height` attributes (read these from the `<svg>` tag). This prevents the browser from scaling or clipping the diagram.
2. **Navigate** — call `mcp__playwright__browser_navigate` with the file URL (e.g. `file:///home/matt/rockport/docs/rockport_architecture_overview.svg`)
3. **Screenshot** — call `mcp__playwright__browser_take_screenshot`. Confirm you received an image back. If the screenshot tool returns an error or empty result, report the failure and move to the next SVG.
4. **Examine the screenshot image only** — report what you can see in the rendered image:
   - Overlapping or clipped text
   - Misaligned boxes, arrows, or connectors
   - Text that's too small or illegible
   - Arrow endpoints that don't connect to targets
   - Elements cut off at viewport edges
   - Excessive whitespace or cramped regions

   Do NOT cite SVG XML attributes (coordinates, font-size values, element IDs) in your visual report. Describe what you see, not what the source says.
5. **Fix if needed** — if issues are found, make targeted SVG XML edits, validate XML, then re-screenshot and verify. Cap at 3 fix-and-verify iterations per SVG.

#### Output format

For each SVG, report one of:
- **PASS** — "Renders correctly, no visual issues found"
- **FIXED** — list what was wrong and what was changed, confirmed by re-screenshot
- **ISSUES** — visual problems found but not fixable via targeted edits (describe what you see)
- **SKIPPED** — Playwright unavailable or screenshot failed (state why)

## Rules

### No bloat (CRITICAL)

- **Only document what is needed and accurate. Be succinct.** Don't add prose, context, or background that doesn't help the reader do something or avoid a mistake.
- **State facts, not explanations.** "Stability AI image edit models use the `us.` cross-region inference prefix" is good. "Because Stability AI models on Bedrock are only available through cross-region inference profiles, which route requests across multiple US regions for improved availability, the model IDs must include the `us.` prefix" is bloat.
- **If the current wording is accurate, leave it alone.** Don't rephrase working descriptions.
- **CLAUDE.md litmus test:** "Would Claude make a mistake without this bullet?" If no, delete it.
- **README.md should be scannable.** Tables over paragraphs. Bullet points over prose. Code examples over descriptions.

### Source of truth

- **Code is the single source of truth** — if docs and code disagree, docs are wrong
- **Every claim must be verifiable** — if you can't find it in the code, it shouldn't be in the docs
- **Precision over prose** — use exact model names, exact paths, exact ports, exact error codes

### Audience

- **README.md is for humans** — explain what things do and how to use them
- **CLAUDE.md is for Claude** — document non-obvious gotchas and constraints that would cause mistakes. Don't document things readable from code
- **No duplication across files** — don't repeat the same fact in both unless the audiences genuinely need different framing

### SVG diagrams

- **SVGs must render correctly** — every edit must produce valid XML. After any SVG edit, validate with `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg'); print('valid')"` before moving on
- **Do not rewrite SVGs** — make targeted text edits only. Changing a `<text>` element's content is fine. Restructuring layout, moving boxes, or adding new elements risks breaking coordinates and alignment. Only add/move SVG elements if you can verify the coordinates are correct by examining adjacent elements
- **SVG text must match code exactly** — routing descriptions, port numbers, model names, memory limits must all come from the source-of-truth files read in Phase 1
- **Test SVG rendering** — Phase 6 handles this via Playwright MCP (opens SVGs in a headless browser, screenshots them, and checks for visual issues). If Playwright is unavailable, at minimum validate XML and check that no coordinates were accidentally changed

### Cleanup

- **Remove stale feature-branch annotations** — bullets ending in "(009-complete-image-services)" or similar should be cleaned up once merged
- **Active Technologies should list only current tech** — no feature-branch-specific entries
- **Remove dead references** — any mention of endpoints, files, or features that no longer exist must be removed, not just updated
