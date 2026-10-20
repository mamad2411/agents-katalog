# Documentation Framework - Agent Awareness (SAP-007)

**SAP ID**: SAP-007
**Version**: 1.1.0
**Status**: Pilot
**Last Updated**: 2025-11-09

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "All agents (first-time orientation)"
  estimated_tokens: 8000
  estimated_time_minutes: 5
  sections:
    - "1. Quick Start for Agents"
    - "2. What You Can Do"
    - "3. When to Use This Capability"
    - "4. Common User Signals"

phase_2_implementation:
  target_audience: "Agents implementing documentation"
  estimated_tokens: 25000
  estimated_time_minutes: 15
  sections:
    - "5. How It Works"
    - "6. Key Workflows"
    - "7. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Agents debugging or customizing documentation"
  estimated_tokens: 50000
  estimated_time_minutes: 30
  files_to_read:
    - "protocol-spec.md (complete Diataxis framework specification)"
    - "capability-charter.md (design rationale)"
    - "scripts/extract_tests.py (test extraction implementation)"
    - "scripts/validate_frontmatter.py (validation implementation)"
```

---

## 📖 Quick Reference

**New to SAP-007?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 📚 **4 Document Types** - Tutorial, How-To, Reference, Explanation (Diátaxis framework)
- 🚀 **4 CLI Commands** - doc-structure, extract-doc-tests, doc-completeness, doc-to-bdd
- 🎓 **Decision Matrix** - When to use each document type
- 🔧 **Troubleshooting** - 3 common documentation problems

**This AGENTS.md provides**: Agent-executable workflows for organizing docs, extracting tests, and Documentation-First development.

---

## 1. Quick Start for Agents

### What is Documentation Framework? (60-second overview)

**Documentation Framework (SAP-007)** provides **Diataxis-based documentation structure** with:

- **4 Document Types**: Tutorial, How-To, Reference, Explanation (organized by user intent)
- **YAML Frontmatter**: Structured metadata with schema validation
- **Executable How-Tos**: Code examples extractable to pytest tests
- **Directory Organization**: user-docs/, dev-docs/, project-docs/
- **Test Extraction**: Automated pytest generation from How-To code blocks

**Purpose**: Standardize documentation structure for consistency, quality, and agent-friendliness.

**Key Benefits**:
- **Clear Structure**: Always know which doc type to use (Diataxis decision matrix)
- **Quality Standards**: Frontmatter validation ensures consistency
- **Executable Docs**: How-Tos become live tests (keep docs accurate)
- **Agent-Friendly**: Structured metadata enables agent reasoning

---

### When Should You Use This?

**Use Documentation Framework when**:
- User asks "how should I structure documentation?"
- Writing documentation for chora-base or SAPs
- Creating tutorials, how-tos, references, or explanations
- Need to extract tests from documentation
- Documentation quality varies or structure unclear

**Don't use Documentation Framework when**:
- Writing informal notes or brainstorming (not formal docs)
- Creating README-only projects (too simple for Diataxis)
- Documentation is purely auto-generated (API docs from docstrings)
- User explicitly wants different structure (Jekyll, Sphinx, etc.)

---

### Quick Command Reference

```bash
# Validate frontmatter
python scripts/validate_frontmatter.py docs/user-docs/

# Extract tests from How-Tos
python scripts/extract_tests.py --input docs/user-docs/how-to/01-example.md --output tests/

# Validate documentation structure
python scripts/validate_docs.py docs/

