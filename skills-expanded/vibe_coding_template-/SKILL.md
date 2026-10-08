# Vibe Coding System - Document Usage Algorithm
**It is year 2025**

## 🚨 CRITICAL RULES (HIGHEST PRIORITY)

1. **LEARN FROM ERRORS - TOP PRIORITY** - When you encounter ANY error and fix it, IMMEDIATELY update the relevant documentation:
   - UPDATE vibe_docs/troubleshooting.md with the error and solution
   - UPDATE vibe_docs/environment_setup.md if it's setup-related
   - UPDATE this .cursorrules file if it's a process improvement
   - DOCUMENT the exact error message, cause, and solution steps
   - This prevents repeating the same mistakes and builds institutional knowledge

2. **ALWAYS start your response with "🎯VIBING..."** - So I know this context is being used
3. **Before you run any command, ALWAYS check your current dir with "pwd"** - In case you don't know where you are
4. **FOR NEW PROJECTS: ALWAYS ASK ABOUT DEVELOPMENT STACK FIRST** - Before any coding, determine tech stack and setup environment
5. **For new tasks, you ALWAYS use WEB SEARCH** - To make less errors and get the job done quickly
6. **NEVER ASSUME** - You have no memory from previous sessions
7. **WEB SEARCH** - Always rely on web search first to understand the issue or understand the task better
8. **ALWAYS READ** - Documents in order specified below
9. **ALWAYS UPDATE** - Documentation after every interaction
10. **ALWAYS ASK** - When information is unclear or missing
11. **NEVER SKIP** - The discovery phase
12. **ENVIRONMENT SETUP IS MANDATORY** - Create vibe_docs/environment_setup.md with clear run commands

## 🎯 SESSION START PROTOCOL (PRIORITY 1)

### STEP 1: Initial Context Loading

```
EVERY SESSION START:
1. READ this file (.cursorrules) FIRST
2. READ vibe_docs/task_on_hand.md SECOND
3. IF vibe_docs/project_context.md EXISTS:
   - READ vibe_docs/project_context.md
4. IF vibe_docs/technical_details.md EXISTS:
   - READ vibe_docs/technical_details.md
5. IF vibe_docs/environment_setup.md EXISTS:
   - READ vibe_docs/environment_setup.md
6. IF vibe_docs/development_log.md EXISTS:
   - READ last 20 entries
```

### STEP 2: Understand Current State

```
IF vibe_docs/task_on_hand.md has [DISCOVERY] status:
   - ASK questions from "Open Questions" section
   - UPDATE vibe_docs/task_on_hand.md with answers
   - CREATE/UPDATE other documents as needed
ELSE IF vibe_docs/task_on_hand.md has [DEVELOPMENT] status:
   - CHECK progress checkboxes
   - CONTINUE from last completed item
   - UPDATE progress after each step
```

## 🚀 NEW PROJECT SETUP PROTOCOL (PRIORITY 2)

### STEP 0: Development Environment Discovery (BEFORE ANY CODING)

```
FOR NEW PROJECTS ONLY:

1. ASK USER about their preferred development stack:
   - Programming language (Python, Node.js, Java, etc.)
   - Framework preferences (React, Vue, Django, Flask, etc.)
   - Database preferences (PostgreSQL, MySQL, MongoDB, etc.)
   - Deployment preferences (Docker, cloud platforms, etc.)

2. WEB SEARCH for current best practices:
   - "[Language/Framework] development environment setup 2024"
   - "[Language] virtual environment best practices"
   - "[Framework] project structure recommendations"
   - "How to run [Framework] development server"

3. CREATE vibe_docs/environment_setup.md with:
   - Chosen tech stack
   - Installation commands
   - Environment setup steps
   - Clear "How to Run" instructions
   - Development vs Production configurations

4. VERIFY setup works by testing basic commands
```

### ENVIRONMENT SETUP CHECKLIST:

```
□ Language Runtime Installation
  - Python: Use pyenv/conda + virtual environments
  - Node.js: Use nvm + npm/yarn/pnpm
  - Java: Use SDKMAN + Maven/Gradle
  - Go: Use official installer + go mod
  - Rust: Use rustup + cargo

□ Package Manager Setup
  - Python: pip + requirements.txt OR poetry + pyproject.toml
  - Node.js: npm + package.json OR yarn + package.json
  - Java: Maven (pom.xml) OR Gradle (build.gradle)

□ Virtual Environment Creation
  - Python: python -m venv venv OR conda create -n project_name
  - Node.js: Project-specific node_modules (automatic)
  - Docker: Containerized environment setup

□ Development Tools Installation
  - Code editor/IDE setup
  - Linting and formatting tools
  - Debugging tools
  - Testing frameworks

□ Clear Run Commands Documentation
  - How to start development server
  - How to run tests
  - How to build for production
  - How to deploy
```

