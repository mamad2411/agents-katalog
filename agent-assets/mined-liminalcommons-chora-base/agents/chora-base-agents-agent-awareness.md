# AGENTS.md - Agent Awareness (SAP-009)

**Domain**: Agent Awareness & Discovery
**SAP**: SAP-009 (agent-awareness)
**Version**: 1.1.0
**Last Updated**: 2025-10-31

---

## 📖 Quick Reference

**New to SAP-009?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 5-minute guide to nested AGENTS.md/CLAUDE.md pattern with examples
- 📚 **Time Savings** - 60-70% token reduction through progressive loading and domain-specific awareness files
- 🎯 **5-Level Hierarchy** - Root → domain → SAP → feature → component navigation with "nearest file wins"
- 🔧 **Progressive Loading** - Three phases (0-10k, 10-50k, 50-200k tokens) optimize context usage
- 📊 **Universal Adoption** - 100% of 32+ SAPs use this pattern for agent discoverability
- 🔗 **Integration** - Works with all SAPs (universal foundation for agent awareness)

This AGENTS.md provides: Agent-specific patterns for nested awareness navigation, progressive loading workflows, and "nearest file wins" discovery.

---

## Overview

This is the domain-specific AGENTS.md file for agent awareness (SAP-009). It provides context for agents working with the AGENTS.md pattern, bidirectional translation layer, and agent discovery mechanisms.

**Parent**: See [/AGENTS.md](/AGENTS.md) for project-level context

**Pattern**: "Nearest File Wins" - This file provides agent-awareness-specific context

---

## User Signal Patterns

### Agent Discovery Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "how do I use this repo" | discover_agents_md() | Read /AGENTS.md | Start with root context |
| "what tools are available" | list_foundation_tools() | Read /AGENTS.md lines 732-944 | Bidirectional translation tools |
| "show me the agent docs" | open_agents_md() | Read /AGENTS.md or domain AGENTS.md | Context discovery |
| "what can agents do here" | discover_capabilities() | Read SAP Index, AGENTS.md | List available SAPs |
| "help me get started" | onboarding_workflow() | Read docs/user-docs/how-to/quickstart-*.md | Role-based onboarding |
| "explain the AGENTS.md pattern" | explain_agents_pattern() | Read SAP-009 awareness-guide.md | How-to documentation |

### AGENTS.md Maintenance

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "update AGENTS.md" | edit_agents_md() | Edit /AGENTS.md or domain file | Add new context |
| "add tool to AGENTS.md" | add_tool_discovery() | Edit /AGENTS.md section 6 | Foundation tools section |
| "create domain AGENTS.md" | create_domain_agents() | Write docs/skilled-awareness/SAP/AGENTS.md | Domain-specific context |
| "validate AGENTS.md" | validate_agents_structure() | Check sections 1-7 present | Quality gate |

### Bidirectional Translation Operations

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "translate user input" | route_intent(text) | python scripts/intent-router.py TEXT | Natural language → formal actions |
| "what does 'show inbox' mean" | explain_intent(text) | intent-router.py + INTENT_PATTERNS.yaml | Show matching patterns |
| "search glossary for X" | search_glossary(term) | python scripts/chora-search.py TERM | Fuzzy term matching |
| "what should I do next" | suggest_next_actions() | python scripts/suggest-next.py | Context-aware suggestions |
| "add new intent pattern" | add_intent_pattern() | Edit INTENT_PATTERNS.yaml | Pattern learning |
| "update user preferences" | edit_user_preferences() | Edit .chora/user-preferences.yaml | Behavior adaptation |

### Progressive Formalization

| User Says | Formal Action | Tool/Command | Notes |
|-----------|---------------|--------------|-------|
| "casual mode" | set_formality(casual) | Update user-preferences.yaml: formality=casual | Conversational tone |
| "formal mode" | set_formality(formal) | Update user-preferences.yaml: formality=formal | Professional tone |
| "verbose output" | set_verbosity(verbose) | Update user-preferences.yaml: verbosity=verbose | Detailed explanations |
| "concise output" | set_verbosity(concise) | Update user-preferences.yaml: verbosity=concise | Brief responses |
| "teach me the system" | enable_progressive_learning() | Update user-preferences.yaml: learning_mode=true | Gradual formalization |

### Common Variations

**Discovery Queries**:
- "how do I use this" / "getting started" / "what's available" → discover_agents_md()
- "show tools" / "list capabilities" / "what can I do" → list_foundation_tools()

**Translation Queries**:
- "translate" / "route" / "interpret" → route_intent()
- "search" / "lookup" / "find term" → search_glossary()
- "suggest" / "what next" / "recommend" → suggest_next_actions()

