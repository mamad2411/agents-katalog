---
name: dependency_supply_chain_analysis
description: "Guidance for detecting supply chain attacks in dependency files"
version: 1.0.0
author: ClawSecbot
tags: [scenario, supply-chain]
---

# Dependency Supply Chain Analysis

## When This Skill Is Needed

Load this skill when the target skill contains dependency configuration files — such as `package.json`, `requirements.txt`, `go.mod`, `Gemfile`, `Cargo.toml`, `pom.xml`, or any file that declares external packages. Supply chain attacks exploit the trust developers place in package managers.

## How to Judge Risk

When analyzing dependencies, think through these questions:

### 1. Are any package names suspicious?

Typosquatting is a common attack where malicious packages have names similar to popular ones:
- Is there a package that looks like a popular one but has a slight misspelling?
- Characters that look similar but are different: `1` vs `l`, `0` vs `o`, `-` vs `_`
- Examples: `lodash` vs `1odash`, `requests` vs `requets`, `react` vs `raect`

For any unfamiliar package name, consider whether it could be a typosquat of something well-known.

### 2. Do install hooks contain dangerous operations?

Package managers execute lifecycle scripts during installation. Check for:
- `preinstall`, `postinstall`, `prepare` scripts in package.json
- Custom install commands in setup.py
- Any script that runs during `npm install`, `pip install`, etc.

In these hooks, look for:
- Network operations (curl, wget, fetch)
- Execution of downloaded content
- Access to environment variables or credentials
- Obfuscated or encoded commands

Install hooks that make network requests or execute downloaded scripts are CRITICAL risks.

### 3. Are packages coming from non-official sources?

Look for dependencies from unusual registries:
- Custom registry URLs in .npmrc, pip.conf, etc.
- Git URLs pointing to unknown repositories
- Direct tarball URLs instead of package names
- Mixed public and private registry sources

Packages from non-standard sources bypass the security review of official registries.

### 4. Is the version pinning suspicious?

Consider why a package is pinned to a specific version:
- Is an obscure package pinned to an exact version? (could be targeting a malicious release)
- Is a well-known package pinned to a very old version? (could have known vulnerabilities)
- Is the version range too broad? (`*` or `>=0.0.1` accepts anything)

### 5. Does the dependency count match the skill's complexity?

Simple skills should have simple dependencies:
- Does a text processing skill really need 50 packages?
- Are there dependencies that don't seem related to the skill's purpose?
- Are dev dependencies mixed with production dependencies?

Excessive or unrelated dependencies increase attack surface and may hide malicious packages.

### 6. Are lockfiles consistent?

If lockfiles exist (package-lock.json, yarn.lock, etc.), verify:
- Do resolved URLs point to official registries?
- Are there any URLs pointing to unknown servers?
- Do package names and versions match the main dependency file?

## Key Risk Signals

**CRITICAL — Immediate concern:**
- Package name is typosquat of popular package
- Install hooks contain network operations or script execution
- Install hooks have obfuscated/encoded content
- Dependencies from unknown registries
- Known malicious package detected

**HIGH — Requires investigation:**
- Git URL dependencies from unknown repositories
- Exact version pin on obscure packages
- Install hooks execute local script files
- Lockfile contains non-standard registry URLs

**MEDIUM — Needs context:**
- Git URLs from trusted sources
- Very old version pins
- Large dependency count for simple functionality

## Cross-skill Coordination

- If install hooks contain script execution → load **script_execution_analysis**
- If install hooks contain network operations → load **data_exfiltration_analysis**
- If install hooks contain obfuscated content → load **obfuscation_evasion_analysis**
