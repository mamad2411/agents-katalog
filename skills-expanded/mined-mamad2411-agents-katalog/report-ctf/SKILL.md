---
name: report-ctf
description: CTF and lab challenge writeup from authorized challenge evidence — document challenge description, enumeration steps, exploitation path, flag capture, lessons learned, and tooling used. Structure adapts to challenge type (web, crypto, pwn, reversing, forensics, stego, misc). Requires lab/competition proof. Never publishes flags without organizer permission or competition end.
disable-model-invocation: true
risk: report-only
allowed-modes: [ctf]
authorization-required: no
evidence-outputs: [report, finding-summary, redaction-notes]
---

# CTF writeup — structured challenge documentation

Use this skill to draft CTF (Capture The Flag) challenge writeups from evidence collected during authorized lab/competition play. A good writeup documents the challenge for yourself (learning), your team (knowledge sharing), and the community (education after the competition ends). This skill structures raw notes, exploit scripts, flag captures, and debug output into a clear, reproducible writeup. It respects competition rules — never publish before the organizer's disclosure window opens, and never leak flags, solutions, or challenge files for an ongoing competition.

## Required inputs

- Challenge name, category, competition/CTF name, and date.
- Challenge description or prompt (if provided by organizers).
- Evidence from challenge play: enumeration notes, exploit scripts, output snippets, flag value.
- Competition rules: disclosure policy, flag-sharing restrictions, writeup publication window.
- Lab/competition authorization proof (even for CTFs — engagement record requires it).

## Required gates

1. `pentest_agent_load_config` and `pentest_agent_validate_policy` to verify reporting policy.
2. `pentest_agent_list_evidence` to load challenge evidence records.
3. No authorization cache required for CTF mode — lab/competition proof is recorded during engagement setup.
4. `pentest_agent_render_report` to produce the final writeup.

## Workflow

### Phase 1 — challenge context and metadata

Record the essential metadata that makes the writeup discoverable and contextual.

1. **Metadata fields**:
   - **CTF Name**: full competition name and year (e.g., "DEF CON CTF 2024 Qualifiers").
   - **Challenge Name**: exact challenge name as listed on the CTF platform.
   - **Category**: web, crypto, pwn/binary exploitation, reversing, forensics, stego, misc, OSINT, blockchain, hardware, AI/ML.
   - **Difficulty**: as rated by organizers (easy/medium/hard/insane) or your own assessment.
   - **Points**: points awarded for solving (or dynamic scoring range).
   - **Solves**: number of teams that solved (if published) — gives context on challenge difficulty.
   - **Team**: your team name.
   - **Date solved**: when the flag was captured.
2. **Challenge description**: copy the challenge prompt verbatim (if permitted by organizers). This gives the reader the same starting information you had. If the prompt contained a downloadable file, reference the file hash (SHA256) and type.

### Phase 2 — challenge-type-specific structure

Adapt the writeup structure to the challenge category.

#### Web challenges

1. **Initial reconnaissance**: what you observed when first accessing the challenge URL. Was it a login page, an API, a note-taking app? What technology clues were visible (headers, HTML comments, JS)?
2. **Enumeration**: what you discovered through exploration — hidden endpoints (robots.txt, sitemap, source code comments, directory brute-force), API endpoints, parameter behavior, error messages with information leaks, debug endpoints.
3. **Vulnerability identification**: what the bug was and how you found it. Specific payloads attempted. False leads you followed and why they didn't work.
4. **Exploitation**: the exact sequence that captured the flag. Include HTTP requests/responses, JavaScript snippets, curl commands, or Python exploit scripts. Redact any session tokens or non-challenge credentials.
5. **Flag**: `<FLAG_FORMAT{redacted_until_writeup_window}>` — redact the flag value until the competition disclosure window opens. Replace with `CTF{...}` in early drafts.

#### Crypto challenges

1. **Ciphertext/cipher description**: what you were given (hex string, encrypted file, network capture, custom algorithm description).
2. **Cryptanalysis approach**: how you analyzed the cipher. Classic attacks: frequency analysis, known-plaintext, chosen-plaintext, padding oracle, hash length extension, nonce reuse, weak random seed.
3. **Mathematical reasoning**: any mathematical properties you exploited. Include formulas where relevant.
4. **Exploitation script**: Python/sage/Pwntools script that decrypts or forges the ciphertext.
5. **Flag**: extracted from decryption output.

