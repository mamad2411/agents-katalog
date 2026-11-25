---
name: verify-agent-skills
description: "Drive agent-skills the way a maintainer does: run the aggregate test suite, spot-check CLIs, capture evidence. Use before opening PRs or after editing notion-sync scripts or leadership-prompts."
---

# Verify agent-skills

Primary surface: **Node CLIs** under `productivity/notion-sync/scripts/` and `leadership/leadership-prompts/scripts/`. No long-running server.

## Launch

Not applicable (CLI-only repo). From repository root:

```bash
npm test
```

Ready when the command exits `0` and prints `✅ All tests passed.`

## Doctor

Read-only checks before driving features:

```bash
node -e "const v=process.versions.node; const [maj,min]=v.split('.').map(Number); const ok=maj>=25||(maj===24&&min>=5)||(maj===22&&min>=21)||maj<22; console.log('node',v, ok?'portable-ok':'protected-sentinel-tests-need-22.21+'); process.exit(ok?0:2)"
node -e "const fs=require('fs');const path=require('path');function d(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?d(path.join(dir,e.name)):(/^test-.*\\.js$/.test(e.name)?[path.join(dir,e.name)]:[]))} const n=d('tests').length; console.log('discovered tests:',n); process.exit(n>=10?0:1)"
```

If doctor exits `2`, portable suites should still pass; only protected-secret transport tests need newer Node.

## Drive

### Feature: full regression

```bash
npm test 2>&1 | tee /tmp/verify-agent-skills-run.log
```

### Feature: leadership CLI smoke

```bash
node leadership/leadership-prompts/scripts/leadership-prompts.js list | head -5
node leadership/leadership-prompts/scripts/leadership-prompts.js random | head -20
```

### Feature: notion-sync help (no network)

```bash
node productivity/notion-sync/scripts/search-notion.js --help
```

## Evidence

Store under `/tmp/verify-agent-skills-evidence/`:

- `run-all.log` — full `npm test` transcript
- `doctor.txt` — doctor command outputs
- Optional: `leadership-random.txt`, `search-help.txt`

Proof standards: exercise real entrypoints (not internal requires), capture exit code + stdout/stderr, and for test suites confirm aggregate pass message.

## Cleanup

No processes to kill. Evidence in `/tmp/verify-agent-skills-evidence/` is kept for PR attachments; remove manually when done.

## Helpers

```bash
mkdir -p /tmp/verify-agent-skills-evidence
```
