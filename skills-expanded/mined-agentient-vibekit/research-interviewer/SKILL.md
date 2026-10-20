---
name: research-interviewer
version: "2.0"
description: >
  Systematic knowledge elicitation through structured interviewing with
  epistemic confidence tracking, MECE coverage verification, and bias-protected questioning.
  PROACTIVELY activate for: (1) Gather research requirements, (2) Elicit problem statements,
  (3) Extract domain knowledge, (4) Clarify research goals, (5) Generate requirements through discovery.
  Triggers: "interview me", "elicit knowledge", "extract information", "research interview",
  "gather requirements", "conduct interview", "knowledge extraction"
---

# Research Interviewer

A systematic knowledge elicitation system that extracts comprehensive, high-fidelity information through adaptive interviewing. Combines deep empathetic understanding with rigorous validation, ensuring captured knowledge is complete, consistent, and ready for downstream use.

---

## 1. Purpose

This skill provides 12 core capabilities:

| # | Capability | Phase | Description |
|---|------------|-------|-------------|
| 1 | **Establish** | 1 | Set interview goal, scope, success criteria, output format |
| 2 | **Map** | 2 | MECE decomposition of topic into coverage dimensions |
| 3 | **Question** | 3 | Adaptive questioning using 8 question types |
| 4 | **Track** | 3-5 | Continuous confidence tracking with epistemic labels |
| 5 | **Validate** | 5 | Cross-reference consistency checking |
| 6 | **Surface** | 3-5 | Assumption identification (explicit, implicit, structural) |
| 7 | **Protect** | 3-5 | Bias protection via frame equivalence, disconfirmation |
| 8 | **Steelman** | 5 | Present strongest version back for confirmation |
| 9 | **Probe** | 6 | Unknown unknowns sweep before termination |
| 10 | **Calibrate** | 6 | Interviewee confidence calibration |
| 11 | **Synthesize** | 5 | Build unified knowledge artifact |
| 12 | **Output** | 6 | Produce format-appropriate deliverable |

---

## 2. When to Use

**Ideal for:**
- Gathering research requirements before creating a research brief
- Eliciting problem statements from stakeholders
- Extracting domain knowledge for documentation
- Clarifying vague or complex requirements
- Discovering unknown unknowns in a problem space
- Building structured knowledge bases from expert interviews

**Avoid when:**
- Information is already well-documented (read docs instead)
- Simple factual lookup (use search instead)
- Interviewee is unavailable or unresponsive
- Topic is outside interviewee's knowledge domain

---

## Checkpoints

This skill uses interactive checkpoints (see `references/checkpoints.yaml`) to resolve ambiguity:

- **output_format_selection** — When output format not specified
- **validation_mode_selection** — When validation mode not specified and context unclear
- **confidence_threshold_adjustment** — When confidence near threshold and domain suggests different
- **premature_termination_check** — When termination criteria met but warning signs present

---

## 3. Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `interview_goal` | string | **yes** | — | What the extracted information will be used for |
| `topic` | string | **yes** | — | What to interview about |
| `output_format` | enum | no | `PROBLEM-STATEMENT` | PROBLEM-STATEMENT \| KNOWLEDGE-CORPUS \| REQUIREMENTS |
| `domain_reference` | enum | no | `none` | product \| architecture \| research \| requirements \| custom \| none |
| `confidence_threshold` | number | no | `0.85` | Target confidence for termination (0.0-1.0) |
| `max_questions` | integer | no | `30` | Maximum questions before forced synthesis |
| `validation_mode` | enum | no | `balanced` | empathetic \| balanced \| rigorous |

### Validation Mode Effects

| Mode | Behavior |
|------|----------|
| **empathetic** | Prioritize rapport, softer probing, accept more at face value |
| **balanced** | Standard verification, targeted probing on inconsistencies |
| **rigorous** | Aggressive assumption challenging, devil's advocate on all claims |

---

## 4. Six-Phase Workflow

### Phase 1: Context Establishment

**Purpose:** Set interview parameters and align on goals.

**Steps:**
1. Receive or elicit `interview_goal` and `topic`
2. Determine `output_format` based on downstream use:
   - PROBLEM-STATEMENT: For research briefs, ideation, evaluation workflows
   - KNOWLEDGE-CORPUS: For RAG systems, documentation, context injection
   - REQUIREMENTS: For development workflows, specification skills

   **CHECKPOINT: output_format_selection**
   - If output_format not specified: **AskUserQuestion**
   - Present format options with downstream implications

