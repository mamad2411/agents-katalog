---
name: course-content-fragmentation-detector
description: "Analyze online course modules for redundancy, conflicts, and gaps with visual dependency maps and reordering recommendations. Use when the user needs to optimize course structure, identify learning progression issues, or improve student outcomes."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_SHEETS_API_KEY"],
        "bins": ["python3", "graphviz"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"]
    },
    "emoji": "🎓",
    "tags": ["course-optimization", "learning-analytics", "content-audit", "instructional-design", "student-success", "educational-technology", "curriculum-design"]
  }
---

## Overview

The **Course Content Fragmentation Detector** is a comprehensive automation tool that audits your online course structure to identify redundancies, conflicting information, outdated examples, and pedagogical gaps that damage student learning outcomes.

This skill uses AI-powered semantic analysis to scan your entire course curriculum—whether hosted on Moodle, Canvas, WordPress LMS, Google Classroom, or Teachable—and generates:

- **Dependency Maps**: Visual graphs showing prerequisite chains and where knowledge gaps exist
- **Fragmentation Reports**: Quantified metrics on redundancy (0-100% scale) and content conflicts
- **Reordering Recommendations**: Specific module sequences optimized for learning progression
- **Quiz Correlation Analysis**: Cross-reference quiz performance data with course structure to pinpoint struggling areas
- **Consolidation Suggestions**: Automated proposals for merging or splitting modules

Perfect for course creators, instructional designers, L&D managers, and educational institutions scaling multi-module programs. Integrates with Slack for notification workflows, Google Sheets for collaborative audits, and GitHub for version control of curriculum changes.

---

## Quick Start

### Example 1: Basic Course Audit

```
Analyze my Python fundamentals course for content fragmentation. 
The course has 12 modules covering variables, loops, functions, and OOP. 
I suspect some lessons are repeating concepts. Generate a fragmentation report 
and show me which modules should be reordered.
```

**What you'll get**: A fragmentation score (0-100), list of redundant topics with confidence levels, and a prioritized reordering roadmap.

---

### Example 2: Analyzing Student Performance Gaps

```
I have a marketing automation course with 8 modules and quiz results from 
150 students. Module 4 (email segmentation) has a 23% failure rate while 
Module 3 (audience targeting) has 92% pass rate. Are there prerequisite 
gaps? Build a dependency map and tell me where learning breaks down.
```

**What you'll get**: A visual dependency graph highlighting the weak link, analysis of whether Module 3 inadequately prepares for Module 4, and specific content recommendations.

---

### Example 3: Conflict & Redundancy Detection

```
My data science bootcamp has 6 sections on statistics, Python, SQL, and ML. 
Last cohort mentioned contradicting explanations about p-values across 
Module 2 and Module 5. Scan for conflicting information and outdated 
examples (especially Python 2 vs 3 code). Show me exact locations.
```

**What you'll get**: Side-by-side conflict analysis with quote extraction, deprecation warnings, and consolidated best-practice versions of conflicting content.

---

## Capabilities

### 1. **Redundancy Detection**
Scans all course content (text, video transcripts, PDFs, quiz questions) using semantic similarity algorithms (OpenAI embeddings). Identifies:
- Duplicate lesson objectives
- Repeated example problems with slight variations
- Overlapping topic coverage across non-consecutive modules
- Unnecessary review sections that duplicate earlier content

**Output**: List of redundancies with similarity confidence (e.g., "Module 3 Lesson 2 is 87% semantically similar to Module 1 Lesson 4")

---

### 2. **Content Conflict Identification**
Detects contradictory statements, outdated information, and conflicting best practices:
- Opposing advice or methodology in different modules
- Deprecated tool versions or API references
- Inconsistent terminology or definitions
- Contradictory case studies or examples

**Output**: Conflict matrix with severity levels (critical, moderate, minor) and suggested unified versions

---

### 3. **Dependency Mapping**
Builds a directed acyclic graph (DAG) of prerequisite relationships:
- Visualizes which modules must precede others
- Identifies missing bridges between concept chains
- Highlights orphaned modules with no clear prerequisites
- Shows parallel learning paths vs. sequential requirements

**Tools Used**: Graphviz for visualization, networkx for graph analysis

**Output**: Interactive SVG/PNG dependency diagrams + JSON data format for Miro/Lucidchart integration

---

### 4. **Learning Progression Analysis**
Evaluates cognitive complexity escalation:
- Bloom's taxonomy mapping (remember → understand → apply → analyze → evaluate → create)
- Checks for abrupt difficulty jumps between modules
- Identifies modules that violate scaffolding principles
- Measures concept density and pacing

**Output**: Progression score (0-100) with recommendations for redistributing content complexity

---

### 5. **Quiz Performance Correlation**
Cross-references student quiz/assessment data with course structure:
- Identifies which modules precede low-scoring sections
- Calculates pass-rate thresholds needed to succeed in later modules
- Detects whether content gaps or poor pedagogy drives test failures
- Highlights mastery bottlenecks

