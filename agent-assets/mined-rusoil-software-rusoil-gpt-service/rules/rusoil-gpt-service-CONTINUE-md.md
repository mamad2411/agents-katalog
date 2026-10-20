# CONTINUE.md - Python Project Guide

## Project Overview
This is a Python project with tools and testing infrastructure. Key components include:
- Backend services
- Testing utilities
- Smoke testing server

## Getting Started
### Prerequisites
- Python 3.7+
- Virtual environment
- Git

### Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Project Structure
```
├── backend/          # Main backend services
├── tests/            # Unit and integration tests
├── tools/            # Helper utilities
├── .continue/        # Continue documentation
└── src/              # Source code
```

## Development Workflow
### Testing
```bash
pytest tests/ -v
```

### Running Server
```bash
python backend/smoke_server.py
```

## Key Concepts
- REST API design
- Unit testing
- Integration testing

## Common Tasks
### Running Tests
```bash
pytest tests/ -m smoke
```

## Troubleshooting
- Check server logs in `backend/`
- Verify test dependencies

## References
- Python documentation
- pytest documentation
- Unit testing best practices

```