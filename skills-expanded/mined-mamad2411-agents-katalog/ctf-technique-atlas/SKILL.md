---
name: ctf-technique-atlas
description: Deep CTF technique atlas for mapping challenge clues to concrete attack
  patterns, tools, scripts, and next probes across Web, Crypto, Forensics, Reverse,
  Pwn, Misc/Jail, OSINT, Mobile, Cloud, Blockchain, Hardware/RF/ICS, Game/Protocol,
  and AI/ML. Use when the user asks to strengthen CTF solving ability, research all
  CTF techniques, classify an unknown CTF challenge, or choose the next attack path.
version: 1.0.0
license: MIT
metadata:
  hermes_origin: import
tags:
- ctf
- technique-atlas
- training
- triage
- exploitation
- writeups
related_skills:
- ctf-web-exploitation
- digital-forensics
- ctf-reverse-engineering
- binary-exploitation
- ctf-kernel-exploitation
- ctf-misc-toolkit
---

# CTF Technique Atlas

## Purpose

Use this skill as the deep technique index when solving or training CTFs. It maps observable clues to likely vulnerabilities, probes, tools, and solver/exploit patterns. It complements the domain skills: load the matching domain skill after classification.

## Operating rule

Do not only explain techniques. User wants practical CTF solving ability first, not mandatory boilerplate. For each challenge, create only the files/scripts needed to solve and verify the result; use full scaffolding only when the challenge is complex or the user asks for it.

## Minimal practical artifacts

For each challenge or drill, prefer the lightest useful structure:

```text
~/ctf-training/<category>/<challenge>/
  artifacts/   # original provided files, if any
  solve.py     # or exploit.py / extract.py / interact.py as appropriate
  notes.md     # short command log / key observations, only when useful
```

Do not spend time generating empty templates. The priority is: run probes, write a working solver/exploit/extractor, verify the flag, and preserve reusable lessons.

## Fast workflow

1. Inventory artifact/service/source and flag format.
2. Create minimal working files only if needed.
3. Match clues against `references/technique-matrix.md`.
4. Load the specific domain skill.
5. Run the first probes from `references/first-probes.md`.
6. Build and execute a solver/exploit/extractor from `references/solver-patterns.md`.
7. Verify flag and update skills if a reusable trick appears.

## Deep references

- `references/technique-matrix.md` — category-by-category attack map and clue-to-technique routing.
- `references/first-probes.md` — first commands/probes for each artifact type.
- `references/solver-patterns.md` — reusable exploitation and solver script patterns.
- `references/tooling-map.md` — practical tools by category and when to use them.
- `references/mastery-drills.md` — progressive drills to strengthen each CTF family.
- `references/oscilloscope-bmp-analysis.md` — multi-frame BMP time-series analysis workflow (NEW)
- `references/scope-trace-bmp-stego.md` — encrypted tool + BMP sequence CTF pattern
- `references/image-sequence-decoding.md` — decoding hidden messages from image sequences

## Scripts

- `scripts/ctf_router.py` — lightweight text/artifact clue classifier that suggests likely CTF categories and first probes.

## 2025-2026 CTF Resource Quick Reference

### Key CTF Archives & Training Resources
- **CTF Archives**: `github.com/sajjadium/ctf-archives` — comprehensive challenge archive (0CTF, HITCON, Google, SekaiCTF, etc.)
- **Kernel-Exploit-Dojo**: `github.com/mito753/Kernel-Exploit-Dojo` — 100+ kernel CTF challenges with exploit code + writeups
- **pyjail-collection**: `github.com/jailctf/pyjail-collection` — 113 pyjail challenges across 20+ CTFs
- **how2heap**: `github.com/shellphish/how2heap` — updated for glibc 2.41/2.42
- **7Rocky/CTF-scripts**: `github.com/7Rocky/CTF-scripts` — SageMath/Python CTF solvers
- **CTFtime**: `ctftime.org` — event calendar, writeups, team rankings
- **CryptoHack**: `cryptohack.org` — interactive crypto challenges including lattice/PQ

### AI-Assisted CTF Tools
- **IDA Pro MCP**: `github.com/mrexodia/ida-pro-mcp` — MCP server for IDA's decompiler
- **GhidraMCP/ReVa**: `github.com/cyberkaida/reverse-engineering-assistant` — 110 tools for Ghidra via MCP
- **OGhidra**: `github.com/LLNL/OGhidra` — AI-powered Ghidra with agentic loop + RAG
- **angr + dAngr**: LLM-guided symbolic execution

### 2025-2026 New Exploitation Techniques Summary

| Domain | Technique | CTF Example | Key Innovation |
|--------|-----------|-------------|----------------|
| Pwn | glibc 2.42 mp_ overwrite | snakeCTF 2025 old-school | tcache disable → fastbin dup → mp_ re-enable |
| Pwn | AArch64 COOP + relative vtables | HITCON CTF 2025 calc | COOP only with legitimate .rodata vtables |
| Kernel | modprobe_path AF_ALG bypass | Theori blog (2025) | request_module via AF_ALG bind() |
| Kernel | Dirty Pipe / page cache | b01lers 2026 throughthewall | pipe_buffer reclaim → /etc/passwd |
| Misc | Python 3.13 setattr jail | HITCON CTF 2025 simp | venv module import execution |
| Misc | pickle/cpickle divergence | DiceCTF 2026 yaps | py3.15+ memo data structure difference |
| Misc | numpy genfromtxt RCE | KalmarCTF 2025 Paper Viper | crafted CSV → arbitrary code execution |
| Web | HTTP/2 request smuggling | TryHackMe 2026 | H2.TE, H2.CL, h2c downgrade attacks |
| Web | React Server Components RCE | CVE-2025-55182 | unsafe deserialization in Flight protocol |
| Crypto | Math.random prediction | Google CTF 2025 | state recovery from observed outputs |

## Maintenance standard

A technique is considered learned only when Hermes can:
- recognize the clue pattern;
- run the right first probes;
- produce a minimal solver/exploit/extractor;
- explain the root cause or hidden signal;
- verify the flag;
- preserve the reusable pattern in a skill or script.
