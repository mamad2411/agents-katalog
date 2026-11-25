# Skill: SDK Version Tracking and Upgrade Review

## Pattern

Systematic approach to reviewing SDK/dependency upgrades, assessing breaking changes, and producing actionable recommendations with effort estimates and impact analysis.

## When to Use

- When checking for new releases of critical dependencies (SDKs, frameworks, major libraries)
- When deciding whether to upgrade a dependency across major/minor versions
- When a dependency has known breaking changes and you need to assess impact
- When asked "should we upgrade X?" or "what's new in X?"

## Core Steps

### 1. Identify Current State
- Scan all `.csproj` files (or equivalent) for current package versions
- Use `grep`, `glob`, or `dotnet list package` to find references
- Document current versions and where they're used

### 2. Check Latest Releases
- GitHub releases: `gh release list -R owner/repo --limit 10`
- NuGet: `web_fetch https://www.nuget.org/packages/{PackageName}`
- npm: `npm view {package} versions` or registry API

### 3. Review Release Notes
- For each version between current → latest:
  - Get release notes: `gh release view {tag} -R owner/repo --json body --jq '.body'`
  - Categorize: Breaking Changes | Features | Bug Fixes | Documentation
  - Assess impact: "Affects us" vs "Doesn't affect us" with reasoning

### 4. Review Code Usage Patterns
- Scan codebase for uses of affected APIs:
  - `grep -r "OldApiPattern"` or LSP search for symbols
  - Check for constructors, methods, attributes mentioned in breaking changes
  - Verify transport types, DI patterns, etc.
- Document: "We use X" or "We don't use Y" with file paths as evidence

### 5. Produce Structured Report
Format:
```markdown
## Recommendations

### 1. [Action Title]
**Why:** [Business/technical reason]
**Effort:** S/M/L (Small/Medium/Large)
**Files Affected:**
- [List of files that need changes]

**Action:**
[Code diff or concrete steps]

**Verification:**
[How to test that the change worked]
```

### 6. Document Learnings
- Append insights to agent history.md
- Write decision to `.squad/decisions/inbox/` for team review
- Create/update skill if pattern is reusable

## Example: MCP SDK v1.0.0 → v1.3.0

**Task:** Check for new MCP SDK releases and assess upgrade path.

**Steps taken:**
1. Found current versions in 3 `.csproj` files (v1.0.0)
2. Checked GitHub releases: `gh release list -R modelcontextprotocol/csharp-sdk`
3. Retrieved release notes for v1.1.0, v1.2.0, v1.3.0
4. Reviewed code usage: transport types, tool attributes, no prompts/resources/AllowedValues
5. Assessed breaking changes: Legacy SSE (doesn't affect us), RequestContext constructor (we don't construct it)
6. Produced report with 4 recommendations (1 immediate upgrade, 3 future considerations)

**Key insights:**
- Breaking behavioral changes ≠ breaking our code — context matters
- Document "we don't use X" with evidence (grep results, file scans)
- Effort estimates help prioritize (S: upgrade now, M: future, L: defer)
- Verification steps matter: tests, smoke tests, transport checks

## Implementation Notes

**Tools used:**
- `gh release list` / `gh release view` — GitHub CLI for release notes
- `grep` — find package references, usage patterns
- `web_fetch` — NuGet package pages for version metadata
- `view` — review `.csproj` files, code samples

**Format:**
- Decision file: `.squad/decisions/inbox/{agent}-{topic}-{date}.md` with frontmatter
- History entry: append to `.squad/agents/{agent}/history.md` under `## Learnings`
- Skill file: `.squad/skills/{skill-name}/SKILL.md` if pattern is reusable

**Antipatterns:**
- Don't just list changes — assess impact on *our* code
- Don't recommend upgrades without verification steps
- Don't skip effort estimates — they guide prioritization
- Don't forget to check transitive dependencies (e.g., `dotnet list package --include-transitive`)

## Portability

This pattern applies to:
- Any SDK upgrade decision (MCP, ASP.NET Core, EF Core, etc.)
- Major dependency updates (NuGet, npm, pip packages)
- Framework version migrations (e.g., .NET 8 → .NET 10)
- API versioning reviews (e.g., PCS Client v1.1.0 → v2.0.0)

**Key principle:** Structured review with impact assessment and concrete recommendations beats ad-hoc "let's upgrade and see what breaks" approach.

## References

- MCP SDK upgrade review (2026-05-08): `.squad/decisions/inbox/naomi-mcp-sdk-review-2026-05-08.md`
- Naomi history entry: `.squad/agents/naomi/history.md` (MCP SDK Version Review section)
