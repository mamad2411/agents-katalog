---
name: script_execution_analysis
description: "Guidance for analyzing executable scripts found in skills"
version: 1.0.0
author: ClawSecbot
tags: [scenario, script-analysis]
---

# Script Execution Analysis

## When This Skill Is Needed

Load this skill when you discover executable scripts (.sh, .py, .js, .ps1, etc.) or embedded code blocks in the target skill. Scripts are the most versatile attack vector because malicious operations can be hidden among legitimate commands.

**CRITICAL**: Never judge a script by its filename alone. A script named `cleanup.sh` could contain data exfiltration code. Always read the actual content.

## How to Judge Risk

When analyzing a script, think through these questions:

### 1. Does the script's behavior match its declared purpose?

A setup script should install dependencies and configure the project. If it's also sending data to external servers or modifying files outside the project directory, that's a red flag. Ask yourself:
- What does the skill claim this script does?
- What does the script actually do when you read it line by line?
- Are there operations that have nothing to do with the stated purpose?

### 2. Does the script operate outside its expected scope?

A text processing skill shouldn't need network access. A code formatter shouldn't modify `~/.bashrc`. Consider:
- Does the script access files outside the skill directory?
- Does it modify system configuration files (bashrc, zshrc, profile, hosts)?
- Does it install persistence mechanisms (cron jobs, startup scripts)?
- Does it make network requests when the skill doesn't need connectivity?

### 3. Are there hidden execution paths?

Scripts may have conditional branches that behave differently under different conditions:
- What happens in the `if` branch vs the `else` branch?
- Does the script check for CI/sandbox environments and behave differently?
- Are there time-based triggers or execution counters?
- Flag any case where one branch is benign but another is dangerous.

### 4. Is there encoding or obfuscation?

Legitimate scripts rarely need to hide their code. Look for:
- Base64 encoded strings being decoded and executed
- Hex escape sequences or variable substitution chains
- Commands split across multiple variables then reassembled
- `eval` or `exec` with string manipulation

### 5. Are there dangerous operations disguised in normal code?

Look for these patterns hidden in otherwise normal-looking scripts:
- `curl | bash` or `wget | sh` — remote code execution
- Commands that read sensitive files (SSH keys, credentials, env vars)
- Commands that send data to external URLs
- Privilege escalation (`sudo`, `chmod +s`, modifying sudoers)
- System destruction commands (`rm -rf`, disk operations)

### 6. Do comments contain executable content?

Some attacks hide payloads in comments that get extracted and executed later:
- Check if any code uses `grep` or `sed` to extract content from comments
- Look for base64 or encoded strings hidden in comment text

## Key Risk Signals

**CRITICAL — Immediate concern:**
- Remote code execution patterns (`curl|bash`, encoded payload execution)
- Reverse shells or backdoor connections
- Credential file access combined with network transmission
- SUID bit manipulation

**HIGH — Requires investigation:**
- Persistence mechanisms (cron, shell config modification)
- Network data transfer to external hosts
- Operations outside expected skill scope
- Conditional execution with asymmetric risk

**MEDIUM — Needs context:**
- Network operations for seemingly legitimate purposes
- Dynamic code execution within controlled context
- File operations with broad scope

## Cross-skill Coordination

- If the script contains network operations sending data externally → load **data_exfiltration_analysis**
- If the script contains encoded/obfuscated content → load **obfuscation_evasion_analysis**
- If the script installs packages → load **dependency_supply_chain_analysis**
