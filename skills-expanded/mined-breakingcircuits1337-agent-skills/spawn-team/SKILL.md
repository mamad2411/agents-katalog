---
name: spawn-team
description: Orchestrates a specialized agent team for rapid full-stack application development. Use when building complete web applications from scratch, MVP development, or rapid prototyping with modern tech stacks.
---

# Spawn Team - Full-Stack Application Development

Orchestrates a specialized agent team to rapidly build complete full-stack applications with modern architectures, best practices, and deployment-ready configurations.

## When to Use This Skill

- Building complete web applications from scratch
- MVP development with tight deadlines
- Rapid prototyping and proof-of-concepts
- Startup product development
- Full-stack rewrites or migrations
- Learning full-stack development patterns
- Creating SaaS applications
- Building e-commerce platforms

## Team Architecture

### Core Team Members

1. **Product Architect** - Requirements analysis & system design
2. **Backend Specialist** - API, database, and server architecture
3. **Frontend Specialist** - UI/UX, component architecture, and client-side logic
4. **DevOps Engineer** - Deployment, CI/CD, and infrastructure
5. **Quality Assurance** - Testing strategy and implementation
6. **Security Specialist** - Security patterns and vulnerability assessment

### Tech Stack Specializations

#### Backend Specializations
- **Node.js/TypeScript** - Express, Fastify, NestJS
- **Python** - FastAPI, Django, Flask
- **Go** - Gin, Echo, Fiber
- **Rust** - Axum, Actix-web
- **Java/Kotlin** - Spring Boot, Ktor

#### Frontend Specializations
- **React** - Next.js, Remix, Vite
- **Vue** - Nuxt 3, Vue 3 + Vite
- **Angular** - Angular 17+ with standalone components
- **Svelte** - SvelteKit
- **React Native** - Mobile apps

#### Database Specializations
- **PostgreSQL** - Primary relational database
- **MongoDB** - Document store
- **Redis** - Caching and sessions
- **Prisma/TypeORM** - Database ORMs
- **Supabase/PlanetScale** - Managed databases

#### Deployment Specializations
- **Docker** - Containerization
- **AWS** - ECS, Lambda, RDS, S3
- **Vercel/Netlify** - Frontend hosting
- **Railway/Render** - Full-stack hosting
- **Kubernetes** - Complex orchestration

## Development Phases

### Phase 1: Requirements & Architecture (Product Architect)

```bash
# Start with requirements gathering
skill spawn-team --phase requirements --app-description "Build a task management app for teams"

# Generate technical specification
skill spawn-team --phase architecture --tech-stack "Next.js + PostgreSQL + Prisma + Tailwind"
```

**Outputs:**
- Technical specification document
- Database schema design
- API endpoint documentation
- Component architecture diagram
- Deployment strategy

### Phase 2: Backend Development (Backend Specialist)

```bash
# Initialize backend project
skill spawn-team --phase backend --framework "Next.js API routes" --database "PostgreSQL"

# Generate database schema and migrations
skill spawn-team --task database --schema "teams, users, tasks, projects"

# Create API endpoints
skill spawn-team --task api --endpoints "auth, teams, tasks, projects"
```

**Features Generated:**
- Authentication system (JWT, session management)
- Database schema and migrations
- REST/GraphQL API endpoints
- Input validation and error handling
- Database connection pooling
- Environment configuration

### Phase 3: Frontend Development (Frontend Specialist)

```bash
# Initialize frontend project
skill spawn-team --phase frontend --framework "Next.js" --styling "Tailwind CSS"

# Generate core components
skill spawn-team --task components --library "shadcn/ui" --types "auth, dashboard, forms"

# Create page templates
skill spawn-team --task pages --templates "landing, dashboard, settings"
```

**Features Generated:**
- Authentication flows (login, signup, reset)
- Dashboard and navigation
- Responsive layouts
- Form components with validation
- State management (Zustand/Context)
- API integration hooks

### Phase 4: Integration & Testing (QA Specialist)

```bash
# Set up testing framework
skill spawn-team --phase testing --framework "Jest + Cypress"

# Generate test suites
skill spawn-team --task tests --coverage "unit, integration, e2e"
```

