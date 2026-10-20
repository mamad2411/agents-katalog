# Documentation Framework - Claude-Specific Awareness (SAP-007)

**SAP ID**: SAP-007
**Version**: 1.0.0
**Status**: Draft (Phase 3)
**Last Updated**: 2025-11-05

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "Claude (first-time orientation)"
  estimated_tokens: 5000
  estimated_time_minutes: 3
  sections:
    - "1. Quick Start for Claude"
    - "2. When to Use Documentation Framework"
    - "3. Tool Integration Patterns"

phase_2_implementation:
  target_audience: "Claude implementing documentation"
  estimated_tokens: 15000
  estimated_time_minutes: 10
  sections:
    - "4. Key Workflows (Claude Code)"
    - "5. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Claude debugging documentation issues"
  estimated_tokens: 30000
  estimated_time_minutes: 20
  files_to_read:
    - "protocol-spec.md (complete Diataxis specification)"
    - "capability-charter.md (design rationale)"
    - "scripts/extract_tests.py (test extraction)"
    - "scripts/validate_frontmatter.py (validation)"
```

---

## 📖 Quick Reference

**New to SAP-007?** → Read **[README.md](README.md)** first (8-min read) for Diátaxis framework, CLI commands, and Documentation-First workflow.

**This CLAUDE.md provides**: Claude Code tool patterns (Write, Read, Edit) for creating docs, extracting tests, and L3 Documentation-First implementation.

---

## 1. Quick Start for Claude

### What is Documentation Framework? (Claude perspective)

**Documentation Framework (SAP-007)** provides **Diataxis-based documentation structure** with:
- **4 Document Types**: Tutorial, How-To, Reference, Explanation
- **YAML Frontmatter**: Structured metadata with schema validation
- **Executable How-Tos**: Code examples → pytest tests
- **Directory Organization**: user-docs/, dev-docs/, project-docs/

**Claude's Role**:
- Choose correct Diataxis type using **decision matrix**
- Add frontmatter using **Write/Edit tool**
- Extract tests using **Bash tool** (scripts/extract_tests.py)
- Validate documentation using **Bash tool** (scripts/validate_frontmatter.py)

---

### When Should Claude Use This?

**Use Documentation Framework when**:
- User asks "how should I document this?"
- Writing documentation for chora-base or SAPs
- User mentions "Tutorial", "How-To", "Reference", or "Explanation"
- Creating AGENTS.md or CLAUDE.md files (use frontmatter)
- Documentation needs test extraction

**Don't use Documentation Framework when**:
- Writing README-only projects (too simple for Diataxis)
- Creating informal notes or brainstorming
- User explicitly wants different structure (Jekyll, Sphinx)
- Documentation is auto-generated (API docs from docstrings)

---

### Tool Integration Patterns

**Bash tool** (for validation and test extraction):
```bash
# Validate frontmatter
python scripts/validate_frontmatter.py docs/user-docs/my-doc.md

# Extract tests from How-Tos
python scripts/extract_tests.py \
  --input docs/user-docs/how-to/01-example.md \
  --output tests/extracted/

# Run extracted tests
pytest tests/extracted/ -v
```

**Read tool** (for existing docs):
```bash
# Check frontmatter
Read docs/user-docs/tutorials/01-first-server.md
# Review first 20 lines (frontmatter block)

# Check directory structure
Read docs/user-docs/README.md
# Understand organization
```

**Write tool** (for new docs):
```bash
# Create new Tutorial
Write docs/user-docs/tutorials/02-advanced-server.md
# Include frontmatter + content

# Create new How-To
Write docs/user-docs/how-to/03-error-handling.md
# Include test_extraction: true
```

**Edit tool** (for existing docs):
```bash
# Add frontmatter to existing doc
Edit docs/user-docs/tutorials/01-first-server.md
# Add YAML frontmatter block

# Fix Diataxis type
Edit docs/user-docs/how-to/wrong-type.md
# Change type: tutorial to type: how-to
```

---

## 2. When to Use Documentation Framework

### User Signal Detection

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Write a tutorial for X" | Create Tutorial with frontmatter | Write (new doc) |
| "How do I document Y?" | Determine Diataxis type, create doc | Read (examples), Write |
| "Add frontmatter to docs" | Add YAML metadata | Edit (existing docs) |
| "Make How-To executable" | Enable test extraction, mark code blocks | Edit (add test_extraction), Bash (extract) |
| "Validate documentation" | Run frontmatter validation script | Bash (validate_frontmatter.py) |

---

## 3. Tool Integration Patterns

### Pattern 1: Diataxis Type Selection

**Always use decision matrix before creating documentation**:

```markdown
Step 1: Understand user intent
User: "Write a tutorial for MCP servers"

