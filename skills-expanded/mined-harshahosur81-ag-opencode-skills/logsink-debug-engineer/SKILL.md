---
name: logsink-debug-engineer
description: Logsink Degug Workflow skill
category: debugging
tags:
- debugging
- logsink
- debug
---
# Antigravity Debug Skill: Systematic Root Cause Analysis

**Description:** A rigorous, phase-based debugging methodology integrated with automated Google Cloud log extraction. This skill forces evidence-based investigation over guesswork.

## The Four Phases

You MUST complete Phase 0 before starting the investigation.

### Phase 0A: Start Debug Session Logging (Optional but Recommended)

**Initialize structured logging for retrospective analysis:**

If `.debug-logs/helpers/start-debug-session.ps1` exists in the project:

```powershell
# Start a debug session
. .debug-logs/helpers/start-debug-session.ps1 -Issue "Brief issue description" -Revision "revision-name"

# This exports helper functions (use throughout debugging):
Log-Command "command"            # Log to commands-run.txt
Log-Error "error message"        # Log to errors-found.txt  
Log-Fix "solution" -Commit "sha" # Log to fixes-applied.txt
Fetch-CloudLogs -Revision "..."  # Fetch and auto-log Cloud Run logs
End-DebugSession -Resolution "" # Close with summary
```

---

### Phase 0B: Automated Evidence Gathering (Log Sink)

**BEFORE thinking about the bug, get the data:**

This tool automatically connects to the GCP Project defined in your current environment context (GitHub Workflow), uses the active Service Account, and fetches all **Errors/Warnings** from the **last 20 minutes**.

**Prerequisites:**
- Service account needs `roles/logging.viewer` permission
- Grant with: `gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SA_EMAIL" --role="roles/logging.viewer"`

**Execute this block to fetch recent errors/warnings:**

**PowerShell (with auto-logging if debug session active):**

```powershell
$PROJECT_ID = "myproject-agentspace-demo"
$REVISION = "simstream-poster-testing-00214-q8r"  # Update as needed

echo "🔍 Scanning logs for project: $PROJECT_ID (last 20 minutes)"

# If debug session active, use helper (auto-logs to gcloud-logs.txt)
if (Get-Command Fetch-CloudLogs -ErrorAction SilentlyContinue) {
    Fetch-CloudLogs -Revision $REVISION -Severity "ERROR" -Limit 10
} else {
    # Fallback: manual gcloud command
    $filter = "resource.type=cloud_run_revision AND resource.labels.revision_name=$REVISION AND severity>=ERROR"
    gcloud logging read $filter --project=$PROJECT_ID --limit=10 --format=json
}
```

**Bash (original):**

// turbo
```bash
# Get project ID from environment or gcloud config, default to myproject-agentspace-demo
PROJECT_ID=$(gcloud config get-value project 2>/dev/null || echo "${PROJECT_ID:-${GCP_PROJECT:-myproject-agentspace-demo}}")

if [ -z "$PROJECT_ID" ]; then
  echo "❌ Error: Could not detect Project ID from context or environment"
  exit 1
fi

echo "🔍 Scanning logs for project: $PROJECT_ID (last 20 minutes)"
echo ""

# Fetch errors and warnings from last 20 minutes
gcloud logging read \
  'timestamp >= "'$(date -u -d '20 minutes ago' '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u -v-20M '+%Y-%m-%dT%H:%M:%SZ')'" AND severity >= WARNING' \
  --project="$PROJECT_ID" \
  --limit=50 \
  --format="json" \
  --freshness=20m
```

**Alternative (Human-Readable Table Format):**

```bash
gcloud logging read \
  'timestamp >= "'$(date -u -d '20 minutes ago' '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date -u -v-20M '+%Y-%m-%dT%H:%M:%SZ')'" AND severity >= WARNING' \
  --project="$PROJECT_ID" \
  --limit=20 \
  --format="table(timestamp.date('%H:%M:%S'), severity, resource.type, resource.labels.service_name, textPayload.slice(0:100))" \
  --freshness=20m
```

