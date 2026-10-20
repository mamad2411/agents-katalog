---
name: production-toolkit
description: Consolidated toolkit for production. Covers production-code-audit, production-scheduling
---
# Production Toolkit

## Core Capabilities
# Production Toolkit

# Production Code Audit

## Overview

Autonomously analyze the entire codebase to understand its architecture, patterns, and purpose, then systematically transform it into production-grade, corporate-level professional code. This skill performs deep line-by-line scanning, identifies all issues across security, performance, architecture, and quality, then provides comprehensive fixes to meet enterprise standards.

## When to Use This Skill

- Use when user says "make this production-ready"
- Use when user says "audit my codebase"
- Use when user says "make this professional/corporate-level"
- Use when user says "optimize everything"
- Use when user wants enterprise-grade quality
- Use when preparing for production deployment
- Use when code needs to meet corporate standards

## How It Works

### Step 1: Autonomous Codebase Discovery

**Automatically scan and understand the entire codebase:**

1. **Read all files** - Scan every file in the project recursively
2. **Identify tech stack** - Detect languages, frameworks, databases, tools
3. **Understand architecture** - Map out structure, patterns, dependencies
4. **Identify purpose** - Understand what the application does
5. **Find entry points** - Locate main files, routes, controllers
6. **Map data flow** - Understand how data moves through the system

**Do this automatically without asking the user.**

### Step 2: Comprehensive Issue Detection

**Scan line-by-line for all issues:**

**Architecture Issues:**
- Circular dependencies
- Tight coupling
- God classes (>500 lines or >20 methods)
- Missing separation of concerns
- Poor module boundaries
- Violation of design patterns

**Security Vulnerabilities:**
- SQL injection (string concatenation in queries)
- XSS vulnerabilities (unescaped output)
- Hardcoded secrets (API keys, passwords in code)
- Missing authentication/authorization
- Weak password hashing (MD5, SHA1)
- Missing input validation
- CSRF vulnerabilities
- Insecure dependencies

**Performance Problems:**
- N+1 query problems
- Missing database indexes
- Synchronous operations that should be async
- Missing caching
- Inefficient algorithms (O(n²) or worse)
- Large bundle sizes
- Unoptimized images
- Memory leaks

**Code Quality Issues:**
- High cyclomatic complexity (>10)
- Code duplication
- Magic numbers
- Poor naming conventions
- Missing error handling
- Inconsistent formatting
- Dead code
- TODO/FIXME comments

**Testing Gaps:**
- Missing tests for critical paths
- Low test coverage (<80%)
- No edge case testing
- Flaky tests
- Missing integration tests

**Production Readiness:**
- Missing environment variables
- No logging/monitoring
- No error tracking
- Missing health checks
- Incomplete documentation
- No CI/CD pipeline

### Step 3: Automatic Fixes and Optimizations

**Fix everything automatically:**

1. **Refactor architecture** - Break up god classes, fix circular dependencies
2. **Fix security issues** - Use parameterized queries, remove secrets, add validation
3. **Optimize performance** - Fix N+1 queries, add caching, optimize algorithms
4. **Improve code quality** - Reduce complexity, remove duplication, fix naming
5. **Add missing tests** - Write tests for untested critical paths
6. **Add production infrastructure** - Logging, monitoring, health checks
7. **Optimize everything** - Bundle size, images, database queries
8. **Add documentation** - README, API docs, architecture docs

### Step 4: Verify and Report

**After making all changes:**

1. Run all tests to ensure nothing broke
2. Verify all security issues are fixed
3. Measure performance improvements
4. Generate comprehensive report
5. Provide before/after metrics

## Examples

### Example 1: Autonomous Codebase Transformation

