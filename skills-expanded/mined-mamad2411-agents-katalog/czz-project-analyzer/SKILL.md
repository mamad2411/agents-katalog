---
name: czz-project-analyzer
description: Comprehensive open source project analysis using a structured template. Use when user asks to analyze an open source project, review code architecture, or evaluate a GitHub repository.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["find", "ls", "tree", "git"] },
        "install": "No installation required - uses standard CLI tools",
        "category": "analysis"
      }
  }
---

# CZZ Project

This skill provides a systematic approach to analyzing projects with structured reporting and visual diagrams.

## When to Use This Skill

Use this skill when the user:

- Asks to "analyze", "review", or "evaluate" a project
- Wants to understand the architecture of a codebase
- Needs a detailed evaluation of a project (local or remote)
- Requests a project report or summary
- Mentions "I want to analyze [project name/path]"
- Asks for recommendations about a specific project

## Supported Project Types

**Local Projects** (Primary):
- Local directory paths: `~/work/my-project`
- Current directory: `.`
- Relative paths: `./my-project`
- Absolute paths: `/Users/ccc/work/todo/kubernetes`

**Remote Projects** (Optional):
- GitHub repositories: `owner/repo`
- Git URLs: `https://github.com/owner/repo`

## Workflow Overview

The analysis follows a **12-step sequential process** with progress reporting:

1. **📋 Project Basic Info** - Basic metadata (language, file count, structure)
2. **🏗️ Project Structure** - Directory structure and module relationships
3. **🛠️ Tech Stack** - Dependencies and frameworks
4. **🎯 Core Features** - Key features with sequence diagram
5. **🏛️ Architecture Design** - Architecture patterns with diagrams
6. **📊 Code Quality** - Code style, testing, complexity
7. **📚 Documentation Quality** - README, API docs, guides
8. **📈 Project Activity** - Commits, issues, PRs (from git if available)
9. **✅ Pros/Cons** - Strengths and weaknesses
10. **🎯 Use Cases** - When to use/not use
11. **💡 Learning Value** - What's worth learning
12. **📝 Summary** - Final verdict

## Advanced Deep-Dive Analysis Mode

For complex or technical projects, enable **Deep Analysis Mode** which adds:

13. **🔧 Source Code Deep Dive** - Key code paths, function call chains
14. **⚙️ Implementation Mechanics** - Internal mechanisms and data flows
15. **🔍 Component Analysis** - Deep dive into critical components
16. **📐 Protocol & Interface Analysis** - API contracts and protocols
17. **🚀 Workflow Tracing** - End-to-end flow analysis
18. **🛡️ Security Analysis** - Security mechanisms and vulnerabilities
19. **⚡ Performance Analysis** - Performance bottlenecks and optimizations
20. **🧪 Testing Strategy Analysis** - Testing approaches and coverage

## Analysis Process

### Step 0: Preparation

0. **Duplicate Analysis Check** - Check if project has already been analyzed
   - Derive `project-name` from project directory basename
   - Check if output directory exists: `~/ai/code-analysi/{project-name}/`
   - Check if project exists in `registry.ts` at `~/ai/code-analysi/site/src/lib/registry.ts`
   - If project already analyzed:
     - **Check if user is appending new content** (via `/czz-project-analyzer {text}` command)
       - If `{text}` is provided, treat as **append mode**
       - Derive new topic name from `{text}` or use incremental naming
       - Add new topic to existing analysis
       - Update main analysis file with new topic reference
       - Update registry.ts with new topic
       - Skip to Step 1-N for the new topic only
     - **If no append content** (standard analysis command):
       - **Ask user** what to do:
         1. **Skip** - Keep existing analysis, do not overwrite
         2. **View** - Show existing analysis summary
         3. **Append** - Add new topics to existing analysis
         4. **Re-analyze** - Overwrite existing analysis (requires explicit confirmation)
       - If user chooses "Skip" or "View", stop analysis and show existing results
       - If user chooses "Append", ask which topics to add
       - If user chooses "Re-analyze", get explicit confirmation before proceeding
   - Only proceed with full analysis if:
     - Project has NOT been analyzed before, OR
     - User explicitly confirms "Re-analyze"