#### Pwn / binary exploitation challenges

1. **Binary analysis**: architecture (x86, x86-64, ARM, MIPS), mitigations (checksec output: NX, PIE, RELRO, Stack Canary, Fortify), file type (ELF, PE, Mach-O), linked libraries.
2. **Vulnerability discovery**: how you found the bug. Static analysis (Ghidra, IDA, Binary Ninja), dynamic analysis (GDB, pwndbg), fuzzing (AFL, libFuzzer).
3. **Vulnerability type**: buffer overflow, format string, use-after-free, heap overflow, integer overflow, type confusion, race condition, ret2libc, ROP, JOP, sigreturn-oriented programming (SROP).
4. **Exploit development**: exploit script with comments. Include: offset calculation, libc leak technique, ROP chain construction, shellcode (if no NX), one_gadget selection.
5. **Exploit execution**: `python3 exploit.py REMOTE` output showing the shell obtained.
6. **Flag**: read from `flag.txt`, `/home/ctf/flag`, or environment variable.

#### Reversing challenges

1. **File analysis**: file type (`file` command), strings output (relevant strings), entropy analysis (packed?), obfuscation indicators.
2. **Static analysis**: decompiled code snippets (Ghidra, IDA). Key functions annotated with your understanding.
3. **Dynamic analysis**: debugger trace, function breakpoints, register/memory inspection, strace/ltrace output.
4. **Solution approach**: how you extracted the flag. Was it a password check to bypass, an encoded string to decode, a custom algorithm to reverse?
5. **Solution script**: Python/GDB script/angr script that automates the solution.
6. **Flag**: extracted or computed.

#### Forensics challenges

1. **Evidence description**: what you were given (disk image, memory dump, PCAP, log file, image, audio, document).
2. **Tool chain**: tools used sequentially — `file`, `strings`, `binwalk`, `foremost`, `volatility`, `wireshark`, `tshark`, `exiftool`, `steghide`, `zsteg`, `Audacity` (audio), `ffmpeg` (video).
3. **Analysis steps**: chronological walkthrough of what you tried, what you found at each step, and how it led to the next step.
4. **Key findings**: the hidden data, deleted file, network stream, or encoded payload that contained the flag.
5. **Flag**: extracted from the evidence.

#### Stego challenges

1. **Carrier file**: type (PNG, JPEG, WAV, MP3, PDF, text).
2. **Stego tools used**: `steghide`, `zsteg`, `stegsolve`, `binwalk`, `exiftool`, `strings`, LSB extraction scripts, `Audacity` (spectrogram), `Sonic Visualizer`.
3. **Extraction method**: exact command lines or tool settings that revealed the hidden data.
4. **Flag**: extracted from carrier.

#### OSINT challenges

1. **Starting clues**: what you were given (image, username, email, domain, description).
2. **Search methodology**: platforms searched, dorks used, reverse image search queries, WHOIS/NSlookup results.
3. **Evidence chain**: how each discovery led to the next. Screenshots of key findings (redacted for PII if real people are involved).
4. **Flag**: how the final answer was derived from OSINT evidence.

#### Misc / general challenges

1. **Challenge description**: what you were asked to do.
2. **Approach**: what you tried, what failed, what worked.
3. **Solution**: the correct approach with explanation.
4. **Flag**: captured.

### Phase 3 — lessons learned and tooling notes

Add educational value beyond just "here's how I solved it."

1. **What I learned**: one or two sentences about the technique, tool, or concept you gained from this challenge.
2. **What I missed** (if applicable): time spent on wrong leads, misconceptions about the challenge, or rabbit holes you went down. Teaching what NOT to do is as valuable as teaching what TO do.
3. **Alternative approaches**: if you later learned of a different solution method, describe it briefly and credit the original solver.
4. **Tools used**: list every tool with a brief note on how it was used. This helps readers build their own toolkit.
5. **References**: links to relevant documentation, writeups, research papers, or CTF resources that helped you understand the vulnerability or technique.

### Phase 4 — flag redaction and publication timing

Respect competition rules regarding flag and solution publication.

