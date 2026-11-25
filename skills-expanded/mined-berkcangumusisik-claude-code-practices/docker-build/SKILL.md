---
name: docker-build
description: Creates or optimizes a Dockerfile for the current project
user-invocable: true
allowed-tools: Read Glob Bash Edit
effort: medium
---

## Docker Setup

1. Detect project type:
```bash
cat package.json 2>/dev/null | grep '"main"\|"start"\|"scripts"' -A 5
ls -la | grep -E "Dockerfile|docker-compose|\.dockerignore"
```

2. If Dockerfile exists, review it for:
   - Multi-stage build (build stage vs runtime stage)
   - Layer caching order (dependencies before source)
   - Running as non-root user
   - `.dockerignore` completeness
   - Image size optimization

3. If no Dockerfile, generate one following best practices:

```dockerfile
# Multi-stage: build → runtime
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS runtime
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

4. Also create/update `.dockerignore`:
```
node_modules
dist
.env*
.git
coverage
*.test.*
```

5. Show `docker build` and `docker run` commands to test.