1. **Initialize Heartbeat Detection** - Create memory-based progress tracking
   - Write analysis start status to OpenClaw memory: `memory/YYYY-MM-DD.md`
   - Record current project path, analysis mode, and start timestamp
   - This prevents analysis interruption and enables resume capability
2. **Read the template** from `~/.agents/skills/czz-project-analyzer/TEMPLATE.md`
3. **Determine output directory**:
   - **Canonical output path**: `~/ai/code-analysi/{project-name}/`
   - `{project-name}` is derived from the project directory's basename (e.g. `kubernetes`, `tokio`, `zinx`)
   - If the user specifies a different output location, use that instead
   - Create `topics/` subdirectory for individual topic documents
   - Example: analyzing `/Users/ccc/work/todo/kubernetes` → output at `~/ai/code-analysi/kubernetes/`
4. **Read current registry.ts** at `~/ai/code-analysi/site/src/lib/registry.ts`:
   - Find the highest `md_N` import number (e.g. if last is `md_299`, record `nextMdIndex = 300`)
   - Record this counter for use throughout the analysis — each new topic file gets the next `md_N`
5. **Create TODO list** using the template from `CHANGELOG_TEMPLATE.md`
   - Create `analysis-todo.md` in the output directory
   - Initialize all topics with "Not Started" status
   - Set estimated times and priorities for each topic
6. **Gather project info** using:

**For Local Projects** (Primary):
- File system analysis: directory structure, file counts
- README analysis: local README files
- Code analysis: local source code examination
- Configuration files: package.json, go.mod, Cargo.toml, etc.
- Build scripts: Makefile, build.sh, etc.

**For Remote Projects** (Optional):
- GitHub API: `gh api repos/owner/repo`
- `gh repo view owner/repo --json description,stargazersCount,forksCount,primaryLanguage,licenseInfo`
- Web fetch for README and documentation
- Code structure exploration via `gh api` or `git clone`

### Step 1-N: Sequential Analysis (Progressive)

For **each of the 12 topics**:

1. **Update Heartbeat** - Write progress to OpenClaw memory
   - Update `memory/YYYY-MM-DD.md` with current topic and progress
   - This ensures analysis can resume if interrupted
2. **Report starting** to user
3. **Update analysis-todo.md** - Mark current topic as "In Progress"
4. **Analyze the topic** (collect info, create diagrams as needed)
5. **Create individual topic document** and save to `~/ai/code-analysi/{project-name}/topics/`
   - Format: `📄 Created: [file-path]`
6. **Update the main analysis file** with findings
7. **Update changelog.md** with document creation record
8. **Update registry.ts** — add this topic to the docs site registry:
   - File: `~/ai/code-analysi/site/src/lib/registry.ts`
   - Add a new `import md_N from '../../../{project-name}/topics/{filename}.md?raw'` at the end of the import block
   - `md_N` uses the counter from Step 0 (increment after each use)
   - If this is the **first topic** of a new project, also add a new project object to the `projects` array with an initial `topics: [...]` containing just this one topic
   - If the project entry **already exists** in the array, just append the new topic to its `topics: [...]` array
   - **Category**: `NN-*.md` → `'core'`, `deep-dive-*.md` → `'deep-dive'`, everything else → `'other'`
   - **Order**: use the `md_N` number
   - **Slug**: filename without `.md`, must be unique within the project
   - Write the updated file immediately
   - Format: `📋 Updated: registry.ts (added md_N → {topic-slug})`
9. **Update analysis-todo.md** - Mark current topic as "Completed"
10. **Update Heartbeat** - Write completion to memory
11. **Report completion** and automatically continue to next topic
11. **Automatically proceed** to next topic immediately (no user confirmation needed)

**Important**:
1. Always report when STARTING each topic analysis
2. Provide immediate file creation feedback
3. Report completion summary
4. Then automatically continue to the next topic without waiting for user confirmation

### Final Step: Complete & Host

After finishing all 12 topics (registry.ts has been updated incrementally in each step):

