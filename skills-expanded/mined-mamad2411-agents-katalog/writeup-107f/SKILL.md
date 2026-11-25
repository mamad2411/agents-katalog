<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-107f
description: CTF writeups and security challenges by 107F.
---

# Writeups by 107F

Source repository: `/repos/107F`

## Repository Index

- bugtrackplus/README.md

## Writeup Content


### File: bugtrackplus/README.md

# BugTrack+  
#### A Coroutine-Based Bug Bounty Logger with CLI, Validation, and Regular Expressions  

**Video Demo**: https://youtu.be/BTLqI3mve8Q  

---

## 📖 Description  
**BugTrack+** is a Python tool designed to simulate logging security vulnerabilities during penetration testing and bug bounty programs. Developed as a final project for Harvard’s [CS50’s Introduction to Programming with Python](https://cs50.harvard.edu/python/), it emphasizes core Python concepts while providing a structured workflow for tracking findings.  

Key highlights:  
- **Coroutine-driven CSV logging** for efficient data streaming.  
- **Strict input validation** using regular expressions and custom exceptions.  
- **Command-line (CLI) and interactive modes** for flexibility.  
- Educational focus on Python’s generators, OOP, and I/O handling.  

---

## 🚀 Getting Started  

### Installation  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/BugTrackPlus.git  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  # Only pytest required  
   ```  

---

## 🛠 Usage  

### Command-Line Interface (CLI)  
Log a bug directly via CLI:  
```bash  
python project.py --log --target example.com --endpoint /login --vuln_type "SQLi" --severity critical  
```  

### Interactive Mode  
Run without arguments to input data interactively:  
```bash  
python project.py  
```  
Follow prompts to enter bug details.  

### Output  
Data is saved to `bugs.csv` with columns:  
- `Timestamp`, `Target`, `Endpoint`, `Vulnerability Type`, `Severity`  

---

## ✨ Features  

### 🌀 Coroutine-Driven Logging  
- Utilizes Python generators (`yield`, `send()`) to keep the CSV file stream open, enabling efficient writes.  
- Logger remains stateful, reducing overhead for frequent entries.  

### 🔍 Input Validation  
- **Target Domain**: Validates format (e.g., `sub.example.com`) using regex.  
- **Severity**: Ensures value is `low`, `medium`, `high`, or `critical`.  
- **Endpoint**: Checks for valid URL path format (e.g., `/login`).  
- Throws `InvalidBugError` for invalid inputs.  

### 📟 CLI & Interactive Modes  
- Supports both quick logging (CLI) and step-by-step input (interactive).  
- Built with `argparse` for robust argument handling.  

### 🧪 Testing  
Run tests with:  
```bash  
pytest test_project.py  
```  
Tests cover:  
- Coroutine functionality  
- Validation rules  
- File I/O operations  

---

## 📂 Project Structure  
```  
BugTrack+  
├── bug.py               # BugReport class (validation logic)  
├── logger.py            # Coroutine logger (CSV writer)  
├── project.py           # CLI entry point  
├── test_project.py      # Unit tests  
├── requirements.txt     # Dependencies (pytest)  
└── README.md  
```  

---

## 🎓 CS50 Concepts Demonstrated  
This project incorporates concepts taught in CS50P:  
- **Generators & Coroutines**: `yield`, `send()`, and streaming data.  
- **OOP**: Classes, properties, and encapsulation.  
- **Error Handling**: Custom exceptions (`InvalidBugError`).  
- **Regex**: Input validation with `re.match`.  
- **File I/O**: CSV writing with `csv.DictWriter`.  
- **CLI**: Argument parsing with `argparse`.  
- **Testing**: Unit tests via `pytest`.  

---

## 🔜 Future Enhancements  
- Export logs to JSON/PDF.  
- Filter logs by severity or domain.  
- Integration with bug bounty platforms (e.g., HackerOne).  
- Interactive dashboard for log analysis.  

---

## 📝 Notes  
- This tool is a **simulation** for educational purposes.  
- Coroutines were chosen to demonstrate Python’s lesser-used features, though higher-level libraries might be preferred in production.  