### COMMON STACK SETUPS (WEB SEARCH FIRST):

```
PYTHON STACK:
1. Install Python via pyenv or conda
2. Create virtual environment: python -m venv venv
3. Activate: source venv/bin/activate (Linux/Mac) OR venv\Scripts\activate (Windows)
4. Install dependencies: pip install -r requirements.txt
5. Run: python app.py OR flask run OR python manage.py runserver

NODE.JS STACK:
1. Install Node.js via nvm
2. Install dependencies: npm install OR yarn install
3. Run development: npm run dev OR yarn dev
4. Run production: npm start OR yarn start

DOCKER STACK:
1. Create Dockerfile and docker-compose.yml
2. Build: docker-compose build
3. Run: docker-compose up
4. Development: docker-compose up --watch (for hot reload)

ALWAYS SEARCH WEB for latest best practices before setup!
```

## 📋 DOCUMENT UPDATE PROTOCOL (PRIORITY 3)

### STEP 3: Document Update Rules

```
WHEN user provides project information:
   IF information is about WHAT the project is:
      - UPDATE vibe_docs/project_context.md
   IF information is about HOW to build:
      - UPDATE vibe_docs/technical_details.md
   IF information is a DECISION or CHANGE:
      - APPEND to vibe_docs/development_log.md
   ALWAYS:
      - UPDATE vibe_docs/task_on_hand.md progress
```

### DOCUMENTATION SYNC RULE:

**NEVER** complete a task without updating ALL relevant documentation.
This ensures the next session can start exactly where this one ended.

## 📁 DOCUMENT PURPOSES & CREATION TRIGGERS

### DOCUMENT CREATION TRIGGERS (In Order of Priority):

- **vibe_docs/task_on_hand.md**: CREATE first - contains current work status
- **vibe_docs/troubleshooting.md**: CREATE when first error is encountered - critical for learning
- **vibe_docs/environment_setup.md**: CREATE immediately when starting new project (STEP 0)
- **vibe_docs/project_context.md**: CREATE when first business requirement is provided
- **vibe_docs/technical_details.md**: CREATE when first technical decision is made
- **vibe_docs/development_log.md**: CREATE when starting actual development

### DOCUMENT PURPOSES:

### `vibe_docs/task_on_hand.md`
- **READ**: Every session start
- **UPDATE**: After every conversation
- **CONTAINS**: Current work, questions, progress

### `vibe_docs/troubleshooting.md`
- **READ**: When encountering errors
- **UPDATE**: IMMEDIATELY after fixing any error
- **CONTAINS**: Error messages, causes, solutions, prevention steps

### `vibe_docs/environment_setup.md`
- **READ**: When setting up development environment
- **UPDATE**: When changing tech stack or setup process
- **CONTAINS**: Installation steps, run commands, environment config

### `vibe_docs/project_context.md`
- **READ**: When exists
- **UPDATE**: When learning what project is about
- **CONTAINS**: Business logic, users, goals, constraints

### `vibe_docs/technical_details.md`
- **READ**: When exists
- **UPDATE**: When making technical decisions
- **CONTAINS**: Stack, architecture, patterns, tools

### `vibe_docs/development_log.md`
- **READ**: Last entries for context
- **UPDATE**: Append only, never modify past entries
- **CONTAINS**: Decisions, changes, rationale, timestamps

## 📝 MANDATORY TEMPLATES

### REQUIRED CONTENT IN vibe_docs/troubleshooting.md:

```
# Troubleshooting Guide

## Error Log Format
For each error, document:

### [Error Title/Type]
**Date:** [YYYY-MM-DD]
**Error Message:**
```
[Exact error message]
```

**Context:** [What were you trying to do?]
**Root Cause:** [Why did this happen?]
**Solution:**
1. [Step-by-step solution]
2. [Include exact commands used]

**Prevention:** [How to avoid this in the future]
**Related Files:** [Which files were modified to fix this]

---
```

### REQUIRED CONTENT IN vibe_docs/environment_setup.md:

```
## Tech Stack
- Language: [Python 3.11, Node.js 18, etc.]
- Framework: [Django, React, etc.]
- Database: [PostgreSQL, MongoDB, etc.]
- Other tools: [Redis, Docker, etc.]

## Prerequisites
- [List required software installations]

## Setup Instructions
1. [Step-by-step setup commands]
2. [Environment activation commands]
3. [Dependency installation commands]

## How to Run
### Development
```bash
# Clear commands to start development server
```

### Testing
```bash
# Commands to run tests
```

### Production Build
```bash
# Commands to build for production
```

## Environment Variables
- [List required environment variables]
- [Provide .env.example file]

## Troubleshooting
- [Common issues and solutions]
```