**Requires**: CSV/JSON export from your LMS (Moodle, Canvas, Teachable) with student IDs, quiz scores, and module completion dates

**Output**: Heatmaps showing performance correlation, minimum-score recommendations for prerequisites

---

### 6. **Consolidation & Reordering Recommendations**
Generates actionable restructuring proposals:
- Suggests merging modules that are too short or fragmented
- Proposes new module sequences optimized for learning
- Identifies where to split overstuffed modules
- Recommends prerequisite enforcement points

**Output**: Before/after module maps, estimated time savings, implementation priority ranking

---

### 7. **Integration with Course Platforms**
Directly connects to:
- **Moodle**: Via REST API (backup/restore integration)
- **Canvas**: LMS API for course structure extraction
- **Google Classroom**: Classroom API for curriculum audits
- **WordPress LMS**: LearnDash, Tutor LMS plugin compatibility
- **Teachable**: Full course export analysis
- **Slack**: Post audit summaries to channels, send alerts when critical fragmentation detected
- **Google Sheets**: Populate audit data for collaborative review and manual override
- **GitHub**: Version control course structure changes, commit audit reports

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API for semantic analysis (GPT-4 recommended)
export OPENAI_API_KEY="sk-..."

# Google Sheets API for reading/writing audit results
export GOOGLE_SHEETS_API_KEY="AIzaSy..."

# LMS Credentials (choose based on platform)
export CANVAS_API_TOKEN="your_canvas_token"
# OR
export MOODLE_API_TOKEN="your_moodle_token"
# OR
export TEACHABLE_API_KEY="your_teachable_key"
```

### Installation

```bash
pip install openai google-auth-oauthlib google-sheets networkx graphviz python-dotenv
```

### Setup Instructions

1. **Export your course**: Download course modules as JSON, CSV, or XML from your LMS
2. **Prepare optional quiz data**: Export student quiz results (student_id, module_id, quiz_score, completion_date)
3. **Set API keys** in `.env` file
4. **Run analysis**:
   ```bash
   python3 analyze_course.py --course-file course_export.json \
     --quiz-data quiz_results.csv \
     --platform moodle
   ```

---

## Example Outputs

### Output 1: Fragmentation Report (JSON)

```json
{
  "course_name": "Advanced Python Programming",
  "modules_analyzed": 8,
  "fragmentation_score": 62,
  "summary": {
    "redundancy_detected": 3,
    "conflicts_found": 1,
    "progression_issues": 2,
    "missing_prerequisites": 1
  },
  "redundancies": [
    {
      "module_1": "Module 2: Functions Basics",
      "module_2": "Module 5: Function Deep Dive (Part 1)",
      "similarity": 0.87,
      "recommendation": "Consolidate into single module or create distinct beginner/advanced tracks"
    }
  ],
  "conflicts": [
    {
      "location_1": "Module 3, Lesson 2: Error Handling",
      "location_2": "Module 6, Lesson 1: Exception Handling",
      "conflict": "Contradicting advice on when to use try-except vs. validation checks",
      "severity": "moderate"
    }
  ],
  "progression_issues": [
    {
      "issue": "Abrupt difficulty jump between Module 4 and Module 5",
      "bloom_level_m4": "understand",
      "bloom_level_m5": "analyze",
      "recommendation": "Add intermediate 'apply' module or restructure Module 5 prerequisites"
    }
  ]
}
```

### Output 2: Visual Dependency Map (SVG)

```
[Dependency diagram showing]:
Module 1 (Python Basics) → Module 2 (Data Types) ⟷ Module 3 (Functions)
                                ↓
                         Module 4 (OOP Fundamentals)
                                ↓
          ┌─────────────────────┼─────────────────────┐
      Module 5 (Classes)    Module 6 (Inheritance)  Module 7 (Polymorphism)
          └────────────────────┬─────────────────────┘
                               ↓
                    Module 8 (Design Patterns)
                         [MASTERY NODE]

[Color coding]:
🟢 Green (0% issues): Modules 1-3
🟡 Yellow (30-60% issues): Modules 4, 5
🔴 Red (70%+ issues): Module 7 (missing prerequisite bridge)
```

### Output 3: Quiz Performance Correlation Heat Map

```
Module Performance vs. Next Module Success Rate:

Module 1 → Module 2: 94% students pass M2 after 85%+ M1 score
Module 2 → Module 3: 67% students pass M3 after 85%+ M2 score ⚠️
Module 3 → Module 4: 41% students pass M4 after 85%+ M3 score ⚠️⚠️

INSIGHT: Content gap between Modules 3-4. 
Recommendation: Add 30-min bridge module on "Applying Concepts" 
before diving into advanced OOP patterns.
```

### Output 4: Consolidation Recommendations (Markdown)

```markdown
## Recommended Course Restructuring

### Current State: 12 modules over 18 weeks

### Proposed State: 8 modules over 12 weeks (33% time savings)

