---
description: "CB - Parallel sub-agent codebase investigation, synthesized into one answer"
---

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

## Initial Setup:

When this command is invoked, respond with:
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

Then wait for the user's research query.

## Steps to follow after receiving the research query:

1. **Read any directly mentioned files first:**
   - If the user mentions specific files (tickets, docs, JSON), read them FULLY first
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files, READ A FILE IN FULL.
   - **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
   - This ensures you have full context before decomposing the research

2. **Scan the codebase for entry points (MANDATORY — use code-index MCP tools, NOT Grep/Glob):**
   - Start with `get_project_summary()` to understand overall project structure
   - Use `find_symbol(name)` to locate specific definitions (NOT Grep)
   - Use `find_usage(name)` to find all call sites and references (NOT Grep)
   - Use `search_symbols(query)` for fuzzy/semantic search by name or description
   - Use `get_file_outline(file_path)` to understand file structure (NOT Read on entire file)
   - Use `get_call_graph(name, depth)` to understand function relationships
   - Use `trace_data_flow(fn, var, direction)` when tracing how data flows through code
   - Use `find_implementations(name)` to find subclasses/interface implementations
   - Use `get_file_dependencies(file_path)` to understand import relationships
   - Use `find_unhandled_errors(language?, file?)` for error handling analysis
   - Use `analyze_coupling(file_or_module?)` for architecture quality assessment
   - Extract specific file paths and line numbers from matches
   - Note promising starting points: functions, classes, components
   - **Only use Grep/Glob for**: string literals, comments, config values, TODO markers, non-code files
   - **Time budget: <30 seconds** - this is a quick scan to target your agents

3. **Analyze and decompose the research question:**
   - Break down the user's query into composable research areas
   - Take time to ultrathink about the underlying patterns, connections, and architectural implications the user might be seeking
   - **Incorporate index findings:** Use file:line references from index scan to focus research
   - Identify specific components, patterns, or concepts to investigate
   - Create a research plan using TodoWrite to track all subtasks
   - Consider which directories, files, or architectural patterns are relevant

4. **Spawn parallel sub-agent tasks for comprehensive research:**
   - Create multiple Task agents to research different aspects concurrently
   - Agents are organized into two tiers: always-spawn and selectable.

   ### Always spawn (every research session):

   | Agent | Purpose |
   |-------|---------|
   | **project-context-analyzer** | Project goals, requirements, decisions — understand WHY the code exists |
   | **quality-risk-analyzer** | Security patterns, error handling, edge cases, test patterns in similar code |

   ### Selectable (orchestrator decides based on research question):

   | Agent | Spawn when the research question... |
   |-------|-------------------------------------|
   | **compliance-research** | Touches auth, data handling, APIs, sessions, logging, crypto, personal data, new dependencies, or deployment — anything with regulatory implications |
   | **codebase-analyzer** | Has specific code to trace (index hits with file:line references) |
   | **codebase-pattern-finder** | Needs examples of similar implementations to follow |
   | **library-analyzer** | May have relevant best practices, security rules, compliance rules, or documentation in `.claude/library/` |
   | **documentation-researcher** | Needs reference docs from .claude/library/documentation/ |
   | **web-researcher** | Needs current external docs, release notes, or best practices |

   If in doubt about **compliance-research**, include it — a "no applicable controls" result is cheap compared to discovering compliance gaps during PR review.

   ### Agent usage notes:

   **project-context-analyzer:**
   - Provides critical context about project goals, requirements, and current state
   - Helps understand WHY the code exists and what problems it solves

   **quality-risk-analyzer:**
   - Provide the feature description so it can identify relevant security areas
   - Reads security rules from `.claude/library/security_rules/` and finds quality patterns in the codebase

   **compliance-research:**
   - Provide the feature description so it can select relevant compliance rule files
   - Reads compliance rules from `.claude/library/compliance_rules/` and performs gap analysis against the codebase

   **codebase-analyzer (targeted, when you have index hits):**
   - Use with SPECIFIC file:line references from indexes
   - **Include relevant index excerpts directly in the agent prompt** — file paths, function signatures, and call relationships. This lets agents jump straight to reading source files instead of doing broad discovery searches.
   - Example prompt template:
     ```
     Research [topic]. The codebase index identified these relevant entry points:
     - `auth/service.py:45` - authenticate(username, password) -> bool — called by api/routes.py, middleware/auth.py
     - `auth/models.py:12` - class User — called by auth/service.py, tests/test_auth.py

     Start by reading these files and trace the implementation flow.
     ```

   **codebase-analyzer (exploratory):**
   - For broad exploration — it will use code-index MCP tools and fall back to Glob/Grep discovery
   - Use the **codebase-pattern-finder** agent if you need examples of similar implementations

   **Library documentation:**
   - Use the context7 MCP server (`mcp__context7__resolve-library-id` and `mcp__context7__query-docs`) to look up current documentation for any third-party library or framework
   - Useful when the research involves third-party package APIs, configuration, or usage patterns

   **library-analyzer:**
   - Discovers and analyzes reference documents in `.claude/library/` (best practices, security rules, compliance rules, documentation)
   - Locates relevant files, reads them, and extracts applicable guidance for the current task
   - Returns concrete rules, constraints, and implementation guidance — not just file paths

   **web-researcher:**
   - Use for external documentation and resources
   - Instruct it to return LINKS with findings, and INCLUDE those links in your final report

   ### General guidelines:
   - **When you have index hits:** Use targeted codebase-analyzer with specific file:line references
   - **For broader context:** Use exploratory locator/pattern-finder agents
   - The library-analyzer handles both discovery and analysis in a single pass
   - Run multiple agents in parallel when they're searching for different things
   - Each agent knows its job - just tell it what you're looking for
   - Don't write detailed prompts about HOW to search - the agents already know

