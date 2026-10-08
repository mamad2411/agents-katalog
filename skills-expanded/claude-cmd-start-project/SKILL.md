---
allowed-tools: all
description: Execute project tasks in intelligent batches using artisan → validation → completion workflow
---

# /start-project ARGUMENTS$

Begin automated project execution using intelligent batch processing with artisan agents, validation agents, and automated task completion tracking.

## 🎯 Mission

Execute tasks from fr3k MCP database in optimal batches, using artisan → validation → (bugsy if needed) → completion workflow. Universal approach works for any project type: web apps, CLI tools, mobile apps, APIs, desktop software, scripts, etc.

## 📋 Arguments Integration

ARGUMENTS$ will be analyzed for:
- **Batch size preference**: Small (2-3 tasks), Medium (3-5 tasks), Large (5-8 tasks)
- **Risk tolerance**: Conservative (validate each task), Balanced (smart batching), Aggressive (larger batches)
- **Focus area**: Specific component or layer to work on first

## 🔄 Intelligent Batch Processing

### Phase 1: Task Analysis & Batch Intelligence

**Universal Batch Grouping Logic:**
1. **Get all incomplete tasks** from mcp__hey-fr3k__get_incomplete_tasks (includes todo, coding_done, needs_fixes, validated)
2. **Analyze task relationships** using universal criteria:
   - **File proximity**: Tasks touching same/related files
   - **Functional cohesion**: Tasks serving same feature/purpose
   - **Dependency chains**: Tasks that depend on each other
   - **Technology layer**: Tasks using same tools/languages/frameworks
   - **Complexity similarity**: Similar-sized tasks that make sense together

**Project-Agnostic Batch Rules:**
```
BATCH TOGETHER when tasks:
- Modify files in same directory/module
- Share common functionality or purpose
- Have sequential dependencies (A enables B)
- Use same technology/language/framework
- Are similar in scope and complexity

SEPARATE BATCHES when tasks:
- Touch completely different parts of codebase
- Use different technologies/languages
- Are independent with no relationship
- One is much larger/complex than others
- Cross major architectural boundaries
```

**Intelligent Batch Examples:**
- **CLI Tool**: Argument parsing + help system + config loading
- **Web API**: Database models + related API endpoints + validation
- **Mobile App**: Related UI screens + navigation + state management
- **Desktop App**: Menu system + preferences + keyboard shortcuts
- **Script/Tool**: Input processing + core logic + output formatting

### Phase 2: Batch Execution Workflow

**For each identified batch:**

1. **Batch Preparation**
   - Log batch contents and rationale
   - Estimate completion time and complexity
   - Identify any cross-batch dependencies

2. **Sequential Implementation within Batch**
   ```
   For each task in current batch:
   - Use mcp__hey-fr3k__get_task [ID] to get full requirements
   - Check task status and ALWAYS use specialized agent based on tech stack:
     * todo/needs_fixes → Spawn SPECIALIZED agent (NEVER artisan unless no specialist exists):
       
       LANGUAGE-SPECIFIC AGENTS (use these FIRST):
       - Go projects → **gopher** agent for all Go development tasks
       - JavaScript/Node.js → **jsmaster** agent for all JS/Node.js tasks  
       - Python projects → **thesnake** agent for all Python development tasks
       - TypeScript → **typegod** agent for all TypeScript tasks
       - React projects → **reactlord** agent for all React component tasks
       - Vue.js projects → **vuelord** agent for all Vue.js tasks
       - Next.js projects → **nextking** agent for all Next.js app tasks
       
       GENERAL AGENTS (use when no language specialist applies):
       - Mixed/Unknown language → **artisan** as LAST RESORT only
       
     * coding_done → Ready for validation
     * validated → Ready for completion
   - Wait for agent completion and status update
   - Move to next task in batch
   ```

3. **Batch Validation**
   ```
   After all batch tasks reach coding_done:
   - Spawn validation agent with entire batch context
   - Provide all task IDs for comprehensive validation
   - Validation sets tasks to validated/needs_fixes
   ```

4. **Fix Loop Handling**
   ```
   If validation marks tasks as needs_fixes:
   - Spawn bugsy agent for each needs_fixes task
   - Bugsy fixes issues and sets back to coding_done
   - Re-validate fixed tasks with validation agent
   - Continue loop until all tasks validated
   ```

5. **Batch Completion**
   ```
   When all batch tasks validated:
   - Use mcp__hey-fr3k__update_task_status to mark each task complete
   - Log batch completion and lessons learned
   - Store any patterns or issues for future batches
   ```

### Phase 3: Progress Management & Optimization

**Continuous Intelligence:**
- **Learn batch patterns**: Track which groupings work well
- **Adapt batch sizes**: Smaller batches if validation failures increase
- **Optimize sequences**: Prefer batches that unblock other work
- **Risk assessment**: Flag complex batches for extra attention

**Progress Tracking:**
- **Batch completion rate** and time estimates
- **Validation success rate** per batch type
- **Overall project progress** toward completion
- **Bottleneck identification** and optimization opportunities

**Adaptive Batching:**
```
- If many tasks get needs_fixes → split into smaller batches next time
- If validation passes first try → consider larger batches next time  
- If fix loops are long → focus on single tasks for complex work
- If dependencies emerge → regroup remaining tasks accordingly
- If status transitions are smooth → batch similar complexity tasks
```

## 🔍 Universal Batch Intelligence Examples

**Any Project Type:**
```
Configuration Files Batch:
- Config parsing + validation + defaults + documentation

Core Logic Batch: 
- Main algorithm + helper functions + error handling + logging

User Interface Batch:
- Related UI components + styling + user interactions + feedback

Data Layer Batch:
- Data structures + persistence + validation + migrations

Integration Batch:
- External API calls + authentication + error handling + retry logic

Testing Batch:
- Test framework setup + unit tests + integration tests + test data

Documentation Batch:
- README + API docs + usage examples + changelog updates
```

## ⚠️ Safety & Quality Controls

**Mandatory Safeguards:**
- **Never skip validation**: Every batch gets validated before marking complete
- **Handle fix loops properly**: Bugsy → coding_done → validation → validated/needs_fixes
- **Maintain task integrity**: Each task's requirements fully satisfied
- **Preserve dependencies**: Don't break execution order from /new-project
- **Status isolation**: Individual task status failures don't affect batch

**Quality Assurance:**
- **Comprehensive validation**: Validator checks all batch files together
- **Fix loop completion**: Continue until all tasks reach validated status
- **Requirement compliance**: All original task requirements met
- **Status progression**: Proper todo → coding_done → validated → complete flow

## 🚀 Success Criteria

**Execution Excellence:**
- [ ] All incomplete tasks grouped into logical, intelligent batches
- [ ] Each batch follows proper status flow: todo → coding_done → validated → complete
- [ ] Task status transitions tracked accurately in fr3k MCP database
- [ ] Validation failures handled with bugsy → coding_done → re-validation loop
- [ ] Batch logic adapts to any project type and structure
- [ ] Progress clearly visible with status-based completion tracking

**Universal Applicability:**
- [ ] Works for web apps, CLI tools, mobile apps, APIs, scripts, any project type
- [ ] Batch grouping makes logical sense regardless of technology stack
- [ ] No hardcoded assumptions about project structure or patterns
- [ ] Adapts batch sizes and strategies based on project characteristics

This command transforms project execution from manual task-by-task work into intelligent, automated batch processing with quality assurance built-in.