# Check for missing frontmatter fields
grep -r "^---$" docs/ -A 10 | grep -E "title:|type:|status:"
```

---

## 2. What You Can Do

### Core Capabilities

1. **Choose Correct Document Type** (Diataxis decision)
   - Tutorial: Teaching through step-by-step lessons
   - How-To: Solving specific problems
   - Reference: Technical specifications
   - Explanation: Design rationale and concepts

2. **Structure Documentation** (frontmatter + content)
   - Add YAML frontmatter with required fields
   - Organize content by Diataxis type
   - Use proper directory structure (user-docs/, dev-docs/, project-docs/)

3. **Write Executable How-Tos** (test extraction)
   - Mark code blocks for test extraction
   - Use pytest-compatible syntax
   - Generate tests with scripts/extract_tests.py

4. **Validate Documentation** (quality checks)
   - Validate frontmatter schema
   - Check Diataxis type consistency
   - Verify test extraction works

5. **Organize by Audience** (directory structure)
   - user-docs/: End-user documentation
   - dev-docs/: Developer documentation
   - project-docs/: Project management documentation

---

### Integration Points

**SAP-000 (sap-framework)**:
- All SAP artifacts follow Diataxis framework
- capability-charter.md = Explanation
- protocol-spec.md = Reference
- awareness-guide.md = How-To (or AGENTS.md)
- adoption-blueprint.md = Tutorial

**SAP-004 (testing-framework)**:
- How-Tos extract to pytest tests
- Documentation examples become test cases
- Test extraction validates documentation accuracy

**SAP-009 (agent-awareness)**:
- AGENTS.md files use frontmatter schema
- Progressive loading metadata enables phased context loading
- Cross-references link related SAPs

**SAP-012 (development-lifecycle)**:
- Documentation-Driven Development (DDD) workflow
- Write docs before code
- Docs define contracts, code implements

---

## 3. When to Use This Capability

### User Signal Pattern: Documentation Structure

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "How should I document this feature?" | Needs Diataxis guidance | Recommend document type using decision matrix |
| "Write a tutorial for X" | Tutorial request | Create step-by-step learning document |
| "Need API documentation" | Reference request | Create Reference doc with schema/parameters |
| "Explain why we chose X" | Explanation request | Create Explanation doc with rationale |
| "How do I solve Y?" | How-To request | Create task-oriented solution guide |

---

### User Signal Pattern: Documentation Quality

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "Documentation is inconsistent" | Missing standards | Apply frontmatter schema, validate structure |
| "How-To examples don't work" | Stale documentation | Extract tests, run automated validation |
| "Can't find relevant docs" | Missing metadata | Add tags, cross-references in frontmatter |
| "Docs duplicated across types" | Diataxis confusion | Refactor using decision matrix |
| "Need to validate docs" | Quality check needed | Run frontmatter validation script |

---

## 4. Common User Signals

### Signal 1: "Should I write a Tutorial or How-To?"

**Context**: User unsure which Diataxis type to use

**Agent Response**:
1. Ask clarifying questions:
   - **Learning-oriented?** → Tutorial (teach concepts step-by-step)
   - **Problem-solving?** → How-To (solve specific task)
   - **Reference lookup?** → Reference (API/schema/config)
   - **Understanding design?** → Explanation (rationale/architecture)

2. Use decision matrix:
   ```
   User Intent              → Document Type
   ─────────────────────────────────────────
   "Teach me to use X"      → Tutorial
   "Show me how to solve Y" → How-To
   "What parameters does Z take?" → Reference
   "Why does X work this way?" → Explanation
   ```

3. Provide examples:
   - Tutorial: "Build your first MCP server" (step-by-step learning)
   - How-To: "Add custom error handling to MCP server" (specific task)
   - Reference: "MCP Protocol Schema" (technical specification)
   - Explanation: "Why we use Diataxis" (design rationale)

**Expected Outcome**: User writes correct Diataxis type

---

### Signal 2: "What frontmatter fields are required?"

**Context**: User writing documentation without frontmatter or with incomplete frontmatter

**Agent Response**:
1. Provide required frontmatter template:
   ```yaml
   ---
   title: "Document Title"
   type: tutorial  # or: how-to, reference, explanation
   status: draft   # or: review, published, deprecated
   audience: users # or: developers, maintainers
   last_updated: 2025-11-05
   ---
   ```

2. Explain optional fields:
   ```yaml
   # Optional but recommended
   tags: ["keyword1", "keyword2"]
   version: "1.0.0"
   related: ["path/to/related-doc.md"]
   test_extraction: true  # For How-Tos only
   ```

3. Validate after adding:
   ```bash
   python scripts/validate_frontmatter.py docs/user-docs/my-doc.md
   ```

**Expected Outcome**: Documentation has complete, valid frontmatter

---

### Signal 3: "How do I make my How-To executable?"

**Context**: User wants code examples to become pytest tests

**Agent Response**:
1. Add test_extraction frontmatter:
   ```yaml
   ---
   title: "How to Add Error Handling"
   type: how-to
   test_extraction: true  # Enable test extraction
   ---
   ```

2. Mark code blocks for extraction:
   ````markdown
   ```python
   # TEST: test_custom_error_handler
   def custom_error_handler(error: Exception) -> dict:
       return {"error": str(error)}

   # Verify error handling
   result = custom_error_handler(ValueError("test"))
   assert result == {"error": "test"}
   ```
   ````

3. Extract tests:
   ```bash
   python scripts/extract_tests.py \
     --input docs/user-docs/how-to/01-error-handling.md \
     --output tests/extracted/
   ```

4. Verify tests work:
   ```bash
   pytest tests/extracted/test_custom_error_handler.py
   ```

**Expected Outcome**: How-To code examples become live pytest tests

---

### Signal 4: "Where should API documentation go?"

**Context**: User unsure about directory structure

**Agent Response**:
1. Determine audience:
   - **End users** (using API as consumers) → `user-docs/reference/`
   - **Developers** (implementing API) → `dev-docs/reference/`
   - **Project maintainers** (API design decisions) → `project-docs/`

2. Determine document type:
   - **API parameters, schemas** → Reference (`reference/api-spec.md`)
   - **Using the API** → How-To (`how-to/01-call-api.md`)
   - **API design rationale** → Explanation (`explanation/api-design.md`)

3. Provide file path:
   ```
   # API reference for end users
   user-docs/reference/api-spec.md

   # Developer API implementation guide
   dev-docs/how-to/01-implement-api-endpoint.md

   # API architecture explanation
   dev-docs/explanation/api-architecture.md
   ```

**Expected Outcome**: Documentation in correct directory with correct type

---

### Signal 5: "Documentation quality varies across docs"

**Context**: Inconsistent frontmatter, structure, or quality

**Agent Response**:
1. Run frontmatter validation:
   ```bash
   python scripts/validate_frontmatter.py docs/
   # Output: Missing fields, invalid types, etc.
   ```

2. Fix common issues:
   - **Missing frontmatter**: Add YAML block with required fields
   - **Wrong type field**: Use Diataxis decision matrix to correct
   - **Missing tags**: Add keywords from `.chora/conventions/tag-vocabulary.yaml`
   - **No last_updated**: Add current date

3. Validate Diataxis consistency:
   ```bash
   # Check if Tutorials are actually learning-oriented
   grep -A 50 "^type: tutorial" docs/user-docs/tutorials/*.md
   # Review content structure
   ```

4. Standardize formatting:
   - Use consistent heading levels
   - Add table of contents for long docs
   - Include examples and code blocks
   - Add cross-references to related docs

**Expected Outcome**: Consistent documentation quality across all docs

---

## 5. How It Works

### Architecture Overview

Documentation Framework uses **Diataxis methodology** with **frontmatter validation** and **test extraction**:

```
Documentation Files (Markdown)
         ↓
YAML Frontmatter (metadata: type, status, audience, tags)
         ↓
Content (structured by Diataxis type)
         ↓
Code Blocks (in How-Tos, marked for test extraction)
         ↓
Test Extraction Script (scripts/extract_tests.py)
         ↓
Pytest Tests (tests/extracted/)
         ↓
CI Runs Tests (validates documentation accuracy)
```

---

### The Four Diataxis Types

**1. Tutorial (Learning-oriented)**:
- **User Intent**: "Teach me how to use this"
- **Structure**: Step-by-step lessons with expected output
- **Example**: "Build your first MCP server"
- **Characteristics**: Sequential, guided, complete workflow

**2. How-To Guide (Task-oriented)**:
- **User Intent**: "Show me how to solve X"
- **Structure**: Problem → Solution with variations
- **Example**: "How to add custom error handling"
- **Characteristics**: Goal-driven, practical, assumes knowledge

**3. Reference (Information-oriented)**:
- **User Intent**: "What parameters does this take?"
- **Structure**: API docs, schemas, configurations
- **Example**: "MCP Protocol Schema Reference"
- **Characteristics**: Structured, complete, technical

**4. Explanation (Understanding-oriented)**:
- **User Intent**: "Why does this work this way?"
- **Structure**: Context, rationale, trade-offs
- **Example**: "Why we use Diataxis for documentation"
- **Characteristics**: Conceptual, background, discussion

---

### Directory Structure

```
project-root/
├── user-docs/           # User-facing documentation
│   ├── tutorials/       # Learning-oriented (Tutorial)
│   ├── how-to/          # Task-oriented (How-To)
│   ├── reference/       # Information-oriented (Reference)
│   ├── explanation/     # Understanding-oriented (Explanation)
│   ├── AGENTS.md        # Quick reference for agents
│   └── README.md        # User docs index

├── dev-docs/            # Developer documentation
│   ├── workflows/       # Development processes (DDD, BDD, TDD)
│   ├── vision/          # Long-term plans, capability evolution
│   ├── examples/        # Code examples, walkthroughs
│   ├── AGENTS.md        # Quick reference for agents
│   └── README.md        # Dev docs index

└── project-docs/        # Project management
    ├── sprints/         # Sprint planning, retrospectives
    ├── releases/        # Release planning, upgrade guides
    ├── metrics/         # Process metrics, velocity tracking
    ├── AGENTS.md        # Quick reference for agents
    └── README.md        # Project docs index
```

---

### Frontmatter Schema

**Required Fields**:
```yaml
---
title: String              # Document title
type: Enum                 # tutorial | how-to | reference | explanation
status: Enum               # draft | review | published | deprecated
audience: Enum             # users | developers | maintainers
last_updated: Date         # YYYY-MM-DD
---
```

**Optional Fields**:
```yaml
version: SemVer            # Document version (e.g., "1.0.0")
tags: [String]             # Keywords for search
test_extraction: Boolean   # Enable test extraction (How-Tos only)
related: [String]          # Related doc paths
sap_id: String             # SAP ID if doc is part of SAP
complexity: Enum           # beginner | intermediate | advanced
```

---

### Test Extraction Workflow

**How test extraction works**:

1. **Write executable How-To** with test-marked code blocks:
   ````markdown
   ```python
   # TEST: test_example_function
   def example_function(x: int) -> int:
       return x * 2

   assert example_function(5) == 10
   ```
   ````

2. **Run extraction script**:
   ```bash
   python scripts/extract_tests.py \
     --input docs/user-docs/how-to/01-example.md \
     --output tests/extracted/
   ```

3. **Script generates pytest test file**:
   ```python
   # tests/extracted/test_example_function.py
   def test_example_function():
       def example_function(x: int) -> int:
           return x * 2

       assert example_function(5) == 10
   ```

4. **CI runs tests** to validate documentation accuracy:
   ```bash
   pytest tests/extracted/
   ```

---

## 6. Key Workflows

### Workflow 1: Choose Correct Diataxis Type

**Goal**: Determine which document type to write

**Steps**:

1. **Understand user intent**:
   - What is the user trying to accomplish?
   - Learning (Tutorial), Solving (How-To), Looking up (Reference), Understanding (Explanation)

2. **Use decision matrix**:

   | User Question | Document Type |
   |---------------|---------------|
   | "How do I get started?" | Tutorial |
   | "How do I solve X?" | How-To |
   | "What are the parameters?" | Reference |
   | "Why does this work?" | Explanation |

3. **Check content characteristics**:

   **Tutorial**:
   - Step-by-step instructions
   - Expected output at each step
   - Complete workflow from start to finish
   - Assumes no prior knowledge

   **How-To**:
   - Goal-oriented (solve specific problem)
   - Assumes prior knowledge
   - Multiple approaches or variations
   - Practical, concise

   **Reference**:
   - Technical specifications
   - API parameters, schemas, configurations
   - Structured, complete, no narrative
   - Lookup-friendly

   **Explanation**:
   - Conceptual background
   - Design rationale, trade-offs
   - Broader context
   - Discussion-oriented

4. **Verify decision**:
   - Does content fit the type?
   - Is content duplicated in other type? (Refactor if yes)
   - Is user intent clear? (Adjust if not)

5. **Set frontmatter type**:
   ```yaml
   ---
   type: tutorial  # or: how-to, reference, explanation
   ---
   ```

**Expected Outcome**: Documentation type matches user intent and content

**Time Estimate**: 2-5 minutes

---

### Workflow 2: Add and Validate Frontmatter

**Goal**: Add complete YAML frontmatter to documentation

**Steps**:

1. **Start with required fields**:
   ```yaml
   ---
   title: "How to Add Error Handling to MCP Server"
   type: how-to
   status: draft
   audience: developers
   last_updated: 2025-11-05
   ---
   ```

2. **Add optional metadata** (if applicable):
   ```yaml
   # For How-Tos with code examples
   test_extraction: true

   # For discoverability
   tags: ["mcp", "error-handling", "python"]

   # For cross-references
   related: ["docs/user-docs/tutorials/01-first-mcp-server.md"]

   # For SAP documentation
   sap_id: "SAP-014"

   # For skill level
   complexity: intermediate
   ```

3. **Validate frontmatter**:
   ```bash
   python scripts/validate_frontmatter.py docs/user-docs/how-to/01-error-handling.md
   ```

4. **Fix validation errors**:
   - **Missing required field**: Add field
   - **Invalid type value**: Use allowed values (tutorial, how-to, reference, explanation)
   - **Invalid status value**: Use allowed values (draft, review, published, deprecated)
   - **Invalid date format**: Use YYYY-MM-DD

5. **Verify validation passes**:
   ```bash
   python scripts/validate_frontmatter.py docs/user-docs/how-to/01-error-handling.md
   # Output: Frontmatter valid ✓
   ```

6. **Commit documentation**:
   ```bash
   git add docs/user-docs/how-to/01-error-handling.md
   git commit -m "docs: Add How-To for error handling (SAP-014)"
   ```

**Expected Outcome**: Documentation has complete, valid frontmatter

**Time Estimate**: 3-5 minutes

---

### Workflow 3: Write Executable How-To with Test Extraction

**Goal**: Create How-To documentation with extractable pytest tests

**Steps**:

1. **Enable test extraction in frontmatter**:
   ```yaml
   ---
   title: "How to Add Custom Error Handler"
   type: how-to
   test_extraction: true  # Enable test extraction
   last_updated: 2025-11-05
   ---
   ```

2. **Write problem statement**:
   ```markdown
   ## Problem

   You need to add a custom error handler to your MCP server to format error responses consistently.
   ```

3. **Write solution with test-marked code**:
   ````markdown
   ## Solution

   Create a custom error handler function:

   ```python
   # TEST: test_custom_error_handler
   def custom_error_handler(error: Exception) -> dict:
       """Format errors consistently."""
       return {
           "error": type(error).__name__,
           "message": str(error),
           "severity": "high"
       }

   # Verify error handling
   test_error = ValueError("Invalid input")
   result = custom_error_handler(test_error)
   assert result["error"] == "ValueError"
   assert result["message"] == "Invalid input"
   assert result["severity"] == "high"
   ```
   ````

4. **Extract tests**:
   ```bash
   python scripts/extract_tests.py \
     --input docs/user-docs/how-to/01-error-handling.md \
     --output tests/extracted/
   ```

5. **Verify tests work**:
   ```bash
   pytest tests/extracted/test_custom_error_handler.py -v
   # Output: test_custom_error_handler PASSED
   ```

6. **If tests fail, fix documentation**:
   - Update code examples in How-To
   - Re-extract tests
   - Re-run pytest
   - Iterate until tests pass

7. **Commit documentation and tests**:
   ```bash
   git add docs/user-docs/how-to/01-error-handling.md tests/extracted/
   git commit -m "docs: Add executable How-To for error handling"
   ```

**Expected Outcome**: How-To documentation becomes live pytest tests

**Time Estimate**: 10-20 minutes

---

### Workflow 4: Enforce SAP-007 Structure (Level 3)

**Goal**: Install and use validation enforcement to maintain documentation structure

**Steps**:

1. **Copy validation script to your project**:
   ```bash
   # From chora-base template
   mkdir -p scripts/
   cp docs/skilled-awareness/documentation-framework/templates/validate-sap-007-structure.py scripts/
   ```

2. **Customize validation rules** (edit `scripts/validate-sap-007-structure.py`):
   ```python
   # ALLOWED_ROOT_FILES - add project-specific exceptions
   ALLOWED_ROOT_FILES = [
       "README.md",
       "AGENTS.md",
       "CLAUDE.md",
       "CHANGELOG.md",
       "CONTRIBUTING.md",
       "LICENSE.md",
       "DOCUMENTATION_STANDARD.md",
       "ROADMAP.md",
       # Add your project-specific root files here
       "YOUR_PROJECT_FILE.md",  # Document rationale in AGENTS.md
   ]

   # REQUIRED_PROJECT_DOCS_SUBDIRS - customize for your project
   REQUIRED_PROJECT_DOCS_SUBDIRS = [
       "sprints",
       "releases",
       "metrics",
       "decisions",
       "retrospectives",
       # Add your project-specific subdirectories
   ]
   ```

3. **Run manual validation**:
   ```bash
   python scripts/validate-sap-007-structure.py
   # Check for violations before installing hook
   ```

4. **Fix any existing violations**:
   ```bash
   # If validation fails, move files to appropriate directories
   # Use decision tree: docs/skilled-awareness/documentation-framework/decision-tree-template.md
   mv ROOT_VIOLATION.md project-docs/sprints/  # Example
   ```

5. **Install pre-commit hook** (prevents future violations):
   ```bash
   # Option 1: Install to .git/hooks/
   mkdir -p .git/hooks
   cp docs/skilled-awareness/documentation-framework/templates/sap-007-check.sh .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit

   # Option 2: Install to .githooks/ (team projects)
   mkdir -p .githooks
   cp docs/skilled-awareness/documentation-framework/templates/sap-007-check.sh .githooks/pre-commit
   chmod +x .githooks/pre-commit
   git config core.hooksPath .githooks
   ```

6. **Test pre-commit hook**:
   ```bash
   # Create intentional violation
   echo "# Test" > TEST_VIOLATION.md
   git add TEST_VIOLATION.md
   git commit -m "test hook"
   # Should fail with SAP-007 validation error

   # Clean up test
   git reset HEAD TEST_VIOLATION.md
   rm TEST_VIOLATION.md
   ```

7. **Add decision tree to AGENTS.md files**:
   ```bash
   # Copy template to your project
   # Add to root AGENTS.md, dev-docs/AGENTS.md, user-docs/AGENTS.md, project-docs/AGENTS.md
   # Customize [PROJECT_SPECIFIC] placeholders
   ```

8. **Verify enforcement is active**:
   ```bash
   # Validation script exists
   test -f scripts/validate-sap-007-structure.py && echo "✓ Validation script ready"

   # Pre-commit hook installed
   test -f .git/hooks/pre-commit && echo "✓ Pre-commit hook installed"
   # OR: test -f .githooks/pre-commit && echo "✓ Pre-commit hook installed"
   ```

**SAP-031 Integration**:
This workflow implements SAP-031 (Discoverability-Based Enforcement) for SAP-007:
- **Layer 1 (Discoverability)**: Decision tree in AGENTS.md (where agents look)
- **Layer 2 (Pre-Commit)**: Validation hook catches violations before commit
- **Layer 4 (Documentation)**: This workflow itself documents enforcement

See: [docs/skilled-awareness/discoverability-based-enforcement/](../discoverability-based-enforcement/)

**Expected Outcome**: SAP-007 structure violations blocked automatically by pre-commit hook

**Time Estimate**: 15-30 minutes (one-time setup)

**Prevention Rate**: 90%+ (proven in chora-workspace pilot)

---

### Workflow 5: Refactor Duplicated Documentation

**Goal**: Remove duplication by applying Diataxis structure

**Steps**:

1. **Identify duplication**:
   ```bash
   # Search for similar content across docs
   grep -r "custom error handler" docs/
   # Output shows same content in Tutorial and How-To
   ```

2. **Analyze each occurrence**:
   - **Tutorial**: Step-by-step error handling as part of building MCP server
   - **How-To**: Focused task: add error handler to existing server
   - **Explanation**: Why error handling matters (architectural rationale)

3. **Apply Diataxis decision matrix**:
   - **Tutorial**: Keep error handling as Step 5 in "Build MCP Server" tutorial
   - **How-To**: Focus on standalone error handler task (assumes server exists)
   - **Explanation**: Move design rationale to separate Explanation doc

4. **Refactor content**:

   **Tutorial** (keep contextual error handling):
   ```markdown
   ## Step 5: Add Error Handling

   Now that your server is running, add error handling...
   [Step-by-step with expected output]
   ```

   **How-To** (focus on specific task):
   ```markdown
   ## How to Add Custom Error Handler

   **Prerequisites**: Existing MCP server

   **Solution**:
   1. Define error handler function
   2. Register with server
   3. Test error scenarios
   ```

   **Explanation** (design rationale):
   ```markdown
   ## Why Error Handling Matters in MCP Servers

   Error handling is critical for MCP servers because...
   [Discussion of trade-offs, design decisions]
   ```

5. **Add cross-references** in frontmatter:
   ```yaml
   # Tutorial frontmatter
   related:
     - "docs/user-docs/how-to/01-error-handling.md"
     - "docs/user-docs/explanation/error-handling-rationale.md"
   ```

6. **Verify no duplication**:
   ```bash
   grep -r "custom error handler" docs/ | wc -l
   # Should be lower count (content refactored)
   ```

**Expected Outcome**: Content organized by Diataxis type, no duplication

**Time Estimate**: 20-40 minutes

---

### Workflow 5: Validate Documentation Structure

**Goal**: Ensure documentation follows framework standards

**Steps**:

1. **Validate frontmatter across all docs**:
   ```bash
   python scripts/validate_frontmatter.py docs/
   # Output: List of files with invalid/missing frontmatter
   ```

2. **Fix frontmatter issues**:
   - **Missing required fields**: Add title, type, status, audience, last_updated
   - **Invalid type**: Change to tutorial, how-to, reference, or explanation
   - **Invalid status**: Change to draft, review, published, or deprecated

3. **Validate directory structure**:
   ```bash
   # Check if Tutorials are in tutorials/
   ls docs/user-docs/tutorials/*.md

   # Check if How-Tos are in how-to/
   ls docs/user-docs/how-to/*.md

   # Verify type matches directory
   grep -r "^type: tutorial" docs/user-docs/tutorials/*.md
   grep -r "^type: how-to" docs/user-docs/how-to/*.md
   ```

4. **Validate test extraction**:
   ```bash
   # Find How-Tos with test_extraction enabled
   grep -r "test_extraction: true" docs/user-docs/how-to/*.md

   # Extract tests
   python scripts/extract_tests.py --input docs/user-docs/how-to/ --output tests/extracted/

   # Run tests
   pytest tests/extracted/ -v
   ```

5. **Check for broken cross-references**:
   ```bash
   # Validate related doc paths exist
   python scripts/validate_links.py docs/
   ```

6. **Generate documentation quality report**:
   ```bash
   python scripts/doc_quality_report.py docs/
   # Output: Summary of documentation health
   # - % docs with valid frontmatter
   # - % How-Tos with test extraction
   # - % docs with tags
   # - Average complexity level
   ```

**Expected Outcome**: All documentation follows framework standards

**Time Estimate**: 15-30 minutes

---

## 7. Integration with Other SAPs

### SAP-000 (sap-framework)

**Integration**: All SAP artifacts follow Diataxis framework

**SAP Artifact Mapping**:
- **capability-charter.md** → Explanation (design rationale)
- **protocol-spec.md** → Reference (technical specification)
- **awareness-guide.md / AGENTS.md** → How-To (task execution)
- **adoption-blueprint.md** → Tutorial (step-by-step adoption)
- **ledger.md** → Reference (adoption metrics)

**Agent workflow**:
1. When creating new SAP, use Diataxis for all 5 artifacts
2. Add frontmatter to each artifact with `sap_id` field
3. Validate frontmatter before committing
4. Extract tests from awareness-guide.md if applicable

---

### SAP-004 (testing-framework)

**Integration**: How-Tos extract to pytest tests

**Testing workflow**:
1. Write How-To with executable code blocks
2. Mark code blocks with `# TEST: test_name`
3. Extract tests with `scripts/extract_tests.py`
4. Run tests in CI to validate documentation

**Agent workflow**:
1. When writing How-To, add `test_extraction: true` to frontmatter
2. Include assertions in code examples
3. Extract tests and verify they pass
4. Commit both documentation and generated tests

---

### SAP-009 (agent-awareness)

**Integration**: AGENTS.md files use frontmatter schema

**Awareness pattern**:
- AGENTS.md files have frontmatter with progressive loading metadata
- Cross-references link related SAPs
- Tags enable agent discovery

**Agent workflow**:
1. When creating AGENTS.md, add frontmatter:
   ```yaml
   ---
   title: "Quality Gates - Agent Awareness"
   type: how-to
   sap_id: "SAP-006"
   progressive_loading:
     phase_1_quick_reference:
       sections: ["1. Quick Start", "2. What You Can Do"]
       estimated_tokens: 8000
     phase_2_implementation:
       sections: ["5. How It Works", "6. Key Workflows"]
       estimated_tokens: 25000
   ---
   ```
2. Use progressive loading hints to guide context loading

---

### SAP-012 (development-lifecycle)

**Integration**: Documentation-Driven Development (DDD) workflow

**DDD process**:
1. **Write Tutorial** (how feature should work from user perspective)
2. **Write How-To** (specific tasks user will perform)
3. **Write Reference** (API contracts, schemas)
4. **Implement code** (guided by documentation contracts)
5. **Extract tests** (from How-Tos to validate implementation)

**Agent workflow**:
1. Before implementing feature, write documentation first
2. Use documentation to define contracts
3. Implement code to match documentation
4. Extract tests to validate alignment

---

## 8. Best Practices

### Best Practice 1: Write Documentation Before Code (DDD)

**Why**: Documentation defines contracts, code implements them

**How**:
1. Write Tutorial (user perspective)
2. Write How-To (task walkthrough)
3. Write Reference (API spec)
4. Implement code
5. Extract tests from How-To

**Benefit**: Clear requirements, testable documentation, fewer bugs

---

### Best Practice 2: Use Diataxis Decision Matrix Consistently

**Why**: Prevents content duplication and confusion

**How**:
- Always ask "What is user intent?"
- Use matrix to choose type
- Refactor if content doesn't match type

**Don't**: Mix Tutorial content in How-To (causes confusion)

**Benefit**: Clear structure, no duplication

---

### Best Practice 3: Enable Test Extraction for All How-Tos

**Why**: Keeps documentation accurate and up-to-date

**How**:
1. Add `test_extraction: true` to frontmatter
2. Mark code blocks with `# TEST: test_name`
3. Extract and run tests regularly
4. Fix documentation if tests fail

**Benefit**: Documentation stays synchronized with code

---

### Best Practice 4: Add Tags for Discoverability

**Why**: Agents and users need to find relevant docs

**How**:
```yaml
---
tags: ["mcp", "error-handling", "python", "debugging"]
---
```

Use controlled vocabulary from `.chora/conventions/tag-vocabulary.yaml`

**Benefit**: Better search, agent discovery

---

### Best Practice 5: Cross-Reference Related Documentation

**Why**: Helps users navigate documentation landscape

**How**:
```yaml
---
related:
  - "docs/user-docs/tutorials/01-first-mcp-server.md"
  - "docs/user-docs/explanation/error-handling-rationale.md"
---
```

**Benefit**: Users find related content, understand broader context

---

## 9. Common Pitfalls

### Pitfall 1: Mixing Diataxis Types

**Problem**: Tutorial with How-To content, How-To with Explanation content

**Symptom**:
- User confused about document purpose
- Content duplicated across types
- Documentation too long or unfocused

**Fix**:
- Use decision matrix to identify correct type
- Refactor content by splitting into multiple docs
- Add cross-references between related docs

**Prevention**: Always validate type matches content before committing

---

### Pitfall 2: Missing or Invalid Frontmatter

**Problem**: Documentation without frontmatter or with incomplete metadata

**Symptom**:
- Validation scripts fail
- Tags missing, docs not discoverable
- Can't track documentation status (draft vs published)

**Fix**:
```bash
# Validate frontmatter
python scripts/validate_frontmatter.py docs/

# Add missing fields
Edit doc.md
# Add required frontmatter
```

**Prevention**: Use frontmatter template, validate before committing

---

### Pitfall 3: How-Tos Without Test Extraction

**Problem**: Code examples in How-Tos not tested, documentation becomes stale

**Symptom**:
- Code examples don't work
- Users report "documentation is wrong"
- Examples use deprecated APIs

**Fix**:
1. Add `test_extraction: true` to frontmatter
2. Mark code blocks with `# TEST: test_name`
3. Extract and run tests
4. Fix examples if tests fail

**Prevention**: Enable test extraction for all How-Tos by default

---

### Pitfall 4: Documentation in Wrong Directory

**Problem**: User docs in dev-docs/, dev docs in user-docs/

**Symptom**:
- Users find technical implementation details (too complex)
- Developers find user-facing tutorials (not detailed enough)

**Fix**:
- **User-facing** (end users) → `user-docs/`
- **Developer-facing** (contributors) → `dev-docs/`
- **Project management** (maintainers) → `project-docs/`

**Prevention**: Clarify audience before choosing directory

---

### Pitfall 5: Duplicated Content Across Types

**Problem**: Same information in Tutorial, How-To, and Explanation

**Symptom**:
- Maintenance burden (update 3 places)
- Inconsistency (one doc updated, others not)
- Confusion (which doc is authoritative?)

**Fix**:
- Refactor using Diataxis:
  - Tutorial: Step-by-step learning context
  - How-To: Focused task solution
  - Explanation: Design rationale only
- Add cross-references
- Remove duplicates

**Prevention**: Use decision matrix to identify primary location, link from others

---

## 10. Self-Evaluation

### Workflow Coverage Analysis

**Protocol Spec Workflows**: 6 (specified in protocol-spec.md)
1. Choose Diataxis type (decision matrix)
2. Add frontmatter (YAML schema)
3. Write executable How-To (test extraction)
4. Validate documentation (frontmatter, structure)
5. Organize by directory (user/dev/project docs)
6. Enforce structure (Level 3 validation) - NEW in v1.1.0

**AGENTS.md Workflows**: 6 (implemented above)
1. Choose Correct Diataxis Type
2. Add and Validate Frontmatter
3. Write Executable How-To with Test Extraction
4. Enforce SAP-007 Structure (Level 3) - NEW in v1.1.0
5. Refactor Duplicated Documentation
6. Validate Documentation Structure

**CLAUDE.md Workflows**: 3 (to be implemented in CLAUDE.md)
1. Create Documentation with Frontmatter (Write tool)
2. Extract and Run Tests from How-Tos (Bash + Read tools)
3. Validate and Fix Documentation Quality (Bash + Edit tools)

**Coverage**: 6/6 = 100% (all protocol-spec workflows covered)

**Variance**: 50% (6 generic workflows vs 3 Claude-specific workflows)

**Rationale**: CLAUDE.md focuses on tool-specific patterns (Bash/Read/Write/Edit), while AGENTS.md provides comprehensive guidance applicable to all agents. Both provide equivalent support for SAP-007 adoption.

**Conclusion**: ✅ Equivalent support across agent types

---

## 11. Version History

**1.1.0** (2025-11-09):
- Added Workflow 4: Enforce SAP-007 Structure (Level 3) - COORD-2025-011
- Added SAP-031 integration (Discoverability-Based Enforcement)
- Added references to validation templates (validate-sap-007-structure.py, sap-007-check.sh)
- Added decision tree template reference
- Total workflows: 5 → 6
- Status: Draft → Pilot

**1.0.0** (2025-11-05):
- Initial AGENTS.md for SAP-007 (documentation-framework)
- 5 workflows: Diataxis type selection, frontmatter, test extraction, refactoring, validation
- Integration with SAP-000, SAP-004, SAP-009, SAP-012
- 5 best practices, 5 common pitfalls
- Progressive context loading frontmatter

---

## Quick Links

- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete Diataxis framework reference
- **Capability Charter**: [capability-charter.md](capability-charter.md) - Design rationale
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- **Validation Script Template**: [templates/validate-sap-007-structure.py](templates/validate-sap-007-structure.py) - NEW in v1.1.0
- **Pre-Commit Hook Template**: [templates/sap-007-check.sh](templates/sap-007-check.sh) - NEW in v1.1.0
- **Decision Tree Template**: [decision-tree-template.md](decision-tree-template.md) - NEW in v1.1.0
- **SAP-031 Enforcement**: [../discoverability-based-enforcement/](../discoverability-based-enforcement/) - Enforcement methodology
- **Test Extraction Script**: [../../scripts/extract_tests.py](../../scripts/extract_tests.py)
- **Frontmatter Validation**: [../../scripts/validate_frontmatter.py](../../scripts/validate_frontmatter.py)

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code tool patterns
2. Read [protocol-spec.md](protocol-spec.md) for complete Diataxis specification
3. Read [adoption-blueprint.md](adoption-blueprint.md) for implementation steps
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