Step 2: Apply decision matrix
Question: What is user intent?
- Learning (teach concepts) → Tutorial ✓
- Solving (specific task) → How-To
- Looking up (API parameters) → Reference
- Understanding (design rationale) → Explanation

Step 3: Create doc with correct type
Write docs/user-docs/tutorials/01-first-mcp-server.md
# type: tutorial in frontmatter
```

**Don't**: Guess at type, always use decision matrix

---

### Pattern 2: Frontmatter-First Approach

**Always add frontmatter before content**:

```markdown
Step 1: Create frontmatter
Write docs/user-docs/tutorials/01-first-server.md
# Start with:
---
title: "Build Your First MCP Server"
type: tutorial
status: draft
audience: users
last_updated: 2025-11-05
---

Step 2: Add content
[Continue writing tutorial content]

Step 3: Validate
Bash: python scripts/validate_frontmatter.py docs/user-docs/tutorials/01-first-server.md
```

**Don't**: Write content first, add frontmatter later (easy to forget)

---

### Pattern 3: Test Extraction Workflow

**For How-Tos with code examples, always extract tests**:

```markdown
Step 1: Write How-To with test_extraction enabled
Write docs/user-docs/how-to/01-error-handling.md
# Frontmatter: test_extraction: true
# Code blocks marked with # TEST: test_name

Step 2: Extract tests
Bash: python scripts/extract_tests.py \
  --input docs/user-docs/how-to/01-error-handling.md \
  --output tests/extracted/

Step 3: Run tests to validate
Bash: pytest tests/extracted/test_error_handler.py -v

