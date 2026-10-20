---
name: managing-junit
description: |
  Use when working with Junit — jUnit testing framework management and analysis.
  Covers test suite configuration, XML report parsing, test runner integration,
  assertion pattern review, parameterized test analysis, and build tool
  integration with Maven and Gradle. Use when managing JUnit test suites,
  investigating test failures, or reviewing Java/Kotlin test configurations.
connection_type: junit
preload: false
---

# JUnit Testing Framework Management Skill

Manage and analyze JUnit test suites, reports, and build configurations.

## Core Helper Functions

```bash
#!/bin/bash

# Parse JUnit XML report
junit_parse() {
    local report="$1"
    python3 -c "
import xml.etree.ElementTree as ET, json, sys
tree = ET.parse('$report')
root = tree.getroot()
suites = root.findall('.//testsuite') if root.tag == 'testsuites' else [root]
results = []
for s in suites:
    results.append({
        'name': s.attrib.get('name',''),
        'tests': int(s.attrib.get('tests',0)),
        'failures': int(s.attrib.get('failures',0)),
        'errors': int(s.attrib.get('errors',0)),
        'skipped': int(s.attrib.get('skipped',0)),
        'time': float(s.attrib.get('time',0))
    })
print(json.dumps(results, indent=2))
" 2>/dev/null
}
```

## MANDATORY: Discovery-First Pattern

**Always discover build configuration and test structure before querying specifics.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Build Tool Detection ==="
if [ -f "pom.xml" ]; then
    echo "Build tool: Maven"
    grep -E "<junit.version>|<junit-jupiter.version>|<surefire" pom.xml | head -5
elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
    echo "Build tool: Gradle"
    grep -E "junit|testImplementation|useJUnitPlatform" build.gradle* | head -10
fi

echo ""
echo "=== Test Source Files ==="
find . -path "*/test/java/*.java" -o -path "*/test/kotlin/*.kt" 2>/dev/null | grep -v build | wc -l | xargs echo "Total test files:"
find . -path "*/test/java/*.java" 2>/dev/null | grep -v build | head -15

echo ""
echo "=== JUnit Version Detection ==="
grep -rn "import org.junit.jupiter\|import org.junit.Test\|import org.junit.Assert" --include="*.java" --include="*.kt" 2>/dev/null | grep -v build | head -1 | grep -oP "junit\.(jupiter|Test)" | head -1 | xargs echo "JUnit API:"

echo ""
echo "=== Test Reports ==="
find . -path "*/surefire-reports/*.xml" -o -path "*/test-results/*.xml" 2>/dev/null | grep -v build/resources | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

echo "=== Test Results Summary ==="
REPORTS=$(find . -path "*/surefire-reports/TEST-*.xml" -o -path "*/test-results/test/TEST-*.xml" 2>/dev/null | head -20)
if [ -n "$REPORTS" ]; then
    TOTAL=0; PASS=0; FAIL=0; ERR=0; SKIP=0
    for f in $REPORTS; do
        T=$(grep -oP 'tests="\K[0-9]+' "$f" | head -1)
        F=$(grep -oP 'failures="\K[0-9]+' "$f" | head -1)
        E=$(grep -oP 'errors="\K[0-9]+' "$f" | head -1)
        S=$(grep -oP 'skipped="\K[0-9]+' "$f" | head -1)
        TOTAL=$((TOTAL + ${T:-0})); FAIL=$((FAIL + ${F:-0})); ERR=$((ERR + ${E:-0})); SKIP=$((SKIP + ${S:-0}))
    done
    PASS=$((TOTAL - FAIL - ERR - SKIP))
    echo "Total: $TOTAL | Passed: $PASS | Failed: $FAIL | Errors: $ERR | Skipped: $SKIP"

    echo ""
    echo "=== Failed Tests ==="
    for f in $REPORTS; do
        grep -l 'failures="[1-9]\|errors="[1-9]' "$f" 2>/dev/null
    done | while read f; do
        junit_parse "$f" | python3 -c "import json,sys; [print(f'{s[\"name\"]}: {s[\"failures\"]}F {s[\"errors\"]}E') for s in json.load(sys.stdin) if s['failures']>0 or s['errors']>0]" 2>/dev/null
    done | head -15
fi

echo ""
echo "=== Code Coverage (JaCoCo) ==="
JACOCO=$(find . -path "*/jacoco/test/jacocoTestReport.xml" -o -path "*/site/jacoco/jacoco.xml" 2>/dev/null | head -1)
if [ -n "$JACOCO" ]; then
    grep -oP 'type="LINE".*?missed="\K[0-9]+|covered="\K[0-9]+' "$JACOCO" | head -4
fi
```

## Output Rules
- **TOKEN EFFICIENCY**: Target 50 lines per output
- Parse Surefire/Failsafe XML reports for structured data
- Never dump full stack traces — extract assertion message and location

## Anti-Hallucination Rules
- NEVER guess test class names — always discover via filesystem
- NEVER fabricate test results — parse actual XML reports
- NEVER assume JUnit version — check imports (JUnit 4 vs JUnit 5/Jupiter)

## Safety Rules
- NEVER modify test files without explicit user confirmation
- NEVER delete test reports without user approval
- Be aware that running tests via Maven/Gradle may trigger full builds

## Output Format

Present results as a structured report:
```
Managing Junit Report
═════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