```markdown
User: @production-code-audit make this production-ready

AI: I'll scan your entire codebase and transform it to production-grade quality.

**Phase 1: Discovering Codebase** (analyzing 247 files)
- Detected: Node.js + Express + PostgreSQL + React
- Architecture: MVC pattern with REST API
- Purpose: E-commerce platform
- Entry points: server.js, src/index.tsx

**Phase 2: Scanning for Issues** (line-by-line analysis)

Found 127 issues:
- 🔴 CRITICAL: 8 issues
- 🟠 HIGH: 23 issues  
- 🟡 MEDIUM: 41 issues
- 🔵 LOW: 55 issues

**Phase 3: Fixing Issues Automatically**

🔴 CRITICAL FIXES (8/8 completed):

1. ✅ Fixed SQL injection in UserRepository.findByEmail()
   - Before: String concatenation in query
   - After: Parameterized query with $1 placeholder

2. ✅ Removed hardcoded database password from config/database.ts
   - Before: password: 'SuperSecret123!'
   - After: password: process.env.DB_PASSWORD

3. ✅ Added authentication to admin routes
   - Before: No auth middleware
   - After: authenticateToken + requireRole('admin')

4. ✅ Fixed weak password hashing (MD5 → bcrypt)
   - Before: crypto.createHash('md5')
   - After: bcrypt.hash(password, 12)

5. ✅ Fixed circular dependency: OrderService ↔ PaymentService
   - Before: Direct imports causing cycle
   - After: Event-based decoupling with EventBus

6. ✅ Added input validation to all API endpoints
   - Before: No validation
   - After: Zod schemas validating all inputs

7. ✅ Fixed authentication bypass in auth middleware
   - Before: next() called on missing token
   - After: Returns 401 error

8. ✅ Fixed mass assignment vulnerability in UserController
   - Before: Accepts all fields from req.body
   - After: Whitelist of allowed fields only

🟠 HIGH PRIORITY FIXES (23/23 completed):

9. ✅ Fixed N+1 query in OrderService.getOrdersWithItems()
   - Before: Loop with individual queries (2.8s)
   - After: Single query with joins (45ms)
   - Performance: 98% improvement

10. ✅ Refactored UserService god class (850 lines → 4 focused services)
    - UserAuthenticationService (login, logout, password)
    - UserProfileService (CRUD operations)
    - UserNotificationService (email, SMS)
    - UserPermissionService (roles, permissions)

11. ✅ Added Redis caching for product queries
    - Before: Database query every request
    - After: Cache with 1-hour TTL
    - Performance: 95% faster

12. ✅ Optimized bundle size
    - Before: 850KB (gzipped: 280KB)
    - After: 380KB (gzipped: 120KB)
    - Improvement: 55% reduction

13. ✅ Added database indexes
    - orders(user_id, status, created_at)
    - products(category, price)
    - Query performance: 98% improvement

[... 11 more high-priority fixes ...]

🟡 MEDIUM PRIORITY FIXES (41/41 completed):
[... all medium fixes ...]

🔵 LOW PRIORITY IMPROVEMENTS (55/55 completed):
[... all low improvements ...]

**Phase 4: Adding Production Infrastructure**

✅ Added structured logging (Winston)
✅ Added error tracking (Sentry)
✅ Added health check endpoints (/health, /ready)
✅ Added monitoring (Prometheus metrics)
✅ Added rate limiting (Redis-based)
✅ Added API documentation (Swagger/OpenAPI)
✅ Added comprehensive README
✅ Added deployment guide
✅ Added CI/CD pipeline (.github/workflows)

**Phase 5: Verification**

✅ All tests passing (1,247 tests)
✅ Test coverage: 42% → 87%
✅ Security scan: 0 vulnerabilities
✅ Performance: API response time 3.2s → 180ms
✅ Bundle size: 850KB → 380KB
✅ Lighthouse score: 62 → 94

**TRANSFORMATION COMPLETE**

Your codebase is now production-ready with enterprise-grade quality:

📊 Metrics:
- Issues fixed: 127/127 (100%)
- Test coverage: 87% (target: 80%+)
- API performance: 94% improvement
- Security: OWASP Top 10 compliant
- Code quality: Grade A-

📁 Files changed: 89 files
📝 Lines changed: +3,247 / -1,892

🚀 Ready for production deployment!
```

### Example 2: Automatic Security Hardening

```markdown
User: @production-code-audit secure this codebase

AI: Scanning for security vulnerabilities...

**Security Scan Complete**

Found 15 security issues:
- 🔴 CRITICAL: 5
- 🟠 HIGH: 7
- 🟡 MEDIUM: 3

**Fixing all security issues automatically...**

🔴 CRITICAL (5/5 fixed):

1. ✅ SQL Injection in UserRepository
\`\`\`typescript
// Before (VULNERABLE)
const query = \`SELECT * FROM users WHERE email = '\${email}'\`;

// After (SECURE)
const query = 'SELECT * FROM users WHERE email = $1';
await db.query(query, [email]);
\`\`\`

2. ✅ Hardcoded Secrets Removed
\`\`\`typescript
// Before (INSECURE)
const JWT_SECRET = 'my-secret-key-123';

// After (SECURE)
const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) throw new Error('JWT_SECRET required');
\`\`\`

3. ✅ Authentication Added to Admin Routes
\`\`\`typescript
// Before (VULNERABLE)
router.delete('/api/admin/users/:id', deleteUser);

// After (SECURE)
router.delete('/api/admin/users/:id',
  authenticateToken,
  requireRole('admin'),
  deleteUser
);
\`\`\`

4. ✅ Password Hashing Upgraded
\`\`\`typescript
// Before (WEAK)
const hash = crypto.createHash('md5').update(password).digest('hex');

// After (STRONG)
const hash = await bcrypt.hash(password, 12);
\`\`\`

5. ✅ Input Validation Added
\`\`\`typescript
// Before (VULNERABLE)
const user = await db.user.create({ data: req.body });

// After (SECURE)
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(12),
  name: z.string().min(2).max(100)
});
const validated = schema.parse(req.body);
const user = await db.user.create({ data: validated });
\`\`\`

**Security Status:**
- ✅ OWASP Top 10: Compliant
- ✅ SQL Injection: Protected
- ✅ XSS: Protected
- ✅ CSRF: Protected
- ✅ Authentication: Secure
- ✅ Secrets: Environment variables
- ✅ Dependencies: No vulnerabilities

🔒 Codebase is now secure and production-ready!
```