Step 4: Fix if tests fail
Edit docs/user-docs/how-to/01-error-handling.md
# Update code examples
# Re-extract and test
```

**Don't**: Write How-To without extracting tests (documentation becomes stale)

---

## 4. Key Workflows (Claude Code)

### Workflow 1: Create Documentation with Frontmatter

**Goal**: Create new documentation with valid frontmatter

**Tools**: Read (examples), Write (new doc), Bash (validate)

**Steps**:

1. **Determine Diataxis type** using decision matrix:
   ```
   User request: "Write a tutorial for MCP servers"

   Decision matrix:
   - User intent: Learning (teach step-by-step)
   - Document type: Tutorial
   ```

2. **Read example for reference**:
   ```bash
   Read docs/user-docs/tutorials/01-existing-tutorial.md
   # Check frontmatter format and structure
   ```

3. **Create new documentation** with frontmatter:
   ```bash
   Write docs/user-docs/tutorials/02-advanced-mcp-server.md
   ```

   Content:
   ```yaml
   ---
   title: "Build an Advanced MCP Server"
   type: tutorial
   status: draft
   audience: users
   last_updated: 2025-11-05
   tags: ["mcp", "tutorial", "advanced", "python"]
   version: "1.0.0"
   related:
     - "docs/user-docs/tutorials/01-first-mcp-server.md"
     - "docs/user-docs/how-to/01-add-error-handling.md"
   complexity: intermediate
   ---

   # Build an Advanced MCP Server

   ## What You'll Learn

   In this tutorial, you'll build an advanced MCP server with:
   - Custom error handling
   - Multi-tool support
   - State management

   ## Prerequisites

   - Completed: [Build Your First MCP Server](01-first-mcp-server.md)
   - Python 3.11+
   - Basic understanding of asyncio

   ## Step 1: Set Up Project Structure

   [Tutorial content continues...]
   ```

4. **Validate frontmatter**:
   ```bash
   Bash: python scripts/validate_frontmatter.py docs/user-docs/tutorials/02-advanced-mcp-server.md
   # Output: Frontmatter valid ✓
   ```

5. **If validation fails, fix errors**:
   ```bash
   # Example error: Invalid type value
   # Fix: Change type to one of: tutorial, how-to, reference, explanation

   Edit docs/user-docs/tutorials/02-advanced-mcp-server.md
   # Correct frontmatter fields
   ```

6. **Commit documentation**:
   ```bash
   Bash: git add docs/user-docs/tutorials/02-advanced-mcp-server.md
   Bash: git commit -m "docs: Add advanced MCP server tutorial"
   ```

**Expected Outcome**: New documentation with valid frontmatter

**Time Estimate**: 10-30 minutes (depending on content length)

**Common Issues**:
- **Wrong type**: Use decision matrix (Tutorial vs How-To confusion common)
- **Missing required fields**: Add title, type, status, audience, last_updated
- **Invalid date format**: Use YYYY-MM-DD

---

### Workflow 2: Extract and Run Tests from How-Tos

**Goal**: Convert How-To code examples to pytest tests

**Tools**: Read (How-To), Edit (add test markers), Bash (extract, run tests)

**Steps**:

1. **Read existing How-To** (or create new one):
   ```bash
   Read docs/user-docs/how-to/01-error-handling.md
   # Check if test_extraction enabled in frontmatter
   ```

2. **Enable test extraction** (if not already enabled):
   ```bash
   Edit docs/user-docs/how-to/01-error-handling.md
   # Add to frontmatter:
   # test_extraction: true
   ```

3. **Mark code blocks for test extraction**:
   ```bash
   Edit docs/user-docs/how-to/01-error-handling.md
   ```

   Add test markers:
   ````markdown
   ## Solution

   Create a custom error handler:

   ```python
   # TEST: test_custom_error_handler
   def custom_error_handler(error: Exception) -> dict:
       """Format errors consistently."""
       return {
           "error": type(error).__name__,
           "message": str(error)
       }

   # Verify error handling works
   test_error = ValueError("test error")
   result = custom_error_handler(test_error)
   assert result["error"] == "ValueError"
   assert result["message"] == "test error"
   ```
   ````

4. **Extract tests**:
   ```bash
   Bash: python scripts/extract_tests.py \
     --input docs/user-docs/how-to/01-error-handling.md \
     --output tests/extracted/
   # Output: Created tests/extracted/test_custom_error_handler.py
   ```

5. **Run tests to validate**:
   ```bash
   Bash: pytest tests/extracted/test_custom_error_handler.py -v
   # Expected output: test_custom_error_handler PASSED
   ```

6. **If tests fail, debug**:
   ```bash
   # Read generated test file
   Read tests/extracted/test_custom_error_handler.py
   # Identify issue

   # Fix How-To code example
   Edit docs/user-docs/how-to/01-error-handling.md
   # Update code block

   # Re-extract and test
   Bash: python scripts/extract_tests.py \
     --input docs/user-docs/how-to/01-error-handling.md \
     --output tests/extracted/
   Bash: pytest tests/extracted/test_custom_error_handler.py -v
   ```

7. **Commit documentation and tests**:
   ```bash
   Bash: git add docs/user-docs/how-to/01-error-handling.md tests/extracted/
   Bash: git commit -m "docs: Add executable How-To for error handling with tests"
   ```

**Expected Outcome**: How-To code examples become passing pytest tests

**Time Estimate**: 15-30 minutes

**Common Issues**:
- **Test markers missing**: Add `# TEST: test_name` before code block
- **Assertions missing**: Add assert statements to validate behavior
- **Import errors**: Include necessary imports in code block
- **Syntax errors**: Validate Python syntax before extracting

---

### Workflow 3: Validate and Fix Documentation Quality

**Goal**: Ensure documentation follows framework standards

**Tools**: Bash (validation scripts), Read (check docs), Edit (fix issues)

**Steps**:

1. **Run frontmatter validation**:
   ```bash
   Bash: python scripts/validate_frontmatter.py docs/
   # Output: List of docs with invalid/missing frontmatter
   ```

   Example output:
   ```
   docs/user-docs/tutorials/01-old-tutorial.md: Missing required field 'last_updated'
   docs/user-docs/how-to/02-old-how-to.md: Invalid type value 'guide' (should be 'how-to')
   ```

2. **Fix frontmatter issues**:
   ```bash
   # Fix missing last_updated
   Edit docs/user-docs/tutorials/01-old-tutorial.md
   # Add: last_updated: 2025-11-05

   # Fix invalid type
   Edit docs/user-docs/how-to/02-old-how-to.md
   # Change: type: guide → type: how-to
   ```

