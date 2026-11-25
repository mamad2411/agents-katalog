---
name: Supply Chain Attack Analyst
description: Analyze software supply chain attacks across package registries (npm, PyPI, RubyGems), CI/CD pipelines (GitHub Actions, GitLab CI), and container ecosystems. Includes detection engineering patterns for Splunk, Sentinel, Elastic, and Sigma.
---

# Supply Chain Attack Analyst Skill

## Configuration

- `$SIEM_PLATFORM` - Target SIEM for detection output: `splunk`, `sentinel`, `elastic`, `sigma`
- `$SECURITY_CONTENT_PATH` - Path to detection content repository

## Overview

Software supply chain attacks compromise the tools, dependencies, and pipelines that developers trust. This skill covers analysis and detection across the major attack surfaces: package registries, CI/CD systems, container images, and code repositories.

## Attack Surface Taxonomy

### 1. Package Registry Attacks

| Vector | Description | Examples |
|--------|-------------|---------|
| **Typosquatting** | Packages with names similar to popular ones | `colourama` vs `colorama`, `noblox.js-proxy` |
| **Dependency confusion** | Public package name matches private internal name | Alex Birsan's 2021 research |
| **Account takeover** | Compromised maintainer credentials | `ua-parser-js`, `coa`, `rc` (2021) |
| **Malicious update** | Legitimate package ships malicious version | `event-stream` (2018), `colors.js` (2022) |
| **Install script abuse** | `preinstall`/`postinstall` hooks run arbitrary code | Common npm attack vector |
| **Starjacking** | Fake GitHub stars/URLs to build false trust | Ongoing across npm/PyPI |

### 2. CI/CD Pipeline Attacks

| Vector | Description | Examples |
|--------|-------------|---------|
| **Poisoned GitHub Action** | Malicious or compromised Action in workflow | `tj-actions/changed-files` (2025) |
| **Workflow injection** | Untrusted input in `run:` blocks | `${{ github.event.issue.title }}` |
| **Secret exfiltration** | CI job leaks secrets to attacker | Via compromised deps or Actions |
| **Build artifact tampering** | Modify artifacts between build and publish | SolarWinds SUNBURST pattern |
| **Self-hosted runner abuse** | Compromise persistent CI runners | Shared runners, credential theft |

### 3. Container & Image Attacks

| Vector | Description | Examples |
|--------|-------------|---------|
| **Malicious base image** | Trojanized images on Docker Hub | Cryptomining images |
| **Image tag mutation** | Tag `latest` or `v1` points to new malicious image | Tag vs digest trust |
| **Build layer injection** | Malicious layer added during multi-stage build | Dockerfile manipulation |
| **Registry compromise** | Container registry itself is compromised | CodeCov breach (2021) |

## Real-World Campaign Analysis Framework

When analyzing a supply chain incident, follow this structure:

### Phase 1: Initial Triage

1. **What was compromised?** — Package name, version range, registry
2. **What was the payload?** — Data exfiltration, backdoor, cryptominer, ransomware
3. **What was the delivery mechanism?** — Install script, import hook, build step
4. **What was the blast radius?** — Download count, dependent packages, time window

### Phase 2: Technical Analysis

1. **Payload extraction** — Deobfuscate and analyze malicious code
2. **C2 identification** — Network indicators (domains, IPs, protocols)
3. **Persistence mechanisms** — Does the payload survive package removal?
4. **Lateral movement** — Does it spread to other packages, repos, or systems?

### Phase 3: Detection Opportunities

Map findings to detectable behaviors:

| Behavior | Data Source | Detection Approach |
|----------|------------|-------------------|
| Unexpected network calls from package install | DNS / proxy logs | Alert on install-time DNS to uncommon domains |
| Environment variable harvesting | Process telemetry | Monitor `env` / `printenv` in CI context |
| File writes outside package directory | File integrity monitoring | Sysmon EventID 11 / auditd |
| Encoded/obfuscated payloads | Static analysis | Entropy analysis, known obfuscation patterns |
| Git credential access | Audit logs | Monitor `.git-credentials`, `~/.ssh/` access |

## Detection Engineering Framework

### npm / Node.js

**Install script monitoring:**

```sigma
title: Suspicious npm Install Script Execution
logsource:
    category: process_creation
    product: linux
detection:
    selection:
        ParentCommandLine|contains:
            - 'npm install'
            - 'npm ci'
            - 'yarn install'
        CommandLine|contains:
            - 'curl '
            - 'wget '
            - '/dev/tcp/'
            - 'base64 -d'
            - 'python -c'
    condition: selection
level: high
```

**Key indicators:**
- `preinstall` / `postinstall` scripts spawning network tools
- `eval()` or `Function()` constructors in package code
- Dynamic `require()` with encoded strings
- Access to `process.env` collecting CI secrets
- DNS lookups during `npm install` to non-registry domains

### PyPI / Python