3. Select `domain_reference` to load appropriate vocabulary and MECE patterns
4. Establish `validation_mode` based on stakes and interviewee relationship

   **CHECKPOINT: validation_mode_selection**
   - If validation_mode not specified and context unclear: **AskUserQuestion**
   - Present mode options with style implications
5. Confirm parameters with interviewee: "We're aiming to [goal]. I'll ask questions about [topic] and produce a [format]. Does that work?"
6. Initialize empty Knowledge Map structure

**Quality Gate:** Goal clarity - interview_goal must be specific, actionable, and measurable

**Output:** Interview contract (parameters confirmed)

---

### Phase 2: MECE Scope Mapping

**Purpose:** Decompose topic into mutually exclusive, collectively exhaustive coverage dimensions.

**Steps:**
1. Load MECE pattern appropriate to domain (see `mece-decomposition-guide.md`):
   - Product domain → Market Research or Technology Evaluation pattern
   - Architecture domain → Technology Evaluation pattern
   - Research domain → Strategic Research pattern
   - Requirements domain → Custom decomposition
2. Adapt pattern to specific topic
3. Create 3-7 coverage dimensions (fewer for narrow topics, more for broad)
4. For each dimension, identify:
   - What knowledge is needed
   - What "complete" looks like
   - Priority level (critical, important, nice-to-have)
5. Present scope map to interviewee: "I've identified [N] areas to cover: [list]. Does this capture everything important?"
6. Refine based on feedback, add missing dimensions

**Quality Gates:**
- Scope definition: All boundaries explicitly stated (in-scope, out-of-scope)
- MECE structure: Categories non-overlapping and collectively exhaustive

**Output:** Coverage Map with dimensions and sub-areas

---

### Phase 3: Adaptive Elicitation (Iterative)

**Purpose:** Extract knowledge through adaptive questioning.

**CRITICAL CONSTRAINT:** Ask ONE question per turn. Wait for response before next question.

**Workflow Per Turn:**

```
1. SELECT DIMENSION
   └─ Choose highest-priority uncovered area

2. SELECT QUESTION TYPE (see Question Taxonomy)
   └─ Based on what's known/unknown about dimension

3. FORMULATE QUESTION
   ├─ Clear and specific
   ├─ Single focus (not compound)
   └─ Non-leading

4. AWAIT RESPONSE
   └─ DO NOT proceed without interviewee input

5. INTEGRATE RESPONSE
   ├─ Update Knowledge Map
   ├─ Link to related findings
   └─ Note any contradictions

6. TRACK CONFIDENCE
   ├─ Assign confidence score (0.0-1.0)
   └─ Tag uncertainty type (EPISTEMIC | ALEATORY | MODEL)

7. SURFACE ASSUMPTIONS
   ├─ Explicit: Directly stated
   ├─ Implicit: Inferred from response
   └─ Structural: About framing itself

8. APPLY BIAS PROTECTION (if needed)
   ├─ Frame equivalence test for critical claims
   └─ Disconfirmation hunt for confident assertions

9. EVALUATE CONTINUATION
   ├─ More questions needed for this dimension?
   └─ Move to next dimension?
```

### Question Type Selection Logic

```
IF dimension is new AND context unknown:
    → GRAND TOUR (establish landscape)

ELIF need to understand organization/hierarchy:
    → STRUCTURAL

ELIF need to differentiate similar concepts:
    → CONTRAST

ELIF response was abstract, need illustration:
    → EXAMPLE

ELIF response was vague or incomplete:
    → PROBING

ELIF need to stress-test assumption or claim:
    → DEVIL'S ADVOCATE

ELIF statement is ambiguous:
    → CLARIFYING

ELIF synthesizing understanding for dimension:
    → CONFIRMING
```

### Adaptive Rules

- **Follow energy:** Pursue topics where interviewee shows engagement
- **Notice gaps:** Track what hasn't been said as carefully as what has
- **Connect threads:** Build on earlier responses, reference previous answers
- **Respect scope:** Stay within established boundaries
- **Vary types:** Don't use same question type consecutively
- **One question per turn:** Never ask multiple questions at once

**Quality Gate:** Epistemic labeling - every finding tagged with uncertainty type

**Output:** Growing Knowledge Map with confidence scores

---

### Phase 4: Continuous Confidence Tracking

**Purpose:** Maintain real-time epistemic status of all gathered knowledge.

**Runs parallel to Phase 3.**

**Mechanism:**

