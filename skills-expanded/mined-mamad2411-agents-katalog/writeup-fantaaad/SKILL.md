<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-fantaaad
description: CTF writeups and security challenges by Fantaaad.
---

# Writeups by Fantaaad

Source repository: `/repos/Fantaaad`

## Repository Index

- HackTheBox-Progress-Tracker-Kali/README.md

## Writeup Content


### File: HackTheBox-Progress-Tracker-Kali/README.md

# HackTheBox Progress Tracker (Kali Linux)

A practical tool to organize your HackTheBox workflow on Kali Linux, allowing you to document, track, and visualize your pentesting practice efficiently.

## Features
- Creates organized folders for each solved machine.
- Runs `nmap` scans automatically.
- Generates Markdown report templates.
- Tracks progress in a CSV file.
- Generates progress graphs.
- Simple CLI usage for daily practice.

## Requirements
- Kali Linux (or any Linux with `bash`, `python3`, `nmap`).
- Python with `matplotlib`:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip nmap -y
  pip3 install matplotlib
  ```

## Installation
Clone the repository:
```bash
git clone https://github.com/fanchote/HackTheBox-Progress-Tracker-Kali.git
cd HackTheBox-Progress-Tracker-Kali
chmod +x track_machine.sh
```

## Usage
After solving an HTB machine, log it automatically:
```bash
./track_machine.sh <IP> <MachineName> <Points> <Difficulty>
```
Example:
```bash
./track_machine.sh 10.10.10.10 Arctic 20 Easy
```

This will:
- Create `~/HTB/MachineName`.
- Run `nmap` and save the output.
- Generate a Markdown report.
- Update your CSV progress.
- Generate your progress graph automatically.

## Viewing Progress
Your progress graph will be saved as:
```
~/HTB/htb_progress.png
```
To open it:
```bash
xdg-open ~/HTB/htb_progress.png
```

## Folder Structure
- `~/HTB/<MachineName>/`: Stores the scan, report, and notes.
- `htb_progress.csv`: Logs your completed machines.
- `htb_progress.png`: Shows your accumulated points visually.

## License
MIT License.

## Contributing
This is for personal learning and structuring HTB practice. Feel free to fork and adapt for your workflow.

**Showcase your growth and structured learning on your GitHub and CV while actively improving your pentesting skills on Kali Linux.**