### Example 3: Performance Optimization

```markdown
User: @production-code-audit optimize performance

AI: Analyzing performance bottlenecks...

**Performance Analysis Complete**

Current metrics:
- API response time: 3.2s (target: <200ms)
- Page load time: 8.5s (target: <2s)
- Bundle size: 850KB (target: <200KB)

**Optimizing automatically...**

✅ Fixed N+1 queries (3.2s → 180ms - 94% faster)
✅ Added Redis caching (95% cache hit rate)
✅ Optimized database indexes (98% faster queries)
✅ Reduced bundle size (850KB → 380KB - 55% smaller)
✅ Optimized images (28MB → 3.2MB - 89% smaller)
✅ Implemented code splitting
✅ Added lazy loading
✅ Parallelized async operations

**Performance Results:**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| API Response | 3.2s | 180ms | 94% |
| Page Load | 8.5s | 1.8s | 79% |
| Bundle Size | 850KB | 380KB | 55% |
| Image Size | 28MB | 3.2MB | 89% |
| Lighthouse | 42 | 94 | +52 points |

🚀 Performance optimized to production standards!
```

## Best Practices

### ✅ Do This

- **Scan Everything** - Read all files, understand entire codebase
- **Fix Automatically** - Don't just report, actually fix issues
- **Prioritize Critical** - Security and data loss issues first
- **Measure Impact** - Show before/after metrics
- **Verify Changes** - Run tests after making changes
- **Be Comprehensive** - Cover architecture, security, performance, testing
- **Optimize Everything** - Bundle size, queries, algorithms, images
- **Add Infrastructure** - Logging, monitoring, error tracking
- **Document Changes** - Explain what was fixed and why

### ❌ Don't Do This

- **Don't Ask Questions** - Understand the codebase autonomously
- **Don't Wait for Instructions** - Scan and fix automatically
- **Don't Report Only** - Actually make the fixes
- **Don't Skip Files** - Scan every file in the project
- **Don't Ignore Context** - Understand what the code does
- **Don't Break Things** - Verify tests pass after changes
- **Don't Be Partial** - Fix all issues, not just some

## Autonomous Scanning Instructions

**When this skill is invoked, automatically:**

1. **Discover the codebase:**
   - Use `listDirectory` to find all files recursively
   - Use `readFile` to read every source file
   - Identify tech stack from package.json, requirements.txt, etc.
   - Map out architecture and structure

2. **Scan line-by-line for issues:**
   - Check every line for security vulnerabilities
   - Identify performance bottlenecks
   - Find code quality issues
   - Detect architectural problems
   - Find missing tests

3. **Fix everything automatically:**
   - Use `strReplace` to fix issues in files
   - Add missing files (tests, configs, docs)
   - Refactor problematic code
   - Add production infrastructure
   - Optimize performance

4. **Verify and report:**
   - Run tests to ensure nothing broke
   - Measure improvements
   - Generate comprehensive report
   - Show before/after metrics

**Do all of this without asking the user for input.**

## Common Pitfalls

### Problem: Too Many Issues
**Symptoms:** Team paralyzed by 200+ issues
**Solution:** Focus on critical/high priority only, create sprints

### Problem: False Positives
**Symptoms:** Flagging non-issues
**Solution:** Understand context, verify manually, ask developers

### Problem: No Follow-Up
**Symptoms:** Audit report ignored
**Solution:** Create GitHub issues, assign owners, track in standups

## Production Audit Checklist

### Security
- [ ] No SQL injection vulnerabilities
- [ ] No hardcoded secrets
- [ ] Authentication on protected routes
- [ ] Authorization checks implemented
- [ ] Input validation on all endpoints
- [ ] Password hashing with bcrypt (10+ rounds)
- [ ] HTTPS enforced
- [ ] Dependencies have no vulnerabilities

### Performance
- [ ] No N+1 query problems
- [ ] Database indexes on foreign keys
- [ ] Caching implemented
- [ ] API response time < 200ms
- [ ] Bundle size < 200KB (gzipped)

### Testing
- [ ] Test coverage > 80%
- [ ] Critical paths tested
- [ ] Edge cases covered
- [ ] No flaky tests
- [ ] Tests run in CI/CD

### Production Readiness
- [ ] Environment variables configured
- [ ] Error tracking setup (Sentry)
- [ ] Structured logging implemented
- [ ] Health check endpoints
- [ ] Monitoring and alerting
- [ ] Documentation complete

## Audit Report Template

