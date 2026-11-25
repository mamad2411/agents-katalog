# osint-profiler

Identity matching skill based on the ESRC framework (Extract → Search → Reason → Calibrate), citing “Large-scale online deanonymization with LLMs” (Lermen et al., 2026). Workflow: extract identity signals from social datasets, compress profiles and find candidate matches via FAISS embedding search, then reason about matches requiring 3+ independent markers across categories; hard contradictions veto.

## Triggers
- "osint profiler"
- "identity matching"
- "esrc framework"
- "deanonymization"
- "identity resolution"
- "social media identity"

## Description
An identity matching skill that uses the ESRC framework (Extract → Search → Reason → Calibrate) to resolve online identities across platforms. Based on research in large-scale online deanonymization with LLMs, it extracts signals from social datasets, uses FAISS for similarity matching, and applies reasoning to confirm matches with multiple independent markers.

## Features
- ESRC framework implementation:
  1. Extract: identity signals from social datasets
  2. Search: FAISS embedding search for candidate matches
  3. Reason: require 3+ independent markers across categories
  4. Calibrate: adjust confidence based on evidence quality
- Hard contradiction veto system
- Profile compression for efficient matching
- Multi-platform identity resolution
- Confidence scoring on matches
- Based on Lermen et al. (2026) research

## Usage
Use when you need to determine if multiple online profiles belong to the same person across different platforms or services.

## Example
```
/osint-profiler match-profile twitter:@user1 github:user1
/osint-profiler extract-signals from linkedin.com/in/johndoe
/osint-profiler reason-about match candidates for user123
/osint-profiler calibrate confidence of identity resolution
```