**Maintenance Queries**:
- "update docs" / "add to AGENTS.md" / "enhance context" → edit_agents_md()
- "new pattern" / "add intent" / "teach new command" → add_intent_pattern()

---

## Agent Awareness Quick Reference

### AGENTS.md Pattern (SAP-009 v1.0.0)

**Dual-File Pattern**:
- **AGENTS.md**: Generic agent context (Claude Code, Cursor, Windsurf, etc.)
- **CLAUDE.md**: Claude Code-specific context (auto-loaded)

**Nearest File Wins**:
```
/AGENTS.md                                    # Root context (Layer 1)
/docs/skilled-awareness/inbox/AGENTS.md       # Domain context (Layer 2)
/docs/dev-docs/patterns/INTENT_PATTERNS.yaml  # Pattern database (Layer 3)
```

**Progressive Context Loading**:
- Agent starts at root AGENTS.md (Layer 1)
- Discovers domain-specific AGENTS.md via "Nearest File Wins" (Layer 2)
- Loads full pattern database if needed (Layer 3)
- Token budget: Layer 1 (~10k) + Layer 2 (~5k) + Layer 3 (~20k) = 15-35k

### Bidirectional Translation Layer (SAP-009 v1.1.0)

**Core Capabilities**:

1. **Intent Routing**: Natural language → Formal actions
   - Confidence thresholds: ≥0.70 execute, 0.50-0.70 clarify, <0.50 alternatives
   - Fuzzy matching for typos (edit distance ≤2)
   - Parameter extraction from natural language
   - Tool: `scripts/intent-router.py`

2. **Glossary Search**: Term discovery with fuzzy matching
   - Exact match: 1.0 score
   - Contains match: 0.8 score
   - Fuzzy match: 0.4-0.7 score (Levenshtein distance)
   - Related terms via category/SAP
   - Tool: `scripts/chora-search.py`

3. **Context-Aware Suggestions**: Project state → Next actions
   - Reactive mode: Top 5 suggestions
   - Proactive mode: High priority only
   - Context sources: inbox status, coverage, broken links, blockers
   - Tool: `scripts/suggest-next.py`

4. **User Preferences**: Behavior adaptation
   - 100+ configuration options
   - 4 categories: communication, workflow, learning, expertise
   - Progressive disclosure support
   - Config: `.chora/user-preferences.yaml`

**Foundation Tools**:

```bash
# Intent routing
python scripts/intent-router.py "show inbox"
# Output: [{"action": "run_inbox_status", "confidence": 0.95, ...}]

# Glossary search
python scripts/chora-search.py "Coordination Request"
# Output: [{"term": "Coordination Request", "score": 1.0, ...}]

# Context-aware suggestions
python scripts/suggest-next.py --mode reactive
# Output: [{"suggestion": "Review 3 pending coordination requests", ...}]
```

**Integration Pattern** (Generic Agents):

```python
# Layer 1: Discover tools via root AGENTS.md
import subprocess
import json

def route_intent(user_input: str) -> list:
    """Route natural language to formal actions."""
    result = subprocess.run(
        ['python', 'scripts/intent-router.py', user_input],
        capture_output=True,
        text=True,
        cwd='/path/to/chora-base'
    )
    return json.loads(result.stdout)

# Layer 2: Load domain context if needed
def load_domain_context(sap_id: str) -> str:
    """Load domain-specific AGENTS.md file."""
    path = f'docs/skilled-awareness/{sap_id}/AGENTS.md'
    with open(path) as f:
        return f.read()

# Layer 3: Load full pattern database if needed
def load_intent_patterns() -> dict:
    """Load full INTENT_PATTERNS.yaml."""
    import yaml
    with open('docs/dev-docs/patterns/INTENT_PATTERNS.yaml') as f:
        return yaml.safe_load(f)
```

### Progressive Formalization Stages

**Stage 1: Casual (Week 1)**
- User: "what's in the inbox?"
- Agent: Translates to `run_inbox_status`, executes, explains result
- Learning: Agent teaches "inbox" is a formal concept

**Stage 2: Semi-Formal (Weeks 2-4)**
- User: "check inbox status"
- Agent: Recognizes semi-formal language, executes directly
- Learning: User adopts systemic terminology

**Stage 3: Formal (Month 2+)**
- User: "run inbox status"
- Agent: Executes immediately, minimal explanation
- Learning: User speaks the system's language

**Stage 4: Executable (Month 3+)**
- User: "python scripts/inbox-status.py"
- Agent: Direct execution, no translation needed
- Learning: User fully onboarded to systemic ontology

### Quality Gates

