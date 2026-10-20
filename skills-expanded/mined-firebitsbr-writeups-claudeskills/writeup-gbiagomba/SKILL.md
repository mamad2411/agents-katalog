<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gbiagomba
description: CTF writeups and security challenges by gbiagomba.
---

# Writeups by gbiagomba

Source repository: `/repos/gbiagomba`

## Repository Index

- clvr/CHANGELOG.md
- clvr/readme.md
- clvr/seeds/example-seed.md

## Writeup Content


### File: clvr/CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-03

### Added
- Comprehensive input validation and sanitization throughout the application
- Path traversal attack prevention with `sanitize_path()` function
- CVSS score and vector validation with proper error messages
- Environment variable support for API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, OLLAMA_HOST)
- Comprehensive error handling and user-friendly error messages
- Unit test suite with pytest covering core functionality
- Support for extracting JSON from AI responses wrapped in markdown code blocks
- Timeout handling for Ollama API requests (120s default)
- Character encoding support (UTF-8) for international vulnerability reports
- Graceful handling of KeyboardInterrupt with proper exit codes
- Enhanced logging and status messages throughout the application

### Changed
- **BREAKING**: Updated OpenAI provider to use new OpenAI client library (v1.x) instead of deprecated API
- **BREAKING**: API keys now primarily sourced from environment variables instead of command-line arguments for security
- Updated Claude provider to use latest model (claude-3-5-sonnet-20241022)
- Enhanced all AI providers with comprehensive error handling and validation
- Improved CLI help text and descriptions
- Refactored code with proper docstrings and type hints where applicable
- Enhanced Markdown rendering with proper formatting

### Security
- **CRITICAL**: Fixed API key exposure vulnerability - keys no longer visible in process list
- **HIGH**: Added path traversal attack prevention for all file operations
- **MEDIUM**: Added input validation to prevent injection attacks
- **LOW**: Improved error messages to avoid leaking sensitive information
- Added comprehensive CVSS validation to prevent invalid security ratings
- Enhanced schema validation with better error reporting

### Fixed
- Fixed deprecated OpenAI API usage (ChatCompletion.create)
- Fixed missing error handling in AI provider modules
- Fixed potential issues with file path handling on Windows
- Fixed empty seed file handling
- Fixed JSON parsing errors from AI responses
- Fixed missing dependency declarations in requirements.txt

### Documentation
- Added comprehensive inline documentation with docstrings
- Improved CLI help text for all commands
- Enhanced error messages with actionable guidance

## [0.1.0] - 2025-08-28

### Added
- Initial release of clvr
- Interactive vulnerability report creation (`clvr new`)
- JSON schema validation (`clvr validate`)
- AI-powered report generation with multiple providers (OpenAI, Claude, Gemini, Ollama)
- Export to Markdown and JSON formats
- Docker support
- Basic Makefile for common operations

[1.0.0]: https://github.com/yourusername/clvr/releases/tag/v1.0.0
[0.1.0]: https://github.com/yourusername/clvr/releases/tag/v0.1.0



### File: clvr/readme.md

# clvr — Command Line Vulnerability Reporter

> 🛡️ Structured, repeatable vulnerability documentation via CLI — export to Markdown + JSON

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/clvr/releases)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 📚 Table of Contents

