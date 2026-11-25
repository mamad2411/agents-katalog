---
name: coverage-tracker
description: "Verify that required skills from job description are present in resume. Use when you need to: (1) Check if all must-have skills are covered, (2) Identify which experiences demonstrate which skills, (3) Calculate overall coverage percentage, (4) Find gaps before content generation. Critical check to ensure all required skills are demonstrated."
---

# Coverage Tracker - Skill Coverage Verification

A tool skill for verifying that all required skills from a job description are present and demonstrated in a resume.

## Overview

Coverage tracker is a safety mechanism that ensures resume optimization never sacrifices required skills. It maintains a coverage matrix mapping which resume experiences demonstrate which job requirements.

## Quick Reference

| Task | Command |
|------|---------|
| Check coverage | `check_coverage.py --resume resume.docx --requirements jd.json` |
| Verify no loss | `verify_unchanged.py --before v1.json --after v2.json` |
| Find gaps | `find_gaps.py --resume resume.docx --requirements jd.json` |
| Map skills | `map_skills.py --resume resume.docx --requirements jd.json` |

## Core Concepts

### Coverage Matrix

Maps which resume experiences demonstrate which required skills:

```json
{
  "skill_coverage": {
    "Python": {
      "required": true,
      "covered": true,
      "importance": 10,
      "evidence": [
        {
          "bullet_id": "bullet_001",
          "text": "Built recommendation system using Python...",
          "relevance": 0.95
        },
        {
          "bullet_id": "bullet_005",
          "text": "Automated data pipeline with Python scripts...",
          "relevance": 0.87
        }
      ],
      "coverage_strength": "strong"
    },
    "Kubernetes": {
      "required": true,
      "covered": false,
      "importance": 8,
      "evidence": [],
      "coverage_strength": "none"
    }
  },
  "overall_coverage": 0.85,
  "must_have_coverage": 0.75,
  "nice_to_have_coverage": 0.95
}
```

### Coverage Strength Levels

- **strong**: 3+ pieces of evidence with high relevance
- **moderate**: 2 pieces of evidence
- **weak**: 1 piece of evidence
- **none**: 0 pieces of evidence (gap!)

## Core Operations

### Check Coverage

Verify all required skills are present:

```bash
python scripts/check_coverage.py --resume resume.docx --requirements jd_analyzed.json
```

**Input format for requirements** (from ats-analyzer):
```json
{
  "required_skills": [
    {
      "skill": "Python",
      "category": "must_have",
      "importance": 10
    },
    {
      "skill": "Tableau",
      "category": "nice_to_have",
      "importance": 6
    }
  ]
}
```

**Output:**
```json
{
  "coverage_percentage": 0.85,
  "must_have_coverage": 0.75,
  "nice_to_have_coverage": 0.95,
  "total_required": 20,
  "total_covered": 17,
  "status": "incomplete",
  "missing_skills": ["Kubernetes", "Docker", "Terraform"]
}
```

### Verify No Loss During Compression

Ensure compression didn't lose any required skills:

```bash
python scripts/verify_unchanged.py --before coverage_v1.json --after coverage_v2.json
```

**Output:**
```json
{
  "coverage_maintained": true,
  "skills_lost": [],
  "skills_weakened": ["SQL"],
  "details": {
    "SQL": {
      "before_evidence_count": 3,
      "after_evidence_count": 2,
      "still_covered": true,
      "strength_change": "strong → moderate"
    }
  }
}
```

**CRITICAL**: If `coverage_maintained` is `false`, compression must be rolled back!

### Find Gaps

Identify missing required skills:

```bash
python scripts/find_gaps.py --resume resume.docx --requirements jd_analyzed.json
```

**Output:**
```json
{
  "gaps": [
    {
      "skill": "Kubernetes",
      "category": "must_have",
      "importance": 8,
      "severity": "critical",
      "suggestions": [
        "Check if Docker experience can be mentioned",
        "Look for container orchestration projects",
        "Consider if coursework covered this"
      ]
    }
  ],
  "prompt_for_user": "This role requires Kubernetes (must-have). Do you have any container orchestration or Kubernetes experience we haven't captured?"
}
```

### Map Skills to Experiences

Create detailed mapping of which experiences demonstrate which skills:

```bash
python scripts/map_skills.py --resume resume.docx --requirements jd_analyzed.json
```

**Output:**
```json
{
  "skill_map": {
    "Python": {
      "exp_001": {
        "company": "Tech Corp",
        "bullets": ["bullet_001", "bullet_003"],
        "relevance": 0.92
      },
      "exp_002": {
        "company": "Data Inc",
        "bullets": ["bullet_007"],
        "relevance": 0.85
      }
    }
  },
  "experience_priority": [
    {
      "exp_id": "exp_001",
      "skills_covered": ["Python", "ML", "A/B Testing"],
      "must_have_count": 3,
      "relevance_score": 9.5,
      "must_include": true
    }
  ]
}
```

