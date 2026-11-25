---
name: pubmed-edirect
description: Search and retrieve literature from PubMed using NCBI's EDirect command-line tools.
requires:
  bins:
    - esearch
    - efetch
    - elink
    - xtract
    - einfo
    - efilter
install:
  - id: edirect
    kind: script
    label: Install NCBI EDirect from official source
    source: https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh
    docs: https://www.ncbi.nlm.nih.gov/books/NBK179288/
metadata:
  openclaw:
    emoji: 🔬
    requires:
      bins:
        - esearch
        - efetch
        - elink
        - xtract
        - einfo
        - efilter
    env:
      - name: NCBI_API_KEY
        optional: true
        description: NCBI API key for increased rate limits (10 requests/sec vs 3 requests/sec)
      - name: NCBI_EMAIL
        optional: true
        description: Email address to identify yourself to NCBI (recommended)
---

# PubMed EDirect Skill

Search and retrieve literature from PubMed using NCBI's EDirect command-line tools.

## Overview

This skill provides access to PubMed and other NCBI databases through the official EDirect (Entrez Direct) utilities. EDirect is a suite of programs that provide access to the NCBI's suite of interconnected databases (publication, sequence, structure, gene, variation, expression, etc.) from Unix terminals.

**Note: This is a local installation skill** – all tools run directly on your system without Docker or containerization. Follow the [INSTALL.md](INSTALL.md) guide for local setup.

## Structure

The skill is organized into the following files:

- **`INSTALL.md`** - Installation and configuration guide
- **`BASICS.md`** - Basic usage and common commands
- **`ADVANCED.md`** - Advanced techniques and complex queries
- **`EXAMPLES.md`** - Practical usage examples
- **`REFERENCE.md`** - Quick reference (field qualifiers, formats, etc.)
- **`OPENCLAW_INTEGRATION.md`** - OpenClaw-specific usage guide
- **`scripts/`** - Useful bash scripts for common tasks

## Quick Start

1. **Install EDirect** (see [INSTALL.md](INSTALL.md))
2. **Try a basic search**:
   ```bash
   esearch -db pubmed -query "CRISPR [TIAB]" | efetch -format abstract
   ```
3. **Explore examples** in [EXAMPLES.md](EXAMPLES.md)

## Core Tools

The skill provides access to EDirect tools through OpenClaw's `exec` capability:

- `esearch` - Search databases
- `efetch` - Retrieve records
- `elink` - Find related records
- `efilter` - Filter results
- `xtract` - Extract data from XML
- `einfo` - Get database information

## Databases Supported

EDirect supports numerous NCBI databases including:

- `pubmed` - Biomedical literature
- `pmc` - PubMed Central full-text articles
- `gene` - Gene information
- `nuccore` - Nucleotide sequences
- `protein` - Protein sequences
- `mesh` - Medical Subject Headings
- And many more...

## Key Features

- **Command-line access** to NCBI databases
- **Pipeline architecture** using Unix pipes
- **Structured data extraction** with XML parsing
- **Batch processing** capabilities
- **Cross-database linking** between records

## Getting Help

- Use `-help` with any EDirect command: `esearch -help`
- Consult the [official documentation](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
- Check troubleshooting in installation guide

## Included Scripts

The `scripts/` directory contains ready-to-use bash scripts:

### `batch_fetch_abstracts.sh`

Fetch abstracts for a list of PMIDs with error handling and rate limiting.

```bash
./scripts/batch_fetch_abstracts.sh pmids.txt abstracts/ 0.5
```

### `search_export_csv.sh`

Search PubMed and export results to CSV with metadata.

```bash
./scripts/search_export_csv.sh "CRISPR [TIAB]" 100 results.csv
```

### `publication_trends.sh`

Analyze publication trends over time with visualization.

```bash
./scripts/publication_trends.sh "machine learning" 2010 2023 trends.csv
```

## Notes

This skill requires EDirect to be installed and configured on your system. It provides command templates and examples that can be executed through OpenClaw's `exec` tool.

For complex workflows, consider creating reusable shell scripts or using the included scripts.
