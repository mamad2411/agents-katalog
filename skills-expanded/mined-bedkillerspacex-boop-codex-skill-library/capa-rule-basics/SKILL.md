---
name: capa-rule-basics
description: >
  CAPA (Capability Analysis) rules for malware/lab binaries you are authorized to
  analyze: rule structure (meta/features/namespaces), block/match logic, testing with
  capa, and contributing detections without false-positive noise. Use when writing
  capa rules, capa explorer, FLARE capa, or capability tagging of samples in a lab.
---

# Capa Rule Basics

## Scope And Authorization

- **In scope:** Malware samples and binaries in isolated labs, CTFs, or authorized malware analysis environments.
- **Out of scope:** Running untrusted malware on production endpoints; analyzing systems without authorization.
- Keep samples in detonation lab; do not redistribute malware carelessly.
- Redact customer-sensitive paths if analyzing proprietary binaries under NDA.
- Pair static RE with binary analysis skills; this skill is CAPA rule authoring.

## When To Use

- Writing or editing `.yml` capa rules for capabilities (e.g. inject, persist, C2).
- Testing whether capa finds expected capabilities on a known sample.
- Reducing FPs by tightening features (API combos, numbers, strings, characteristics).
- Organizing namespaces/libraries for an internal rule pack.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full malware RE methodology | binary-re / malware analysis skills |
| YARA packing detection only | YARA skills |
| Dynamic detonation orchestration | sandbox skills |
| Ghidra headless alone | Ghidra skills |
| Implementation quality for non-rule code | `code-quality-standards` |

## Domain Focus

| Field | Role |
| --- | --- |
| `rule` meta | name, authors, scopes, references, examples |
| `features` | boolean logic of API/string/number/characteristic/match |
| `namespace` | taxonomy path e.g. `host-interaction/process/inject` |
| `scope` | function / basic block / file / process (as supported) |
| `att&ck` / `mbc` | optional mappings |
| `examples` | sample SHA256 + offset notes for regression |

## Workflow

### 1. Confirm scope and success criteria

1. Lab sample set, capa version, rule path format.
2. Success: rule matches intended samples; no match on clean corpus subset; docs/examples filled.
3. Isolate analysis host from production networks.

### 2. Inventory existing coverage

```bash
capa --version
capa -r /path/to/rules sample.bin
capa -vv sample.bin  # feature debug
# List rules
find rules -name '*.yml' | head
```

1. Search for overlapping rules before duplicating.
2. Note capa supported feature set for your version.

### 3. Draft rule structure

```yaml
rule:
  meta:
    name: inject shellcode via VirtualAlloc + WriteProcessMemory
    namespace: host-interaction/process/inject
    authors:
      - your-team
    scope: function
    references:
      - https://attack.mitre.org/techniques/T1055/
    examples:
      - aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:0x401000
    att&ck:
      - Defense Evasion::Process Injection [T1055]
  features:
    and:
      - api: kernel32.VirtualAlloc
      - api: kernel32.WriteProcessMemory
      - optional:
          - api: kernel32.CreateRemoteThread
```

1. Prefer **capability** names that describe behavior, not malware family alone.
2. Use `or` / `and` / `not` / `optional` thoughtfully — optional should not make rule vacuous.
3. Numbers/strings: beware packing; prefer API graphs when possible.
4. `match:` subrule references for composition.

### 4. Feature selection tips

| Feature type | Tip |
| --- | --- |
| `api` | Include DLL context when needed; watch forwarded exports |
| `string` | Avoid short generic strings (`cmd`, `http`) alone |
| `number` | Constants like `0x40` (RWX) with surrounding APIs |
| `characteristic` | `embedded pe`, `loop`, etc. as supporting |
| `import` / `export` | File-scope hints |
| `substring` / regex | Higher FP risk — test carefully |

1. Function scope reduces FPs vs file-wide loose ORs.
2. Require 2+ independent signals for noisy APIs.

### 5. Test rules

```bash
# Positive
capa -r ./rules -f my-inject.yml sample_known.bin
# Or full rules + your path first
capa -r ./rules sample_known.bin | rg -i inject

# Negative corpus (clean utilities)
for f in clean/*; do capa -r ./rules/my-inject.yml "$f"; done

# Feature trace when missing match
capa -vv sample_known.bin 2>&1 | rg -i VirtualAlloc
```

1. Add `examples` with SHA256 for CI regression.
2. If capa uses rule linters in repo, run them.
3. Document intended OS/arch (x86 PE vs ELF).

### 6. Tune FPs / FNs

1. FN: sample packed → note limitation; maybe add packer capability separately.
2. FP: remove single generic API; require combo or number.
3. Avoid overfit to one sample’s odd strings unless family rule is the goal.

### 7. Hand off

1. PR with before/after capa output on examples.
2. Namespace placement reviewed by peers.
3. Version pin capa in lab docs.
4. Never commit live malware samples to public repos — hashes only.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Logic | API combo + scope function | Single `api: CreateFile` rule |
| Meta | examples SHA256 | Empty meta |
| Naming | Behavior-oriented | `rule1_final_v3` |
| Testing | Clean + dirty corpus | Only one malware hit |
| Safety | Isolated lab | Detonate on corp laptop domain-joined |
| Mapping | ATT&CK when clear | Random T-codes for vanity |

## Output Checklist

- [ ] Authorization/lab isolation confirmed
- [ ] capa version noted
- [ ] Overlap search done
- [ ] Rule YAML with meta/features/namespace
- [ ] Positive match on intended samples
- [ ] Negative check on clean set
- [ ] examples hashes recorded
- [ ] FP/FN notes in PR
- [ ] No malware binaries committed to public git

## Rules

- Authorized malware analysis environments only.
- Prefer precise multi-feature logic over broad noisy rules.
- Document limitations (packing, arch).
- Hashes not samples in git.
- Full reverse engineering workflow lives in broader RE skills.