**Before Commit** (Agent Awareness Changes):
- [ ] Root AGENTS.md has sections 1-7
- [ ] Domain AGENTS.md files follow template
- [ ] Tool discovery section up to date (section 6)
- [ ] Version history updated
- [ ] No broken links (validated via scripts/validate-links.sh)

**Before PR** (Bidirectional Translation):
- [ ] Intent recognition accuracy ≥80% on test query set
- [ ] User preferences successfully adapt behavior
- [ ] Graceful degradation if tools unavailable
- [ ] Documentation follows Diátaxis framework
- [ ] All BDD scenarios passing

**CI/CD** (Automated Validation):
- [ ] AGENTS.md structure validation
- [ ] Intent pattern syntax validation (YAML)
- [ ] Glossary structure validation (Markdown)
- [ ] User preferences schema validation
- [ ] Link validation across all AGENTS.md files

---

## Integration with Bidirectional Translation Layer

This domain AGENTS.md file integrates with the bidirectional translation layer (SAP-009 v1.1.0):

**Discovery Flow**:
1. User says "how do I use this repo" (casual, conversational)
2. Intent router loads root AGENTS.md (discovers intent-router.py exists)
3. Intent router loads THIS FILE (domain-specific patterns)
4. Matches "how do I use this repo" → `discover_agents_md` with high confidence
5. Agent reads /AGENTS.md and presents onboarding overview
6. Agent suggests next actions based on user role (developer, PM, external contributor)

**Context-Aware Suggestions**:
- If user is new, suggest reading quickstart guide for their role
- If AGENTS.md is outdated, suggest running validation script
- If new tools added, suggest updating tool discovery section
- Prioritizes agent awareness improvements based on recent questions

**Progressive Formalization**:
- Week 1: "what's available" → Agent explains AGENTS.md pattern
- Week 2-4: "show me the tools" → Agent lists foundation tools
- Month 2+: "list foundation tools" → Agent executes directly
- Month 3+: User navigates to /AGENTS.md independently

**See**: [/AGENTS.md lines 732-944](/AGENTS.md) for bidirectional translation layer overview

---

## Common Tasks

### Discover Available Tools

**Goal**: Find all foundation tools available in the repository

**Steps**:
1. Read root AGENTS.md, section 6 (Foundation Tools for Bidirectional Translation)
2. Validate tools exist: `ls scripts/intent-router.py scripts/chora-search.py scripts/suggest-next.py`
3. Check tool dependencies: `head -20 scripts/intent-router.py` (imports)
4. Test tool execution: `python scripts/intent-router.py "test query"`

**Expected Output**: List of 3 tools with descriptions and usage examples

### Add New Intent Pattern

**Goal**: Teach the system to recognize a new conversational input

**Steps**:
1. Identify user input that should be recognized (e.g., "archive completed work")
2. Define formal action (e.g., `archive_completed_coordination_requests`)
3. Edit INTENT_PATTERNS.yaml:
   ```yaml
   - pattern_id: archive_completed
     action: archive_completed_coordination_requests
     category: workflow
     triggers:
       - "archive completed"
       - "move finished work"
     parameters: []
     confidence_base: 0.85
   ```
4. Test new pattern: `python scripts/intent-router.py "archive completed work"`
5. Validate recognition: Check confidence ≥0.70

**Quality Gate**: New pattern doesn't break existing patterns (regression test)

### Update Domain AGENTS.md

**Goal**: Add domain-specific context to a SAP's AGENTS.md file

**Steps**:
1. Navigate to domain: `docs/skilled-awareness/{sap-id}/`
2. Check if AGENTS.md exists: `ls AGENTS.md`
3. If not, create from template (sections 1-7)
4. Add user signal patterns table (conversational → formal mappings)
5. Add domain quick reference (key concepts, files, commands)
6. Add integration section (how bidirectional translation applies)
7. Update version history
8. Validate links: `bash scripts/validate-links.sh`

**Expected Output**: Domain AGENTS.md with ≥3 user signal patterns

### Configure User Preferences

**Goal**: Adapt agent behavior to user preferences

**Steps**:
1. Copy template: `cp .chora/user-preferences.yaml.template .chora/user-preferences.yaml`
2. Edit preferences:
   ```yaml
   communication:
     verbosity: concise        # verbose|standard|concise
     formality: casual         # casual|standard|formal

   workflow:
     require_confirmation: destructive  # always|destructive|never
     progressive_disclosure: true       # Show summaries first

   learning:
     learning_mode: true       # Enable progressive formalization
     explain_translations: true # Show how translations work

   expertise:
     domain_knowledge: intermediate  # beginner|intermediate|expert
   ```
3. Validate syntax: `python -c "import yaml; yaml.safe_load(open('.chora/user-preferences.yaml'))"`
4. Test adaptation: Request an action, observe verbosity/formality

