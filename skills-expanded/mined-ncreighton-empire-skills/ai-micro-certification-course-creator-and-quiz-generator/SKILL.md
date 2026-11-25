---
name: ai-micro-certification-course-creator-and-quiz-generator
description: "Transform expertise into structured micro-certification courses with auto-generated quizzes, flashcards, and skill assessments. Use when the user needs to create lead magnets, paid courses, or training programs from raw content without instructional design experience."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","ANTHROPIC_API_KEY"],"bins":["curl","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🎓"}}
---

## Overview

The **AI Micro-Certification Course Creator and Quiz Generator** automates the transformation of raw expertise—transcripts, blog posts, video descriptions, PDFs, or LinkedIn articles—into production-ready micro-certification courses. This skill is purpose-built for solopreneurs, coaches, and subject matter experts who want to monetize knowledge without hiring instructional designers.

### Why This Matters

Creating courses manually takes 40-60 hours per course. This skill reduces that to minutes by:
- **Automatically structuring content** into learning modules with clear learning objectives
- **Generating quiz questions** at multiple difficulty levels (Bloom's taxonomy-aligned)
- **Creating flashcards** for spaced repetition and retention
- **Mapping prerequisites** so learners follow optimal learning paths
- **Calibrating difficulty** to target audience (beginner, intermediate, advanced)
- **Exporting to multiple platforms**: WordPress LMS, Google Classroom, Teachable, Kajabi, Moodle

### Integrations & Platforms

This skill outputs content compatible with:
- **WordPress LMS plugins**: LearnDash, LifterLMS, Tutor LMS
- **Standalone platforms**: Teachable, Kajabi, Thinkific, Podia
- **Google Classroom** (CSV/JSON export)
- **Slack** (course summaries, quiz notifications)
- **Notion** (course outlines, study guides)
- **Airtable** (prerequisite mapping, student progress tracking)
- **PDF export** for offline distribution

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Convert Blog Post Series to Course Module
```
Convert this 3-part blog series on "Email Marketing Fundamentals" 
into a structured course module with:
- 1 learning objective
- 5 quiz questions (2 multiple choice, 2 true/false, 1 short answer)
- 10 flashcards for key terms
- Difficulty level: Beginner

Blog content:
[Paste your 3 blog posts here]

Output format: JSON with module structure, quiz answers, and flashcard pairs.
```

### Example 2: Generate Assessment from Video Transcript
```
I have a 15-minute training video transcript on "Advanced Excel Formulas."
Create a comprehensive assessment with:
- Pre-assessment quiz (5 questions, beginner level)
- Post-assessment quiz (8 questions, intermediate level)
- Skill rubric with 4 competency levels
- 15 flashcards for formula syntax
- Estimated completion time

Transcript:
[Paste transcript here]

Include difficulty calibration and prerequisite skills needed.
```

### Example 3: Build Full Micro-Certification Course
```
Create a complete micro-certification course from my expertise:

Topic: "Social Media Content Strategy for E-commerce"
Target audience: Small business owners, no prior experience
Course length: 4 modules, 30-45 minutes total
Certification requirement: 80% pass rate

Content sources:
1. My 10-page guide on content pillars
2. 5 LinkedIn articles on platform strategy
3. 3 case studies from my client work

Deliverables:
- Course outline with module structure
- 4 module summaries (300 words each)
- 4 module quizzes (8 questions each, mixed difficulty)
- 50 flashcards for key concepts
- Final certification exam (15 questions)
- Certificate template text
- Prerequisite map (what learners must complete first)
- WordPress LMS export (LearnDash format)

Tone: Professional but conversational, encouraging for beginners.
```

---

## Capabilities

### 1. Content Structuring & Module Generation
- Analyzes raw content (any format: text, transcripts, PDFs, URLs)
- Auto-generates 3-5 learning objectives per module using SMART criteria
- Creates module summaries (300-500 words) with clear progression
- Maps content to Bloom's taxonomy levels (Remember → Create)
- Suggests optimal module sequencing based on prerequisite dependencies

**Usage:**
```
Structure my 50-page whitepaper on "B2B SaaS Sales Cycles" 
into 5 micro-modules with clear learning objectives and 
prerequisite mapping.
```

### 2. Quiz & Assessment Generation
- **Multiple question types**: Multiple choice, true/false, short answer, matching, scenario-based
- **Difficulty calibration**: Adjusts question complexity (Bloom's L1-L6) to target audience
- **Answer explanations**: Generates detailed rationales for correct/incorrect answers
- **Randomization**: Creates question banks so each learner gets unique quizzes
- **Scoring rubrics**: Builds competency-based rubrics for skill assessments
- **Adaptive testing**: Suggests question selection based on learner performance

**Usage:**
```
Generate 3 quiz versions (easy, medium, hard) for my module on 
"Python Data Structures" with 10 questions each. Include 
explanations for all answers and a scoring guide.
```

### 3. Flashcard & Spaced Repetition
- Creates Anki-compatible flashcard decks (`.apkg` format)
- Generates 8-15 flashcards per module automatically
- Includes images/diagrams where relevant (via DALL-E integration)
- Exports to Quizlet, Anki, or native app formats
- Builds progressive difficulty (foundation → advanced concepts)

**Usage:**
```
Create 12 flashcards for my "Advanced Google Analytics" module.
Include metric definitions, formulas, and real-world examples.
Export as Quizlet and Anki formats.
```

### 4. Prerequisite & Learning Path Mapping
- Analyzes content dependencies and creates prerequisite chains
- Visualizes learning pathways (Mermaid diagrams)
- Identifies skill gaps and suggests supplementary modules
- Recommends sequencing for optimal comprehension
- Flags content that assumes prior knowledge

**Usage:**
```
Map prerequisites for my 6-module course on "Advanced Digital Marketing."
Show which modules must be completed first and identify skill gaps.
Output as a visual learning path diagram.
```

### 5. Difficulty Calibration & Audience Targeting
- Analyzes content complexity using readability metrics (Flesch-Kincaid, SMOG)
- Adjusts language, examples, and pacing for target audience
- Suggests content additions for prerequisite knowledge
- Calibrates quiz difficulty to learner level (novice → expert)
- Recommends estimated completion times

**Usage:**
```
Calibrate my "Advanced Python" course for intermediate learners 
(6-12 months programming experience). Adjust explanations, examples, 
and quiz difficulty accordingly.
```

### 6. Multi-Platform Export
- **WordPress LMS**: LearnDash, LifterLMS, Tutor LMS (XML/JSON)
- **Standalone platforms**: Teachable, Kajabi, Thinkific (CSV/JSON)
- **Google Classroom**: Assignments, quizzes, rubrics
- **PDF**: Printable study guides, certificates
- **SCORM**: Compatible with enterprise LMS platforms
- **Markdown**: For GitHub, Notion, or custom platforms

**Usage:**
```
Export my 4-module course to LearnDash format (WordPress), 
Teachable CSV, and PDF study guides. Include certificate templates.
```

---

## Configuration

### Required Environment Variables
```bash
export OPENAI_API_KEY="sk-..."           # GPT-4 for content generation
export ANTHROPIC_API_KEY="sk-ant-..."    # Claude for assessment design
```

### Optional Environment Variables
```bash
export DALLE_API_KEY="sk-..."            # For flashcard images
export SLACK_WEBHOOK_URL="https://..."   # For progress notifications
export WORDPRESS_API_KEY="..."           # For direct LMS export
export NOTION_API_KEY="..."              # For Notion export
```

### Configuration Options
```json
{
  "content_analysis": {
    "extract_topics": true,
    "identify_prerequisites": true,
    "readability_level": "flesch-kincaid"
  },
  "quiz_generation": {
    "question_types": ["multiple_choice", "true_false", "short_answer"],
    "difficulty_levels": ["beginner", "intermediate", "advanced"],
    "questions_per_module": 8,
    "include_explanations": true
  },
  "flashcard_generation": {
    "cards_per_module": 12,
    "include_images": true,
    "export_formats": ["anki", "quizlet", "json"]
  },
  "export_targets": {
    "wordpress_lms": "learndash",
    "standalone": ["teachable", "kajabi"],
    "formats": ["pdf", "json", "csv"]
  },
  "audience": {
    "level": "beginner",
    "prior_knowledge": "none",
    "learning_style": "visual"
  }
}
```

---

## Example Outputs

### Sample Module Structure (JSON)
```json
{
  "course": {
    "title": "Email Marketing Fundamentals",
    "modules": [
      {
        "module_id": "mod_001",
        "title": "Email Basics & List Building",
        "learning_objectives": [
          "Understand email marketing ROI and best practices",
          "Build a compliant email list using ethical methods",
          "Choose the right email service provider"
        ],
        "content_summary": "This module covers...",
        "estimated_time": "12 minutes",
        "prerequisites": [],
        "quiz": {
          "questions": [
            {
              "id": "q1",
              "type": "multiple_choice",
              "question": "What is the average ROI of email marketing?",
              "options": ["$42:1", "$32:1", "$22:1"],
              "correct_answer": "$42:1",
              "explanation": "Email marketing delivers...",
              "difficulty": "beginner"
            }
          ],
          "passing_score": 80
        },
        "flashcards": [
          {
            "front": "What does GDPR require for email lists?",
            "back": "Explicit opt-in consent from subscribers"
          }
        ]
      }
    ]
  }
}
```

### Sample Quiz Output
```
MODULE 1: Email Basics & List Building
Quiz (8 questions, 15 minutes)

1. (Multiple Choice) What is the average ROI of email marketing?
   A) $42 return per $1 spent ✓ CORRECT
   B) $32 return per $1 spent
   C) $22 return per $1 spent
   
   Explanation: According to the Data & Marketing Association, email marketing 
   delivers an average ROI of $42 for every $1 spent. This makes it one of the 
   highest-ROI marketing channels.

[Questions 2-8 follow same format]

SCORING GUIDE:
7-8 correct: Advanced (90-100%)
5-6 correct: Intermediate (70-89%)
3-4 correct: Beginner (50-69%)
0-2 correct: Review module content (Below 50%)
```

### Sample Flashcard Deck (Anki Format)
```
Front: What is list segmentation?
Back: Dividing your email list into groups based on behavior, 
demographics, or engagement level to send targeted messages.

Front: Name 3 email list-building strategies
Back: 1) Lead magnets (free guides, templates)
      2) Webinar sign-ups
      3) Content upgrades on blog posts

Front: What's the difference between opt-in and opt-out?
Back: Opt-in = user explicitly agrees to receive emails (GDPR compliant)
      Opt-out = user must unsubscribe (not GDPR compliant in EU)
```

---

## Tips & Best Practices

### 1. Content Preparation
- **Use high-quality source material**: Transcripts, blog posts, and case studies work best
- **Include multiple formats**: Mix video transcripts, written guides, and real-world examples
- **Provide context**: Tell the skill the target audience, industry, and use case
- **Specify depth**: Indicate whether you want beginner-friendly or advanced content

### 2. Quiz Optimization
- **Mix question types**: Combine multiple choice (easier to grade) with short answer (deeper learning)
- **Use real-world scenarios**: Include case studies and practical applications
- **Test at multiple levels**: Create pre-quizzes, module quizzes, and final exams
- **Include immediate feedback**: Always provide explanations for correct/incorrect answers

### 3. Course Structure
- **Keep modules focused**: 1-2 learning objectives per module (not 5+)
- **Aim for 10-15 minute modules**: Optimal for completion and retention
- **Map prerequisites carefully**: Prevent learners from skipping foundational content
- **Progressive difficulty**: Start beginner, end advanced (Bloom's L1→L6)

### 4. Export & Distribution
- **Test exports**: Verify WordPress/Teachable imports work before launching
- **Use certificate incentives**: Boost completion rates by 30-40%
- **Enable mobile access**: Ensure flashcards and quizzes work on phones
- **Track completion**: Use LMS analytics to identify drop-off points

### 5. Iterative Improvement
- **Collect learner feedback**: Ask what was confusing or missing
- **Monitor quiz difficulty**: Adjust if >80% pass or <50% pass
- **Update content quarterly**: Keep examples and case studies current
- **A/B test quizzes**: Try different question types to maximize engagement

---

## Safety & Guardrails

### What This Skill Will NOT Do

**❌ Guarantee subject matter accuracy**: This skill generates content based on your input. You remain responsible for factual accuracy, compliance, and legal requirements. Always review generated content before publishing.

**❌ Create original research or data**: The skill structures and formats existing knowledge. It does not conduct original research, generate fabricated statistics, or create unsourced claims.

**❌ Replace human instructional design for complex topics**: For highly technical, regulated (healthcare, finance, law), or safety-critical content, human instructional designers should review and validate the output.

**❌ Handle sensitive personal data**: Do not use this skill with personally identifiable information (PII), health records, or confidential business data. All content is processed via third-party APIs.

**❌ Guarantee WCAG accessibility compliance**: Generated content should be reviewed for accessibility standards (alt text, color contrast, keyboard navigation) before publishing.

**❌ Ensure copyright/IP compliance**: You are responsible for ensuring all source content is your own or properly licensed. The skill does not verify copyright status.

### Boundaries & Limitations

- **Maximum content size**: 50,000 words per request (split larger courses into multiple requests)
- **Language support**: English optimized; other languages may have reduced accuracy
- **Quiz randomization**: Limited to 10 question variations per question (not infinite)
- **Image generation**: DALL-E integration limited to 10 flashcard images per request
- **Export formats**: Not compatible with all legacy LMS platforms (pre-2015)
- **Real-time updates**: Exports are static; changes require re-export

### Compliance Considerations

- **GDPR**: Do not process EU learner data without explicit consent
- **COPPA**: Do not create courses for children <13 without parental consent mechanisms
- **ADA/Section 508**: Review accessibility before publishing to public audiences
- **Professional licensing**: Verify that certifications comply with regulatory requirements in your jurisdiction
- **IP rights**: Ensure you own or have licensed all source material

---

## Troubleshooting

### Common Issues & Solutions

**Q: Generated quiz questions are too easy/hard**
- A: Specify target audience explicitly: "Intermediate learners with 2+ years experience"
- Adjust difficulty levels in config: `"difficulty_levels": ["intermediate", "advanced"]`
- Request specific Bloom's levels: "Focus on Analysis (L4) and Synthesis (L5) questions"

**Q: Flashcards have too much/too little information**
- A: Specify card length: "Create concise 1-2 sentence flashcards" or "Create detailed flashcards with examples