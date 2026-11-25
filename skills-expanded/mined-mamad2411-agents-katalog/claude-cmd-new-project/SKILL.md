---
allowed-tools: all
description: Analyze fr3k_project.md and create optimally sequenced task database using senior developer principles
---

# /new-project ARGUMENTS$

Transform your project requirements into an intelligently sequenced task database using Google-level development practices.

## 🎯 Mission

Parse fr3k_project.md requirements and generate optimal task sequences that embody senior developer wisdom: understand deeply, design first, tackle risk early, build foundations, work outside-in with contracts, deliver incrementally.

## 📋 Arguments Integration

ARGUMENTS$ will be analyzed for:
- **Project type override**: If specified, use instead of inferring from fr3k_project.md
- **Priority focus**: Rush mode, quality focus, or balanced approach
- **Technology constraints**: Specific tech stack requirements or limitations

## 🔄 Phase-Based Execution

### Phase 1: Requirements Extraction

**Critical Analysis:**
1. **Read fr3k_project.md** - Extract ALL requirements, not just features
2. **Project structure extraction** - Extract custom structure recommendation from 📁 section
3. **Project type classification** - Web app, CLI, mobile, API, etc.
4. **Tech stack analysis** - Implications for task sequencing
5. **Risk identification** - What could kill this project?
6. **Dependency mapping** - Critical path and parallel opportunities
7. **User journey mapping** - Core paths vs nice-to-haves

**Success Criteria:**
- [ ] Complete understanding of project goals and constraints
- [ ] Custom project structure extracted and understood from fr3k_project.md
- [ ] Clear project type identification with sequencing implications
- [ ] Risk assessment with high-priority items identified (from fr3k_project.md constraints)
- [ ] Dependency graph mapped for optimal ordering

### Phase 2: Architecture & Task Design

**Senior Developer Principles Applied:**
- **Contracts first**: API contracts, DB schemas, interfaces before implementation
- **Risk early**: Tackle unknowns and complex integrations first
- **Foundation priority**: Core abstractions before features
- **Test inclusion**: Every task includes testing approach
- **Incremental delivery**: Each task produces working, testable software

**CLAUDE.md Integration:**
- **No Silent Fallbacks**: Tasks must fail loudly when primary approach doesn't work
- **Simple + Verified**: Generate simple, testable solutions first - avoid over-engineering
- **Read First**: Every task requires checking existing code before modifying
- **Test Everything**: All tasks must verify code actually runs
- **Fail Fast**: Stop and report when foundational approaches fail - no workarounds

**Task Creation Intelligence:**

**For Web Applications:**
```
1. Architecture design & risk assessment
2. Database schema + API contract design
3. Backend foundation + testing framework + mocks
4. Core business logic with comprehensive tests
5. Frontend foundation + component library + mock integration
6. API implementation (replace mocks progressively)
7. Feature implementation by dependency order
8. Integration, performance, security, deployment
```

**For CLI Tools:**
```
1. UX design & command structure definition
2. Argument parsing framework + testing setup
3. Core business logic with comprehensive test coverage
4. Output formatting & error handling
5. Edge case handling & integration testing
6. Distribution setup & documentation
```

**For Mobile Apps:**
```
1. User flow design & navigation architecture
2. Backend API contracts + mock server setup
3. Core UI foundation + design system
4. State management & navigation framework
5. Feature screens with mock data integration
6. Backend implementation & real data connection
7. Platform optimization & performance tuning
```

**For APIs/Backend Services:**
```
1. API design & contract specification
2. Database schema design + migration framework
3. Core service architecture + testing framework
4. Authentication & authorization implementation
5. Business logic with comprehensive testing
6. API endpoint implementation with validation
7. Performance optimization & security hardening
8. Documentation & deployment pipeline
```

### Phase 3: Intelligent Task Generation

**For each identified task:**
1. **Use mcp__hey-fr3k__add_task** with complete context and **scope: 'project'**:
   - **Task**: Clear, actionable description WITH AGENT ASSIGNMENT
   - **Requirements**: Specific acceptance criteria and technical requirements + REQUIRED SPECIALIZED AGENT
   - **Files**: Exact files to be created/modified (following extracted structure from fr3k_project.md)
   - **Expected results**: Concrete deliverables and success criteria
   - **Scope**: 'project' (for project initialization tasks)

