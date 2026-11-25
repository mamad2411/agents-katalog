<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-andysitoop
description: CTF writeups and security challenges by Andysitoop.
---

# Writeups by Andysitoop

Source repository: `/repos/Andysitoop`

## Repository Index

- deep-eye-2.0/CHANGELOG.md
- deep-eye-2.0/CONTRIBUTING.md
- deep-eye-2.0/README.md
- deep-eye-2.0/docs/ARCHITECTURE.md
- deep-eye-2.0/docs/QUICKSTART.md
- deep-eye-2.0/plugins/README.md

## Writeup Content


### File: deep-eye-2.0/README.md

<center>
<img src="./assets/Screenshot 2025-10-20 150312.png" height="400">
</center>

# Deep Eye 🔍

An advanced AI-driven vulnerability scanner and penetration testing tool that integrates multiple AI providers (OpenAI, Grok, OLLAMA, Claude) with comprehensive security testing modules for automated bug hunting, intelligent payload generation, and professional reporting.

![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## 🚀 Features

### Core Capabilities
- **Multi-AI Provider Support**: Dynamic switching between OpenAI, Grok, OLLAMA, and Claude
- **Intelligent Payload Generation**: AI-powered, CVE-aware, context-sensitive payloads
- **Comprehensive Scanning**: 45+ attack methods with framework-specific tests
- **Advanced Reconnaissance**: Passive OSINT, DNS enumeration, subdomain discovery
- **Professional Reporting**: PDF/HTML/JSON reports with OSINT intelligence and executive summaries
- **Collaborative Scanning**: Team-based distributed scanning with session management
- **Custom Plugin System**: Extend Deep Eye with your own vulnerability scanners
- **Multi-Channel Notifications**: Real-time alerts via Email, Slack, and Discord

### Vulnerability Detection

#### Core Vulnerabilities
- SQL Injection (Error-based, Blind, Time-based)
- Cross-Site Scripting (XSS)
- Command Injection
- SSRF (Server-Side Request Forgery)
- XXE (XML External Entity)
- Path Traversal
- CSRF (Cross-Site Request Forgery)
- Open Redirect
- CORS Misconfiguration
- Security Headers Analysis

#### v1.3.0 Additional Vulnerabilities
- Local File Inclusion (LFI)
- Remote File Inclusion (RFI)
- Server-Side Template Injection (SSTI)
- CRLF Injection
- Host Header Injection
- LDAP Injection
- XML Injection
- Insecure Deserialization
- Authentication Bypass
- Information Disclosure
- Sensitive Data Exposure
- JWT Vulnerabilities
- Broken Authentication

#### v1.1.0 Advanced Modules
- **API Security Testing** (OWASP API Top 10 2023)
- **GraphQL Security** (Introspection, Depth limits, Batch attacks)
- **Business Logic Flaws** (Price manipulation, Workflow bypass, Race conditions)
- **Authentication Testing** (Session management, JWT, OAuth, MFA bypass)
- **File Upload Vulnerabilities** (Unrestricted upload, Path traversal, Type bypass)
- **Collaborative Scanning** (Team-based distributed scanning)

#### v1.2.0 Advanced Modules
- **WebSocket Testing** (Origin validation, Auth, Injection, DoS protection)
- **ML-Based Anomaly Detection** (Behavioral analysis, Pattern recognition)
- **Interactive HTML Reports** (Charts, Filtering, Real-time search)
- **Enhanced OSINT** (Google dorking, Breach databases, CT logs, GitHub/Pastebin)
- **Advanced Payload Obfuscation** (11+ techniques for WAF bypass)

#### v1.3.0 New Features
- **Custom Plugin System** (Extend with your own scanners)
- **Multi-Channel Notifications** (Email, Slack, Discord alerts)
- **Enhanced OSINT Reporting** (Reconnaissance data in all reports)

And 17+ more attack vectors

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- API keys for AI providers (at least one):
  - OpenAI API Key
  - Anthropic (Claude) API Key
  - Grok API Key
  - OLLAMA (local installation)

## 🔧 Installation

### Quick Install (Recommended)

**Windows:**
```powershell
.\scripts\install.ps1
```

**Linux/Mac:**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Manual Installation

1. Clone the repository:
```bash
git clone https://github.com/Andysitoop/deep-eye-2.0.git
cd deep-eye
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AI providers:
```bash
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your API keys
```

## 🎯 Usage

### Quick Start
```bash
# Scan with target from CLI
python deep_eye.py -u https://example.com

# Scan with configuration file
python deep_eye.py -c myconfig.yaml

# Verbose mode
python deep_eye.py -u https://example.com -v
```

### Configuration-Driven Scanning
All scan options are configured in `config/config.yaml`:

```yaml
scanner:
  target_url: "https://example.com"  # Default target
  ai_provider: "openai"               # AI provider
  default_depth: 2                    # Crawl depth
  default_threads: 5                  # Thread count
  enable_recon: true                  # Enable reconnaissance
  full_scan: false                    # Full/quick scan mode
  proxy: ""                           # Proxy settings
  custom_headers: {}                  # Custom headers

reporting:
  enabled: true                       # Auto-generate reports
  output_directory: "reports"         # Report directory
  default_format: "html"              # Report format
```

Then run:
```bash
python deep_eye.py
```

### Command Line Options (Minimal)
```
-u, --url              Target URL (overrides config)
-c, --config           Configuration file path (default: config/config.yaml)
-v, --verbose          Enable verbose output
--version              Show version and exit
--no-banner            Disable banner display
```

**Note:** All scanning options (depth, threads, AI provider, scan mode, proxy, etc.) are now configured in `config.yaml` for better management and repeatability.

## 📁 Project Structure

```
deep-eye/
├── core/                      # Core scanning engine
├── ai_providers/              # AI provider integrations
├── modules/                   # Security testing modules
├── utils/                     # Utility functions
├── config/                    # Configuration files
├── templates/                 # Report templates
├── examples/                  # Usage examples
├── scripts/                   # Installation scripts
├── docs/                      # Documentation
├── deep_eye.py               # Main entry point
├── setup.py                  # Package setup
└── requirements.txt          # Dependencies
```

For detailed structure, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## � Troubleshooting

### PDF Report Generation

**Issue**: PDF generation errors on Windows (WeasyPrint library issues)

**Solution**: The tool now uses ReportLab (Windows-friendly) for PDF generation by default. If you encounter any issues:

1. Ensure ReportLab is installed:
```bash
pip install reportlab>=4.0.0
```

2. If PDF generation fails, the tool will automatically fall back to HTML format.

3. For advanced HTML-to-PDF conversion (optional), you can install additional tools, but it's not required.

### Common Issues

**AI Provider Connection Errors**
- Verify your API keys in `config/config.yaml`
- Check your internet connection
- Ensure API key has sufficient credits

**Scanning Errors**
- Verify target URL is accessible
- Check if target has rate limiting or WAF
- Try reducing thread count with `-t` option

## �🛡️ Legal Disclaimer

**IMPORTANT**: Deep Eye is designed for authorized security testing only.

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal
- Users are responsible for complying with all applicable laws
- The developers assume no liability for misuse

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## � Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get started quickly
- **[Architecture](docs/ARCHITECTURE.md)** - System design and structure
- **[Testing Guide](docs/TESTING_GUIDE.md)** - Testing procedures
- **[Contributing](docs/CONTRIBUTING.md)** - How to contribute
- **[Changelog](docs/CHANGELOG.md)** - Version history

## �🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude
- OWASP for security testing methodologies
- The security research community

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**⚠️ Use Responsibly | 🔒 Test Ethically | 💡 Learn Continuously**



### File: deep-eye-2.0/plugins/README.md

# Custom Vulnerability Scanner Plugins

This directory contains custom vulnerability scanner plugins for Deep Eye.

## Quick Start

1. Create a new Python file in this directory (e.g., `my_scanner.py`)
2. Import and extend `PluginBase` class
3. Implement the `scan()` method
4. Enable plugins in `config/config.yaml`

## Example Plugin

```python
from typing import Dict, List
from core.plugin_manager import PluginBase


class MyCustomScanner(PluginBase):
    """My custom vulnerability scanner."""
    
    # Plugin metadata
    name = "My Custom Scanner"
    version = "1.0.0"
    author = "Your Name"
    description = "Scans for custom vulnerabilities"
    
    def scan(self, url: str, context: Dict) -> List[Dict]:
        """
        Scan URL for vulnerabilities.
        
        Args:
            url: Target URL
            context: Scan context (response, headers, etc.)
            
        Returns:
            List of vulnerabilities found
        """
        vulnerabilities = []
        
        # Your scanning logic here
        response = context.get('response')
        if response:
            # Example: Check for custom header
            if 'X-Custom-Header' not in response.headers:
                vulnerabilities.append({
                    'type': 'Missing Custom Header',
                    'severity': 'low',
                    'url': url,
                    'evidence': 'X-Custom-Header not found',
                    'description': 'Custom security header is missing',
                    'remediation': 'Add X-Custom-Header to responses',
                    'plugin': self.name
                })
        
        return vulnerabilities
```

## Configuration

Enable plugins in `config/config.yaml`:

```yaml
plugin_manager:
  enabled: true
  plugin_directory: "plugins"
  auto_load: true

# Plugin-specific configuration
plugins:
  mycustomscanner:  # Plugin ID (lowercase class name without 'plugin')
    enabled: true
    custom_setting: "value"
```

## Plugin API

### PluginBase Class

**Attributes:**
- `name` (str) - Plugin display name
- `version` (str) - Plugin version
- `author` (str) - Plugin author
- `description` (str) - Plugin description
- `http_client` - HTTP client instance
- `config` - Full configuration dictionary
- `plugin_config` - Plugin-specific configuration

**Methods:**
- `get_plugin_id()` - Get unique plugin identifier
- `is_enabled()` - Check if plugin is enabled
- `scan(url, context)` - Main scanning method (implement this)
- `get_info()` - Get plugin information

### Context Dictionary

The `context` parameter contains:
- `url` - Target URL
- `response` - HTTP response object
- `headers` - Response headers
- `osint_data` - OSINT data from reconnaissance (if available)

### Vulnerability Dictionary Format

Each vulnerability should be a dictionary with:
- `type` (str) - Vulnerability type
- `severity` (str) - critical, high, medium, low, info
- `url` (str) - Vulnerable URL
- `evidence` (str) - Evidence of vulnerability
- `description` (str) - Detailed description
- `remediation` (str) - How to fix
- `plugin` (str) - Plugin name (optional)
- `parameter` (str) - Vulnerable parameter (optional)
- `payload` (str) - Payload used (optional)

## Best Practices

1. **Error Handling** - Always wrap code in try/except
2. **Logging** - Use `logger` for debugging
3. **Performance** - Limit number of requests
4. **Documentation** - Add docstrings to methods
5. **Testing** - Test plugins thoroughly before deployment

## Plugin Lifecycle

1. Plugin file placed in `plugins/` directory
2. PluginManager scans for `.py` files
3. Loads classes extending PluginBase
4. Checks if plugin is enabled in config
5. Runs plugin during scanning phase
6. Results merged into final report

## Available Plugins

- `example_plugin.py` - Example security header checker

## Need Help?

See the example plugin or open an issue on GitHub.




### File: deep-eye-2.0/CHANGELOG.md

# Changelog

All notable changes to Deep Eye will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-10-20

### Added

#### New Features
- **Custom Plugin System** - Extensible architecture for custom vulnerability scanners
  - Plugin base class for easy development
  - Hot-reload plugin loading from `plugins/` directory
  - Example plugin included for demonstration
  - Plugin enable/disable via configuration
  - Automatic plugin discovery and initialization
  
- **Multi-Channel Notification System** - Real-time alerts for scan completion and critical findings
  - **Email Notifications** - SMTP-based email alerts with HTML formatting
  - **Slack Integration** - Webhook-based Slack notifications with rich formatting
  - **Discord Integration** - Discord webhook notifications with embed support
  - Immediate alerts for critical vulnerabilities
  - Configurable notification triggers
  - Detailed scan summary in notifications
  
- **Enhanced Reporting with OSINT Data** - Comprehensive reconnaissance data in reports
  - DNS records displayed in PDF and HTML reports
  - OSINT findings integration (emails, subdomains, technologies)
  - GitHub leak detection in reports
  - Breach database results
  - Social media footprint
  - Beautiful formatting with dedicated sections

#### New Vulnerability Scanners
- **15 New Vulnerability Scanners** - Expanded from 30+ to 45+ attack methods
  - **Local File Inclusion (LFI)** - Detects file inclusion vulnerabilities for reading local files
  - **Remote File Inclusion (RFI)** - Identifies remote file inclusion leading to potential RCE
  - **Server-Side Template Injection (SSTI)** - Tests for template injection vulnerabilities
  - **CRLF Injection** - Checks for header manipulation and response splitting
  - **Host Header Injection** - Detects cache poisoning and SSRF via Host header
  - **LDAP Injection** - Tests for LDAP query manipulation vulnerabilities
  - **XML Injection** - Identifies XML structure manipulation issues
  - **Insecure Deserialization** - Detects unsafe deserialization patterns (Java, Python, PHP)
  - **Authentication Bypass** - Tests various authentication bypass techniques
  - **Information Disclosure** - Scans for exposed sensitive information (passwords, API keys, secrets)
  - **Sensitive Data Exposure** - Detects PII exposure (SSN, credit cards, emails, phone numbers)
  - **JWT Vulnerabilities** - Checks for JWT "none" algorithm and weak signing algorithms
  - **Broken Authentication** - Tests session management security (Secure/HttpOnly flags, weak session IDs)
  - **API Vulnerabilities** (alias) - Backward compatibility for api_security
  - **GraphQL Vulnerabilities** (alias) - Backward compatibility for graphql_security

### Changed
- Updated vulnerability scanner from 30+ to 45+ attack methods
- Enhanced scanner engine with comprehensive coverage of OWASP Top 10 and beyond
- All new scanners include detailed evidence collection and remediation guidance
- Improved error handling and logging for all scanner modules
- **CLI simplified** - All scan options now configured via config.yaml (CLI only has -u, -c, -v, --version)
- **Report generation** - Now fully controlled by config (output directory, filename, format)
- **Config-driven architecture** - All modules read settings from centralized config

### Fixed
- **PDF Report Generation** - Fixed XML/HTML special character escaping for valid PDF output
- **OSINT Integration** - Enhanced OSINT data collection and proper integration into reconnaissance flow
- **Reconnaissance Data Flow** - OSINT results properly flattened and accessible in reports (emails, subdomains, technologies, breaches, GitHub leaks)

## [1.2.1] - 2025-10-15

### Fixed
- **PDF Report Generation on Windows**
  - Replaced WeasyPrint with ReportLab for Windows compatibility
  - WeasyPrint requires GTK libraries which are problematic on Windows
  - ReportLab provides native Windows support with no external dependencies
  - Added automatic fallback to HTML if PDF generation fails
  - Improved error handling and user feedback
  - Updated requirements.txt (WeasyPrint now optional/commented)

### Changed
- **Report Generator Improvements**
  - Enhanced PDF layout with professional styling
  - Added color-coded severity indicators in PDF reports
  - Improved table formatting for better readability
  - Added comprehensive metadata section
  - Better vulnerability detail presentation

- **OSINT Refactoring**
  - Moved OSINT gathering from vulnerability scanner to reconnaissance phase
  - OSINT intelligence is now collected during reconnaissance (--recon flag)
  - Integrated EnhancedOSINT module into ReconEngine
  - OSINT data is now available in scan context for all modules
  - Updated configuration: removed 'osint_gathering' from vulnerability_scanner checks
  - Added 'osint_gathering' to reconnaissance enabled_modules
  - Cleaner separation of concerns: recon gathers intelligence, scanner tests vulnerabilities

## [1.2.0] - 2025-10-15

### Added
- **WebSocket Security Testing Module**
  - Origin header validation testing
  - WebSocket authentication verification
  - Message injection attack detection (XSS, SQLi, Command injection)
  - DoS attack testing (large payloads, message flooding)
  - Rate limiting verification
  - TLS/SSL verification for WSS connections
  - Protocol downgrade attack detection
  - Information disclosure testing
  - Automatic WebSocket endpoint detection
- **Machine Learning Anomaly Detection Module**
  - Unsupervised anomaly detection using IsolationForest
  - Response time pattern analysis
  - Status code anomaly detection
  - Error message clustering
  - Response size analysis
  - Parameter behavior monitoring
  - Baseline training capability
  - Composite anomaly scoring
- **Interactive HTML Report Generator**
  - Dynamic JavaScript-based filtering by severity
  - Real-time vulnerability search
  - Interactive Chart.js visualizations (doughnut, bar charts)
  - Responsive modern design with gradient backgrounds
  - Severity statistics dashboard
  - Vulnerability type distribution charts
  - Color-coded severity badges
  - Detailed evidence and remediation sections
  - Print-friendly styling
  - Mobile-responsive layout
- **Enhanced OSINT Reconnaissance Module**
  - Automated Google dorking with common queries
  - Email address harvesting from public sources
  - Document and image metadata extraction
  - Social media footprint analysis
  - Breach database integration (HaveIBeenPwned)
  - Certificate Transparency log queries
  - GitHub code and secret search
  - Pastebin leak detection
- **Advanced Payload Obfuscation Module**
  - Base64 encoding variations
  - URL encoding (single, double, mixed)
  - Unicode character encoding
  - Hexadecimal encoding
  - Random case manipulation
  - SQL/JavaScript comment insertion
  - String concatenation techniques
  - Null byte injection
  - Multiple encoding layers
  - Character substitution (homoglyphs)
  - WAF-specific bypass patterns

### Changed
- Updated core vulnerability scanner to integrate v1.2.0 modules
- Enhanced configuration with WebSocket, ML, OSINT, and obfuscation settings
- Added new dependencies: websocket-client, scikit-learn, numpy, pandas
- Updated README.md with v1.2.0 feature descriptions
- Improved vulnerability scanner with obfuscated payload testing
- Added OSINT and anomaly detection helper methods to scanner

## [1.1.0] - 2025-10-15

### Added
- **API Security Testing Module** - OWASP API Top 10 2023 compliance
  - Broken authentication detection
  - Excessive data exposure testing
  - Rate limiting verification
  - Object-level authorization testing (IDOR)
  - Mass assignment vulnerability detection
  - Security misconfiguration checks
  - Injection testing (SQL, NoSQL, Command, XML)
  - Improper assets management detection
  - Insufficient logging verification
- **GraphQL Security Module**
  - Introspection query testing
  - Query depth limit testing
  - Batch query attack detection
  - Field suggestion information disclosure testing
- **Business Logic Testing Module**
  - Price manipulation detection
  - Quantity manipulation testing
  - Workflow bypass detection
  - Race condition testing
  - Coupon/promo code abuse detection
  - Referral program abuse testing
  - Action limit bypass detection
- **Authentication Testing Module**
  - Weak password acceptance testing
  - Brute force protection verification
  - Default credentials detection
  - Session fixation testing
  - Session timeout verification
  - JWT security testing (none algorithm, weak signatures)
  - Password reset token security
  - OAuth implementation testing
  - MFA bypass detection
- **File Upload Vulnerability Module**
  - Unrestricted file upload detection
  - Path traversal in uploads
  - File type bypass testing (MIME type manipulation)
  - Malicious content detection (polyglot files)
  - File size limit testing
  - Double extension vulnerability testing
  - SVG XSS detection
  - XXE via file upload testing
- **Collaborative Scanning Features**
  - Team-based scanning sessions
  - Work distribution among team members
  - Real-time progress tracking
  - Vulnerability discovery attribution
  - Session export (JSON/CSV formats)
  - Session finalization with statistics

### Changed
- Updated vulnerability scanner from 25+ to 30+ attack methods
- Enhanced configuration with new module settings
- Improved README with new feature descriptions
- Updated scanner engine to integrate new modules

## [1.0.0] - 2025-10-15

### Added
- Initial release of Deep Eye
- Multi-AI provider support (OpenAI, Claude, Grok, OLLAMA)
- Comprehensive vulnerability scanner with 25+ attack methods
- SQL Injection detection (Error-based, Blind, Time-based)
- Cross-Site Scripting (XSS) detection
- Command Injection testing
- SSRF vulnerability detection
- XXE vulnerability detection
- Path Traversal testing
- CSRF detection
- Open Redirect detection
- CORS misconfiguration detection
- Security headers analysis
- Web crawler with configurable depth
- Multi-threaded scanning engine
- AI-powered payload generation
- Context-aware testing
- Reconnaissance module with DNS enumeration
- Subdomain discovery
- Technology detection
- Professional report generation (HTML, PDF, JSON)
- Executive summary generation
- Severity-based vulnerability classification
- Rich CLI with progress indicators
- Comprehensive logging system
- Configuration management
- Proxy support
- Custom headers and cookies support
- Rate limiting
- SSL certificate verification
- Retry logic for failed requests
- Error handling and recovery

### Security
- Input validation for all user inputs
- Safe API key handling
- SSL/TLS verification
- Rate limiting to prevent abuse
- Secure report storage

### Documentation
- Comprehensive README with usage examples
- Quick start guide
- Configuration examples
- API documentation
- Contributing guidelines
- Legal disclaimer and licensing

## [Unreleased]

### Planned Features
- Authentication testing module
- Session management analysis
- API security testing
- GraphQL vulnerability scanning
- WebSocket testing
- File upload vulnerability detection
- Business logic testing
- Machine learning-based anomaly detection
- Interactive HTML reports
- Database integration for result storage
- RESTful API for programmatic access
- Web UI dashboard
- Scheduled scanning
- Notification system (email, Slack, Discord)
- Integration with CI/CD pipelines
- Docker containerization
- Kubernetes deployment support
- Cloud deployment options
- Enhanced reconnaissance with OSINT
- Advanced payload obfuscation
- Custom plugin system
- Collaborative scanning features

---

For older versions and detailed changes, see [GitHub Releases](https://github.com/zakirkun/deep-eye/releases)



### File: deep-eye-2.0/CONTRIBUTING.md

# Deep Eye - Contributing Guide

Thank you for your interest in contributing to Deep Eye! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Follow ethical security practices
- Never use this tool for illegal purposes
- Report security issues responsibly

## How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/zakirkun/deep-eye.git
cd deep-eye
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Update tests if applicable
- Update documentation

### 4. Test Your Changes
```bash
python -m pytest tests/
```

### 5. Submit Pull Request
- Write clear commit messages
- Reference any related issues
- Update CHANGELOG.md

## Development Setup

### Install Development Dependencies
```powershell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests
```powershell
pytest tests/ -v
```

### Code Formatting
```powershell
# Format code
black .

# Check linting
flake8 .
```

## Project Structure

```
deep-eye/
├── core/               # Core scanning engine
├── ai_providers/       # AI provider integrations
├── modules/           # Security testing modules
├── utils/             # Utility functions
├── config/            # Configuration files
├── templates/         # Report templates
├── tests/             # Unit tests
└── examples/          # Usage examples
```

## Adding New Features

### Adding a New Vulnerability Check
1. Create test module in `modules/exploits/`
2. Implement detection logic
3. Add to vulnerability scanner
4. Update documentation

### Adding a New AI Provider
1. Create provider class in `ai_providers/`
2. Implement generate() method
3. Add to provider manager
4. Update configuration template

### Adding Report Formats
1. Create template in `templates/`
2. Implement generator in `report_generator.py`
3. Add format option to CLI
4. Update documentation

## Security

### Reporting Security Issues
- **DO NOT** open public issues for security vulnerabilities
- Email: security@deepeye.io
- Use PGP key if available
- Provide detailed reproduction steps

### Security Best Practices
- Never commit API keys or secrets
- Use environment variables for sensitive data
- Follow OWASP guidelines
- Implement rate limiting
- Add input validation

## Documentation

- Keep README.md up to date
- Add docstrings to all public APIs
- Update QUICKSTART.md for new features
- Include code examples

## Testing Guidelines

- Write unit tests for new features
- Maintain >80% code coverage
- Test edge cases
- Mock external API calls

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue with the "question" label or contact the maintainers.

---

**Thank you for contributing to Deep Eye! 🔍🛡️**



### File: deep-eye-2.0/docs/ARCHITECTURE.md

# Deep Eye - Project Structure

```
deep-eye/
│
├── deep_eye.py                 # Main entry point
├── setup.py                    # Installation setup
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── QUICKSTART.md              # Quick start guide
├── CONTRIBUTING.md            # Contributing guidelines
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT License
├── .gitignore                 # Git ignore rules
├── install.ps1                # Windows installation script
├── install.sh                 # Linux/Mac installation script
│
├── core/                      # Core functionality
│   ├── __init__.py
│   ├── scanner_engine.py      # Main scanning orchestrator
│   ├── ai_payload_generator.py # AI-powered payload generation
│   ├── vulnerability_scanner.py # Vulnerability detection
│   └── report_generator.py    # Report creation
│
├── ai_providers/              # AI provider integrations
│   ├── __init__.py
│   ├── provider_manager.py    # Provider management
│   ├── openai_provider.py     # OpenAI/GPT-4 integration
│   ├── claude_provider.py     # Anthropic Claude integration
│   ├── grok_provider.py       # xAI Grok integration
│   └── ollama_provider.py     # OLLAMA local LLM integration
│
├── modules/                   # Security testing modules
│   ├── __init__.py
│   └── reconnaissance/        # OSINT & enumeration
│       ├── __init__.py
│       └── recon_engine.py
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── logger.py             # Logging utilities
│   ├── config_loader.py      # Configuration management
│   ├── http_client.py        # HTTP client with retry logic
│   └── parser.py             # URL and response parsing
│
├── config/                    # Configuration files
│   └── config.example.yaml   # Example configuration
│
├── templates/                 # Report templates
│   └── (HTML/PDF templates)
│
├── examples/                  # Usage examples
│   └── basic_usage.py        # Basic usage example
│
├── logs/                      # Log files (auto-created)
├── data/                      # Database files (auto-created)
└── reports/                   # Generated reports (auto-created)
```

## Module Descriptions

### Core Modules

#### scanner_engine.py
- Orchestrates the entire penetration testing process
- Multi-threaded web crawling
- URL discovery and management
- Coordinates vulnerability scanning
- Manages scan lifecycle

#### ai_payload_generator.py
- Generates intelligent, context-aware payloads
- Integrates with multiple AI providers
- CVE-aware payload generation
- Framework-specific attack vectors
- Adaptive payload mutation

#### vulnerability_scanner.py
- Implements 25+ vulnerability detection methods
- SQL Injection (Error, Blind, Time-based)
- XSS (Reflected, Stored, DOM)
- Command Injection
- SSRF, XXE, Path Traversal
- CSRF, Open Redirect
- Security misconfigurations

#### report_generator.py
- Professional report generation
- Multiple formats (HTML, PDF, JSON)
- Executive summaries
- Severity-based classification
- Remediation recommendations

### AI Providers

#### provider_manager.py
- Dynamic provider switching
- Unified interface for all AI providers
- Failover and retry logic
- API key management

#### Individual Providers
- **OpenAI**: GPT-4o integration
- **Claude**: Anthropic Claude 3.5 Sonnet
- **Grok**: xAI Grok Beta
- **OLLAMA**: Local LLM support

### Modules

#### reconnaissance/recon_engine.py
- DNS enumeration
- WHOIS lookup
- Subdomain discovery
- Technology detection
- SSL certificate analysis
- Port scanning

### Utilities

#### logger.py
- Centralized logging
- File and console output
- Log rotation
- Severity levels

#### config_loader.py
- YAML configuration management
- Environment variable support
- Default configurations
- Validation

#### http_client.py
- Robust HTTP client
- Automatic retries
- Proxy support
- Custom headers/cookies
- SSL verification

#### parser.py
- URL parsing and normalization
- HTML content extraction
- Form detection
- Technology fingerprinting
- Link extraction

## Data Flow

```
User Input → Scanner Engine → Web Crawler → URL Discovery
                ↓
        AI Payload Generator ← AI Provider
                ↓
    Vulnerability Scanner → HTTP Client → Target
                ↓
        Results Collection
                ↓
        Report Generator → Output (HTML/PDF/JSON)
```

## Configuration

All settings are managed through `config/config.yaml`:
- AI provider credentials
- Scanner parameters
- Vulnerability checks
- Reconnaissance modules
- Report settings
- Logging configuration

## Extending Deep Eye

### Adding New Vulnerability Checks
1. Add check method to `vulnerability_scanner.py`
2. Register in enabled_checks
3. Update documentation

### Adding New AI Providers
1. Create provider class in `ai_providers/`
2. Implement `generate()` method
3. Register in `provider_manager.py`
4. Update configuration

### Adding New Report Formats
1. Create template in `templates/`
2. Add generator method in `report_generator.py`
3. Update CLI options

## Best Practices

- Always activate virtual environment
- Keep dependencies updated
- Use configuration files for settings
- Never commit API keys
- Test on authorized targets only
- Follow ethical hacking guidelines



### File: deep-eye-2.0/docs/QUICKSTART.md

# Deep Eye Quick Start Guide

## Installation

1. **Install Python Dependencies:**
```powershell
pip install -r requirements.txt
```

2. **Configure AI Providers:**
```powershell
# Copy example config
Copy-Item config\config.example.yaml config\config.yaml

# Edit config.yaml and add your API keys
notepad config\config.yaml
```

## Basic Usage

### Simple Scan
```powershell
python deep_eye.py -u https://example.com
```

### Full Scan with AI
```powershell
python deep_eye.py -u https://example.com --ai-provider openai --full-scan
```

### Reconnaissance Mode
```powershell
python deep_eye.py -u https://example.com --recon --output report.html
```

## Configuration

### AI Providers Setup

#### OpenAI (GPT-4)
1. Get API key from https://platform.openai.com/api-keys
2. Add to config.yaml:
```yaml
ai_providers:
  openai:
    enabled: true
    api_key: "sk-your-key-here"
    model: "gpt-4o"
```

#### Claude (Anthropic)
1. Get API key from https://console.anthropic.com/
2. Add to config.yaml:
```yaml
ai_providers:
  claude:
    enabled: true
    api_key: "sk-ant-your-key-here"
    model: "claude-3-5-sonnet-20241022"
```

#### Grok (xAI)
1. Get API key from https://console.x.ai/
2. Add to config.yaml:
```yaml
ai_providers:
  grok:
    enabled: true
    api_key: "xai-your-key-here"
```

#### OLLAMA (Local)
1. Install OLLAMA from https://ollama.ai/
2. Pull a model: `ollama pull llama2`
3. Add to config.yaml:
```yaml
ai_providers:
  ollama:
    enabled: true
    base_url: "http://localhost:11434"
    model: "llama2"
```

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-u, --url` | Target URL | `-u https://example.com` |
| `-d, --depth` | Crawl depth | `-d 3` |
| `-t, --threads` | Number of threads | `-t 10` |
| `--ai-provider` | AI provider | `--ai-provider openai` |
| `--recon` | Enable reconnaissance | `--recon` |
| `--full-scan` | Enable all tests | `--full-scan` |
| `--quick-scan` | Quick scan only | `--quick-scan` |
| `-o, --output` | Output file | `-o report.pdf` |
| `--format` | Report format | `--format html` |
| `--proxy` | Proxy URL | `--proxy http://127.0.0.1:8080` |

## Examples

### 1. Basic Website Scan
```powershell
python deep_eye.py -u https://testsite.com
```

### 2. Deep Scan with Custom Depth
```powershell
python deep_eye.py -u https://testsite.com -d 5 -t 15
```

### 3. Full Reconnaissance + Scan
```powershell
python deep_eye.py -u https://testsite.com --recon --full-scan --format pdf -o full_report.pdf
```

### 4. Scan Through Proxy
```powershell
python deep_eye.py -u https://testsite.com --proxy http://127.0.0.1:8080
```

### 5. Using Different AI Provider
```powershell
python deep_eye.py -u https://testsite.com --ai-provider claude --full-scan
```

## Troubleshooting

### Import Errors
Install missing dependencies:
```powershell
pip install -r requirements.txt --upgrade
```

### AI Provider Errors
- Check API keys in `config/config.yaml`
- Verify API key has sufficient credits
- Check network connectivity

### SSL Errors
Disable SSL verification (not recommended for production):
Edit config.yaml:
```yaml
scanner:
  verify_ssl: false
```

## Legal Notice

⚠️ **IMPORTANT**: Only use Deep Eye on systems you own or have explicit permission to test. Unauthorized security testing is illegal.

## Support

For issues and questions:
- GitHub Issues: https://github.com/zakirkun/deep-eye/issues
- Documentation: See README.md