1. **Classify each finding** using uncertainty taxonomy:
   - **EPISTEMIC:** We don't know, but COULD find out with more questions
   - **ALEATORY:** Inherent uncertainty that CANNOT be reduced (future events, randomness)
   - **MODEL:** Answer depends on definitions/framework choices

2. **Assign confidence score** (0.0-1.0) based on:
   - Clarity of response
   - Consistency with other findings
   - Evidence quality (direct experience vs. hearsay)
   - Specificity (concrete vs. vague)

3. **Track coverage** per dimension:
   - Questions asked
   - Findings captured
   - Confidence level
   - Remaining gaps

4. **Calculate overall confidence:**
   - Per-dimension: Average of finding confidences
   - Overall: Weighted average (critical dimensions weighted 1.5x)

5. **Identify high-value targets:**
   - EPISTEMIC gaps in critical dimensions → ask more questions
   - MODEL uncertainties → surface for explicit choice
   - ALEATORY factors → document and move on

**Quality Gate:** Confidence threshold - overall confidence >= `confidence_threshold`

---

### Phase 5: Validation and Synthesis

**Purpose:** Verify consistency and build unified artifact.

**Steps:**

#### 5.1 Consistency Matrix

Cross-reference all findings for contradictions:
- Compare related claims across dimensions
- Flag any inconsistencies
- If conflict found: Present both versions to interviewee for resolution

```
"Earlier you mentioned [X]. Just now you said [Y].
These seem to conflict. Can you help me understand?"
```

#### 5.2 Assumption Inventory

Compile all surfaced assumptions:

| Type | Description | Examples |
|------|-------------|----------|
| **Explicit** | Directly stated by interviewee | "We're assuming budget isn't a constraint" |
| **Implicit** | Inferred from responses | User said "real-time" implying high availability need |
| **Structural** | Embedded in interview framing | We focused on technical aspects, not organizational |

Validate critical assumptions: "It sounds like we're assuming [X]. Is that right? What would change if that assumption were wrong?"

#### 5.3 Steelmanning

Present the strongest version of gathered knowledge:

```
"Let me play back what I've understood. The core issue is [X],
driven by [Y], with the key constraint being [Z]. The main
stakeholders are [A, B, C], and success looks like [criteria].

Is this an accurate and complete representation?"
```

Iterate until interviewee confirms.

#### 5.4 Synthesis

Build unified knowledge structure:
- Organize findings by dimension
- Ensure all MECE dimensions covered
- Apply output format structure (see Output Specifications)
- Calculate final confidence scores

**Quality Gates:**
- Consistency verified: No unresolved contradictions
- Assumptions surfaced: All critical assumptions documented and validated

**Output:** Synthesized knowledge ready for formatting

---

### Phase 6: Calibrated Termination

**Purpose:** Ensure completeness and produce deliverable.

**Steps:**

#### 6.1 Unknown Unknowns Probe

Ask these five questions before concluding:

1. "What haven't I asked about that I should have?"
2. "What would someone who knows this domain well be surprised I didn't ask?"
3. "Are there adjacent areas that connect to this topic we should touch on?"
4. "What assumptions might I be making that aren't valid?"
5. "What could go wrong that we haven't discussed?"

#### 6.2 Coverage Assessment

Review Coverage Map:
- All dimensions at minimum confidence?
- Any CRITICAL gaps remaining?
- Epistemic gaps that could be closed with one more question?

#### 6.3 Interviewee Calibration

Capture the interviewee's confidence:

```
"How confident are you in the completeness of what we've covered?"
"Which areas are you most certain about? Least certain?"
```

Map to final confidence report.

#### 6.4 Termination Decision

**CHECKPOINT: confidence_threshold_adjustment**
- If confidence near threshold and domain suggests different: **AskUserQuestion**
- Example: "Confidence is 0.82 (threshold 0.85). For exploratory, 0.80 is often sufficient."

**CHECKPOINT: premature_termination_check**
- If termination criteria met but warning signs present: **AskUserQuestion**
- Warning signs: new areas surfaced, critical dimension gaps, unexplored topics mentioned

```
TERMINATE IF:
  - confidence_threshold met (default 0.85)
  - max_questions reached
  - Interviewee signals completion
  - No new significant information in last 3 questions

CONTINUE IF:
  - Critical gaps remain
  - Unresolved contradictions exist
  - Unknown unknowns probe surfaced new areas
```

#### 6.5 Output Generation

