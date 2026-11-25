# /project:system-design

**Interactive System & API Design**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:system-design AB#123
/project:system-design AB#123 --role=backend --variant=java
/project:system-design AB#123 --create-api-spec
```

## What This Does

1. **Loads acceptance criteria** from story
2. **Asks design questions** (data model, APIs, service boundaries)
3. **Generates data model** (ER diagram, schemas)
4. **Creates API specifications** (OpenAPI 3.1 format)
5. **Documents deployment strategy** (containers, scaling, monitoring)
6. **Creates design ADR** if major decisions made

## Interactive Flow

```
User: /project:system-design AB#123 --role=backend

Claude: 📐 System & API Design

✅ STORY LOADED:
  Story: Multi-language signup orchestration
  AC: 8 items (phone, OTP, profile, language selection)
  Architecture Decisions: Twilio SMS, CDN i18n, workflow service

📊 DATA MODEL QUESTIONS:

1. User Profile Table Structure?
   
   Option A: Monolithic
   ```
   users (id, phone, language, first_name, last_name, created_at, ...)
   ```
   
   Option B: Normalized with Localization
   ```
   users (id, phone, language_pref, created_at)
   user_profiles (id, user_id, first_name, last_name, bio, ...)
   user_localization (id, user_id, language, ui_language, ...)
   ```

   Your architecture chose B. Confirm?
     [1] Yes, proceed with normalized schema
     [2] Adjust schema
     [3] Use document DB instead

User: [1]

✓ Confirmed normalized schema.

2. OTP Storage & Validation?
   
   Options:
     [1] In-memory cache (Redis, TTL 10min)
     [2] Database table with TTL
     [3] JWT tokens (stateless)

   Recommendation: [1] for performance (matches P95 <200ms target)

User: [1]

✓ OTP via Redis.

3. Internationalization Storage?
   
   Options:
     [1] Database translations (i18n_keys + i18n_translations tables)
     [2] CDN JSON bundles (static files)
     [3] Hybrid (DB for user-editable, CDN for static)

   Your architecture chose [2]. Confirm?
     [1] Yes, CDN bundles
     [2] Change to hybrid
     [3] Change to DB

User: [1]

✓ CDN bundles for i18n.

📊 GENERATED DATA MODEL:

Tables:
  • users (id, phone, password_hash, language_pref, created_at, updated_at)
  • user_profiles (id, user_id, first_name, last_name, ...)
  • user_localization (id, user_id, language, ui_language, timezone)
  • otp_cache (id, user_id, code, expires_at, attempts)
  • language_bundles (id, language, version, bundle_url, updated_at)

Relationships:
  • users 1-to-1 user_profiles
  • users 1-to-many user_localization
  • users 1-to-many otp_cache

🔌 API DESIGN:

REST Endpoints:
  
  POST /api/v1/signup/initiate
    Request: { phone: "+1234567890", language: "es" }
    Response: { session_id: "...", otp_sent_at: "..." }
  
  POST /api/v1/signup/verify-otp
    Request: { session_id: "...", code: "123456" }
    Response: { session_token: "...", next_step: "profile" }
  
  POST /api/v1/signup/profile
    Request: { session_token: "...", first_name: "...", last_name: "..." }
    Response: { user_id: "...", auth_token: "...", status: "active" }
  
  GET /api/v1/languages
    Response: { languages: [{ code: "en", name: "English", ... }, ...] }

OpenAPI Spec: See below

📝 DEPLOYMENT STRATEGY:

Containers:
  • signup-service (Node.js, replicas: 3)
  • workflow-orchestrator (Java, replicas: 2)
  • otp-validator (Python, replicas: 1)

Infrastructure:
  • Kubernetes (EKS)
  • RDS PostgreSQL (Multi-AZ)
  • ElastiCache Redis (for OTP cache + sessions)
  • CloudFront CDN (for language bundles)

Scaling:
  • Horizontal: Add replicas under load (HPA triggers at CPU 70%)
  • Database: Read replicas for analytics queries
  • Cache: Redis cluster with 3-node setup

Monitoring:
  • Metrics: Latency (p50/p95/p99), error rate, RPS
  • Logs: CloudWatch + ELK stack
  • Alerts: P95 >200ms, error rate >0.1%, availability <99.9%

CREATE API SPEC (OpenAPI 3.1)?
  [1] Yes, generate OpenAPI spec
  [2] Preview design first
  [3] Skip, I'll create manually

User: [1]

✓ Generated OpenAPI 3.1 specification
✓ Saved data model to .sdlc/memory/system-design-AB#123-datamodel.md
✓ Saved API spec to .sdlc/memory/system-design-AB#123-openapi.yaml
✓ Saved deployment strategy to .sdlc/memory/system-design-AB#123-deployment.md

REVIEW & POST TO ADO?
  [1] Yes, post design review
  [2] Edit design first
  [3] Cancel

User: [1]

✓ Posted system design to AB#123
✓ Linked OpenAPI spec and data model
✓ System design review complete
```

## CLI Mode

```bash
$ sdlc skill system-design AB#123 --role=backend --variant=java
$ sdlc skill system-design AB#123 --create-api-spec --create-erd
$ sdlc skill system-design --sprint=12 --auto-create
```

## Outputs Generated

- **Data Model**: ER diagram + table schemas with constraints
- **OpenAPI 3.1**: Full REST API specification with examples
- **Database Migrations**: v1__initial_schema.sql with migrations
- **Deployment Strategy**: Container configuration, scaling policy, monitoring
- **ADO Documentation**: Links to all design artifacts

## G4 Gate Clear Conditions (if not completed in Architecture Review)

Gate requires:
- Data model diagram and schema definitions
- OpenAPI specification (all endpoints documented)
- Deployment architecture (containers, infrastructure, scaling policy)
- No NFR conflicts identified

## Next Commands

- `/project:sprint-planning AB#123` - Plan sprint implementation
- `/project:implementation AB#123` - Begin development
- `/project:code-review AB#123` - Review code against design

---

## Model & Token Budget
- **Model Tier:** Sonnet (design generation)
- Input: ~2K tokens (story + architecture decisions)
- Output: ~3.5K tokens (data model + API spec + deployment)

