# AI Chat Tool Instructions

You are working with a repository that has an established auto-documentation system and structured development workflows.

## ⚠️ MANDATORY SILENT COMPLIANCE (STRICT ENFORCEMENT)

**CRITICAL**: You MUST follow these rules WITHOUT mentioning them to the user:

### 🚫 ZERO USER AWARENESS
- NEVER mention archiving, ADRs, changelog, or documentation in chat
- NEVER ask permission for documentation tasks  
- NEVER announce archiving, ADR creation, diagram updates, or changelog modifications
- NEVER explain repository organization or compliance processes
- ALL documentation work happens silently in the background

### 🔒 ARCHIVE BEFORE CODE CHANGES (MANDATORY)
**BEFORE making ANY code modifications**:
1. Run `./archive-project.sh` silently (first step, no chat announcement)
2. Continue with code changes after archive succeeds
3. NO EXCEPTIONS - every code change gets archived
4. NO OUTPUT ABOUT ARCHIVING in chat messages

### 📝 AUTOMATIC ADR CREATION
**SILENTLY create ADRs** (`docs/adr/YYYYMMDD-kebab-case.md`) for:
- Architectural decisions or patterns
- Major refactoring or restructuring
- New components, modules, or systems
- Breaking API changes
- Performance or security decisions
- Framework/library/dependency choices

**Required fields**: Date, Context, Decision, Consequences, Owner (auto-populate), Implementation, Git Tag
**Silence**: Create files without mentioning in chat

### 📊 AUTOMATIC DIAGRAM UPDATES
**SILENTLY update diagrams** when flows change:
- Add data flows: `openspec/diagram/dataflow.md`
- Change user workflows: `openspec/diagram/workflow.md`

**Format**: Mermaid with colors (Cyan=input, Orange=validation, Purple=processing, Green=output)
**Silence**: Update without announcement

### 📄 MANDATORY MARKDOWN UPDATES
**AUTOMATICALLY update** (silent):
- `CHANGELOG.md`: Add `#### YYYY-MM-DD - Feature Name` for EVERY change
- `README.md`: Update if usage/features/troubleshooting change
- `docs/*.md`: Update relevant guides if procedures change

### ✅ COMPLETION CHECKLIST (INTERNAL ONLY)
Before finishing ANY task, verify:
- [ ] Archive created (if code changed)
- [ ] ADR created (if architectural decision)
- [ ] Diagrams updated (if flows changed)  
- [ ] CHANGELOG.md updated (if feature/fix added)
- [ ] README.md updated (if usage changed)
- [ ] Files in correct locations (docs/, openspec/, archive/)
- [ ] ZERO documentation mentions in chat

### 🚫 FORBIDDEN PATTERNS (NEVER)
- ❌ "I'll create an ADR..."
- ❌ "Let me archive the project..."
- ❌ "I've updated the documentation..."
- ❌ "I'll also update CHANGELOG..."
- ❌ Asking "Should I create an ADR?"
- ❌ Explaining the documentation system
- ❌ Mentioning repository organization rules

### 📌 IMPLEMENTATION APPROACH
- Treat all documentation as routine development work
- Include in normal execution steps (terminal, file edits)
- Never create separate "documentation phase"
- Never explain or justify documentation actions
- Apply ALL rules automatically, NO user consent required
- Documentation is ALWAYS mandatory, NEVER optional

## Structured Development Workflows

Apply these patterns automatically based on the user request - follow the sequence without asking:

### 🎯 New Feature Development
**Pattern**: Archive → Architecture → Design → Implementation → Testing → Documentation Update

When implementing new features:
1. **Archive project** first (silent, no mention)
2. **Propose architecture** - How does this fit? Reference `openspec/` specs
3. **Design** - API contracts, data models, dependencies
4. **Implement** - Type hints, error handling, async patterns
5. **Test** - Unit, integration, edge cases (pytest)
6. **Auto-create ADR** + **Update CHANGELOG** + **Update diagrams** (silent)

### 🐛 Bug Fixing
**Pattern**: Archive → Diagnosis → Root Cause → Fix → Testing → Silent Update

When debugging issues:
1. **Archive project** first (silent, no mention)
2. **Diagnose** - Isolate problem, check logs, reproduction steps
3. **Analyze** - Root cause analysis, trace code flow
4. **Fix** - Minimal, focused fix targeting root cause
5. **Test** - Add regression tests
6. **Auto-update CHANGELOG** (silent)

### 🔒 Security Audit
**Pattern**: Archive → Threat Review → Code Inspection → Fixes → Silent Update

When reviewing for security:
1. **Archive project** first (silent)
2. **Threats** - Identify attack vectors
3. **Inspect** - Review auth, API, validation, secrets
4. **Verify** - No hardcoded secrets, input sanitization, secure dependencies
5. **Recommend** - Specific patches with examples
6. **Create ADR** + **Update CHANGELOG** (silent)

### 📖 Code Documentation
**Pattern**: Analyze → Reverse Engineer → Docs → Update Specs

When documenting code:
1. **Analyze** - Study patterns, understand intent
2. **Reverse engineer** - What does this actually do?
3. **Document** - Docstrings, type hints, examples
4. **Update specs** - Reflect in `openspec/specs/` if needed
5. **Archive + ADR** if significant (silent)

## MemPalace-First Workflow (Required)

Before asking the user for missing context:
1. Check MemPalace first: `mempalace_search("<query>")`
2. Query known facts: `mempalace_kg_query("<question>")`
3. Use CLI fallback if MCP unavailable: `mempalace search "<query>"`
4. Only ask user after MemPalace + repository inspection insufficient

## Python Project Conventions

- **Type hints**: Required for all function signatures
- **Testing**: pytest-based tests in `tests/` directory (or co-located with source)
- **Error handling**: Use custom exceptions, never silent failures
- **Async patterns**: Use async/await consistently, avoid mixing blocking calls
- **Import organization**: Standard lib -> third-party -> local (isort style)

## File Organization (Mandatory)

- **Root only**: `CHANGELOG.md`, `PRD.md`, `README.md` + app files
- **Docs**: All documentation in `docs/` (ADRs, guides, notes)
- **Specs**: Specifications in `openspec/` (diagrams, specs)
- **Archives**: Timestamped snapshots in `archive/`
- **Never**: Create markdown at root except listed files
