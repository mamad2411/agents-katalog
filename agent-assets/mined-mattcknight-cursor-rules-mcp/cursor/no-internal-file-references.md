# No Internal File References in Architecture Documents

**Priority:** 🔴 CRITICAL  
**Applies To:** Solution Architecture, Technical Design, TRAC documents  
**Status:** MANDATORY

---

## Critical Rule: Never Reference Internal Files

**NEVER reference `.md` files or internal repository paths in architecture documents unless explicitly instructed by the user.**

---

## ❌ INCORRECT Examples:

```markdown
Complex routing logic documented in docs/analysis/routing_baseline.md

See VERIFICATION.md for analysis details

Reference: analysis-documents/DECISION.md

Based on findings in docs/internal/ANALYSIS_PHASE_1.md
```

---

## ✅ CORRECT Examples:

```markdown
Complex routing logic is based on payment type + method combination

Payment routing is determined by PaymentProcessorRouter based on multiple factors

See baseline analysis documentation for full routing matrix

Based on comprehensive analysis of routing requirements
```

---

## Rationale

### Why This Rule Exists:

1. **Document Portability**: Architecture documents should be self-contained and not rely on repository-specific file paths
2. **External Distribution**: Documents may be shared outside the repository (Confluence, email, presentations, stakeholder reviews)
3. **Link Breakage**: File paths may change over time, breaking references
4. **Professional Presentation**: External file references make documents look incomplete or internal-only
5. **TRAC Compliance**: TRAC documents should not contain repository file paths
6. **Accessibility**: External stakeholders may not have repository access

---

## Implementation

**When writing Solution Architecture, Technical Design, or TRAC documents:**

### ✅ DO:
- Include critical information inline if it's essential
- Use generic references like "baseline analysis documentation" or "analysis documents"
- Reference external systems by name (not file path)
- Describe findings and conclusions directly in the document
- Use appendices for detailed information if needed

### ❌ DON'T:
- Include `.md` file paths
- Reference internal repository structure
- Link to analysis documents by file path
- Assume readers have access to internal files
- Use relative or absolute paths to internal documents

---

## Exception

**Only reference internal files if:**
- User explicitly instructs you to do so
- Document is clearly marked as "Internal Only"
- Reference is to a standard external resource (e.g., public GitHub repo)

---

## Examples by Document Type

### Solution Architecture Document

❌ **WRONG:**
```markdown
## Architecture Analysis

See `docs/analysis/BASELINE_ANALYSIS.md` for detailed component analysis.

Routing logic is documented in `docs/technical/ROUTING_DESIGN.md`.
```

✅ **CORRECT:**
```markdown
## Architecture Analysis

Detailed component analysis revealed three key integration points:
1. API Gateway handles authentication
2. Router distributes based on business rules
3. Processor executes transactions

Routing logic determines flow based on payment type and method combination.
```

### Technical Design Document

❌ **WRONG:**
```markdown
## Implementation Details

Refer to `PHASE_1_VERIFICATION.md` for validation requirements.

See `ARCHITECTURE_UPDATES_REQUIRED.md` for system changes.
```

✅ **CORRECT:**
```markdown
## Implementation Details

Validation requirements include:
- Amount validation (>= 0)
- Payment type validation (Vendor only)
- Configuration check (feature flag enabled)

System changes required:
- Update validation layer
- Modify processor bypass logic
- Enhance reporting filters
```

### TRAC Document

❌ **WRONG:**
```markdown
## Data Flow

Data flow diagram available in `docs/diagrams/DATA_FLOW.md`

Privacy assessment documented in `docs/security/PRIVACY_ANALYSIS.md`
```

✅ **CORRECT:**
```markdown
## Data Flow

[Include actual data flow diagram inline]

Data flows through the following stages:
1. Input validation
2. Business rule processing
3. External API calls
4. Response handling

## Privacy Assessment

PII Handling:
- User email: Encrypted at rest
- Payment details: Tokenized before storage
- Audit logs: Contain no PII
```

---

## Summary

**Golden Rule:** Architecture documents should be self-contained and readable without access to the repository.

**Best Practice:** If information is critical enough to reference, include it inline in the document.

**Remember:** Your audience includes stakeholders who may not have repository access.

---

**Rule Status:** ACTIVE  
**Scope:** All Solution Architecture, Technical Design, and TRAC documents  
**Purpose:** Ensure documents are portable and accessible to all stakeholders
