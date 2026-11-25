---
memory_layer: durable_knowledge
para_section: pages/skills/verification-before-completion
gigabrain_tags: verification, quality-assurance, testing, validation, evidence-based
openstinger_context: completion-verification, quality-gates, evidence-based-claims
last_updated: 2026-03-30
related_docs:
  - docs/testing/0000_TESTING_FRAMEWORK.md
  - docs/error-tracking/0000_ERROR_FIXES_SUMMARY.md
related_skills:
  - testing-verification
  - systematic-debugging
  - test-driven-development
frequency_percent: 95.0
success_rate_percent: 96.0
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## When to Use This Skill

**Trigger Conditions:**
- Before claiming any work is complete or successful
- Before committing code changes to version control
- Before creating pull requests or submitting for review
- Before expressing satisfaction with implementation
- Before moving to the next task or phase
- When delegating work to agents and verifying completion
- When about to make any positive statement about work status
- Before shipping features or marking tasks as done
- When tired or under time pressure (prevents false claims)
- After any implementation work requiring validation

**Mandatory Application:**
- Always apply before any completion claims
- No exceptions for "obvious" or "simple" changes
- Required even when delegating to agents
- Must be applied before any communication of success

## Step-by-Step Procedure

### Step 1: Identify Verification Command
**Determine what command proves the claim:**

```javascript
// Identify the appropriate verification method
const verificationMethods = {
  tests: {
    claim: 'tests pass',
    command: 'npm test',
    success: 'All tests pass with 0 failures'
  },
  build: {
    claim: 'build succeeds',
    command: 'npm run build',
    success: 'Exit code 0, no compilation errors'
  },
  lint: {
    claim: 'code is clean',
    command: 'npm run lint',
    success: '0 linting errors or warnings'
  },
  requirements: {
    claim: 'requirements met',
    command: 'manual checklist verification',
    success: 'All requirements checked and confirmed'
  }
};
```

**Verification Command Identification:**
- Tests: Full test suite execution
- Build: Complete build process
- Linting: Code quality checks
- Requirements: Manual checklist verification
- Agent work: VCS diff and functionality verification

### Step 2: Execute Fresh Verification
**Run the complete verification command from scratch:**

```bash
# Execute verification with full output capture
VERIFICATION_OUTPUT=$(mktemp)
VERIFICATION_EXIT_CODE=0

# Run the verification command
case $CLAIM_TYPE in
  "tests")
    npm test 2>&1 | tee "$VERIFICATION_OUTPUT"
    VERIFICATION_EXIT_CODE=${PIPESTATUS[0]}
    ;;
  "build")
    npm run build 2>&1 | tee "$VERIFICATION_OUTPUT"
    VERIFICATION_EXIT_CODE=${PIPESTATUS[0]}
    ;;
  "lint")
    npm run lint 2>&1 | tee "$VERIFICATION_OUTPUT"
    VERIFICATION_EXIT_CODE=${PIPESTATUS[0]}
    ;;
esac
```

**Fresh Execution Requirements:**
- Complete command execution (not partial)
- Full output capture for analysis
- Exit code verification
- No reliance on previous runs

### Step 3: Analyze Complete Output
**Read and analyze the full verification output:**

```javascript
// Analyze verification results
function analyzeVerificationOutput(output, exitCode) {
  const results = {
    success: exitCode === 0,
    failureCount: countFailures(output),
    errorMessages: extractErrors(output),
    warnings: extractWarnings(output),
    summary: generateSummary(output)
  };

  return results;
}

// Count different types of failures
function countFailures(output) {
  return {
    testFailures: (output.match(/FAILED|✗/g) || []).length,
    buildErrors: (output.match(/ERROR|error/g) || []).length,
    lintErrors: (output.match(/error|Error/g) || []).length,
    compilationErrors: (output.match(/Compilation failed/g) || []).length
  };
}
```

**Output Analysis:**
- Check exit code (0 = success)
- Count failures and errors
- Extract error messages
- Identify warning conditions
- Generate summary assessment

### Step 4: Verify Claim Against Evidence
**Compare claim against actual verification results:**

