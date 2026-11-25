# DevOps Skill

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

A skill responsible for deployment script inspection and local development environment configuration.

## Role

1. **Deployment Script Inspection**: Review Dockerfile, docker-compose, CI/CD configuration
2. **Local Environment Setup**: Prepare development server execution environment
3. **Dependency Management**: Package installation and environment variable configuration
4. **Health Check**: Service status verification and monitoring

## Supported Stacks

### Backend
- **Node.js/NestJS**: npm/yarn, package.json
- **Python/FastAPI**: pip, requirements.txt, venv
- **Docker**: Dockerfile, docker-compose.yml

### Frontend
- **Next.js/React**: npm/yarn, package.json
- **Vite**: vite.config.ts

### Infrastructure
- **Docker Compose**: Multi-container orchestration
- **Environment Variables**: .env, .env.example

## Workflow

### 1. Project Analysis
```
From the project root:
1. Check package.json / requirements.txt
2. Check Dockerfile / docker-compose.yml
3. Check .env.example or environment variable requirements
4. Check execution scripts (scripts/, Makefile, etc.)
```

### 2. Environment Setup
```
1. Install dependencies
   - Node.js: npm install / yarn install
   - Python: python -m venv venv && pip install -r requirements.txt

2. Configure environment variables
   - Copy .env.example → .env
   - Verify required environment variables and provide guidance

3. Check data files
   - Large files (e.g., ephemeris, ML models)
   - Whether external downloads are needed
```

### 3. Service Execution
```
Priority:
1. Docker Compose (recommended)
   docker-compose up -d

2. Individual service execution
   - Backend: npm run start:dev / uvicorn app.main:app
   - Frontend: npm run dev

3. Health check
   - Verify each service's /health endpoint
   - Check for port conflicts
```

### 4. Troubleshooting
```
Common issues:
- Port conflict: lsof -i :PORT && kill -9 PID
- Dependency error: Delete node_modules/venv and reinstall
- Missing environment variables: Check .env file
- Docker not running: Guide to start Docker Desktop
```

## Checklist

### Pre-deployment Check
- [ ] Dockerfile build success
- [ ] docker-compose up runs correctly
- [ ] Health check endpoint responds
- [ ] Environment variables documented (.env.example)
- [ ] Port mapping verified
- [ ] Volume mounts verified

### Local Development Environment
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Development server can start
- [ ] Hot reload working
- [ ] External service connections (DB, API, etc.)

## Command Reference

### Docker
```bash
# Build
docker build -t <image-name> .
docker-compose build

# Run
docker-compose up -d
docker-compose logs -f <service>

# Clean up
docker-compose down
docker system prune -f
```

### Node.js
```bash
# Dependencies
npm install
npm ci  # For CI environments (clean install)

# Run
npm run start:dev   # Development
npm run start:prod  # Production
npm run build       # Build
```

### Python
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Dependencies
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload --port 8000
```

### Process Management
```bash
# Check port
lsof -i :3000
netstat -tulpn | grep :3000

# Kill process
pkill -f "node"
pkill -f "uvicorn"

# Background execution
nohup npm run start &
```

## Output Format

After skill execution, provide the following information:

```markdown
## Environment Status

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| NestJS | 3000 | ✅ Running | API server |
| Python | 8001 | ✅ Running | Seasonal service |
| Docker | - | ❌ Not running | Desktop required |

## Execution Commands

\`\`\`bash
# Start all services
./scripts/start-all.sh

# Individual services
cd server && npm run start:dev
cd python-service && source venv/bin/activate && uvicorn app.main:app
\`\`\`

## Environment Variable Check

- ✅ OPENAI_API_KEY: Configured
- ❌ DATABASE_URL: Not configured (required)
- ⚠️ PYTHON_SERVICE_URL: Using default (http://localhost:8001)
```

## Usage Examples

```
User: "Start the server locally"
User: "Check the deployment scripts"
User: "Verify the docker-compose configuration"
User: "Set up the development environment"
```
