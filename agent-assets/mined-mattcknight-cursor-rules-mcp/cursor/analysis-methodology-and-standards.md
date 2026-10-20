---
description: Analysis methodology and quality standards - thorough, holistic, fact-based analysis with 90%+ accuracy gates
alwaysApply: false
tags: [development, analysis, methodology, quality-gates, accuracy, standards]
priority: 1
version: 2.0.0
consolidatedFrom: [analysis-methodology.mdc, persona-analysis-quality-gates.mdc]
---

# Analysis Methodology & Quality Standards

**Mandatory principles and quality gates for all analysis work.**

**Priority:** 🔴 CRITICAL  
**Applies To:** ALL source code analysis, impact analysis, verification work, persona analysis  
**Status:** MANDATORY - No exceptions

---

## Core Motto

> **"Be thorough, holistic, fact-based, careful, cautious, no assumptions."**

This motto is **NON-NEGOTIABLE** for all analysis work. Every analysis task must demonstrate adherence to these principles.

---

## Section 1: Analysis Principles

### 1. Thorough
- Analyze ALL relevant files, not just samples
- Search exhaustively for patterns
- Verify edge cases
- Document what was checked, not just what was found

**Example:**
- ✅ GOOD: "Searched all 171 files for pattern X → 0 found"
- ❌ BAD: "Checked a few files, they look fine"

---

### 2. Holistic
- Consider the entire system, not isolated components
- Trace dependencies across layers (API → Jobs → Database → Reports)
- Identify all integration points
- Think about downstream impacts

**Example:**
- ✅ GOOD: "Analyzed API endpoints, scheduled jobs, AND database queries"
- ❌ BAD: "Checked the main file, should be good"

---

### 3. Fact-Based
- Use actual code inspection, not guesses
- Count files programmatically
- Quote line numbers and code snippets
- Cite sources (file paths, line numbers)

**Example:**
- ✅ GOOD: "Line 204-206 in FileA.php: `if ($amount > 0) {`"
- ❌ BAD: "The code probably has an amount filter"

---

### 4. Careful
- Double-check counts and numbers
- Verify aliases in queries
- Test regex patterns before claiming "no matches"
- Read full context, not just snippets

**Example:**
- ✅ GOOD: "Verified pattern in ALL 170 files (170/170)"
- ❌ BAD: "Pattern seems consistent across files"

---

### 5. Cautious
- State confidence levels (HIGH, MEDIUM, LOW)
- Flag uncertainties explicitly
- Recommend verification steps when unsure
- Don't extrapolate from limited samples

**Example:**
- ✅ GOOD: "Confidence Level: 🟢 HIGH (exhaustive analysis completed)"
- ❌ BAD: "Everything looks fine"

---

### 6. No Assumptions
- **NEVER** assume without verification
- If uncertain, state: "⚠️ UNVERIFIED: [topic] - requires manual inspection"
- Provide verification commands when making statements
- Test hypotheses with actual searches

**Example:**
- ✅ GOOD: "⚠️ UNVERIFIED: External API integration - no observable calls found, but may exist in unanalyzed files"
- ❌ BAD: "No external API integration" (without verifying)

---

## Section 2: Methodology Enforcement

### Before Starting Analysis

**Checklist:**
- [ ] Understand the full scope (what needs to be analyzed?)
- [ ] Identify ALL relevant files and directories
- [ ] Plan the search strategy (patterns, tools, techniques)
- [ ] Define confidence criteria (what makes this thorough?)

### During Analysis

**Mandatory Practices:**
1. **Use grep/search tools** - Don't rely on memory or sampling
2. **Count programmatically** - Verify totals with file counts
3. **Document searches** - Log all patterns checked (even if 0 results)
4. **Quote sources** - Include file paths and line numbers for findings

### After Analysis

**Verification:**
- [ ] All relevant files checked?
- [ ] All patterns searched?
- [ ] Counts double-checked?
- [ ] Confidence level stated?
- [ ] Uncertainties flagged?

---

## Section 3: Quality Gates & Accuracy Standards

### Mandatory Accuracy Target

**ALL persona analysis passes MUST achieve ≥90% solution quality accuracy before proceeding to the next phase.**

**Quality is measured through:**
- Completeness of analysis (all requirements addressed)
- Technical correctness (architecture decisions validated)
- Implementation feasibility (design can be implemented as specified)
- Alignment with industry standards and best practices
- Consistency across documents (architecture → design → specification)

---

### Quality Gates Per Persona Pass

#### Pass 1: Solution Architecture Analysis
- **Accuracy Target**: ≥90% solution quality
- **Quality Gate Criteria**:
  - All architectural decisions validated and documented
  - Technology choices justified with rationale
  - Deployment architecture complete and feasible
  - Data flow patterns validated
- **If <90%**: Perform refinement pass with additional analysis

#### Pass 2: Technical Design Analysis
- **Accuracy Target**: ≥90% solution quality
- **Quality Gate Criteria**:
  - All API contracts fully specified (request/response models)
  - Database schema complete with all constraints and indexes
  - Service interfaces and implementations defined
  - Sequence diagrams validate all flows
- **If <90%**: Perform refinement pass with additional analysis

#### Pass 3: Implementation Specification
- **Accuracy Target**: ≥90% solution quality
- **Quality Gate Criteria**:
  - Complete project structure (every file and folder specified)
  - Code patterns and conventions documented
  - Service interfaces match technical design
  - Framework configurations specified
- **If <90%**: Perform refinement pass with additional analysis

#### Pass 4: Test Strategy & Planning
- **Accuracy Target**: ≥90% solution quality
- **Quality Gate Criteria**:
  - All services have unit test requirements specified
  - Integration test scenarios defined for all critical paths
  - Test coverage targets specified (minimum 70-85% code coverage)
  - Test data and mocking strategy documented
  - Performance test requirements defined
