---
name: ai-data-sanitization-expert
description: Expert workflow for configuring, troubleshooting, and enhancing AI-powered database sanitization frameworks. Use when: setting up PII detection systems, configuring multi-file database connections, debugging AI API integrations, validating sanitization workflows, troubleshooting import/path issues, or coordinating complex data processing pipelines with AI enhancement.
---

# AI Data Sanitization Expert

## Workflow Overview

This skill provides a systematic approach to configuring and troubleshooting AI-enhanced database sanitization systems, handling the complexity of multi-file configurations, API integrations, and workflow validation.

## Phase 1: Configuration Audit & Setup

### Step 1: Inventory Configuration Files
```bash
# Identify all configuration touchpoints
find . -name "*.json" -path "*/config/*" | head -10
find . -name ".env*" | head -5
grep -r "database\|server\|api_key" --include="*.py" --include="*.json" . | head -20
```

**Checklist:**
- [ ] Environment files (`.env`, `.env.example`)
- [ ] JSON configuration files (`config/*.json`)
- [ ] Hardcoded values in Python scripts
- [ ] API configuration (tokens, endpoints, models)

### Step 2: Validate Configuration Consistency
**Decision Matrix:**
- **Production Ready**: All configs point to same database, API keys configured
- **Mixed Environment**: Some files point to different databases → **Requires harmonization**
- **Missing Keys**: API tokens not configured → **Requires credential setup**

### Step 3: Test Core Connectivity
**Validation Sequence:**
1. Database connection test
2. AI API connectivity test  
3. Schema extraction validation
4. End-to-end dry run

## Phase 2: AI Integration Configuration

### Step 1: API Configuration Validation
```python
# Standard validation pattern
def validate_ai_config(config):
    required_keys = ["api_url", "api_key_env_var", "model", "timeout_seconds"]
    missing = [key for key in required_keys if key not in config.get("ai", {})]
    if missing:
        return f"Missing AI config keys: {missing}"
    return "✓ AI configuration valid"
```

### Step 2: Model & Endpoint Testing
**Testing Hierarchy:**
1. **Authentication**: Verify API key validity
2. **Model Access**: Confirm model availability (gpt-4o, etc.)
3. **Request/Response**: Test with sample schema data
4. **Rate Limits**: Validate batch processing capabilities

### Step 3: AI Detection Workflow
**Systematic Flow:**
1. Extract database schema metadata
2. Batch schema data for AI processing
3. Send to AI API with PII detection prompts
4. Parse and validate AI responses
5. Generate configuration files

## Phase 3: Troubleshooting Methodology

### Common Issue Patterns

#### Import Path Errors
**Symptoms**: `ModuleNotFoundError: No module named 'src'`
**Solutions**:
```bash
# Method 1: PYTHONPATH approach
PYTHONPATH=. python script.py

# Method 2: Check for direct scripts (bypass examples/)
ls *_direct.py

# Method 3: Verify package structure
ls src/__init__.py
```

#### Configuration File Path Issues
**Symptoms**: `Config file not found: configpii_config.json`
**Root Cause**: Windows path separator handling
**Solutions**:
```bash
# Use forward slashes or quotes
python script.py config/file.json
python script.py "config\file.json"
```

#### Syntax Errors in Generated Code
**Symptoms**: `f-string: invalid syntax`
**Detection**: Look for variable names with spaces in f-strings
**Fix Pattern**: Replace `{var name}` with `{var_name}`

### Step-by-Step Debugging Process

1. **Isolate the Layer**
   - Configuration issue → Check file paths and JSON syntax
   - Connection issue → Test database connectivity directly
   - AI API issue → Test API endpoints independently
   - Import issue → Check Python path and module structure

2. **Use Direct Scripts First**
   - Prefer `*_direct.py` scripts over `examples/*.py`
   - Direct scripts often have fewer dependencies and clearer error messages

3. **Validate Each Step**
   - Run each phase independently before combining
   - Use dry-run modes extensively
   - Check logs and output files after each step

## Phase 4: Production Readiness

### Validation Checklist
- [ ] All configuration files point to production database
- [ ] API credentials secured and validated
- [ ] Foreign key relationships identified and handled
- [ ] Backup strategy confirmed
- [ ] Dry run completed successfully
- [ ] Data integrity validation passed

### Configuration Harmonization
When updating database settings across multiple files:

**Priority Order:**
1. `.env` (primary configuration)
2. `config/pii_config_ai_generated.json` (working configuration)
3. Direct script hardcoded values
4. Example and template files

**Batch Update Pattern:**
```bash
# Find all files needing updates
grep -r "old_database_name" --include="*.json" --include="*.py" .
grep -r "old_server_name" --include="*.json" --include="*.py" .

# Update systematically using multi-replace operations
```

## Decision Points

### When to Use Direct Scripts vs Examples
- **Examples failing with import errors** → Use `*_direct.py` equivalents
- **Need quick testing** → Direct scripts are more reliable
- **Production workflow** → Use examples with proper PYTHONPATH

### Configuration Strategy Selection
- **Single database** → Update all configs to match
- **Multi-environment** → Use environment-specific config files
- **Team collaboration** → Keep `.env.example` updated, ignore `.env`

### AI Model Selection
- **High accuracy needed** → Use GPT-4o or Claude-3.5-sonnet
- **Fast processing** → Consider GPT-3.5-turbo for simple schemas
- **Cost optimization** → Batch multiple tables per request

## Quality Gates

**Before proceeding to next phase:**
- [ ] No syntax errors in generated files
- [ ] All required configuration keys present
- [ ] Database connectivity confirmed
- [ ] AI API responding correctly
- [ ] Dry run shows expected transformations
- [ ] Foreign key relationships preserved

## Assets & Templates

### Environment File Template
```bash
# Database Configuration
SQLSERVER_HOST=your_server
SQLSERVER_DB=your_database
SQLSERVER_AUTH=windows

# AI API Configuration  
GITHUB_COPILOT_TOKEN=your_token
GITHUB_MODELS_DEFAULT_MODEL=gpt-4o
```

### Configuration Validation Script
```python
def validate_full_config(config_path):
    """Comprehensive configuration validation"""
    # Load and parse JSON
    # Validate database connectivity
    # Test AI API access
    # Check PII column definitions
    # Verify schema consistency
    pass
```

This skill transforms complex AI-enhanced data processing setup from ad-hoc troubleshooting into a systematic, repeatable workflow.