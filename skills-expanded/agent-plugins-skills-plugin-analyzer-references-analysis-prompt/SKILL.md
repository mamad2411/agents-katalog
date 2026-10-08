# Plugin Analysis Prompt

You are reviewing a plugin for a Claude Code / Copilot CLI plugin marketplace. Analyze every file provided below thoroughly and produce actionable findings.

## Analysis Categories

Evaluate the plugin across all of the following categories:

1. **Code Quality & Structure** — File organization, naming conventions, manifest correctness, adherence to plugin marketplace guidelines
2. **Edge Cases & Error Handling** — Missing guards, unhappy paths, failure modes not addressed
3. **Workflow Gaps & Ambiguities** — Steps that are unclear, underspecified, or could be interpreted multiple ways
4. **Documentation Quality** — README completeness, SKILL.md clarity, inline instructions, examples
5. **Scalability Concerns** — How well the plugin handles large inputs, many files, or complex scenarios
6. **User Experience** — Friction points, confusing prompts, missing feedback, unclear outputs
7. **Missing Features** — Capabilities that would meaningfully improve the plugin
8. **Placement & Architecture** — Where should this plugin live (standalone repo vs marketplace) and why; structural recommendations

## Output Format

Return your findings as a numbered list. For each finding:

```
### Finding <N>: <concise title>

- **Category:** <one of the 8 categories above>
- **Severity:** bug | enhancement | documentation
- **Affected files:** `<file path>` (lines ~X-Y)
- **Problem:** <detailed description of the issue>
- **Proposed fix:** <specific, actionable recommendation with code/text examples where helpful>
```

## Rules

- Be specific — cite file names and line numbers
- Be actionable — every finding must have a concrete proposed fix
- Do NOT flag style preferences or formatting opinions
- Do NOT suggest adding features unrelated to the plugin's stated purpose
- Focus on issues that would matter to a user or maintainer
- Minimum 5 findings, maximum 20
- Order findings by severity: bugs first, then enhancements, then documentation

## Plugin Files

The following files comprise the plugin being analyzed:

---

{PLUGIN_FILES}