**Testing Coverage:**
- Unit tests for business logic
- API integration tests
- Component testing
- E2E user flows
- Performance testing
- Security testing

### Phase 5: Deployment & DevOps (DevOps Engineer)

```bash
# Configure deployment
skill spawn-team --phase deployment --target "Vercel + Railway"

# Set up CI/CD
skill spawn-team --task cicd --platform "GitHub Actions"
```

**Infrastructure Generated:**
- Docker configuration
- Environment variable management
- CI/CD pipelines
- Database provisioning
- SSL certificates
- Monitoring setup

## Quick Start Commands

### Simple MVP (React + Node.js)
```bash
# One-command MVP generation
skill spawn-team --create mvp \
  --name "task-manager" \
  --stack "Next.js + PostgreSQL + Prisma + Tailwind" \
  --features "auth, teams, tasks, real-time"
```

### Full SaaS Application
```bash
# Enterprise-ready SaaS
skill spawn-team --create saas \
  --name "project-platform" \
  --stack "Next.js + AWS + Stripe + Supabase" \
  --features "auth, billing, teams, projects, analytics, admin"
```

### Mobile + Web App
```bash
# Cross-platform application
skill spawn-team --create mobile \
  --name "social-app" \
  --stack "React Native + Node.js + MongoDB" \
  --features "auth, profiles, posts, chat, notifications"
```

## Generated Project Structure

```
your-app/
├── README.md                 # Complete documentation
├── docker-compose.yml        # Local development
├── .github/workflows/        # CI/CD pipelines
├── apps/
│   ├── web/                 # Frontend application
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utility functions
│   │   └── styles/         # Global styles
│   ├── api/                # Backend API
│   │   ├── src/
│   │   │   ├── controllers/ # Route handlers
│   │   │   ├── services/   # Business logic
│   │   │   ├── models/     # Database models
│   │   │   ├── middleware/ # Express middleware
│   │   │   └── utils/      # API utilities
│   │   ├── prisma/         # Database schema
│   │   └── tests/          # API tests
│   └── mobile/             # React Native app
├── packages/
│   ├── shared/             # Shared types and utils
│   ├── ui/                 # Component library
│   └── config/             # ESLint, TypeScript configs
├── infrastructure/
│   ├── terraform/          # Infrastructure as code
│   ├── docker/             # Dockerfiles
│   └── k8s/                # Kubernetes manifests
└── docs/                   # Project documentation
```

## Feature Templates

### Authentication System
```bash
skill spawn-team --feature auth \
  --methods "email, oauth" \
  --providers "Google, GitHub" \
  --roles "admin, user, guest"
```

**Generated:**
- JWT token management
- Password hashing with bcrypt
- OAuth integration
- Role-based access control
- Session management
- Password reset flows
- Email verification

### Real-time Features
```bash
skill spawn-team --feature realtime \
  --technology "WebSocket" \
  --features "chat, notifications, presence"
```

**Generated:**
- WebSocket server setup
- Real-time event handling
- Connection management
- Room-based messaging
- Live notifications
- Online presence tracking

### Payment Integration
```bash
skill spawn-team --feature payments \
  --provider "Stripe" \
  --models "subscription, one-time"
```

**Generated:**
- Stripe webhook handlers
- Subscription management
- Payment processing
- Invoice generation
- Customer portal
- Webhook security

### Admin Dashboard
```bash
skill spawn-team --feature admin \
  --permissions "crud, analytics, users"
```

**Generated:**
- Admin authentication
- User management interface
- Analytics dashboard
- System health monitoring
- Content moderation
- Bulk operations

## Quality Standards

### Code Quality
- TypeScript throughout (95%+ type coverage)
- ESLint + Prettier configuration
- Husky pre-commit hooks
- Automated code reviews
- Dependency vulnerability scanning

### Testing Standards
- 80%+ code coverage target
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
- Performance benchmarks
- Security testing suite

