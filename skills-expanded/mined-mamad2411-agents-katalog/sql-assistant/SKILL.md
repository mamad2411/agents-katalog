---
name: sql-assistant
description: SQL Smart Assistant - A natural language to SQL query tool supporting major databases (MySQL, PostgreSQL, SQL Server, MongoDB, Redis, SQLite) and LLM providers (OpenAI, Claude, Gemini). Helps users query databases, generate SQL statements, and explain execution plans through natural language.
---

# SQL Assistant

## Overview

SQL Assistant is a powerful natural language to SQL query tool that allows users to ask questions in natural language, automatically generate SQL statements, and execute queries. It supports multiple mainstream databases and LLM providers, offering both a web interface and REST API.

## Installation

### Method 1: Global Installation

```bash
pip install sql-assistant
```

### Method 2: Virtual Environment Installation (Recommended)

```bash
# Install uv (Python package manager)
pip install uv

# Initialize virtual environment
uv init

# Add sql-assistant package
uv add sql-assistant

# Activate virtual environment
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Optional Dependencies

```bash
# Install SQL Server support
pip install sql-assistant[sqlserver]

# Install Gemini support
pip install sql-assistant[gemini]

# Install Claude support
pip install sql-assistant[claude]

# Install all optional dependencies
pip install sql-assistant[sqlserver,gemini,claude]
```

## Quick Start

### Start the Service

After installation, run the following command to start SQL Assistant:

```bash
# Method 1: Use command-line script
sql-assistant

# Method 2: Use module approach
python -m sql_assistant.main
```

Access the service at:
- Web UI: http://localhost:5010
- API Docs: http://localhost:5010/docs

## Core Capabilities

### 1. Natural Language to SQL
- Convert natural language questions into SQL queries
- Support multiple SQL dialects (MySQL, PostgreSQL, SQL Server)
- Automatic table and column name matching

### 2. Database Management
- Support MySQL, PostgreSQL, SQL Server, MongoDB, Redis, SQLite
- Connection configuration management
- Database backup and restore

### 3. Query Execution & Explain
- Execute generated SQL statements
- Explain SQL execution plans
- Format query results for display

### 4. Conversation History
- Save query history records
- Support session management
- Query template functionality

## API Usage

### Natural Language to SQL

```bash
curl -X POST http://localhost:5010/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Query order count for the last 7 days", "db_connection": "mysql_connection"}'
```

### Explain SQL

```bash
curl -X POST http://localhost:5010/api/explain \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT COUNT(*) FROM orders", "db_connection": "mysql_connection"}'
```

### Execute SQL

```bash
curl -X POST http://localhost:5010/api/execute \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT * FROM users LIMIT 10", "db_connection": "mysql_connection"}'
```

## Configuration

### LLM Providers
- OpenAI (default)
- Claude (anthropic)
- Gemini (google)

### Database Connections
- MySQL
- PostgreSQL
- SQL Server
- MongoDB
- Redis
- SQLite

## Features

- Web UI with light/dark theme support
- Multi-session management
- SQL query history
- Query template saving
- Database backup functionality
- Execution plan explanation

## Resources

### scripts/
Python scripts for starting and managing the service.

### references/
API documentation and usage guides.

### assets/
Configuration template files.