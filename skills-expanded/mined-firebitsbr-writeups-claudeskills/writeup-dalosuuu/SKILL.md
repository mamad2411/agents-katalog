<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dalosuuu
description: CTF writeups and security challenges by Dalosuuu.
---

# Writeups by Dalosuuu

Source repository: `/repos/Dalosuuu`

## Repository Index

- IDOR-CrawlerScanSuite/README.md
- IDOR-CrawlerScanSuite/demo/README.md
- IDOR-CrawlerScanSuite/docs/CONFIG.md

## Writeup Content


### File: IDOR-CrawlerScanSuite/README.md

# IDOR Vulnerability Scanner

A comprehensive, modular tool for discovering **Insecure Direct Object Reference (IDOR)** vulnerabilities in web applications. Designed for security professionals and bug bounty hunters.

## Overview

IDOR vulnerabilities occur when applications expose direct references to internal objects (like database keys, file names, or user IDs) without proper authorization checks. This scanner automates the discovery and testing of potential IDOR vulnerabilities through intelligent parameter identification and systematic testing.

## Features

### Advanced Web Crawling
- Intelligent link discovery and form extraction
- Configurable crawling depth and rate limiting
- Respects robots.txt and implements politeness policies
- Same-domain restriction to stay in scope

### Smart Parameter Identification
- Detects multiple parameter types: numeric IDs, UUIDs, hashes, filenames, usernames
- Intelligent suspicion scoring based on parameter names and values
- Supports both URL parameters and form fields
- Configurable minimum suspicion threshold

### Sophisticated IDOR Testing
- Multiple test value generation strategies
- Advanced response analysis techniques
- Content similarity comparison
- Status code transition detection
- Success/failure indicator pattern matching

### Robust Authentication Support
- Username/password login automation
- Cookie-based authentication
- Custom header support (API keys, Bearer tokens)
- CSRF token extraction and handling
- Session persistence across requests

### Comprehensive Reporting
- **HTML Reports**: Interactive, collapsible findings with risk-based color coding
- **JSON Reports**: Machine-readable format for integration
- **CSV Reports**: Spreadsheet-compatible for analysis
- **Text Reports**: Clean summary format
- Risk-level categorization (HIGH/MEDIUM/LOW)

### Performance & Safety
- Configurable rate limiting to avoid detection
- Request timeout handling
- Error recovery and continuation
- Progress tracking and logging
- Graceful interruption handling

## Installation

### Prerequisites
- Python 3.12 or higher
- uv package manager (recommended) or pip

### Using uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/Dalosuuu/IDOR-CrawlerScanSuite.git
cd IDORs-Crawler

# Install dependencies
uv sync

# Run the scanner
uv run ./idor_scanner -u https://example.com
```

### Using pip
```bash
# Clone the repository
git clone https://github.com/Dalosuuu/IDOR-CrawlerScanSuite.git
cd IDORs-Crawler

# Install dependencies
pip install -r requirements.txt

# Run the scanner
python -m src.idor_scanner.main -u https://example.com
```

## Project Structure

```
IDORs-Crawler/
├── src/                           # Source code
│   └── idor_scanner/             # Core scanner modules
│       ├── __init__.py
│       ├── main.py               # Main application and CLI
│       ├── crawler.py            # Web crawling and link discovery
│       ├── parameter_identifier.py  # Parameter detection and scoring
│       ├── idor_tester.py        # IDOR vulnerability testing
│       ├── session_manager.py    # Authentication and session handling
│       └── reporter.py           # Report generation
├── demo/                         # Demo and testing
│   ├── test_server.py            # Vulnerable test server
│   └── test_scanner.py           # Parameter detection tests
├── docs/                         # Documentation
│   └── CONFIG.md                 # Configuration guide
├── idor_scanner                  # Main CLI entry point
├── examples.sh                   # Usage examples (USE FOR DEMO)
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## Usage

### Basic Usage

```bash
# Simple scan
./idor_scanner -u https://example.com

# Authenticated scan
./idor_scanner -u https://example.com \
               --login-url https://example.com/login \
               --username your_username \
               --password your_password

# Advanced scan with custom settings
./idor_scanner -u https://example.com \
               --max-depth 5 \
               --min-score 1 \
               --rate-limit 0.5 \
               --reports html,json,csv \
               --output-dir ./reports
```

### Command Line Options

```
Required Arguments:
  -u, --url URL              Target URL to scan

Authentication Options:
  --login-url URL            URL of the login page
  --username TEXT            Username for authentication
  --password TEXT            Password for authentication
  --cookies TEXT             Authentication cookies (name=value;name2=value2)
  --headers TEXT             Additional headers (Name: value;Name2: value2)

Scan Configuration:
  --max-depth N              Maximum crawling depth (default: 3)
  --min-score N              Minimum suspicion score (default: 2)
  --rate-limit FLOAT         Delay between requests in seconds (default: 1.0)

Output Options:
  --output-dir DIR           Report directory (default: reports)
  --reports FORMAT           Report formats: html,json,csv,txt (default: html)
  --log-level LEVEL          Logging level: DEBUG,INFO,WARNING,ERROR (default: INFO)
  --no-summary               Don't print console summary
```

### Example Scenarios

