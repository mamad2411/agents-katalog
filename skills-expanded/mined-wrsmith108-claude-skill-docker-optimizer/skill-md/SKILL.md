# Docker Optimizer Skill

Analyzes and optimizes Dockerfiles for faster builds and smaller images.

## Trigger Phrases

- "slow docker build"
- "optimize Dockerfile"
- "layer caching"
- "reduce image size"
- "docker build taking too long"
- "docker optimization"
- "dockerfile performance"
- "image too large"

## Capabilities

1. **Layer Order Analysis** - Detects inefficient layer ordering that breaks cache
2. **Multi-stage Build Detection** - Identifies opportunities for multi-stage builds
3. **Base Image Optimization** - Recommends slim/alpine variants
4. **Production Dependencies** - Ensures dev dependencies are excluded
5. **Package Manager Cleanup** - Verifies apt-get/apk cleanup
6. **Build Time Estimation** - Estimates time savings from optimizations
7. **Image Size Estimation** - Estimates size reduction from optimizations

## Usage

### Command Line

```bash
# Analyze Dockerfile in current directory
npx tsx scripts/index.ts

# Analyze specific Dockerfile
npx tsx scripts/index.ts /path/to/Dockerfile

# JSON output for programmatic use
npx tsx scripts/index.ts --json
```

## Optimization Checks

| Check | Description | Impact |
|-------|-------------|--------|
| Layer order | COPY source after npm install | High |
| Multi-stage build | Separate build and runtime stages | High |
| Slim base image | Use node:X-slim or alpine | Medium |
| Production deps | --production flag on npm ci | Medium |
| Package cleanup | apt-get clean after install | Medium |
| .dockerignore | Exclude node_modules, .git | Medium |
| WORKDIR usage | Explicit WORKDIR instead of cd | Low |
| Non-root user | Run as non-root for security | Low |

## Requirements

- Node.js 18+
- tsx (for TypeScript execution)