```javascript
// Verify claim matches evidence
function verifyClaim(claim, verificationResults) {
  const claimVerification = {
    'tests pass': verificationResults.success && verificationResults.failureCount.testFailures === 0,
    'build succeeds': verificationResults.success && verificationResults.failureCount.buildErrors === 0,
    'code is clean': verificationResults.success && verificationResults.failureCount.lintErrors === 0,
    'requirements met': verificationResults.manualChecklistComplete,
    'bug fixed': verificationResults.regressionTestPasses,
    'feature complete': verificationResults.allAcceptanceCriteriaMet
  };

  return {
    claimValid: claimVerification[claim] || false,
    evidence: verificationResults,
    discrepancies: identifyDiscrepancies(claim, verificationResults)
  };
}
```

**Claim Verification:**
- Tests pass: 0 test failures, exit code 0
- Build succeeds: No compilation errors, exit code 0
- Code clean: 0 linting errors, exit code 0
- Requirements met: All checklist items verified
- Bug fixed: Regression test passes

### Step 5: Report Actual Status with Evidence
**State the verified status with supporting evidence:**

```javascript
// Report verified status
function reportVerifiedStatus(claim, verificationResults) {
  if (verificationResults.success) {
    return `[Verification: ${verificationResults.command}] [Result: ${verificationResults.summary}] "${claim}"`;
  } else {
    return `[Verification: ${verificationResults.command}] [Result: ${verificationResults.summary}] "Claim invalid - ${verificationResults.errorMessages.join(', ')}"`;
  }
}

// Example outputs:
// ✅ [npm test] [34/34 tests pass] "All tests pass"
// ❌ [npm run build] [3 compilation errors] "Build fails - missing imports in Component.tsx"
```

**Evidence-Based Reporting:**
- Include verification command executed
- Show actual results (pass/fail counts)
- Provide specific error messages if failed
- Never make claims without fresh evidence

### Step 6: Handle Agent-Delegated Work
**Verify agent completion independently:**

```javascript
// Verify agent work completion
function verifyAgentWork(agentReport, taskRequirements) {
  const independentVerification = {
    vcsChanges: checkGitDiff(agentReport.expectedFiles),
    functionality: testActualBehavior(taskRequirements),
    requirements: verifyAcceptanceCriteria(taskRequirements),
    quality: runQualityChecks()
  };

  return {
    agentReportValid: compareWithIndependentVerification(agentReport, independentVerification),
    evidence: independentVerification,
    discrepancies: findDiscrepancies(agentReport, independentVerification)
  };
}
```

**Agent Verification:**
- Check actual VCS changes (not just agent reports)
- Test actual functionality implemented
- Verify requirements are truly met
- Run independent quality checks

### Step 7: Implement Red-Green Verification for Tests
**Verify regression tests with proper red-green cycle:**

```javascript
// Red-Green verification for regression tests
async function verifyRegressionTest(testCode, originalFailingCode) {
  // 1. Write the test
  writeTestFile(testCode);
  
  // 2. Run with original code (should FAIL)
  const redResult = await runTest();
  if (redResult.success) {
    throw new Error('Test should fail with original code');
  }
  
  // 3. Implement fix
  implementFix(originalFailingCode);
  
  // 4. Run test again (should PASS)
  const greenResult = await runTest();
  if (!greenResult.success) {
    throw new Error('Test should pass with fix implemented');
  }
  
  return {
    verified: true,
    redConfirmed: !redResult.success,
    greenConfirmed: greenResult.success
  };
}
```

**Red-Green Verification:**
- Confirm test fails with original broken code
- Implement minimal fix
- Confirm test passes with fixed code
- Ensures test actually catches the bug

### Step 8: Create Requirements Verification Checklist
**Systematically verify requirements completion:**

```javascript
// Requirements verification checklist
function createRequirementsChecklist(planDocument, implementation) {
  const checklist = planDocument.tasks.map(task => ({
    taskId: task.id,
    description: task.description,
    verificationMethod: determineVerificationMethod(task),
    status: 'pending',
    evidence: null
  }));

  return checklist;
}

// Verify each requirement
async function verifyRequirements(checklist) {
  for (const item of checklist) {
    item.evidence = await executeVerification(item.verificationMethod);
    item.status = item.evidence.success ? 'verified' : 'failed';
  }

  return {
    allMet: checklist.every(item => item.status === 'verified'),
    summary: generateVerificationSummary(checklist),
    gaps: checklist.filter(item => item.status === 'failed')
  };
}
```