#### Bug Bounty Hunting
```bash
# Target with login authentication
./idor_scanner -u https://target.com \
               --login-url https://target.com/signin \
               --username your_email@example.com \
               --password your_password \
               --min-score 1

# API target with token authentication
./idor_scanner -u https://api.target.com \
               --headers "Authorization: Bearer eyJhbGc..." \
               --reports html,csv
```

#### Session-based Authentication
```bash
# Using browser cookies
./idor_scanner -u https://app.example.com \
               --cookies "session_id=abc123;csrf_token=xyz789" \
               --reports html,json
```

## Testing

The project includes a comprehensive testing environment:

### Test Server
Run the included vulnerable test server to validate the scanner:

```bash
# Start the test server (in one terminal)
uv run python demo/test_server.py

# Run the scanner against it (in another terminal)
./idor_scanner -u http://localhost:5000 \
               --min-score 1 \
               --max-depth 2 \
               --reports html,json
```

### Quick Test
```bash
# Automated test mode
./examples.sh test
```

## Architecture

The scanner is built with a modular architecture for maintainability and extensibility:

- **main.py**: CLI interface and orchestration
- **crawler.py**: Web crawling and content discovery
- **parameter_identifier.py**: Parameter analysis and scoring
- **idor_tester.py**: Vulnerability testing engine
- **session_manager.py**: Authentication and session handling
- **reporter.py**: Multi-format report generation

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Disclaimer

This tool is intended for authorized security testing only. Users are responsible for ensuring they have proper permission before scanning any target. The authors are not responsible for any misuse of this tool.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for bug bounty hunters and security professionals
- Inspired by common IDOR vulnerability patterns
- Special focus on automation and accuracy



### File: IDOR-CrawlerScanSuite/demo/README.md

# Demo & Testing

This directory contains demonstration materials and testing utilities for the IDOR Scanner.

## Sample Report
![Sample HTML Report](htmlReportSample.png)

## Contents

### Test Server (`test_server.py`)
A Flask-based vulnerable web application specifically designed to test IDOR vulnerability detection:

- **User API Endpoint**: `/api/user?id=1` - Access user profiles by ID
- **Document Access**: `/document/1` - Access documents by numeric ID
- **Admin Panel**: `/admin?user_id=2` - Admin functionality with user context
- **File Download**: `/download?file=report_1.pdf` - File access by filename
- **Search Form**: `/search` - POST form with hidden user_id parameter

**WARNING**: This server contains intentional vulnerabilities and should only be used for testing purposes.

### Test Scanner (`test_scanner.py`)
A debugging utility for testing parameter detection capabilities against various URL patterns.

### Reports Directory (`reports/`)
Contains example scan reports demonstrating the scanner's output formats:

- HTML reports with interactive UI
- JSON reports for programmatic analysis
- CSV reports for spreadsheet analysis

## Running the Demo

### Start the Test Server
```bash
uv run python demo/test_server.py
```
The server will be available at `http://localhost:5000`

### Scan the Test Server
```bash
# Basic scan
./idor_scanner -u http://localhost:5000 --min-score 1

# Comprehensive scan with multiple report formats
./idor_scanner -u http://localhost:5000 \
               --min-score 1 \
               --max-depth 2 \
               --rate-limit 0.3 \
               --reports html,json,csv
```

### Expected Results
The scanner should detect several IDOR vulnerabilities:

1. **High Risk**: User ID parameter in `/api/user?id=1`
2. **High Risk**: Hidden user_id field in search form
3. **Medium Risk**: Document ID in `/document/1`
4. **Medium Risk**: File parameter in download endpoint



### File: IDOR-CrawlerScanSuite/docs/CONFIG.md

# IDOR Scanner Configuration Examples

## Basic Configuration
The scanner can be configured through command-line arguments or by modifying the default values in the code.

### Scan Parameters
- `max_depth`: Maximum depth for crawling (default: 3)
- `rate_limit`: Delay between requests in seconds (default: 1.0)
- `min_suspicion_score`: Minimum score for parameter testing (default: 2)

### Authentication Methods
1. **Username/Password Login**
2. **Cookie-based Authentication**
3. **Header-based Authentication (API keys, tokens)**

### Parameter Detection
The scanner identifies potentially vulnerable parameters based on:
- Parameter names (id, user_id, account_id, etc.)
- Parameter values (numeric IDs, UUIDs, hashes, etc.)
- Context (URL parameters vs form fields)

### Suspicion Scoring
Parameters are scored based on:
- Name patterns: +2 points for suspicious names
- Value types: +3 for numeric/UUID, +2 for hashes/filenames
- Combined score determines testing priority

### IDOR Detection Methods
1. **Response Code Analysis**: 403/404 → 200 transitions
2. **Content Comparison**: Significant content differences
3. **Success Indicators**: Presence of user data, dashboards
4. **Access Control Bypass**: Removal of "access denied" messages

### Risk Levels
- **HIGH**: Strong evidence of IDOR (confidence + suspicion ≥ 8)
- **MEDIUM**: Moderate evidence (confidence + suspicion ≥ 5)
- **LOW**: Potential IDOR (confidence + suspicion < 5)

## Report Formats
- **HTML**: Interactive report with collapsible findings
- **JSON**: Machine-readable format for integration
- **CSV**: Spreadsheet-compatible format
- **TXT**: Plain text summary report

