---
name: cybersecurity-hub
description: Routes cybersecurity questions to the most relevant specialized skill from the Anthropic-Cybersecurity-Skills catalog and loads that skill's instructions on demand. Use for defensive security, incident response, forensics, malware analysis, threat hunting, cloud security, application security, authorized penetration testing, compliance, and related cybersecurity tasks.
---

# Cybersecurity Skill Hub

## Purpose

This skill is a lightweight router for a large external cybersecurity skill catalog. Do not try to memorize or enumerate the whole catalog. Load only the specialized skill needed for the current request.

## Instructions

When the user asks a cybersecurity question:

1. Call the `run_js` tool using `index.html`.
2. Pass `data` as a JSON string with:
   - `query`: String. The user's cybersecurity request, preserving important technical terms.
   - `top_k`: Number. Usually `1`; use up to `3` only when the request clearly spans multiple cybersecurity specialties.
   - `max_chars`: Number. Usually `18000`.
3. Read the JSON returned by the tool.
4. If `result.loaded_skills` contains one or more skills, treat each returned `instructions` field as specialized task guidance for this turn.
5. Answer the user's original request using that specialized guidance, while respecting the actual capabilities of the mobile environment.
6. Never claim that a command, binary, scanner, exploit framework, forensic utility, or desktop tool was executed unless it really was available and executed through an actual tool.
7. If the loaded skill tells you to use a tool that is unavailable on the phone, explain the command or workflow the user can run in an authorized environment instead of pretending to execute it.
8. Use offensive or intrusive procedures only for systems, applications, networks, devices, accounts, and data the user owns or is explicitly authorized to assess.

### Exact skill loading

If the user explicitly names an upstream skill, call `run_js` with:

- script name: `index.html`
- data: a JSON string containing:
  - `skill`: String. Exact upstream skill name.
  - `max_chars`: Number. Usually `18000`.

### Search-only mode

If the user asks what skills are available for a topic rather than asking to perform the task, call `run_js` with:

- `query`: String
- `top_k`: Number from 3 to 10
- `search_only`: true

Then summarize the returned matches without loading their full instructions.

## Notes

The catalog is fetched dynamically from the public repository `mukul975/Anthropic-Cybersecurity-Skills`. Network access is required for first use and for fetching skill content.