**Requirements Verification:**
- Create checklist from plan document
- Verify each requirement systematically
- Provide evidence for each verification
- Report completion status with gaps

### Step 9: Prevent Premature Claims
**Implement verification gates before any success communication:**

```javascript
// Verification gate function
function verificationGate(claim, context) {
  return new Promise((resolve, reject) => {
    // Prevent premature claims
    if (isSuccessClaim(claim) && !hasFreshVerification(context)) {
      reject(new Error('Cannot make success claims without fresh verification'));
    }

    // Require verification for critical actions
    if (isCriticalAction(context.action)) {
      const verification = runVerification(getVerificationCommand(claim));
      if (!verification.success) {
        reject(new Error(`Verification failed: ${verification.errorMessage}`));
      }
    }

    resolve(true);
  });
}

// Critical actions requiring verification
const criticalActions = [
  'commit', 'push', 'create-pr', 'mark-complete',
  'claim-success', 'express-satisfaction', 'delegate-completion'
];
```

**Verification Gates:**
- Block premature success claims
- Require verification for critical actions
- Prevent unverified commits/pushes
- Enforce evidence-based communication

### Step 10: Document Verification Results
**Record verification evidence for audit trail:**

```javascript
// Document verification for audit trail
function documentVerification(claim, verificationResults, context) {
  const verificationRecord = {
    timestamp: new Date().toISOString(),
    claim: claim,
    command: verificationResults.command,
    exitCode: verificationResults.exitCode,
    output: verificationResults.output,
    success: verificationResults.success,
    context: context,
    verifiedBy: 'verification-before-completion-skill'
  };

  // Store in verification log
  appendToVerificationLog(verificationRecord);

  // Include in commit messages if applicable
  if (context.action === 'commit') {
    return `Verification: ${verificationResults.summary}`;
  }

  return verificationRecord;
}
```

**Verification Documentation:**
- Timestamp all verifications
- Record command and results
- Maintain audit trail
- Include in version control history

## Success Criteria

- [ ] Fresh verification command executed before any claims
- [ ] Complete output analyzed (not partial checks)
- [ ] Exit codes verified (0 for success)
- [ ] Failure counts accurately reported
- [ ] Claims match verification evidence exactly
- [ ] Agent work verified independently
- [ ] Red-green cycle completed for regression tests
- [ ] Requirements checklist fully verified
- [ ] No premature success expressions
- [ ] Verification results documented

## Common Pitfalls

1. **Trusting Previous Runs** - Always run fresh verification
2. **Partial Output Reading** - Read complete command output
3. **Ignoring Exit Codes** - Check exit codes, not just output appearance
4. **Agent Report Reliance** - Verify agent work independently
5. **Premature Satisfaction** - Never express success before verification
6. **Confidence-Based Claims** - Evidence required, not confidence
7. **Shortcut Temptation** - No exceptions for "obvious" cases

## Verification Command Reference

### Testing Verification
```bash
# Unit tests
npm test -- --testPathPattern=component.test.js

# Integration tests  
npm run test:integration

# E2E tests
npm run test:e2e

# Specific test file
npm test path/to/specific.test.js
```

### Build Verification
```bash
# Full build
npm run build

# Production build
npm run build:prod

# Type checking
npx tsc --noEmit
```

### Code Quality Verification
```bash
# Linting
npm run lint

# Formatting check
npm run format:check

# Security audit
npm audit
```

### Requirements Verification
```bash
# Manual checklist verification
# (Review plan document against implementation)
```

## Cross-References

### Related Procedures
- [Testing Framework Guide](docs/testing/0000_TESTING_FRAMEWORK.md) - Testing verification methods
- [Error Fixes Summary](docs/error-tracking/0000_ERROR_FIXES_SUMMARY.md) - Common verification failures

### Related Skills
- `testing-verification` - Comprehensive testing strategies
- `systematic-debugging` - Debugging verification failures
- `test-driven-development` - Test-first development with verification

### Related Agents
- `QualityForge_AI_Team` - Verification assistance and quality checks
- `DevForge_AI_Team` - Implementation verification support

## Performance Metrics

- **Application Frequency:** Used in 95% of development tasks
- **Success Rate:** 96% of verifications completed correctly
- **False Claims Prevented:** 85% reduction in unverified success claims
- **Trust Building:** 90% improvement in stakeholder confidence

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
