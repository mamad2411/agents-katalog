---
name: dictation
description: Fix speech-to-text errors, correct technical terminology, and improve text clarity in documentation and workflows.
license: MIT
---
# Skill: dictation

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Apply dictation correction protocols to fix common speech-to-text errors, especially technical terms from the project glossary.

## Core Process

1. **Identify**: Scan the input text for common speech-to-text misrecognitions, filler words, and unclear phrasing.
2. **Correct**: Apply project-specific technical term corrections, hyphenation rules, and engine name formatting.
3. **Refine**: Remove filler words, improve conciseness, and ensure technical accuracy without modifying code/examples.

## Core Principles

- **Glossary Compliance**: Strict adherence to the project technical glossary.
- **Accurate Hyphenation**: Ensure correct hyphenation for compound modifiers (e.g., `pull-request`, `cache-memory`).
- **Engine Capitalization**: Proper spelling and casing for AI engines (e.g., GitHub Copilot, Claude, Gemini).
- **No Code Generation**: Do not generate code examples or output step-by-step planning to the user. You may follow the Core Process internally, but the response should primarily be the corrected text.
- **Maintain Intent**: Do not simplify technical concepts or alter the user's intended meaning.

## WHEN TO USE

- When processing raw dictation or speech-to-text input.
- When refining draft documentation or workflow descriptions that contain filler words or inaccuracies.

## WHEN NOT TO USE

- For refactoring actual source code, where technical syntax must remain untouched by NLP heuristics.
- When generating new content from scratch (use documentation generation skills instead).
- For translating text between distinct human languages.

## Common Pitfalls

- **Over-Correction**: Attempting to "fix" valid code snippets or shell commands that happen to contain words resembling dictation errors (e.g., changing a literal `"get actions"` variable name to `"GitHub Actions"`).
- **Losing Tone**: Stripping out conversational nuance entirely when editing a community-facing discussion, making it sound robotic.
- **Ignoring Project Context**: Applying global acronyms (like expanding `API`) when the project glossary specifically demands a different domain-specific expansion.

## Quick Start

```markdown
User: "The get actions work flow needs safe outputs for the cache memory"
Agent: Corrects to "The GitHub Actions workflow needs safe-outputs for the cache-memory"
```

## Vocabulary & Corrections

### GitHub and Git Terms

- "get hub" -> GitHub
- "git lab" -> GitLab
- "get actions" -> GitHub Actions
- "pull request" -> pull-request (as compound modifier)
- "issue ops" -> IssueOps
- "label ops" -> LabelOps
- "chat ops" -> ChatOps
- "multi repo ops" -> MultiRepoOps
- "project ops" -> ProjectOps
- "data ops" -> DataOps
- "dispatch ops" -> DispatchOps
- "daily ops" -> DailyOps

### Workflow Configuration

- "front matter" -> frontmatter
- "safe outputs" -> safe-outputs
- "safe inputs" -> safe-inputs
- "lock file" -> .lock.yml or lockfile
- "tool sets" -> toolsets
- "M.C.P." or "M C P" -> MCP
- "repo memory" -> repo-memory
- "cache memory" -> cache-memory
- "work flow" -> workflow
- "timeout minutes" -> timeout-minutes
- "runs on" -> runs-on
- "min integrity" -> min-integrity
- "mcp gateway" -> mcp-gateway
- "mcp scripts" -> mcp-scripts
- "staged mode" -> staged-mode
- "token weights" -> token-weights
- "effective tokens" -> effective-tokens

### AI Engines

- "co-pilot" -> GitHub Copilot
- "code x" -> Codex
- "cloud" -> Claude
- "gem ini" -> Gemini
- "serena" -> Serena

### Commands and Operations

- "G.H. A.W." -> gh-aw or `gh aw`
- "re-compile" -> recompile
- "work flow dispatch" -> workflow_dispatch
- "action lint" -> actionlint
- "ziz more" -> zizmor
- "poo teen" -> poutine
- "queue M.D." -> qmd

### File Formats and Extensions

- "dot M.D." -> .md
- "dot Y.A.M.L." or "dot Y M L" -> .yaml or .yml
- "dot lock dot Y M L" -> .lock.yml
- "jason" -> JSON
- "wasm" -> WebAssembly or wasm

### Technical Patterns

- "A.P.I." -> API
- "U.R.L." -> URL
- "H.T.T.P." -> HTTP
- "H.T.T.P.S." -> HTTPS
- "S.H.A." -> SHA
- "C.I." -> CI
- "G.H." -> GH
- "Y.A.M.L." -> YAML
- "O.I.D.C." -> OIDC
- "S.A.R.I.F." -> SARIF

### Environment Variables

Capitalize fully: `GITHUB_TOKEN`, `GH_TOKEN`, `COPILOT_GITHUB_TOKEN`, `GH_AW_GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, `CODEX_API_KEY`

## Clean Up and Improve Text

- **Remove Filler Words**: humm, um, uh, uhh, umm, you know, like, basically, actually, literally, kind of, sort of, I mean, I think, right?, okay?, so yeah, well.
- **Improve Clarity**: Remove redundant phrases ("in order to" -> "to", "at this point in time" -> "now"), make text more concise, and maintain technical accuracy.

## What to Avoid

- Generating code examples.
- Providing step-by-step planning.
- Simplifying technical concepts.

## References

- [Official DICTATION.md](https://github.com/github/gh-aw/blob/v0.74.3/DICTATION.md)
