# Postman API Lifecycle Management Tools

This repository provides command-line tools for complete Postman API lifecycle management.

## Available Tools

All tools are Python scripts in the `scripts/` directory. Reference `tools.json` for complete documentation.

### Quick Reference

**Discovery**
- `python scripts/list_collections.py [--all|--environments|--monitors|--apis]` - List all resources
- `python scripts/list_workspaces.py` - List workspaces

**Collections**
- `python scripts/manage_collections.py [--list|--get|--create|--update|--delete|--duplicate]` - Collection CRUD
- `python scripts/manage_collection_workflow.py [create|import|duplicate|compare]` - Collection workflows

**Environments**
- `python scripts/manage_environments.py [--list|--get|--create|--update|--delete|--duplicate]` - Environment CRUD

**Design**
- `python scripts/manage_api.py [--list|--get|--name|--spec-file]` - Legacy API Builder
- `python scripts/manage_spec.py [create|list|get|generate-collection]` - Spec Hub (recommended)
- `python scripts/validate_schema.py [--api|--spec|--file]` - OpenAPI validation
- `python scripts/detect_breaking_changes.py [--api|--spec|--collection|--file]` - Breaking change detection

**Development**
- `python scripts/generate_code.py --collection <id> [--language|--all]` - Code generation (curl, Python, JS, Node.js, Go)

**Testing**
- `python scripts/run_collection.py --collection <name-or-id> [--environment]` - Run collection tests

**Security**
- `python scripts/audit_security.py [--api|--collection|--spec|--all-collections|--all-apis]` - Security auditing

**Deployment**
- `python scripts/manage_mocks.py [--list|--get|--create|--update|--delete]` - Mock server management

**Monitoring**
- `python scripts/manage_monitors.py [--list|--get|--create|--update|--delete|--analyze]` - Monitor management

**Documentation**
- `python scripts/publish_docs.py [--publish|--status|--compare|--changelog]` - Documentation publishing

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure API key: `cp .env.example .env` and add your `POSTMAN_API_KEY`
3. Run any script with `--help` for detailed options

## Environment Variables

Required:
- `POSTMAN_API_KEY` - Your Postman API key from https://go.postman.co/settings/me/api-keys

Optional:
- `POSTMAN_WORKSPACE_ID` - Default workspace ID
- `POSTMAN_BASE_URL` - API base URL (default: https://api.postman.com)
- `POSTMAN_TIMEOUT` - Request timeout in seconds (default: 30)
- `POSTMAN_MAX_RETRIES` - Max retry attempts (default: 3)

## Usage in Cursor

When the user asks to perform Postman operations, use these tools directly:

**Example 1: List collections**
```bash
python scripts/list_collections.py --all
```

**Example 2: Create API from OpenAPI spec**
```bash
python scripts/manage_spec.py create --name="User API" --file=openapi.json
```

**Example 3: Run tests**
```bash
python scripts/run_collection.py --collection="My Collection" --environment="Production"
```

**Example 4: Security audit**
```bash
python scripts/audit_security.py --collection <collection-id>
```

**Example 5: Generate code**
```bash
python scripts/generate_code.py --collection <id> --language python
```

## Architecture

- `scripts/postman_client.py` - Core API client
- `scripts/config.py` - Configuration management
- `utils/` - Helper utilities for formatting, errors, retries
- `tools.json` - Universal tool manifest

## Integration Notes

- All scripts use the same configuration from `.env`
- Scripts automatically handle rate limiting with exponential backoff
- JSON output can be piped to other tools for processing
- All operations support both names and IDs for resources