- [Background](#background)
- [Features](#features)
- [Installation](#installation)
  - [Quick Install (Unix/Linux/macOS)](#quick-install-unixlinuxmacos)
  - [Quick Install (Windows)](#quick-install-windows)
  - [Manual Install](#manual-install)
  - [Using Docker](#using-docker)
- [Usage](#usage)
  - [Create New Report](#create-new-report)
  - [AI-Powered Generation](#ai-powered-generation)
  - [Validate Reports](#validate-reports)
  - [Export Reports](#export-reports)
- [Configuration](#configuration)
- [Development](#development)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 Background

`clvr` was born from the chaos of bug bounty chaos and red team notes. It's a terminal-first vulnerability reporter designed to streamline how security researchers, engineers, and bug bounty hunters document, validate, and share vulnerability reports — in both human-readable Markdown and structured JSON formats.

### Why clvr?

- **Standardized Reporting**: Consistent vulnerability documentation across teams
- **Multi-Format Export**: Generate both Markdown (for humans) and JSON (for automation)
- **AI-Powered**: Leverage OpenAI, Claude, Gemini, or local Ollama models
- **Secure by Default**: Environment-based API key management, input validation, path traversal protection
- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Schema Validation**: Built-in JSON schema validation ensures report quality

---

## ✨ Features

- ✅ **Interactive Report Creation** - `clvr new` guides you through creating structured reports
- ✅ **AI-Assisted Generation** - Use ChatGPT, Claude, Gemini, or Ollama to generate reports from seeds
- ✅ **Multi-Format Export** - Markdown for Obsidian/Notion/GitHub + JSON for automation
- ✅ **Schema Validation** - Ensure reports meet security standards with `clvr validate`
- ✅ **CVSS v3.1 Support** - Built-in validation for CVSS scores and vector strings
- ✅ **Secure Design** - No API keys in process lists, path traversal protection, input sanitization
- ✅ **Docker Support** - Run in isolated containers
- ✅ **Cross-Platform** - Automated installers for Unix/Linux/macOS and Windows

---

## 💾 Installation

### Quick Install (Unix/Linux/macOS)

```bash
git clone https://github.com/yourusername/clvr.git
cd clvr
chmod +x install.sh
./install.sh
```

The installer will:
- Detect your OS and install Python 3.8+ if needed
- Create a virtual environment
- Install all dependencies
- Run tests to verify installation
- Optionally add `clvr` to your PATH

### Quick Install (Windows)

```powershell
git clone https://github.com/yourusername/clvr.git
cd clvr
.\install.ps1
```

The installer will:
- Check for Python 3.8+ and offer to install via winget
- Create a virtual environment
- Install all dependencies
- Create a `clvr.bat` wrapper for easier execution
- Run tests to verify installation

### Manual Install

```bash
# Clone repository
git clone https://github.com/yourusername/clvr.git
cd clvr

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make CLI executable (Unix/Linux/macOS only)
chmod +x cli/clvr.py

# Verify installation
python3 cli/clvr.py --help
```

### Using Docker

```bash
# Build container
docker build -t clvr .

# Run interactively
docker run -it -v $(pwd):/home/clvr clvr new

# Validate a report
docker run -v $(pwd):/home/clvr clvr validate examples/2025-08-28-insecure-jwt-trust.json
```

---

## 🚀 Usage

### Create New Report

Create a vulnerability report interactively:

```bash
# Basic usage
./cli/clvr.py new

# With pre-filled values
./cli/clvr.py new \
  --product "Acme App" \
  --vuln-name "Insecure JWT Trust" \
  --cvss-score 8.8 \
  --cvss-vector "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N"
```

**Output:**
- `examples/YYYY-MM-DD-slug.md` - Human-readable Markdown
- `examples/YYYY-MM-DD-slug.json` - Machine-readable JSON

### AI-Powered Generation

Generate reports using AI models:

```bash
# Using OpenAI (ChatGPT)
export OPENAI_API_KEY="your-key-here"
./cli/clvr.py ai --provider chatgpt --seed seeds/sql-injection-seed.md

# Using Anthropic Claude
export ANTHROPIC_API_KEY="your-key-here"
./cli/clvr.py ai --provider claude --seed seeds/xss-seed.md

# Using Google Gemini
export GOOGLE_API_KEY="your-key-here"
./cli/clvr.py ai --provider gemini --seed seeds/csrf-seed.md

# Using local Ollama (no API key needed)
./cli/clvr.py ai --provider ollama --seed seeds/rce-seed.md
```

**Seed File Format:**
Create a Markdown file describing the vulnerability:

```markdown
# SQL Injection in Login Form

## Context
The login form at /auth/login accepts username and password...

## Vulnerability
User input is not properly sanitized...

## Impact
An attacker can bypass authentication...
```

### Validate Reports

Validate JSON reports against the schema:

```bash
# Validate single report
./cli/clvr.py validate examples/2025-08-28-insecure-jwt-trust.json

# Validate all reports
make validate
```

### Export Reports

Convert existing JSON to Markdown:

```bash
./cli/clvr.py export examples/2025-08-28-insecure-jwt-trust.json
```

---

## ⚙️ Configuration

### Environment Variables

Set API keys and configuration via environment variables:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-..."

# Google Gemini
export GOOGLE_API_KEY="..."

# Ollama (optional, defaults to http://localhost:11434)
export OLLAMA_HOST="http://localhost:11434"
```

**Make Permanent (Unix/Linux/macOS):**
```bash
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

**Make Permanent (Windows PowerShell):**
```powershell
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key", "User")
```

---

## 🛠 Development

### Using the Makefile

```bash
# Show all available commands
make help

# Install development dependencies
make install-dev

# Run tests
make test

# Run tests with coverage
make test-coverage

# Format code
make format

# Lint code
make lint

# Build Docker image
make docker-build

# Clean generated files
make clean
```

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run with coverage
python3 -m pytest tests/ --cov=cli --cov-report=html

# Run specific test
python3 -m pytest tests/test_clvr.py::TestSlugify -v
```

### Project Structure

```
clvr/
├── cli/
│   ├── clvr.py           # Main CLI entry point
│   ├── ai_logic.py       # AI provider logic
│   └── providers/        # AI provider implementations
│       ├── base.py
│       ├── openai.py
│       ├── claude.py
│       ├── gemini.py
│       └── ollama.py
├── tests/                # Unit tests
├── schemas/              # JSON schemas
├── examples/             # Example reports
├── seeds/                # AI seed templates
├── docs/                 # Documentation
├── Dockerfile            # Docker configuration
├── Makefile              # Build automation
├── install.sh            # Unix installer
├── install.ps1           # Windows installer
├── requirements.txt      # Python dependencies
└── CHANGELOG.md          # Version history
```

---

## 🔒 Security

### Security Features

- **API Key Protection**: Keys stored in environment variables, never in command-line arguments
- **Input Validation**: All user inputs validated and sanitized
- **Path Traversal Protection**: File paths validated to prevent directory traversal attacks
- **CVSS Validation**: Scores and vectors validated against CVSSv3.1 specification
- **Schema Validation**: All reports validated against JSON schema
- **Non-Root Docker**: Container runs as unprivileged user

### Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do NOT** open a public issue
2. Email: security@yourdomain.com
3. Include: Description, steps to reproduce, impact assessment

### Security Audit Log

See [CHANGELOG.md](CHANGELOG.md) for security fixes in each release.

---

## 🧪 CI/CD

This project uses GitHub Actions for continuous integration:

- ✅ Automated testing on push/PR
- ✅ Multi-platform builds (Ubuntu, macOS, Windows)
- ✅ Multi-architecture Docker images (amd64, arm64)
- ✅ Automated releases with binaries

---

## 🤝 Contributing

We welcome contributions! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `make test`
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new features
- Update documentation
- Follow [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📋 Flags & Options

### `clvr new`

| Flag | Description | Example |
|------|-------------|---------|
| `--product` | Product/application name | `--product "Acme App"` |
| `--vuln-name` | Vulnerability title | `--vuln-name "SQL Injection"` |
| `--cvss-score` | CVSS base score (0.0-10.0) | `--cvss-score 8.8` |
| `--cvss-vector` | CVSS vector string | `--cvss-vector "CVSS:3.1/..."` |

### `clvr ai`

| Flag | Description | Example |
|------|-------------|---------|
| `--provider` | AI provider (chatgpt, claude, gemini, ollama) | `--provider claude` |
| `--seed` | Path to seed markdown file | `--seed seeds/xss.md` |
| `--api-key` | API key (optional, uses env var) | `--api-key sk-...` |

### `clvr validate`

| Argument | Description | Example |
|----------|-------------|---------|
| `file` | Path to JSON file | `examples/report.json` |

---

## 📜 License

`clvr` is licensed under the **GNU General Public License v3.0** (GPL-3.0).

© 2025 Gilles Biagomba

See [LICENSE](LICENSE) for full details.

---

## 🙏 Acknowledgments

- Built with [Python](https://www.python.org/)
- AI providers: [OpenAI](https://openai.com/), [Anthropic](https://www.anthropic.com/), [Google](https://ai.google/), [Ollama](https://ollama.ai/)
- Schema validation: [jsonschema](https://python-jsonschema.readthedocs.io/)

---

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/clvr/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/clvr/discussions)

---

**Made with ❤️ for the security community**



### File: clvr/seeds/example-seed.md

# 🛡️ Security Vulnerability Documentation – Project Instructions

## Vulnerability Title
Reflected XSS via Error Parameter in Login Redirect

## CVSSv3 Score & Vector
CVSSv3 Base Score: 6.1  
Vector String: CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N  
Justification: The vulnerability is network-exploitable, requires no privileges, but needs user interaction. A successful attack could leak tokens or perform account takeover if chained with other flaws.

## Executive Summary
An attacker can craft a malicious URL that triggers a reflected Cross-Site Scripting (XSS) attack via the `error` parameter in the login redirect endpoint. This could result in sensitive cookie exfiltration or unauthorized UI manipulation. Since the endpoint is accessible to unauthenticated users, the impact is platform-wide and user-targeted.

## Detailed Technical Analysis
The login redirect endpoint (`/auth/login?error=`) reflects unsanitized user input back into the HTML response. This occurs before any templating or encoding layer is applied, allowing arbitrary JavaScript injection in modern browsers. A typical payload such as `<script>alert(document.cookie)</script>` is executed immediately in the login context, where tokens are often still valid.

Root cause appears to be a lack of input sanitization or output encoding. This pattern suggests the use of a custom-built auth handler without appropriate escaping on the query parameter.

## Impact Assessment (Attacker Mindset)
An attacker could craft a phishing email containing a malicious login URL. When clicked, it executes JavaScript in the login context — potentially stealing cookies, session tokens, or performing UI redressing. In SSO-enabled orgs, this could enable impersonation of legitimate users or harvest auth tokens for secondary attacks.

## Affected Assets
- `src/routes/auth.js:87`
- `https://app.example.com/auth/login?error=<payload>`
- `production`

## Remediation and Mitigation Strategy
### Mitigation Principles
All reflected user input should be HTML-escaped by default. The login handler should reject unknown query parameters or sanitize them before reflection. Additionally, HTTP-only flags on tokens can limit damage.

### Proposed Remediation
```javascript
const escapeHtml = require('escape-html');
const errorMessage = escapeHtml(req.query.error || '');
res.send(`<div>Error: ${errorMessage}</div>`);
```
References
	1.	https://owasp.org/www-community/attacks/xss/
	2.	https://cwe.mitre.org/data/definitions/79.html
	3.	https://portswigger.net/web-security/cross-site-scripting