5. **Wait for all sub-agents to complete and synthesize findings:**
   - IMPORTANT: Wait for ALL sub-agent tasks to complete before proceeding
   - Compile all sub-agent results using the following **priority order**:

   **Information Source Priority (highest to lowest):**
   1. **Project context** - Frames the why/what/goals (always start here)
   2. **Live codebase** - Primary source of truth about current implementation
   3. **Quality context** - Security rules, error handling patterns, edge cases from similar code
   4. **Best practices** - Architectural and engineering principles from `.claude/library/best_practices/`
   5. **Compliance context** - Applicable standards, required controls, gaps (from compliance-research)
   6. **Library documentation** (context7 MCP server) - External library/framework documentation
   7. **Web research** - General information (only when explicitly requested, lowest priority)

   **Synthesis Guidelines:**
   - When sources conflict, prefer higher-priority sources
   - Live codebase is authoritative for "what exists now"
   - Library documentation (via context7) is authoritative for "how libraries work"
   - Include the quality-risk-analyzer findings in the Quality Context section
   - Include the compliance-research findings in a Compliance Context section
   - Cite specific control IDs (ISO A.8.x, ASVS Vx.x.x, GDPR Art. x) in findings
   - If compliance-research wasn't spawned, omit the Compliance Context section
   - Highlight security rules that must be followed during implementation
   - Note error handling conventions the implementation must follow
   - Connect findings back to project goals and requirements
   - Connect findings across different components
   - Include specific file paths and line numbers for reference
   - Highlight patterns, connections, and architectural decisions
   - Answer the user's specific questions with concrete evidence

6. **Save research document:**
   - Run `.claude/helpers/get_metadata.sh` to collect metadata (date, git commit, branch, repo name, UUID, timestamp for filename)
   - Use the template at `.claude/templates/research.md`
   - Write the research document to `.claude/memories/YYYY-MM-DD-description.md` (add ticket number if relevant, e.g. `.claude/memories/YYYY-MM-DD-ENG-1478-description.md`). The content includes frontmatter and all research findings.
   - Fill in frontmatter using the metadata from `get_metadata.sh`
   - Fill in the Quality Context section with findings from the quality-risk-analyzer agent
   - Omit template sections that have no findings — don't include empty headings

7. **Present findings:**
   - Present a concise summary of findings to the user
   - Include key file references for easy navigation
   - Ask if they have follow-up questions or need clarification

8. **Handle follow-up questions:**
   - If the user has follow-up questions, append to the same research document
   - Update the frontmatter fields `last_updated` and `last_updated_by` to reflect the update
   - Add `last_updated_note: "Added follow-up research for [brief description]"` to frontmatter
   - Add a new section: `## Follow-up Research [timestamp]`
   - Spawn new sub-agents as needed for additional investigation
   - Continue updating the document

## API Testing Coverage

**If the project has an `api_tools/` directory AND the research involves API endpoints:**

1. Check `.claude/index/index_*_api_tools.md` for the URL → Bruno File Map, or use code-index MCP tools (`find_symbol`, `search_symbols`) to find API endpoint definitions
2. Cross-reference discovered endpoints against existing `.bru` files in `api_tools/`
3. Include an **API Test Coverage** section in the research document noting:
   - Endpoints that have Bruno requests
   - Endpoints missing Bruno requests
   - Existing `.bru` files that may need updating (changed URLs, body schemas, headers)

## Important notes:
- **Code-index-first approach:** Use code-index MCP tools in step 2 to identify specific file:line targets for your agents
- **Targeted agent prompts:** Use index findings to make agent prompts specific (e.g., "Start at auth/service.py:45") instead of broad searches
- **Always use project-context-analyzer first** to understand project goals and requirements
- Always use parallel Task agents to maximize efficiency and minimize context usage
- Always run fresh codebase research - never rely solely on existing research documents
- Prior research and project docs provide historical context to supplement live findings
- Focus on finding concrete file paths and line numbers for developer reference
- Research documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only operations
- Consider cross-component connections and architectural patterns
- Include temporal context (when the research was conducted)
- Link to GitHub when possible for permanent references
- Keep the main agent focused on synthesis, not deep file reading
- Encourage sub-agents to find examples and usage patterns, not just definitions
- Explore all of `.claude/library/` reference content when relevant
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks
- **Critical ordering**: Follow the numbered steps exactly
- ALWAYS read mentioned files first before spawning sub-tasks (step 1)
- ALWAYS wait for all sub-agents to complete before synthesizing (step 5)
- ALWAYS gather metadata before writing the document (step 6 before step 7)
- NEVER write the research document with placeholder value