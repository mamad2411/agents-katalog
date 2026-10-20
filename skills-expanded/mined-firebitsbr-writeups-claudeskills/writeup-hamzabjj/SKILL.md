<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hamzabjj
description: CTF writeups and security challenges by Hamzabjj.
---

# Writeups by Hamzabjj

Source repository: `/repos/Hamzabjj`

## Repository Index

- network_pentester/README.md
- network_pentester/SETUP.md

## Writeup Content


### File: network_pentester/README.md

# Pentesting Automation Framework

A Python framework for safely executing pentesting playbooks, validating IP addresses, and generating educational HTML reports.

## Features

- ✅ **IP Validation**: Ensures only private IPs and lab networks (HTB/THM) are targeted
- ✅ **Playbook Loading**: Loads and validates YAML playbooks with structured steps
- ✅ **Safe Command Execution**: Executes commands with validation, timeout, and output capture
- ✅ **HTML Reports**: Generates beautiful, educational reports with explanations per step
- ✅ **Security**: Blocks dangerous commands and validates all inputs

## Installation

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
pentesting_framework/
├── ip_validator.py          # IP address validation module
├── playbook_loader.py       # YAML playbook loader and validator
├── command_executor.py      # Safe command execution module
├── report_generator.py      # HTML report generator
├── main.py                  # Main entry point
├── playbooks/               # YAML playbook files
├── reports/                 # Generated HTML reports
└── requirements.txt         # Python dependencies
```

## Usage

### Basic Usage

```bash
python main.py playbooks/example_playbook.yaml
```

You will be prompted to enter the target IP (lab/private only). Or pass it directly:

```bash
python main.py playbooks/example_playbook.yaml --target 192.168.1.1
```

### Options

```bash
python main.py playbooks/example_playbook.yaml \
    --target 10.10.10.5 \
    --timeout 60 \
    --output-dir reports \
    --no-ip-validation  # Not recommended!
```

### Skip Execution (Test Playbook Structure)

```bash
python main.py playbooks/example_playbook.yaml --skip-execution
```

## Playbook Format

Playbooks are YAML files with the following structure:

```yaml
name: Network Enumeration Playbook
description: A sample playbook for network enumeration
version: 1.0.0
author: Security Team

steps:
  - name: Initial Port Scan
    action: nmap -p 1-1000 {{target}}
    description: Perform initial port scan on target
    timeout: 60
    
  - name: Service Detection
    action: nmap -sV -p 80,443,22 {{target}}
    description: Detect services running on common ports
```

Use `{{target}}` in actions; it is replaced at runtime with the IP you enter (must be private/lab only).

### Required Fields

- `name`: Playbook name (string)
- `steps`: List of step objects

### Step Fields

- `name`: Step name (required, string)
- `action`: Command to execute (required, string)
- `description`: Optional step description
- `timeout`: Optional execution timeout in seconds

## Modules

### IP Validator (`ip_validator.py`)

Validates IP addresses against private ranges and known lab networks:

```python
from ip_validator import IPValidator, validate_ip

# Validate an IP
try:
    validate_ip("10.10.10.5")
    print("IP is valid")
except InvalidIPException as e:
    print(f"Invalid IP: {e}")
```

### Playbook Loader (`playbook_loader.py`)

Loads and validates YAML playbooks:

```python
from playbook_loader import PlaybookLoader

loader = PlaybookLoader("playbook.yaml")
for step in loader:
    print(f"Step: {step['name']}")
```

### Command Executor (`command_executor.py`)

Safely executes commands:

```python
from command_executor import CommandExecutor

executor = CommandExecutor(validate_ips=True, timeout=30)
result = executor.execute("ping -c 4 10.10.10.5")
print(f"Success: {result.success}")
print(f"Output: {result.stdout}")
```

### Report Generator (`report_generator.py`)

Generates HTML reports:

```python
from report_generator import ReportGenerator

generator = ReportGenerator(output_dir="reports")
report_path = generator.generate_report(
    playbook_name="My Playbook",
    steps=steps,
    results=results,
    metadata={"author": "Security Team"}
)
```

## Security Features

- **IP Validation**: Only allows private IPs (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) and lab networks
- **Command Blocking**: Blocks dangerous commands (rm, del, format, etc.)
- **Timeout Protection**: Prevents commands from running indefinitely
- **Safe Execution**: Uses subprocess with shell=False by default

## Educational Reports

Reports include:

- 📊 Summary statistics (total steps, success/failure counts, execution time)
- 📚 Educational explanations for each step
- 🔍 Command output (stdout/stderr) with syntax highlighting
- ✅ Success/failure status for each step
- 📝 Detailed execution metadata

## Example Playbook

See `playbooks/example_playbook.yaml` for a complete example.

## Requirements

- Python 3.7+
- pyyaml

## License

This project is for educational purposes only. Use responsibly and only on systems you own or have explicit permission to test.

## Disclaimer

This framework is designed by Benjee for educational purposes and authorized security testing only. Always ensure you have proper authorization before testing any system. The authors are not responsible for misuse of this tool.



### File: network_pentester/SETUP.md

# Setup Complete! 🎉

Your Pentesting Automation Framework is ready to use!

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test suite:**
   ```bash
   python test_framework.py
   ```

3. **Execute a playbook:**
   ```bash
   python main.py playbooks/example_playbook.yaml
   ```

## Project Structure

```
pentesting_framework/
├── ip_validator.py          # IP address validation
├── playbook_loader.py       # YAML playbook loader
├── command_executor.py      # Safe command execution
├── report_generator.py      # HTML report generator
├── main.py                  # Main entry point
├── test_framework.py        # Test suite
├── playbooks/               # YAML playbook files
│   └── example_playbook.yaml
├── reports/                 # Generated HTML reports
├── requirements.txt         # Dependencies
├── README.md               # Full documentation
└── .gitignore              # Git ignore file
```

## Features Implemented

✅ **Step 1**: IP Validator Module
- Validates private IP ranges (RFC 1918)
- Validates HTB/THM lab networks
- Raises exceptions for invalid IPs

✅ **Step 2**: Playbook Loader
- Loads YAML playbooks
- Validates structure
- Exposes steps sequentially

✅ **Step 3**: Command Executor
- Safely executes external commands
- Captures stdout/stderr
- Returns structured results

✅ **Step 4**: Report Generator
- Generates structured HTML reports
- Includes educational explanations per step
- Beautiful, interactive interface

## Next Steps

1. Customize playbooks in `playbooks/` directory
2. Run playbooks and view reports in `reports/` directory
3. Extend the framework with additional modules as needed

## Git Commit (Optional)

If you have git installed, you can commit the project:

```bash
git add .
git commit -m "Initial commit: Pentesting Automation Framework"
```

## Notes

- All modules are tested and working
- Reports are generated with educational content
- IP validation ensures only safe targets are used
- Commands are executed safely with validation

Enjoy using the framework! 🚀

