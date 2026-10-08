---
name: data_exfiltration_analysis
description: "Guidance for identifying data theft patterns in skills"
version: 1.0.0
author: ClawSecbot
tags: [scenario, data-exfiltration]
---

# Data Exfiltration Analysis

## When This Skill Is Needed

Load this skill when you detect network requests or data transfer patterns in the target skill — such as `curl`, `wget`, `fetch`, HTTP POST requests, cloud storage uploads, or any code that sends data to external servers. Data exfiltration is often the ultimate goal of an attack.

## How to Judge Risk

When analyzing potential data exfiltration, trace the complete data flow and think through these questions:

### 1. What data is being collected?

Trace backwards from the network request to find the data source:
- Is it reading sensitive files? (SSH keys, AWS credentials, .env files, browser data)
- Is it capturing environment variables? (API_KEY, TOKEN, SECRET, PASSWORD)
- Is it collecting system information? (hostname, username, IP, running processes)
- Is it accessing data through function calls or config files that eventually contain sensitive information?

The sensitivity of the data determines the severity of the risk. Credentials and private keys are CRITICAL. System fingerprinting is MEDIUM.

### 2. Where is the data being sent?

Analyze the destination of the network request:
- Is it a raw IP address instead of a domain? (avoiding DNS logging)
- Is it a free hosting service, file sharing site, or webhook service?
- Is it a recently registered or suspicious-looking domain?
- Is it using non-standard ports?
- Is the destination disguised as "analytics", "telemetry", or "crash reporting"?

Legitimate skill functionality rarely needs to send data to unknown external servers.

### 3. How is the data being packaged?

Look at what happens to the data before transmission:
- Is it being base64 encoded, compressed, or encrypted? (possibly to evade detection)
- Is it being split into chunks and sent across multiple requests?
- Are there multiple encoding layers? (gzip → base64 → POST is highly suspicious)
- Is data hidden in DNS queries, HTTP headers, or other covert channels?

Multi-layer encoding before transmission is a strong indicator of malicious intent.

### 4. Is the exfiltration conditional?

Check if data is only sent under certain conditions:
- Does it check for CI/sandbox environments and skip exfiltration there?
- Is there a time-based trigger or execution counter?
- Does it only run for specific users or on specific platforms?

Conditional exfiltration that avoids detection environments is CRITICAL.

### 5. Is the data flow reasonable for the skill's purpose?

Consider the skill's stated functionality:
- Does a code formatter need to upload anything?
- Does a text processing skill need AWS credentials?
- Would a legitimate tool send your SSH keys anywhere?

If the data collection and transmission don't serve the skill's purpose, it's likely malicious.

## Key Risk Signals

**CRITICAL — Immediate concern:**
- Credentials or API keys being transmitted
- SSH private keys or certificates being uploaded
- Data sent through covert channels (DNS tunneling, ICMP)
- Multi-layer encoding hiding exfiltration
- Conditional exfiltration avoiding CI/sandbox

**HIGH — Requires investigation:**
- Source code or .env files being uploaded
- Encoded/encrypted data before transmission
- Transfer to raw IP addresses
- Webhook/messaging platforms receiving file content
- System information being collected and sent

**MEDIUM — Needs context:**
- Legitimate-looking analytics or telemetry
- Transfer to known CI/CD services
- Documentation being published externally

## Cross-skill Coordination

- If data exfiltration is driven by script execution → load **script_execution_analysis**
- If data payload appears obfuscated → load **obfuscation_evasion_analysis**
- If exfiltration is triggered by package installation → load **dependency_supply_chain_analysis**