1. **Update Heartbeat** - Mark analysis as complete in memory
   - Write completion status to `memory/YYYY-MM-DD.md`
   - Clear active analysis flag to prevent resume attempts
2. **Present summary** with key insights
3. **Show file location**: `~/ai/code-analysi/{project-name}/`
   - Example: `~/ai/code-analysi/kubernetes/`
4. **Rebuild the docs site**:
   ```bash
   cd ~/ai/code-analysi/site && bun run build
   ```
   If the site does not exist yet, invoke `/docs-site ~/ai/code-analysi --multi` first.
5. **Report**: site URL, new project pages, total topic count
6. **Offer follow-up** (e.g., "Want me to dive deeper into any specific area?")

## Information Gathering Strategy

### For Local Projects (Primary)

**For Basic Info (Topic 1)**:
```bash
# Directory analysis
ls -la [project-path]
find [project-path] -type f | wc -l
find [project-path] -name "README*" -o -name "readme*"

# Language detection
find [project-path] -name "*.go" | wc -l
find [project-path] -name "*.js" | wc -l
find [project-path] -name "*.py" | wc -l

# Configuration files
ls [project-path]/*.json [project-path]/*.mod [project-path]/*.toml
```

**For Project Structure (Topic 2)**:
```bash
# Directory tree
tree -L 3 [project-path]  # or: find [project-path] -type d | head -20

# File statistics
find [project-path] -type f -name "*.go" | head -10
find [project-path] -type f -name "*.md" | head -10

# Key directories
ls -la [project-path]/cmd/
ls -la [project-path]/pkg/
ls -la [project-path]/src/
```

**For Tech Stack (Topic 3)**:
```bash
# Check for dependency files
cat [project-path]/package.json
cat [project-path]/go.mod
cat [project-path]/requirements.txt
cat [project-path]/Cargo.toml

# Build tools
ls [project-path]/Makefile
ls [project-path]/build.sh
cat [project-path]/.github/workflows/*.yml
```

**For Activity (Topic 8)**:
```bash
# Git history (if available)
cd [project-path] && git log --oneline -10
git log --since="1 month ago" --oneline | wc -l
git log --since="1 year ago" --pretty=format:"%h %ad" --date=short | head -10
```

### For Remote Projects (Optional)

**For Basic Info (Topic 1)**:
```bash
gh api repos/owner/repo
```

**For Project Structure (Topic 2)**:
```bash
gh api repos/owner/repo/git/trees/main?recursive=1
```

**For Tech Stack (Topic 3)**:
```bash
# Common dependency files
gh api repos/owner/repo/contents/package.json
gh api repos/owner/repo/requirements.txt
gh api repos/owner/repo/Cargo.toml
gh api repos/owner/repo/go.mod
```

**For Activity (Topic 8)**:
```bash
gh api repos/owner/repo/issues?state=open&per_page=10
gh api repos/owner/repo/pulls?state=open&per_page=10
gh api repos/owner/repo/stats/commit_activity
```

## Mermaid Diagram Guidelines

### Use these diagrams based on project type:

| Topic | Diagram Types | When to Use |
|-------|--------------|-------------|
| Project Structure | Module graph | Always - show dependencies |
| Tech Stack | Dependency graph | Always - show stack layers |
| Core Features | Sequence diagram | When user flows are clear |
| Architecture Design | Architecture flowchart | Always - show layers |
| Architecture Design | Data flow diagram | When data flow is complex |
| Summary | State diagram | For FSM/state-based projects |
| Summary | ER diagram | For database-heavy projects |
| Summary | Git graph | For projects with interesting branching |

### Example Module Graph:
```mermaid
graph LR
    A[Core Module] --> B[Utils]
    A --> C[Config]
    D[API] --> A
    E[Tests] --> A
```

### Example Sequence Diagram:
```mermaid
sequenceDiagram
    User->>Frontend: Action
    Frontend->>Backend: API Call
    Backend->>DB: Query
    DB-->>Backend: Data
    Backend-->>Frontend: Response
    Frontend-->>User: Result
```

### 📚 Complete Mermaid Examples Reference

