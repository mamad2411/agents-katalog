---
name: mcp-server-hub
description: "MCP Server Hub — organizing, managing, and invoking 38+ dockerized security tools as MCP servers. Use when managing or invoking MCP security tool servers."
---

# MCP Server Hub

## Overview

MCP Server Hub is a centralized skill for organizing, managing, and invoking over 38 dockerized security tools (such as Nmap, Nuclei, Ghidra, SQLMap, Hashcat, etc.) as MCP servers. Every tool runs under a non-root user within minimal, Trivy-scanned Docker containers. This skill allows agents to invoke security tools directly via the MCP protocol, parse their outputs into a standardized format, and monitor resource consumption.

**Core principle:** EACH TOOL RUNS IN ITS OWN ISOLATED CONTAINER; NO TOOL MAY DIRECTLY ACCESS THE HOST SYSTEM.

## The Iron Law

```
NO MCP SERVER CONTAINER CAN ACCESS THE HOST NETWORK OR FILESYSTEM DIRECTLY. ALL TOOLS MUST RUN IN ISOLATED, NON-ROOT, RESOURCE-CONSTRAINED CONTAINERS.
```

## When to Use

**Use this when:**
- You need to perform a security scan on a target system.
- You need to execute network discovery, vulnerability scanning, or cryptographic analysis.
- You need to run multiple security tools sequentially or in parallel.
- You want to integrate security tools into an automated pipeline.

**Use this ESPECIALLY when:**
- Under time pressure, you think, "Let me quickly run an Nmap scan" — the hub is pre-configured and fast.
- You need to compile output from multiple security tools for client reporting.
- You need to execute security testing during a CI/CD pipeline run.

**Don't skip when:**
- You only need to check a simple log or metric (if a lighter tool is sufficient, do not spin up the hub).
- You are operating in an environment that does not support containerization (use local alternative tools).

## Phase 1: Review the Tool Catalog

**BEFORE proceeding:**

1. **Verify the tool inventory** — Confirm each tool's name, version, and capabilities.
2. **Identify tool categories** — Network scanning, vulnerability analysis, cryptography, reverse engineering, etc.
3. **Check dependencies** — Determine if a tool requires input from the output of another MCP server.

```
mcp-server-hub inventory list
mcp-server-hub inventory show --tool nmap
```

## Phase 2: Container Configuration and Resource Limits

**BEFORE proceeding:**

1. **Set CPU limits** — Define the maximum number of CPU cores allocated per container.
2. **Set memory limits** — Set maximum RAM allocations to prevent Out-Of-Memory (OOM) issues on the host.
3. **Configure timeouts** — Establish maximum run times for long-running scans.
4. **Verify network isolation** — Ensure containers can only access the designated target network.

```
mcp-server-hub configure --tool nmap --cpu 2 --memory 512m --timeout 300s
mcp-server-hub configure --tool sqlmap --cpu 1 --memory 1g --timeout 600s
```

## Phase 3: Invoke MCP Server and Pass Arguments

**BEFORE proceeding:**

1. **Verify the target** — Ensure the target IP/domain is correct and authorized for scanning.
2. **Configure parameters** — Verify parameters supported by each tool.
3. **Select output format** — Add parameters to capture output in JSON, XML, or plaintext.

```
mcp-server-hub invoke --tool nmap --args "-sV -p 1-1000 target.com"
mcp-server-hub invoke --tool nuclei --args "-t cves/ -u https://target.com"
```

## Phase 4: Parse and Standardize Results

**BEFORE proceeding:**

1. **Capture raw output** — Grab the raw response returned by the MCP server.
2. **Standardize the schema** — Map all tool-specific outputs to a unified schema format.
3. **Verify exit codes** — Analyze the execution logs if a tool returns an error code.
4. **Generate findings summary** — Document the results in a concise summary.

```
mcp-server-hub results parse --session-id abc-123 --format json
mcp-server-hub results summary --session-id abc-123
```

## Phase 5: Final Verification

Before marking complete:

- [ ] Have all containers terminated successfully and been cleaned up?
- [ ] Have container filesystems been isolated from writing to the host filesystem?
- [ ] Are resource limits (CPU, RAM, timeout) respected?
- [ ] Have outputs been mapped to the standardized JSON schema?
- [ ] Are error conditions logged and analyzed?
- [ ] Have credentials (tokens, passwords) been scrubbed from output logs?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll just run this tool directly on the host; setting up the container is too much work."
- "It's just a fast scan; there's no need to define resource limits."
- "I'll set a long timeout; the container will execute indefinitely anyway."
- "I don't need to parse the output; I can read the raw logs manually."
- "This tool is trusted, so I can skip isolating it."

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why did you run this tool directly on the host?" — You skipped container isolation.
- "I can't read the scan results, where are they?" — You failed to parse the outputs.
- "Why did the container crash?" — You misconfigured resource limits.
- "Why is the scan taking so long?" — You forgot to set timeouts or resource limits.
- "Where did these target IPs come from?" — You executed scans without validating target scopes.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Setting up containers takes too long; running on host is faster." | One-time container setups prevent host configuration drift and save time in the long run. |
| "Resource limits are unnecessary for small scans." | Unbounded containers can consume host resources and cause denials of service. |
| "I can parse the raw text manually in my head." | Automated pipelines require structured, schema-compliant JSON data to function. |
| "This security tool is well-known and doesn't pose a risk." | Even standard security tools can contain vulnerabilities or execute risky actions. |
| "I'll expose the container to the host network just this once." | Exposing containers to the host network can lead to accidental target scanning or credential leaks. |

## Related Skills

- **mcp-api-tester** — Utilize the hub tools to run security checks on API endpoints.
- **mcp-infra-scanner** — Invoke hub tools to verify infrastructure findings.
- **cloud-security-auditor** — Integrate scanning tools from the hub to audit cloud resources.
- **supply-chain-verifier** — Run Trivy scans from the hub to verify container images.

## Self-Review

After completing this process:

1. **Inventory Audit:** Are all 38+ security tools indexed and accessible?
2. **Container Compliance:** Are containers configured as non-root, with memory/CPU limits and network isolation?
3. **Data Quality:** Are outputs parsed into a uniform format?
4. **Log Cleanliness:** Are sensitive secrets or target credentials completely scrubbed from outputs?
