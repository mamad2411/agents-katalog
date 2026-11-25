# SuperClaude → OpenCode Framework

This configuration brings SuperClaude's specialized agent system to OpenCode with 20 agents and 28 commands.

## Agent Architecture

Agents are organized by domain and follow the principle of least privilege for tool access.

### Architecture & Design (read-only analysis)
- **backend-architect** — Backend systems, APIs, databases, security
- **frontend-architect** — UI/UX, accessibility (WCAG), Core Web Vitals
- **system-architect** — Scalable architecture, dependency management, patterns

### Security & Performance (analysis + investigation)
- **security-engineer** — Vulnerability assessment, OWASP, threat modeling, compliance
- **performance-engineer** — Measurement-driven optimization, benchmarking, profiling

### Research & Analysis (read + web access)
- **deep-research-agent** — Comprehensive research with adaptive strategies
- **deep-research** — External knowledge gathering with credibility assessment
- **root-cause-analyst** — Evidence-based problem investigation, hypothesis testing
- **requirements-analyst** — Requirements discovery, PRD creation, scope definition

### Development (full code access)
- **python-expert** — Production-ready Python with SOLID, TDD, security-first
- **refactoring-expert** — Code quality improvement, technical debt reduction
- **devops-architect** — CI/CD, IaC, observability, container orchestration

### Quality & Review
- **quality-engineer** — Testing strategies, edge cases, automation, coverage
- **self-review** — Post-implementation validation, checklist-style reports

### Education & Communication
- **learning-guide** — Progressive programming education with examples
- **socratic-mentor** — Socratic method for discovery-based learning
- **technical-writer** — Audience-targeted documentation

### Strategy & Project Management
- **business-panel-experts** — 9-expert strategy panel (Christensen, Porter, Drucker, etc.)
- **pm-agent** — PDCA workflow, memory integration, knowledge management
- **repo-index** — Repository indexing for token-efficient context

## Command Quick Reference

| Command | Description | Default Agent |
|---------|-------------|---------------|
| `/analyze` | Code quality/security/performance analysis | current |
| `/brainstorm` | Requirements discovery via Socratic dialogue | requirements-analyst |
| `/build` | Project compilation and packaging | devops-architect |
| `/business-panel` | Multi-expert business strategy analysis | business-panel-experts |
| `/cleanup` | Dead code removal, import optimization | refactoring-expert |
| `/design` | System/component architecture design | system-architect |
| `/document` | Documentation generation | technical-writer |
| `/estimate` | Time/effort/complexity estimation | current |
| `/explain` | Code and concept explanation | learning-guide |
| `/git` | Intelligent Git operations | current |
| `/help` | Command help and guidance | current |
| `/implement` | Code implementation from specs | python-expert |
| `/improve` | Code quality improvement | refactoring-expert |
| `/index-repo` | Repository indexing | repo-index |
| `/load` | Restore session context | pm-agent |
| `/pm` | Project management (PDCA) | pm-agent |
| `/recommend` | Technology recommendations | system-architect |
| `/reflect` | Post-implementation reflection | self-review |
| `/research` | Deep research with citations | deep-research-agent |
| `/save` | Save session state | pm-agent |
| `/select-tool` | Tool recommendations | current |
| `/spawn` | Spawn specialized subagent | current |
| `/spec-panel` | Technical specification review | current |
| `/task` | Task management and tracking | pm-agent |
| `/test` | Testing strategy and execution | quality-engineer |
| `/troubleshoot` | Problem investigation | root-cause-analyst |
| `/workflow` | Multi-step workflow orchestration | pm-agent |
| `/agent` | Agent management | current |

## Workflow Patterns

**New Feature**: `/brainstorm` → `/design` → `/implement` → `/test` → `/reflect`

**Bug Fix**: `/troubleshoot` → `/implement` → `/test` → `/reflect`

**Code Quality**: `/analyze` → `/improve` → `/cleanup` → `/test`

**Research**: `/research` → `/recommend` → `/design`

**Project Kickoff**: `/index-repo` → `/brainstorm` → `/estimate` → `/workflow`
