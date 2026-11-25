---
name: system-design-doc
description: Create comprehensive system design documents with architecture diagrams, component specs, data flows, and scaling strategies.
argument-hint: [system requirements, scale, constraints]
allowed-tools: Read, Write
---

# System Design Document

Create production-grade system design docs that communicate architecture clearly to engineers, stakeholders, and future maintainers. Not vague boxes — concrete components, data flows, API contracts, and scaling strategies.

## Process

1. **Define requirements.** Functional (what it does), non-functional (scale, latency, availability).
2. **Estimate scale.** Users, requests/sec, data volume, growth rate.
3. **Design high-level.** Major components, data flow, external dependencies.
4. **Detail components.** Tech stack, API contracts, database schema.
5. **Plan scaling.** Bottlenecks, caching, sharding, replication.
6. **Address failures.** Single points of failure, disaster recovery.
7. **Document decisions.** Trade-offs, alternatives considered, why chosen.

## Output Format

### System Design: [System Name]

**Purpose:** [One sentence]  
**Scale:** [Users, QPS, data volume]  
**SLA:** [Latency p99, availability %]  
**Key Constraints:** [Budget, compliance, legacy systems]

---

## Example: URL Shortener

### Requirements

**Functional:**
- Shorten URLs (POST /shorten → short URL)
- Redirect (GET /{short} → original URL)
- Custom aliases (optional)
- Analytics (click count, referrers)

**Non-Functional:**
- **Scale:** 100M URLs created/month, 1B redirects/month
- **Latency:** p99 < 50ms for redirects
- **Availability:** 99.9% uptime
- **Data Retention:** URLs never expire

### Capacity Estimation

**Storage:**
- 100M URLs/month × 12 months = 1.2B URLs/year
- Assuming 500 bytes per URL entry
- Storage needed: 1.2B × 500 bytes = 600 GB/year
- 5-year projection: 3 TB

**Traffic:**
- Writes: 100M/month ÷ (30 days × 86,400s) ≈ 40 writes/sec
- Reads: 1B/month ÷ (30 days × 86,400s) ≈ 400 reads/sec
- Read/Write ratio: 10:1

**Bandwidth:**
- Write: 40 req/s × 500 bytes = 20 KB/s
- Read: 400 req/s × 500 bytes = 200 KB/s
- Negligible bandwidth

### High-Level Design

```
┌─────────┐
│  Client │
└────┬────┘
     │
     ↓
┌─────────────────────────────────────┐
│        Load Balancer (NGINX)        │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ↓                     ↓
┌─────────┐         ┌─────────┐
│  API 1  │   ...   │  API N  │  (Stateless, Horizontal Scaling)
└────┬────┘         └────┬────┘
     │                   │
     └──────────┬────────┘
                ↓
         ┌──────────────┐
         │  Redis Cache │  (Read-through cache)
         └──────┬───────┘
                ↓
         ┌──────────────┐
         │  PostgreSQL  │  (Primary storage)
         └──────────────┘
```

### Component Details

#### API Server (FastAPI)
**Responsibility:** Handle requests, validation, business logic

**Endpoints:**
```
POST /api/shorten
  Request: { "url": "https://example.com/very/long/url" }
  Response: { "short_url": "https://short.ly/abc123" }

GET /{short_id}
  Response: 302 Redirect to original URL

GET /api/stats/{short_id}
  Response: { "clicks": 1234, "created_at": "..." }
```

**Tech Stack:** Python 3.11, FastAPI, uvicorn  
**Instances:** 5 (auto-scaled 3-10)  
**Resources:** 500m CPU, 512Mi RAM per instance

#### Database (PostgreSQL)
**Schema:**
```sql
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_id VARCHAR(7) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    clicks BIGINT DEFAULT 0
);

CREATE INDEX idx_urls_short_id ON urls(short_id);
```

**Sizing:**
- Instance: PostgreSQL 15, 4 vCPU, 16 GB RAM
- Storage: 1 TB SSD (room for growth)
- Replication: 1 primary + 2 read replicas

#### Cache (Redis)
**Purpose:** Cache URL mappings (read-heavy workload)

**Data Structure:**
```
Key: "url:{short_id}"
Value: "https://example.com/original"
TTL: 24 hours
```

**Sizing:**
- Instance: 8 GB RAM
- Hit rate target: > 90%
- Eviction: LRU

**Cache Strategy:**
```python
def redirect(short_id: str):
    # Check cache
    cached = redis.get(f"url:{short_id}")
    if cached:
        increment_clicks_async(short_id)
        return redirect(cached)
    
    # Cache miss: query DB
    url = db.query(URL).filter_by(short_id=short_id).one()
    
    # Store in cache
    redis.setex(f"url:{short_id}", 86400, url.original_url)
    
    increment_clicks_async(short_id)
    return redirect(url.original_url)
```

### Short ID Generation

**Algorithm:** Base62 encoding of auto-increment ID

```python
import string

BASE62 = string.ascii_letters + string.digits  # a-zA-Z0-9

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    
    result = []
    while num:
        num, rem = divmod(num, 62)
        result.append(BASE62[rem])
    
    return ''.join(reversed(result))

# Example:
# ID 1 → "b"
# ID 62 → "ba"
# ID 1000000 → "4c92"
```

