---
name: readme-auto-toc-with-markers
description: Use HTML comment markers (`<!-- BEGIN AUTO GENERATED X -->`/`<!-- END AUTO GENERATED X -->`) to carve mutable regions inside README.md and regenerate them idempotently from source of truth.
category: build-tooling
version: 1.0.0
version_origin: extracted
tags: [docs, readme, codegen, markers, idempotent]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/ChromeDevTools/chrome-devtools-mcp.git
source_ref: main
source_commit: 0a6aaa52ebacb2db834ffa437863e5844aa3730b
source_project: chrome-devtools-mcp
source_path: scripts/generate-docs.ts
imported_at: 2026-04-18T00:00:00Z
---

# README Auto-Regenerated Regions

## When to use

- Your README has one or more sections that need to reflect code (tool list, CLI options, supported env vars) and you hate hand-keeping them in sync.
- You want humans to edit everything else around them without risk of accidental stomp.

## How it works

- In your README, place paired markers: `<!-- BEGIN AUTO GENERATED TOOLS -->` and `<!-- END AUTO GENERATED TOOLS -->`. You can have multiple marker pairs with different names.
- In your docs generator: `const before = readmeContent.slice(0, beginIndex + beginMarker.length); const after = readmeContent.slice(endIndex); fs.writeFileSync(README_PATH, before + '\n\n' + newContent + '\n' + after);`
- Always leave the markers themselves in the file (`before + ... + endMarker + after`). The regex only replaces the content between them.
- On missing markers, warn and skip. Don't refuse the build — the generator should be best-effort.
- Run all generator passes in sequence (tools TOC, options list, anything else) against the same README, each finding its own markers.

## Example

```ts
function updateReadmeRegion(readmePath, begin, end, newContent) {
  const content = fs.readFileSync(readmePath, 'utf8');
  const beginIdx = content.indexOf(begin);
  const endIdx = content.indexOf(end);
  if (beginIdx === -1 || endIdx === -1) {
    console.warn(`Missing markers ${begin} / ${end} in ${readmePath}`);
    return;
  }
  const before = content.slice(0, beginIdx + begin.length);
  const after = content.slice(endIdx);
  fs.writeFileSync(readmePath, before + '\n\n' + newContent + '\n' + after);
}

updateReadmeRegion('./README.md',
  '<!-- BEGIN AUTO GENERATED TOOLS -->',
  '<!-- END AUTO GENERATED TOOLS -->',
  generateToolsTOC(categories));
```

## Gotchas

- Marker names must be unique — `<!-- BEGIN AUTO GENERATED -->` alone collides when you add more sections. Name them (`TOOLS`, `OPTIONS`, `ENV`).
- `indexOf` finds the first occurrence. If a PR accidentally commits two begin markers, the second-region replacement nukes content. Add a "refuse if marker appears twice" guard.
- Include the markers in committed README — never auto-generate them as part of the content or they vanish on a broken build.
- Run the generator in CI and fail the build if the file changed. That's how you enforce "docs stay in sync".
- Prefer HTML comments over custom block fences; HTML comments survive Markdown rendering as nothing visible.