| Current Module | Recommendation | Rationale |
|---|---|---|
| 1. Intro to Python | Keep (Prerequisite) | Essential foundation |
| 2. Variables | Merge with Module 3 | Both <45min, same complexity |
| 3. Data Types | Merge with Module 2 | Closely related concepts |
| 4. Functions Basics | Keep but split into 2 | Too dense (4.5 hours) |
| 5. Function Advanced | Merge remainder into 4 | Redundancy detected (87% sim) |
| 6. Error Handling | Relocate after Module 4 | Better prerequisite alignment |

### Expected Impact:
- 📈 25% improvement in Module 5 pass rates (prerequisite clarity)
- ⏱️ 33% reduction in student time investment
- ✅ Improved progression coherence
```

---

## Tips & Best Practices

### 1. **Prepare Your Data First**
- Export course content in standardized format (JSON or CSV)
- Ensure quiz data includes timestamps to track progression
- Clean up outdated modules before analysis (this tool detects fragmentation, not deprecation)

### 2. **Interpret Fragmentation Scores Contextually**
- **0-30**: Highly optimized course (rare)
- **30-50**: Well-structured with minor improvements possible
- **50-70**: Moderate fragmentation, consolidation recommended
- **70-100**: Severe issues, major restructuring advised

Don't aim for zero fragmentation—some redundancy (10-15%) aids learning through spaced repetition.

### 3. **Use Quiz Data for Credibility**
Student performance data transforms this from a structural audit into a **learning outcomes audit**. A module flagged as redundant becomes actionable only if it correlates with lower downstream scores.

### 4. **Implement Changes Incrementally**
- Apply high-confidence recommendations first (redundancies >85% similarity)
- Test reordering with a pilot cohort before full rollout
- Monitor pass rates for 2-3 cohorts post-restructuring
- Document all changes in version control (GitHub)

### 5. **Schedule Quarterly Audits**
Course fragmentation grows over time as instructors add content incrementally. Run this skill every 3-6 months to catch new issues early.

### 6. **Combine with Student Feedback**
This tool is data-driven but agnostic to student sentiment. Cross-reference findings with:
- Course reviews ("This module felt repetitive")
- Learner surveys on clarity
- Support ticket patterns (which topics generate questions?)

### 7. **Leverage Integration Workflows**
Set up a Slack bot that:
- Posts weekly fragmentation alerts if new conflicts detected
- Notifies course team when a cohort hits a bottleneck threshold
- Automatically creates GitHub issues for recommended changes

---

## Safety & Guardrails

### What This Skill WILL Do
✅ Identify redundancies, conflicts, and progression gaps through objective analysis
✅ Provide evidence-based reordering recommendations
✅ Correlate quiz data with course structure
✅ Integrate with your existing LMS and analytics platforms
✅ Generate audit reports suitable for institutional review

### What This Skill WILL NOT Do
❌ **Not a replacement for human instructional design**: Recommendations are algorithmic and should be reviewed by subject-matter experts
❌ **Does not assess content quality**: A non-redundant, well-sequenced course can still have poor explanations, unclear visuals, or ineffective assessments
❌ **Does not evaluate pedagogy**: This tool is content-structure focused; it won't flag issues like "too much lecture" or "insufficient interactive activities"
❌ **Does not replace learner voice**: Student experience, engagement, and satisfaction require qualitative feedback beyond this analysis
❌ **Does not handle multimedia analysis**: Video content analysis is limited to transcripts; visual design quality is not evaluated
❌ **Does not account for learner diversity**: Recommendations assume linear progression; adaptive learning paths are outside scope
❌ **Does not guarantee improved outcomes**: Structural optimization is necessary but not sufficient for improving pass rates without also addressing pedagogy, support, and motivation

### Limitations & Boundaries

1. **Data Privacy**: Quiz performance data should be anonymized (no student PII in exports). This tool does not store data; it processes and returns results only
2. **API Rate Limits**: OpenAI embeddings API has quota limits (~10k modules/hour). Large institutions may need batching
3. **Language Support**: Currently optimized for English; other languages may have reduced accuracy for semantic similarity
4. **Format Requirements**: Works best with structured exports (JSON, CSV); unstructured PDFs require OCR preprocessing
5. **Graph Complexity**: Courses with >50 modules may generate dense dependency graphs; manual review recommended

### Ethical Considerations

- Use this skill to *enhance* course quality, not to justify cutting content
- Never implement recommendations without instructor review
- Student data used for correlation analysis should be aggregated and anonymized
- Be transparent with students about course restructuring and its rationale

---

## Troubleshooting

### "No redundancies detected" but I know modules overlap

**Diagnosis**: OpenAI embeddings may require exact terminology to detect semantic similarity. Modules with different examples but same concepts sometimes score as distinct.

**Solution**: 
- Manually review modules flagged as "similar" at 70%+ threshold (lower than default 85%)
- Check that module titles and learning objectives are descriptive (vague titles reduce detection)
- If using transcripts, ensure transcription quality is high (poor transc