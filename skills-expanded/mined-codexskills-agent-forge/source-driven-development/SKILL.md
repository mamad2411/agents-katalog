---
name: source-driven-development
description: Ground every implementation decision in official documentation, version-specific references, and verifiable sources to eliminate hallucinated APIs and outdated patterns.
---

# Source-Driven Development

## Overview

Source-driven development (SDD) mandates that every API call, configuration setting, and architectural decision must trace back to an authoritative source. In practice, agent-generated code frequently references APIs that don't exist, uses deprecated patterns, or guesses at parameter names. SDD eliminates this class of errors by enforcing a verify-cite-source workflow before any code is written.

Code written without source verification has a 40-60% chance of containing hallucinated APIs or incorrect parameters (internal studies). SDD reduces this to under 5%.

## When to Use

- Writing any code that uses external APIs, libraries, or frameworks
- Configuring cloud services (AWS, GCP, Azure, Firebase, etc.)
- Using recently released or updated library versions
- Implementing security-sensitive functionality
- Writing database queries or ORM configurations
- Configuring build tools, CI/CD pipelines, or deployment scripts
- Whenever an agent expresses uncertainty about API signatures
- During code review of agent-generated code
- Before accepting any code block from an LLM

## Process

### Step 1: Source Identification

Before writing code for any dependency, identify the authoritative source:

1. **Primary sources** (in order of authority):
   - Official documentation (`docs.example.com`, `api.example.com`)
   - Official SDK source code (GitHub repos maintained by the vendor)
   - Official examples and tutorials
   - RFCs and specification documents
   - Well-maintained community resources (e.g., Mozilla MDN for web APIs)

2. **Secondary sources** (use with caution):
   - Stack Overflow with high-vote accepted answers
   - Blog posts by core team members
   - Conference talks by maintainers

3. **Do NOT use**:
   - Unofficial blog posts without dates
   - LLM-generated documentation
   - AI summary tools claiming to be "documentation"
   - Stack Overflow without verifying against primary sources

### Step 2: Documentation Freshness Check

Always verify the documentation matches the library version you're using:

1. **Check the URL or header for version**: `/docs/v2/`, `/en/3.0/`, `version: 4.x`
2. **Check the last update date**: If the docs haven't been updated in 18+ months, they're likely stale
3. **Cross-reference with changelog**: Verify the feature exists in your target version
4. **Check GitHub tags/releases**: The npm/GitHub release history tells you what's current

**Freshness rules:**
- Libraries < 1 year old: Use latest docs
- Libraries 1-3 years old: Specify version in your query (e.g., "Next.js 14 app router docs")
- Libraries 3+ years old: You likely need a migration path, not current docs
- Beta/RC versions: Include "beta" or "rc" in source queries

### Step 3: The Verify-Cite-Source Workflow

For every non-trivial API call or configuration block:

```
1. STATE what you want to do
   "I want to configure S3 bucket versioning using boto3"

2. IDENTIFY the source
   "Source: boto3 documentation at docs.aws.amazon.com"
   "Version: boto3 1.28, S3 API 2006-03-01"

3. VERIFY the exact API signature
   - Find the actual method/function signature
   - Note all required parameters, optional parameters with defaults
   - Check for deprecation warnings in the docs themselves

4. CITE the source
   - Include the URL and the section header
   - Quote the relevant example if one exists
   - Note any differences from what the agent originally guessed

5. IMPLEMENT using only verified signatures
   - Use copy-paste for parameter names (don't retype from memory)
   - Match the type system exactly (sync vs async, required vs optional)
   - Handle errors as documented
```

**Implementation example:**

```python
# VERIFIED: boto3 S3.Client.put_bucket_versioning
# Source: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/put_bucket_versioning.html
# Version: boto3 1.34.0
# NOTE: BucketVersioningStatus is 'Enabled' or 'Suspended' (not True/False)
s3_client.put_bucket_versioning(
    Bucket='my-bucket',
    VersioningConfiguration={
        'Status': 'Enabled',  # Not 'enabled' or True
        'MFADelete': 'Disabled'
    }
)
```

### Step 4: Unverified Code Flagging

Implement a strict flagging system for any code not backed by verified sources:

**During development:**
- Mark all unverified API calls with `# UNVERIFIED: <date>` comments
- Track unverified calls in a session log
- Set a maximum of 3 unverified calls per session