**If you see permission errors**, grant logging access:
```bash
# Replace with your actual service account email
gcloud projects add-iam-policy-binding myproject-agentspace-demo \
  --member="serviceAccount:github-deployer@myproject-agentspace-demo.iam.gserviceaccount.com" \
  --role="roles/logging.viewer"
```

---

### Phase 1: Root Cause Investigation

**Once you have the logs from Phase 0:**

1. **Analyze Phase 0 Output**
   - Look at the `json` output above.
   - **Cluster:** Do you see multiple errors sharing the same `trace` ID?
   - **Timing:** Did the errors start exactly 20 mins ago, or are they sporadic?

2. **Read Error Messages Carefully**
   - Don't skip past errors or warnings found in Phase 0.
   - They often contain the exact solution.
   - Read stack traces completely.
   - Note line numbers, file paths, error codes.

3. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess.

4. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits.
   - New dependencies, config changes.
   - Environmental differences.

5. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets available in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Layer 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Layer 4: Actual signing
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **This reveals:** Which layer fails (secrets → workflow ✓, workflow → build ✗)

6. **Trace Data Flow**

   **WHEN error is deep in call stack:**

   See `root-cause-tracing.md` in this directory for the complete backward tracing technique.

   **Quick version:**
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source.
   - Fix at source, not at symptom.

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase.
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY.
   - Don't skim - read every line.
   - Understand the pattern fully before applying.

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small.
   - Don't assume "that can't matter".

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y".
   - Write it down.
   - Be specific, not vague.

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis.
   - One variable at a time.
   - Don't fix multiple things at once.

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4.
   - Didn't work? Form NEW hypothesis.
   - DON'T add more fixes on top.

4. **When You Don't Know**
   - Say "I don't understand X".
   - Don't pretend to know.
   - Ask for help.
   - Research more.

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   - Simplest possible reproduction.
   - Automated test if possible.
   - One-off test script if no framework.
   - MUST have before fixing.
   - Use the `superpowers:test-driven-development` skill for writing proper failing tests.

2. **Implement Single Fix**
   - Address the root cause identified.
   - ONE change at a time.
   - No "while I'm here" improvements.
   - No bundled refactoring.

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?
   - Issue actually resolved?

4. **If Fix Doesn't Work**
   - STOP.
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1, re-analyze with new information.
   - **If ≥ 3: STOP and question the architecture (step 5 below).**
   - DON'T attempt Fix #4 without architectural discussion.

5. **If 3+ Fixes Failed: Question Architecture**

   **Pattern indicating architectural problem:**
   - Each fix reveals new shared state/coupling/problem in different place.
   - Fixes require "massive refactoring" to implement.
   - Each fix creates new symptoms elsewhere.

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Are we "sticking with it through sheer inertia"?
   - Should we refactor architecture vs. continue fixing symptoms?

   **Discuss with your human partner before attempting more fixes.**

   This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.5)

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Is that not happening?" - You assumed without verifying.
- "Will it show us...?" - You should have added evidence gathering.
- "Stop guessing" - You're proposing fixes without understanding.
- "Ultrathink this" - Question fundamentals, not just symptoms.
- "We're stuck?" (frustrated) - Your approach isn't working.

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **0A. Log Session** | Start debug session (optional) | Logging initialized |
| **0B. Logs** | Run script, find Error/Warning (20m) | Clean evidence list |
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process.
2. Document what you investigated.
3. Implement appropriate handling (retry, timeout, error message).
4. Add monitoring/logging for future investigation.

**But:** 95% of "no root cause" cases are incomplete investigation.

## Supporting Techniques

These techniques are part of systematic debugging and available in this directory:

- **`root-cause-tracing.md`** - Trace bugs backward through call stack to find original trigger
- **`defense-in-depth.md`** - Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** - Replace arbitrary timeouts with condition polling

**Related skills:**
- **superpowers:test-driven-development** - For creating failing test case (Phase 4, Step 1)
- **superpowers:verification-before-completion** - Verify fix worked before claiming success