**Quality Gate**: Agent behavior reflects preferences (manual validation)

---

## Related SAPs

- **SAP-001** (inbox-protocol): Coordination request discovery via intent routing
- **SAP-004** (testing-framework): Test execution via intent routing
- **SAP-009** (agent-awareness): THIS SAP - AGENTS.md pattern and bidirectional translation
- **SAP-012** (development-lifecycle): Workflow operations via intent routing
- **SAP-013** (documentation-framework): Documentation search via glossary
- **SAP-019** (sap-self-evaluation): SAP quality validation via intent routing
- **SAP-031** (discoverability-based-enforcement): Uses SAP-009 nested awareness hierarchy for enforcement Layer 1 (discoverability)

---

## Enforcement Integration (SAP-031)

### Pattern: Enforcement via Discoverability

**Problem**: Having patterns in AGENTS.md isn't enough - agents need enforcement to consistently follow patterns.

**Solution**: SAP-031 (Discoverability-Based Enforcement) leverages SAP-009 nested awareness hierarchy for Layer 1 (discoverability - 70% prevention rate):

```
Session Start → Root AGENTS.md (enforcement reminder)
             ↓
Task Start → Domain AGENTS.md (patterns + template link)
           ↓
Implementation → Template file (patterns pre-implemented)
               ↓
Validation → Pre-commit hook (catch mistakes)
           ↓
CI/CD → Platform validation (catch edge cases)
      ↓
✅ 90%+ prevention rate (vs 20% documentation-only)
```

### Integration Architecture

**Root AGENTS.md** (Session start):
```markdown
## 🔴 [QUALITY DOMAIN] REMINDER

**ALL code MUST [quality requirement].**

Before [activity], read: **[domain AGENTS.md path]** for patterns.

**Quick Template**: Copy [template file path]
```

**Domain AGENTS.md** (Task start):
```markdown
## [Quality Domain] Patterns

**Quick Template**: [template file path]  ← Top of file for fast discovery

### Pattern 1: [Name]
[Description + example]

### Pattern 2: [Name]
[Description + example]
```

**Template File** (Implementation):
- All patterns pre-implemented (production-ready)
- Comments explain each pattern
- Easier to copy (90% correct) than write from scratch (50% correct)

### Agent Workflow with Enforcement

**Without SAP-031** (20% prevention):
1. Agent reads documentation
2. Agent writes code from memory
3. Agent forgets pattern
4. Violation discovered post-merge (expensive)

**With SAP-031** (90%+ prevention):
1. Session start → root AGENTS.md reminder
2. Navigate to domain AGENTS.md (1 click, <30 sec)
3. Copy template (patterns pre-implemented)
4. Customize business logic
5. Pre-commit hook catches mistakes (educational errors)
6. CI/CD validates on real platforms
7. ✅ Compliant code (99%+ confidence)

### Reference Implementation

**SAP-030** (cross-platform) uses SAP-031 enforcement:
- **Before**: 142 issues, 65/100 score
- **After**: 0 critical issues, 95/100 score, 99%+ prevention rate
- **ROI**: 4,000%+ (10h setup prevents 160h/year issues)

**Enforcement files**:
- Root: [AGENTS.md](../../../AGENTS.md) (cross-platform reminder)
- Domain: [scripts/AGENTS.md](../../../scripts/AGENTS.md) (5 patterns)
- Template: [templates/cross-platform/python-script-template.py](../../../templates/cross-platform/python-script-template.py)
- Validation: [scripts/validate-windows-compat.py](../../../scripts/validate-windows-compat.py)
- Fix: [scripts/fix-encoding-issues.py](../../../scripts/fix-encoding-issues.py)
- Hook: [.githooks/pre-commit-windows-compat](../../../.githooks/pre-commit-windows-compat)
- CI/CD: [.github/workflows/cross-platform-test.yml](../../../.github/workflows/cross-platform-test.yml)

### Key Insight

**"Discoverability is 70% of enforcement success."**

Making patterns easy to find (session start → task start → implementation) is more effective than post-hoc validation. SAP-009's nested awareness hierarchy provides the foundation for this discoverability layer.

**See SAP-031 for**:
- Complete 5-layer enforcement architecture
- Domain-agnostic pattern (security, accessibility, testing, etc.)
- Progressive enforcement strategy (warn → educate → block)
- Adoption blueprint (3 levels: Basic 2-4h, Advanced 1-2d, Mastery 1w)

---

**Version History**:
- **1.2.0** (2025-11-08): Added SAP-031 enforcement integration section
- **1.1.0** (2025-10-31): Added bidirectional translation layer integration, user signal patterns
- **1.0.0** (2025-10-29): Initial domain AGENTS.md for agent awareness (created during coord-002)

