# CLAUDE.md - n8n Self-Hosted Development Guidelines

## Project Overview
Self-hosted n8n automation platform with PostgreSQL database.
- **Local Development**: Docker Compose
- **Production**: Kubernetes (AWS EKS) with Helm charts

## Build Commands

### Local Development (Docker Compose)
- Start services: `docker-compose up -d`
- Stop services: `docker-compose down`
- View logs: `docker-compose logs -f [service-name]`
- Update n8n: `docker-compose pull n8n && docker-compose up -d n8n`

### Kubernetes Deployment
- Validate Helm charts: `helm lint infra/deployment/{staging,production}/k8s/`
- Build Docker image: `docker build -f Dockerfile.k8s -t n8n-platform:test .`
- Deploy staging: `cd infra/deployment/staging && helm upgrade --install n8n-platform-staging k8s [options]`
- Check deployment: `kubectl get pods -n default`
- View logs: `kubectl logs -f deployment/n8n-platform-staging`

## Environment Setup
- Configure `.env` file before first run
- Required variables: POSTGRES_PASSWORD, POSTGRES_NON_ROOT_PASSWORD, N8N_BASIC_AUTH_PASSWORD, N8N_ENCRYPTION_KEY
- Generate encryption key: `openssl rand -hex 32`

## Access
- n8n Web Interface: http://localhost:5678
- PostgreSQL: localhost:5432 (user: n8n, database: n8n)

## Data Persistence
- n8n data: Docker volume `n8n-data`
- PostgreSQL data: Docker volume `postgres-data`
- n8n files: `./n8n-files/` directory

## Backup & Restore
- Backup: `docker-compose exec postgres pg_dump -U postgres n8n > backup.sql`
- Restore: `docker-compose exec -T postgres psql -U postgres n8n < backup.sql`

## Infrastructure

### Local Development
- Infrastructure code located in `infra/` directory
- Uses Docker Compose for service orchestration
- PostgreSQL initialization via `init-data.sql`

### Kubernetes (Production)
- Helm charts in `infra/deployment/{staging,production}/k8s/`
- AWS EKS clusters:
  - Staging: `f4fpay-staging-20250109` (us-east-1)
  - Production: `f4fpay-production-20230709` (us-east-1)
- ECR registry: `169829274692.dkr.ecr.ap-east-1.amazonaws.com/n8n-platform`
- Domains:
  - Staging: `staging-n8n.first4figures.com`
  - Production: `n8n.first4figures.com`
- CI/CD: GitHub Actions (`.github/workflows/`)
  - `ci.yml`: Validates Helm charts and Dockerfile
  - `deploy.yml`: Automated deployment to staging/production

## Code Style Conventions
- Docker: Follow Docker Compose best practices
- Kubernetes: Follow Helm chart best practices
- YAML: 2-space indentation for K8s manifests
- Helm templates: Use `{{- }}` for whitespace control
- Shell scripts: Use shellcheck for linting
- SQL: PostgreSQL standard formatting

## Security
- Never commit `.env` file with secrets
- Change default passwords in production
- Use HTTPS in production (configure reverse proxy for local, ingress for K8s)
- Regular backups and updates
- Kubernetes secrets passed via `helm --set` from GitHub Secrets
- Use different encryption keys for staging and production
- TLS certificates managed by cert-manager (Let's Encrypt)

## Deployment Workflow

### Staging Deployment
1. Push to `main` branch or create PR
2. CI workflow validates Helm charts and Dockerfile
3. After CI passes, deploy workflow automatically deploys to staging
4. Can also trigger via `/deploy:staging` comment on PR

### Production Deployment (Currently disabled)
1. After staging deployment succeeds
2. Production deployment runs automatically
3. Currently commented out in `.github/workflows/deploy.yml`
4. Will be enabled after staging validation

## Common Tasks

### Check Deployment Status
```bash
kubectl get pods -n default
kubectl rollout status deployment/n8n-platform-staging
kubectl get ingress
```

### View Application Logs
```bash
kubectl logs -f deployment/n8n-platform-staging
kubectl logs -f n8n-platform-staging-postgres-0
```

### Access Staging n8n
- URL: https://staging-n8n.first4figures.com
- Port-forward: `kubectl port-forward svc/n8n-platform-staging 5678:5678`

### Rollback Deployment
```bash
kubectl rollout undo deployment/n8n-platform-staging
# or
helm rollback n8n-platform-staging
```

## Documentation
- [README.md](README.md) - Quick start and local development
- [DEPLOYMENT.md](DEPLOYMENT.md) - Comprehensive Kubernetes deployment guide
- [.github/workflows/](/.github/workflows/) - CI/CD pipeline definitions