For comprehensive examples of all diagram types with proper syntax, reference:
`~/.agents/skills/czz-project-analyzer/demo-mermaid.md`

This file contains 2 examples for each of 15 diagram types, all following the mandatory syntax rules below.

**When creating any mermaid diagram during analysis:**
1. Consult `demo-mermaid.md` for the correct diagram type and structure
2. Copy the relevant example as a template
3. Adapt the content to match the project being analyzed
4. Verify all syntax rules are followed (see below)

### Mermaid Syntax Rules (MANDATORY)

Every mermaid block generated during analysis MUST follow these rules. Violations cause parse errors.

**Bracket Matching** — opening and closing brackets for node shapes MUST match:
| Opening | Closing | Shape | Example |
|---------|---------|-------|---------|
| `[` | `]` | Rectangle | `A[Label]` |
| `{` | `}` | Diamond | `D{Decision}` |
| `(` | `)` | Rounded | `R(Label)` |
| `([` | `])` | Stadium | `S([Start])` |
| `[[` | `]]` | Subroutine | `X[[Process]]` |
| `[(` | `)]` | Cylinder | `DB[(Database)]` |

**NEVER** mix: `{Decision]` or `[Choice}` are syntax errors.

**Reserved keywords** (case-insensitive) — never use as node/participant IDs:
`loop`, `end`, `alt`, `opt`, `par`, `critical`, `break`

Use a suffix: `LoopNode`, `EndState`, `AltPath`.

**Comment syntax**: use `%%` only. `#` causes parse error.

**Subgraph labels**: always quote labels containing spaces or special characters:
```
subgraph "Frontend Layer"   %% correct
    A[UI]
end
```

**ALL node labels MUST use double quotes** — always wrap in `["..."]`, even for plain text:
```
A["User: Analyze project"]          %% correct — safe from `:` parsing
B["SKILL.md: Step 0 Preparation"]   %% correct — safe from `.` `:` parsing
C["Read TEMPLATE.md"]               %% correct — consistent style
```
NEVER use bare brackets: `A[Label text]` is fragile — always use `A["Label text"]`.

**Node labels with special characters** — these are the most common breakage cases:
- Contains `@`: `ID["@ notification"]`
- Contains `[]`: `ID["items[0]"]`
- Contains `:` + `/`: `ID["CIDR: 10.0.0.0/16"]`
- Contains `/` (path-like): `ID["openclaw/plugin-sdk"]` — paths with slashes must use square bracket wrapping with quotes
- Contains `<br/>` + `()`: `ID["Process<br/>(async)"]`
- Contains `{}`: `ID["Create ~/path/{project-name}/ dir"]` — `{}` is parsed as DIAMOND_START/END
- **Contains `()` inside `[]`**: `ID["HTTP API (/admin, /api)"]` — parentheses inside brackets MUST be quoted; bare `ID[Label (text)]` causes parse errors

**Decision/condition node labels** — use `{condition?}` without quotes around the whole label:
```
DecisionNode{condition?}              %% correct — condition inside diamond
DecisionNode{"condition?"}            %% WRONG — quotes force literal {}, then inner {} conflicts
```
When you write `{"condition?"}`, Mermaid parses the outer `"..."` as a label string, but the inner `{}` is still evaluated as a hexagon shape, causing rendering errors. Always use unquoted `{condition?}` for decision nodes.

**Node IDs must not contain spaces** — the ID (before the brackets) is a single token:
```
AIProviders["LLM APIs"]     %% correct — no space in ID
AI Providers["LLM APIs"]    %% WRONG — space causes parse error
```
Use camelCase or underscores: `MyNode`, `ai_providers`.

**Edge labels MUST be enclosed in `|"..."|` with both a source and target node**:
```
A -->|"label text"| B          %% correct — closed pipes + target
A -->|"label text"              %% WRONG — missing closing | and target node
```
Every `-->|"..."|` must have a matching `|` followed by a destination node on the same line.

**sequenceDiagram rules**:

**Participant references must match declared IDs exactly** — declared aliases are only for display; messages must use the short ID:
```
participant G as Gateway       %% declared ID is G, display alias is Gateway
CH->>G: Route request          %% correct — uses G
CH->>Gateway: Route request    %% WRONG — "Gateway" is not a declared ID
```

