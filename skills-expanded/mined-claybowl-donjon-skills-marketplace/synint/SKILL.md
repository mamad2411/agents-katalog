# SYNINT

Local-first, modular OSINT investigation framework positioned as “stealthy / API-free” with a large agent catalog (46 agents) spanning collection, entity resolution, infrastructure pivoting, media forensics, contradiction detection, lead generation, and structured export. Supports both “run-all concurrently” and staged pipelines (quick / standard / deep), with collection modes like low_noise, balanced, stealth, and deep_browser. Collector engine layer can fall back across bounded HTTP and optional crawl/browser engines; outputs include per-run artifact folders plus export bundles (markdown + JSON/CSV + graphs/timelines/leads).

## Triggers
- "synint"
- "osint investigation framework"
- "local first osint"
- "stealth osint"
- "api free investigation"
- "modular osint"

## Description
SYNINT is a local-first, modular OSINT investigation framework designed for stealthy, API-free operations. It includes a large catalog of 46 specialized agents covering various aspects of intelligence work and supports flexible deployment modes from quick scans to deep investigations.

## Features
- 46 specialized agents covering:
  - Collection
  - Entity resolution
  - Infrastructure pivoting
  - Media forensics
  - Contradiction detection
  - Lead generation
  - Structured export
- Local-first operation (minimal external dependencies)
- API-free capable mode
- Flexible pipeline execution:
  - Run-all concurrently
  - Staged pipelines (quick/standard/deep)
- Collection modes:
  - low_noise
  - balanced
  - stealth
  - deep_browser
- Fallback collector engine (bounded HTTP, crawl/browser)
- Structured output formats:
  - Per-run artifact folders
  - Export bundles (markdown + JSON/CSV + graphs/timelines/leads)

## Usage
Use when you need to conduct OSINT investigations with minimal external dependencies, particularly in environments where stealth or API limitations are concerns.

## Example
```
/synint run quick pipeline on target domain
/synint execute deep investigation with stealth collection
/synint run entity resolution on social media profiles
/synint export findings as markdown bundle
/synint switch to balanced collection mode
```