Select template based on `output_format`:
- PROBLEM-STATEMENT → See Section 6.1 of Output Specifications
- KNOWLEDGE-CORPUS → See Section 6.2 of Output Specifications
- REQUIREMENTS → See Section 6.3 of Output Specifications

**Quality Gates:**
- Confidence threshold met
- Interviewee calibration complete

**Output:** Final deliverable in specified format

---

## 5. Question Taxonomy

### The 8 Question Types

| # | Type | Purpose | When to Use |
|---|------|---------|-------------|
| 1 | **Grand Tour** | Establish broad landscape | Opening a new dimension |
| 2 | **Structural** | Understand organization/hierarchy | Need to see relationships |
| 3 | **Contrast** | Differentiate similar concepts | Clarify distinctions |
| 4 | **Example** | Ground abstract in concrete | Need illustration |
| 5 | **Probing** | Drill into specifics | Response was vague |
| 6 | **Devil's Advocate** | Stress-test assumptions | Challenge conviction |
| 7 | **Clarifying** | Resolve ambiguity | Statement unclear |
| 8 | **Confirming** | Validate understanding | Close a dimension |

### Typical Flow Within a Dimension

```
Grand Tour → Structural → Example → Probing → Contrast → Devil's Advocate → Confirming
```

**Reference:** See `references/question-taxonomy.md` for detailed examples and templates.

---

## 6. Output Specifications

### 6.1 PROBLEM-STATEMENT Format

Aligns with CONTRACT-01 from artifact-contracts.yaml.

```xml
<problem_statement contract="CONTRACT-01">
  <metadata>
    <artifact_id>[PS-YYYY-MM-DD-XXXXX]</artifact_id>
    <contract_type>PROBLEM-STATEMENT</contract_type>
    <created_at>[ISO 8601]</created_at>
    <created_by>research-interviewer</created_by>
    <confidence>[0.0-1.0]</confidence>
  </metadata>

  <statement>[Clear, actionable problem statement]</statement>

  <jtbd_format>
    <situation>[When/context in which the problem arises]</situation>
    <motivation>[What the user wants to do]</motivation>
    <outcome>[Desired result/benefit]</outcome>
  </jtbd_format>

  <context>
    <domain>[product | architecture | strategy | research | ...]</domain>
    <stakeholders>
      <stakeholder role="[role]">[Who]</stakeholder>
    </stakeholders>
    <constraints>
      <constraint>[Hard constraint]</constraint>
    </constraints>
    <assumptions>
      <assumption type="[explicit|implicit|structural]" validated="[true|false]">
        [Assumption text]
      </assumption>
    </assumptions>
  </context>

  <success_criteria>
    <criterion measurable="[true|false]" priority="[must_have|should_have|nice_to_have]">
      [Criterion text]
    </criterion>
  </success_criteria>

  <epistemic_status>
    <overall_confidence>[0.0-1.0]</overall_confidence>
    <uncertainty_breakdown>
      <epistemic_gaps>[What we don't know but could find out]</epistemic_gaps>
      <aleatory_factors>[Inherent uncertainties]</aleatory_factors>
      <model_dependencies>[Framework-dependent answers]</model_dependencies>
    </uncertainty_breakdown>
  </epistemic_status>
</problem_statement>
```

### 6.2 KNOWLEDGE-CORPUS Format

Optimized for RAG systems and context injection.

```xml
<knowledge_corpus>
  <metadata>
    <corpus_id>[KC-YYYY-MM-DD-XXXXX]</corpus_id>
    <topic>[Interview topic]</topic>
    <created_at>[ISO 8601]</created_at>
    <created_by>research-interviewer</created_by>
    <overall_confidence>[0.0-1.0]</overall_confidence>
  </metadata>

  <coverage_map>
    <dimension id="D1" name="[Name]" confidence="[0.0-1.0]">
      <finding id="D1F1" confidence="[0.0-1.0]"
               uncertainty_type="[EPISTEMIC|ALEATORY|MODEL]">
        <statement>[What was learned]</statement>
        <evidence>[How we know this]</evidence>
        <source_question>[Question that elicited this]</source_question>
      </finding>
    </dimension>
  </coverage_map>

  <relationships>
    <relationship from="[finding_id]" to="[finding_id]"
                  type="[depends_on|contradicts|supports|refines]">
      [Description]
    </relationship>
  </relationships>

  <assumption_inventory>
    <assumption id="A1" type="[explicit|implicit|structural]"
                validated="[true|false]" confidence="[0.0-1.0]">
      <statement>[Assumption]</statement>
      <implications>[What depends on this]</implications>
    </assumption>
  </assumption_inventory>

  <gaps_registry>
    <gap dimension="[dimension_id]" severity="[critical|significant|minor]">
      <description>[What's missing]</description>
      <suggested_resolution>[How to close]</suggested_resolution>
    </gap>
  </gaps_registry>
</knowledge_corpus>
```