**Collision:** None (auto-increment guarantees uniqueness)  
**Length:** 7 chars supports 62^7 = 3.5 trillion URLs

### Data Flow

**Create Short URL:**
```
1. Client → POST /api/shorten → API
2. API → Validate URL format
3. API → INSERT into PostgreSQL → Get auto-increment ID
4. API → Encode ID to base62 → short_id
5. API → Return short URL
```

**Redirect:**
```
1. Client → GET /{short_id} → API
2. API → Check Redis cache → HIT: Return original URL
3. (Cache MISS) → Query PostgreSQL
4. API → Store in Redis (24h TTL)
5. API → Async: Increment click counter
6. API → 302 Redirect to original URL
```

### Scaling Strategies

**Bottleneck 1: Database Writes**
- **Current:** 40 writes/sec (well below PostgreSQL limit)
- **Future (10x):** 400 writes/sec
- **Solution:** Database vertical scaling (sufficient) or write sharding if needed

**Bottleneck 2: Database Reads**
- **Current:** 400 reads/sec
- **Mitigated:** Redis cache (90%+ hit rate) → 40 DB reads/sec
- **Future:** Add read replicas if needed

**Bottleneck 3: API Instances**
- **Current:** 5 instances @ 80 req/s each = 400 req/s
- **Solution:** Horizontal autoscaling (HPA) 3-10 instances

### Failure Scenarios

**API Server Down:**
- **Impact:** Load balancer removes from pool
- **Mitigation:** Min 3 instances, auto-restart
- **Recovery:** < 30 seconds

**Database Primary Down:**
- **Impact:** Writes fail, reads served from replicas
- **Mitigation:** Promote replica to primary (auto-failover)
- **Recovery:** 1-2 minutes

**Redis Down:**
- **Impact:** Higher DB load, slower redirects
- **Mitigation:** Graceful degradation (direct DB queries)
- **Recovery:** Cache warmup after restart

**Full Region Outage:**
- **Impact:** Service unavailable
- **Mitigation:** Multi-region deployment (future)
- **Recovery:** DNS failover to backup region

### Monitoring

**Metrics:**
```
- Request rate (req/s)
- Latency (p50, p95, p99)
- Error rate (%)
- Cache hit rate (%)
- Database connections (active, idle)
- Database query time (ms)
```

**Alerts:**
- p99 latency > 100ms
- Error rate > 1%
- Cache hit rate < 80%
- Database connections > 80% max

### API Rate Limiting

```python
# Per-IP rate limit: 100 requests/minute
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/shorten")
@limiter.limit("100/minute")
def shorten_url(request: Request, url: URLRequest):
    ...
```

### Security

**Input Validation:**
- Validate URL format (regex)
- Block malicious domains (blocklist)
- Sanitize custom aliases (alphanumeric only)

**DDoS Protection:**
- CloudFlare in front
- Rate limiting per IP
- CAPTCHA for suspicious traffic

**Data Protection:**
- HTTPS only
- No PII stored
- Anonymized analytics

### Cost Estimation (AWS)

| Component | Type | Cost/Month |
|-----------|------|------------|
| API Servers | 5× t3.small | $100 |
| PostgreSQL | db.t3.large | $150 |
| Redis | t3.medium | $50 |
| Load Balancer | ALB | $25 |
| Data Transfer | 100 GB/month | $10 |
| **Total** | | **$335/month** |

### Alternative Designs Considered

**Alternative 1: Hash-Based ID**
- **Pros:** Deterministic, no DB lookup for duplicate URLs
- **Cons:** Collision risk, longer IDs
- **Decision:** Rejected (auto-increment simpler, safer)

**Alternative 2: NoSQL (DynamoDB)**
- **Pros:** Infinite scaling, managed
- **Cons:** Higher cost, more complex queries
- **Decision:** Rejected (PostgreSQL sufficient for scale, lower cost)

**Alternative 3: Serverless (Lambda)**
- **Pros:** No server management, pay-per-use
- **Cons:** Cold start latency, cost at scale
- **Decision:** Rejected (predictable traffic, containers more economical)

### Future Enhancements

**Phase 2 (6 months):**
- Custom domains (vanity URLs)
- QR code generation
- Link expiration

**Phase 3 (12 months):**
- Analytics dashboard
- A/B testing (multiple destinations)
- Geographic routing

### Deployment Plan

**Week 1:** Infrastructure setup (PostgreSQL, Redis, K8s cluster)  
**Week 2:** API development and testing  
**Week 3:** Load testing, performance tuning  
**Week 4:** Beta launch (10% traffic), monitoring  
**Week 5:** Full launch (100% traffic)

## Rules

- Requirements must specify numbers — "high traffic" is vague, "1000 req/s" is concrete.
- Capacity estimation is mandatory — storage, bandwidth, cost projections.
- Component diagrams must show data flow direction — arrows matter.
- Every component needs tech stack specified — not "database", but "PostgreSQL 15".
- Single points of failure must be identified and mitigated — no "hope it doesn't fail".
- Trade-offs must be documented — why you chose X over Y.
- Failure scenarios must include recovery time — "failover happens" is not enough.
- Monitoring and alerting are not optional — define SLOs and alert thresholds.
- Cost estimation required for production systems — surprises in AWS bills are bad.
- API contracts must be concrete — actual request/response JSON, not descriptions.