**Message syntax requires a colon** — `Source->>Target: text` is mandatory; never omit the `: text` portion:
```
A->>T: Tool result             %% correct — colon + message text
A->>Tool Result                %% WRONG — no colon, "Tool Result" parsed as node string
```
- `alt`/`else`/`end` blocks only — never `alt cond1|cond2| target`
- `style` directive does NOT work in sequenceDiagram — never use it there
- `Note over A,B: text` is valid only in sequenceDiagram

**flowchart/graph rules**:
- `style` directive works ONLY in graph/flowchart — never in sequenceDiagram or stateDiagram
- Keep style directives simple: `style A fill:#bbf,stroke:#333` (omit `stroke-width`)
- **Direction choice** — avoid `LR` for long linear chains (8+ sequential nodes); use `TD` instead:
  ```
  flowchart TD    %% correct — vertical layout for long chains
  flowchart LR    %% WRONG for 8+ nodes — crushed horizontally, text unreadable
  ```
  `LR` is fine for short fan-out diagrams (≤7 nodes in longest chain).

- **Subgraph labels must not share a name with any child node ID** — causes "Setting X as parent of X would create a cycle":
  ```
  subgraph "Dedupe"                    %% WRONG — subgraph name = node ID
      Dedupe["Dedupe Cache"]
  end

  subgraph "Dedupe"                    %% correct — different ID
      DedupeCache["Dedupe Cache"]
  end
  ```

**Avoid fragile diagram types**:
- `gitGraph` — unreliable rendering; use `graph LR` flowchart instead
- Nested subgraphs with empty labels — always give meaningful labels
- `stateDiagram` with complex transitions — keep simple

**Self-check before saving**: after writing any mermaid block, verify:
1. Every opening bracket has a matching closing bracket of the same type
2. No reserved keyword used as node/participant ID
3. No `style` in sequenceDiagram or stateDiagram
4. All subgraph labels quoted if they contain spaces
5. No `#` comments (use `%%`)
6. Labels containing `{}``[]` `()` must be wrapped in double quotes
7. No spaces in node IDs — use camelCase or underscores
8. Every `-->|"label"|` has closing `|` and a target node
9. sequenceDiagram messages use declared participant IDs (not display aliases)
10. Every `->>` / `-->>` message has a colon and text after the target
11. Long linear chains (8+ nodes) use `TD` direction, not `LR`
12. **Decision nodes use `{condition?}` without outer quotes** — never `{"condition?"}` which causes inner `{}` to be parsed as hexagon shape

## Progress Reporting Format

Always report after completing each topic:

```
✅ [Topic Name] completed (progress X/12)

[2-3 bullet points of key findings]

[Optional: Show a small preview of the section content]

📁 Files created/updated:
• Created: [specific-file-path]
• Updated: [specific-file-path]
• Updated: changelog.md
• Updated: analysis-todo.md (progress X/12)

🔄 Continuing to next topic...
```

**CRITICAL**: Every topic completion MUST include explicit file operation feedback showing exactly which files were created and updated.

## Template and Guide Locations

- **Analysis template**: `~/.claude/skills/czz-project-analyzer/TEMPLATE.md`
- **Changelog template**: `~/.claude/skills/czz-project-analyzer/CHANGELOG_TEMPLATE.md`
- **Progressive workflow guide**: `~/.claude/skills/czz-project-analyzer/WORKFLOW.md`
- **Documentation guidelines**: `~/.claude/skills/czz-project-analyzer/DOCUMENTATION_GUIDELINES.md`
- **Path storage guide**: `~/.claude/skills/czz-project-analyzer/PATH_GUIDE.md`
- **Usage examples**: `~/.claude/skills/czz-project-analyzer/EXAMPLE_WORKFLOW.md`
- **Mermaid diagram examples**: `~/.claude/skills/czz-project-analyzer/demo-mermaid.md` ⭐ **Reference for all diagram types**
- **Output directory**: `~/ai/code-analysi/{project-name}/` (centralized hub)
- **Output naming**: `{project-name}-analysis.md`