**Key indicators:**
- `setup.py` with `cmdclass` overrides executing code at install time
- `__init__.py` with obfuscated imports
- Use of `exec()`, `eval()`, `compile()` with encoded payloads
- `subprocess.Popen` or `os.system` calls in library code
- Typosquat names close to popular packages (e.g., `reqeusts`)

**Detection approach:**

```sigma
title: Suspicious Python Package Install Behavior
logsource:
    category: process_creation
    product: linux
detection:
    selection:
        ParentCommandLine|contains:
            - 'pip install'
            - 'pip3 install'
            - 'python setup.py'
        CommandLine|contains:
            - 'curl '
            - 'wget '
            - '/bin/sh -c'
            - 'base64'
    condition: selection
level: high
```

### GitHub Actions

**Workflow injection detection:**

Look for untrusted input flowing into `run:` blocks:

```yaml
# VULNERABLE — attacker-controlled title goes into shell
- run: echo "Issue: ${{ github.event.issue.title }}"

# SAFE — use environment variable
- run: echo "Issue: $ISSUE_TITLE"
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
```

**Key indicators:**
- Actions using `actions/checkout` with `persist-credentials: true` on PRs from forks
- Workflow triggers on `pull_request_target` with code checkout
- `GITHUB_TOKEN` with write permissions in fork-triggered workflows
- Third-party Actions pinned to branch (`@main`) instead of SHA (`@a1b2c3d`)
- Self-hosted runners used for public repo workflows

### Container Supply Chain

**Key indicators:**
- Images pulled by tag instead of digest (`nginx:latest` vs `nginx@sha256:abc...`)
- Multi-stage builds with unpinned base images
- `RUN curl ... | sh` patterns in Dockerfiles
- Images from unofficial registries or unverified publishers

## MITRE ATT&CK Mappings

| Technique | Supply Chain Relevance |
|-----------|----------------------|
| T1195.001 | Supply Chain Compromise: Compromised Software Dependencies |
| T1195.002 | Supply Chain Compromise: Compromised Software Supply Chain |
| T1059.006 | Command and Scripting: Python (PyPI attacks) |
| T1059.007 | Command and Scripting: JavaScript (npm attacks) |
| T1204.002 | User Execution: Malicious File |
| T1036.005 | Masquerading: Match Legitimate Name (typosquatting) |
| T1588.001 | Obtain Capabilities: Malware (repackaged legit tools) |

## Investigation Checklist

When a suspected supply chain compromise is reported:

- [ ] Identify affected package name, version(s), and registry
- [ ] Determine download count / install window
- [ ] Extract and deobfuscate payload
- [ ] Identify C2 infrastructure (domains, IPs)
- [ ] Check if payload persists after package removal
- [ ] Enumerate dependent packages (transitive dependencies)
- [ ] Search for similar typosquat variants still active
- [ ] Check if maintainer account was compromised vs new account
- [ ] File registry takedown request (npm: `npm unpublish`, PyPI: admin report)
- [ ] Create IOC-based detections for immediate response
- [ ] Create behavioral detections for long-term coverage
- [ ] Update package lockfiles across affected projects
- [ ] Audit CI/CD pipelines for exposed secrets during compromise window

## Prevention Recommendations

| Control | Implementation |
|---------|---------------|
| **Lockfiles** | Always commit `package-lock.json` / `poetry.lock` / `Gemfile.lock` |
| **Pin Actions by SHA** | `uses: actions/checkout@a1b2c3d` not `@v4` |
| **Pin images by digest** | `FROM nginx@sha256:abc123` not `FROM nginx:latest` |
| **Scope npm tokens** | Use granular, read-only tokens; enable 2FA for publish |
| **Private registry proxy** | Artifactory/Nexus as intermediary; block direct public access |
| **SLSA/Sigstore** | Verify build provenance and artifact signatures |
| **Dependency review** | GitHub Dependency Review Action, Socket.dev, Snyk |
| **Minimal CI permissions** | `permissions: read-all` default; grant write explicitly |

## Adapting Detections to Your SIEM

The Sigma rules above are platform-agnostic. Convert to your target SIEM:

```bash
# Splunk
sigma convert -t splunk -p sysmon rule.yml

# Sentinel / KQL
sigma convert -t microsoft365defender rule.yml

# Elastic
sigma convert -t elasticsearch rule.yml
```

For SIEM-native rules, adapt the detection logic using the appropriate field schema:
- **Splunk CIM:** `process_name`, `parent_process_name`, `process`
- **Elastic ECS:** `process.name`, `process.parent.name`, `process.command_line`
- **Sentinel MDE:** `FileName`, `InitiatingProcessFileName`, `ProcessCommandLine`

## Resources

- [SLSA Framework](https://slsa.dev/) — Supply chain Levels for Software Artifacts
- [OpenSSF Scorecard](https://securityscorecards.dev/) — Automated security health checks for OSS
- [Socket.dev](https://socket.dev/) — Package supply chain security
- [Sigstore](https://sigstore.dev/) — Keyless signing and verification
- [CISA Supply Chain Security](https://www.cisa.gov/supply-chain) — Government guidance
