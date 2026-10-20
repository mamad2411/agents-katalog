# NestJS Sample - Copilot Instructions

## Overview

This document provides GitHub Copilot with context for this NestJS-based Node.js application, specifically for security patch analysis aligned with BC Government OCIO requirements.

## Required Security Context Files

For vulnerability analysis, read these files first:

- `docs/security/app-context.md`
- `docs/security/architecture.md`
- `docs/security/threat-model.md`

Do not assume the service is internet-facing unless `docs/security/app-context.md` explicitly says so.

## Code Context

### Project Type
- **Framework**: NestJS 11.x
- **Language**: TypeScript (ES2022 target)
- **Runtime**: Node.js 24
- **Architecture**: Microservice/API backend
- **Deployment**: OCI containers (Docker)

### Code Patterns

#### NestJS Module Structure
```typescript
// Standard NestJS module pattern
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';

@Module({
  imports: [ConfigModule.forRoot()],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```

#### Dependency Injection
```typescript
// Copilot: Use constructor-based DI for NestJS
@Injectable()
export class AppService {
  constructor(private configService: ConfigService) {}
}
```

#### Environment Configuration
```typescript
// Use @nestjs/config for environment variables
@Injectable()
export class AppService {
  private apiUrl = this.configService.get<string>('API_URL');
}
```

## Security-Focused Instructions

### When Analyzing Dependencies

**DO:**
- ✅ Check npm audit output for all dependencies
- ✅ Classify vulnerabilities by CVSS score
- ✅ Reference OCIO timelines (72h/14d/30d/1y)
- ✅ Use repository security context files before scoring exposure
- ✅ Separate external exposure from internal/lateral exposure
- ✅ Use the 3-factor scoring model and show calculation
- ✅ Test patches with full test suite before recommending
- ✅ Document CVE IDs in commit messages
- ✅ Flag production dependencies as higher priority

**DON'T:**
- ❌ Recommend patches without running tests
- ❌ Ignore dev dependencies (still security-relevant)
- ❌ Miss CRITICAL or HIGH severity vulnerabilities
- ❌ Skip breaking change analysis
- ❌ Forget to update package-lock.json
- ❌ Assume internet exposure without evidence

### When Suggesting Code Changes

**For Security Updates:**
```typescript
// ❌ Don't: Create new source files to fix vulnerabilities
// This creates technical debt and deployment confusion

// ✅ DO: Update dependencies and test existing code
// Patches are applied at package.json level, not code level
```

**For Testing:**
```typescript
// Copilot: Use Jest for unit tests, supertest for E2E
import { Test, TestingModule } from '@nestjs/testing';
import * as request from 'supertest';

describe('AppController', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/ (GET)', () => {
    return request(app.getHttpServer())
      .get('/')
      .expect(200);
  });
});
```

## Patch Analysis Workflow

### Step 0: Read Repository Context
```text
Read docs/security/app-context.md, docs/security/architecture.md, docs/security/threat-model.md.
Extract: deployment model, real exposure, data sensitivity, and business criticality.
```

### Step 1: Identify Vulnerabilities
```bash
npm audit
# Output includes:
# - Package name and vulnerable range
# - CVE ID(s)
# - CVSS score and description
# - Remediation options
```

### Step 1.5: Classify The CVE Before Scoring
```text
Classify the finding into one of these buckets before recommending a fix:
1. Direct runtime dependency
2. Transitive runtime dependency
3. Dev-tooling or non-runtime dependency
4. Infrastructure or environment component not proven from this repository

Rules:
- Bucket 1: prove the package is declared directly in package.json and assess whether the vulnerable feature is used at runtime.
- Bucket 2: prove the dependency chain from package-lock.json or npm ls and distinguish direct dependency upgrades from transitive fixes or overrides.
- Bucket 3: do not describe the deployed service runtime as directly vulnerable unless the package ships there; assess CI/developer impact separately.
- Bucket 4: state that repository evidence is insufficient for a package-level patch plan and identify what platform or ownership evidence is missing.
```

### Step 2: Score Risk Using BC Gov Model
```text
Exploitability: 1-5
Exposure: 1-5
Criticality: 1-5

Risk = (Exploitability * 0.4) + (Exposure * 0.3) + (Criticality * 0.3)
```

### Step 3: Map To OCIO Classification
```text
CRITICAL: active exploitation or high-impact RCE/high exposure -> 72 hours
HIGH: serious vulnerability with restricted exposure/mitigations -> 14 days
MEDIUM: authenticated or limited impact -> 30 to 90 days
LOW: minimal impact or strong controls
```

### Step 4: Test the Patch
```bash
# Update package.json manually or use npm update
npm install

# Run full test suite
npm test                 # Unit tests
npm run test:cov         # Coverage
npm run test:e2e         # API tests
npm run lint             # Code quality
npm run build            # TypeScript compilation
```