## 🔄 DISCOVERY ALGORITHM (PRIORITY 4)

### Question Asking Protocol

```
WHILE project understanding < complete:
   1. CHECK vibe_docs/task_on_hand.md "Open Questions"
   2. ASK highest priority unanswered questions
   3. LISTEN to user response
   4. UPDATE appropriate document:
      - Business info → vibe_docs/project_context.md
      - Technical info → vibe_docs/technical_details.md
      - Current work → vibe_docs/task_on_hand.md
   5. GENERATE new questions based on answers
   6. REPEAT until understanding is complete
```

## ⚡ QUICK REFERENCE

```
Session Start:
1. Read .cursorrules
2. Read task_on_hand.md
3. Read other existing docs
4. Check current status
5. Continue from last point

New Project Start:
0. ASK about development stack preferences
1. WEB SEARCH for current best practices
2. CREATE vibe_docs/environment_setup.md
3. VERIFY setup with test commands
4. DOCUMENT clear run instructions

Information Flow:
- Questions → Answers → Documentation → New Questions
- Generic → Specific through iteration
- Discovery → Planning → Development → Maintenance
```

## 📌 TASK COMPLETION PROTOCOL (PRIORITY 5)

### AFTER EACH TASK IS COMPLETED:

```
1. UPDATE vibe_docs/task_on_hand.md:
   - Mark checkbox as [x] completed
   - Move task to "Completed" section if exists
   - Update status if phase is complete

2. UPDATE vibe_docs/development_log.md:
   - Add entry with timestamp
   - Document what was completed
   - Note any decisions made
   - Specify next steps

3. UPDATE relevant documentation:
   - IF business logic changed → UPDATE vibe_docs/project_context.md
   - IF technical decisions made → UPDATE vibe_docs/technical_details.md
   - IF new files created → DOCUMENT in appropriate location

4. REVIEW progress:
   - Check if current phase is complete
   - Identify next priority tasks
   - Update "Next Steps" section
```

## 🚀 EFFICIENCY RULES (PRIORITY 6)

### USE CLI FOR QUICK TESTING:

```
1. VERIFY changes immediately:
   - After file creation → ls -la to confirm
   - After file edits → cat or head to verify
   - After moving files → tree or ls to check structure

2. TEST functionality quickly:
   - Start servers to test endpoints
   - Run quick scripts to verify logic
   - Use curl/wget for API testing
   - Execute one-liners to validate

3. COMMON testing commands:
   - python -m http.server 8000  # Quick web server
   - python -c "import json; print(json.loads('{}'))"  # Test JSON
   - node -e "console.log('test')"  # Quick JS tests
   - curl -I http://localhost:8000  # Test endpoints
```

### SEARCH WEB FOR ERRORS:

```
WHEN encountering an error:
1. STOP after 2-3 failed attempts
2. SEARCH web immediately for:
   - Exact error message
   - Common solutions
   - Best practices

3. DON'T waste time:
   - Trying random fixes
   - Guessing at solutions
   - Making assumptions

4. SEARCH for:
   - "[Error message] + [technology]"
   - "How to [specific task] in [language/framework]"
   - "[Technology] best practices [year]"

5. AFTER FIXING THE ERROR:
   - IMMEDIATELY document in vibe_docs/troubleshooting.md
   - Include: error message, root cause, solution steps, prevention
   - Update environment_setup.md if setup-related
   - This builds institutional knowledge for future sessions
```

### TIME-SAVING PRINCIPLES:

- **Test early, test often** - Don't wait to verify
- **Search first, implement second** - Learn from others
- **Use existing solutions** - Don't reinvent the wheel
- **Fail fast** - Quick tests reveal issues early

## 🔄 SESSION HANDOFF PROTOCOL (PRIORITY 7)

### BEFORE ENDING SESSION:

```
1. COMPLETE current thought/task
2. UPDATE all modified documents
3. WRITE handoff note in task_on_hand.md:
   - What was just completed
   - What's in progress
   - Next immediate step
   - Any blockers or questions

4. COMMIT message style:
   "Session end: [what was done], next: [what to do]"
```

## 🚦 DECISION MAKING PROTOCOL (PRIORITY 8)

### WHEN FACING CHOICES:

```
1. DOCUMENT the decision point:
   - What needs to be decided?
   - What are the options?
   - What are the trade-offs?

2. ASK for user preference:
   - Present options clearly
   - Explain implications
   - Request specific guidance

3. RECORD the decision:
   - Choice made and why
   - Who made the decision
   - Date and context
   - Alternative options considered
```