- **If <90%**: Perform refinement pass with additional analysis

---

### Quality Assurance Process

**After Each Pass:**
1. Review deliverables against quality criteria
2. Measure solution quality accuracy
3. **If accuracy <90%**: Perform additional refinement pass
4. Cross-persona validation ensures consistency
5. Final review by all personas before proceeding

**If Quality Gate Fails (<90% accuracy):**
1. Identify gaps in analysis
2. Perform targeted refinement pass
3. Re-measure quality
4. Repeat until ≥90% achieved

---

## Section 4: Example Analysis Report Structure

### Recommended Template

```markdown
# [Analysis Title]

## Summary
[Brief overview of findings]

## Methodology
- **Files Analyzed:** [count] files in [directories]
- **Search Patterns:** [list all patterns used]
- **Tools Used:** grep, codebase_search, file_search
- **Confidence Level:** 🟢 HIGH / 🟡 MEDIUM / 🔴 LOW

## Findings

### Finding 1: [Title]
**Source:** `path/to/file.ext` (Lines 123-456)
**Code Snippet:**
\`\`\`language
[actual code]
\`\`\`
**Impact:** [description]
**Confidence:** [HIGH/MEDIUM/LOW]

### Finding 2: [Title]
...

## Verification Commands

\`\`\`bash
# Reproduce findings with these commands:
grep -r "pattern" directory/
find . -name "*.ext" | wc -l
\`\`\`

## Uncertainties

⚠️ **UNVERIFIED:** [List anything that couldn't be confirmed]
- Item 1 - Reason
- Item 2 - Reason

**Recommended Next Steps:**
1. Manual inspection of [files]
2. Additional search for [patterns]
3. Verification with team

## Quality Metrics

- **Files Checked:** X/Y (100% coverage)
- **Patterns Searched:** Z patterns (all documented)
- **Confidence Level:** 🟢 HIGH
- **Accuracy Estimate:** ≥90%
```

---

## Section 5: Common Analysis Patterns

### Pattern 1: Exhaustive File Search

```bash
# Count all files of type
find . -name "*.php" | wc -l

# Search all files for pattern
grep -r "pattern" directory/ | wc -l

# Verify pattern absence
grep -r "pattern" directory/
# If output is empty → pattern not found (verified)
```

### Pattern 2: Database Query Analysis

```bash
# Find all database queries
grep -r "DB::" src/ | wc -l
grep -r "\$this->db" src/ | wc -l
grep -r "QueryBuilder" src/ | wc -l

# Categorize by operation
grep -r "->insert(" src/ | wc -l
grep -r "->update(" src/ | wc -l
grep -r "->delete(" src/ | wc -l
grep -r "->select(" src/ | wc -l
```

### Pattern 3: API Endpoint Discovery

```bash
# Find all route definitions
grep -r "Route::" app/
grep -r "@Route" src/
grep -r "app.get\|app.post\|app.put\|app.delete" src/
```

---

## Section 6: Confidence Levels

### 🟢 HIGH Confidence
- Exhaustive search completed (100% coverage)
- All patterns verified programmatically
- Code inspected directly (not inferred)
- Counts double-checked
- No assumptions made

### 🟡 MEDIUM Confidence
- Representative sample analyzed (>50% coverage)
- Most patterns verified
- Some manual inspection required
- Minor uncertainties flagged
- Limited assumptions (stated explicitly)

### 🔴 LOW Confidence
- Limited sample (<50% coverage)
- Patterns not exhaustively verified
- Significant manual inspection needed
- Many uncertainties
- Multiple assumptions (all stated)

**NEVER proceed with LOW confidence analysis. Upgrade to MEDIUM or HIGH before proceeding.**

---

## Section 7: Enforcement & Compliance

### Mandatory For

- ✅ All source code analysis
- ✅ Impact analysis
- ✅ Refactoring verification
- ✅ Architecture analysis
- ✅ Technical design review
- ✅ Implementation specification
- ✅ Test strategy planning

### Zero Tolerance For

- ❌ Assumptions without verification
- ❌ Incomplete searches
- ❌ Unsupported claims
- ❌ "Looks good" without evidence
- ❌ Samples treated as exhaustive
- ❌ <90% accuracy in persona analysis passes

---

## Section 8: Review Checklist

Before finalizing ANY analysis, verify:

- [ ] **Thorough:** All relevant files analyzed
- [ ] **Holistic:** System-wide perspective taken
- [ ] **Fact-Based:** All claims supported by code references
- [ ] **Careful:** Counts and numbers double-checked
- [ ] **Cautious:** Confidence level stated, uncertainties flagged
- [ ] **No Assumptions:** All assumptions explicitly stated or verified
- [ ] **Quality Gate:** ≥90% accuracy achieved (for persona analysis)
- [ ] **Documentation:** All searches and patterns documented
- [ ] **Verification:** Commands provided to reproduce findings

---

## Remember

✅ **Methodology First** - Follow the principles before claiming completion
✅ **Evidence Required** - Every claim needs code references
✅ **Uncertainty is OK** - Flag it, don't hide it
✅ **Quality Over Speed** - Never sacrifice accuracy for completion
✅ **90% Minimum** - Persona analysis passes require ≥90% solution quality
✅ **Thorough > Fast** - Take the time to do it right

---

**Rule Status:** 🔴 CRITICAL - MANDATORY  
**Enforcement:** ZERO TOLERANCE  
**Priority:** 1  
**Version:** 2.0.0  
**Last Updated:** 2025-11-17  
**Consolidation:** Merged analysis-methodology.mdc and persona-analysis-quality-gates.mdc  
**Savings:** -1 file, ~6 KB, ~1,500 tokens