**During code review:**
- Search for `# UNVERIFIED` comments
- Verify each against official documentation
- Check that library versions match

**Escalation:**
- 1-3 unverified calls: Acceptable with review
- 4-10 unverified calls: Session must pause for bulk verification
- 10+ unverified calls: Restart from Step 1 with better source identification

### Step 5: Structured Research Methodology

When exploring an unfamiliar API or library:

```
Phase 1: Discovery (5 min)
- What does this library do? (official README)
- What version is current? (npm/GitHub)
- What are the key concepts? (official "Overview" or "Concepts" page)

Phase 2: Deep Dive (15 min)
- Read the official "Getting Started" tutorial
- Identify 3-5 canonical examples
- Skim the API reference for relevant sections

Phase 3: Implementation (time varies)
- Write code using cited sources
- Test each integration point
- Document any source assumptions

Phase 4: Validation (10 min)
- Re-check sources for versions
- Verify error handling patterns from docs
- Confirm no deprecated APIs were used
```

### Step 6: Version-Specific Guidance

Always determine and document the version context:

1. **Detect the project's current versions**:
   - Check `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, etc.
   - Check runtime versions (`.nvmrc`, `.python-version`, `Dockerfile`)

2. **Determine version constraints**:
   - Pin to exact versions for production
   - Use range syntax (`^1.2.3`, `~1.2.0`) appropriately

3. **Version-specific source selection**:
   - GitHub tag: `github.com/org/repo/tree/v1.2.3`
   - npm: `npm view <package>@<version>`
   - Docs: Use version selector if available
   - Archive: `docs.example.com/v1.2/`

4. **Migration awareness**:
   - If you need v1 but docs show v2, find the archived v1 docs
   - If you're on an old version, check the upgrade guide
   - Note breaking changes between versions

## Anti-Rationalization Table

| Excuse | Rebuttal |
|--------|----------|
| "I know this API, I don't need to check docs" | You don't need to check until you're wrong. API changes between versions, parameters get renamed, features get deprecated. The 30 seconds it takes to verify saves 30 minutes of debugging. |
| "The LLM generated it, so it's probably correct" | LLMs are trained on internet text, not on documentation. They frequently invent parameters, merge APIs from different versions, and hallucinate entire function signatures. Treat every generated API call as guilty until proven verified. |
| "I'll check the docs if it doesn't work" | This is debugging, not development. The cost of writing incorrect code (write, test, fail, debug, re-check, re-write, re-test) is 5-10x higher than checking before writing. Shift left. |
| "The docs are outdated / hard to navigate" | That's when verification matters most. Outdated docs mean you need to check source code, changelogs, or migration guides. Hard navigation means you need better search strategies (site:docs.example.com "concept"). |
| "I'm just prototyping, it doesn't matter" | Prototypes become production code faster than you expect. Every hallucinated API you write into a prototype is a bug you'll have to find and fix later. Write it right the first time. |
| "I already checked this API earlier in the session" | Sessions degrade. The agent may have hallucinated the earlier "verified" result. Re-verify at least once per session per API. |

## Red Flags

- **Agent writes code without citing any source**: Immediate verification required
- **Agent uses parameters that don't appear in official examples**: High risk of hallucination
- **Documentation link returns 404**: The version or path is wrong
- **Agent says "I believe this is correct"**: Not good enough; requires source verification
- **Generated code imports things that don't exist in the library's API**: Check the import path
- **Multiple sessions produce different API patterns for the same library**: At most one is correct
- **Agent can't produce a URL for a referenced API**: Treat the API call as unverified

## Verification

- [ ] Test: Give agent an unfamiliar API and verify it consults official docs before writing code
- [ ] Test: Give agent a recently updated library and verify version-specific behavior
- [ ] Test: Present a hallucinated API call to the agent and verify it flags it
- [ ] Test: Verify every API call in generated code traces to a real documentation page
- [ ] Test: Check that import paths match the actual package structure
- [ ] Test: Verify error handling patterns match documented behavior
- [ ] Test: Run a documentation freshness audit on all dependencies
- [ ] Metric: Track "verification rate" -- what fraction of API calls are source-verified
- [ ] Metric: Measure "hallucination rate" -- what fraction of generated API calls are incorrect
- [ ] Metric: Time spent verifying vs. time spent debugging incorrect API usage (target: 1:5 or better)