### Step 5: Document and Commit
```bash
git add package.json package-lock.json
git commit -m "fix: patch CVE-2024-XXXXX in axios

- CVSS Score: 9.8 (CRITICAL)
- OCIO Timeline: 72 hours
- Updated: axios from 1.17.0 to 1.7.1
- Tests: All passing
- Breaking Changes: None"
```

## Required Analysis Output Structure

Always return this section order:

1. Application Overview
2. Vulnerability Summary
3. Scoring (Exploitability / Exposure / Criticality)
4. Risk Calculation
5. OCIO Classification (with patch timeline)
6. Key Interpretation
7. Required Actions
8. Justification Statement

## Common Scenarios

### Scenario: CRITICAL RCE Vulnerability
```
Detected: axios has a remote code execution vulnerability
CVSS: 9.8 | Type: CRITICAL | Timeline: 72 HOURS

Recommendation:
1. Update axios to patched version immediately
2. Run all tests
3. Build and deploy
4. Monitor production for issues
5. Post-incident review within 24 hours
```

### Scenario: HIGH Severity Authentication Bypass
```
Detected: @nestjs/common has authentication bypass
CVSS: 7.2 | Type: HIGH | Timeline: 14 DAYS

Recommendation:
1. Plan patch within 1-2 days
2. Coordinate with QA for expedited testing
3. Stage in non-production first
4. Deploy with monitoring
5. Document patch timeline compliance
```

### Scenario: MEDIUM Severity in Dev Dependency
```
Detected: @types/jest has an issue
CVSS: 5.1 | Type: MEDIUM | Timeline: 30 DAYS

Recommendation:
1. Schedule for next update cycle
2. Include with other MEDIUM patches
3. Standard testing process
4. Deploy with regular release
```

## Key Files to Reference

| File | Purpose |
|------|---------|
| `package.json` | Dependency declarations and versions |
| `package-lock.json` | Locked dependency tree (auto-generated) |
| `.github/workflows/test.yaml` | Test automation pipeline |
| `jest.config.js` | Test configuration |
| `src/main.ts` | Application bootstrap |
| `src/app.module.ts` | NestJS module definitions |
| `tsconfig.json` | TypeScript compiler options |

## For GitHub Copilot Chat

When asking Copilot about this codebase:

### Good Prompts
```
"What vulnerabilities does npm audit show for this project?"
"How should I patch CVE-2024-XXXXX in axios following OCIO guidelines?"
"What are the breaking changes in upgrading @nestjs/common from 11.1.26 to 11.2.0?"
"How do I run the complete test suite to validate a patch?"
```

### Poor Prompts
```
"Fix all vulnerabilities" (too vague, needs OCIO context)
"Update all dependencies to latest" (ignores breaking changes and testing)
"Create a patch script" (patches come from npm, not scripts)
```

## Security Principles

1. **OCIO Compliance is Mandatory**
   - Patches must meet OCIO timelines
   - Missed deadlines require formal risk acceptance
   - Compensating controls do NOT exempt from patching

2. **Test Everything**
   - No patch without passing tests
   - All test suites must pass (unit, E2E, lint, build)
   - Coverage should not decrease

3. **Document Everything**
   - CVE IDs in commit messages
   - OCIO timeline compliance in documentation
   - Breaking changes documented with migration steps

4. **No Manual Lock File Edits**
   - Always use `npm install` to update package-lock.json
   - Never manually edit package-lock.json

5. **Production-First Thinking**
  - Determine exposure from `docs/security/app-context.md`
  - Treat vulnerabilities as higher severity only when exposure evidence supports it
   - Security patches take priority over feature work

## Copilot Collaboration Tips

When working with Copilot on security patches:

1. **Provide Context**: "Use docs/security/app-context.md and architecture.md to determine exposure before scoring CVE-XXXX."

2. **Ask for Analysis**: "Analyze this npm audit output and prioritize by OCIO timeline (72h/14d/30d/1y)."

3. **Request Validation**: "After updating axios, run this test sequence and report results: npm test, npm run test:e2e, npm audit."

4. **Document Together**: "Draft a commit message that includes CVE ID, CVSS score, OCIO timeline, and test results for this patch."

5. **Review Compatibility**: "Check if this new version of @nestjs/common has breaking changes with our current TypeScript and Node.js versions."

## Performance Notes

- **Build Time**: TypeScript compilation takes ~5-10 seconds
- **Test Time**: Full suite (unit + E2E) typically runs in 30-60 seconds
- **npm install**: Expect 2-3 minutes for full dependency resolution
- **Docker Build**: OCI image build takes ~3-5 minutes

Use these timelines when estimating patch cycle duration.
