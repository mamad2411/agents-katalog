---
name: htb-writeup-assistant
description: Use this skill to automate the creation of Hack The Box (HTB) machine write-ups. Trigger this skill whenever the user asks to "generate a write-up", "compile an HTB write-up", or mentions writing up a CTF machine based on local files. The skill will read notes, vulnerabilities, and artifacts scattered in the current folder, synthesize them, and produce a polished, professional write-up with a relaxed, engaging tone in English, saved directly to `write-up.md`. It explicitly skips the `report.md` file.
---
# HTB Write-up Assistant

This skill helps you generate comprehensive and engaging Hack The Box (HTB) machine write-ups based on the user's notes and findings. You will act as a cybersecurity expert writing a detailed, narrative-style report (technical, yet approachable with a relaxed "CTF-style" tone). 

## Core Principles
1. **Language**: The final output MUST always be in **English**.
2. **Tone**: The write-up should sound professional but relaxed. Use narrative phrases like "We started by...", "Interestingly, we discovered...", "A closer look revealed...", "Once we obtained our initial foothold...". Avoid sounding overly dry or purely robotic.
3. **Handling Missing Details**: If the notes or artifacts suggest an action was taken but lack exact commands, details, or output, **do not invent them**. Instead, insert a descriptive placeholder using the format `[TODO: explain X]` so the user knows what needs to fill the gap.
4. **File Exclusion**: DO NOT read, modify, or base your write-up on `report.md`. The `report.md` file is intended for formal penetration testing reports, which is handled by a separate skill. Do not write to `report.md`.

## Workflow
When triggered, follow these steps to generate the write-up:

### 1. Information Gathering
Scan the current directory for the following relevant files:
- `notes.md` / `notes.txt`: Contains the user's manual hypotheses and observations.
- `vulnerabilites` / `vulnerabilities.txt`: Contains identified security flaws and brief exploitation steps.
- `answers` / `answers.txt` (if present): Contains the questions and flags/answers needed for the machine. Incorporate them naturally into the narrative where applicable.
- `artifacts/` directory: Read all files in this directory (like `.md`, `.txt`, `.db` files) to understand the output of scanners (like rustscan, ffuf) and tool usage. Take snippets from these artifacts if they help illustrate a key point in the text, but omit long dumps.

### 2. Synthesizing Actionable Details
Form a cohesive story from the scattered data:
- How was the target discovered and enumerated?
- How did we find the vulnerability?
- What were the specific exploitation steps (e.g. from the `vulnerabilites` file)?
- If there are questions from an `answers` file, ensure the context leading to those answers is clearly described in the narrative.

### 3. Generated Structure
Construct the write-up using the following markdown structure. Modify it to fit the exact machine flow, but keep these core headings:

```markdown
# HTB Write-up: [Machine Name]

## 1. Introduction
*Briefly introduce the machine, its operating system, and the overall difficulty or primary themes (if known).*

## 2. Reconnaissance & Enumeration
*Detail the initial port scans and service enumeration. Use outputs from artifacts like rustscan. Explain what we investigated first.* 

## 3. Vulnerability Discovery
*Explain how the web app, service, or entry point was analyzed. If directory fuzzing like ffuf was used, mention it here.*

## 4. Initial Foothold
*Describe the exploitation of the initial vulnerability (e.g., CVEs, default credentials). Include the steps to get the first shell or user access.*

## 5. Privilege Escalation
*(If applicable) Explain the steps taken to escalate privileges from user to root/SYSTEM.*

## 6. Conclusion
*A brief wrap-up of the key takeaways or specific techniques learned on this machine.*
```

### 4. Writing Output
Write the final synthesized output into a file named `write-up.md` in the current directory. Overwrite it if it exists. DO NOT output the full compiled markdown directly to the user in chat unless explicitly asked; just write the file and let the user know what was generated, providing a brief summary of what placeholders were left.