3. **Validate directory structure**:
   ```bash
   # Check if documents are in correct directories
   Bash: grep -r "^type: tutorial" docs/user-docs/tutorials/*.md | wc -l
   # Should equal number of files in tutorials/

   Bash: grep -r "^type: how-to" docs/user-docs/how-to/*.md | wc -l
   # Should equal number of files in how-to/
   ```

4. **If documents in wrong directory, move them**:
   ```bash
   # Example: Tutorial mistakenly in how-to/
   Bash: git mv docs/user-docs/how-to/wrong-tutorial.md docs/user-docs/tutorials/
   ```

5. **Check for missing test extraction**:
   ```bash
   # Find How-Tos without test_extraction
   Bash: grep -L "test_extraction: true" docs/user-docs/how-to/*.md
   ```

6. **Enable test extraction where appropriate**:
   ```bash
   Edit docs/user-docs/how-to/03-missing-tests.md
   # Add frontmatter: test_extraction: true
   # Mark code blocks with # TEST: test_name
   ```

7. **Extract and run all tests**:
   ```bash
   Bash: python scripts/extract_tests.py \
     --input docs/user-docs/how-to/ \
     --output tests/extracted/
   Bash: pytest tests/extracted/ -v
   # Verify all tests pass
   ```

8. **Check for broken cross-references**:
   ```bash
   Bash: python scripts/validate_links.py docs/
   # Output: List of broken related doc paths
   ```

9. **Fix broken cross-references**:
   ```bash
   Read docs/user-docs/tutorials/01-with-broken-link.md
   # Check related: field in frontmatter

   Edit docs/user-docs/tutorials/01-with-broken-link.md
   # Update related: paths to correct locations
   ```

10. **Re-validate all documentation**:
    ```bash
    Bash: python scripts/validate_frontmatter.py docs/
    # Output: All frontmatter valid ✓

    Bash: python scripts/validate_links.py docs/
    # Output: All links valid ✓

    Bash: pytest tests/extracted/ -v
    # Output: All tests passing ✓
    ```

11. **Commit fixes**:
    ```bash
    Bash: git add docs/ tests/extracted/
    Bash: git commit -m "docs: Fix frontmatter and validation issues"
    ```

**Expected Outcome**: All documentation follows framework standards

**Time Estimate**: 20-40 minutes (depending on number of issues)

**Common Issues**:
- **Missing frontmatter**: Add YAML block with required fields
- **Wrong Diataxis type**: Use decision matrix to determine correct type
- **Broken links**: Update related: paths to match actual file locations
- **Failed test extraction**: Add test markers and assertions to code blocks

---

## 5. Integration with Other SAPs

### SAP-000 (sap-framework)

**Integration**: All SAP artifacts follow Diataxis framework

**Claude workflow**:
1. When creating new SAP, read SAP-000 artifact templates:
   ```bash
   Read docs/skilled-awareness/sap-framework/protocol-spec.md
   # Understand 5-artifact pattern
   ```
2. Create artifacts with frontmatter:
   ```yaml
   # capability-charter.md
   ---
   title: "Capability Charter: {SAP Name}"
   type: explanation
   sap_id: "SAP-XXX"
   ---

   # protocol-spec.md
   ---
   title: "Protocol Specification: {SAP Name}"
   type: reference
   sap_id: "SAP-XXX"
   ---

   # AGENTS.md
   ---
   title: "{SAP Name} - Agent Awareness"
   type: how-to
   sap_id: "SAP-XXX"
   ---
   ```
3. Validate all artifacts have frontmatter:
   ```bash
   Bash: python scripts/validate_frontmatter.py docs/skilled-awareness/{sap-name}/
   ```

---

### SAP-004 (testing-framework)

**Integration**: How-Tos extract to pytest tests

**Claude workflow**:
1. When writing How-To, enable test extraction:
   ```yaml
   ---
   test_extraction: true
   ---
   ```
2. Mark code blocks for extraction:
   ````markdown
   ```python
   # TEST: test_feature
   [code with assertions]
   ```
   ````
3. Extract and run tests:
   ```bash
   Bash: python scripts/extract_tests.py --input docs/user-docs/how-to/01-feature.md --output tests/extracted/
   Bash: pytest tests/extracted/test_feature.py
   ```

---

### SAP-009 (agent-awareness)

**Integration**: AGENTS.md files use frontmatter with progressive loading

