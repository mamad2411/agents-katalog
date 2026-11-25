---
name: pwrl-learnings-classify
description: "Classify and prioritize learnings by type, domain, severity, and applicability."
argument-hint: "[extraction artifact from pwrl-learnings-extract]"
---

# pwrl-learnings-classify — Learning Classification

**Purpose:** Phase 2 of learnings workflow. Refines preliminary classifications from extraction phase and assigns priority, domain, applicability scores, and tags. Enables effective filtering and retrieval of learnings.

## Interaction Method

- Primarily automated classification using heuristics.
- Minimal user interaction; ask only for ambiguous cases.
- Show classification summary before proceeding.
- If learning ambiguous: "Should this be 'Gotcha' or 'Pattern'?"
- No approval gate; proceed to next skill.

## Input: Extraction Artifact

Expects artifact from `pwrl-learnings-extract` with:

```yaml
extract_id: YYYY-MM-DD-NNN-extract
learnings: [array of extracted learning candidates]
```

Each learning has: type, title, problem, application, source, confidence.

## Output: Classification Artifact

Emit classification artifact (YAML + markdown):

```yaml
---
format: pwrl-learnings-classify-artifact
version: "1.0"
classify_id: YYYY-MM-DD-NNN-classify
created: ISO-8601-timestamp
source_extract_id: YYYY-MM-DD-NNN-extract
---

# Learning Classification Results

## Summary
- **Total Classified:** [count]
- **By Type:**
  - Gotchas: [count]
  - Patterns: [count]
  - Decisions: [count]
  - Technical Fixes: [count]
  - Workflows: [count]

- **By Domain:**
  - Backend: [count]
  - Frontend: [count]
  - Architecture: [count]
  - DevOps: [count]
  - Security: [count]
  - Performance: [count]
  - Process: [count]
  - Testing: [count]

- **By Priority:**
  - Critical: [count]
  - Important: [count]
  - Nice to Know: [count]

## Classified Learnings

### Learning 1
- **Type:** [refined type]
- **Domain:** [backend | frontend | architecture | devops | security | performance | process | testing]
- **Priority:** [critical | important | nice_to_know]
- **Applicability:** [0-10] (current project relevance)
- **General Applicability:** [0-10] (general relevance)
- **Tags:** [language, framework, topic, difficulty]
- **Title:** [Learning title]
- **Problem:** [What problem does this address?]
- **Application:** [How to apply this learning]
- **Related Learnings:** [If duplicates or related learnings found]

[Additional classified learnings...]

## Quality Metrics
- **Average Applicability:** [0-10 score]
- **High Priority Count:** [critical + important]
- **Low Confidence Count:** [learnings with medium/low confidence]
- **Duplicate Count:** [potential duplicates found]

## Classification Status
- **Status:** success
- **Ambiguous Classifications:** [count]
- **Manual Review Needed:** [true/false]

## Ready for Deduplication
- **Next Skill:** pwrl-learnings-structure
- **Artifacts Passed:** This classification artifact
```

Artifact passed to `pwrl-learnings-structure`.

## Detailed Workflow

For complete step-by-step instructions, see [classify-learnings-detailed-workflow.md](references/classify-learnings-detailed-workflow.md).

This SKILL.md provides an overview. The detailed workflow document contains:

- Type refinement heuristics
- Domain assignment logic and keywords
- Priority assessment rules
- Applicability scoring methodology
- Tag assignment strategies
- Related learning detection
- Interaction flow examples

## Early Duplicate Detection (Phase 2 Enhancement)

This phase includes early duplicate detection to improve coverage:

1. **Load existing learnings** from `docs/learnings/.index.json`
2. **Check each candidate** against existing learnings by type + domain + tags
3. **Flag potential updates** (candidates matching existing learnings)
4. **Warn user** before proceeding to next phase

