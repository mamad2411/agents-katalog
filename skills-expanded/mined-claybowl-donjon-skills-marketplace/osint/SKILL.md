# osint-skill

OSINT “dossier” skill aimed at going from a name/handle to a structured report using a phased pipeline. Includes six research phases: Seed Collection → Platform Extraction → Cross-Reference → Psychoprofile → Completeness Check → Dossier Output. Explicitly includes psychographic profiling (MBTI/Big Five / comms style) and confidence grading on verified facts (A/B/C/D).

## Triggers
- "osint dossier"
- "create intelligence report"
- "person investigation"
- "handle to dossier"
- "name research"
- "social media investigation"

## Description
An OSINT skill that transforms a name or handle into a structured intelligence dossier through a six-phase pipeline. The skill includes psychographic profiling capabilities and confidence grading for verified facts, making it suitable for professional intelligence work.

## Features
- Six-phase research pipeline:
  1. Seed Collection
  2. Platform Extraction
  3. Cross-Reference
  4. Psychoprofile (MBTI/Big Five/communications style)
  5. Completeness Check
  6. Dossier Output
- Psychographic profiling capabilities
- Confidence grading on verified facts (A/B/C/D scale)
- Broad tool coverage (Apify actors + multiple search APIs)
- Optional “swarm mode” for parallel sub-agent processing
- Structured, actionable intelligence output

## Usage
Use when you need to gather comprehensive intelligence on an individual or entity starting from minimal information like a name, username, or handle.

## Example
```
/osint-skill investigate @johndoe123
/osint-skill create dossier for elonmusk
/osint-skill run psychoprofile on vitalik-buterin
/osint-skill swarm-mode investigation of satoshinakamoto
```
