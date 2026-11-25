---
name: security-intake-before-import
description: Performs security intake before importing external code, scripts, MCP servers, skills, packages, or GitHub repos. Use when copying, installing, operationalising, or running third-party artefacts in an agent harness or developer environment.
---

# Security Intake Before Import

## Overview

Use this skill before bringing external code into a live environment.

Agents are good at copying useful things. They are also good at accidentally installing supply-chain landmines. Do the intake first.

## When to Use

- Importing a GitHub repo, script, MCP server, skill, plugin, package, prompt pack, or binary.
- Running an upstream install script.
- Copying code into live config.
- Giving a tool access to local files, browser state, tokens, shell, or network.
- Testing software that reads transcripts, history, or credentials.

## Intake Checklist

### 1. Identify source

Record:

- URL;
- owner;
- default branch;
- commit SHA;
- licence;
- stars/forks if relevant;
- recent maintenance;
- whether this is the expected upstream.

Pin a commit. Do not import from a floating branch when reproducibility matters.

### 2. Inspect before execution

Review:

- install scripts;
- package manifests;
- postinstall hooks;
- CI files;
- shell commands;
- network calls;
- filesystem writes;
- credential/env access;
- binary blobs;
- minified or generated code.

### 3. Scan where possible

Use available scanners without installing random new tooling from the target repo.

Examples:

```bash
gitleaks detect --no-git --redact
semgrep scan --config auto
npm audit --package-lock-only
python -m compileall .
bash -n script.sh
node --check file.js
```

If a scanner is missing, say it is missing. Do not pretend.

### 4. Minimise import

Import only what is needed:

- one script instead of whole repo;
- one skill instead of whole skill pack;
- pinned package version instead of latest;
- read-only config before write-capable config.

### 5. Synthetic first

If the tool reads private history, browser state, transcripts, credentials, or local repos, test with synthetic data first.

Live data requires explicit approval and a redaction plan.

## Report Format

```text
Source:
Commit pinned:
Licence:
Executable surfaces:
Network access:
Filesystem access:
Credential access:
Scans run:
Findings:
Imported artefacts:
Residual risk:
Verdict: import / hold / reject
```

## Stop Conditions

Reject or hold if:

- source cannot be identified;
- licence is incompatible;
- install script exfiltrates data;
- binary blob is required but unaudited;
- package has suspicious postinstall;
- tool needs secrets without a clear boundary;
- live user data would be read before synthetic proof.