See [duplicate-handling-consolidated.md](../pwrl-learnings/references/duplicate-handling-consolidated.md#early-duplicate-detection-phase-2) for detailed early detection logic.

## Quality Gate Validation

After completing this phase, run quality gate validation:

```bash
/pwrl-phase-checkpoint learnings 2 [artifact-path]
```

See [pwrl-phase-checkpoint](../../pwrl-phase-checkpoint/SKILL.md) for validation rules.

---

1. Check that input artifact has:
   - Valid `extract_id`
   - `learnings` array populated
   - Each learning has type, title, problem, application

2. **If verification fails:**
   - Return error: "Extraction artifact invalid. Return to pwrl-learnings-extract."

### Step 2: Refine Type Classification

**Improve preliminary types from extraction with higher confidence:**

| Preliminary   | Refinement Heuristics                                  | Refined Type      |
| ------------- | ------------------------------------------------------ | ----------------- |
| Gotcha        | Warning, "beware", trap, edge case                     | **Gotcha**        |
| Pattern       | "Use X for Y", reusable approach, best practice        | **Pattern**       |
| Decision      | "Why X?", "Why not Y?", architectural choice, tradeoff | **Decision**      |
| Technical Fix | "How to solve X", bug workaround, debugging technique  | **Technical Fix** |
| Workflow      | Process, checklist, sequence of steps                  | **Workflow**      |

**Ambiguous cases:**

- If could be "Pattern" or "Workflow": Ask user or flag for review
- If could be "Gotcha" or "Technical Fix": "Gotcha" (avoidance-oriented)
- If strong evidence of type: Use refined type

### Step 3: Assign Domain

**Categorize learning by technology/area:**

```
Domain Heuristics:

Backend:        Node.js, Python, Java, databases, APIs, auth
Frontend:       React, Vue, TypeScript, CSS, UI, browsers
Architecture:   System design, scalability, patterns, microservices
DevOps:         Docker, CI/CD, deployment, infrastructure, monitoring
Security:       Vulnerabilities, injection, XSS, auth, secrets, validation
Performance:    Optimization, caching, algorithms, memory, benchmarks
Process:        Git workflow, code review, planning, documentation
Testing:        Unit tests, mocking, coverage, integration tests
```

**Assignment logic:**

1. Scan title, problem, application for domain keywords
2. Check source context (file path, framework)
3. If multiple domains: Pick primary (first match wins) + tag others

**Examples:**

- "Race condition in cache" → Architecture (system behavior), also tag Performance
- "FIXME in React component" → Frontend, tag Performance if optimization
- "SQL injection risk" → Security (primary)

### Step 4: Assess Priority

**Determine severity level:**

| Priority         | Criteria                                                    |
| ---------------- | ----------------------------------------------------------- |
| **CRITICAL**     | Security risk, data loss, blocking issue, prevents shipping |
| **IMPORTANT**    | Best practice, common mistake, performance, should know     |
| **NICE_TO_KNOW** | Edge case, rare, optimization, nice-to-have knowledge       |

**Priority rules:**

- If domain = "Security": CRITICAL or IMPORTANT
- If domain = "Performance" and applicability > 7: IMPORTANT
- If "race condition", "injection", "overflow": CRITICAL
- If "best practice", "common mistake": IMPORTANT
- If "edge case", "rare": NICE_TO_KNOW
- Default: IMPORTANT

### Step 5: Score Applicability

**Rate relevance to current project and general use:**

```
Current Project Applicability (0-10):
- 9-10: Tech/framework/domain directly used in project
- 7-8: Related to project's architecture/goals
- 5-6: Somewhat relevant; might apply in future
- 3-4: Peripherally relevant; useful to know
- 0-2: Niche; unlikely to use in this project

General Applicability (0-10):
- 9-10: Universal principle; applies to most projects
- 7-8: Widely applicable; most projects benefit
- 5-6: Moderately useful; specialized but not niche
- 3-4: Niche; applies to specific tech/domain
- 0-2: Very niche; rarely needed outside context
```

**Scoring heuristics:**

1. **Check source context:**
   - If from codebase: high current project applicability
   - If from external source: lower current project applicability

2. **Check generality of problem:**
   - "Race condition in any multi-threaded system" → general 9/10
   - "Race condition in our specific cache" → project-specific 8/10, general 6/10

3. **Check tech/domain:**
   - "React anti-pattern" → highly applicable to React projects; general 7/10
   - "Kubernetes deployment edge case" → niche 5/10 general

### Step 6: Assign Tags

**Add searchable tags to each learning:**

```
Tag Categories:

Language:       javascript, typescript, python, java, sql, bash, etc.
Framework:      react, express, nextjs, django, fastapi, docker, etc.
Topic:          performance, security, architecture, testing, deployment, etc.
Difficulty:     beginner, intermediate, advanced, expert
Severity:       critical, high, medium, low (for security/performance issues)
```

**Tagging rules:**

- Assign 2-5 tags per learning
- Include language/framework if mentioned
- Include main topic
- Include difficulty level
- Include severity if applicable

**Examples:**

- Race condition learning: `[typescript, architecture, critical, intermediate]`
- React hook gotcha: `[javascript, react, beginner, nice-to-know]`
- SQL injection fix: `[sql, security, critical, intermediate]`

### Step 7: Identify Related Learnings

**Detect duplicates and complementary learnings:**

1. **Duplicate detection:**
   - Same title or very similar wording
   - Same problem stated differently
   - Flag for deduplication phase

2. **Complementary detection:**
   - "Race condition" pairs with "Mutex usage"
   - "SQL injection risk" pairs with "Input validation"
   - Document relationship but don't deduplicate

**Format:**

```yaml
Related Learnings:
  - [duplicate]: "Title of duplicate"
  - [complements]: "Title of related learning"
  - [prevented_by]: "Learning that prevents this issue"
```

### Step 8: Generate Classification Artifact

**Emit artifact with:**

- All learnings with refined classifications
- Type, domain, priority, applicability scores
- Tags for searching/filtering
- Related learnings references
- Quality metrics summary
- Ready flag for next skill

## Edge Cases & Heuristics

**Ambiguous Type Refinements:**

```
Learning: "Use async/await instead of callbacks"
→ Could be Pattern or Workflow
→ Rule: If "how to do X", it's Pattern. If "step 1, step 2", it's Workflow.
→ Classification: Pattern (shows best practice approach)
```

**Cross-Domain Learnings:**

```
Learning: "Always validate user input to prevent SQL injection"
→ Primary Domain: Security
→ Secondary: Backend (where validation happens)
→ Tags: [security, backend, validation, critical]
```

**Applicability Edge Case:**

```
Learning from DevOps error: "Docker image optimization technique"
→ If project uses Docker: applicability 9/10
→ If project uses Kubernetes only: applicability 5/10
→ General applicability: 8/10 (Docker is widespread)
```

## Error Handling

| Error                       | Recovery                                           |
| --------------------------- | -------------------------------------------------- |
| Extraction artifact invalid | Return error; direct to pwrl-learnings-extract     |
| Ambiguous learning          | Flag for manual review; use default classification |
| No learnings to classify    | Return empty artifact; continue to next skill      |
| Domain/priority unclear     | Use heuristic; flag for review                     |

## Testing Coverage

Test file: `tests/pwrl-learnings/classify-learnings.test.ts`

**Happy Path Tests:**

- ✅ Security gotcha (critical, security domain)
- ✅ Performance pattern (important, performance domain)
- ✅ Architecture decision (important, architecture domain)
- ✅ Technical fix (important, backend domain)
- ✅ Process workflow (nice-to-know, process domain)

**Edge Cases:**

- ✅ Ambiguous type (flagged for review)
- ✅ Cross-domain learning (primary + secondary)
- ✅ Very niche learning (low applicability)
- ✅ High-confidence extraction (refined type)
- ✅ Low-confidence extraction (marked for review)

**Output Validation Tests:**

- ✅ All learnings classified
- ✅ Applicability scores in range [0-10]
- ✅ Priority is valid (critical/important/nice-to-know)
- ✅ Domain is valid
- ✅ Tags present (2-5 per learning)
- ✅ Related learnings identified