**Claude workflow**:
1. When creating AGENTS.md, add progressive loading metadata:
   ```yaml
   ---
   title: "{SAP Name} - Agent Awareness"
   type: how-to
   sap_id: "SAP-XXX"
   progressive_loading:
     phase_1_quick_reference:
       sections: ["1. Quick Start", "2. What You Can Do"]
       estimated_tokens: 8000
       estimated_time_minutes: 5
     phase_2_implementation:
       sections: ["5. How It Works", "6. Key Workflows"]
       estimated_tokens: 25000
       estimated_time_minutes: 15
   ---
   ```
2. Structure content to match progressive loading phases
3. Add cross-references to related SAPs:
   ```yaml
   related_to:
     saps: ["SAP-000", "SAP-009", "SAP-015"]
   ```

---

## 6. Claude-Specific Tips

### Tip 1: Use Decision Matrix First, Write Second

**Pattern**:
```markdown
Step 1: User asks "Write docs for X"
Step 2: Apply decision matrix (Tutorial/How-To/Reference/Explanation)
Step 3: Write documentation with correct type in frontmatter
```

**Why**: Prevents wrong Diataxis type, saves refactoring time

**Don't**: Guess at type, always use decision matrix

---

### Tip 2: Read Existing Examples Before Writing

**Pattern**:
```markdown
Step 1: User asks "Write a Tutorial"
Step 2: Read existing tutorial for reference
Read docs/user-docs/tutorials/01-existing.md
Step 3: Follow same structure and frontmatter format
Write docs/user-docs/tutorials/02-new.md
```

**Why**: Consistent structure, correct frontmatter format

**Don't**: Write from scratch without checking examples

---

### Tip 3: Validate Immediately After Creating

**Pattern**:
```markdown
Step 1: Write documentation
Write docs/user-docs/tutorials/01-new.md

Step 2: Validate frontmatter immediately
Bash: python scripts/validate_frontmatter.py docs/user-docs/tutorials/01-new.md

Step 3: Fix issues before continuing
Edit docs/user-docs/tutorials/01-new.md
```

**Why**: Catch errors early, prevent accumulation

**Don't**: Write multiple docs before validating (errors compound)

---

### Tip 4: Extract Tests for All How-Tos with Code

**Pattern**:
```markdown
Step 1: Write How-To with code examples
Step 2: Enable test_extraction in frontmatter
Step 3: Mark code blocks with # TEST: test_name
Step 4: Extract tests immediately
Bash: python scripts/extract_tests.py --input [file] --output tests/extracted/
Step 5: Run tests to validate
Bash: pytest tests/extracted/ -v
```

**Why**: Keeps documentation accurate, prevents stale examples

**Don't**: Skip test extraction (documentation becomes outdated)

---

### Tip 5: Add Tags for Discoverability

**Pattern**:
```yaml
---
tags: ["mcp", "error-handling", "python", "debugging"]
---
```

Use controlled vocabulary from `.chora/conventions/tag-vocabulary.yaml`

**Why**: Better search, agent discovery, topic clustering

**Don't**: Use arbitrary tags (hard to search)

---

## 7. Common Pitfalls

### Pitfall 1: Wrong Diataxis Type

**Problem**: Writing Tutorial when user needs How-To (or vice versa)

**Symptom**:
- User confused about document purpose
- Content too long/short for type
- Feedback: "This doesn't answer my question"

**Fix**:
```markdown
Step 1: Re-evaluate user intent using decision matrix
Step 2: Edit frontmatter to correct type
Edit docs/user-docs/tutorials/wrong-type.md
# Change type: tutorial → type: how-to
Step 3: Refactor content to match type
Step 4: Move file to correct directory if needed
Bash: git mv docs/user-docs/tutorials/wrong-type.md docs/user-docs/how-to/
```

**Prevention**: Always use decision matrix before writing

---

### Pitfall 2: Missing Frontmatter

**Problem**: Creating documentation without YAML frontmatter

**Symptom**:
- Validation scripts fail
- Documentation not discoverable
- No metadata for agents

**Fix**:
```markdown
Step 1: Edit file to add frontmatter
Edit docs/user-docs/tutorials/missing-frontmatter.md

Step 2: Add YAML block at top
---
title: "Title Here"
type: tutorial
status: draft
audience: users
last_updated: 2025-11-05
---

Step 3: Validate
Bash: python scripts/validate_frontmatter.py docs/user-docs/tutorials/missing-frontmatter.md
```