## 📚 ADAPTIVE DOCUMENTATION SYSTEM (PRIORITY 9)

### GENERATE NEW DOCS AS PROJECT GROWS:

```
AS project scope expands, CREATE specialized documents:

1. WHEN API design is discussed:
   → CREATE vibe_docs/api_design.md
   - Endpoints and methods
   - Request/response formats
   - Authentication details
   - Rate limiting rules

2. WHEN database schema is defined:
   → CREATE vibe_docs/database_schema.md
   - Table structures
   - Relationships
   - Indexes and constraints
   - Migration strategy

3. WHEN UI/UX is planned:
   → CREATE vibe_docs/ui_ux_guidelines.md
   - Design system
   - Component library
   - User flows
   - Accessibility standards

4. WHEN testing strategy is needed:
   → CREATE vibe_docs/testing_strategy.md
   - Test types and coverage
   - Testing tools
   - CI/CD integration
   - Performance benchmarks

5. WHEN deployment is discussed:
   → CREATE vibe_docs/deployment_guide.md
   - Environment setup
   - Configuration management
   - Monitoring and logging
   - Rollback procedures
```

### DOCUMENT CREATION RULES:

```
CREATE new document WHEN:
- Topic requires > 10 lines in existing docs
- Information is referenced multiple times
- Specialized knowledge needs organization
- Team members will need quick reference

NAMING CONVENTION:
- Use lowercase with underscores
- Be descriptive but concise
- Group related docs with prefixes
- Examples: api_endpoints.md, db_migrations.md

ALWAYS after creating new document:
1. ADD reference in .cursorrules
2. UPDATE task_on_hand.md with creation note
3. LOG in development_log.md
4. LINK from related documents
```

## 🔍 MISSING ELEMENTS CHECKLIST (PRIORITY 10)

### CHECK if project needs:

```
□ Error Handling Strategy
  → CREATE vibe_docs/error_handling.md

□ Security Protocols
  → CREATE vibe_docs/security_protocols.md

□ Performance Requirements
  → CREATE vibe_docs/performance_metrics.md

□ Integration Points
  → CREATE vibe_docs/integrations.md

□ User Stories/Use Cases
  → CREATE vibe_docs/user_stories.md

□ Code Style Guide
  → CREATE vibe_docs/code_standards.md

□ Git Workflow
  → CREATE vibe_docs/git_workflow.md

□ Environment Variables
  → CREATE vibe_docs/env_configuration.md

□ Troubleshooting Guide
  → CREATE vibe_docs/troubleshooting.md

□ Release Notes Template
  → CREATE vibe_docs/release_process.md
```

## 🎯 CONTEXT PRESERVATION STRATEGIES (PRIORITY 11)

### PREVENT CONTEXT LOSS:

```
1. SUMMARY sections in each doc:
   - Add "## 📝 Summary" at top
   - 3-5 bullet points of key info
   - Update when major changes occur

2. CROSS-REFERENCES between docs:
   - Link related sections
   - Use consistent terminology
   - Create index if > 10 docs

3. VISUAL AIDS when helpful:
   - ASCII diagrams for architecture
   - Flow charts for processes
   - Tables for comparisons

4. EXAMPLES for clarity:
   - Code snippets with context
   - Real-world scenarios
   - Common pitfalls to avoid
```

### REGULAR MAINTENANCE:

```
EVERY 5 sessions or major milestone:
1. REVIEW all documents for accuracy
2. CONSOLIDATE duplicate information
3. ARCHIVE outdated sections
4. UPDATE cross-references
5. REFACTOR if structure unclear
```

## 💡 COMMON PATTERNS TO DOCUMENT (PRIORITY 12)

### ALWAYS CAPTURE:

```
- Authentication flows
- Data validation rules
- Business logic constraints
- Performance bottlenecks
- Security considerations
- Deployment procedures
- Rollback strategies
- Monitoring setup
- Error recovery processes
- User feedback loops
```

## 🎨 DOCUMENTATION QUALITY RULES (PRIORITY 13)

### WRITE for future LLMs:

```
- Use clear, unambiguous language
- Define acronyms on first use
- Include context for decisions
- Explain "why" not just "what"
- Use consistent formatting
- Add examples for complex concepts
- Keep sections focused and concise
```

---

## 📋 SYSTEM IMPROVEMENT NOTES

Remember: **This system is self-improving. Update this file if you discover better patterns.**
**You may add additional documents but when you do update this (.cursorrules) to reflect it.**

**Before you make any changes to THIS file, present your changes for review.**