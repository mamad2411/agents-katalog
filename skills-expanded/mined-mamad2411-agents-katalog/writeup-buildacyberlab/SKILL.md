<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-buildacyberlab
description: CTF writeups and security challenges by BuildaCyberLab.
---

# Writeups by BuildaCyberLab

Source repository: `/repos/BuildaCyberLab`

## Repository Index

- recon_tool/README.md

## Writeup Content


### File: recon_tool/README.md

# Bounty Recon Tool

## 🔥 Automated Bug Bounty Reconnaissance

Bounty Recon Tool is a powerful automated reconnaissance script for bug bounty hunters, security researchers, and penetration testers. It automates subdomain enumeration, live subdomain filtering, directory fuzzing, and endpoint discovery while generating reports in Markdown, HTML, and PDF formats.

## 📌 Features
- **Subdomain Enumeration** using `subfinder`
- **Live Subdomain Filtering** using `httpx`
- **Directory Fuzzing** using `ffuf`
- **Exposed Endpoints Discovery** using `waybackurls` and `gau`
- **Exploit Suggestions** based on common endpoint keywords
- **Beautiful Markdown Reports** with automated HTML & PDF conversion
- **Loading Animations with Inspirational Quotes** for an engaging experience

## 🚀 Installation

### Prerequisites
Ensure you have the following installed:
- Linux-based OS (Ubuntu/Kali/BlackArch recommended)
- `subfinder`
- `httpx`
- `ffuf`
- `waybackurls`
- `gau`
- `aha` (for HTML conversion)
- `wkhtmltopdf` (for PDF conversion)

Install dependencies:
```bash
sudo apt update && sudo apt install -y subfinder httpx ffuf aha wkhtmltopdf
```
For `waybackurls` and `gau`, install via `go`:
```bash
go install github.com/tomnomnom/waybackurls@latest
go install github.com/lc/gau@latest
```
Add Go binaries to PATH:
```bash
export PATH=$HOME/go/bin:$PATH
```

## 📂 Setup
Clone the repository and navigate into it:
```bash
git clone https://github.com/yourusername/recon_tool.git
cd recon_tool
bash recon_tool.sh
```

## 🔥 Usage
Run the script with a target domain:
```bash
bash recon_tool.sh example.com
```

## 📜 Output
All reports will be saved in `~/bounty_recon_tool/reports/` as:
- **Markdown**: `example.com_report.md`
- **HTML**: `example.com_report.html`
- **PDF**: `example.com_report.pdf`

![image](https://github.com/user-attachments/assets/b7c34850-7806-4b1d-8ecd-58551beaa3d5)

## 🤝 Contributions
Feel free to contribute! Fork the repo, make your changes, and submit a pull request.

## 📜 License
MIT License. Free to use and modify.

## 🌟 Acknowledgments
Inspired by the pursuit of knowledge and the wisdom of the cosmos.