## Important: Document Location

**Analysis documents are ALWAYS saved to the centralized analysis hub at `~/ai/code-analysi/`:**
```
~/ai/code-analysi/
├── {project-name}/
│   ├── changelog.md
│   ├── {project-name}-analysis.md
│   ├── analysis-todo.md
│   ├── topics/
│   │   ├── 01-project-basic-info.md
│   │   ├── 02-project-structure.md
│   │   └── ...
│   └── assets/
├── {another-project}/
│   └── ...
└── site/                    ← docs-site skill scaffolds this
```

**Examples:**
- Analyzing `/Users/ccc/work/todo/kubernetes` → Documents saved in `~/ai/code-analysi/kubernetes/`
- Analyzing `/Users/ccc/work/my-project` → Documents saved in `~/ai/code-analysi/my-project/`
- Analyzing `.` (current directory named `zinx`) → Documents saved in `~/ai/code-analysi/zinx/`

**This centralized layout enables the `docs-site` skill to scaffold a multi-project hub** that hosts all analysis documents as a browsable web site.

## Example Response Pattern

### When Project Has Already Been Analyzed

**Standard command** (no append content):
When user says "Analyze /Users/ccc/work/todo/kubernetes" (but it was already analyzed):

```
⚠️ Project already analyzed!

Project: kubernetes
Output directory: ~/ai/code-analysi/kubernetes/
Analysis date: 2026-03-15
Topics completed: 12/12 + 8 deep-dive topics

What would you like to do?

1. 📖 View existing analysis
2. ✏️ Update specific topics
3. 📎 Append new topics
4. 🔄 Re-analyze (overwrite existing)
5. ❌ Cancel

Please choose (1-5):
```

If user chooses "View existing analysis":
```
📊 Kubernetes Analysis Summary

📍 Location: ~/ai/code-analysi/kubernetes/
📅 Analysis Date: 2026-03-15
📚 Topics: 12 core + 8 deep-dive

Key findings:
• [Brief summary of key insights...]

View full analysis:
• Main report: ~/ai/code-analysi/kubernetes/kubernetes-analysis.md
• Topics: ~/ai/code-analysi/kubernetes/topics/
• Online: [docs-site-url if available]
```

If user chooses "Re-analyze":
```
⚠️ Confirm re-analysis

This will OVERWRITE the existing analysis of kubernetes.

Existing analysis will be backed up to:
~/ai/code-analysi/kubernetes.backup.20260329/

Are you sure you want to proceed? (yes/no):
```

Only proceed with analysis if user explicitly confirms "yes".

### Append Mode (Adding New Topics to Existing Analysis)

When user says "/czz-project-analyzer model-loading-architecture" for an already-analyzed project:

```
📎 Append mode detected

Project: openclaw (already analyzed)
Existing analysis: ~/ai/code-analysi/openclaw/
Existing topics: 12 core + 8 deep-dive
New topic: Model Loading Architecture

🔵 Analyzing new topic: Model Loading Architecture

📋 Analysis scope: Model loading flow, provider runtime, LLM resolution
🎯 Focus areas: Model catalog, resolution engine, provider plugins

[... analysis in progress ...]

✅ Model Loading Architecture completed

📁 Files created/updated:
• Created: ~/ai/code-analysi/openclaw/topics/13-model-loading-architecture.md
• Updated: ~/ai/code-analysi/openclaw/openclaw-analysis.md
• Updated: ~/ai/code-analysi/site/src/lib/registry.ts (added md_320)

📊 Updated analysis summary:
• Total topics: 13 core + 8 deep-dive
• New topic added: Model Loading Architecture

Online: [docs-site-url]
```

**In append mode**:
- Do NOT create new output directory
- Do NOT overwrite existing main analysis file
- Add new topic document to `topics/` directory
- Append topic reference to main analysis file
- Update registry.ts with new `md_N` import
- Use incremental topic numbering (13, 14, etc.)

### When Project Has NOT Been Analyzed Before

When user says "Analyze /Users/ccc/work/todo/kubernetes":

