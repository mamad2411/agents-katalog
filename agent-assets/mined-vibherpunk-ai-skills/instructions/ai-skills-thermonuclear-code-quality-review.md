# Copilot Instructions: Thermonuclear Code Quality Review
Description: A strict, ambitious code review skill focused on structural improvements, maintainability, and eliminating complexity through aggressive refactoring and code judo moves.

# Thermonuclear Code Review Skill

## Overview
This skill implements an extremely rigorous code review process focused on structural quality and maintainability. Key aspects:
- **Ambitious refactoring** ("code judo" moves)
- **Strict size limits** (1K lines/file maximum)
- **Type safety enforcement** (no any/unknown)

See [Core Concepts](references/core_concepts.md) for philosophical foundations.

## Workflow
1. **Initial Scan**
   - Run size analysis on all changed files
   - Flag any type safety violations immediately

2. **Deep Review**
   - For each file, apply the [Workflow Guide](references/workflow_guide.md)
   - Generate specific refactor proposals

3. **Decision Making**
   - Use severity-based prioritization
   - Reject PRs that degrade codebase health

## Best Practices
- **Be aggressive** with structural suggestions (transcript example: deleting 20+ lines via abstraction)
- **Focus on types** (transcript example: converting scattered if-checks to type-driven design)
- **Keep files small** (1K line absolute maximum)

## Pitfalls
1. **False positives** (transcript example: misunderstanding template args system)
   - Mitigation: Include domain context in review

2. **Over-optimization**
   - Rule: "Don't micro-optimize unless proven bottleneck"

3. **Test blindness**
   - Always verify test coverage for new abstractions

## Validation
1. For each recommendation:
   - Verify behavior preservation
   - Check actual reduction in complexity metrics
   - Confirm type safety improvements

2. Sample validation questions:
   - Did we eliminate any `any` types?
   - Is the file structure now flatter?
   - Are there fewer concepts per function?

Use [Prompt Templates](references/prompt_templates.md) for consistent review language.

## Reference Guides

### Core Concepts

# Core Concepts of Thermonuclear Code Review

## Code Judo

The principle of finding structural improvements that dramatically simplify code by reframing problems. Examples from transcript:
- Replacing scattered if-statements with type-driven logic
- Creating generic functions to eliminate 20+ lines of boilerplate
- Splitting large files (>1K lines) into focused modules

## Structural Simplification

Key metrics to enforce:
1. File size limits (1K lines maximum)
2. Abstraction quality (dedicated helpers over inline logic)
3. Type boundaries (eliminate any/unknown/unnecessary optionality)

## Review Priorities

1. Blocking structural issues (file size violations, spaghetti growth)
2. Type safety violations
3. Duplication and boilerplate
4. Legibility concerns

## Non-Negotiables

- Never let a file grow beyond 1K lines without exceptional justification
- Treat nested conditionals as design problems requiring abstraction
- Prefer boring, direct code over clever solutions
- Challenge all type safety compromises (any, unknown, excessive casting)

### Prompt Templates

# Review Prompt Templates

## Main Review Directive
```
Perform a thermonuclear code quality audit of the current changes. Rethink implementations to:
1. Improve abstractions and modularity
2. Eliminate spaghetti code
3. Strengthen type boundaries
4. Reduce concepts readers must hold

Be extremely ambitious - propose structural changes that delete whole categories of complexity.
```

## Type Safety Checklist
```markdown
For each type boundary:
- [ ] No `any` or `unknown` types
- [ ] No unnecessary optionality (?) 
- [ ] Clear input/output contracts
- [ ] Proper discriminated unions for variant types
```

## File Size Enforcement
```
BLOCKER: File {filename} is {currentLines} lines (max 1000)
Required action:
1. Split into {recommendedFiles} focused modules by:
   - {concern1} -> {newFile1}.ts
   - {concern2} -> {newFile2}.ts
```

## Code Judo Examples
```typescript
// Before: Scattered conditionals
if (tracker === 'custom') { /* special case */ }

// After: Type-driven design
type Tracker = Standard | Custom;
interface Custom { isCustom: true; handler: () => void; }
```

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Can Cursor's HARDCORE Review Skill Stop The Slop?](https://www.youtube.com/watch?v=mh5XZ-L5SFQ)** by Matt Pocock

### Workflow Guide

# Step-by-Step Review Workflow

## 1. Initial Scan
- Calculate current file sizes and flag any over 1K lines
- Identify all type boundaries (look for any/unknown/optional markers)
- Map control flow complexity (nesting depth, conditional branches)

## 2. Deep Audit
For each changed file:
1. Check for "code judo" opportunities (structural simplifications)
2. Verify type safety at all boundaries
3. Evaluate abstraction quality (helper functions vs inline logic)
4. Detect unnecessary sequential operations

## 3. Findings Prioritization
Organize issues by severity:
```
1. BLOCKER: File size violations (>1K lines)
2. CRITICAL: Type safety issues (any/unknown)
3. HIGH: Duplicated logic
4. MEDIUM: Legibility concerns
```

## 4. Recommendation Phase
For each finding:
- Propose specific refactors (example: "Split initService.ts into 3 modules")
- Provide code samples for ideal solutions
- Estimate complexity/benefit ratio

## 5. Approval Decision
Reject PRs that:
- Introduce new files >1K lines
- Add type safety violations
- Increase overall complexity

Approve only when:
- Behavior remains correct
- Codebase is cleaner than before
- All critical issues addressed