### Security Practices
- OWASP security guidelines
- Input validation and sanitization
- Rate limiting and DDoS protection
- Security headers (CSP, HSTS)
- Environment variable encryption
- Regular security audits

## Deployment Patterns

### Development Environment
```bash
# Local development setup
skill spawn-team --setup dev --database "local" --services "redis, mailhog"
```

### Staging Environment
```bash
# Production-like staging
skill spawn-team --setup staging --provider "AWS" --services "RDS, ElastiCache"
```

### Production Environment
```bash
# Production deployment
skill spawn-team --setup production --provider "Vercel + Railway" --monitoring "Sentry"
```

## Monitoring & Analytics

### Application Monitoring
```bash
skill spawn-team --monitoring setup \
  --services "Sentry, LogRocket" \
  --metrics "performance, errors, user-behavior"
```

### Business Analytics
```bash
skill spawn-team --analytics setup \
  --platform "Plausible, Mixpanel" \
  --events "user-actions, conversions, retention"
```

## Customization Options

### Framework Selection
```bash
# Specify exact versions and configurations
skill spawn-team --customize \
  --frontend "Next.js 14 + App Router" \
  --backend "Node.js 20 + Express" \
  --database "PostgreSQL 15 + Prisma 5" \
  --styling "Tailwind CSS 3 + shadcn/ui"
```

### Enterprise Features
```bash
# Add enterprise-grade features
skill spawn-team --enterprise \
  --sso "SAML, OIDC" \
  --audit "comprehensive logging" \
  --compliance "GDPR, SOC2" \
  --multi-tenancy "true"
```

## Support and Maintenance

### Documentation Generation
- API documentation with OpenAPI/Swagger
- Component documentation with Storybook
- Architecture decision records (ADRs)
- Deployment runbooks
- Onboarding guides

### Maintenance Automation
- Automated dependency updates
- Security patch notifications
- Performance regression detection
- Database migration automation
- Backup and recovery procedures

## Example Workflows

### Workflow 1: Social Media MVP (2 days)
```bash
# Day 1: Backend + Auth
skill spawn-team --create mvp \
  --name "social-app" \
  --stack "Next.js + PostgreSQL + Prisma" \
  --features "auth, posts, likes, comments"

# Day 2: Frontend + Deployment
skill spawn-team --phase frontend --theme "minimal"
skill spawn-team --phase deployment --target "Vercel"
```

### Workflow 2: B2B SaaS Platform (1 week)
```bash
# Days 1-2: Architecture + Core Features
skill spawn-team --create saas \
  --name "crm-platform" \
  --stack "Next.js + AWS + Stripe" \
  --features "auth, teams, billing, admin"

# Days 3-4: Advanced Features
skill spawn-team --feature analytics --provider "Mixpanel"
skill spawn-team --feature notifications --channels "email, push"

# Days 5-7: Testing + Deployment
skill spawn-team --phase testing --coverage "90%"
skill spawn-team --phase deployment --target "production"
```

## Integration with Existing Skills

This skill orchestrates and coordinates with other specialized skills:
- **webapp-testing** - For E2E testing setup
- **api-design-principles** - For API architecture
- **browser-automation** - For testing workflows
- **mcp-integration** - For external service connections
- **documentation-templates** - For project documentation

## Troubleshooting

### Common Issues
- **Port conflicts**: Use `skill spawn-team --fix ports`
- **Database connection**: Run `skill spawn-team --doctor database`
- **Environment variables**: Use `skill spawn-team --setup env`
- **Deployment failures**: Check `skill spawn-team --logs deployment`

### Performance Optimization
```bash
# Analyze and optimize performance
skill spawn-team --optimize performance --target "bundle-size, database-queries"
```

## Resources

- **templates/mvp-structure/**: Complete MVP project templates
- **patterns/authentication/**: Auth implementation patterns
- **patterns/real-time/**: WebSocket and real-time features
- **deployment/docker/**: Production-ready Docker configs
- **scripts/database-migrations/**: Migration management tools
- **testing/e2e-flows/**: Common E2E test scenarios
- **security/checklist.md**: Security review checklist
- **performance/optimization.md**: Performance tuning guide