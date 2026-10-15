---
name: hermes-edu-skills
description: Install and use China-focused education Agent Skills for textbook sync, exam prep, mistake review, daily practice, and teacher workflows with Hermes Agent
triggers:
  - how do I install Chinese education skills into Hermes
  - use hermes-edu-skills for textbook aligned questions
  - install agent skills for Chinese K12 education
  - how to add exam prep skills to my Hermes agent
  - integrate education skill pack with Hermes
  - search hermes-edu-skills for mistake review
  - export hermes education skills to Cursor
  - install textbook-sync category into Hermes
---

# hermes-edu-skills

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

`hermes-edu-skills` is an open-source Agent Skill Pack providing 170 structured education capabilities aligned with China's K-12 curriculum. It enables Hermes Agent and other AI tools to understand Chinese textbook versions (人教, 统编, 北师大, 苏教, etc.), grade levels, units, exam systems, and real education workflows.

Unlike prompt collections, each skill is a structured `SKILL.md` with triggers, roles, parameters, boundaries, and standard metadata. Skills cover:

- **Textbook sync** (41 skills): Grade/unit/lesson-aligned exercises and explanations
- **Learning core** (15 skills): Study plans, photo Q&A, mistake review, learning reports
- **Daily practice** (28 skills): Mental math, dictation, recitation, vocabulary drills
- **Reading & writing** (10 skills): Chinese/English composition, academic writing
- **Exam prep** (27 skills): Midterm, high school entrance, college entrance, certification exams
- **Teacher tools** (31 skills): Lesson prep, assignment generation, class analysis
- **Family education** (8 skills): Parent-child learning, reading habits, homework support
- **Language learning** (3 skills): Adult English, IELTS/TOEFL, oral practice
- **Career learning** (7 skills): University, certification, professional development

