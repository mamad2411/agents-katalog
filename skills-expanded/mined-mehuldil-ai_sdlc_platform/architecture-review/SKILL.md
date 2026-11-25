# /project:architecture-review

**Interactive Architecture Feasibility & ADR Review**

Works in: Cursor IDE chat + Claude Code + CLI

## Usage

```
/project:architecture-review AB#123
/project:architecture-review AB#123 --role=backend --stack=java
/project:architecture-review AB#123 --create-adr
```

## What This Does

1. **Loads story** acceptance criteria and NFRs
2. **Assesses architectural implications** (scalability, data model, APIs)
3. **Asks architecture questions** (sync vs async, DB choices, service boundaries)
4. **Detects risks** (external dependency, tech debt, compliance)
5. **Creates Architecture Decision Record (ADR)** if needed
6. **Validates NFR feasibility** (latency, throughput, availability targets)

## Interactive Flow

```
User: /project:architecture-review AB#123 --role=backend

Claude: 🏗️ Architecture Review & Feasibility

✅ STORY LOADED:
  Story: Multi-language signup API (AB#12346)
  AC: 8 items (phone validation, OTP, profile setup)
  NFRs: P95 <200ms, 99.9% availability, >1000 RPS

🤔 ARCHITECTURE QUESTIONS:

1. OTP Delivery Method?
   Context: AC-02 requires OTP validation
   Options:
     [1] SMS via Twilio
     [2] In-app JWT token
     [3] Hybrid (SMS primary, app fallback)
   Impact: [1] = external dependency, [2] = simpler but less secure, [3] = most robust

2. Language Pack Strategy?
   Context: AC-03 requires 5 languages
   Options:
     [1] Static JSON files in app/code
     [2] Dynamic CDN-served bundles
     [3] Fetch from i18n service at runtime
   Impact: [1] = no latency, larger bundle; [2] = dynamic, CDN cost; [3] = most flexible

3. Database Normalization?
   Context: User profile table will store language preference + settings
   Options:
     [1] Single user_profile table (denormalized)
     [2] user_profile + user_localization (normalized)
     [3] Document-based (MongoDB) for flexibility
   Impact: [1] = simpler queries, higher storage; [2] = multiple joins, cleaner; [3] = schema-less

4. API Synchronicity?
   Context: Signup flow involves 3+ steps (phone, OTP, profile)
   Options:
     [1] Synchronous REST endpoints (3 API calls)
     [2] Orchestrated workflow service (1 call, service handles steps)
     [3] Event-driven async pipeline (Kafka topics)
   Impact: [1] = client complexity, but simple backend; [2] = centralized logic; [3] = decoupled, harder to debug

Answer questions to finalize architecture:

User: [1] SMS via Twilio
User: [2] Dynamic CDN-served bundles  
User: [2] Normalized with user_localization table
User: [2] Orchestrated workflow service

✓ Captured decisions.

🎯 ARCHITECTURE SUMMARY:

- OTP: SMS via Twilio (external dependency noted)
- i18n: CDN-served dynamic bundles
- Database: user_profile + user_localization (normalized)
- API: Orchestrated workflow service (single endpoint)

⚠️ RISKS DETECTED:

1. External Dependency: Twilio
   Mitigation: Implement fallback in-app OTP, retry logic
   ADR Needed: "OTP Provider Strategy"

2. CDN Cost: Language bundle delivery
   Mitigation: Version bundles, cache aggressively
   ADR Needed: "i18n Bundle Distribution Strategy"

3. Complex Workflow Orchestration
   Mitigation: Use step-functions or workflow engine
   ADR Needed: "Signup Workflow Orchestration Pattern"

CREATE ADRS FOR ARCHITECTURE DECISIONS?
  [1] Yes, create all 3 ADRs
  [2] Create selected ADRs
  [3] Preview first
  [4] Skip, architect will create manually

User: [1]

✓ Created ADR-001: OTP Provider Strategy
✓ Created ADR-002: i18n Bundle Distribution
✓ Created ADR-003: Signup Workflow Orchestration
✓ Saved architecture decisions to .sdlc/memory/architecture-review-AB#123.md

VALIDATE NFR FEASIBILITY?
  [1] Yes, run feasibility analysis
  [2] Skip for now
  [3] Ask me about load testing

User: [1]

📊 NFR FEASIBILITY ANALYSIS:

| NFR | Target | Assessment | Risk | Recommendation |
|-----|--------|-----------|------|---|
| P95 Latency <200ms | 200ms | ✓ FEASIBLE | Low | Cache language packs, optimize Twilio calls |
| Availability 99.9% | 99.9% | ⚠️ AT RISK | Medium | Twilio SLA only 99.9%, need fallback |
| Throughput >1000 RPS | 1000 RPS | ✓ FEASIBLE | Low | Workflow service needs horizontal scaling |

Next?
  [1] Post architecture review to ADO
  [2] Modify decisions and re-assess
  [3] Cancel

User: [1]

✓ Posted architecture review comment to AB#123
✓ Linked ADRs to story
✓ Architecture review complete
```

## CLI Mode

```bash
# Interactive
$ sdlc skill architecture-review AB#123 --role=backend

# Create ADRs automatically
$ sdlc skill architecture-review AB#123 --create-adr

# Batch review across sprint
$ sdlc skill architecture-review --sprint=12 --auto-create
```

## Skill: nfr-validator

Validates that NFRs are:
- Concrete (e.g., "P95 <200ms" not "fast")
- Measurable (testable, observable)
- Realistic (considering stack constraints)
- Documented in story
- Cross-checked against org defaults (see rules/nfr-targets.md)

## ADO Outcomes

- **ADR Creation**: Numbered ADRs for major architectural decisions
- **Feasibility Assessment**: Linked as comment with risk matrix
- **Tagging**: `adr:required`, `architecture:reviewed` tags added
- **Follow-up**: Posts gaps/risks as ADO comment (user provides notes in chat before posting)

## G4 Gate Clear Conditions

Gate G4 is CLEAR when:
- All architecture questions answered and documented
- ADRs created for major decisions (3+ options evaluated)
- NFR feasibility validated (no "at risk" items without mitigation)
- No blocking dependencies discovered
- Architect has reviewed and commented "approved"

## Next Commands

- `/project:system-design AB#123` - Create detailed system design
- `/project:code-review AB#123` - Review code for architecture alignment
- `/project:sprint-planning AB#123` - Plan implementation approach

---

## Model & Token Budget
- **Model Tier:** Sonnet or Opus (complex architecture decisions)
- Input: ~2.5K tokens (story + requirements)
- Output: ~3K tokens (questions + ADRs + feasibility)

