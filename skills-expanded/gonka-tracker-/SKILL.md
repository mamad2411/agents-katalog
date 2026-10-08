# Gonka Chain Observer - Cursor Rules

## Project Overview

This is a minimalistic full-stack tracker/observer for Gonka Chain - a decentralized AI infrastructure that optimizes computational power for AI model training and inference using a novel Proof of Work 2.0 consensus mechanism.

## Design Principles

### Core Philosophy
- **Crazy Simple**: Minimal code, maximum clarity
- **Minimalistic**: Single responsibility, no boilerplate, no unnecessary abstraction
- **Standard**: Follow established patterns and project structures
- **Clean**: Pure functionality, no comments explaining obvious code
- **Modern**: Use contemporary tooling and best practices

### Architecture Style
- Containerized microservices with Docker
- Clear separation between frontend and backend
- Traefik reverse proxy for routing
- Environment-based configuration
- Top-level consolidated configuration files

### Code Standards
- No emoji in code, documentation, or commits
- No comments unless absolutely necessary for complex logic
- Prefer explicit over implicit
- Test-driven where appropriate
- Keep files focused and small

## Gonka Chain Architecture

### API Endpoints Available
The tracker interacts with Gonka Chain through multiple API layers:

1. **Gonka SDK API** - Primary decentralized API
2. **/chain-rpc/** - Direct RPC access to chain nodes
3. **/chain-api/** - REST API for chain queries

### Epoch-Based System
Gonka Chain operates in 24-hour epoch cycles with distinct phases:

1. **PoC Generation Phase** (5 minutes)
   - Nodes generate proof-of-compute batches
   
2. **PoC Validation Phase** (20 minutes)
   - Nodes validate generated batches
   
3. **Inference Phase** (remaining ~23.5 hours)
   - Nodes serve vLLM inference requests

State transitions: INFERENCE → POC (generating) → POC (validating) → INFERENCE

## Technology Stack

### Backend
- Python 3.11
- FastAPI
- uv for dependency management
- pytest for testing
- Docker for deployment

### Frontend
- React 18+
- TypeScript
- Vite
- npm for package management
- Multi-stage Docker builds with nginx

### Infrastructure
- Docker Compose for orchestration
- Traefik v2.10+ for reverse proxy
- Environment variables for configuration

## Project Structure

```
tracker/
├── backend/          # FastAPI service
├── frontend/         # React + TypeScript UI
├── planning/         # Task planning and specifications
├── config.env        # Environment configuration
├── Makefile          # Build and run commands
└── docker-compose.yaml  # Service orchestration
```

## Development Workflow

### Planning
- **All tasks MUST be described in planning/ directory**
- Use markdown format: task-N.md
- Include: Task description, expected result, structure, approach
- Keep planning docs focused and concise

### Implementation
- Implement exactly what's specified in planning docs
- No over-engineering or premature optimization
- Prefer composition over inheritance
- Keep functions small and focused
- Write tests alongside implementation

### Testing
- Backend: Unit tests with pytest
- Frontend: Consider Vitest for testing
- Integration: Test live services with make test-integration
- Always test Docker builds locally

## API Design

### Backend Endpoints
- Prefix all routes with /v1/
- Use RESTful conventions
- Return clear error messages
- Enable CORS for frontend communication

### Frontend Integration
- Use environment variables for API URLs
- Handle loading and error states
- Keep components small and reusable
- Prefer functional components with hooks

## Docker Conventions

### Backend
- Base: python:3.11-slim
- Single-stage build
- Install dependencies first (layer caching)
- Run as non-root user where possible

### Frontend
- Multi-stage build (Node + nginx)
- Build artifacts in first stage
- Serve with nginx in second stage
- Use build args for configuration

### Compose
- Traefik for routing
- Use labels for Traefik configuration
- Explicit service dependencies
- Volume mounts only when necessary

## Commands

All commands through Makefile:
- `make setup-env` - Initialize environment
- `make run-app` - Start all services
- `make test-backend` - Run backend tests
- `make test-integration` - Test live services
- `make test-all` - Complete test suite

## Common Patterns

### Backend
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/v1/resource")
async def get_resource():
    return {"data": "value"}
```

### Frontend
```typescript
export function Component() {
  const [data, setData] = useState<Data | null>(null);
  
  useEffect(() => {
    fetch('/api/v1/resource')
      .then(res => res.json())
      .then(setData);
  }, []);
  
  return <div>{data?.value}</div>;
}
```

## What NOT to Do

- Do not add unnecessary dependencies
- Do not create abstractions prematurely
- Do not write comments for self-explanatory code
- Do not use emoji anywhere
- Do not deviate from planning without updating planning docs
- Do not skip Docker testing
- Do not commit untracked config files with secrets

## Integration with Gonka Chain

When building features:
- Consider the 24-hour epoch cycle
- Account for phase transitions
- Handle RPC/API failures gracefully
- Cache appropriately for phase durations
- Display epoch information prominently
- Show phase transitions in real-time

## Questions?

Refer to:
- Planning docs in planning/
- Main Gonka README: ../README.md
- Backend README: backend/README.md (if exists)
- Frontend README: frontend/README.md (if exists)