The project is maintained by [Shineway Technology](https://www.shineway.tech/) and released under MIT license.

## Installation

### Install CLI globally or via npx

```bash
# Use npx (recommended - no install needed)
npx hermes-edu-skills --version

# Or install globally
npm install -g hermes-edu-skills
```

### Install all 170 skills into Hermes Agent

```bash
# Default: installs all skills + generates HERMES.md prompt
npx hermes-edu-skills install hermes --config ~/.hermes/config.yaml

# Install without generating prompt
npx hermes-edu-skills install hermes --config ~/.hermes/config.yaml --no-prompt

# Force overwrite existing HERMES.md
npx hermes-edu-skills install hermes --config ~/.hermes/config.yaml --overwrite-prompt
```

This command:
1. Adds `skills/` directory to Hermes `skills.external_dirs` in config
2. Generates `HERMES.md` in current directory with project-level prompt
3. Makes all 170 skills discoverable by Hermes

### Install by category

```bash
# Install textbook sync category (41 skills)
npx hermes-edu-skills install hermes textbook-sync --config ~/.hermes/config.yaml

# Install learning core category (15 skills)
npx hermes-edu-skills install hermes learning-core --config ~/.hermes/config.yaml

# Install exam prep category (27 skills)
npx hermes-edu-skills install hermes exam-prep --config ~/.hermes/config.yaml

# Chinese category names also supported
npx hermes-edu-skills install hermes 教材同步 --config ~/.hermes/config.yaml
```

Category-specific install generates scoped `HERMES.md` prompting Hermes to search only that category.

### Install single skill

```bash
# Install only study plan skill
npx hermes-edu-skills install hermes agent-study-plan --config ~/.hermes/config.yaml

# Install mistake review skill
npx hermes-edu-skills install hermes agent-mistake-review --config ~/.hermes/config.yaml
```

Single skill install generates `HERMES.md` scoped to that skill's triggers.

## Key Commands

### Search and discovery

```bash
# Search skills by keyword
npx hermes-edu-skills search 错题
npx hermes-edu-skills search textbook
npx hermes-edu-skills search exam

# Get detailed info about a skill
npx hermes-edu-skills info agent-mistake-review
npx hermes-edu-skills info textbook-exercise-generator

# List all categories
npx hermes-edu-skills list categories

# List skills in a category
npx hermes-edu-skills list textbook-sync
```

### Interactive query with skill routing

```bash
# Ask a question - shows matched skills then calls Hermes
npx hermes-edu-skills ask "帮我出5道八年级下册物理力学选择题"

# The command will:
# 1. Search relevant skills (e.g. textbook-exercise-generator)
# 2. Display matched skills
# 3. Route to Hermes with skill context
```

### Generate project prompt

```bash
# View full HERMES.md prompt content
npx hermes-edu-skills prompt

# Save to file
npx hermes-edu-skills prompt > HERMES.md

# Generate prompt for specific category
npx hermes-edu-skills prompt --category textbook-sync > HERMES_TEXTBOOK.md
```

### Diagnostics

```bash
# Check installation status, version, config, Hermes visibility
npx hermes-edu-skills doctor

# Output shows:
# - Number of skills installed
# - Categories available
# - Hermes config path and status
# - HERMES.md existence
# - Version info
```

## Export to Other AI Tools

### Export to Cursor

```bash
# Install to Cursor workspace
npx hermes-edu-skills install cursor --workspace /path/to/project

# Installs to /path/to/project/.cursor/skills/
```

### Export to OpenClaw

```bash
npx hermes-edu-skills install openclaw

# Installs to ~/.openclaw/skills/hermes-edu-skills/
```

### Export to Codex

```bash
npx hermes-edu-skills install codex

# Installs to ~/.codex/skills/hermes-edu-skills/
```

### Export to Claude

```bash
npx hermes-edu-skills install claude

# Installs to ~/.claude/skills/hermes-edu-skills/
```

### Generic export

```bash
# Export all skills to custom directory
npx hermes-edu-skills export generic --target ./dist/agent-skills

# Export single category
npx hermes-edu-skills export generic --target ./dist/textbook --category textbook-sync
```

## Configuration

### Hermes config.yaml structure

The installer modifies `~/.hermes/config.yaml` (or custom path via `--config`):

```yaml
skills:
  dirs:
    - ~/.hermes/skills
  external_dirs:
    - /path/to/hermes-edu-skills/skills  # Added by installer
  
  discovery:
    enabled: true
    auto_load: true
```

### Environment variables

```bash
# Override default Hermes config path
export HERMES_CONFIG_PATH=~/custom/hermes/config.yaml

# Use custom install location
export HERMES_EDU_SKILLS_PATH=~/my-skills/hermes-edu
```

## Real Usage Examples

### Example 1: Textbook-aligned exercise generation

After installing `textbook-sync` category:

```javascript
// In Hermes Agent session or via API
const request = {
  skill: 'textbook-exercise-generator',
  params: {
    subject: '物理',
    grade: '八年级',
    semester: '下册',
    textbook_version: '人教版',
    unit: '第七单元：力',
    exercise_type: '选择题',
    difficulty: '中等',
    quantity: 5
  }
};

// Hermes routes to skill and returns structured exercises
```

User query that triggers this:
```
"帮我出5道八年级下册物理力学选择题，人教版"
```

### Example 2: Mistake review workflow

After installing `agent-mistake-review` skill:

```javascript
// User uploads photo of wrong problem
const mistakeReview = {
  skill: 'agent-mistake-review',
  input: {
    image: 'data:image/jpeg;base64,...',
    subject: '数学',
    grade: '九年级'
  }
};

// Skill returns:
// 1. Original problem transcription
// 2. Student's wrong answer analysis
// 3. Correct solution step-by-step
// 4. Knowledge point summary
// 5. Similar practice problems (3-5)
```

User query:
```
"这道题我做错了，帮我分析一下" [with image]
```

### Example 3: Daily math drill

After installing `daily-practice` category:

```javascript
// Generate daily mental math practice
const dailyDrill = {
  skill: 'daily-mental-math',
  params: {
    grade: '三年级',
    operation_types: ['加法', '减法'],
    difficulty: '基础',
    quantity: 20,
    time_limit_minutes: 5
  }
};

// Returns 20 problems with timer and auto-grading
```

User query:
```
"给我三年级的口算练习，20道题，加减法"
```

### Example 4: Teacher lesson prep

After installing `teacher-tools` category:

```javascript
// Generate lesson plan
const lessonPrep = {
  skill: 'teacher-lesson-planner',
  params: {
    subject: '语文',
    grade: '五年级',
    semester: '上册',
    textbook_version: '统编版',
    lesson: '第15课：桂花雨',
    class_duration: 40,
    teaching_goals: ['理解课文内容', '感受思乡情感', '学习生字词']
  }
};

// Returns:
// - Teaching objectives
// - Key/difficult points
// - Teaching process (导入-新授-练习-总结)
// - Classroom activities
// - Homework assignment
```

User query:
```
"帮我备课，五年级语文统编版第15课桂花雨，一节课40分钟"
```

### Example 5: Exam prep study plan

After installing `exam-prep` category:

```javascript
// Generate high school entrance exam prep plan
const examPlan = {
  skill: 'exam-prep-study-planner',
  params: {
    exam_type: '中考',
    subjects: ['数学', '物理', '化学'],
    current_level: '中等',
    target_score: '优秀',
    days_until_exam: 90,
    daily_study_hours: 2
  }
};

// Returns:
// - 90-day phased plan (基础-强化-冲刺)
// - Daily task breakdown by subject
// - Weekly mock exam schedule
// - Weak point focus areas
// - Progress tracking checkpoints
```

User query:
```
"距离中考还有90天，帮我制定数理化复习计划，每天2小时"
```

## Skill Structure

Each skill is a `SKILL.md` file with:

```markdown
---
id: skill-unique-id
name: Display Name
description: One-line description
category: textbook-sync
subcategory: exercise-generation
version: 1.0.0
author: Shineway
tags: [grade, subject, textbook]
triggers:
  - "natural phrase user might say"
  - "another trigger phrase"
parameters:
  - name: grade
    type: string
    required: true
    options: [一年级, 二年级, ..., 高三]
  - name: subject
    type: string
    required: true
roles: [student, teacher, parent]
complexity: medium
estimated_tokens: 500
---

# Skill Content

Detailed prompt and workflow...
```

## Common Patterns

### Pattern 1: Grade/semester parameter normalization

Skills normalize Chinese grade expressions:

```javascript
// All these map to same internal grade level:
"一年级上册" → grade: 1, semester: 1
"小学一年级第一学期" → grade: 1, semester: 1  
"1年级上" → grade: 1, semester: 1
```

### Pattern 2: Textbook version detection

Skills recognize major Chinese textbook publishers:

- 人教版 (People's Education Press)
- 统编版 (National Unified Edition)
- 北师大版 (Beijing Normal University)
- 苏教版 (Jiangsu Education)
- 鲁科版 (Shandong Science & Tech)

### Pattern 3: Difficulty calibration

Standard difficulty levels across skills:

- `基础` (basic): 60-70% students should master
- `中等` (medium): 40-50% students should master  
- `提高` (advanced): 20-30% students should master
- `拔高` (olympiad): <10% students should master

### Pattern 4: Multi-skill workflow

Complex tasks chain multiple skills:

```javascript
// 1. Photo Q&A extracts problem
skill: 'agent-photo-qa'

// 2. Mistake review analyzes error  
skill: 'agent-mistake-review'

// 3. Exercise generator creates similar problems
skill: 'textbook-exercise-generator'

// 4. Daily practice adds to drill queue
skill: 'daily-practice-tracker'
```

## Troubleshooting

### Skills not appearing in Hermes

**Check config path:**
```bash
npx hermes-edu-skills doctor

# Verify skills.external_dirs contains correct path
cat ~/.hermes/config.yaml | grep external_dirs
```

**Manually add to config:**
```yaml
skills:
  external_dirs:
    - /absolute/path/to/hermes-edu-skills/skills
```

**Restart Hermes:**
```bash
hermes restart
```

### Hermes not routing to education skills

**Verify HERMES.md exists and is loaded:**
```bash
# Check current directory for HERMES.md
ls -la HERMES.md

# Regenerate if missing
npx hermes-edu-skills prompt > HERMES.md
```

**Check Hermes project prompt loading:**
```bash
# Hermes should load HERMES.md from project root
# Or from config-specified project_prompt_path
```

**Test with explicit skill mention:**
```
"使用 hermes-edu-skills 的 textbook-exercise-generator 技能出5道题"
```

### Search returns no results

**Update catalog:**
```bash
# Catalog is pre-built, but if modified locally:
cd hermes-edu-skills/
node scripts/build-catalog.js
```

**Check skill ID spelling:**
```bash
# List all skill IDs
npx hermes-edu-skills list all | grep "id:"
```

### Export fails for target platform

**Check target directory permissions:**
```bash
# Cursor export
ls -ld ~/.cursor/skills/
mkdir -p ~/.cursor/skills/  # if missing

# Generic export
mkdir -p ./target/dir
npx hermes-edu-skills export generic --target ./target/dir
```

**Use absolute paths:**
```bash
npx hermes-edu-skills install cursor --workspace $(pwd)/my-project
```

## Development and Contribution

### Run from source

```bash
git clone https://github.com/zhongweiv/hermes-edu-skills.git
cd hermes-edu-skills/

# Install dependencies
npm install

# Run CLI locally
npm run cli -- install hermes --config ~/.hermes/config.yaml

# Run tests
npm test

# Validate all skills
npm run validate
```

### Create new skill

1. Copy template from `skills/_template/SKILL.md`
2. Fill in YAML frontmatter and content
3. Place in appropriate category directory: `skills/<category>/<skill-id>/SKILL.md`
4. Run validation:

```bash
npm run validate
```

5. Update catalog:

```bash
node scripts/build-catalog.js
```

6. Test installation:

```bash
npm run cli -- info your-new-skill-id
npm run cli -- install hermes your-new-skill-id --config ~/.hermes/config.yaml
```

### Validation rules

Skills must pass:

- YAML frontmatter syntax
- Required fields: id, name, description, category, triggers
- Triggers: 6-8 natural phrases
- Parameters: valid types (string, number, boolean, array, object)
- File location: `skills/<category>/<id>/SKILL.md`
- Unique ID across all skills

Run validator:

```bash
npx hermes-edu-skills validate
```

## API Reference (if running as library)

```javascript
import { HermesEduSkills } from 'hermes-edu-skills';

const skills = new HermesEduSkills();

// Search skills
const results = skills.search('错题复盘');

// Get skill metadata
const skill = skills.getSkill('agent-mistake-review');

// List categories
const categories = skills.listCategories();

// Install programmatically
await skills.install('hermes', {
  configPath: '~/.hermes/config.yaml',
  categories: ['textbook-sync'],
  generatePrompt: true
});
```

## Resources

- **GitHub**: https://github.com/zhongweiv/hermes-edu-skills
- **Homepage**: https://www.shineway.tech/
- **Skill Catalog**: [catalog.json](https://github.com/zhongweiv/hermes-edu-skills/blob/main/catalog.json)
- **Discovery Index**: [.well-known/skills/index.json](https://github.com/zhongweiv/hermes-edu-skills/blob/main/.well-known/skills/index.json)
- **Demo Video**: https://zhongweiv.github.io/hermes-edu-skills/demo/
- **License**: MIT

---

This skill enables AI agents to help developers integrate China-focused education capabilities into Hermes Agent and other AI tools through structured, curriculum-aligned Agent Skills.