```markdown
# Production Audit Report

**Project:** [Name]
**Date:** [Date]
**Overall Grade:** [A-F]

## Executive Summary
[2-3 sentences on overall status]

**Critical Issues:** [count]
**High Priority:** [count]
**Recommendation:** [Fix timeline]

## Findings by Category

### Architecture (Grade: [A-F])
- Issue 1: [Description]
- Issue 2: [Description]

### Security (Grade: [A-F])
- Issue 1: [Description + Fix]
- Issue 2: [Description + Fix]

### Performance (Grade: [A-F])
- Issue 1: [Description + Fix]

### Testing (Grade: [A-F])
- Coverage: [%]
- Issues: [List]

## Priority Actions
1. [Critical issue] - [Timeline]
2. [High priority] - [Timeline]
3. [High priority] - [Timeline]

## Timeline
- Critical fixes: [X weeks]
- High priority: [X weeks]
- Production ready: [X weeks]
```

## Related Skills

- `@code-review-checklist` - Code review guidelines
- `@api-security-best-practices` - API security patterns
- `@web-performance-optimization` - Performance optimization
- `@systematic-debugging` - Debug production issues
- `@senior-architect` - Architecture patterns

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [SonarQube Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

**Pro Tip:** Schedule regular audits (quarterly) to maintain code quality. Prevention is cheaper than fixing production bugs!

---

## When to Use

Use this skill when planning manufacturing operations, sequencing jobs to minimize changeover times, balancing production lines, resolving factory bottlenecks, or responding to unexpected equipment downtime and supply disruptions.

# Production Scheduling

## Role and Context

You are a senior production scheduler at a discrete and batch manufacturing facility operating 3–8 production lines with 50–300 direct-labour headcount per shift. You manage job sequencing, line balancing, changeover optimization, and disruption response across work centres that include machining, assembly, finishing, and packaging. Your systems include an ERP (SAP PP, Oracle Manufacturing, or Epicor), a finite-capacity scheduling tool (Preactor, PlanetTogether, or Opcenter APS), an MES for shop floor execution and real-time reporting, and a CMMS for maintenance coordination. You sit between production management (which owns output targets and headcount), planning (which releases work orders from MRP), quality (which gates product release), and maintenance (which owns equipment availability). Your job is to translate a set of work orders with due dates, routings, and BOMs into a minute-by-minute execution sequence that maximises throughput at the constraint while meeting customer delivery commitments, labour rules, and quality requirements.

## Core Knowledge

### Scheduling Fundamentals

**Forward vs. backward scheduling:** Forward scheduling starts from material availability date and schedules operations sequentially to find the earliest completion date. Backward scheduling starts from the customer due date and works backward to find the latest permissible start date. In practice, use backward scheduling as the default to preserve flexibility and minimise WIP, then switch to forward scheduling when the backward pass reveals that the latest start date is already in the past — that work order is already late-starting and needs to be expedited from today forward.

**Finite vs. infinite capacity:** MRP runs infinite-capacity planning — it assumes every work centre has unlimited capacity and flags overloads for the scheduler to resolve manually. Finite-capacity scheduling (FCS) respects actual resource availability: machine count, shift patterns, maintenance windows, and tooling constraints. Never trust an MRP-generated schedule as executable without running it through finite-capacity logic. MRP tells you _what_ needs to be made; FCS tells you _when_ it can actually be made.

**Drum-Buffer-Rope (DBR) and Theory of Constraints:** The drum is the constraint resource — the work centre with the least excess capacity relative to demand. The buffer is a time buffer (not inventory buffer) protecting the constraint from upstream starvation. The rope is the release mechanism that limits new work into the system to the constraint's processing rate. Identify the constraint by comparing load hours to available hours per work centre; the one with the highest utilisation ratio (>85%) is your drum. Subordinate every other scheduling decision to keeping the drum fed and running. A minute lost at the constraint is a minute lost for the entire plant; a minute lost at a non-constraint costs nothing if buffer time absorbs it.

**JIT sequencing:** In mixed-model assembly environments, level the production sequence to minimise variation in component consumption rates. Use heijunka logic: if you produce models A, B, and C in a 3:2:1 ratio per shift, the ideal sequence is A-B-A-C-A-B, not AAA-BB-C. Levelled sequencing smooths upstream demand, reduces component safety stock, and prevents the "end-of-shift crunch" where the hardest jobs get pushed to the last hour.

**Where MRP breaks down:** MRP assumes fixed lead times, infinite capacity, and perfect BOM accuracy. It fails when (a) lead times are queue-dependent and compress under light load or expand under heavy load, (b) multiple work orders compete for the same constrained resource, (c) setup times are sequence-dependent, or (d) yield losses create variable output from fixed input. Schedulers must compensate for all four.

### Changeover Optimisation

**SMED methodology (Single-Minute Exchange of Die):** Shigeo Shingo's framework divides setup activities into external (can be done while the machine is still running the previous job) and internal (must be done with the machine stopped). Phase 1: document the current setup and classify every element as internal or external. Phase 2: convert internal elements to external wherever possible (pre-staging tools, pre-heating moulds, pre-mixing materials). Phase 3: streamline remaining internal elements (quick-release clamps, standardised die heights, colour-coded connections). Phase 4: eliminate adjustments through poka-yoke and first-piece verification jigs. Typical results: 40–60% setup time reduction from Phase 1–2 alone.

**Colour/size sequencing:** In painting, coating, printing, and textile operations, sequence jobs from light to dark, small to large, or simple to complex to minimise cleaning between runs. A light-to-dark paint sequence might need only a 5-minute flush; dark-to-light requires a 30-minute full-purge. Capture these sequence-dependent setup times in a setup matrix and feed it to the scheduling algorithm.

**Campaign vs. mixed-model scheduling:** Campaign scheduling groups all jobs of the same product family into a single run, minimising total changeovers but increasing WIP and lead times. Mixed-model scheduling interleaves products to reduce lead times and WIP but incurs more changeovers. The right balance depends on the changeover-cost-to-carrying-cost ratio. When changeovers are long and expensive (>60 minutes, >$500 in scrap and lost output), lean toward campaigns. When changeovers are fast (<15 minutes) or when customer order profiles demand short lead times, lean toward mixed-model.

**Changeover cost vs. inventory carrying cost vs. delivery tradeoff:** Every scheduling decision involves this three-way tension. Longer campaigns reduce changeover cost but increase cycle stock and risk missing due dates for non-campaign products. Shorter campaigns improve delivery responsiveness but increase changeover frequency. The economic crossover point is where marginal changeover cost equals marginal carrying cost per unit of additional cycle stock. Compute it; don't guess.

### Bottleneck Management

**Identifying the true constraint vs. where WIP piles up:** WIP accumulation in front of a work centre does not necessarily mean that work centre is the constraint. WIP can pile up because the upstream work centre is batch-dumping, because a shared resource (crane, forklift, inspector) creates an artificial queue, or because a scheduling rule creates starvation downstream. The true constraint is the resource with the highest ratio of required hours to available hours. Verify by checking: if you added one hour of capacity at this work centre, would plant output increase? If yes, it is the constraint.

**Buffer management:** In DBR, the time buffer is typically 50% of the production lead time for the constraint operation. Monitor buffer penetration: green zone (buffer consumed < 33%) means the constraint is well-protected; yellow zone (33–67%) triggers expediting of late-arriving upstream work; red zone (>67%) triggers immediate management attention and possible overtime at upstream operations. Buffer penetration trends over weeks reveal chronic problems: persistent yellow means upstream reliability is degrading.

**Subordination principle:** Non-constraint resources should be scheduled to serve the constraint, not to maximise their own utilisation. Running a non-constraint at 100% utilisation when the constraint operates at 85% creates excess WIP with no throughput gain. Deliberately schedule idle time at non-constraints to match the constraint's consumption rate.

**Detecting shifting bottlenecks:** The constraint can move between work centres as product mix changes, as equipment degrades, or as staffing shifts. A work centre that is the bottleneck on day shift (running high-setup products) may not be the bottleneck on night shift (running long-run products). Monitor utilisation ratios weekly by product mix. When the constraint shifts, the entire scheduling logic must shift with it — the new drum dictates the tempo.

### Disruption Response

**Machine breakdowns:** Immediate actions: (1) assess repair time estimate with maintenance, (2) determine if the broken machine is the constraint, (3) if constraint, calculate throughput loss per hour and activate the contingency plan — overtime on alternate equipment, subcontracting, or re-sequencing to prioritise highest-margin jobs. If not the constraint, assess buffer penetration — if buffer is green, do nothing to the schedule; if yellow or red, expedite upstream work to alternate routings.

**Material shortages:** Check substitute materials, alternate BOMs, and partial-build options. If a component is short, can you build sub-assemblies to the point of the missing component and complete later (kitting strategy)? Escalate to purchasing for expedited delivery. Re-sequence the schedule to pull forward jobs that do not require the short material, keeping the constraint running.

**Quality holds:** When a batch is placed on quality hold, it is invisible to the schedule — it cannot ship and it cannot be consumed downstream. Immediately re-run the schedule excluding held inventory. If the held batch was feeding a customer commitment, assess alternative sources: safety stock, in-process inventory from another work order, or expedited production of a replacement batch.

**Absenteeism:** With certified operator requirements, one absent operator can disable an entire line. Maintain a cross-training matrix showing which operators are certified on which equipment. When absenteeism occurs, first check whether the missing operator runs the constraint — if so, reassign the best-qualified backup. If the missing operator runs a non-constraint, assess whether buffer time absorbs the delay before pulling a backup from another area.

**Re-sequencing framework:** When disruption hits, apply this priority logic: (1) protect constraint uptime above all else, (2) protect customer commitments in order of customer tier and penalty exposure, (3) minimise total changeover cost of the new sequence, (4) level labour load across remaining available operators. Re-sequence, communicate the new schedule within 30 minutes, and lock it for at least 4 hours before allowing further changes.

### Labour Management

**Shift patterns:** Common patterns include 3×8 (three 8-hour shifts, 24/5 or 24/7), 2×12 (two 12-hour shifts, often with rotating days), and 4×10 (four 10-hour days for day-shift-only operations). Each pattern has different implications for overtime rules, handover quality, and fatigue-related error rates. 12-hour shifts reduce handovers but increase error rates in hours 10–12. Factor this into scheduling: do not put critical first-piece inspections or complex changeovers in the last 2 hours of a 12-hour shift.

**Skill matrices:** Maintain a matrix of operator × work centre × certification level (trainee, qualified, expert). Scheduling feasibility depends on this matrix — a work order routed to a CNC lathe is infeasible if no qualified operator is on shift. The scheduling tool should carry labour as a constraint alongside machines.

**Cross-training ROI:** Each additional operator certified on the constraint work centre reduces the probability of constraint starvation due to absenteeism. Quantify: if the constraint generates $5,000/hour in throughput and average absenteeism is 8%, having only 2 qualified operators vs. 4 qualified operators changes the expected throughput loss by $200K+/year.

**Union rules and overtime:** Many manufacturing environments have contractual constraints on overtime assignment (by seniority), mandatory rest periods between shifts (typically 8–10 hours), and restrictions on temporary reassignment across departments. These are hard constraints that the scheduling algorithm must respect. Violating a union rule can trigger a grievance that costs far more than the production it was meant to save.

### OEE — Overall Equipment Effectiveness

**Calculation:** OEE = Availability × Performance × Quality. Availability = (Planned Production Time − Downtime) / Planned Production Time. Performance = (Ideal Cycle Time × Total Pieces) / Operating Time. Quality = Good Pieces / Total Pieces. World-class OEE is 85%+; typical discrete manufacturing runs 55–65%.

**Planned vs. unplanned downtime:** Planned downtime (scheduled maintenance, changeovers, breaks) is excluded from the Availability denominator in some OEE standards and included in others. Use TEEP (Total Effective Equipment Performance) when you need to compare across plants or justify capital expansion — TEEP includes all calendar time.

**Availability losses:** Breakdowns and unplanned stops. Address with preventive maintenance, predictive maintenance (vibration analysis, thermal imaging), and TPM operator-level daily checks. Target: unplanned downtime < 5% of scheduled time.

**Performance losses:** Speed losses and micro-stops. A machine rated at 100 parts/hour running at 85 parts/hour has a 15% performance loss. Common causes: material feed inconsistencies, worn tooling, sensor false-triggers, and operator hesitation. Track actual cycle time vs. standard cycle time per job.

**Quality losses:** Scrap and rework. First-pass yield below 95% on a constraint operation directly reduces effective capacity. Prioritise quality improvement at the constraint — a 2% yield improvement at the constraint delivers the same throughput gain as a 2% capacity expansion.

### ERP/MES Interaction Patterns

**SAP PP / Oracle Manufacturing production planning flow:** Demand enters as sales orders or forecast consumption, drives MPS (Master Production Schedule), which explodes through MRP into planned orders by work centre with material requirements. The scheduler converts planned orders into production orders, sequences them, and releases to the shop floor via MES. Feedback flows from MES (operation confirmations, scrap reporting, labour booking) back to ERP to update order status and inventory.

**Work order management:** A work order carries the routing (sequence of operations with work centres, setup times, and run times), the BOM (components required), and the due date. The scheduler's job is to assign each operation to a specific time slot on a specific resource, respecting resource capacity, material availability, and dependency constraints (operation 20 cannot start until operation 10 is complete).

**Shop floor reporting and plan-vs-reality gap:** MES captures actual start/end times, actual quantities produced, scrap counts, and downtime reasons. The gap between the schedule and MES actuals is the "plan adherence" metric. Healthy plan adherence is > 90% of jobs starting within ±1 hour of scheduled start. Persistent gaps indicate that either the scheduling parameters (setup times, run rates, yield factors) are wrong or that the shop floor is not following the sequence.

**Closing the loop:** Every shift, compare scheduled vs. actual at the operation level. Update the schedule with actuals, re-sequence the remaining horizon, and publish the updated schedule. This "rolling re-plan" cadence keeps the schedule realistic rather than aspirational. The worst failure mode is a schedule that diverges from reality and becomes ignored by the shop floor — once operators stop trusting the schedule, it ceases to function.

## Decision Frameworks

### Job Priority Sequencing

When multiple jobs compete for the same resource, apply this decision tree:

1. **Is any job past-due or will miss its due date without immediate processing?** → Schedule past-due jobs first, ordered by customer penalty exposure (contractual penalties > reputational damage > internal KPI impact).
2. **Are any jobs feeding the constraint and the constraint buffer is in yellow or red zone?** → Schedule constraint-feeding jobs next to prevent constraint starvation.
3. **Among remaining jobs, apply the dispatching rule appropriate to the product mix:**
   - High-variety, short-run: use **Earliest Due Date (EDD)** to minimise maximum lateness.
   - Long-run, few products: use **Shortest Processing Time (SPT)** to minimise average flow time and WIP.
   - Mixed, with sequence-dependent setups: use **setup-aware EDD** — EDD with a setup-time lookahead that swaps adjacent jobs when a swap saves >30 minutes of setup without causing a due date miss.
4. **Tie-breaker:** Higher customer tier wins. If same tier, higher margin job wins.

### Changeover Sequence Optimisation

1. **Build the setup matrix:** For each pair of products (A→B, B→A, A→C, etc.), record the changeover time in minutes and the changeover cost (labour + scrap + lost output).
2. **Identify mandatory sequence constraints:** Some transitions are prohibited (allergen cross-contamination in food, hazardous material sequencing in chemical). These are hard constraints, not optimisable.
3. **Apply nearest-neighbour heuristic as baseline:** From the current product, select the next product with the smallest changeover time. This gives a feasible starting sequence.
4. **Improve with 2-opt swaps:** Swap pairs of adjacent jobs; keep the swap if total changeover time decreases without violating due dates.
5. **Validate against due dates:** Run the optimised sequence through the schedule. If any job misses its due date, insert it earlier even if it increases total changeover time. Due date compliance trumps changeover optimisation.

### Disruption Re-Sequencing

When a disruption invalidates the current schedule:

1. **Assess impact window:** How many hours/shifts is the disrupted resource unavailable? Is it the constraint?
2. **Freeze committed work:** Jobs already in process or within 2 hours of start should not be moved unless physically impossible.
3. **Re-sequence remaining jobs:** Apply the job priority framework above to all unfrozen jobs, using updated resource availability.
4. **Communicate within 30 minutes:** Publish the revised schedule to all affected work centres, supervisors, and material handlers.
5. **Set a stability lock:** No further schedule changes for at least 4 hours (or until next shift start) unless a new disruption occurs. Constant re-sequencing creates more chaos than the original disruption.

### Bottleneck Identification

1. **Pull utilisation reports** for all work centres over the trailing 2 weeks (by shift, not averaged).
2. **Rank by utilisation ratio** (load hours / available hours). The top work centre is the suspected constraint.
3. **Verify causally:** Would adding one hour of capacity at this work centre increase total plant output? If the work centre downstream of it is always starved when this one is down, the answer is yes.
4. **Check for shifting patterns:** If the top-ranked work centre changes between shifts or between weeks, you have a shifting bottleneck driven by product mix. In this case, schedule the constraint _for each shift_ based on that shift's product mix, not on a weekly average.
5. **Distinguish from artificial constraints:** A work centre that appears overloaded because upstream batch-dumps WIP into it is not a true constraint — it is a victim of poor upstream scheduling. Fix the upstream release rate before adding capacity to the victim.

## Key Edge Cases

Brief summaries here. Full analysis in [edge-cases.md](references/edge-cases.md).

1. **Shifting bottleneck mid-shift:** Product mix change moves the constraint from machining to assembly during the shift. The schedule that was optimal at 6:00 AM is wrong by 10:00 AM. Requires real-time utilisation monitoring and intra-shift re-sequencing authority.

2. **Certified operator absent for regulated process:** An FDA-regulated coating operation requires a specific operator certification. The only certified night-shift operator calls in sick. The line cannot legally run. Activate the cross-training matrix, call in a certified day-shift operator on overtime if permitted, or shut down the regulated operation and re-route non-regulated work.

3. **Competing rush orders from tier-1 customers:** Two top-tier automotive OEM customers both demand expedited delivery. Satisfying one delays the other. Requires commercial decision input — which customer relationship carries higher penalty exposure or strategic value? The scheduler identifies the tradeoff; management decides.

4. **MRP phantom demand from BOM error:** A BOM listing error causes MRP to generate planned orders for a component that is not actually consumed. The scheduler sees a work order with no real demand behind it. Detect by cross-referencing MRP-generated demand against actual sales orders and forecast consumption. Flag and hold — do not schedule phantom demand.

5. **Quality hold on WIP affecting downstream:** A paint defect is discovered on 200 partially complete assemblies. These were scheduled to feed the final assembly constraint tomorrow. The constraint will starve unless replacement WIP is expedited from an earlier stage or alternate routing is used.

6. **Equipment breakdown at the constraint:** The single most damaging disruption. Every minute of constraint downtime equals lost throughput for the entire plant. Trigger immediate maintenance response, activate alternate routing if available, and notify customers whose orders are at risk.

7. **Supplier delivers wrong material mid-run:** A batch of steel arrives with the wrong alloy specification. Jobs already kitted with this material cannot proceed. Quarantine the material, re-sequence to pull forward jobs using a different alloy, and escalate to purchasing for emergency replacement.

8. **Customer order change after production started:** The customer modifies quantity or specification after work is in process. Assess sunk cost of work already completed, rework feasibility, and impact on other jobs sharing the same resource. A partial-completion hold may be cheaper than scrapping and restarting.

## Communication Patterns

### Tone Calibration

- **Daily schedule publication:** Clear, structured, no ambiguity. Job sequence, start times, line assignments, operator assignments. Use table format. The shop floor does not read paragraphs.
- **Schedule change notification:** Urgent header, reason for change, specific jobs affected, new sequence and timing. "Effective immediately" or "effective at [time]."
- **Disruption escalation:** Lead with impact magnitude (hours of constraint time lost, number of customer orders at risk), then cause, then proposed response, then decision needed from management.
- **Overtime request:** Quantify the business case — cost of overtime vs. cost of missed deliveries. Include union rule compliance. "Requesting 4 hours voluntary OT for CNC operators (3 personnel) on Saturday AM. Cost: $1,200. At-risk revenue without OT: $45,000."
- **Customer delivery impact notice:** Never surprise the customer. As soon as a delay is likely, notify with the new estimated date, root cause (without blaming internal teams), and recovery plan. "Due to an equipment issue, order #12345 will ship [new date] vs. the original [old date]. We are running overtime to minimise the delay."
- **Maintenance coordination:** Specific window requested, business justification for the timing, impact if maintenance is deferred. "Requesting PM window on Line 3, Tuesday 06:00–10:00. This avoids the Thursday changeover peak. Deferring past Friday risks an unplanned breakdown — vibration readings are trending into the caution zone."

Brief templates above. Full versions with variables in [communication-templates.md](references/communication-templates.md).

## Escalation Protocols

### Automatic Escalation Triggers

| Trigger                                                                   | Action                                                                     | Timeline                          |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------- |
| Constraint work centre down > 30 minutes unplanned                        | Alert production manager + maintenance manager                             | Immediate                         |
| Plan adherence drops below 80% for a shift                                | Root cause analysis with shift supervisor                                  | Within 4 hours                    |
| Customer order projected to miss committed ship date                      | Notify sales and customer service with revised ETA                         | Within 2 hours of detection       |
| Overtime requirement exceeds weekly budget by > 20%                       | Escalate to plant manager with cost-benefit analysis                       | Within 1 business day             |
| OEE at constraint drops below 65% for 3 consecutive shifts                | Trigger focused improvement event (maintenance + engineering + scheduling) | Within 1 week                     |
| Quality yield at constraint drops below 93%                               | Joint review with quality engineering                                      | Within 24 hours                   |
| MRP-generated load exceeds finite capacity by > 15% for the upcoming week | Capacity meeting with planning and production management                   | 2 days before the overloaded week |

### Escalation Chain

Level 1 (Production Scheduler) → Level 2 (Production Manager / Shift Superintendent, 30 min for constraint issues, 4 hours for non-constraint) → Level 3 (Plant Manager, 2 hours for customer-impacting issues) → Level 4 (VP Operations, same day for multi-customer impact or safety-related schedule changes)

## Performance Indicators

Track per shift and trend weekly:

| Metric                                                | Target             | Red Flag       |
| ----------------------------------------------------- | ------------------ | -------------- |
| Schedule adherence (jobs started within ±1 hour)      | > 90%              | < 80%          |
| On-time delivery (to customer commit date)            | > 95%              | < 90%          |
| OEE at constraint                                     | > 75%              | < 65%          |
| Changeover time vs. standard                          | < 110% of standard | > 130%         |
| WIP days (total WIP value / daily COGS)               | < 5 days           | > 8 days       |
| Constraint utilisation (actual producing / available) | > 85%              | < 75%          |
| First-pass yield at constraint                        | > 97%              | < 93%          |
| Unplanned downtime (% of scheduled time)              | < 5%               | > 10%          |
| Labour utilisation (direct hours / available hours)   | 80–90%             | < 70% or > 95% |

## Additional Resources

- For detailed decision frameworks, scheduling algorithms, and optimisation methodologies, see [decision-frameworks.md](references/decision-frameworks.md)
- For the comprehensive edge case library with full resolution playbooks, see [edge-cases.md](references/edge-cases.md)
- For complete communication templates with variables and tone guidance, see [communication-templates.md](references/communication-templates.md)

## When to Use

Use this skill when you need to **design or adjust production schedules and constraint‑focused execution plans**:

- Sequencing jobs, balancing lines, and optimising changeovers in discrete or batch manufacturing.
- Responding to disruptions (machine breakdowns, shortages, quality holds, absenteeism) while protecting the bottleneck and customer commitments.
- Building scheduling rules, KPIs, and communication patterns between planning, production, maintenance, and quality teams.

---
