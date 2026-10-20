---
name: crate-search
description: Find ready-to-use Rust crates or frameworks for an architectural, code, or design need by searching crates.io, and report candidates with downloads, version, and maintenance data. Use this skill whenever the Researcher role is asked to find a library, crate, or framework in Rust, compare options for a requirement, or check whether a ready-made solution exists before code is written.
---

# crate-search

Writing code that a mature crate already provides costs time and adds defects. The Researcher finds candidates, and the Architect and Developer decide.

## Procedure

1. Write the need in one sentence from the issue (for example "MQTT client, async, TLS"). Note hard constraints: `no_std`, license, async runtime, platform.
2. Search with two or three different queries (synonyms, the protocol name, the task name):

```bash
python3 $AGENT_INFRA_DIR/harness/library/skills/crate-search/scripts/search_crates.py "mqtt client" --sort downloads
```

The script drops every crate with fewer than 10000 "Downloads all time". This is a project rule, not a preference. Do not add a dropped crate to the list, even if it looks good.
3. For each remaining candidate, open the repository and check: last release date, open issues trend, license, `unsafe` use, direct dependencies, and whether it fits the constraints. Use `crate-download-filter` to re-check names you found elsewhere.
4. Report a table: `crate | version | downloads | last update | license | fit | risk`. Give a recommendation and a fallback. If nothing qualifies, say so. "No suitable crate found" is a valid result and the Developer then writes the code.
5. Comment on the issue (see `issue-comment-protocol`). Put long comparisons in the wiki.

## Rules

- Report only data you read. Do not fill in a license or date from memory.
- Prefer fewer dependencies. A crate that pulls in fifty others is a cost.
- Do not edit `Cargo.toml`. Choosing the crate is the Architect's and Developer's job.
