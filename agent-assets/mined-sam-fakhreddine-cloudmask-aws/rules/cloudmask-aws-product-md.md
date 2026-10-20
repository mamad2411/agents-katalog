# CloudMask-AWS Product Overview

## Purpose

CloudMask-AWS is a Python library and CLI tool that anonymizes AWS infrastructure identifiers to enable secure sharing of infrastructure data with Large Language Models (LLMs) and external tools. It provides hash-based deterministic anonymization that is fully reversible while maintaining AWS resource structure.

## Value Proposition

- **Security First**: Safely share AWS infrastructure configurations, diagrams, and logs with LLMs without exposing sensitive identifiers
- **Reversible**: Complete bidirectional mapping allows restoration of original values after processing
- **Structure-Preserving**: Maintains AWS resource ID prefixes (vpc-, i-, sg-, etc.) for readability and context
- **Zero Trust**: All anonymization happens locally with no external API calls

## Key Features

### Core Capabilities
- Hash-based deterministic anonymization (same input → same output)
- Reversible mappings stored in secure JSON files
- AWS resource ID prefix preservation (vpc-xxx, i-xxx, sg-xxx)
- AWS Account ID anonymization (12-digit numbers)
- AWS ARN anonymization
- IP address anonymization
- Domain name anonymization (optional)
- Company name anonymization (configurable)
- Custom regex pattern support

### Interfaces
- **CLI Tool**: Command-line interface for quick workflows
- **Python Library**: Programmatic API for integration into scripts and applications
- **Clipboard Support**: Direct anonymization/unanonymization from clipboard

### Configuration
- YAML-based configuration files
- Custom pattern definitions via regex
- Configurable anonymization rules
- Template system for common configurations

### Security Features
- Secure central storage (~/.cloudmask/) with 700 permissions
- Mapping files created with 600 permissions (owner-only access)
- Seed-based verification prevents mapping corruption
- Auto-merge of mappings with same seed
- No external dependencies for core anonymization

## Target Users

### Primary Users
- **DevOps Engineers**: Anonymize infrastructure configs before sharing with LLMs for troubleshooting
- **Security Teams**: Analyze infrastructure without exposing sensitive identifiers
- **Cloud Architects**: Share architecture diagrams and documentation safely
- **Developers**: Get LLM assistance with AWS code without security concerns

### Use Cases
- 🤖 **LLM Assistance**: Get help with infrastructure problems without exposing IDs
- 📊 **Data Sharing**: Share configs and diagrams with external teams/vendors
- 🔍 **Security Analysis**: Analyze infrastructure with third-party tools
- 📝 **Documentation**: Create shareable examples from real infrastructure
- 🎓 **Training**: Use real infrastructure patterns in training materials

## What Gets Anonymized

- AWS Resource IDs (vpc-, i-, sg-, ami-, subnet-, rtb-, igw-, nat-, eni-, vol-, snap-, etc.)
- AWS Account IDs (12-digit numbers)
- AWS ARNs (arn:aws:service:region:account:resource)
- IP Addresses (IPv4 and IPv6)
- Company names (from configuration)
- Custom patterns (via regex configuration)
- Domain names (optional, configurable)

## Technical Highlights

- **Modern Python**: Requires Python 3.10+ with pattern matching and union types
- **Minimal Dependencies**: Only PyYAML, pyperclip, and cryptography
- **Type-Safe**: Full type hints with mypy validation
- **Well-Tested**: Comprehensive test suite with high coverage
- **Production-Ready**: Used in real-world infrastructure workflows