```
Starting analysis of /Users/ccc/work/todo/kubernetes project...
Output directory: ~/ai/code-analysi/kubernetes/

🔵 Project Basic Info started (progress 1/12)
📋 Analysis scope: Project metadata, language statistics, file structure overview
🎯 Focus areas: Primary language, file counts, project path, README analysis
🔄 Starting analysis...

📋 Project Basic Info completed (progress 1/12)
- Main language: Go (95%+)
- Total files: 50,000+
- Project path: /Users/ccc/work/todo/kubernetes

📁 Files created/updated:
• Created: ~/ai/code-analysi/kubernetes/topics/01-project-basic-info.md
• Updated: ~/ai/code-analysi/kubernetes/kubernetes-analysis.md
• Updated: ~/ai/code-analysi/kubernetes/changelog.md
• Updated: ~/ai/code-analysi/kubernetes/analysis-todo.md (progress 1/12)

🔄 Continuing to next topic...
[... continues through all 12 topics ...]

✅ Analysis completed!
Analysis documents saved: ~/ai/code-analysi/kubernetes/

🔧 Updating registry...
• Added 12 imports to registry.ts (md_300–md_311)
• Added project entry: kubernetes (12 topics)

🔧 Rebuilding docs site...
[cd ~/ai/code-analysi/site && bun run build]

Would you like to dive deeper into any specific area?
```

## Important Notes

- **🚨 Check for existing analysis first** - Before starting any analysis, ALWAYS check if the project has already been analyzed. Ask user what to do if it has.
- **Never overwrite without explicit confirmation** - If project exists, get user's explicit consent before re-analyzing
- **Backup existing analysis** - When re-analyzing, create a backup of the existing analysis directory
- **Always complete all 12 topics** - don't stop early unless user says "stop"
- **🔵 Report STARTING each topic** - always inform user when beginning each topic analysis
- **Report after each topic** - immediately inform user when each topic is done
- **Continue automatically** - proceed to next topic without waiting for user confirmation
- **Create individual topic documents** - each topic gets its own markdown file
- **Save incrementally** - create and save each topic document immediately after analysis
- **Update main document** - consolidate all findings into the main analysis file
- **🎉 CRITICAL: File operation feedback** - ALWAYS report every file creation and update operation
- **Detailed file tracking** - distinguish between "Created" (new files) and "Updated" (modified files)
- **Use mermaid diagrams** where appropriate - they add significant value
- **Be specific** - avoid generic comments, provide concrete details
- **Cite sources** - mention where info came from (GitHub, docs, etc.)
- **Template-driven** - follow the template structure closely

## Analysis Behavior Guidelines

### When user requests analysis:
1. **Start immediately** - no confirmation or questions needed
2. **Complete topic by topic** - report after each topic completion
3. **Continue automatically** - automatically start next topic after reporting
4. **Complete fully** - finish all topics unless user says "stop"

### Reporting Format:
```
✅ [Topic Name] completed (progress X/12)

Key findings:
• Finding 1
• Finding 2
• Finding 3

📁 Files created/updated:
• Created: [topic-document-path]
• Updated: [main-analysis-file]
• Updated: changelog.md
• Updated: analysis-todo.md (progress X/12)

🔄 Continuing to next topic...
```

### User Experience:
- Users can see real-time progress
- **Clear feedback when STARTING each topic** - users know what's being analyzed next
- Clear feedback after each topic completion
- **Immediate file creation feedback** - users know exactly when files are created
- Detailed file operation tracking (created vs updated)
- No frequent interaction needed, analysis proceeds automatically
- Users can say "stop" at any time to interrupt the analysis
- Complete audit trail of all file operations

## Incremental Documentation Strategy

### File Organization

Each analysis generates multiple files under the centralized hub:

