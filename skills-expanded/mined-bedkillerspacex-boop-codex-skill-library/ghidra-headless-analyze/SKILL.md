---
name: ghidra-headless-analyze
description: >
  Run Ghidra in headless (analyzeHeadless) mode for batch import, auto-analysis,
  script execution, and project/export automation on local or authorized binaries.
  Use for CTF/lab/owned firmware and CI reverse-engineering pipelines — not for
  unauthorized analysis of third-party proprietary software outside license/ROE.
---

# Ghidra Headless Analyze

## Scope And Authorization

- **In scope:** Binaries you own, open-source, CTF challenges, authorized malware lab samples
  in isolated environments.
- **Out of scope:** Processing stolen IP outside authorization; executing malware outside
  a controlled lab; distributing decompiled vendor code against license terms.
- Headless analysis can run scripts with filesystem access — sandbox CI runners.
- Keep original samples immutable; write Ghidra projects to a separate work directory.

## When To Use

- Batch-analyzing many binaries without GUI.
- CI pipeline: import → analyze → run Ghidra script → export results.
- Reproducing analysis with scripted flags (processor, compiler, timeout).
- Prepping projects for later GUI review.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Interactive GUI RE | Manual Ghidra use + RE methodology skills |
| Ghidra Java scripts deep dive | `ghidra-scripting-java` |
| Ghidra Python/basic scripting | `ghidra-scripting-basics` |
| Dynamic debugging pretty-printers | `gdb-python-pretty-printers` |
| Vulnerability exploitation | CTF exploit skills with authorization |
| Implementation quality of product | `code-quality-standards` |

## Concepts

| Term | Meaning |
| --- | --- |
| `analyzeHeadless` | Ghidra command-line launcher |
| Project | Container of programs under a directory |
| Import | Load binary into project |
| Auto-analysis | Default analyzers (disassembly, decompiler props, etc.) |
| `-postScript` / `-preScript` | Run Ghidra scripts around analysis |
| `-process` | Open existing program by name |
| `-import` | Import file path |
| Processor / compiler spec | Override language detection when needed |

## Workflow

### 1. Confirm environment

```bash
# Locate install (examples)
echo "$GHIDRA_HOME"
# Windows often: C:\ghidra_* or user-defined

# Headless script path
ls "$GHIDRA_HOME/support/analyzeHeadless"
# Windows: %GHIDRA_HOME%\support\analyzeHeadless.bat
```

1. Record Ghidra version, sample hash, authorization.
2. Success: project created; analysis completes; script artifacts written.

### 2. Create work layout

```text
work/
  samples/          # immutable copies or read-only mounts
  ghidra_projects/  # project directories
  out/              # exported JSON/C/logs
  scripts/          # local Ghidra scripts
```

```bash
sha256sum work/samples/target.bin
mkdir -p work/ghidra_projects work/out
```

### 3. Basic headless import + analyze

```bash
"$GHIDRA_HOME/support/analyzeHeadless" \
  /path/to/work/ghidra_projects \
  LabProject \
  -import /path/to/work/samples/target.bin \
  -analysisTimeoutPerFile 300 \
  -deleteProject
```

Notes:

- Omit `-deleteProject` to keep project for GUI.
- First arg: **project directory parent**; second: **project name**.
- On Windows use `analyzeHeadless.bat` and PowerShell-friendly paths.

### 4. Re-open and process existing program

```bash
"$GHIDRA_HOME/support/analyzeHeadless" \
  /path/to/work/ghidra_projects \
  LabProject \
  -process target.bin \
  -noanalysis \
  -postScript ExportFunctions.py /path/to/work/out/functions.json
```

### 5. Scripts and parameters

```bash
"$GHIDRA_HOME/support/analyzeHeadless" \
  /path/to/work/ghidra_projects Proj \
  -import sample.bin \
  -scriptPath /path/to/work/scripts \
  -preScript Prepare.py \
  -postScript DumpStrings.java out/strings.txt \
  -log out/headless.log
```

Script args follow script name as additional tokens — parse inside script.

### 6. Language overrides and recursive import

```bash
# Recursive directory import
"$GHIDRA_HOME/support/analyzeHeadless" \
  /path/to/work/ghidra_projects Bulk \
  -import /path/to/work/samples/dir \
  -recursive \
  -analysisTimeoutPerFile 120

# Force language if detection fails (example id)
# -processor x86:LE:64:default -cspec gcc
```

Confirm language IDs from Ghidra processor manuals / GUI import dialog.

### 7. CI tips

| Topic | Guidance |
| --- | --- |
| JVM memory | `JAVA_TOOL_OPTIONS=-Xmx4g` or Ghidra support env vars |
| Timeouts | Set per-file analysis timeout |
| Caching | Cache Ghidra install; do not cache malware projects publicly |
| Artifacts | Export summaries only; avoid full decompilation of proprietary code to public CI logs |
| Headless + xvfb | Usually unnecessary for analyzeHeadless |

### 8. Verify outputs

1. Log contains `REPORT: Analysis succeeded` / no fatal analyzer errors.
2. Project opens in GUI with expected functions.
3. Post-script files exist and parse.
4. Hash of sample still matches original.

```bash
test -f work/out/functions.json
tail -n 50 work/out/headless.log
```

## Common flags reference

| Flag | Purpose |
| --- | --- |
| `-import PATH` | Import binary/dir |
| `-process NAME` | Open program in project |
| `-recursive` | Import tree |
| `-noanalysis` | Skip auto-analysis |
| `-analysisTimeoutPerFile SEC` | Cap analysis time |
| `-scriptPath DIR` | Additional script dirs |
| `-preScript` / `-postScript` | Scripts |
| `-deleteProject` | Remove project on exit |
| `-readOnly` | Do not save (when supported) |
| `-log FILE` | Log path |
| `-max-cpu N` | Limit CPU if available in version |

Always check `analyzeHeadless -help` for your Ghidra release.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Samples | Hashed immutable store | Overwrite originals in place |
| Batch | Timeouts + logs | Endless hang on huge bins |
| Scripts | Versioned in repo | One-off unsigned blobs only on laptop |
| CI | Isolated runner | Analyze malware on dev laptop AV-off forever |
| Legal | Authorized samples | Warehouse of pirated apps |

## Output Checklist

- [ ] Authorization and sample hashes recorded
- [ ] GHIDRA_HOME / version documented
- [ ] Project path layout created
- [ ] Headless import/analyze command succeeded
- [ ] Scripts run with outputs in `out/`
- [ ] Log reviewed for analyzer failures
- [ ] GUI open smoke test optional
- [ ] Secrets/IP handling per ROE
- [ ] Repro command saved in notes

## Rules

- Authorized binaries only; isolate hostile samples.
- Do not execute unknown malware on host — analysis ≠ running the sample outside sandbox.
- Keep scripts and projects out of world-readable temp if sensitive.
- Prefer scripted reproducibility over GUI-only tribal knowledge.
- Deep script authoring → `ghidra-scripting-basics` / `ghidra-scripting-java`.
