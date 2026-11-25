# OnionClaw

OpenClaw skill + standalone CLI that provides AI agents Tor/.onion access and a full dark-web OSINT toolkit “in one folder.” Built on the SICRY engine; supports searching across 18 dark web search engines, fetching pages through Tor, and optionally running LLM analysis in multiple modes. Exposes seven core commands (Tor check, identity/circuit renewal, engine health check, multi-engine search, Tor fetch, LLM analysis, and a one-shot “pipeline” that does refine → search → filter → scrape → analyze).

## Triggers
- "onionclaw"
- "dark web osint"
- "tor access"
- ".onion search"
- "darkweb investigation"
- "sicry engine"

## Description
OnionClaw provides AI agents with secure access to the Tor network and dark web for OSINT investigations. It combines the SICRY engine with Tor capabilities to enable searching across multiple dark web search engines, fetching content through Tor, and performing LLM analysis on gathered information.

## Features
- Tor/.onion network access for AI agents
- SICRY search engine foundation
- Search across 18 dark web search engines
- Fetch web pages through Tor network
- Multiple LLM analysis modes
- Seven core commands:
  1. Tor check
  2. Identity/circuit renewal
  3. Engine health check
  4. Multi-engine search
  5. Tor fetch
  6. LLM analysis
  7. One-shot pipeline (refine → search → filter → scrape → analyze)
- Explicit dual-use warnings in documentation
- Can become an “operation loop” if repurposed

## Usage
Use when you need to conduct OSINT investigations on the dark web or Tor network while maintaining operational security.

## Example
```
/onionclaw check-tor-status
/onionclaw renew-identity-circuit
/onionclaw search-darkweb for leaked credentials
/onionclaw fetch-onion-page http://example.onion/page
/onionclaw run-pipeline on ransomware threat actors
```