1. **During an active competition**: never publish writeups, share flags with other teams, or post solutions publicly. This is cheating and may result in disqualification.
2. **After the competition ends, before the writeup window**: many CTFs allow writeups after the competition ends but some have a blackout period. Check the organizer's Discord, CTFtime page, or rules document.
3. **Flag redaction in final writeups**: some competitions require flags to be redacted even after the writeup window (e.g., flags used across multiple CTF instances). Replace with `CTF{...}` and note "Flag redacted per organizer request."
4. **If the challenge used realistic/published exploits against simulation targets**: do not include working exploit code that could be used against real targets. Abstract the technique without the paste-ready payload. Mention the vulnerability class and reference the CVE if applicable.

### Phase 5 — report structure

Build the writeup in a clean, skimmable format.

**Standard writeup template**:

```markdown
# [Challenge Name] — [CTF Name] [Year]

| Field | Value |
|---|---|
| Category | [web/crypto/pwn/rev/forensics/stego/misc/OSINT] |
| Difficulty | [easy/medium/hard/insane] |
| Points | [N] pts / [N] dynamic |
| Solves | [N] teams |
| Team | [Your Team Name] |
| Solved | [YYYY-MM-DD] |

## Challenge Description
> [Challenge prompt or description as provided by organizers]

## Enumeration / Analysis
[What you observed, tried, and discovered. Include screenshots or code snippets.]

### Key Findings
- Finding 1: ...
- Finding 2: ...

## Exploitation / Solution
[Step-by-step walkthrough of the solution.]

### Exploit / Solution Script
```python
# Exploit script with comments
```

```bash
# Key commands and output
```

## Flag
```
[FLAG_FORMAT{redacted_or_actual_flag}]
```

## Lessons Learned
- [What you learned]
- [What you would do differently]

## Tools Used
| Tool | Purpose |
|---|---|
| `tool_name` | How it was used |

## References
- [Link to relevant documentation or writeups]
```

## Decision points

- **Challenge was solved collaboratively with teammate(s)**: credit each contributor and describe who did what. Collaboration is a core CTF skill — documenting it honestly is better than claiming solo solves.
- **Solution relied on a 0-day or unpatched vulnerability in challenge infrastructure**: do not publish the exploit details if they could affect real systems. Abstract the technique. Notify organizers privately.
- **Challenge was unsolved during the competition but solved later**: mark the writeup as "post-competition solve." Note what you missed during the competition.
- **Writeup is for an ongoing CTF platform (HackTheBox, TryHackMe, picoCTF, etc.)**: these platforms have strict no-spoiler policies. Do not publish writeups for active machines/challenges. Some platforms allow writeups for retired machines only.
- **Flag format reveals the solution method**: if the flag content is itself a hint (e.g., `CTF{sqli_is_easy}`), consider redacting or noting "Flag content confirmed the vulnerability class."

## Prohibited behavior

- Publishing writeups or sharing solutions during an active competition (cheating).
- Publishing flags for active/ongoing CTF platform challenges (spoiler policy violation).
- Including working exploit code for vulnerabilities that could affect real-world systems.
- Sharing downloadable challenge files from the competition without organizer permission.
- Impersonating competition organizers or falsely claiming official endorsement of the writeup.
- Including PII of competitors, organizers, or third parties without consent.

## Evidence template

```text
CTF writeup for: DEF CON CTF 2024 Qualifiers
Total challenges solved: 5 / 12
Writeups drafted: 5

Challenge 1: "Baby Web" (web, 100 pts, easy)
  → Flag: CTF{...} (redacted for writeup window)
  → Technique: SQL injection via UNION SELECT in search parameter
  → Time to solve: 45 min
  → Key tool: sqlmap

Challenge 2: "XOR Madness" (crypto, 200 pts, medium)
  → Flag: CTF{...} (redacted)
  → Technique: Known-plaintext XOR attack with crib dragging
  → Time to solve: 2 hours
  → Key tool: Python + pwntools XOR

[...]

Redaction notes:
  - All flags redacted per CTF organizer policy (writeup window not yet open)
  - Challenge files not included (organizer request)

Publication plan:
  - Drafts saved locally
  - Will publish to CTFtime and personal blog after 2024-06-01 (30-day embargo)
  - Will notify organizers before publication
```

## Handoff

1. Store writeup drafts under `.pi/pentest-agent/engagements/<id>/reports/ctf/`.
2. After the competition writeup window opens, `pentest_agent_export_report` for each published writeup.
3. Explicitly note: all flags are redacted in the draft reports, competition rules regarding writeup publication are respected, no active-competition solutions were shared, and no challenge files are included without organizer permission.
