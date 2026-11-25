# Doc-Stitcher Skill

**Domain**: content
**Trigger**: QSTITCH
**Purpose**: Concatenate multiple markdown documents efficiently using bash commands to save tokens and improve context coherence.

---

## Role

You are a token-efficient document concatenation specialist. Your core expertise is stitching multiple markdown files into a single coherent document using bash commands, eliminating the need for multiple Read tool invocations.

---

## When to Use This Skill

### ✅ Use QSTITCH When:
- Working with multi-part documents (PR-FAQ split into 4 parts)
- Need all content in single context for analysis/revision
- Files are in predictable order (part1, part2, part3...)
- Want to save context window space
- Creating final deliverable from multiple drafts

### ❌ Don't Use QSTITCH When:
- Files are small (<200 lines each) - direct Read is fine
- Need to selectively read specific sections
- Files are in different formats (not all markdown)
- Order is unclear or requires user input

---

## Core Capabilities

1. **Concatenate Multiple Files**: Use bash `cat` to merge files in order
2. **Remove Duplicate Headers**: Strip redundant "# Part N" headers between sections
3. **Add Section Breaks**: Insert `---` dividers between major parts
4. **Preserve Formatting**: Maintain markdown structure, code blocks, tables
5. **Handle Edge Cases**: File paths with spaces, missing files, encoding issues
6. **Verify Output**: Check line count, structure, completeness

---

## Tools Available

- **Bash**: Execute concatenation commands (cat, sed, awk)
- **Read**: Verify output integrity
- **Write**: Create final output if modifications needed

---

## Usage Pattern

### Basic Invocation
```bash
# Concatenate 4 files in order
cat part1.md part2.md part3.md part4.md > combined.md
```

### With Header Removal
```bash
# Remove first 2 lines from each part (skip "# Part N" headers)
cat part1.md > combined.md
tail -n +3 part2.md >> combined.md
tail -n +3 part3.md >> combined.md
tail -n +3 part4.md >> combined.md
```

### With Section Breaks
```bash
# Add dividers between parts
cat part1.md > combined.md
echo -e "\n---\n" >> combined.md
tail -n +3 part2.md >> combined.md
echo -e "\n---\n" >> combined.md
tail -n +3 part3.md >> combined.md
```

### Using the Script
```bash
# Use provided script for common patterns
./scripts/stitch-docs.sh \
  --files "part1.md part2.md part3.md part4.md" \
  --output combined.md \
  --remove-headers \
  --section-breaks
```

---

## Workflow

### Step 1: Identify Files to Stitch
Determine the files and their order:
```bash
ls -1 requirements/pr-faq-*.md
# Output: pr-faq-01-press-release.md
#         pr-faq-02-external-faq.md
#         pr-faq-03-internal-faq.md
#         pr-faq-04-appendices.md
```

### Step 2: Choose Stitching Strategy
- **Simple concatenation**: Files don't have duplicate headers
- **Header removal**: Each file has "# Part N" header to remove
- **Section breaks**: Add visual dividers between parts

### Step 3: Execute Bash Command
```bash
# Example: PR-FAQ with header removal
cd requirements
cat pr-faq-01-press-release.md > pr-faq-STITCHED.md
tail -n +3 pr-faq-02-external-faq.md >> pr-faq-STITCHED.md
tail -n +3 pr-faq-03-internal-faq.md >> pr-faq-STITCHED.md
tail -n +3 pr-faq-04-appendices.md >> pr-faq-STITCHED.md
```

### Step 4: Verify Output
```bash
# Check line count
wc -l pr-faq-STITCHED.md
# Expected: sum of all parts minus removed headers

# Check structure
head -50 pr-faq-STITCHED.md
tail -50 pr-faq-STITCHED.md
```

### Step 5: Report to User
"Stitched 4 files into `pr-faq-STITCHED.md` (1,330 lines). Removed duplicate headers from parts 2-4. File ready for review at `/requirements/pr-faq-STITCHED.md`."

---

## Token Savings Analysis

### Without Stitching (Traditional Approach)
- Read part1.md (500 tokens)
- Read part2.md (400 tokens)
- Read part3.md (600 tokens)
- Read part4.md (300 tokens)
- **Total: 4 Read invocations, fragmented context**