### 6.3 REQUIREMENTS Format

Job stories with acceptance criteria.

```xml
<requirements>
  <metadata>
    <requirements_id>[REQ-YYYY-MM-DD-XXXXX]</requirements_id>
    <topic>[Interview topic]</topic>
    <created_at>[ISO 8601]</created_at>
    <created_by>research-interviewer</created_by>
    <overall_confidence>[0.0-1.0]</overall_confidence>
  </metadata>

  <job_stories>
    <job_story id="JS1" priority="[must_have|should_have|nice_to_have]"
               confidence="[0.0-1.0]">
      <situation>When [context/trigger]</situation>
      <motivation>I want to [action/capability]</motivation>
      <outcome>So that [benefit/result]</outcome>
      <acceptance_criteria>
        <criterion id="JS1AC1" testable="[true|false]">[Criterion]</criterion>
      </acceptance_criteria>
    </job_story>
  </job_stories>

  <constraints>
    <constraint id="C1" type="[technical|business|regulatory]"
                non_negotiable="[true|false]">
      <description>[Constraint]</description>
      <rationale>[Why this constraint exists]</rationale>
    </constraint>
  </constraints>

  <non_functional_requirements>
    <nfr id="NFR1" category="[performance|security|scalability|...]">
      <description>[NFR description]</description>
      <measurement>[How to verify]</measurement>
    </nfr>
  </non_functional_requirements>

  <traceability>
    <finding_to_requirement from="[finding_id]" to="[requirement_id]">
      [How finding led to requirement]
    </finding_to_requirement>
  </traceability>
</requirements>
```

**Reference:** See `references/output-templates.md` for complete templates with examples.

---

## 7. Quality Gates

| # | Gate | Criterion | Phase |
|---|------|-----------|-------|
| 1 | **Goal Clarity** | Interview goal is specific, actionable, measurable | 1 |
| 2 | **Scope Definition** | All boundaries explicitly defined and confirmed | 2 |
| 3 | **MECE Structure** | Coverage dimensions are non-overlapping and exhaustive | 2 |
| 4 | **Epistemic Labeling** | Every finding tagged as EPISTEMIC/ALEATORY/MODEL | 3-4 |
| 5 | **Consistency Verified** | No unresolved contradictions in gathered knowledge | 5 |
| 6 | **Assumptions Surfaced** | All critical assumptions documented and validated | 5 |
| 7 | **Confidence Threshold** | Overall confidence >= `confidence_threshold` parameter | 6 |
| 8 | **Interviewee Calibration** | Interviewee confidence captured and documented | 6 |

---

## 8. Workflow Integration

This skill serves as the upstream elicitation component in the research workflow:

```
┌─────────────────────────┐
│  research-interviewer   │  ◀── THIS SKILL
│                         │  Elicit research requirements
└───────────┬─────────────┘
            │
            │ Produces: PROBLEM-STATEMENT | KNOWLEDGE-CORPUS | REQUIREMENTS
            │
            ▼
┌─────────────────────────┐
│  create-research-brief  │  Design multi-LLM research strategy
│       (Phase 1)         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   Execute Research      │  Run prompts across models
│   (Manual or Agent)     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  create-research-brief  │  Consolidate into report
│       (Phase 2)         │
└─────────────────────────┘
```

### Artifact Flow

| This Skill Produces | Consumed By |
|---------------------|-------------|
| PROBLEM-STATEMENT (CONTRACT-01) | create-research-brief, generate-ideas, EVAL skills |
| KNOWLEDGE-CORPUS | RAG systems, context injection, documentation skills |
| REQUIREMENTS | Development workflows, specification skills |

---

## 9. Behavioral Guidelines

- **Curious not interrogating:** Maintain genuine interest, avoid feeling like an interrogation
- **Patient with complexity:** Allow time for complex explanations
- **Humble about understanding:** Check assumptions, don't assume you understand
- **Goal-anchored:** Keep interview goal visible throughout
- **Efficient with time:** Respect interviewee's time, don't over-ask covered areas
- **One question at a time:** Never bundle multiple questions

---

## 10. References