## Integration with rescume Workflow

### Initial Coverage Check (After JD Analysis)

```bash
# 1. ATS analyzer creates jd_analyzed.json
# 2. Check initial coverage
python scripts/check_coverage.py --resume current_resume.docx --requirements jd_analyzed.json

# Output: 85% coverage, missing Kubernetes
```

### Gap Filling Loop

```bash
# 3. Find gaps
python scripts/find_gaps.py --resume current_resume.docx --requirements jd_analyzed.json

# 4. Interview conductor asks user about Kubernetes
# 5. User provides Docker experience
# 6. Database updated

# 7. Re-check coverage
python scripts/check_coverage.py --resume updated_resume.docx --requirements jd_analyzed.json

# Output: 100% coverage ✓
```


## Python Script Reference

### check_coverage.py

Check overall skill coverage.

**Usage:**
```bash
python scripts/check_coverage.py --resume <docx> --requirements <json>
```

**Parameters:**
- `--resume`: Path to resume DOCX file
- `--requirements`: Path to JD requirements JSON (from ats-analyzer)

**Returns:** JSON with coverage metrics

### verify_unchanged.py

Verify coverage hasn't degraded.

**Usage:**
```bash
python scripts/verify_unchanged.py --before <json> --after <json>
```

**Parameters:**
- `--before`: Coverage before compression
- `--after`: Coverage after compression

**Returns:** JSON indicating if coverage maintained

**Exit codes:**
- `0`: Coverage maintained ✓
- `1`: Coverage lost ✗ (CRITICAL!)

### find_gaps.py

Find missing required skills.

**Usage:**
```bash
python scripts/find_gaps.py --resume <docx> --requirements <json>
```

**Parameters:**
- `--resume`: Path to resume DOCX
- `--requirements`: Path to JD requirements JSON

**Returns:** JSON with gaps and user prompts

### map_skills.py

Map skills to experiences.

**Usage:**
```bash
python scripts/map_skills.py --resume <docx> --requirements <json>
```

**Parameters:**
- `--resume`: Path to resume DOCX
- `--requirements`: Path to JD requirements JSON

**Returns:** JSON with detailed skill-to-experience mapping

## Skill Matching Algorithm

The coverage tracker uses fuzzy matching to detect skills in resume text:

### Exact Match
- "Python" in requirements → finds "Python" in resume ✓

### Synonym Match
- "ML" in requirements → finds "Machine Learning" in resume ✓
- "A/B Testing" → finds "experimentation" ✓

### Abbreviation Expansion
- "SQL" → finds "Structured Query Language" ✓

### Technology Families
- "AWS" → finds "Amazon Web Services", "S3", "EC2" ✓
- "React" → finds "React.js", "ReactJS" ✓

## Coverage Rules

### Must-Have Skills
- **Required**: 100% coverage
- **Action if missing**: Trigger interview-conductor to fill gap
- **Compression rule**: NEVER remove last evidence of must-have skill

### Nice-to-Have Skills
- **Target**: 80%+ coverage
- **Action if missing**: Note in coverage report, but not critical
- **Compression rule**: Can remove if necessary for space


## Safety Mechanisms

### Hard Constraints
1. **Ensure 100% must-have coverage before content generation**
2. **Track evidence strength for all required skills**
3. **Flag if coverage strength is weak (single evidence)**

### Warning Signals
- Must-have skill with only 1 piece of evidence (weak coverage)
- Nice-to-have coverage drops below 70%
- Required skill has no evidence (gap)

## Best Practices

1. **Check coverage after JD analysis** before content generation
2. **Map skills early** to identify high-priority experiences
3. **Never skip gap filling** - always get to 100% must-have coverage before content generation
4. **Keep evidence diverse** - don't rely on single experience for multiple skills
5. **Prioritize experiences** that demonstrate multiple required skills

## Error Handling

All scripts return proper exit codes:
- `0`: Success, coverage OK
- `1`: Coverage lost or incomplete
- `2`: File not found
- `3`: Invalid requirements format

Critical checks (verify_unchanged.py):
```bash
if ! python scripts/verify_unchanged.py --before coverage_v1.json --after coverage_v2.json; then
    echo "CRITICAL: Coverage lost during compression!"
    # Rollback to previous version
    cp draft_v1.docx draft_v2.docx
fi
```

## Notes

- Coverage tracking uses DOCX text content, not structured database
- Skills are case-insensitive matched
- Fuzzy matching allows ~10% character differences
- Re-run coverage check after any resume edits
- Coverage matrix saved alongside resume for audit trail