```
~/ai/code-analysi/
├── {project-name}/                      # One directory per analyzed project
│   ├── analysis-todo.md                 # Analysis TODO list (created in Step 0)
│   ├── changelog.md                     # Analysis changelog (updated throughout)
│   ├── {project-name}-analysis.md       # Main consolidated report
│   ├── topics/                          # Individual topic documents
│   │   ├── 01-project-basic-info.md
│   │   ├── 02-project-structure.md
│   │   ├── 03-tech-stack.md
│   │   ├── ...
│   │   └── 20-testing-strategy-analysis.md   # For deep-dive mode
│   └── assets/                          # Diagrams and images
│       ├── architecture-diagram.md
│       └── flowcharts/
├── {another-project}/
│   └── ...
└── site/                                ← docs-site scaffolds this
```

### Topic Document Template

Each individual topic document follows this structure:

```markdown
# [Topic Name] - [Project Name]

## 📋 Topic Overview
- **Analysis Topic**: [Topic Name]
- **Project**: [Project Name]
- **Analysis Time**: [Timestamp]
- **Analysis Status**: ✅ Completed

## 🔍 Analysis Content

[Detailed analysis content for this specific topic]

## 📊 Key Findings

- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

## 🔗 Related Resources

- Source location: [file:line]
- Reference docs: [links]
- Related topics: [links to other topic documents]

---

*This document was auto-generated by czz-project-analyzer skill*
*Generated at: [timestamp]*
```

## Deep Code Analysis Methodology (Advanced)

When conducting source code deep dives, follow this systematic approach:

### Analysis Principles
1. **From Architecture to Implementation**: Understand overall architecture first, then dive into code
2. **Flow-Driven**: Trace through actual workflows to understand code paths
3. **Visual + Code**: Combine Mermaid diagrams with code annotations
4. **Continuable**: Provide guides for continued analysis
5. **Practice-Oriented**: Include configuration examples and troubleshooting

### Code Analysis Structure
- **Resource Structure Details**: Source code locations, core type definitions, field explanations
- **Working Principles**: Architecture diagrams, key mechanisms, data flow processes
- **Source Code Deep Analysis**: Key code paths, function call chains, implementation details
- **Implementation Comparison**: Comparison of different implementations, pros/cons, use cases
- **Configuration and Practice**: Configuration examples, best practices, performance optimization
- **Monitoring and Observability**: Metrics, logging, monitoring solutions
- **Troubleshooting**: Common issues, troubleshooting steps, debugging commands

### Progressive Analysis Workflow
1. **Entry Point Analysis**: Identify main entry points (main functions, API endpoints)
2. **Data Structure Mapping**: Understand core data structures and their relationships
3. **Control Flow Tracing**: Follow execution paths through the codebase
4. **Dependency Analysis**: Map dependencies between modules and components
5. **Interface Analysis**: Understand API contracts and communication patterns
6. **State Management**: Analyze how state is managed and transitions occur
7. **Error Handling**: Review error handling and recovery mechanisms
8. **Extension Points**: Identify plugin systems, hooks, or extension mechanisms

## Analysis Triggers

### Standard Analysis Mode (12 steps)
Use when user asks for:
- "analyze [project]"
- "review [project]"
- "evaluate [project]"
- General project understanding

### Deep-Dive Mode (20 steps)
Use when user asks for:
- "deep dive into [project]"
- "source code analysis of [project]"
- "how does [project] work internally"
- "implementation details of [project]"
- Technical architecture evaluation
- Performance/security analysis requirements

### Quick Assessment Mode (6 steps)
Use when user asks for:
- "quick overview of [project]"
- "brief analysis of [project]"
- "should I use [project]"
- Basic project evaluation (steps 1,3,4,9,10,12 only)

## Related Skills and Resources

### Related Skills
- `docs-site` - For scaffolding the multi-project documentation hub at `~/ai/code-analysi/site/`
- `pretty-mermaid` - For advanced Mermaid diagram rendering
- `github` - For GitHub API access and repository data

### Supporting Documentation
- `WORKFLOW.md` - Progressive analysis methodology and deep-dive workflows
- `DOCUMENTATION_GUIDELINES.md` - File organization standards and naming conventions
- `PATH_GUIDE.md` - Path storage rules and best practices
- `EXAMPLE_WORKFLOW.md` - Complete usage examples with Kubernetes project
- `INTEGRATION_SUMMARY.md` - Kubernetes analysis methodology integration details