| File | Purpose |
|------|---------|
| `references/question-taxonomy.md` | 8 question types with examples and templates |
| `references/assumption-surfacing-protocol.md` | 3 assumption types with surfacing techniques |
| `references/bias-protection-techniques.md` | Frame equivalence, disconfirmation methods |
| `references/output-templates.md` | Complete XML templates for all output formats |
| `references/epistemic-labeling-guide.md` | 5-tier epistemic classification (FACT/LIKELY/PLAUSIBLE/ASSUMPTION/UNCERTAIN) |
| `references/domain-references.md` | Domain-specific vocabulary, MECE patterns, stakeholders |

### External References

| File | Purpose |
|------|---------|
| `../create-research-brief/references/uncertainty-taxonomy.md` | Epistemic classification protocol |
| `../create-research-brief/references/mece-decomposition-guide.md` | MECE patterns by domain |
| `@core/artifact-contracts.yaml` | CONTRACT-01 schema |

---

## 11. Templates

| File | Purpose |
|------|---------|
| `templates/problem-statement-output.md` | CONTRACT-01 compliant template with field guidance and examples |
| `templates/knowledge-corpus-output.md` | RAG-optimized XML template with chunking recommendations |
| `templates/requirements-output.md` | Job stories template with acceptance criteria patterns |

---

## 12. Examples

### Example 1: Problem Statement Elicitation

```yaml
input:
  interview_goal: "Understand authentication pain points for research brief"
  topic: "User authentication system"
  output_format: PROBLEM-STATEMENT
  domain_reference: product
  validation_mode: balanced

flow:
  phase_1: Confirmed goal, selected PROBLEM-STATEMENT output
  phase_2: Created 5 MECE dimensions - UX, security, maintenance, scalability, integration
  phase_3: 18 questions across dimensions
           - Grand Tour on current auth flow
           - Structural on user types and permissions
           - Example on recent authentication failure
           - Probing on "complicated" password reset
           - Devil's Advocate on SSO assumption
           - Confirming on core pain point
  phase_4: Tracked confidence per dimension
           - UX: 0.90, Security: 0.85, Maintenance: 0.75
           - Scalability: 0.60 (EPISTEMIC gap identified)
           - Integration: 0.80
  phase_5: Built consistency matrix, no contradictions
           Surfaced 4 assumptions (2 explicit, 2 implicit)
           Steelmanned: "Users abandon MFA due to friction in recovery flow"
  phase_6: Unknown unknowns probe revealed compliance requirement
           Final confidence: 0.87

output: PROBLEM-STATEMENT artifact per CONTRACT-01 schema
```

### Example 2: Knowledge Corpus Extraction

```yaml
input:
  interview_goal: "Document data pipeline architecture for context"
  topic: "Data engineering infrastructure"
  output_format: KNOWLEDGE-CORPUS
  domain_reference: architecture
  validation_mode: rigorous

flow:
  phase_1: Established goal for RAG context generation
  phase_2: 5 dimensions - ingestion, processing, storage, serving, monitoring
  phase_3: 24 questions, heavy Structural and Example types
           Rigorous mode triggered more Devil's Advocate probes
  phase_4: 3 MODEL uncertainties flagged (definition-dependent)
           12 EPISTEMIC findings, 9 ALEATORY factors documented
  phase_5: Built knowledge graph with 47 findings
           12 inter-finding relationships documented
  phase_6: Confidence: 0.91, interviewee highly confident

output: KNOWLEDGE-CORPUS with 47 findings across 5 dimensions
```

### Example 3: Requirements Discovery

```yaml
input:
  interview_goal: "Gather requirements for executive reporting feature"
  topic: "Executive reporting dashboard"
  output_format: REQUIREMENTS
  domain_reference: requirements
  validation_mode: empathetic

flow:
  phase_1: Empathetic mode for executive stakeholder
  phase_2: 5 dimensions - data sources, visualizations, access control, export, scheduling
  phase_3: 15 questions, softer probing style
           Heavy use of Example and Confirming questions
  phase_4: High ALEATORY uncertainty around future metrics
           Documented as "subject to change"
  phase_5: Generated 8 job stories with acceptance criteria
           Traced each to source findings
  phase_6: Confidence: 0.86, stakeholder confirmed completeness

output: REQUIREMENTS with 8 job stories, 4 constraints, 3 NFRs
```

---

## Quick Start

```
/research-interviewer
interview_goal: "[What you'll use the information for]"
topic: "[Subject to interview about]"
output_format: PROBLEM-STATEMENT
```