**CRITICAL: ASSIGN SPECIALIZED AGENTS IN REQUIREMENTS:**
When creating tasks, ALWAYS specify in the requirements which specialized agent should handle implementation:
- **Go tasks** → "Implementation by **gopher** agent"
- **JavaScript/Node.js tasks** → "Implementation by **jsmaster** agent"
- **Python tasks** → "Implementation by **thesnake** agent"
- **TypeScript tasks** → "Implementation by **typegod** agent"
- **React tasks** → "Implementation by **reactlord** agent"
- **Vue.js tasks** → "Implementation by **vuelord** agent"
- **Next.js tasks** → "Implementation by **nextking** agent"
- **Mixed/Unknown** → "Implementation by **artisan** agent" (ONLY as last resort)

**Structure Implementation Priority:**
- **First task must be**: Create the recommended folder structure from fr3k_project.md
- **All subsequent tasks**: Place files according to the established structure
- **Structure reasoning**: Include rationale for file placement in task requirements

**Task Quality Standards:**
- **Atomic**: Can be completed and tested independently
- **Dependency-clear**: Obvious prerequisites and dependencies
- **Risk-aware**: High-risk tasks prioritized early in sequence
- **Test-inclusive**: Testing approach specified in requirements
- **Contract-driven**: Interfaces and schemas defined before implementation
- **No-fallback**: Each task has ONE primary approach - no backup solutions or workarounds
- **Simple-first**: Avoid over-engineered solutions - working code beats perfect architecture

**Smart Sequencing Logic:**
1. **Foundation tasks first**: Infrastructure, core abstractions, frameworks
2. **Risk mitigation early**: Unknown technologies, complex integrations
3. **Critical path priority**: Tasks that block other work
4. **Parallel opportunities**: Tasks that can run simultaneously
5. **Incremental delivery**: Each milestone produces working software

### Phase 4: Validation & Optimization

**Use validation agent to verify:**
1. **Completeness**: All fr3k_project.md requirements covered
2. **Structure compliance**: All tasks follow the custom structure from fr3k_project.md
3. **Sequencing logic**: Tasks in optimal dependency order
4. **Risk management**: High-risk items tackled early
5. **Quality standards**: Each task meets senior developer criteria
6. **Parallel opportunities**: Identify tasks suitable for concurrent execution

**Final Output:**
- Database populated with optimally sequenced tasks
- Custom project structure implementation as first priority task
- Clear parallel execution opportunities identified
- Risk mitigation built into early tasks
- Foundation-to-features progression established
- Testing and quality assurance integrated throughout

## ⚠️ Mandatory Requirements

**Never:**
- Create generic or templated task sequences
- Skip risk assessment or dependency analysis
- Generate tasks without clear acceptance criteria
- Sequence tasks randomly or by convenience

**Always:**
- Apply senior developer judgment to task ordering
- Include comprehensive testing in task requirements
- Use contracts and mocks for rapid feedback loops
- Prioritize foundation and risk mitigation
- Create atomic, independently testable tasks
- Validate that each task advances toward working software

## 🚀 Success Criteria

**Project Setup Excellence:**
- [ ] fr3k_project.md thoroughly analyzed and understood
- [ ] Project type correctly classified with appropriate patterns
- [ ] All tasks created with complete fr3k MCP metadata
- [ ] Optimal dependency ordering with parallel opportunities identified
- [ ] Risk mitigation built into early-phase tasks
- [ ] Each task includes testing approach and success criteria
- [ ] Foundation-to-features progression clearly established

**Quality Assurance:**
- [ ] validation agent confirms completeness and logic
- [ ] Task database ready for parallel validation workflow
- [ ] Project positioned for rapid, high-quality development
- [ ] Senior developer principles consistently applied throughout

This command transforms project planning from guesswork into systematic, intelligent task generation using proven senior developer methodologies.