### With Stitching (QSTITCH Approach)
- Bash stitch (50 tokens)
- Read combined.md (1800 tokens)
- **Total: 1 Read invocation, coherent context**

**Benefit**: Not token reduction, but **context coherence** - all content available in single context for holistic analysis/revision.

---

## Common Use Cases

### 1. PR-FAQ Consolidation
```bash
# Stitch 4-part PR-FAQ into single document
./scripts/stitch-docs.sh \
  --files "pr-faq-01-press-release.md pr-faq-02-external-faq.md pr-faq-03-internal-faq.md pr-faq-04-appendices.md" \
  --output productization-pr-faq-FINAL-v3.md \
  --remove-headers
```

### 2. Requirements Consolidation
```bash
# Merge multiple REQ files
cat requirements/req-401-410.md requirements/req-411-420.md > requirements/requirements-complete.md
```

### 3. Multi-Chapter Report
```bash
# Combine chapters with section breaks
cat chapter1.md > report.md
echo -e "\n---\n" >> report.md
cat chapter2.md >> report.md
echo -e "\n---\n" >> report.md
cat chapter3.md >> report.md
```

---

## Edge Cases & Solutions

### File Paths with Spaces
```bash
# Use quotes
cat "part 1.md" "part 2.md" > combined.md
```

### Missing Files
```bash
# Check existence first
for file in part1.md part2.md part3.md; do
  if [ ! -f "$file" ]; then
    echo "Error: $file not found"
    exit 1
  fi
done
cat part1.md part2.md part3.md > combined.md
```

### Wrong Order
```bash
# Use explicit ordering (not glob patterns)
cat pr-faq-01-*.md pr-faq-02-*.md pr-faq-03-*.md pr-faq-04-*.md > combined.md
# NOT: cat pr-faq-*.md (may sort incorrectly)
```

---

## Script Reference

### stitch-docs.sh
Location: `.claude/skills/content/doc-stitcher/scripts/stitch-docs.sh`

**Options**:
- `--files`: Space-separated list of files (in order)
- `--output`: Output filename
- `--remove-headers`: Remove first N lines from parts 2+ (default: 2)
- `--section-breaks`: Add `---` dividers between parts
- `--verify`: Run verification checks after stitching

**Example**:
```bash
./scripts/stitch-docs.sh \
  --files "part1.md part2.md part3.md" \
  --output combined.md \
  --remove-headers \
  --section-breaks \
  --verify
```

### verify-stitch.sh
Location: `.claude/skills/content/doc-stitcher/scripts/verify-stitch.sh`

**Checks**:
- Line count matches expected (sum of parts - removed headers)
- No duplicate headers remain
- Markdown structure valid (matching code blocks, lists)
- File size reasonable (not truncated)

---

## References

- `references/bash-concat-patterns.md`: Bash concatenation best practices
- `references/markdown-best-practices.md`: Preserving markdown structure
- `examples/pr-faq-stitch.sh`: PR-FAQ stitching example
- `examples/requirements-stitch.sh`: Requirements consolidation example

---

## Integration with CLAUDE.md

Add to QShortcuts section:
```markdown
- **QSTITCH**: Concatenate markdown documents using bash to save tokens → **skills/content/doc-stitcher** (tools: stitch-docs.sh, verify-stitch.sh)
```

---

## Success Criteria

After stitching, verify:
- ✅ All source files included in output
- ✅ Correct order preserved
- ✅ Duplicate headers removed (if requested)
- ✅ Markdown structure intact (code blocks, lists, tables)
- ✅ Line count matches expected
- ✅ File readable with Read tool

---

## Limitations

- **Not a replacement for selective reading**: If you only need part 2, just read part 2 directly
- **Token cost**: Stitching + reading still costs tokens (just better context)
- **File size limits**: Very large stitched files (>50KB) may hit tool limits
- **Formatting loss**: Complex markdown (nested tables, unusual syntax) may break

---

## Example Session

```
User: "I have 4 PR-FAQ parts. Can you stitch them into a single document?"