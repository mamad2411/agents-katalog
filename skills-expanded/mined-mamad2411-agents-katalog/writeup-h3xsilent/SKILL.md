<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-h3xsilent
description: CTF writeups and security challenges by H3XSILENT.
---

# Writeups by H3XSILENT

Source repository: `/repos/H3XSILENT`

## Repository Index

- observatory/README.md
- observatory/04-Scans/README.md

## Writeup Content


### File: observatory/04-Scans/README.md

# rvuln – Reconnaissance & Vulnerability Automation Framework

rvuln is a modular reconnaissance and vulnerability scanning framework designed for offensive security research, bug bounty workflows, and red‑team automation.

Built with a professional pipeline mindset: **recon → crawl → parameter mining → scanning**.

---

## Features

- Subdomain enumeration (Subfinder, Findomain)  
- Live host resolution (httpx)  
- URL crawling (GAU, Hakrawler)  
- Parameter extraction and reflection‑parameter detection (Gxss)  
- Fragment (`#`) harvesting for DOM‑based attack surface  
- Technology fingerprinting (httpx)  
- HTTP status intelligence report  
- Modular scanning pipeline (Nuclei, Dalfox, Subjack, SQLMap)  
- Stealth mode with configurable delays  
- Modular architecture (easy to extend and adapt)

---

## Philosophy

rvuln is **not a one‑click auto‑pwn script**.

It follows a professional bug‑bounty methodology:

1. Passive reconnaissance  
2. Surface mapping  
3. Target filtering  
4. Controlled active scanning  

**Signal > noise.** Automation supports thinking; it does not replace it.

---

## Directory Structure

```text
rvuln/
├── main.sh        # Entry point
├── config.sh      # Global configuration
├── utils.sh       # Logging and helper functions
├── recon.sh       # Subdomain discovery and host resolution
├── crawl.sh       # URL discovery and crawling
├── params.sh      # Parameter and fragment extraction
├── scan.sh        # Technology detection and vulnerability scanners
└── data/          # Output directory
```

---

## Requirements

Install the following tools:

- subfinder  
- findomain  
- httpx  
- gau  
- hakrawler  
- gxss  
- nuclei  
- dalfox  
- subjack  
- sqlmap  

Recommended:

- Seclists  

---

## Installation

```bash
git clone https://github.com/HexSilent/rvuln.git
cd rvuln
chmod +x *.sh
```

### Usage

**Standard Recon Mode (Safe)**

```bash
./main.sh example.com
```

**Aggressive Mode (Active Scanners)**

```bash
./main.sh example.com --aggressive
```

> **Warning:** Aggressive mode may trigger WAFs, rate limits, or violate scope policies.

---

## Output Structure

```text
data/
├── recon/
│   ├── subs.txt
│   ├── resolv.txt
├── crawl/
│   ├── urls.txt
├── params/
│   ├── parameters.txt
│   ├── reflected.txt
│   ├── fragments.txt
├── scan/
│   ├── tech.json
│   ├── status.txt
│   ├── nuclei.txt
│   ├── xss.txt
│   ├── sqlmap.txt
│   ├── takeover.txt
```

---

## Configuration

Edit `config.sh` to tune:

- Threads  
- Timeout  
- Delay (stealth mode)  
- Nuclei template path  
- User‑Agent list  

---

## Legal & Ethical Disclaimer

This tool is intended **exclusively for educational purposes and authorized security testing**.

You must:

- Have explicit permission to test the target  
- Respect bug‑bounty program scope and rules  
- Follow applicable local laws and regulations  

The author assumes **no responsibility** for misuse or unauthorized testing.

---

## Roadmap

- SQLite backend for recon history  
- Recon diff detection (new assets alert)  
- Proxy rotation and WAF‑adaptive rate control  
- TUI interface (ncurses)  
- JSON consolidated report export  
- Dockerized deployment  

---

## Author

HexSilent  
Offensive Security Researcher | Bug Bounty Hunter | Cyberpunk‑oriented engineer  

---

## Final Note

Automation makes you faster. Critical thinking makes you dangerous.



### File: observatory/README.md

# Observatory  
Mapping attack surface with rigor, clarity, and methodology.

This repository gathers an organized collection of studies, techniques, and processes used in bug bounty and offensive security, with focus on two areas that usually receive superficial attention:

1. Reconnaissance — the process of understanding the real structure of a target.  
2. Reporting — the art of communicating vulnerabilities in a professional and verifiable way.

The goal is not to compile tool lists or ready‑made exploits.  
It is to document **how to think**, **how to map**, and **how to analyze** — elements that truly differentiate a competent hunter from someone who only repeats tutorials.

---

## Repository Structure

```
/01-Recon/
  mentalidade.md
  recon-passivo.md
  recon-ativo.md
  automacao.md
  checklist.md

/02-Vulnerabilidades/
  sqli.md
  ssrf.md
  xss.md
  idor.md
  auth-bypass.md
  misconfig.md
  lfi-rfi.md

/03-Relatorios/
  metodologia.md
  templates.md
  melhores-praticas.md
  exemplos.md
  erros-comuns.md

/04-Scans/
  metodologia-scans.md
  pipelines.md
  ferramentas.md
  interpretacao-resultados.md

README.md
LICENSE
```

Each section is written to be clear, deep, and practical — without noise and without artificial complexity.

---

## Project Philosophy

**Depth over aesthetics.  
Clarity over complexity.  
Methodology over tools.**

This material is intended for those who want to:

- understand how a target actually works;  
- learn to find weak signals that go unnoticed;  
- structure investigations in a consistent way;  
- produce reports that are reproducible, professional, and complete.

---

## Target Audience

Ideal for:

- Beginners seeking clear direction;  
- Intermediate hunters who want to improve quality and speed;  
- Professionals who need a solid recon foundation;  
- Anyone who values reasoning over checklists.

---

## License

This project is licensed under **Creative Commons BY-SA 4.0**.  
Contributions and forks are welcome.  
Derivative works must retain the same license.

---

## Contributing

Pull requests are accepted as long as they follow:

- clarity  
- technical rigor  
- verifiability  

Opinionated or superficial content will not be merged.