**Prevention**: Always add frontmatter before content (frontmatter-first approach)

---

### Pitfall 3: Not Extracting Tests from How-Tos

**Problem**: Writing How-To with code examples but not extracting tests

**Symptom**:
- Code examples become stale
- Users report "code doesn't work"
- Documentation drifts from implementation

**Fix**:
```markdown
Step 1: Enable test extraction
Edit docs/user-docs/how-to/01-no-tests.md
# Add frontmatter: test_extraction: true

Step 2: Mark code blocks
# Add: # TEST: test_name

Step 3: Extract tests
Bash: python scripts/extract_tests.py --input docs/user-docs/how-to/01-no-tests.md --output tests/extracted/

Step 4: Run tests
Bash: pytest tests/extracted/ -v

Step 5: Fix if tests fail
Edit docs/user-docs/how-to/01-no-tests.md
# Update code examples
```

**Prevention**: Always enable test_extraction for How-Tos with code

---

### Pitfall 4: Broken Cross-References

**Problem**: Adding related: paths that don't exist

**Symptom**:
- Link validation fails
- Users click broken links
- Documentation navigation broken

**Fix**:
```markdown
Step 1: Validate links
Bash: python scripts/validate_links.py docs/

Step 2: Fix broken paths
Edit docs/user-docs/tutorials/01-broken-links.md
# Update related: field with correct paths

Step 3: Re-validate
Bash: python scripts/validate_links.py docs/
```

**Prevention**: Use Tab completion or Read tool to verify paths exist

---

### Pitfall 5: Mixing Content Types in One Document

**Problem**: Tutorial with How-To content, How-To with Explanation content

**Symptom**:
- Document too long or unfocused
- Users confused about purpose
- Content duplicated across docs

**Fix**:
```markdown
Step 1: Identify mixed content
Read docs/user-docs/tutorials/01-mixed-content.md
# Notice How-To and Explanation sections

Step 2: Split into separate documents
Write docs/user-docs/how-to/01-specific-task.md
# Extract How-To content

Write docs/user-docs/explanation/01-design-rationale.md
# Extract Explanation content

Step 3: Keep only Tutorial content in original
Edit docs/user-docs/tutorials/01-mixed-content.md
# Remove How-To and Explanation sections

Step 4: Add cross-references
Edit docs/user-docs/tutorials/01-mixed-content.md
# Add related: links to new docs
```

**Prevention**: Use decision matrix to keep content focused

---

## 8. Quick Reference

### Common Bash Commands

```bash
# Validate frontmatter
python scripts/validate_frontmatter.py docs/

# Extract tests from How-Tos
python scripts/extract_tests.py --input docs/user-docs/how-to/01-example.md --output tests/extracted/

# Run extracted tests
pytest tests/extracted/ -v

# Validate links
python scripts/validate_links.py docs/

# Check directory structure
ls docs/user-docs/tutorials/
ls docs/user-docs/how-to/
```

---

### Decision Matrix Quick Reference

| User Intent | Document Type |
|-------------|---------------|
| "Teach me to use X" | Tutorial |
| "Show me how to solve Y" | How-To |
| "What parameters does Z take?" | Reference |
| "Why does X work this way?" | Explanation |

---

### Required Frontmatter Template

```yaml
---
title: "Document Title"
type: tutorial  # or: how-to, reference, explanation
status: draft   # or: review, published, deprecated
audience: users # or: developers, maintainers
last_updated: 2025-11-05
---
```

---

## 9. Version History

**1.0.0** (2025-11-05):
- Initial CLAUDE.md for SAP-007 (documentation-framework)
- 3 workflows: create with frontmatter, extract tests, validate quality
- Integration with SAP-000, SAP-004, SAP-009
- 5 Claude-specific tips, 5 common pitfalls
- Tool usage patterns (Bash, Read, Write, Edit)

---

## Quick Links

- **AGENTS.md**: [AGENTS.md](AGENTS.md) - Generic agent patterns (5 workflows)
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete Diataxis reference
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Design rationale
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- **Scripts**: [../../scripts/](../../scripts/) - Validation and extraction tools

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for comprehensive workflow details
2. Read [protocol-spec.md](protocol-spec.md) for complete Diataxis specification
3. Read [adoption-blueprint.md](adoption-blueprint.md) for implementation steps
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
